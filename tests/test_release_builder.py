"""Release tests use only tiny temporary fixtures, never repository payloads."""

import csv
import importlib.util
import io
import json
import stat
import zipfile
from pathlib import Path

import pytest
import yaml

SPEC = importlib.util.spec_from_file_location(
    "release_builder", Path(__file__).resolve().parents[1] / "scripts" / "build_release.py"
)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


def put(root, rel, data=b"fixture\n"):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
    return path


def csv_bytes(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def write_policy(root, policy):
    put(root, builder.DEFAULT_CONFIG, yaml.safe_dump(policy, sort_keys=True))


def write_reviews(root, policy, mutate=None):
    paths = builder.collect(root, policy)
    rows = []
    for path in paths:
        if path in builder.PUBLIC_NOTEBOOKS or (
            path.startswith("results/") and path not in {"results/README.md", "results/.run_id"}
        ):
            row = {key: "" for key in builder.REVIEW_COLUMNS}
            row.update(artifact_path=path, artifact_type="fixture",
                       source_sha256=builder.digest((root / path).read_bytes()),
                       public_sha256=builder.digest((root / path).read_bytes()),
                       review_status="approved", action="include", source_code_changed="false")
            rows.append(row)
    if mutate:
        mutate(rows)
    put(root, policy["public_artifact_review"], csv_bytes(sorted(builder.REVIEW_COLUMNS), rows))


@pytest.fixture
def release(tmp_path):
    policy = {
        "version": builder.VERSION, "run_id": builder.RUN_ID,
        "demo_manifest": "data/manifest.csv",
        "public_artifact_review": "docs/public_artifact_review.csv",
        "include_latest": True,
        "include_files": sorted(builder.ROOT_FILES | builder.PUBLIC_NOTEBOOKS | {
            "data/README.md", "data/manifest.csv", "results/README.md", "results/.run_id",
            "docs/public_artifact_review.csv",
            f"results/runs/{builder.RUN_ID}/EXECUTION_REPORT.md",
        }),
    }
    policy["include_trees"] = sorted(builder.allowed_trees(policy))
    for rel in policy["include_files"]:
        put(tmp_path, rel)
    put(tmp_path, "pyproject.toml", '[project]\nname = "fixture"\nversion = "1.0.0"\n')
    put(tmp_path, "CITATION.cff", "version: 1.0.0\n")
    put(tmp_path, ".zenodo.json", json.dumps({"version": "v1.0.0"}))
    put(tmp_path, "CHANGELOG.md", "# Changes\n\n## [1.0.0] - 2026-10-08\n")
    put(tmp_path, "results/.run_id", builder.RUN_ID + "\n")
    for rel in builder.PUBLIC_NOTEBOOKS:
        put(tmp_path, rel, '{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}\n')
    for tree in policy["include_trees"]:
        put(tmp_path, tree + "/fixture.txt")
    rows = []
    for n in range(1, 12):
        path = f"data/demo/input-{n:03d}.bin"
        data = bytes([n]) * n
        put(tmp_path, path, data)
        rows.append({"dataset_id": f"DEMO-{n:03d}", "path": path,
                     "size_bytes": str(len(data)), "sha256": builder.digest(data),
                     "source_type": "synthetic", "redistribution_allowed": "yes"})
    put(tmp_path, "data/manifest.csv", csv_bytes(list(rows[0]), rows))
    write_policy(tmp_path, policy)
    write_reviews(tmp_path, policy)
    return tmp_path, policy


def test_archive_exactly_matches_sorted_manifest_and_hashes(release):
    root, policy = release
    archive = builder.build_release(root)
    manifest = root / "dist/release_manifest.csv"
    checksums = root / "dist/artifact_checksums.sha256"
    rows = builder.verify_archive(archive, manifest, checksums)
    expected = builder.collect(root, policy)
    assert [r["path"] for r in rows] == expected == sorted(set(expected))
    assert sum(p.startswith("data/demo/") for p in expected) == 11
    with zipfile.ZipFile(archive) as zf:
        assert zf.namelist() == expected
        for info, row in zip(zf.infolist(), rows):
            data = zf.read(info.filename)
            assert int(row["size_bytes"]) == info.file_size == len(data)
            assert row["sha256"] == builder.digest(data)
            assert data == (root / info.filename).read_bytes()
            assert info.date_time == (1980, 1, 1, 0, 0, 0)
    assert not any(p.startswith("dist/") for p in expected)


def test_repeat_build_is_identical_despite_mtime_changes(release):
    root, _ = release
    archive = builder.build_release(root)
    before = {p.name: p.read_bytes() for p in (root / "dist").iterdir()}
    import os
    for path in root.rglob("*"):
        if path.is_file():
            os.utime(path, (1700000000, 1700000000))
    builder.build_release(root)
    assert {p.name: p.read_bytes() for p in (root / "dist").iterdir()} == before
    assert builder.build_release(root, verify_only=True) == archive


@pytest.mark.parametrize("rel", [
    "docs/.env", "scripts/private_key.txt", "tests/token.txt", "docs/x.pem",
    "docs/x.docx", "docs/x:Zone.Identifier", "src/nested/dist/package.txt",
    "src/nested/build/package.txt", "src/module.egg-info/PKG-INFO",
    "tests/__pycache__/test.pyc", "docs/backups/notes.md", "scripts/.git/config",
    "scripts/.venv/fixture.txt", "docs/.pytest_cache/state", "docs/notes.bak",
])
def test_discovered_denied_files_are_skipped(release, rel):
    root, policy = release
    put(root, rel, b"dummy fixture secret, not real\n")
    assert rel not in builder.collect(root, policy)
    archive = builder.build_release(root)
    with zipfile.ZipFile(archive) as zf:
        assert rel not in zf.namelist()


@pytest.mark.parametrize("rel", [
    "results/analysis result/payload.bin", "notebooks/original/raw.ipynb",
    "PM_BG_+_AES_(works)_ori.ipynb", "notebooks/demo_colab.ipynb",
    "data/demo/unlisted.bin", "results/runs/other/raw/data.csv", "docs/private.txt",
    "docs/file.docx", "dist/old.zip",
])
def test_explicit_denied_or_unapproved_inclusion_fails(release, rel):
    root, policy = release
    put(root, rel)
    policy["include_files"].append(rel)
    with pytest.raises(builder.ReleaseError, match="explicit inclusion"):
        builder.collect(root, policy)


@pytest.mark.parametrize("rel", ["results", "notebooks", "data", "data/demo", "docs/dist"])
def test_broad_or_denied_explicit_tree_fails(release, rel):
    root, policy = release
    policy["include_trees"].append(rel)
    with pytest.raises(builder.ReleaseError, match="explicit tree"):
        builder.collect(root, policy)


def test_unknown_files_unlisted_data_other_runs_and_scratch_are_excluded(release):
    root, policy = release
    unexpected = ["unknown.txt", "data/demo/extra.bin", "data/private.bin",
                  "notebooks/public/extra.ipynb", "results/runs/older/raw/data.bin",
                  f"results/runs/{builder.RUN_ID}/extra.bin",
                  f"results/runs/{builder.RUN_ID}/raw/scratch/secret.bin",
                  "results/analysis result/restricted.bin"]
    for path in unexpected:
        put(root, path)
    assert not set(unexpected) & set(builder.collect(root, policy))


@pytest.mark.parametrize("rel", ["../outside", "/absolute", "docs/../README.md",
                                      "docs//file", "docs/./file", "C:/file", "docs\\file"])
def test_noncanonical_and_traversal_paths_fail(release, rel):
    root, policy = release
    policy["include_files"].append(rel)
    with pytest.raises(builder.ReleaseError, match="unsafe relative path"):
        builder.collect(root, policy)


@pytest.mark.parametrize("rel", ["docs/link.txt", "docs/private_link", "docs/linked-tree"])
def test_symlinks_fail_even_with_denied_names(release, rel):
    root, policy = release
    target = root / "outside.txt"
    target.write_text("dummy fixture")
    try:
        (root / rel).symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable on this platform")
    with pytest.raises(builder.ReleaseError, match="symlink"):
        builder.collect(root, policy)


def test_symlink_output_directory_fails(release):
    root, _ = release
    other = root / "other"
    other.mkdir()
    try:
        (root / "dist").symlink_to(other, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks unavailable on this platform")
    with pytest.raises(builder.ReleaseError, match="symlink"):
        builder.build_release(root)


@pytest.mark.parametrize("problem", ["hash", "size", "permission", "duplicate", "count", "traversal"])
def test_demo_manifest_is_fail_closed(release, problem):
    root, policy = release
    fields, rows = builder.read_csv((root / "data/manifest.csv").read_bytes(), "fixture")
    if problem == "hash":
        rows[0]["sha256"] = "0" * 64
    elif problem == "size":
        rows[0]["size_bytes"] = "99"
    elif problem == "permission":
        rows[0]["redistribution_allowed"] = "no"
    elif problem == "duplicate":
        rows[1]["path"] = rows[0]["path"]
    elif problem == "count":
        rows.pop()
    else:
        rows[0]["path"] = "data/demo/../../private.bin"
    put(root, "data/manifest.csv", csv_bytes(sorted(fields), rows))
    with pytest.raises(builder.ReleaseError):
        builder.collect(root, policy)


@pytest.mark.parametrize("problem", ["missing", "pending", "excluded", "hash", "source", "code", "duplicate"])
def test_public_review_gate(release, problem):
    root, policy = release
    def mutate(rows):
        index = next(i for i, row in enumerate(rows) if row["artifact_path"] in builder.PUBLIC_NOTEBOOKS)
        row = rows[index]
        if problem == "missing":
            rows.pop(index)
        elif problem == "pending":
            row["review_status"] = "pending"
        elif problem == "excluded":
            row["action"] = "exclude"
        elif problem == "hash":
            row["public_sha256"] = "0" * 64
        elif problem == "source":
            row["source_sha256"] = "not a hash"
        elif problem == "code":
            row["source_code_changed"] = "true"
        else:
            rows.append(dict(row))
    write_reviews(root, policy, mutate)
    with pytest.raises(builder.ReleaseError):
        builder.build_release(root)
    assert not (root / "dist").exists()


def test_review_header_required_and_no_self_hash_required(release):
    root, policy = release
    builder.build_release(root)  # fixture review CSV has no review of itself
    put(root, policy["public_artifact_review"], "artifact_path,public_sha256\n")
    with pytest.raises(builder.ReleaseError, match="columns"):
        builder.build_release(root)


@pytest.mark.parametrize("rel", ["pyproject.toml", "CITATION.cff", ".zenodo.json", "CHANGELOG.md"])
def test_metadata_version_mismatch_fails(release, rel):
    root, _ = release
    path = root / rel
    path.write_text(path.read_text().replace("1.0.0", "0.1.0"))
    with pytest.raises(builder.ReleaseError):
        builder.build_release(root)
    assert not (root / "dist").exists()


@pytest.mark.parametrize("problem", ["pointer", "content", "extra", "missing"])
def test_latest_mirrors_must_match_selected_run(release, problem):
    root, policy = release
    if problem == "pointer":
        put(root, "results/.run_id", "older-run\n")
    elif problem == "content":
        put(root, "results/figures/fixture.txt", "different")
    elif problem == "extra":
        put(root, "results/raw/extra.csv")
    else:
        (root / "results/logs/fixture.txt").unlink()
    with pytest.raises(builder.ReleaseError):
        builder.collect(root, policy)


def test_selected_run_only_mode(release):
    root, policy = release
    policy["include_latest"] = False
    policy["include_trees"] = sorted(builder.allowed_trees(policy))
    write_policy(root, policy)
    write_reviews(root, policy)
    archive = builder.build_release(root)
    with zipfile.ZipFile(archive) as zf:
        assert "results/.run_id" in zf.namelist()
        assert not any(p.startswith("results/raw/") for p in zf.namelist())
        assert any(p.startswith(f"results/runs/{builder.RUN_ID}/raw/") for p in zf.namelist())


@pytest.mark.parametrize("key,value", [
    ("version", "0.1.0"), ("run_id", "other"), ("include_latest", "yes"),
    ("unknown", True), ("include_files", []),
])
def test_config_schema_fails_closed(release, key, value):
    root, policy = release
    policy[key] = value
    write_policy(root, policy)
    with pytest.raises(builder.ReleaseError):
        builder.build_release(root)


def test_missing_required_file_and_omitted_required_tree(release):
    root, policy = release
    policy["include_trees"].remove("src")
    with pytest.raises(builder.ReleaseError, match="trees omitted"):
        builder.collect(root, policy)
    policy["include_trees"].append("src")
    (root / "LICENSE").unlink()
    with pytest.raises(builder.ReleaseError, match="missing"):
        builder.collect(root, policy)


@pytest.mark.parametrize("problem", ["extra", "missing", "duplicate", "order", "content", "symlink", "corrupt"])
def test_zip_validation_rejects_tampering(release, problem):
    root, _ = release
    archive = builder.build_release(root)
    manifest = root / "dist/release_manifest.csv"
    with zipfile.ZipFile(archive) as zf:
        entries = [(i.filename, zf.read(i)) for i in zf.infolist()]
    if problem == "corrupt":
        archive.write_bytes(b"not a ZIP")
    else:
        if problem == "extra":
            entries.append(("unexpected.txt", b"extra"))
        elif problem == "missing":
            entries.pop()
        elif problem == "duplicate":
            entries.append(entries[0])
        elif problem == "order":
            entries.reverse()
        elif problem == "content":
            entries[0] = (entries[0][0], b"tampered")
        with zipfile.ZipFile(archive, "w") as zf:
            for n, (name, data) in enumerate(entries):
                info = zipfile.ZipInfo(name)
                if problem == "symlink" and n == 0:
                    info.create_system = 3
                    info.external_attr = (stat.S_IFLNK | 0o777) << 16
                if problem == "duplicate" and n == len(entries) - 1:
                    with pytest.warns(UserWarning, match="Duplicate name"):
                        zf.writestr(info, data)
                else:
                    zf.writestr(info, data)
    with pytest.raises(builder.ReleaseError):
        builder.verify_archive(archive, manifest)


@pytest.mark.parametrize("problem", ["hash", "size", "order", "duplicate", "traversal"])
def test_manifest_validation_rejects_tampering(release, problem):
    root, _ = release
    archive = builder.build_release(root)
    manifest = root / "dist/release_manifest.csv"
    _, rows = builder.read_csv(manifest.read_bytes(), "manifest")
    if problem == "hash":
        rows[0]["sha256"] = "0" * 64
    elif problem == "size":
        rows[0]["size_bytes"] = "999"
    elif problem == "order":
        rows.reverse()
    elif problem == "duplicate":
        rows.append(rows[0])
    else:
        rows[0]["path"] = "../outside"
    manifest.write_bytes(builder.manifest_bytes(rows))
    with pytest.raises(builder.ReleaseError):
        builder.verify_archive(archive, manifest)


def test_checksum_and_workspace_changes_detected_without_writes(release):
    root, _ = release
    archive = builder.build_release(root)
    checksum = root / "dist/artifact_checksums.sha256"
    original = checksum.read_bytes()
    checksum.write_text("wrong\n")
    with pytest.raises(builder.ReleaseError, match="checksum"):
        builder.build_release(root, verify_only=True)
    checksum.write_bytes(original)
    before = {p.name: p.read_bytes() for p in archive.parent.iterdir()}
    put(root, "README.md", "changed reviewed documentation")
    with pytest.raises(builder.ReleaseError, match="workspace"):
        builder.build_release(root, verify_only=True)
    assert {p.name: p.read_bytes() for p in archive.parent.iterdir()} == before


def test_failed_build_preserves_previous_outputs(release):
    root, _ = release
    builder.build_release(root)
    before = {p.name: p.read_bytes() for p in (root / "dist").iterdir()}
    put(root, "results/.run_id", "wrong-run")
    with pytest.raises(builder.ReleaseError):
        builder.build_release(root)
    assert {p.name: p.read_bytes() for p in (root / "dist").iterdir()} == before


def test_cli_build_verify_and_error(release, capsys):
    root, _ = release
    assert builder.main(["--root", str(root), "--config", builder.DEFAULT_CONFIG]) == 0
    assert builder.main(["--root", str(root), "--verify"]) == 0
    put(root, "results/.run_id", "wrong")
    assert builder.main(["--root", str(root), "--verify"]) == 1
    assert "release validation failed" in capsys.readouterr().err


def test_verify_missing_outputs_does_not_build(release):
    root, _ = release
    with pytest.raises(OSError):
        builder.build_release(root, verify_only=True)
    assert not (root / "dist").exists()
