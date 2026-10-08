"""Create sanitized public notebook copies.

Keeps each code/markdown cell's joined ``source`` byte-identical while removing
saved ``outputs``, ``execution_count`` and cell-level metadata (Colab widget
ids, ``execution``/``executionInfo`` timestamps, ``base_uri``, ``outputId``).
Notebook-level ``metadata`` is reduced to ``kernelspec`` and ``language_info``.

The original evidence notebooks are preserved elsewhere; this tool only writes
the reviewed public copies under ``notebooks/public/``. It never executes a
notebook and never reads or modifies excluded research payloads.

Usage:
    python scripts/sanitize_notebooks.py            # write public copies
    python scripts/sanitize_notebooks.py --check    # verify only, exit 1 on drift
"""

import argparse
import json
from pathlib import Path

# original source -> public destination (repository-relative POSIX paths)
MAPPING = {
    "PM_BG_+_AES_(works)_ori.ipynb": "notebooks/public/PM_BG_+_AES_(works)_ori.ipynb",
    "PM_BG_+_AES_(works)_workshop.ipynb": "notebooks/public/PM_BG_+_AES_(works)_workshop.ipynb",
    "notebooks/demo_colab.ipynb": "notebooks/public/demo_colab.ipynb",
    "notebooks/analyze_results.ipynb": "notebooks/public/analyze_results.ipynb",
}
KEEP_METADATA = ("kernelspec", "language_info")


def sanitize(nb):
    cells = []
    for cell in nb.get("cells", []):
        clean = {
            "cell_type": cell.get("cell_type"),
            "metadata": {},
            "source": list(cell.get("source", [])),
        }
        if "id" in cell:
            clean["id"] = cell["id"]
        if cell.get("cell_type") == "code":
            clean["execution_count"] = None
            clean["outputs"] = []
        cells.append(clean)
    metadata = {k: nb["metadata"][k] for k in KEEP_METADATA if k in nb.get("metadata", {})}
    return {
        "cells": cells,
        "metadata": metadata,
        "nbformat": nb.get("nbformat", 4),
        "nbformat_minor": nb.get("nbformat_minor", 5),
    }


def render(nb):
    return json.dumps(nb, indent=1, ensure_ascii=False) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true",
                        help="verify existing public copies without writing")
    args = parser.parse_args(argv)
    root = Path(args.root)
    status = 0
    for source, dest in MAPPING.items():
        src_path, dst_path = root / source, root / dest
        data = render(sanitize(json.loads(src_path.read_text(encoding="utf-8"))))
        if args.check:
            current = dst_path.read_text(encoding="utf-8") if dst_path.is_file() else None
            if current != data:
                print(f"drift: {dest}")
                status = 1
            else:
                print(f"ok: {dest}")
        else:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.write_text(data, encoding="utf-8", newline="\n")
            print(f"wrote: {dest}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
