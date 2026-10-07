"""One-command reproduction: validate → data → experiments → summaries → figures.

Creates ``results/runs/<run_id>/`` (UTC timestamp); never overwrites prior
runs. Refreshes the ``results/{raw,summary,figures,logs}`` latest-copy tree
and ``.run_id`` pointer. Runs pytest (stored to ``logs/test_report.txt``)
and a CLI encrypt/decrypt/verify smoke test. Writes ``environment.json``,
``run_config.json``, and ``EXECUTION_REPORT.md``.
"""

import argparse
import datetime
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def _cpu_model():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def _pkg_versions():
    out = {}
    for mod, dist in (("numpy", "numpy"), ("Crypto", "pycryptodome"),
                      ("psutil", "psutil"), ("matplotlib", "matplotlib"),
                      ("scipy", "scipy"), ("yaml", "pyyaml")):
        try:
            out[dist] = __import__("importlib.metadata").metadata.version(dist)
        except Exception:
            out[dist] = "unknown"
    return out


def _git_commit():
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                           text=True, check=False)
        return r.stdout.strip() if r.returncode == 0 else "uncommitted workspace (no git repo)"
    except Exception:
        return "uncommitted workspace (git unavailable)"


def main(argv=None) -> int:
    """Entry point."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/demo.yaml")
    ap.add_argument("--results", default="results")
    ap.add_argument("--run-id", default=None)
    args = ap.parse_args(argv)
    run_id = args.run_id or datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ")
    run_dir = os.path.join(args.results, "runs", run_id)
    os.makedirs(os.path.join(run_dir, "logs"), exist_ok=True)
    explog = open(os.path.join(run_dir, "logs", "experiment.log"), "a")

    def log(m):
        print(m)
        explog.write(m + "\n")
        explog.flush()

    log(f"run_id={run_id} config={args.config}")
    env = {"PYTHONPATH": os.pathsep.join(["src", os.environ.get("PYTHONPATH", "")])}
    py = sys.executable

    # 1. Validate config + demo data present.
    import yaml

    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    for key in ("warmup_runs", "measured_repetitions", "demo_password",
                "demo_dir", "manifest"):
        assert key in cfg, f"config missing key: {key}"
    assert os.path.exists(cfg["manifest"]), "manifest missing; run generate_demo_data.py"
    log("config validated")

    # 2. Tests.
    t = subprocess.run([py, "-m", "pytest", "tests/", "-q"], capture_output=True,
                       text=True, env={**os.environ, **env})
    with open(os.path.join(run_dir, "logs", "test_report.txt"), "w") as f:
        f.write(t.stdout + "\n" + t.stderr)
    log(f"pytest returncode={t.returncode}")
    log(t.stdout.strip().splitlines()[-1] if t.stdout.strip() else "no pytest output")
    if t.returncode != 0:
        log("TESTS FAILED — aborting experiment run")
        explog.close()
        return 4

    # 3. Experiments.
    steps = [
        ([py, "scripts/run_experiments.py", "--config", args.config,
          "--run-dir", run_dir, "--run-id", run_id], "experiments"),
        ([py, "scripts/summarize_results.py", "--run-dir", run_dir], "summarize"),
        ([py, "scripts/generate_figures.py", "--run-dir", run_dir,
          "--demo-dir", cfg["demo_dir"]], "figures"),
    ]
    for cmd, name in steps:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           env={**os.environ, **env})
        explog.write(f"--- {name} ---\n" + r.stdout + r.stderr + "\n")
        log(f"{name}: returncode={r.returncode}")
        if r.returncode != 0:
            log(f"STEP FAILED: {name}\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
            explog.close()
            return 5

    # 4. CLI smoke test (encrypt → decrypt → verify on DEMO-002).
    import glob as _glob

    demo2 = sorted(_glob.glob(os.path.join(cfg["demo_dir"], "demo_002*")))[0]
    smoke = os.path.join(run_dir, "scratch", "smoke")
    os.makedirs(smoke, exist_ok=True)
    enc = os.path.join(smoke, "tiny.enc")
    dec = os.path.join(smoke, "tiny.dec")
    smoke_env = {**os.environ, **env,
                 "PM_BG_AES_DEMO_PASSWORD": cfg["demo_password"]}
    for cmd in (["-m", "pm_bg_aes.cli", "encrypt", demo2, "-o", enc],
                ["-m", "pm_bg_aes.cli", "decrypt", enc, "-o", dec],
                ["-m", "pm_bg_aes.cli", "verify", demo2, dec]):
        r = subprocess.run([py, *cmd], capture_output=True, text=True, env=smoke_env)
        log(f"cli {' '.join(cmd[1:4])}: rc={r.returncode} {r.stdout.strip()}")
        if r.returncode != 0:
            log(f"CLI SMOKE FAILED: {r.stderr[-1000:]}")
            explog.close()
            return 6

    # 5. Provenance.
    with open(cfg["manifest"]) as f:
        manifest_text = f.read()
    environment = {
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "os": platform.platform(), "architecture": platform.machine(),
        "python": platform.python_version(), "cpu_model": _cpu_model(),
        "logical_cpus": os.cpu_count(), "ram": None,
        "dependencies": _pkg_versions(), "git_commit": _git_commit(),
        "manifest_sha256": hashlib.sha256(manifest_text.encode()).hexdigest(),
        "measurement": "perf_counter incl. file I/O (protocol B); "
                       "time.time probe (protocol A); tracemalloc traced peak; "
                       "psutil cpu sample; warmup excluded from summaries",
    }
    try:
        import psutil

        environment["ram"] = psutil.virtual_memory()._asdict()
    except Exception:
        pass
    with open(os.path.join(run_dir, "raw", "environment.json"), "w") as f:
        json.dump(environment, f, indent=2, default=str)
    with open(os.path.join(run_dir, "raw", "run_config.json"), "w") as f:
        json.dump({"run_id": run_id, "config_path": args.config,
                   "config": cfg,
                   "config_sha256": _sha(args.config)}, f, indent=2)

    # 6. Latest-copy tree.
    for sub in ("raw", "summary", "figures", "logs"):
        dst = os.path.join(args.results, sub)
        if os.path.isdir(dst) and not os.path.islink(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(run_dir, sub), dst,
                        ignore=shutil.ignore_patterns("scratch"))
    with open(os.path.join(args.results, ".run_id"), "w") as f:
        f.write(run_id + "\n")

    # 7. Execution report.
    import csv as _csv

    with open(os.path.join(run_dir, "summary", "performance_summary.csv")) as f:
        perf = list(_csv.DictReader(f))
    with open(os.path.join(run_dir, "summary", "integrity_summary.csv")) as f:
        integ = list(_csv.DictReader(f))
    lines = [f"# Execution report — {run_id}", "",
             "These are new local demonstration measurements, not reproductions",
             "of the manuscript's original numerical results.", "",
             "## Integrity (all datasets must be ok/1)", ""]
    for r in integ:
        lines.append(f"- {r['dataset_id']}: {r['roundtrip_status']} "
                     f"match={r['exact_byte_match']} rate={r['measured_decrypt_match_rate']}")
    lines += ["", "## Throughput means (MiB/s, measured runs)", ""]
    for r in perf:
        lines.append(f"- {r['dataset_id']} {r['phase']}: "
                     f"{float(r['throughput_mean_mib_s']):.2f} "
                     f"(elapsed mean {float(r['elapsed_mean_s']):.4f}s, n={r['n_runs']})")
    lines += ["", f"Environment: {environment['os']} / Python {environment['python']} / "
                   f"{environment['cpu_model']} / {environment['logical_cpus']} CPUs", ""]
    with open(os.path.join(run_dir, "EXECUTION_REPORT.md"), "w") as f:
        f.write("\n".join(lines) + "\n")
    log("report written; run complete")
    explog.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
