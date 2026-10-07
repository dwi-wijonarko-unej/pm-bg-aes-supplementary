"""Core encrypt/decrypt pipeline (no prints, no timing, no CLI).

Faithful to canonical ``enkripsi``/``dekripsi``::

    mp = uint8(input); n = selector(mp); p, q = n//2, n-n//2
    len_shift = N % n; len_hill = N - len_shift
    hill = (P @ mp[:len_hill].reshape(n, len_hill/n) % 256).u8  [int32 mult]
    tail = AES(iv + CBC(SHA256("0."+pw+"1"), pad(mp[len_hill:])))
    out  = header(n, len_hill) + hill.flat + tail
    decrypt: parse header, split, P.T @ hill % 256, AES-decrypt tail, concat.

``decrypt`` with a wrong password raises ``ValueError`` (invalid padding)
in the common case, but this format has no authentication tag, so detection
is NOT guaranteed — see ``docs/limitations.md``. Zero-residual files still
carry one AES padding block, so a wrong password is still normally caught
by unpad; tests assert behaviour only where deterministic.
"""

import numpy as np

from pm_bg_aes.aes_tail import aes_decrypt, aes_encrypt
from pm_bg_aes.file_format import CipherFormatError, pack_header, unpack_ciphertext
from pm_bg_aes.permutation import key_matrix, split_n
from pm_bg_aes.selector import select_matrix_size

__all__ = [
    "CipherFormatError",
    "split_payload",
    "hill_encrypt",
    "hill_decrypt",
    "encrypt_bytes",
    "decrypt_bytes",
    "encrypt_file",
    "decrypt_file",
]


def split_payload(nbytes: int, n: int) -> tuple:
    """Return ``(len_hill, len_shift)`` for input length and matrix order."""
    len_shift = nbytes % n
    return nbytes - len_shift, len_shift


def hill_encrypt(main: np.ndarray, n: int) -> np.ndarray:
    """Permutation-transform of the main part (encrypt direction)."""
    P, _ = key_matrix(n)
    mat = np.asarray(main, dtype=np.uint8).ravel()[: len(main)].reshape(n, len(main) // n)
    return (np.dot(P.astype(np.int32), mat.astype(np.int32)) % 256).astype(np.uint8)


def hill_decrypt(hill: np.ndarray, n: int) -> np.ndarray:
    """Inverse permutation-transform (decrypt direction, ``P.T``)."""
    _, Pt = key_matrix(n, for_decrypt=True)
    mat = np.asarray(hill, dtype=np.uint8).ravel().reshape(n, len(np.asarray(hill).ravel()) // n)
    return (np.dot(Pt.astype(np.int32), mat.astype(np.int32)) % 256).astype(np.uint8)


def encrypt_bytes(plaintext: bytes, password, n: int = None) -> tuple:
    """Encrypt bytes; return ``(ciphertext_bytes, n, len_hill, len_shift)``."""
    mp = np.frombuffer(bytes(plaintext), dtype=np.uint8).copy()
    if n is None:
        n = select_matrix_size(mp)
    p, q = split_n(n)  # noqa: F841 — partition kept for provenance parity
    len_hill, _len_shift = split_payload(int(mp.size), n)
    hill = hill_encrypt(mp[:len_hill], n).reshape(len_hill) if len_hill else np.empty(0, dtype=np.uint8)
    tail = np.array(aes_encrypt(mp[len_hill:], password), dtype=np.uint8)
    blob = np.concatenate((pack_header(n, len_hill), hill, tail))
    return bytes(blob), n, len_hill, _len_shift


def decrypt_bytes(ciphertext: bytes, password) -> bytes:
    """Decrypt bytes; raises :class:`CipherFormatError` or ``ValueError``."""
    mc = np.frombuffer(bytes(ciphertext), dtype=np.uint8).copy()
    n, len_hill, hill_part, aes_part = unpack_ciphertext(mc)
    main = hill_decrypt(hill_part, n).reshape(len_hill) if len_hill else np.empty(0, dtype=np.uint8)
    tail = np.array(aes_decrypt(aes_part.tolist(), password), dtype=np.uint8)
    return bytes(np.concatenate((main, tail)))


def encrypt_file(input_path: str, output_path: str, password, n: int = None) -> dict:
    """Encrypt a file; return ``{n, len_hill, len_shift, sizes}`` metadata."""
    with open(input_path, "rb") as f:
        blob, n, len_hill, len_shift = encrypt_bytes(f.read(), password, n)
    with open(output_path, "wb") as f:
        f.write(blob)
    return {"n": n, "len_hill": len_hill, "len_shift": len_shift,
            "input_size": len(open(input_path, "rb").read()), "output_size": len(blob)}


def decrypt_file(input_path: str, output_path: str, password) -> dict:
    """Decrypt a file; return ``{n, len_hill, sizes}`` metadata."""
    with open(input_path, "rb") as f:
        plain = decrypt_bytes(f.read(), password)
    with open(output_path, "wb") as f:
        f.write(plain)
    return {"output_size": len(plain)}
