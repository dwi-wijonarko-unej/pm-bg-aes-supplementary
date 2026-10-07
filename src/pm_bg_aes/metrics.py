"""Metrics reporting: notebook-compatible report + structured local protocol.

``report_notebook_style`` reproduces ``cetak_laporan_performa`` exactly
(throughput denominator = input size, divisor ``1024*1024`` — i.e. MiB/s
units despite the notebook's "MB/detik" label; see ``docs/limitations.md``).

``summarize`` aggregates measured runs (warmup excluded): count, mean,
median, sample stdev (``statistics.stdev``, n>=2), min, max.
"""

import statistics

__all__ = ["throughput_mib_s", "format_notebook_report", "summarize"]


def throughput_mib_s(size_bytes: int, elapsed_s: float) -> float:
    """Throughput in MiB/s (``size / 1024**2 / elapsed``)."""
    return (size_bytes / (1024 * 1024)) / elapsed_s if elapsed_s > 0 else 0.0


def format_notebook_report(title, elapsed, peak_kb, cpu, orig_size, proc_size,
                           orig_entropy, proc_entropy) -> str:
    """Render the ``cetak_laporan_performa`` report text (units labelled honestly)."""
    throughput = throughput_mib_s(orig_size, elapsed)
    lines = [
        "",
        "=" * 80,
        f" METRIKS EVALUASI PERFORMA METODE ({title.upper()}) [notebook-compatible; MiB/s]",
        "=" * 80,
        f" [1] Waktu Eksekusi         : {elapsed:.4f} detik",
        f" [2] Throughput             : {throughput:.2f} MiB/detik",
        f" [3] Traced Peak Allocation : {peak_kb:.2f} KB ({peak_kb / 1024:.2f} MB) [tracemalloc, not RSS]",
        f" [4] Penggunaan CPU         : {cpu:.1f} % [psutil sample]",
        f" [5] Ukuran File Input      : {orig_size} bytes",
        f" [6] Ukuran File Output     : {proc_size} bytes (Overhead: {proc_size - orig_size:+d} bytes)",
        f" [7] Shannon Entropy (Input): {orig_entropy:.4f} / 8.0",
        f" [8] Shannon Entropy (Output): {proc_entropy:.4f} / 8.0",
        "=" * 80,
        "",
    ]
    return "\n".join(lines)


def summarize(values: list) -> dict:
    """Summary stats over measured (non-warmup) values."""
    vals = [float(v) for v in values]
    out = {"count": len(vals), "mean": None, "median": None, "stdev": None,
           "min": None, "max": None}
    if not vals:
        return out
    out["mean"] = statistics.mean(vals)
    out["median"] = statistics.median(vals)
    out["min"] = min(vals)
    out["max"] = max(vals)
    out["stdev"] = statistics.stdev(vals) if len(vals) >= 2 else 0.0
    return out
