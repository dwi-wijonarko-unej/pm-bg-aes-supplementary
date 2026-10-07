# Limitations (Read Before Any Claim)

1. **Not production cryptography.** Single-pass SHA-256 password hashing, no
   salt, random-but-unspecified IV storage, PKCS#7 without authentication
   tag. Tampering and wrong passwords are NOT reliably detected (invalid
   padding is common, not guaranteed). See `docs/file_format.md`.
2. **"AI selector" is rule-based.** Deterministic size×entropy thresholds;
   no trained model exists in the sources.
3. **Permutation diversity is tiny.** At most two fixed row swaps per `n`
   (≤4 distinct matrices); `n!` in the manuscript is a combinatorial bound,
   not implemented diversity. Low-entropy structured data keeps its
   histogram shape through the linear layer (permutation only reorders
   within each n-block column pattern) — entropy/correlation figures must
   not be presented as security proofs or IND-CPA/IND-CCA evidence.
4. **Units.** Notebook "MB/detik" divides by `1024*1024` → values are MiB/s.
   Memory figures are `tracemalloc` traced peaks, not RSS/total RAM.
5. **Demo data ≠ manuscript data.** All measurements are category C on
   category D synthetic inputs. Manuscript F-values are category F and never
   enter `results/raw`. File extensions of synthetic inputs are generic
   (`.bin`/`.txt`/`.zip`); no fake MP4/EXE/MSI "valid-format" claims.
6. **Missing pieces (no imitations built):** UCEF analyzer (no 60/100
   re-scoring), Shift-128 definition (AES tail is not Shift-128), exact
   formulae behind Tables 8–9/χ²/correlation values (OMML blanks in DOCX
   extraction), original F1..F9 files.
7. **Wrong-password tests** assert only deterministic cases (malformed
   header always raises; AES-tamper usually — not always — raises).
8. **Throughput scale.** Demo files are small by design; timing noise on ms
   runs is reported honestly via repetitions, not hidden.
