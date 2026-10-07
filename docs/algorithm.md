# Algorithm (Archival, Faithful to Canonical Notebook Cell 1)

## Pipeline

Given input bytes `mp` (uint8 array, order preserved as read) and password
`password2`:

1. **Entropy**: 256-bin histogram over 0..255, Shannon base-2
   (`src/pm_bg_aes/entropy.py`). Empty input returns `0.0` (engineering
   edge case; the notebook emits a `RuntimeWarning` and `-0.0`).
2. **Rule-based selector** (`src/pm_bg_aes/selector.py`, thresholds in
   **bytes**):
   `<50000: 4/6 (ent<5)` · `<500000: 8/12 (ent<6)` ·
   `<5000000: 16/24 (ent<7)` · else `32/48 (ent<7.5)`.
   The notebook's "AI selector" wording refers to these conditional rules;
   there is no trained model in the supplied code.
3. **Partition**: `p = n//2`, `q = n-p`. Permutation matrix = identity with
   rows `p↔p+1` swapped if `q>=2`, plus rows `p+2↔p+3` if `q>=4`
   (`src/pm_bg_aes/permutation.py`). Inverse = transpose (orthogonality).
   No password-seeded shuffling, no extra swaps, no graph traversal at
   runtime; the `n!` key-space phrase in the manuscript is a combinatorial
   upper bound, not the implemented diversity (at most 4 distinct matrices
   per `n`). Do not claim otherwise.
4. **Split**: `len_shift = N % n` (AES tail), `len_hill = N - len_shift`
   (matrix part).
5. **Matrix transform**: `hill = (P_int32 @ main.reshape(n, len_hill/n)_int32)
   % 256 → uint8`, flattened in the same C order. Decrypt uses `P.T`.
6. **AES tail**: key = `SHA256("0."+str(password)+"1")`, random IV, AES-CBC,
   PKCS#7; output `IV + ciphertext` (`src/pm_bg_aes/aes_tail.py`).
   Actual behaviour: any password string is accepted (the "digits only"
   prompt is not enforced by the code).
7. **Container**: `header(n) + header(len_hill) + hill + aes_tail`; decrypt
   parses, splits, inverts, concatenates (`src/pm_bg_aes/crypto.py`,
   `src/pm_bg_aes/file_format.py`).

## Engineering vs. semantic changes

Engineering (no valid-output change): local file I/O instead of
`google.colab.files`; `input()` → argparse/getpass; prints removed from core;
empty-input guard; `CipherFormatError` structural validation; metrics moved
out of the crypto path. Semantic changes: **none** in archival mode.
Hardening ideas (PBKDF2/Argon2, salt, AEAD, full-payload encryption) are
future work only — see `docs/limitations.md`.
