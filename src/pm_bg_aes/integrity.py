"""Integrity digests: SHA-256 (primary) and MD5 (legacy comparison only).

The notebook defines ``md5(fname)`` over 4096-byte chunks; MD5 is kept solely
as the legacy comparison digest the manuscript uses alongside SHA-256, never
as a security mechanism.
"""

import hashlib

__all__ = ["sha256_bytes", "sha256_file", "md5_bytes", "md5_file"]


def sha256_bytes(data: bytes) -> str:
    """Hex SHA-256 of bytes."""
    return hashlib.sha256(bytes(data)).hexdigest()


def sha256_file(path: str) -> str:
    """Hex SHA-256 of a file (streamed)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def md5_bytes(data: bytes) -> str:
    """Hex MD5 of bytes (legacy comparison only)."""
    return hashlib.md5(bytes(data)).hexdigest()


def md5_file(path: str) -> str:
    """Hex MD5 of a file in 4096-byte chunks, as in the notebook."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()
