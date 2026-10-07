"""Generate PNG+SVG figures from raw measurements (Agg backend).

Figures (demo IDs, never manuscript S-numbers):
- demo-throughput: encrypt/decrypt mean throughput per dataset (MiB/s).
- demo-elapsed: mean elapsed per dataset per direction (log scale).
- demo-entropy: input / ciphertext / recovered entropy per dataset.
- demo-hist-<id>: byte histogram (original vs ciphertext) for DEMO-005.
- demo-scatter-<id>: adjacent-byte scatter (original vs ciphertext,
  4000-point subsample) for DEMO-004.
Writes ``figure_manifest.csv`` alongside the figures.
"""

import argparse
import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _load(run_dir):
    import csv as _csv

    with open(os.path.join(run_dir, "raw", "benchmark_runs.csv")) as f:
        runs = list(_csv.DictReader(f))
    with open(os.path.join(run_dir, "raw", "integrity_checks.csv")) as f:
        integ = {r["dataset_id"]: r for r in _csv.DictReader(f)}
    return runs, integ


def _means(runs, phase, field):
    out = {}
    for r in runs:
        if (r["phase"] == phase and r["protocol"] == "local-structured"
                and str(r["warmup"]).lower() in ("false", "0", "")
                and r["status"] == "ok"):
            out.setdefault(r["dataset_id"], []).append(float(r[field]))
    return {k: float(np.mean(v)) for k, v in out.items()}


def _bar(ax, ids, series, ylabel, title):
    x = np.arange(len(ids))
    w = 0.8 / max(len(series), 1)
    for i, (label, vals) in enumerate(series):
        ax.bar(x + i * w, [vals.get(d, 0) for d in ids], w, label=label)
    ax.set_xticks(x + w * (len(series) - 1) / 2)
    ax.set_xticklabels(ids, rotation=30, ha="right", fontsize=7)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8)


def main(argv=None) -> int:
    """Entry point."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--demo-dir", default="data/demo")
    args = ap.parse_args(argv)
    figdir = os.path.join(args.run_dir, "figures")
    os.makedirs(figdir, exist_ok=True)
    runs, _integ = _load(args.run_dir)
    manifest = []
    run_id = runs[0]["run_id"] if runs else ""
    ids = sorted({r["dataset_id"] for r in runs if r["protocol"] == "local-structured"})

    enc_tp = _means(runs, "encrypt", "throughput_mib_s")
    dec_tp = _means(runs, "decrypt", "throughput_mib_s")
    fig, ax = plt.subplots(figsize=(10, 4))
    _bar(ax, ids, [("encrypt", enc_tp), ("decrypt", dec_tp)],
         "MiB/s", "Mean throughput by demo dataset (local-structured, measured runs)")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "demo_throughput.png"), dpi=150)
    fig.savefig(os.path.join(figdir, "demo_throughput.svg"))
    plt.close(fig)
    manifest.append(("demo-throughput", "demo_throughput.png",
                     "results/raw/benchmark_runs.csv", ids))

    enc_el = _means(runs, "encrypt", "elapsed_seconds")
    dec_el = _means(runs, "decrypt", "elapsed_seconds")
    fig, ax = plt.subplots(figsize=(10, 4))
    _bar(ax, ids, [("encrypt", enc_el), ("decrypt", dec_el)],
         "seconds (log)", "Mean elapsed time by demo dataset (log scale)")
    ax.set_yscale("log")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "demo_elapsed.png"), dpi=150)
    fig.savefig(os.path.join(figdir, "demo_elapsed.svg"))
    plt.close(fig)
    manifest.append(("demo-elapsed", "demo_elapsed.png",
                     "results/raw/benchmark_runs.csv", ids))

    ent_orig, ent_cipher, ent_rec = {}, {}, {}
    for r in runs:
        if r["protocol"] == "local-structured" and r["status"] == "ok" \
                and str(r["warmup"]).lower() in ("false", "0", ""):
            if r["phase"] == "encrypt":
                ent_orig.setdefault(r["dataset_id"], []).append(float(r["entropy_input"]))
                ent_cipher.setdefault(r["dataset_id"], []).append(float(r["entropy_output"]))
            else:
                ent_rec.setdefault(r["dataset_id"], []).append(float(r["entropy_output"]))
    avg = lambda d: {k: float(np.mean(v)) for k, v in d.items()}
    fig, ax = plt.subplots(figsize=(10, 4))
    _bar(ax, ids, [("original", avg(ent_orig)), ("ciphertext", avg(ent_cipher)),
                   ("recovered", avg(ent_rec))],
         "bits/byte", "Shannon entropy: original / ciphertext / recovered")
    ax.set_ylim(0, 8.2)
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "demo_entropy.png"), dpi=150)
    fig.savefig(os.path.join(figdir, "demo_entropy.svg"))
    plt.close(fig)
    manifest.append(("demo-entropy", "demo_entropy.png",
                     "results/raw/benchmark_runs.csv", ids))

    # Histogram (DEMO-005 pseudorandom) + scatter (DEMO-004 structured):
    # byte arrays come from demo files; ciphertext via one fresh encryption.
    sys.path.insert(0, "src")
    from pm_bg_aes.crypto import decrypt_bytes, encrypt_bytes  # noqa: E402

    with open(os.path.join(args.demo_dir, "demo_005_pseudorandom_100k.bin"), "rb") as f:
        h_orig = f.read()
    h_ct, _, _, _ = encrypt_bytes(h_orig, "PMBG-AES-DEMO-2026")
    ho = np.bincount(np.frombuffer(h_orig, dtype=np.uint8), minlength=256)
    hc = np.bincount(np.frombuffer(h_ct, dtype=np.uint8), minlength=256)
    fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
    axes[0].bar(range(256), ho)
    axes[0].set_title("DEMO-005 original byte histogram (n=100000)")
    axes[1].bar(range(256), hc)
    axes[1].set_title("DEMO-005 ciphertext byte histogram (whole file incl. header)")
    axes[1].set_xlabel("byte value")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "demo_hist_DEMO-005.png"), dpi=150)
    fig.savefig(os.path.join(figdir, "demo_hist_DEMO-005.svg"))
    plt.close(fig)
    manifest.append(("demo-hist-DEMO-005", "demo_hist_DEMO-005.png",
                     "data/demo/demo_005_pseudorandom_100k.bin + fresh encryption",
                     ["DEMO-005"]))

    with open(os.path.join(args.demo_dir, "demo_004_structured_text.txt"), "rb") as f:
        s_orig = f.read()
    s_ct, _, _, _ = encrypt_bytes(s_orig, "PMBG-AES-DEMO-2026")
    so = np.frombuffer(s_orig, dtype=np.uint8).astype(float)
    sc = np.frombuffer(s_ct, dtype=np.uint8).astype(float)
    idx = np.linspace(0, len(so) - 2, min(4000, len(so) - 1)).astype(int)
    idxc = np.linspace(0, len(sc) - 2, min(4000, len(sc) - 1)).astype(int)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharex=True, sharey=True)
    axes[0].scatter(so[idx], so[idx + 1], s=1, alpha=0.4)
    axes[0].set_title("DEMO-004 original: byte[i] vs byte[i+1]")
    axes[1].scatter(sc[idxc], sc[idxc + 1], s=1, alpha=0.4)
    axes[1].set_title("DEMO-004 ciphertext: byte[i] vs byte[i+1]")
    for a in axes:
        a.set_xlabel("byte[i]")
    axes[0].set_ylabel("byte[i+1]")
    fig.tight_layout()
    fig.savefig(os.path.join(figdir, "demo_scatter_DEMO-004.png"), dpi=150)
    fig.savefig(os.path.join(figdir, "demo_scatter_DEMO-004.svg"))
    plt.close(fig)
    manifest.append(("demo-scatter-DEMO-004", "demo_scatter_DEMO-004.png",
                     "data/demo/demo_004_structured_text.txt + fresh encryption",
                     ["DEMO-004"]))

    with open(os.path.join(figdir, "figure_manifest.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["figure_id", "file_path", "data_source", "script",
                    "command", "dataset_id", "description",
                    "manuscript_mapping", "status"])
        for fig_id, fname, source, dsids in manifest:
            stem = fname.rsplit(".", 1)[0]
            for ext in ("png", "svg"):
                w.writerow([fig_id, f"results/figures/{stem}.{ext}", source,
                            "scripts/generate_figures.py",
                            f"python scripts/generate_figures.py --run-dir <run> --demo-dir {args.demo_dir}",
                            ";".join(dsids),
                            f"{fig_id} from new local demo measurements",
                            "demo equivalent only; not a manuscript figure",
                            "generated"])
    print(f"wrote {len(manifest)} figures (+svg) to {figdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
