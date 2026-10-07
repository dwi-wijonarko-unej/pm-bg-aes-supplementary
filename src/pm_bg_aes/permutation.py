"""Permutation matrix from the K_{p,q} construction, faithful to ``kunci_permutasi``.

Source semantics preserved::

    p = n // 2; q = n - p
    P = eye(n, int32); perm = arange(n)
    if q >= 2: swap rows p, p+1
    if q >= 4: swap rows p+2, p+3
    P = P[perm, :]; inverse = P.T

The notebook's ``ed='e'`` second return is ``0`` (cells 0–1) or the identity
(workshop cell 2); callers always discard it. Here ``key_matrix(n)`` returns
``(P, None)`` for encryption and ``(P, P.T)`` for decryption to make the
inverse explicit without changing any output byte.
"""

import numpy as np

__all__ = ["split_n", "permutation_order", "key_matrix"]


def split_n(n: int) -> tuple:
    """Partition ``n`` into ``(p, q) = (n // 2, n - n // 2)``."""
    p = n // 2
    return p, n - p


def permutation_order(n: int) -> list:
    """Row-permutation order applied to the identity matrix."""
    p, q = split_n(n)
    perm = list(range(n))
    if q >= 2:
        perm[p], perm[p + 1] = perm[p + 1], perm[p]
    if q >= 4:
        perm[p + 2], perm[p + 3] = perm[p + 3], perm[p + 2]
    return perm


def key_matrix(n: int, for_decrypt: bool = False) -> tuple:
    """Return ``(P, inverse)``; inverse is ``None`` (encrypt) or ``P.T``."""
    P = np.eye(n, dtype=np.int32)[permutation_order(n), :]
    if for_decrypt:
        return P, P.T.copy()
    return P, None
