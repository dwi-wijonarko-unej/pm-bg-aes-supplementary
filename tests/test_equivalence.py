"""Equivalence: package vs. verbatim notebook reference (category C vs. A).

Compares n, len_hill, permutation matrix, main transformed bytes, header
parsing, and recovered bytes. Full-ciphertext equality is asserted under a
fixed IV injected into BOTH implementations via the test harness only
(production default remains random IV).
"""

import numpy as np
import pytest
from Crypto.Cipher import AES as _AES_module

import tests.notebook_reference as ref
from pm_bg_aes import aes_tail as pkg_aes
from pm_bg_aes.crypto import decrypt_bytes, encrypt_bytes
from pm_bg_aes.file_format import parse_header
from pm_bg_aes.permutation import key_matrix

FIXED_IV = bytes(range(16))
_orig_new = _AES_module.new


def _fixed_iv_new(key, mode, *args, **kwargs):
    if not args and "iv" not in kwargs:
        kwargs["iv"] = FIXED_IV
    return _orig_new(key, mode, *args, **kwargs)


@pytest.fixture()
def fixed_iv(monkeypatch):
    """Inject deterministic IV into both implementations (test-only)."""
    monkeypatch.setattr(_AES_module, "new", _fixed_iv_new)
    monkeypatch.setattr(pkg_aes.AES, "new", _fixed_iv_new)
    return FIXED_IV


PAYLOADS = [
    np.arange(64, dtype=np.uint8),
    np.frombuffer(b"hybrid-permutation-aes demo payload 0123456789!@#", dtype=np.uint8).copy(),
    np.zeros(6000, dtype=np.uint8),
    (np.arange(1000, dtype=np.uint16) % 256).astype(np.uint8),
]


@pytest.mark.parametrize("i", range(len(PAYLOADS)))
def test_equivalence_deterministic_ciphertext(fixed_iv, i):
    mp = PAYLOADS[i]
    ref_blob, ref_n, ref_lh = ref.enkripsi_bytes(mp, "44", iv=FIXED_IV)
    pkg_blob, pkg_n, pkg_lh, _ = encrypt_bytes(bytes(mp), "44")
    assert pkg_n == ref_n and pkg_lh == ref_lh
    assert bytes(pkg_blob) == bytes(ref_blob)


def test_equivalence_matrices_and_recovery(fixed_iv):
    mp = PAYLOADS[1]
    n = int(ref.pilih_matriks_ai(mp))
    p, q = n // 2, n - n // 2
    refP, _ = ref.kunci_permutasi(p, q, "e")
    pkgP, _ = key_matrix(n)
    assert np.array_equal(np.asarray(pkgP), np.asarray(refP))
    _, refPt = ref.kunci_permutasi(p, q, "d")
    _, pkgPt = key_matrix(n, for_decrypt=True)
    assert np.array_equal(np.asarray(pkgPt), np.asarray(refPt))
    ref_blob, _, _ = ref.enkripsi_bytes(mp, "44", iv=FIXED_IV)
    pkg_blob, _, _, _ = encrypt_bytes(bytes(mp), "44")
    assert parse_header(bytes(ref_blob)) == parse_header(bytes(pkg_blob))
    assert bytes(ref.dekripsi_bytes(np.asarray(ref_blob), "44")) == bytes(mp)
    assert decrypt_bytes(bytes(ref_blob), "44") == bytes(mp)


def test_equivalence_empty_and_single_block():
    for raw in (b"", b"A" * 16, b"B" * 37):
        mp = np.frombuffer(raw, dtype=np.uint8).copy()
        ref_blob, ref_n, ref_lh = ref.enkripsi_bytes(mp, "7", iv=FIXED_IV)
        # package with random IV: compare non-AES segments + recovery
        pkg_blob, pkg_n, pkg_lh, _ = encrypt_bytes(raw, "7")
        assert (pkg_n, pkg_lh) == (ref_n, ref_lh)
        assert bytes(pkg_blob[: 12 + pkg_lh]) == bytes(ref_blob[: 12 + ref_lh])
        assert decrypt_bytes(bytes(ref_blob), "7") == raw
