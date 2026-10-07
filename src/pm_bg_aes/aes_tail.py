"""AES-CBC residual tail, faithful to ``aes_encrypt``/``aes_decrypt``.

Preserved exactly:

* key derivation: ``"0." + str(password) + "1"``, UTF-8 encoded, single-pass
  SHA-256 digest as the 32-byte (AES-256) key;
* random IV from the library (``cipher.iv``), prepended to the ciphertext;
* PKCS#7 pad/unpad with ``AES.block_size`` (16);
* encrypt returns ``list(iv + ciphertext)``; decrypt splits IV at 16 bytes.

No password validation is performed (the notebook's "digits only" prompt is
not enforced by its code — see ``docs/limitations.md`` Q10). No salt, no
KDF iterations, no authentication tag; documented as future work, not
implemented here (archival mode forbids silent security changes).
"""

import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

__all__ = ["derive_key_string", "derive_key", "aes_encrypt", "aes_decrypt"]


def derive_key_string(password) -> str:
    """Build the derivation string ``"0." + str(password) + "1"``."""
    return "0." + str(password) + "1"


def derive_key(password) -> bytes:
    """Single-pass SHA-256 digest of the derivation string (AES-256 key)."""
    return hashlib.sha256(derive_key_string(password).encode()).digest()


def aes_encrypt(message, password, iv: bytes = None) -> list:
    """Encrypt tail bytes; ``iv`` override exists for tests only (None = random)."""
    data = bytes(message)
    cipher = AES.new(derive_key(password), AES.MODE_CBC, iv=iv) if iv is not None else AES.new(derive_key(password), AES.MODE_CBC)
    return list(cipher.iv + cipher.encrypt(pad(data, AES.block_size)))


def aes_decrypt(data, password) -> list:
    """Decrypt an ``IV + ciphertext`` tail; raises ``ValueError`` on bad padding/key."""
    raw = bytes(data)
    cipher = AES.new(derive_key(password), AES.MODE_CBC, iv=raw[: AES.block_size])
    return list(unpad(cipher.decrypt(raw[AES.block_size :]), AES.block_size))
