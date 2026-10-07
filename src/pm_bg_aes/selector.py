"""Rule-based matrix-size selector, faithful to ``pilih_matriks_ai``.

The notebook calls this the "AI selector"; the implementation is a
deterministic conditional rule table over (file size in **bytes**, Shannon
entropy in bits/byte) — not a trained machine-learning model. All docs use
the accurate term "rule-based selector" and note the notebook's wording.

Thresholds (bytes, preserved exactly; NOT KiB/MiB)::

    filesize < 50000:    n = 4  if entropy < 5   else 6
    filesize < 500000:   n = 8  if entropy < 6   else 12
    filesize < 5000000:  n = 16 if entropy < 7   else 24
    else:                n = 32 if entropy < 7.5 else 48
"""

from pm_bg_aes.entropy import shannon_entropy

__all__ = ["SUPPORTED_SIZES", "select_matrix_size", "select_matrix_size_for"]

SUPPORTED_SIZES = (4, 6, 8, 12, 16, 24, 32, 48)


def select_matrix_size_for(filesize: int, entropy: float) -> int:
    """Pure rule table: (size in bytes, entropy) -> n. Boundary-testable."""
    if filesize < 50000:
        return 4 if entropy < 5 else 6
    if filesize < 500000:
        return 8 if entropy < 6 else 12
    if filesize < 5000000:
        return 16 if entropy < 7 else 24
    return 32 if entropy < 7.5 else 48


def select_matrix_size(data) -> int:
    """Select n for a byte sequence (computes entropy, like the notebook)."""
    import numpy as np

    arr = np.asarray(data, dtype=np.uint8).ravel()
    return select_matrix_size_for(int(arr.size), shannon_entropy(arr))
