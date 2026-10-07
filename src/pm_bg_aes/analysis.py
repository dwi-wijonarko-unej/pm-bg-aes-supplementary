"""Derived transparency analyses (category E — NOT in the notebook).

Included: byte-frequency histogram, Shannon entropy, adjacent-byte Pearson
correlation (NaN when either lagged variance is zero), chi-square
goodness-of-fit vs. the uniform byte distribution (with scipy p-value when
scipy is available; else ``p_value=None``), and exact original-vs-recovered
equality.

Explicitly NOT claimed: any security proof, IND-CPA/IND-CCA conclusion, or
"avalanche" analysis (arrays of different lengths are never compared
without a stated alignment; ciphertext headers/overhead are documented).
Chi-square p-values near underflow are reported as returned by the library
with the statistic kept; never as "exactly zero probability".
"""

import math

import numpy as np

__all__ = [
    "byte_histogram",
    "adjacent_correlation",
    "chi_square_uniform",
    "byte_divergence_same_length",
]


def byte_histogram(data) -> np.ndarray:
    """256-bin counts over bytes 0..255."""
    arr = np.asarray(data, dtype=np.uint8).ravel()
    return np.bincount(arr, minlength=256).astype(np.int64)


def adjacent_correlation(data) -> float:
    """Pearson r between ``x[:-1]`` and ``x[1:]``; NaN if variance is zero."""
    arr = np.asarray(data, dtype=np.uint8).ravel().astype(np.float64)
    if arr.size < 2:
        return float("nan")
    x, y = arr[:-1], arr[1:]
    if x.std() == 0.0 or y.std() == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def chi_square_uniform(data) -> dict:
    """Chi-square vs. discrete-uniform over 256 byte values.

    Returns ``{statistic, dof, p_value, n, expected}``. Expected counts
    require ``n / 256 >= 1`` for the statistic to be meaningful; small
    samples are still computed but flagged via ``expected < 5`` in notes.
    """
    counts = byte_histogram(data).astype(np.float64)
    n = float(counts.sum())
    if n == 0:
        return {"statistic": float("nan"), "dof": 255, "p_value": None,
                "n": 0, "expected": 0.0, "note": "empty input"}
    expected = n / 256.0
    stat = float(np.sum((counts - expected) ** 2 / expected))
    p_value = None
    try:
        from scipy.stats import chi2 as _chi2

        p_value = float(_chi2.sf(stat, 255))
    except Exception:
        p_value = None
    return {"statistic": stat, "dof": 255, "p_value": p_value, "n": n,
            "expected": expected,
            "note": "expected<5; approximate" if expected < 5 else "ok"}


def byte_divergence_same_length(a: bytes, b: bytes) -> dict:
    """Fraction of differing bytes; requires equal length (alignment defined)."""
    ra = np.frombuffer(bytes(a), dtype=np.uint8)
    rb = np.frombuffer(bytes(b), dtype=np.uint8)
    if ra.size != rb.size:
        raise ValueError(
            f"length mismatch {ra.size} != {rb.size}: no alignment assumed"
        )
    if ra.size == 0:
        return {"divergence": float("nan"), "differing": 0, "n": 0}
    diff = int(np.count_nonzero(ra != rb))
    return {"divergence": diff / ra.size, "differing": diff, "n": int(ra.size)}
