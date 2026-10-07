"""Build the local release candidate (no remote side effects).

Includes: source, original notebooks, demo notebooks, tests, configs, docs,
demo data, actual results, lock file, draft metadata. Excludes: .venv,
.git, caches, secrets, scratch dirs, DOCX manuscript, non-redistributable
data. Verifies manifest, checksums, and placeholder-only DOI/URLs.
"""

import argparse
import csv
import hashlib
import os
import sys
import zipfile

VERSION = "0.1.0"
ARCHIVE = f"dist/pm-bg-aes-supplementary-v{VERSION}.zip"

INCLUDE_TOP = ["README.md", "LICENSE", "CITATION.cff", "CHANGELOG.md",
               "pyproject.toml", "requirements.txt", "requirements-lock.txt",
               ".gitignore", ".zenodo.json"]
INCLUDE_DIRS = ["src", "notebooks", "configs", "scripts", "tests", "docs",
                "data", "results"]

FORBIDDEN_SUBSTR = [".docx", "Zone.Identifier", ".venv", "/.git/",
                    "__pycache__", ".ipynb_checkpoints"]
SKIP_SUBSTR = ["/scratch", ".run_id", "artifact_checksums", "release_manifest"]


def collect(root: str) -> list:
    """Collect releasable relative paths (sorted, deterministic)."""
    out = []
    for top in INCLUDE_TOP:
        p = os.path.join(root, top)
        if os.path.exists(p):
            out.append(top)
    for d in INCLUDE_DIRS:
        for base, _dirs, files in os.walk(os.path.join(root, d)):
            _dirs[:] = sorted(x for x in _dirs
                              if x not in (".ipynb_checkpoints", "__pycache__", "scratch"))
            for fn in sorted(files):
                rel = os.path.relpath(os.path.join(base, fn), root)
                if any(s in rel for s in (".ipynb_checkpoints", "__pycache__")):
                    continue
                if any(s in rel for s in SKIP_SUBSTR):
                    continue
                out.append(rel)
    return sorted(set(out))


def main(argv=None) -> int:
    """Entry point."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    os.makedirs(os.path.join(root, "dist"), exist_ok=True)

    files = collect(root)
    bad = [f for f in files if any(s in f for s in FORBIDDEN_SUBSTR)]
    # .run_id/artifact files live outside collected trees; guard explicitly:
    assert not bad, f"forbidden paths collected: {bad}"
    assert files, "nothing to archive"

    # Originals must be checksum-identical to workspace sources.
    pairs = [("PM_BG_+_AES_(works)_ori.ipynb",
              "notebooks/original/PM_BG_+_AES_(works)_ori.ipynb"),
             ("PM_BG_+_AES_(works)_workshop.ipynb",
              "notebooks/original/PM_BG_+_AES_(works)_workshop.ipynb")]
    for src, dst in pairs:
        ha = hashlib.sha256(open(os.path.join(root, src), "rb").read()).hexdigest()
        hb = hashlib.sha256(open(os.path.join(root, dst), "rb").read()).hexdigest()
        assert ha == hb, f"original mismatch: {src}"

    # No fake DOI/URL: placeholders only.
    import re as _re

    for rel in files:
        if rel.startswith("notebooks/original/"):
            continue  # preserved originals: third-party metadata untouched
        if rel.endswith((".png", ".svg", ".zip", ".bin", ".enc", ".dec")):
            continue
        try:
            text = open(os.path.join(root, rel), encoding="utf-8",
                        errors="strict").read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        # No fake publication identifiers: any github/zenodo/doi reference
        # must be a bracketed placeholder; docs URLs are allowed.
        for m in _re.finditer(
                r"(https?://(github\.com|zenodo\.org|doi\.org)\S+)|(\b10\.\d{4}/\S+)", text):
            assert False, f"publication-like identifier in {rel}: {m.group(0)[:80]}"

    manifest = os.path.join(root, "dist", "release_manifest.csv")
    with open(manifest, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path", "sha256", "size_bytes"])
        for rel in files:
            full = os.path.join(root, rel)
            h = hashlib.sha256()
            with open(full, "rb") as fh:
                for c in iter(lambda: fh.read(65536), b""):
                    h.update(c)
            w.writerow([rel, h.hexdigest(), os.path.getsize(full)])

    archive = os.path.join(root, ARCHIVE)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in files:
            zf.write(os.path.join(root, rel), rel)
    assert os.path.getsize(archive) > 0, "empty archive"

    # Record archive checksum; verify manifest entries exist in the zip.
    digest = hashlib.sha256(open(archive, "rb").read()).hexdigest()
    with open(os.path.join(root, "dist", "artifact_checksums.sha256"), "w") as f:
        f.write(f"{digest}  {os.path.basename(archive)}\n")
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    missing = [rel for rel in files if rel not in names]
    assert not missing, f"missing from archive: {missing[:5]}"
    print(f"archive: {ARCHIVE} ({os.path.getsize(archive)} bytes, "
          f"{len(files)} files, sha256={digest[:16]}…) — LOCAL ONLY, not published")
    return 0


if __name__ == "__main__":
    sys.exit(main())
