"""Byte Shannon entropy (base 2), faithful to notebook ``hitung_entropy``.

Source::

    hist = np.bincount(data, minlength=256)
    prob = hist / np.sum(hist)
    entropy = -np.sum([p * np.log2(p) for p in prob if p > 0])

Engineering edge case: the notebook has no empty-input guard (empty input
raises ``RuntimeWarning`` and yields ``-0.0``). This module returns ``0.0``
for empty input explicitly; documented in ``docs/algorithm.md``.
"""

import numpy as np

__all__ = ["shannon_entropy"]


def shannon_entropy(data) -> float:
    """Shannon entropy (bits/byte) of a uint8 byte sequence."""
    arr = np.asarray(data, dtype=np.uint8).ravel()
    if arr.size == 0:
        return 0.0
    hist = np.bincount(arr, minlength=256)
    prob = hist / np.sum(hist)
    return float(-np.sum([p * np.log2(p) for p in prob if p > 0]))
