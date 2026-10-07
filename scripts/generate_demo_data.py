"""Generate the DEMO-*** demonstration dataset (category D).

Deterministic: ``random.Random`` with explicit seeds (NOT cryptographically
secure — documented; it only produces test payloads). AES IVs stay random
(the generator never touches crypto randomness). The ZIP uses a fixed
timestamp for byte-reproducibility. Idempotent: existing files with matching
SHA-256 are kept; mismatches abort unless ``--force``.
"""

import argparse
import csv
import hashlib
import os
import random
import sys
import zipfile

DATASETS = [
    # (dataset_id, filename, category, notes)
    ("DEMO-001", "demo_001_empty.bin", "empty", "zero-length edge case"),
    ("DEMO-002", "demo_002_tiny.bin", "tiny-binary", "very small payload; nonzero residual"),
    ("DEMO-003", "demo_003_repeated_byte.bin", "low-entropy", "single repeated byte; zero residual (6000 % 4 == 0, n=4)"),
    ("DEMO-004", "demo_004_structured_text.txt", "structured-text", "repeated structured text ~6 kB (F8 scale class, different content)"),
    ("DEMO-005", "demo_005_pseudorandom_100k.bin", "pseudorandom", "deterministic PRNG 100 kB; exercises n=8/12 branch"),
    ("DEMO-006", "demo_006_mixed_600k.bin", "mixed", "structured + pseudorandom 600 kB; exercises n=16/24 branch"),
    ("DEMO-007", "demo_007_archive.zip", "real-archive", "genuine ZIP (fixed timestamp) of demo text"),
    ("DEMO-008", "demo_008_pseudorandom_5m.bin", "large-pseudorandom", "deterministic PRNG 5.2 MB; exercises n=32/48 branch"),
    ("DEMO-009", "demo_009_structured_100k.txt", "structured-mid", "repeated structured text 100 kB; exercises n=8 branch"),
    ("DEMO-010", "demo_010_structured_600k.txt", "structured-large", "repeated structured text ~600 kB; exercises n=16 branch"),
    ("DEMO-011", "demo_011_zeros_5m.bin", "large-low-entropy", "zero bytes 5.2 MB; exercises n=32 branch"),
]

SEED = 20260912
TEXT_BLOCK = (
    "PM-BG-AES demonstration payload. Enterprise record #{i:06d}: "
    "graph-based permutation matrix Hill cipher with AES-CBC residual tail. "
    "The quick brown fox jumps over the lazy dog 0123456789.\n"
)


def payload(kind: str, rng: random.Random) -> bytes:
    """Build payload bytes for a dataset kind."""
    if kind == "empty":
        return b""
    if kind == "tiny":
        return bytes([(i * 37 + 11) % 256 for i in range(37)])
    if kind == "repeated":
        return b"\x41" * 6000
    if kind == "text":
        return "".join(TEXT_BLOCK.format(i=i) for i in range(32)).encode()
    if kind == "random100k":
        return bytes(rng.randrange(256) for _ in range(100_000))
    if kind == "mixed600k":
        head = ("MIXED-HEADER|" + "field=value;" * 200 + "\n").encode() * 40
        body = bytes(rng.randrange(256) for _ in range(500_000))
        tail = ("TRAILER|" + "checksum=deadbeef;" * 100 + "\n").encode() * 20
        blob = (head + body + tail)
        return blob[:600_000].ljust(600_000, b".")
    if kind == "random5m":
        return bytes(rng.randrange(256) for _ in range(5_200_000))
    if kind == "text100k":
        block = TEXT_BLOCK.format(i=7).encode()
        return (block * (100_000 // len(block) + 1))[:100_000]
    if kind == "text600k":
        block = TEXT_BLOCK.format(i=42).encode()
        return (block * (600_000 // len(block) + 1))[:600_000]
    if kind == "zeros5m":
        return b"\x00" * 5_200_000
    raise KeyError(kind)


def sha256(b: bytes) -> str:
    """Hex SHA-256."""
    return hashlib.sha256(b).hexdigest()


def md5(b: bytes) -> str:
    """Hex MD5 (legacy comparison)."""
    return hashlib.md5(b).hexdigest()


def build_zip(text: bytes, dest: str) -> None:
    """Write a deterministic ZIP (fixed timestamp/metadata)."""
    info = zipfile.ZipInfo("demo_payload.txt", date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    with zipfile.ZipFile(dest, "w") as zf:
        zf.writestr(info, text)


def generate(demo_dir: str, force: bool = False) -> list:
    """Generate all datasets; return manifest rows."""
    os.makedirs(demo_dir, exist_ok=True)
    rng = random.Random(SEED)
    rows = []
    kinds = ["empty", "tiny", "repeated", "text", "random100k", "mixed600k",
             None, "random5m", "text100k", "text600k", "zeros5m"]
    for (dsid, fname, category, notes), kind in zip(DATASETS, kinds):
        dest = os.path.join(demo_dir, fname)
        if kind is None:  # DEMO-007 real archive
            text = "".join(TEXT_BLOCK.format(i=i) for i in range(64)).encode()
            if os.path.exists(dest) and not force:
                with open(dest, "rb") as f:
                    existing = f.read()
                rows.append((dsid, fname, category, existing, notes))
                continue
            build_zip(text, dest)
            with open(dest, "rb") as f:
                blob = f.read()
        else:
            blob = payload(kind, rng)
            if os.path.exists(dest) and not force:
                with open(dest, "rb") as f:
                    existing = f.read()
                if sha256(existing) == sha256(blob):
                    rows.append((dsid, fname, category, existing, notes))
                    continue
                if not force:
                    raise SystemExit(f"checksum mismatch for {dest}; re-run with --force")
            with open(dest, "wb") as f:
                f.write(blob)
        rows.append((dsid, fname, category, blob, notes))
    return rows


def write_manifest(rows: list, demo_dir: str, manifest_path: str) -> None:
    """Write data/manifest.csv."""
    with open(manifest_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset_id", "filename", "path", "category", "source_type",
                    "size_bytes", "sha256", "md5", "generator", "seed",
                    "license_status", "redistribution_allowed",
                    "manuscript_dataset_id", "notes"])
        for dsid, fname, category, blob, notes in rows:
            w.writerow([dsid, fname, os.path.join("data/demo", fname), category,
                        "synthetic", len(blob), sha256(blob), md5(blob),
                        "scripts/generate_demo_data.py", SEED,
                        "CC0-1.0 (pending author approval)", "yes",
                        "", notes])


def main(argv=None) -> int:
    """Entry point."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo-dir", default="data/demo")
    ap.add_argument("--manifest", default="data/manifest.csv")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    rows = generate(args.demo_dir, args.force)
    write_manifest(rows, args.demo_dir, args.manifest)
    for dsid, fname, _c, blob, _n in rows:
        print(f"{dsid} {fname} {len(blob)} bytes sha256={sha256(blob)[:16]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
