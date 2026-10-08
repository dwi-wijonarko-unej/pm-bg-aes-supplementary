"""Validate demos, test, benchmark, summarize and plot in a new immutable run ID.

Provenance describes the executed workspace (including dirty state), not a
claim that the candidate version is a clean release commit. Failed runs keep
logs, environment, configuration and actual command exit codes.
"""

import argparse
import csv
import datetime
import hashlib
import importlib.metadata
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

PUBLIC_DEMO_PASSWORD = "PMBG-AES-DEMO-2026"


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def _json(path, value):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, default=str)
        f.write("\n")


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
    for dist in ("numpy", "pycryptodome", "psutil", "matplotlib", "scipy",
                 "PyYAML", "pytest", "pm-bg-aes"):
        try:
            out[dist] = importlib.metadata.version(dist)
        except importlib.metadata.PackageNotFoundError:
            out[dist] = "not installed as a distribution"
    return out


def _git_state(commands):
    """Read baseline before creating outputs; do not modify Git or use remotes."""
    def read(args):
        cmd = ["git", "--no-optional-locks", "--no-pager", *args]
        record = {"step": "git provenance", "argv": cmd, "cwd": os.getcwd(),
                  "started_at_utc": _utc()}
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, check=False)
            record.update(exit_code=r.returncode, finished_at_utc=_utc())
            commands.append(record)
            return r.stdout if r.returncode == 0 else None
        except OSError as exc:
            record.update(exit_code=None, error=str(exc), finished_at_utc=_utc())
            commands.append(record)
            return None

    commit = read(["rev-parse", "HEAD"])
    status = read(["status", "--porcelain=v1", "--untracked-files=all"])
    diff = read(["diff", "--binary", "HEAD", "--"])
    return {"baseline_commit": commit.strip() if commit else None,
            "dirty": bool(status) if status is not None else None,
            "status_porcelain": status.splitlines() if status is not None else None,
            "tracked_diff_sha256": hashlib.sha256(diff.encode()).hexdigest()
            if diff is not None else None,
            "captured_at_utc": _utc(),
            "interpretation": "baseline plus executed workspace changes; not a clean candidate commit"}


def _source_hashes():
    paths = []
    for directory in ("scripts", "src", "tests"):
        paths.extend(Path(directory).rglob("*.py"))
    paths.extend(Path("notebooks/original").glob("*.ipynb"))
    paths.extend(Path(name) for name in ("pyproject.toml", "requirements.txt",
                                        "requirements-lock.txt") if Path(name).is_file())
    return {p.as_posix(): _sha(p) for p in sorted(paths)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/demo.yaml")
    ap.add_argument("--results", default="results")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--candidate-version", default="1.0.0")
    args = ap.parse_args(argv)
    run_id = args.run_id or datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ")
    if (run_id in (".", "..") or not run_id or "/" in run_id or "\\" in run_id
            or os.path.basename(run_id) != run_id):
        ap.error("run-id must be a single directory name")
    run_dir = Path(args.results) / "runs" / run_id
    if os.path.lexists(run_dir):
        print(f"refusing to overwrite existing run directory: {run_dir}", file=sys.stderr)
        return 2

    started = _utc()
    commands = []
    git_state = _git_state(commands)
    # exist_ok=False is the atomic overwrite guard, including concurrent runs.
    run_dir.parent.mkdir(parents=True, exist_ok=True)
    try:
        run_dir.mkdir(exist_ok=False)
    except FileExistsError:
        print(f"refusing to overwrite existing run directory: {run_dir}", file=sys.stderr)
        return 2
    for sub in ("raw", "logs"):
        (run_dir / sub).mkdir()
    py = sys.executable
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([
        str(Path("src").resolve()), os.environ.get("PYTHONPATH", "")])}
    environment = {
        "run_id": run_id, "candidate_version": args.candidate_version,
        "timestamp_utc": started, "started_at_utc": started,
        "os": platform.platform(), "architecture": platform.machine(),
        "python": platform.python_version(), "python_full": sys.version,
        "python_executable": py, "python_prefix": sys.prefix,
        "python_base_prefix": sys.base_prefix, "cwd": os.getcwd(),
        "cpu_model": _cpu_model(), "logical_cpus": os.cpu_count(),
        "physical_cpus": None, "ram": None, "dependencies": _pkg_versions(),
        "installed_distributions": dict(sorted(
            (d.metadata["Name"], d.version) for d in importlib.metadata.distributions()
            if d.metadata["Name"])),
        "git_commit": git_state["baseline_commit"], "git_dirty": git_state["dirty"],
        "git": git_state, "source_sha256": _source_hashes(),
        "measurement": {
            "protocol_B": "perf_counter read/transform/write; input staging excluded; warmup excluded",
            "protocol_A": "time.time read/transform/write; separate notebook-compatible probe",
            "memory": "tracemalloc peak traced Python allocations, not RSS",
            "cpu": "two immediate psutil cpu_percent(interval=None) calls after timing; usually zero; not operation utilization",
            "randomness": "synthetic input seeds in dataset manifest; production AES IVs remain random",
        },
    }
    try:
        import psutil
        environment["ram"] = psutil.virtual_memory()._asdict()
        environment["physical_cpus"] = psutil.cpu_count(logical=False)
    except Exception as exc:
        environment["hardware_probe_error"] = str(exc)
    _json(run_dir / "raw" / "environment.json", environment)
    _json(run_dir / "raw" / "commands.json", commands)
    password = ""
    failure = None
    code = 1
    explog = open(run_dir / "logs" / "experiment.log", "a", encoding="utf-8")

    def redact(text):
        if password and password != PUBLIC_DEMO_PASSWORD:
            return text.replace(password, "[REDACTED]")
        return text

    def log(text):
        text = redact(text)
        print(text)
        explog.write(text + "\n")
        explog.flush()

    def execute(cmd, name, child_env=None):
        record = {"step": name, "argv": cmd, "command": shlex.join(cmd),
                  "cwd": os.getcwd(), "started_at_utc": _utc(), "exit_code": None,
                  "log_path": f"logs/{name}.txt"}
        commands.append(record)
        _json(run_dir / "raw" / "commands.json", commands)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               env=child_env or env, check=False)
        except OSError as exc:
            record.update(error=redact(str(exc)), finished_at_utc=_utc())
            _json(run_dir / "raw" / "commands.json", commands)
            raise
        record.update(exit_code=r.returncode, finished_at_utc=_utc())
        output = redact(r.stdout + "\n" + r.stderr)
        with open(run_dir / record["log_path"], "w", encoding="utf-8") as f:
            f.write(output)
        _json(run_dir / "raw" / "commands.json", commands)
        log(f"{name}: exit_code={r.returncode} command={shlex.join(cmd)}")
        if r.returncode:
            log(output[-3000:])
        return r.returncode

    try:
        import yaml
        with open(args.config, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        for key in ("warmup_runs", "measured_repetitions", "demo_password", "demo_dir", "manifest"):
            if key not in cfg:
                raise ValueError(f"config missing key: {key}")
        password = cfg["demo_password"]
        if not isinstance(password, str) or not password:
            raise ValueError("demo_password must be a nonempty string")
        if int(cfg["warmup_runs"]) != 1 or int(cfg["measured_repetitions"]) != 5:
            raise ValueError("demo requires 1 warmup and 5 measured repetitions")
        safe_cfg = dict(cfg)
        if password != PUBLIC_DEMO_PASSWORD:
            safe_cfg["demo_password"] = "[REDACTED]"
        _json(run_dir / "raw" / "run_config.json", {
            "run_id": run_id, "candidate_version": args.candidate_version,
            "started_at_utc": started, "config_path": args.config,
            "config": safe_cfg, "config_sha256": _sha(args.config),
            "invocation": [py, "scripts/reproduce_all.py", *(sys.argv[1:] if argv is None else argv)],
        })
        # Import the same validator used by standalone experiments.
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        sys.path.insert(0, str(Path("src").resolve()))
        from run_experiments import load_manifest
        datasets = load_manifest(cfg["manifest"], cfg["demo_dir"])
        if {d for d, _ in datasets} != {f"DEMO-{i:03d}" for i in range(1, 12)}:
            raise ValueError("demo manifest must contain exactly DEMO-001 through DEMO-011")
        environment["manifest_sha256"] = _sha(cfg["manifest"])
        environment["manifest_validation"] = {
            "status": "passed", "validated_at_utc": _utc(), "dataset_count": len(datasets),
            "checks": ["size_bytes", "sha256", "md5", "unique IDs", "synthetic redistribution"],
        }
        _json(run_dir / "raw" / "environment.json", environment)
        log(f"run_id={run_id}; manifest validated; candidate={args.candidate_version}; "
            f"baseline={git_state['baseline_commit']}; dirty={git_state['dirty']}")
        if execute([py, "-m", "pytest", "tests/", "-q"], "test_report"):
            code = 4
            raise RuntimeError("tests failed; benchmarks not started")
        steps = [
            ([py, "scripts/run_experiments.py", "--config", args.config,
              "--run-dir", str(run_dir), "--run-id", run_id], "experiments"),
            ([py, "scripts/summarize_results.py", "--run-dir", str(run_dir)], "summarize"),
            ([py, "scripts/generate_figures.py", "--run-dir", str(run_dir),
              "--demo-dir", cfg["demo_dir"]], "figures"),
        ]
        for cmd, name in steps:
            if execute(cmd, name):
                code = 5
                raise RuntimeError(f"step failed: {name}")
        with open(cfg["manifest"], newline="") as f:
            demo2 = next(r for r in csv.DictReader(f) if r["dataset_id"] == "DEMO-002")
        original = os.path.join(cfg["demo_dir"], demo2["filename"])
        smoke = run_dir / "scratch" / "smoke"
        smoke.mkdir(parents=True)
        enc, dec = str(smoke / "tiny.enc"), str(smoke / "tiny.dec")
        smoke_env = {**env, "PM_BG_AES_DEMO_PASSWORD": password}
        for name, cmd in (
                ("cli_encrypt", ["encrypt", original, "-o", enc]),
                ("cli_decrypt", ["decrypt", enc, "-o", dec]),
                ("cli_verify", ["verify", original, dec])):
            if execute([py, "-m", "pm_bg_aes.cli", *cmd], name, smoke_env):
                code = 6
                raise RuntimeError(f"CLI smoke failed: {name}")
        code = 0
    except Exception as exc:
        failure = redact(f"{type(exc).__name__}: {exc}")
        log(f"RUN FAILED: {failure}")
    finally:
        environment.update(finished_at_utc=_utc(), exit_code=code,
                           status="completed" if code == 0 else "failed", failure=failure)
        _json(run_dir / "raw" / "environment.json", environment)
        _json(run_dir / "raw" / "commands.json", commands)
        lines = [f"# Execution report — {run_id}", "",
                 "New local synthetic demonstration measurements, not the manuscript's original results.", "",
                 f"Candidate version: {args.candidate_version}",
                 f"Baseline commit: {git_state['baseline_commit']}; workspace dirty: {git_state['dirty']}",
                 "The baseline is not a claim of a clean candidate release commit.",
                 f"Started: {started}; finished: {environment['finished_at_utc']}",
                 f"Status: {environment['status']}; exit code: {code}",
                 f"Failure: {failure or 'none'}", "", "## Actual commands and exit codes", ""]
        for r in commands:
            lines.append(f"- `{shlex.join(r['argv'])}`: exit_code={r['exit_code']}")
        for filename, heading in (("integrity_summary.csv", "Integrity"),
                                  ("performance_summary.csv", "Measured performance")):
            path = run_dir / "summary" / filename
            if path.exists():
                lines.extend(["", f"## {heading}", ""])
                with open(path, newline="") as f:
                    for row in csv.DictReader(f):
                        lines.append("- " + "; ".join(f"{k}={v}" for k, v in row.items()))
        lines.extend(["", f"Environment: {environment['os']} / Python {environment['python']} / "
                      f"{environment['cpu_model']} / {environment['logical_cpus']} logical CPUs",
                      f"RAM total bytes: {(environment['ram'] or {}).get('total', 'unknown')}",
                      "CPU samples are immediate post-operation probes, not operation utilization.", ""])
        with open(run_dir / "EXECUTION_REPORT.md", "w", encoding="utf-8") as f:
            f.write(redact("\n".join(lines)))
        log("report written; run " + environment["status"])
        explog.close()

    if code == 0:
        # Refresh only the explicit latest-copy tree; previous runs remain intact.
        for sub in ("raw", "summary", "figures", "logs"):
            dst = Path(args.results) / sub
            if dst.is_symlink():
                dst.unlink()
            elif dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(run_dir / sub, dst)
        with open(Path(args.results) / ".run_id", "w", encoding="utf-8") as f:
            f.write(run_id + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
