# Limitations (Read Before Any Claim)

Updated 2026-10-08. See `docs/evidence_audit.md` for supporting artifacts and
`docs/author_questions.md` for pending decisions.

1. **Not production cryptography.** Single-pass SHA-256 password hashing, no
   salt, AES-CBC with a stored random IV and PKCS#7 but no authentication tag.
   Tampering and wrong passwords are not reliably detected; invalid padding
   is common, not guaranteed. Structural validation is not authentication.
2. **The main permutation is not password-keyed.** For each selected `n`,
   the implementation constructs one fixed permutation (up to two row swaps).
   `n` is stored in the header and the inverse is publicly reconstructible.
   Password-derived AES protects only the residual tail, not the main part.
   The manuscript's `n!` combinatorial bound is not implemented key diversity.
   Main-part reordering preserves its histogram and entropy. Do not present
   byte differences, histograms, correlations or round-trip success as
   security proofs or IND-CPA/IND-CCA evidence.
3. **"AI selector" is rule-based.** The supplied PM-BG code uses deterministic
   size/entropy thresholds; no trained model was found.
4. **Units and memory.** Notebook MB/s divides by `1024**2`, i.e. MiB/s.
   Memory figures are `tracemalloc` traced peaks, not RSS/total process RAM.
5. **Demo data and supplied research materials are distinct.** The pipeline's
   `results/raw/`, summaries and demo figures are new measurements on
   DEMO-001..011 synthetic inputs. They are not the original-run evidence for
   Tables 3/7. Supplied F1..F9 triplets and reports are now available locally
   under `results/analysis result/`; artifact consistency is verified while
   historical-run attribution and distribution decisions remain unconfirmed.
   The draft recommends excluding this folder from the initial public release,
   not assuming rights are granted or denied. See `docs/team_review_draft.md`.
   Do not mix supplied reported values into new raw CSVs.
6. **Consistency is not complete reproduction.** Table 3 matches saved notebook
   stdout, Table 7 matches supplied TXT/MD, and 9/9 original–decrypted pairs
   match. This does not establish original execution version, environment,
   repetitions or authenticity of timing measurements. Inputs for the stored
   FileAttachment and COMNET runs remain unavailable.
7. **UCEF reports exist; the tool is missing.** Code-analysis v1.0 and
   data-analysis v3.0 DOCX reports are available, but source/binary,
   configuration, input hashes, sampling rules and standalone exports have
   not been located. Full-file F9 entropy/chi-square/adjacent Pearson differ
   from report values. The cause is unconfirmed. Do not imitate the scorer
   or claim the score/statistics have been independently reproduced.
8. **Shift128 exists in another implementation family.** The additional
   graph/unimodular/full-AES notebook implements `+128/-128 mod 256`; the
   canonical PM-BG AES tail is not Shift128. For F9, plaintext residual length
   is zero (`5423488 % 32 == 0`). The paper/report's evaluated residual and
   relation to Figure 7 need confirmation.
9. **Difference rates are alignment-dependent.** Reported F9 byte and bit
   difference rates match original vs ciphertext prefix including the header,
   not a controlled plaintext/key-perturbation avalanche experiment. The UCEF
   report records differential testing/KPA as not executed and CPA as not
   demonstrated; these must not be described as passed tests.
10. **Formula extraction is not numerical provenance.** OMML mathematical text
    can be extracted; earlier text blanks do not prove formulas absent.
    Tables 8–9 derivation code and rate assumptions remain unconfirmed.
11. **Validation is limited.** Tests cover exercised reference/package cases,
    including deterministic malformed-input/wrong-password cases, not every
    possible password/tamper outcome or manuscript statistic. Small demo
    files have timing noise; repetitions do not erase it.
12. **MIT is not blanket artifact or publication approval.** On 2026-10-08
    the repository maintainer/user confirmed "Lisensi kami gunakan MIT" for
    repository-owned code, documentation, and synthetic demo data; approval
    from all authors has not been verified. MIT does not automatically grant
    rights to third-party F1..F9, the manuscript, or UCEF/supplied reports.
    Contributor attribution, per-artifact rights, experimental provenance,
    and publication approval remain pending. The release builder traverses
    all `results/` without per-file rights gating; its forbidden-path assertion
    is not a distribution policy. Review an explicit inclusion policy, private
    content and experimental passwords before any archive.
