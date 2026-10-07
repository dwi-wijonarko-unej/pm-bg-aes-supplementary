"""Aggregate raw benchmark/integrity CSVs into summary CSVs (warmup excluded).

``performance_summary.csv`` columns: run_id, dataset_id, phase, n_runs,
elapsed_{mean,median,stdev(sample, n>=2 else 0.0),min,max},
throughput_mib_s_{mean,median,stdev,min,max}. No confidence intervals.
``integrity_summary.csv``: per-dataset roundtrip status (from the dedicated
integrity rows) plus measured-run match rate.
"""

import argparse
import csv
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

    with open(os.path.join(raw, "integrity_checks.csv")) as f:
        integ = list(csv.DictReader(f))
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
    print(f"summarized {len(groups)} (dataset, phase) groups")
    return 0


if __name__ == "__main__":
    sys.exit(main())
