import numpy as np
import pytest

from pm_bg_aes.crypto import decrypt_bytes, encrypt_bytes, split_payload
from pm_bg_aes.file_format import CipherFormatError, pack_header, parse_header, unpack_ciphertext
from pm_bg_aes.integrity import md5_bytes, sha256_bytes


def test_header_pack_unpack_roundtrip():
    h = pack_header(24, 2006736)
    assert len(h) == 12 and list(h[:4]) == [0, 0, 0, 24]
    assert parse_header(h) == (24, 2006736)


def test_full_file_roundtrip_small_and_zero_residual():
    plain = bytes([i % 4 for i in range(6000)])  # entropy 2.0 -> n=4
    blob, n, len_hill, shift = encrypt_bytes(plain, "44")
    assert (n, len_hill, shift) == (4, 6000, 0)
    assert decrypt_bytes(blob, "44") == plain


def test_full_file_roundtrip_nonzero_residual():
    plain = b"A" * 5999 + b"BC"  # 6001 bytes
    blob, n, len_hill, shift = encrypt_bytes(plain, "44")
    assert shift == 6001 % n and len_hill == 6001 - shift
    assert decrypt_bytes(blob, "44") == plain


def test_empty_file_roundtrip():
    blob, n, len_hill, shift = encrypt_bytes(b"", "44")
    assert (n, len_hill, shift) == (4, 0, 0)
    assert decrypt_bytes(blob, "44") == b""


def test_byte_and_hash_equality():
    plain = bytes(range(256)) * 10
    recovered = decrypt_bytes(encrypt_bytes(plain, "222")[0], "222")
    assert recovered == plain
    assert sha256_bytes(recovered) == sha256_bytes(plain)
    assert md5_bytes(recovered) == md5_bytes(plain)


def test_split_payload():
    assert split_payload(2006753, 24) == (2006736, 17)


@pytest.mark.parametrize("mutate", ["short-header", "bad-n", "bad-lenhill", "truncated", "short-tail"])
def test_malformed_ciphertext_raises(mutate):
    blob, *_ = encrypt_bytes(b"hello world, padding test!!", "44")
    raw = bytearray(blob)
    if mutate == "short-header":
        raw = raw[:7]
    elif mutate == "bad-n":
        raw[:4] = (99).to_bytes(4, "big")
    elif mutate == "bad-lenhill":
        raw[4:12] = (999).to_bytes(8, "big")
    elif mutate == "truncated":
        raw = raw[: len(raw) - 5]
    elif mutate == "short-tail":
        _n, lh = parse_header(bytes(raw[:12]))
        raw = raw[: 12 + lh + 20]  # 20-byte tail: malformed (needs >=32, %16==0)
    with pytest.raises((CipherFormatError, ValueError)):
        decrypt_bytes(bytes(raw), "44")


def test_unpack_rejects_bad_tail_size():
    blob, n, lh, _s = encrypt_bytes(b"0123456789abcdef" * 3, "44")
    cut = bytearray(blob[: 12 + lh + 20])  # 20-byte tail: >=16 IV but malformed
    with pytest.raises(CipherFormatError):
        unpack_ciphertext(bytes(cut))
