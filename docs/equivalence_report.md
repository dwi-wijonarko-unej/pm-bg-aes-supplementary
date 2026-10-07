# Equivalence Report — Package vs. Notebook Reference

`tests/test_equivalence.py` compares `src/pm_bg_aes/*` against
`tests/notebook_reference.py` (verbatim-logic port of canonical ori cell 1;
only I/O adapted, fixed IV injected into **both** sides by the harness —
production default remains random IV).

## Compared (and equal)

- Selector `n` and `len_hill` for payloads of 0, 16, 37, 44, 64, 1000, 6000
  bytes (empty, block-aligned, residual, low/high entropy).
- Permutation matrix `P` and inverse `P.T` for the exercised `n` values.
- Full ciphertext byte-equality under fixed IV (header + hill + AES tail).
- Cross-decryption: package decrypts reference ciphertext and vice versa;
  recovered bytes equal the original in all cases.
- Non-AES segments (header + hill payload) equal under random IV; recovery
  exact.

## Not compared byte-for-byte

- Random-IV ciphertexts across runs (expected to differ; IV is random by
  design — both sides).
- Console prints / Colab upload-download (adapted, not cryptographic).
- `kunci_permutasi(..., 'e')` second return (`0` vs `None`): discarded by
  every caller on both sides; no behavioural effect.

## Verdict

`pytest tests/test_equivalence.py` — all pass (see
`results/logs/test_report.txt`). The packaged implementation is
behaviour-equivalent to the canonical notebook cell on all exercised inputs.
Wrong-password and malformed-input behaviour is covered in
`tests/test_aes_tail.py` / `tests/test_crypto_format.py` with the
non-guarantee documented in `docs/limitations.md`.
