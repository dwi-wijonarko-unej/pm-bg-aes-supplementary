"""Small synthetic fixtures only: never launch the full reproduction pipeline."""

import csv
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]


def _script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _digest(blob):
    return hashlib.sha256(blob).hexdigest()


def _manifest(path, demo_dir, entries):
    columns = ["dataset_id", "filename", "size_bytes", "sha256", "md5",
               "source_type", "redistribution_allowed"]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for dsid, filename, blob in entries:
            (demo_dir / filename).write_bytes(blob)
            writer.writerow({"dataset_id": dsid, "filename": filename,
                             "size_bytes": len(blob), "sha256": _digest(blob),
                             "md5": hashlib.md5(blob).hexdigest(),
                             "source_type": "synthetic", "redistribution_allowed": "yes"})


def test_existing_run_rejected_without_touching_files(tmp_path, monkeypatch):
    reproduce = _script("reproduce_all")
    results = tmp_path / "results"
    previous = results / "runs" / "already-used"
    previous.mkdir(parents=True)
    marker = previous / "keep.txt"
    marker.write_text("previous run")
    monkeypatch.setattr(reproduce, "_git_state", lambda _: pytest.fail("must reject before provenance"))
    assert reproduce.main(["--results", str(results), "--run-id", "already-used"]) == 2
    assert marker.read_text() == "previous run"
    assert list(previous.iterdir()) == [marker]


def test_manifest_hash_mismatch_blocks_benchmark(tmp_path, monkeypatch):
    experiments = _script("run_experiments")
    demo = tmp_path / "demo"
    demo.mkdir()
    manifest = tmp_path / "manifest.csv"
    _manifest(manifest, demo, [("DEMO-002", "tiny.bin", b"abc")])
    (demo / "tiny.bin").write_bytes(b"abd")  # Same size, different hash.
    config = tmp_path / "demo.yaml"
    config.write_text(f"manifest: {manifest.as_posix()}\ndemo_dir: {demo.as_posix()}\n"
                      "demo_password: PMBG-AES-DEMO-2026\nwarmup_runs: 1\nmeasured_repetitions: 5\n")
    monkeypatch.setattr(experiments, "run_dataset", lambda **_: pytest.fail("must not benchmark"))
    with pytest.raises(ValueError, match="manifest size/hash mismatch"):
        experiments.main(["--config", str(config), "--run-dir", str(tmp_path / "run"),
                          "--run-id", "test"])
    assert not (tmp_path / "run").exists()


@pytest.fixture
def retained_run(tmp_path):
    experiments = _script("run_experiments")
    demo, run = tmp_path / "demo", tmp_path / "run"
    demo.mkdir()
    (run / "raw").mkdir(parents=True)
    scratch = run / "scratch"
    scratch.mkdir()
    entries = [("DEMO-004", "structured.txt", b"record=synthetic;\n" * 8),
               ("DEMO-005", "random.bin", bytes(range(256)) + b"tail!")]
    manifest = run / "raw" / "dataset_manifest.csv"
    _manifest(manifest, demo, entries)
    assert experiments.load_manifest(str(manifest), str(demo)) == [(d, b) for d, _, b in entries]
    bench, integ = [], []
    for dsid, _, blob in entries:
        experiments.run_dataset("fixture", dsid, blob, "PMBG-AES-DEMO-2026", 1, 5,
                                str(scratch), bench, integ, lambda _: None)
    assert all(len(r) == len(experiments.BENCH_COLUMNS) for r in bench)
    assert all(len(r) == len(experiments.INTEG_COLUMNS) for r in integ)
    for filename, columns, rows in (("benchmark_runs.csv", experiments.BENCH_COLUMNS, bench),
                                    ("integrity_checks.csv", experiments.INTEG_COLUMNS, integ)):
        with (run / "raw" / filename).open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
    return run, demo


def test_figures_use_retained_reference_and_record_derivation(retained_run, monkeypatch):
    run, demo = retained_run
    figures = _script("generate_figures")
    import pm_bg_aes.crypto as crypto
    monkeypatch.setattr(crypto, "encrypt_bytes", lambda *_: pytest.fail("figures must never encrypt"))
    assert figures.main(["--run-dir", str(run), "--demo-dir", str(demo)]) == 0
    derivation = json.loads((run / "figures" / "figure_derivation.json").read_text())
    with (run / "figures" / "figure_manifest.csv").open(newline="") as f:
        manifest = list(csv.DictReader(f))
    assert len(manifest) == 10
    for row in manifest:
        assert row["run_id"] == "fixture"
        assert row["figure_sha256"] == _digest((run / row["file_path"]).read_bytes())
        assert row["derivation_sha256"] == _digest((run / row["derivation_path"]).read_bytes())
        assert "<run>" not in row["command"] and str(run) in row["command"]
    for dsid, figure_id in (("DEMO-005", "demo-hist-DEMO-005"),
                            ("DEMO-004", "demo-scatter-DEMO-004")):
        metadata = derivation["figures"][figure_id]
        retained = (run / metadata["ciphertext_path"]).read_bytes()
        assert retained == (run / "scratch" / f"{dsid}-ref.out").read_bytes()
        assert metadata["ciphertext_sha256"] == _digest(retained)
        assert metadata["original_sha256"] == _digest(Path(metadata["original_path"]).read_bytes())
    hist = derivation["figures"]["demo-hist-DEMO-005"]
    cipher = (run / hist["ciphertext_path"]).read_bytes()
    assert hist["histogram_ciphertext_counts"] == np.bincount(
        np.frombuffer(cipher, dtype=np.uint8), minlength=256).tolist()
    scatter = derivation["figures"]["demo-scatter-DEMO-004"]
    for prefix in ("original", "ciphertext"):
        size = scatter[f"{prefix}_size_bytes"]
        expected = np.linspace(0, size - 2, min(4000, size - 1)).astype(int).tolist()
        assert scatter[f"sampled_{prefix}_positions"] == expected
    # Artifact inputs remain usable even when excluded scratch is gone.
    import shutil
    shutil.rmtree(run / "scratch")
    rows, integ = figures._load(str(run))
    figures._reference_inputs(str(run), str(demo), "DEMO-004", rows, integ)


def test_tampered_retained_ciphertext_is_rejected(retained_run):
    run, demo = retained_run
    figures = _script("generate_figures")
    rows, integ = figures._load(str(run))
    path = run / integ["DEMO-005"]["ciphertext_path"]
    cipher = path.read_bytes()
    path.write_bytes(bytes([cipher[0] ^ 1]) + cipher[1:])
    with pytest.raises(ValueError, match="retained figure input"):
        figures._reference_inputs(str(run), str(demo), "DEMO-005", rows, integ)


def test_summary_requires_complete_raw_measurements(retained_run):
    run, _ = retained_run
    summaries = _script("summarize_results")
    assert summaries.main(["--run-dir", str(run)]) == 0
    with (run / "summary" / "performance_summary.csv").open(newline="") as f:
        performance = list(csv.DictReader(f))
    assert len(performance) == 4 and all(r["n_runs"] == "5" for r in performance)
    with (run / "raw" / "benchmark_runs.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))
    with (run / "raw" / "integrity_checks.csv").open(newline="") as f:
        integ = list(csv.DictReader(f))
    summaries._validate_raw(rows, integ)
    with pytest.raises(ValueError, match="incomplete measurement plan"):
        summaries._validate_raw(rows[:-1], integ)
    rows[-1]["exact_byte_match"] = "0"
    with pytest.raises(ValueError, match="raw measurement/integrity failure"):
        summaries._validate_raw(rows, integ)


def test_exception_rows_preserve_extended_schema(tmp_path, monkeypatch):
    experiments = _script("run_experiments")
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    original_encrypt = experiments._encrypt_once
    original_decrypt = experiments._decrypt_once
    def encrypt(plain, password, tmp, tag, counter):
        if not tag.endswith("-ref"):
            raise ValueError(f"failure {password}")
        return original_encrypt(plain, password, tmp, tag, counter)
    def decrypt(cipher, password, tmp, tag, counter):
        if not tag.endswith("-ref"):
            raise ValueError(f"failure {password}")
        return original_decrypt(cipher, password, tmp, tag, counter)
    monkeypatch.setattr(experiments, "_encrypt_once", encrypt)
    monkeypatch.setattr(experiments, "_decrypt_once", decrypt)
    bench, integ = [], []
    experiments.run_dataset("fixture", "DEMO-002", b"tiny", "private-password", 1, 5,
                            str(scratch), bench, integ, lambda _: None)
    assert len(bench) == 14
    assert all(len(row) == len(experiments.BENCH_COLUMNS) for row in bench)
    assert all("private-password" not in str(row) for row in bench)
    assert all(row[experiments.BENCH_COLUMNS.index("status")] == "error" for row in bench)
