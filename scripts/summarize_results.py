"""Aggregate raw benchmark/integrity CSVs into summary CSVs (warmup excluded).

``performance_summary.csv`` columns: run_id, dataset_id, phase, n_runs,
elapsed_{mean,median,stdev(sample, n>=2 else 0.0),min,max},
throughput_mib_s_{mean,median,stdev,min,max}. No confidence intervals.
``integrity_summary.csv``: per-dataset roundtrip status (from the dedicated
integrity rows) plus measured-run match rate.
"""

import argparse
import csv
import hashlib
import json
import os
import statistics
import sys


def _stats(vals):
    vals = [float(v) for v in vals]
    if not vals:
        return {"n": 0, "mean": "", "median": "", "stdev": "", "min": "", "max": ""}
    return {"n": len(vals), "mean": statistics.mean(vals),
            "median": statistics.median(vals),
            "stdev": statistics.stdev(vals) if len(vals) >= 2 else 0.0,
            "min": min(vals), "max": max(vals)}


def _validate_raw(rows, integ, warmup=1, repetitions=5):
    """Never report a partial/failed benchmark as successful measured results."""
    if not rows or not integ:
        raise ValueError("raw benchmark/integrity data is empty")
    run_ids = {r["run_id"] for r in rows + integ}
    if len(run_ids) != 1:
        raise ValueError("mixed run IDs in raw data")
    refs = {r["dataset_id"]: r for r in integ}
    if len(refs) != len(integ) or set(refs) != {r["dataset_id"] for r in rows}:
        raise ValueError("raw dataset IDs do not match integrity records")
    for dsid, ref in refs.items():
        if (ref["status"] != "ok" or ref["exact_byte_match"] != "1"
                or ref["sha256_original"] != ref["sha256_recovered"]):
            raise ValueError(f"reference roundtrip failed: {dsid}")
        for phase in ("encrypt", "decrypt"):
            group = [r for r in rows if r["dataset_id"] == dsid and r["phase"] == phase]
            local = [r for r in group if r["protocol"] == "local-structured"]
            probe = [r for r in group if r["protocol"] == "notebook-compatible"]
            if (len(group) != warmup + repetitions + 1 or len(probe) != 1
                    or len(local) != warmup + repetitions
                    or sorted(int(r["repetition"]) for r in local) != list(range(warmup + repetitions))
                    or any((str(r["warmup"]).lower() == "true") != (int(r["repetition"]) < warmup)
                           for r in local)):
                raise ValueError(f"incomplete measurement plan: {dsid} {phase}")
            for r in group:
                if (r["status"] != "ok" or not r.get("sha256_ciphertext")
                        or r["sha256_original"] != ref["sha256_original"]
                        or (phase == "decrypt" and (
                            r["exact_byte_match"] != "1"
                            or r["sha256_recovered"] != ref["sha256_original"]
                            or r["sha256_ciphertext"] != ref["sha256_ciphertext"]))):
                    raise ValueError(f"raw measurement/integrity failure: {dsid} {phase}")


def main(argv=None) -> int:
    """Entry point."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args(argv)
    raw = os.path.join(args.run_dir, "raw")
    summary = os.path.join(args.run_dir, "summary")
    os.makedirs(summary, exist_ok=True)

    with open(os.path.join(raw, "benchmark_runs.csv")) as f:
        rows = list(csv.DictReader(f))
    with open(os.path.join(raw, "integrity_checks.csv")) as f:
        integ = list(csv.DictReader(f))
    config_path = os.path.join(raw, "run_config.json")
    cfg = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            cfg = json.load(f)["config"]
    _validate_raw(rows, integ, int(cfg.get("warmup_runs", 1)),
                  int(cfg.get("measured_repetitions", 5)))
    measured = [r for r in rows
                if r["protocol"] == "local-structured"
                and str(r["warmup"]).lower() in ("false", "0", "")
                and r["status"] == "ok"]

    groups = {}
    for r in measured:
        groups.setdefault((r["dataset_id"], r["phase"]),
                          {"el": [], "tp": []})
        groups[(r["dataset_id"], r["phase"])]["el"].append(float(r["elapsed_seconds"]))
        groups[(r["dataset_id"], r["phase"])]["tp"].append(float(r["throughput_mib_s"]))

    with open(os.path.join(summary, "performance_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run_id", "dataset_id", "phase", "n_runs",
                    "elapsed_mean_s", "elapsed_median_s", "elapsed_stdev_s",
                    "elapsed_min_s", "elapsed_max_s", "throughput_mean_mib_s",
                    "throughput_median_mib_s", "throughput_stdev_mib_s",
                    "throughput_min_mib_s", "throughput_max_mib_s"])
        for (dsid, phase), g in sorted(groups.items()):
            se, st = _stats(g["el"]), _stats(g["tp"])
            w.writerow([rows[0]["run_id"] if rows else "", dsid, phase, se["n"],
                        se["mean"], se["median"], se["stdev"], se["min"], se["max"],
                        st["mean"], st["median"], st["stdev"], st["min"], st["max"]])

    match_rate = {}
    for r in measured:
        k = r["dataset_id"]
        match_rate.setdefault(k, [])
        if r["phase"] == "decrypt":
            match_rate[k].append(int(r["exact_byte_match"]))
    with open(os.path.join(summary, "integrity_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run_id", "dataset_id", "roundtrip_status",
                    "exact_byte_match", "measured_decrypt_match_rate",
                    "sha256_original", "sha256_recovered"])
        for r in integ:
            mr = match_rate.get(r["dataset_id"], [])
            rate = (sum(mr) / len(mr)) if mr else ""
            w.writerow([r["run_id"], r["dataset_id"], r["status"],
                        r["exact_byte_match"], rate, r["sha256_original"],
                        r["sha256_recovered"]])
    def digest(path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    with open(os.path.join(summary, "summary_manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"run_id": rows[0]["run_id"],
                   "source_sha256": {f"raw/{name}": digest(os.path.join(raw, name))
                                     for name in ("benchmark_runs.csv", "integrity_checks.csv")},
                   "output_sha256": {f"summary/{name}": digest(os.path.join(summary, name))
                                     for name in ("performance_summary.csv", "integrity_summary.csv")},
                   "filter": "local-structured; warmup=false; status=ok",
                   "expected_measured_repetitions": int(cfg.get("measured_repetitions", 5)),
                   "statistics": "arithmetic mean, median, sample stdev (n>=2), min, max",
                   "validation": "complete plan; all reference and measured decrypt byte/hash matches"},
                  f, indent=2)
    print(f"summarized {len(groups)} (dataset, phase) groups")
    return 0


if __name__ == "__main__":
    sys.exit(main())
