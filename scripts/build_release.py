"""Build and verify a local, explicitly scoped release; never publish anything."""

import argparse
import csv
import hashlib
import io
import json
import os
import re
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

import yaml

VERSION = "1.0.0"
RUN_ID = "v1.0.0-demo-20261008T020017Z"
ARCHIVE = f"dist/pm-bg-aes-supplementary-v{VERSION}.zip"
DEFAULT_CONFIG = "configs/release_v1.0.0.yaml"
ROOT_FILES = {
    "LICENSE", "README.md", "CITATION.cff", ".zenodo.json", "CHANGELOG.md",
    "pyproject.toml", "requirements.txt", "requirements-lock.txt", ".gitignore",
}
PUBLIC_NOTEBOOKS = {
    "notebooks/public/" + name for name in (
        "PM_BG_+_AES_(works)_ori.ipynb", "PM_BG_+_AES_(works)_workshop.ipynb",
        "demo_colab.ipynb", "analyze_results.ipynb",
    )
}
MIRRORS = ("raw", "summary", "figures", "logs")
REVIEW_COLUMNS = {
    "artifact_path", "artifact_type", "source_sha256", "public_sha256",
    "review_status", "action", "redaction_categories", "source_code_changed", "notes",
}
MANIFEST_FIELDS = ["path", "sha256", "size_bytes"]


class ReleaseError(ValueError):
    """Invalid policy, unapproved input, or failed integrity validation."""


def relative_path(value):
    """Reject ambiguous, absolute and traversal paths rather than normalizing them."""
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ReleaseError(f"unsafe relative path: {value!r}")
    parts = value.split("/")
    if any(p in ("", ".", "..") for p in parts) or PurePosixPath(value).is_absolute():
        raise ReleaseError(f"unsafe relative path: {value!r}")
    return value


def prohibited(rel):
    parts = rel.lower().split("/")
    names = {
        ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
        ".ruff_cache", ".cache", "cache", "caches", ".hypothesis", ".tox", ".nox",
        ".ipynb_checkpoints", "build",
        "dist", "scratch", "backup", "backups", "secrets", "secret", "tokens",
        "token", "credentials", "analysis result", "original",
    }
    return any(
        p in names or p.startswith((".env", "private", "token"))
        or p.endswith((".docx", ".pem", ".key", ".pyc", ".pyo", ".egg-info",
                       ".bak", ".backup", ".old", "~"))
        or "zone.identifier" in p
        for p in parts
    )


def checked_path(root, rel):
    if root.is_symlink():
        raise ReleaseError(f"symlink root is not allowed: {root}")
    relative_path(rel)
    current = root
    for component in rel.split("/"):
        current = current / component
        if current.is_symlink():
            raise ReleaseError(f"symlink is not allowed: {rel}")
    if not current.resolve().is_relative_to(root.resolve()):
        raise ReleaseError(f"path escapes root: {rel}")
    return current


def file_bytes(root, rel):
    path = checked_path(root, rel)
    if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
        raise ReleaseError(f"required regular file missing: {rel}")
    return path.read_bytes()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_csv(data, label):
    try:
        reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ReleaseError(f"invalid CSV header: {label}")
        rows = list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            raise ReleaseError(f"malformed CSV: {label}")
        return set(reader.fieldnames), rows
    except (UnicodeError, csv.Error) as exc:
        raise ReleaseError(f"invalid CSV: {label}") from exc


def load_config(root, config=DEFAULT_CONFIG):
    policy = yaml.safe_load(file_bytes(Path(root), config))
    if not isinstance(policy, dict):
        raise ReleaseError("release config must be a mapping")
    required = {"version", "run_id", "include_files", "include_trees", "demo_manifest",
                "public_artifact_review", "include_latest"}
    if set(policy) != required:
        raise ReleaseError(f"config keys must be exactly {sorted(required)}")
    if str(policy["version"]) != VERSION or policy["run_id"] != RUN_ID:
        raise ReleaseError("config version/run_id is not the approved release")
    if type(policy["include_latest"]) is not bool:
        raise ReleaseError("include_latest must be boolean")
    for key in ("include_files", "include_trees"):
        values = policy[key]
        if not isinstance(values, list) or not values or any(not isinstance(v, str) for v in values):
            raise ReleaseError(f"{key} must be a nonempty path list")
        if len(values) != len(set(values)):
            raise ReleaseError(f"duplicate {key}")
    return policy


def allowed_file(rel, policy):
    return rel in ROOT_FILES | PUBLIC_NOTEBOOKS | {
        "data/README.md", "data/manifest.csv", "results/README.md", "results/.run_id",
        policy["public_artifact_review"],
    }


def allowed_trees(policy):
    run = f"results/runs/{RUN_ID}"
    trees = {"src", "tests", "scripts", "configs", "docs"}
    trees.update(f"{run}/{name}" for name in MIRRORS)
    if policy["include_latest"]:
        trees.update(f"results/{name}" for name in MIRRORS)
    return trees


def tree_files(root, rel):
    base = checked_path(root, rel)
    if not base.is_dir():
        raise ReleaseError(f"required directory missing: {rel}")
    out = []
    for directory, dirs, files in os.walk(base, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(directory) / name
            child = path.relative_to(root).as_posix()
            # Even a prohibited symlink is rejected, not silently followed or skipped.
            if path.is_symlink():
                raise ReleaseError(f"symlink is not allowed: {child}")
            if prohibited(child):
                if name in dirs:
                    dirs.remove(name)
                continue
            if name in files:
                file_bytes(root, child)
                out.append(child)
        dirs.sort()
    return out


def demo_files(root, policy):
    manifest = relative_path(policy["demo_manifest"])
    if manifest != "data/manifest.csv":
        raise ReleaseError("demo manifest must be data/manifest.csv")
    fields, rows = read_csv(file_bytes(root, manifest), manifest)
    if not {"dataset_id", "path", "size_bytes", "sha256", "source_type",
            "redistribution_allowed"} <= fields:
        raise ReleaseError("demo manifest missing required columns")
    ids = [row["dataset_id"] for row in rows]
    if len(rows) != 11 or set(ids) != {f"DEMO-{n:03d}" for n in range(1, 12)}:
        raise ReleaseError("demo manifest must contain exactly DEMO-001..DEMO-011")
    paths = []
    for row in rows:
        rel = relative_path(row["path"])
        if not rel.startswith("data/demo/") or prohibited(rel) or rel in paths:
            raise ReleaseError(f"invalid/duplicate demo path: {rel}")
        data = file_bytes(root, rel)
        if (row["source_type"] != "synthetic" or row["redistribution_allowed"] != "yes"
                or row["size_bytes"] != str(len(data)) or row["sha256"] != digest(data)):
            raise ReleaseError(f"demo integrity/permission mismatch: {rel}")
        paths.append(rel)
    return paths


def collect(root, policy=None):
    """Return the sorted allowlist, with hard denial taking precedence."""
    root = Path(root).absolute()
    policy = load_config(root) if policy is None else policy
    relative_path(policy["public_artifact_review"])
    if policy["public_artifact_review"] != "docs/public_artifact_review.csv":
        raise ReleaseError("review record must be docs/public_artifact_review.csv")
    out = set()
    report = f"results/runs/{RUN_ID}/EXECUTION_REPORT.md"
    for rel in policy["include_files"]:
        relative_path(rel)
        if prohibited(rel) or not (allowed_file(rel, policy) or rel == report):
            raise ReleaseError(f"explicit inclusion outside approved scope: {rel}")
        file_bytes(root, rel)
        out.add(rel)
    for rel in policy["include_trees"]:
        relative_path(rel)
        if prohibited(rel) or rel not in allowed_trees(policy):
            raise ReleaseError(f"explicit tree outside approved scope: {rel}")
        out.update(tree_files(root, rel))
    out.update(demo_files(root, policy))
    required = ROOT_FILES | PUBLIC_NOTEBOOKS | {
        report, "data/manifest.csv", "data/README.md", "results/README.md",
        "results/.run_id", policy["public_artifact_review"], DEFAULT_CONFIG,
    }
    if not required <= out:
        raise ReleaseError(f"required release files omitted: {sorted(required - out)}")
    if not allowed_trees(policy) <= set(policy["include_trees"]):
        raise ReleaseError("required release trees omitted")
    if file_bytes(root, "results/.run_id").decode("utf-8").strip() != RUN_ID:
        raise ReleaseError("results/.run_id does not identify selected run")
    if policy["include_latest"]:
        for name in MIRRORS:
            prefix = f"results/runs/{RUN_ID}/{name}/"
            selected = {p[len(prefix):]: p for p in out if p.startswith(prefix)}
            latest_prefix = f"results/{name}/"
            latest = {p[len(latest_prefix):]: p for p in out if p.startswith(latest_prefix)}
            if selected.keys() != latest.keys() or any(
                file_bytes(root, selected[p]) != file_bytes(root, latest[p]) for p in selected
            ):
                raise ReleaseError(f"latest mirror differs from selected run: {name}")
    return sorted(out)


def validate_metadata(root):
    """Check release versions without banning legitimate repository/DOI URLs."""
    text = file_bytes(root, "pyproject.toml").decode("utf-8")
    # Python 3.10 is supported; only the [project] version is relevant here.
    project = re.search(r"(?ms)^\[project\]\s*\n(.*?)(?=^\[|\Z)", text)
    version = re.search(r'^version\s*=\s*[\'\"]([^\'\"]+)[\'\"]\s*$',
                        project.group(1) if project else "", re.MULTILINE)
    citation = yaml.safe_load(file_bytes(root, "CITATION.cff"))
    zenodo = json.loads(file_bytes(root, ".zenodo.json"))
    if (not version or version.group(1) != VERSION or not isinstance(citation, dict)
            or str(citation.get("version")) != VERSION or not isinstance(zenodo, dict)
            or str(zenodo.get("version", "")).removeprefix("v") != VERSION):
        raise ReleaseError("pyproject/CITATION/Zenodo release version mismatch")
    changelog = file_bytes(root, "CHANGELOG.md").decode("utf-8")
    if not re.search(r"(?m)^##\s+\[?v?1\.0\.0(?:\]|\s|$)", changelog):
        raise ReleaseError("CHANGELOG missing v1.0.0 section")


def validate_reviews(root, files, policy):
    rel = policy["public_artifact_review"]
    fields, rows = read_csv(file_bytes(root, rel), rel)
    if not REVIEW_COLUMNS <= fields:
        raise ReleaseError("public artifact review missing required columns")
    reviews = {}
    for row in rows:
        path = relative_path(row["artifact_path"])
        if path in reviews:
            raise ReleaseError(f"duplicate artifact review: {path}")
        reviews[path] = row
    # Review documents/reports are not required to hash themselves. The selected
    # run's execution report IS gated; docs describing the review are not.
    gated = [p for p in files if p in PUBLIC_NOTEBOOKS or
             (p.startswith("results/") and p not in {"results/README.md", "results/.run_id"})]
    for path in gated:
        row = reviews.get(path)
        if not row or row["review_status"].lower() not in {"approved", "approved_public", "public"}:
            raise ReleaseError(f"public approval missing: {path}")
        if row["action"].lower() not in {"include", "keep", "sanitized", "redacted", "redact"}:
            raise ReleaseError(f"review action does not permit inclusion: {path}")
        if row["public_sha256"] != digest(file_bytes(root, path)):
            raise ReleaseError(f"public review hash mismatch: {path}")
        if not re.fullmatch(r"[0-9a-f]{64}", row["source_sha256"]):
            raise ReleaseError(f"invalid source review hash: {path}")
        if path in PUBLIC_NOTEBOOKS and row["source_code_changed"].lower() not in {"false", "no"}:
            raise ReleaseError(f"notebook source code preservation not confirmed: {path}")


def manifest_bytes(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def verify_archive(archive, manifest, checksums=None):
    """Validate exact member equality, ordering, paths, sizes, CRC and SHA-256."""
    fields, rows = read_csv(Path(manifest).read_bytes(), str(manifest))
    if fields != set(MANIFEST_FIELDS) or not rows:
        raise ReleaseError("invalid/empty release manifest")
    paths = [relative_path(row["path"]) for row in rows]
    if paths != sorted(set(paths)) or any(prohibited(p) for p in paths):
        raise ReleaseError("manifest paths must be unique, sorted and permitted")
    try:
        with zipfile.ZipFile(archive) as zf:
            infos = zf.infolist()
            if [i.filename for i in infos] != paths:
                raise ReleaseError("ZIP members differ from sorted manifest")
            for info, row in zip(infos, rows):
                mode = info.external_attr >> 16
                if info.is_dir() or stat.S_ISLNK(mode) or info.flag_bits & 1:
                    raise ReleaseError(f"invalid ZIP member: {info.filename}")
                data = zf.read(info)
                if str(info.file_size) != row["size_bytes"] or digest(data) != row["sha256"]:
                    raise ReleaseError(f"ZIP size/hash mismatch: {info.filename}")
            if zf.testzip() is not None:
                raise ReleaseError("ZIP CRC validation failed")
    except (zipfile.BadZipFile, RuntimeError, EOFError) as exc:
        raise ReleaseError(f"invalid ZIP: {exc}") from exc
    if checksums is not None:
        expected = f"{digest(Path(archive).read_bytes())}  {Path(archive).name}\n"
        if Path(checksums).read_text(encoding="utf-8") != expected:
            raise ReleaseError("archive checksum mismatch")
    return rows


def build_release(root, config=DEFAULT_CONFIG, verify_only=False):
    """Return ZIP path. Verify-only also checks current policy and workspace hashes."""
    root = Path(root).absolute()
    policy = load_config(root, config)
    files = collect(root, policy)
    validate_metadata(root)
    validate_reviews(root, files, policy)
    rows = [{"path": p, "sha256": digest(file_bytes(root, p)),
             "size_bytes": str(len(file_bytes(root, p)))} for p in files]
    dist = checked_path(root, "dist")
    archive = checked_path(root, ARCHIVE)
    manifest = checked_path(root, "dist/release_manifest.csv")
    checksums = checked_path(root, "dist/artifact_checksums.sha256")
    if verify_only:
        if verify_archive(archive, manifest, checksums) != rows:
            raise ReleaseError("archive manifest differs from current approved workspace")
        return archive
    dist.mkdir(exist_ok=True)
    # Validate temporary artifacts before replacing any existing release outputs.
    with tempfile.TemporaryDirectory(prefix="release-", dir=dist) as temporary:
        temp = Path(temporary)
        candidate = temp / archive.name
        candidate_manifest = temp / manifest.name
        candidate_checksums = temp / checksums.name
        candidate_manifest.write_bytes(manifest_bytes(rows))
        with zipfile.ZipFile(candidate, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for row in rows:
                data = file_bytes(root, row["path"])
                if digest(data) != row["sha256"]:
                    raise ReleaseError(f"input changed during build: {row['path']}")
                info = zipfile.ZipInfo(row["path"], date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, data, compresslevel=9)
        candidate_checksums.write_text(
            f"{digest(candidate.read_bytes())}  {archive.name}\n", encoding="utf-8", newline="\n")
        verify_archive(candidate, candidate_manifest, candidate_checksums)
        for source, target in ((candidate, archive), (candidate_manifest, manifest),
                               (candidate_checksums, checksums)):
            os.replace(source, target)
    return archive


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="root-relative policy path")
    parser.add_argument("--verify", action="store_true", help="validate existing outputs without writing")
    args = parser.parse_args(argv)
    try:
        archive = build_release(args.root, args.config, args.verify)
    except (ReleaseError, OSError, UnicodeError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"release validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"{'verified' if args.verify else 'built'}: {archive} — LOCAL ONLY, not published")
    return 0


if __name__ == "__main__":
    sys.exit(main())
