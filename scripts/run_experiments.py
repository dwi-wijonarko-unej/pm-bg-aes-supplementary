"""Structured local benchmark (protocol B) + notebook-compatible probe (protocol A).

For every dataset in the manifest, per direction (encrypt/decrypt):
- Protocol A (one probe run): notebook cell-1 boundaries — ``time.time()``
  around read→transform→write, ``tracemalloc`` traced peak, single
  ``psutil`` cpu sample, ``orig_size/1024**2/elapsed`` throughput.
- Protocol B (1 warmup + N measured, ``perf_counter`` including file I/O).

Decrypt input is the ciphertext produced once per dataset (its SHA-256 is
recorded). CSV column ``len_tail`` = AES-tail *input* length (``len_shift``,
residual bytes); ``output_size_bytes`` captures the tail overhead.

Writes ``benchmark_runs.csv`` and ``integrity_checks.csv`` to the run dir.
"""

import argparse
import csv
import json
import os
import shutil
import sys
import time
import tracemalloc

import numpy as np

from pm_bg_aes.crypto import decrypt_bytes, encrypt_bytes
from pm_bg_aes.entropy import shannon_entropy
from pm_bg_aes.file_format import parse_header
from pm_bg_aes.integrity import md5_bytes, sha256_bytes
from pm_bg_aes.metrics import throughput_mib_s

BENCH_COLUMNS = ["run_id", "dataset_id", "phase", "protocol", "repetition",
                 "warmup", "input_size_bytes", "output_size_bytes",
                 "selected_n", "len_hill", "len_tail", "elapsed_seconds",
                 "throughput_mib_s", "traced_peak_bytes", "cpu_percent",
                 "entropy_input", "entropy_output", "sha256_original",
                 "sha256_recovered", "md5_original", "md5_recovered",
                 "exact_byte_match", "status", "error_message",
                                  "sha256_ciphertext"]

INTEG_COLUMNS = ["run_id", "dataset_id", "input_size_bytes",
                 "ciphertext_size_bytes", "recovered_size_bytes", "selected_n",
                 "len_hill", "len_tail", "sha256_original", "sha256_recovered",
                 "md5_original", "md5_recovered", "exact_byte_match", "status",
                                  "sha256_ciphertext", "ciphertext_path"]


def _cpu_sample(process):
    try:
        import psutil

        proc = process or psutil.Process(os.getpid())
        proc.cpu_percent(interval=None)
        return proc, proc.cpu_percent(interval=None)
    except Exception:
        return process, 0.0


def _encrypt_once(plain: bytes, password: str, tmp: str, tag: str,
                  use_perf_counter: bool):
    """One encrypt pass through files (disk I/O included); return metrics."""
    src = os.path.join(tmp, f"{tag}.in")
    dst = os.path.join(tmp, f"{tag}.out")
    with open(src, "wb") as f:
        f.write(plain)
    tracemalloc.start()
    proc = None
    clock = time.perf_counter if use_perf_counter else time.time
    t0 = clock()
    with open(src, "rb") as f:
        blob, n, len_hill, len_shift = encrypt_bytes(f.read(), password)
    with open(dst, "wb") as f:
        f.write(blob)
    elapsed = clock() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    proc, cpu = _cpu_sample(proc)
    with open(dst, "rb") as f:
        cipher = f.read()
    return {"blob": cipher, "n": n, "len_hill": len_hill,
            "len_shift": len_shift, "elapsed": elapsed, "peak": peak,
            "cpu": cpu}


def _decrypt_once(cipher: bytes, password: str, tmp: str, tag: str,
                  use_perf_counter: bool):
    """One decrypt pass through files (disk I/O included); return metrics."""
    src = os.path.join(tmp, f"{tag}.cin")
    dst = os.path.join(tmp, f"{tag}.cout")
    with open(src, "wb") as f:
        f.write(cipher)
    tracemalloc.start()
    proc = None
    clock = time.perf_counter if use_perf_counter else time.time
    t0 = clock()
    with open(src, "rb") as f:
        plain = decrypt_bytes(f.read(), password)
    with open(dst, "wb") as f:
        f.write(plain)
    elapsed = clock() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    proc, cpu = _cpu_sample(proc)
    return {"plain": plain, "elapsed": elapsed, "peak": peak, "cpu": cpu}


def run_dataset(run_id: str, dsid: str, plain: bytes, password: str,
                warmup: int, reps: int, tmp: str,
                bench_rows: list, integ_rows: list, log) -> None:
    """Benchmark one dataset in both directions; append CSV rows."""
    first_row = len(bench_rows)
    ent_in = shannon_entropy(np.frombuffer(plain, dtype=np.uint8)) if plain else 0.0

    # Reference ciphertext for decrypt + dedicated integrity roundtrip.
    ref = _encrypt_once(plain, password, tmp, f"{dsid}-ref", True)
    cipher = ref["blob"]
    n, len_hill = parse_header(cipher)
    rec = _decrypt_once(cipher, password, tmp, f"{dsid}-ref", True)["plain"]
    match = rec == plain
    # Keep the exact reference used for every decrypt, outside excluded scratch.
    retained_dir = os.path.join(os.path.dirname(tmp), "raw", "ciphertexts")
    os.makedirs(retained_dir, exist_ok=True)
    retained_path = os.path.join(retained_dir, f"{dsid}-ref.enc")
    with open(retained_path, "xb") as f:
        f.write(cipher)
    cipher_rel = f"raw/ciphertexts/{dsid}-ref.enc"
    integ_rows.append([run_id, dsid, len(plain), len(cipher), len(rec), n,
                       len_hill, len(plain) - len_hill,
                       sha256_bytes(plain), sha256_bytes(rec),
                       md5_bytes(plain), md5_bytes(rec),
                       int(match), "ok" if match else "MISMATCH",
                       sha256_bytes(cipher), cipher_rel])
    log(f"{dsid}: n={n} len_hill={len_hill} roundtrip={'OK' if match else 'FAIL'}")

    ent_ct = shannon_entropy(np.frombuffer(cipher, dtype=np.uint8))

    # Protocol A probe (notebook boundary): single run each direction.
    for phase, fn, inp, out_ent in (
            ("encrypt", _encrypt_once, plain, None),
            ("decrypt", _decrypt_once, cipher, ent_in)):
        try:
            if phase == "encrypt":
                r = fn(inp, password, tmp, f"{dsid}-A", False)
                out = r["blob"]
                oent = shannon_entropy(np.frombuffer(out, dtype=np.uint8))
                row = [run_id, dsid, phase, "notebook-compatible", 0, True,
                       len(inp), len(out), r["n"], r["len_hill"],
                       r["len_shift"], r["elapsed"],
                       throughput_mib_s(len(inp), r["elapsed"]), r["peak"],
                       r["cpu"], ent_in if phase == "encrypt" else ent_ct,
                       oent, sha256_bytes(plain), "", md5_bytes(plain), "",
                       "", "ok", ""]
            else:
                r = fn(inp, password, tmp, f"{dsid}-A", False)
                rec_ent = shannon_entropy(np.frombuffer(r["plain"], dtype=np.uint8)) if r["plain"] else 0.0
                row = [run_id, dsid, phase, "notebook-compatible", 0, True,
                       len(inp), len(r["plain"]), n, len_hill,
                       len(plain) - len_hill, r["elapsed"],
                       throughput_mib_s(len(inp), r["elapsed"]), r["peak"],
                       r["cpu"], ent_ct, rec_ent,
                       sha256_bytes(plain), sha256_bytes(r["plain"]),
                       md5_bytes(plain), md5_bytes(r["plain"]),
                       int(r["plain"] == plain), "ok", ""]
            row.append(sha256_bytes(out if phase == "encrypt" else cipher))
            bench_rows.append(row)
        except Exception as exc:  # noqa: BLE001 — recorded, not hidden
            bench_rows.append([run_id, dsid, phase, "notebook-compatible", 0,
                               True, len(inp), 0, "", "", "", 0.0, 0.0, 0,
                               0.0, "", "", "", "", "", "", "", "error",
                                                              str(exc).replace(password, "[REDACTED]"), ""])

    # Protocol B: warmup + measured.
    for phase in ("encrypt", "decrypt"):
        for rep in range(warmup + reps):
            is_warm = rep < warmup
            try:
                if phase == "encrypt":
                    r = _encrypt_once(plain, password, tmp, f"{dsid}-B{rep}", True)
                    out = r["blob"]
                    oent = shannon_entropy(np.frombuffer(out, dtype=np.uint8))
                    bench_rows.append(
                        [run_id, dsid, phase, "local-structured", rep,
                         is_warm, len(plain), len(out), r["n"],
                         r["len_hill"], r["len_shift"], r["elapsed"],
                         throughput_mib_s(len(plain), r["elapsed"]),
                         r["peak"], r["cpu"], ent_in, oent,
                         sha256_bytes(plain), "", md5_bytes(plain), "", "",
                         "ok", "", sha256_bytes(out)])
                else:
                    r = _decrypt_once(cipher, password, tmp, f"{dsid}-B{rep}", True)
                    bench_rows.append(
                        [run_id, dsid, phase, "local-structured", rep,
                         is_warm, len(cipher), len(r["plain"]), n, len_hill,
                         len(plain) - len_hill, r["elapsed"],
                         throughput_mib_s(len(cipher), r["elapsed"]),
                         r["peak"], r["cpu"], ent_ct,
                         shannon_entropy(np.frombuffer(r["plain"], dtype=np.uint8)),
                         sha256_bytes(plain), sha256_bytes(r["plain"]),
                         md5_bytes(plain), md5_bytes(r["plain"]),
                         int(r["plain"] == plain), "ok", "", sha256_bytes(cipher)])
            except Exception as exc:  # noqa: BLE001
                bench_rows.append([run_id, dsid, phase, "local-structured",
                                   rep, is_warm, 0, 0, "", "", "", 0.0, 0.0,
                                   0, 0.0, "", "", "", "", "", "", "",
                                   "error", str(exc).replace(password, "[REDACTED]"), ""])

    if not match or any(row[BENCH_COLUMNS.index("status")] != "ok"
                        or (row[2] == "decrypt"
                            and row[BENCH_COLUMNS.index("exact_byte_match")] != 1)
                        for row in bench_rows[first_row:]):
        log(f"{dsid}: benchmark/integrity failure recorded")


def load_manifest(manifest_path: str, demo_dir: str) -> list:
    """Validate all manifest bytes before returning any benchmark inputs."""
    import csv as _csv

    items = []
    seen = set()
    with open(manifest_path, newline="", encoding="utf-8") as f:
        for row in _csv.DictReader(f):
            dsid, filename = row["dataset_id"], row["filename"]
            if (dsid in seen or not dsid.startswith("DEMO-")
                    or not dsid[5:].isdigit()
                    or os.path.basename(filename) != filename
                    or "/" in filename or "\\" in filename):
                raise ValueError(f"invalid/duplicate manifest dataset: {dsid}")
            if (row.get("source_type") != "synthetic"
                    or row.get("redistribution_allowed", "").lower() != "yes"):
                raise ValueError(f"only redistributable synthetic demos allowed: {dsid}")
            seen.add(dsid)
            p = os.path.join(demo_dir, filename)
            with open(p, "rb") as fh:
                blob = fh.read()
            if (len(blob) != int(row["size_bytes"])
                    or sha256_bytes(blob) != row["sha256"]
                    or md5_bytes(blob) != row["md5"]):
                raise ValueError(f"manifest size/hash mismatch: {dsid} ({p})")
            items.append((dsid, blob))
    if not items:
        raise ValueError("manifest contains no datasets")
    return items


def main(argv=None) -> int:
    """Entry point (also importable by reproduce_all)."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/demo.yaml")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args(argv)

    import yaml

    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    # Validate before timing or creating reference artifacts, including direct use.
    items = load_manifest(cfg["manifest"], cfg["demo_dir"])
    for name in ("benchmark_runs.csv", "integrity_checks.csv", "ciphertexts"):
        if os.path.lexists(os.path.join(args.run_dir, "raw", name)):
            raise FileExistsError(f"refusing to overwrite existing raw artifact: {name}")
    os.makedirs(os.path.join(args.run_dir, "raw"), exist_ok=True)
    shutil.copyfile(cfg["manifest"], os.path.join(args.run_dir, "raw", "dataset_manifest.csv"))
    tmp = os.path.join(args.run_dir, "scratch")
    os.makedirs(tmp, exist_ok=True)
    log_path = os.path.join(args.run_dir, "logs", "experiment.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logf = open(log_path, "a")
    log = lambda m: (print(m), logf.write(m + "\n"), logf.flush())

    bench_rows, integ_rows = [], []
    for dsid, plain in items:
        run_dataset(run_id=args.run_id, dsid=dsid, plain=plain,
                    password=cfg["demo_password"],
                    warmup=int(cfg.get("warmup_runs", 1)),
                    reps=int(cfg.get("measured_repetitions", 5)),
                    tmp=tmp, bench_rows=bench_rows, integ_rows=integ_rows,
                    log=log)
    with open(os.path.join(args.run_dir, "raw", "benchmark_runs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(BENCH_COLUMNS)
        w.writerows(bench_rows)
    with open(os.path.join(args.run_dir, "raw", "integrity_checks.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(INTEG_COLUMNS)
        w.writerows(integ_rows)
    log(f"wrote {len(bench_rows)} benchmark rows, {len(integ_rows)} integrity rows")
    logf.close()
    failed = any(row[BENCH_COLUMNS.index("status")] != "ok"
                 or (row[2] == "decrypt"
                     and row[BENCH_COLUMNS.index("exact_byte_match")] != 1)
                 for row in bench_rows)
    return 2 if failed or any(row[13] != "ok" for row in integ_rows) else 0


if __name__ == "__main__":
    sys.exit(main())
