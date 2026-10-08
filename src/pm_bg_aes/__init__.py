"""PM-BG-AES archival implementation.

Faithful modular port of the canonical notebook cell
(``PM_BG_+_AES_(works)_ori.ipynb`` cell 1, ``7495Mw2mNX3t`` — byte-identical
to workshop cell 1). Colab-only I/O (``google.colab.files``,
``input()``, ``!pip install``) is adapted to local file paths; algorithmic
semantics are preserved (see ``docs/source_traceability.csv``).

Not for production use: unauthenticated, single-pass SHA-256 key derivation,
no security proof. See ``docs/limitations.md``.
"""

from pm_bg_aes.aes_tail import aes_decrypt, aes_encrypt, derive_key_string
from pm_bg_aes.crypto import (
    CipherFormatError,
    decrypt_bytes,
    decrypt_file,
    encrypt_bytes,
    encrypt_file,
)
from pm_bg_aes.entropy import shannon_entropy
from pm_bg_aes.file_format import (
    SUPPORTED_N,
    pack_header,
    parse_header,
    unpack_ciphertext,
)
from pm_bg_aes.integrity import md5_bytes, md5_file, sha256_bytes, sha256_file
from pm_bg_aes.permutation import key_matrix
from pm_bg_aes.selector import SUPPORTED_SIZES, select_matrix_size

__all__ = [
    "aes_decrypt",
    "aes_encrypt",
    "derive_key_string",
    "CipherFormatError",
    "decrypt_bytes",
    "decrypt_file",
    "encrypt_bytes",
    "encrypt_file",
    "shannon_entropy",
    "SUPPORTED_N",
    "pack_header",
    "parse_header",
    "unpack_ciphertext",
    "md5_bytes",
    "md5_file",
    "sha256_bytes",
    "sha256_file",
    "key_matrix",
    "SUPPORTED_SIZES",
    "select_matrix_size",
]

__version__ = "1.0.0"
