import numpy as np
import pytest

from pm_bg_aes import aes_tail
from pm_bg_aes.aes_tail import aes_decrypt, aes_encrypt, derive_key_string


def test_key_derivation_string_format():
    assert derive_key_string("44") == "0.441"
    assert derive_key_string(222) == "0.2221"


def test_aes_tail_roundtrip_random_iv():
    msg = list(np.arange(37, dtype=np.uint8))
    assert aes_decrypt(aes_encrypt(msg, "44"), "44") == msg


def test_aes_tail_empty_message_roundtrip():
    assert aes_decrypt(aes_encrypt([], "44"), "44") == []


def test_aes_tail_fixed_iv_deterministic_for_harness():
    iv = bytes(range(16))
    a = aes_encrypt([1, 2, 3], "44", iv=iv)
    b = aes_encrypt([1, 2, 3], "44", iv=iv)
    assert a == b and bytes(a[:16]) == iv


def test_aes_tail_iv_is_16_bytes_prefix():
    out = aes_encrypt([9] * 5, "44")
    assert len(out) >= 32 and len(out) % 16 == 0


def test_wrong_password_not_silently_trusted():
    """Unauthenticated format: wrong password must never return original bytes."""
    good = aes_encrypt(list(range(50)), "44")
    try:
        bad = aes_decrypt(good, "wrong")
    except ValueError:
        return  # common case: invalid padding
    assert bad != list(range(50))
