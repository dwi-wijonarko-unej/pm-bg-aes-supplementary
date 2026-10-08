# Ciphertext File Format

```
offset  size  field      dtype   endianness  notes
0       4     n          uint32  big         matrix order; must be in {4,6,8,12,16,24,32,48}
4       8     len_hill   uint64  big         main-part length; must satisfy len_hill % n == 0
12      len_hill  hill   uint8   —           permutation-transformed bytes (C-order flatten)
12+len_hill  variable  aes_tail uint8 —      16-byte IV + k×16-byte CBC ciphertext (k>=1)
```

For nonnegative residual length `len_shift`, the precise size is:

```text
aes_tail_size = 16 + 16 * (floor(len_shift / 16) + 1)
total_size = 12 + len_hill + aes_tail_size
```

PKCS#7 always adds 1..16 bytes, so the tail is at least 32 bytes, including
its IV. F9's available ciphertext has `n=32`, `len_hill=5423488` and no
plaintext residual; its 32-byte AES segment and 12-byte header still add
44 bytes. This segment is not evidence of a Shift128 plaintext residual.
See `docs/evidence_audit.md`.

## Structural validation (`unpack_ciphertext`)

1. fewer than 12 bytes → `CipherFormatError("header too short")`;
2. `n` outside the supported set → error (the notebook would silently build
   a wrong-size matrix or crash in reshape);
3. `len_hill % n != 0` → error;
4. `12 + len_hill > total` → truncated-payload error;
5. AES tail `< 32` bytes or not a multiple of 16 → malformed-tail error;
6. wrong password / tampered tail → `ValueError` from unpad (common but NOT
   guaranteed — the format is unauthenticated; validation is structural, not
   a tamper proof).
