"""Ciphertext file format: header pack/parse with structural validation.

Layout (offsets in bytes)::

    0..4    n        uint32 big-endian  (matrix order)
    4..12   len_hill uint64 big-endian  (main-part length)
    12..    hill payload (len_hill bytes, permutation-transformed)
    ..      AES tail (16-byte IV + PKCS#7 ciphertext of the residual)

Validation raises :class:`CipherFormatError` (an engineering addition: the
notebook would crash with reshape/IndexError on malformed input). Valid
inputs produce byte-identical outputs to the notebook.
"""

import numpy as np

from pm_bg_aes.selector import SUPPORTED_SIZES

__all__ = [
    "HEADER_LEN",
    "SUPPORTED_N",
    "CipherFormatError",
    "pack_header",
    "parse_header",
    "unpack_ciphertext",
]

HEADER_LEN = 12
SUPPORTED_N = SUPPORTED_SIZES


class CipherFormatError(ValueError):
    """Malformed ciphertext header or truncated payload."""


def _as_u8(blob) -> np.ndarray:
    """View bytes-like or array input as a flat uint8 array."""
    if isinstance(blob, (bytes, bytearray, memoryview)):
        return np.frombuffer(bytes(blob), dtype=np.uint8)
    return np.asarray(blob, dtype=np.uint8).ravel()


def pack_header(n: int, len_hill: int) -> np.ndarray:
    """Pack ``(n, len_hill)`` into 12 header bytes (uint8 array)."""
    return np.array(
        list(int(n).to_bytes(4, byteorder="big"))
        + list(int(len_hill).to_bytes(8, byteorder="big")),
        dtype=np.uint8,
    )


def parse_header(blob) -> tuple:
    """Parse and validate the 12-byte header; return ``(n, len_hill)``."""
    raw = _as_u8(blob)
    if raw.size < HEADER_LEN:
        raise CipherFormatError(
            f"header too short: {raw.size} bytes, need {HEADER_LEN}"
        )
    n = int.from_bytes(bytes(raw[:4]), byteorder="big")
    len_hill = int.from_bytes(bytes(raw[4:12]), byteorder="big")
    if n not in SUPPORTED_N:
        raise CipherFormatError(f"unsupported matrix size n={n}")
    if len_hill % n != 0:
        raise CipherFormatError(f"len_hill={len_hill} not divisible by n={n}")
    return n, len_hill


def unpack_ciphertext(blob) -> tuple:
    """Split a ciphertext blob into ``(n, len_hill, hill_part, aes_part)``."""
    raw = _as_u8(blob)
    n, len_hill = parse_header(raw)
    if HEADER_LEN + len_hill > raw.size:
        raise CipherFormatError(
            f"payload truncated: need {HEADER_LEN + len_hill} bytes, "
            f"have {raw.size}"
        )
    hill_part = raw[HEADER_LEN : HEADER_LEN + len_hill]
    aes_part = raw[HEADER_LEN + len_hill :]
    if aes_part.size < 32 or aes_part.size % 16 != 0:
        raise CipherFormatError(
            f"malformed AES tail: {aes_part.size} bytes "
            "(need >= 32 and multiple of 16: 16-B IV + blocks)"
        )
    return n, len_hill, hill_part, aes_part
