# Workspace Evidence Audit — 2026-10-08

## Conclusion and scope

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on 2026-10-08. The conservative v1.0.0 scope is adopted: repository-owned code/docs/synthetic demo under MIT, with exclusion of all F1..F9 payloads and the entire `results/analysis result/` tree. Historical artifact-consistency findings are documented, but original-run attribution, timing reproduction, UCEF reproducibility, and original figure generation remain unconfirmed scientific limitations.

For team discussion, the proposed provenance conclusion is **artifact consistency verified; historical-run attribution unconfirmed**. The proposed initial public release excludes supplied F1–F9 triplets and the entire `results/analysis result/` folder, pending per-artifact permission/privacy review. This is a recommendation, not a rights-holder decision or an enforced builder policy. See `docs/team_review_draft.md` and `docs/dataset_distribution_review.csv`. Neither experiments nor archives were rerun/rebuilt for this draft.

This audit inspected notebook JSON/source/saved outputs, the benchmark TXT/MD, DOCX text and OMML, file sizes/hashes, ciphertext structure, and repository code. Notebooks were not executed wholesale; EXE/MSI files were not executed. Dataset contents and password values are not reproduced in this document. Paths below are relative to the repository root.

The initial 2026-10-07 inventory described a smaller workspace. F1–F9 and additional reports/notebooks are present in the 2026-10-08 audit; their date of arrival and experimental provenance are not established by that observation.

## 1. Evidence and remaining confirmation

| Item              | Available evidence                                                                                          | Remaining requirement                                                   |
| ----------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Implementation    | Root `ori`/`workshop`, preserved copies, Python port; additional notebooks under `results/analysis result/` | Experimenter's notebook/cell/version mapping to each result             |
| Table 3           | Exact numeric match with `ori` cell 1 saved stdout                                                          | Input file, run provenance and environment                              |
| Table 7           | All nine rows match supplied TXT/MD; F1–F9 triplets available                                               | Original-run provenance, repetitions, environment and rights            |
| Dataset integrity | 9/9 original–decrypted pairs equal; full SHA-256 recorded                                                   | Confirmation these are manuscript inputs and redistribution decisions   |
| UCEF              | Code-analysis v1.0 and data-analysis v3.0 DOCX reports                                                      | Tool, configuration, input hashes, exports and permission               |
| Shift128          | `+128/-128 mod 256` in a different notebook pipeline                                                        | Relationship to Figure 7 and exact evaluated residual                   |
| Statistics        | Reported values and independent full-file comparisons                                                       | Explanation of sampling/preprocessing/segment differences               |
| Figures           | Demo PNG/SVG and figures embedded in supplied reports                                                       | Original standalone figure/data exports and mapping                     |
| License choice    | MIT confirmed by repository maintainer/user on 2026-10-08                                                   | All-author approval not verified; per-artifact rights review remains    |
| Publication       | Draft metadata; no external publication checked                                                             | Provenance, contributors, inclusion scope and explicit release approval |

## 2. Notebook identity and implementation families

Root notebooks and their copies in `notebooks/original/` are byte-identical:

- `PM_BG_+_AES_(works)_ori.ipynb`:
  `7c226d4fe3c9fa124c6dcc78564cb13138584ead112b1bc7e055cfeb580fb8b5`.
- `PM_BG_+_AES_(works)_workshop.ipynb`:
  `6bf294a5388bb7f1a24f17640a788836d887572ec6a0c02d3b647e83289740ca`.

Source of cells 0 and 1 agrees between these two notebooks. Cell 1 of `ori` (index 1, ID `7495Mw2mNX3t`) remains the selected archival reference, not an author-confirmed implementation for every manuscript experiment.

Additional notebooks:

| Path under `results/analysis result/` | SHA-256                                                            | Finding                                                               |
| ------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------- |
| `PM-BG + AES (works)_ori.ipynb`       | `237b00153efdb9f026581238936f502bf948e9b18614166887210a6750bde61f` | Source and saved outputs match root `ori`; execution metadata differs |
| `PM-BG + AES (works).ipynb`           | `02c99ab93e873c7eb3431f05f8bb501d8740c1ab60f2931aba288ac996aefa85` | Different complete-graph/unimodular/Shift128/AES pipeline             |

The additional `ori` has execution count 2 and execution metadata on cell 1; root `ori` has null execution counts despite saved outputs. This does not establish chronology or authorship.

The canonical PM-BG family uses fixed row permutations and AES-256-CBC only on the residual tail. The other notebook uses `N = 2 * user_n`, complete-graph and unimodular matrices, Shift128 on residual bytes, then AES-128-CBC on the whole combined payload with deterministic parameter-derived key/IV.

Its saved decryption (104272 → 104267 bytes, 0.1824 s, throughput 0.55) is not the Table 3 run. No replacement scorer or missing-method imitation was built.

## 3. Tables 3 and 7

### Table 3

`ori` cell 1 saved stdout matches the manuscript: 0.0070 s, throughput 14.27,
traced peak 1125.57 KB, CPU 99.9%, 104300 → 104267 bytes, entropy
7.3843 → 7.3840. The logged input is `FileAttachment.pdf_encrypted`;
the corresponding input/recovered files were not found.

The `workshop` saved encryption uses `COMNET-S-26-08200.pdf`, 2006753 bytes,
`n=24`, 17 residual bytes, 0.1287 s and throughput 14.88. Its input was also
not found. Matching stored numbers is not a rerun of either experiment.

### Table 7

The following supplied reports are byte-identical (21403 bytes):

- `results/analysis result/2. File TXT - Paper PM-BG + AES_ori.txt`
- `results/analysis result/File TXT - Paper PM-BG + AES_ori.md`

SHA-256: `9a2819b951992a79f2a06fa23c48b8baeacd0ba310a415ffd609027bd046d08a`.

| ID  | Input bytes |   n | Encrypt seconds / MiB/s | Decrypt seconds / MiB/s | Encryption overhead bytes |
| --- | ----------: | --: | ----------------------: | ----------------------: | ------------------------: |
| F1  |    19123560 |  32 |           2.0109 / 9.07 |           2.0659 / 8.83 |                        36 |
| F2  |     3779324 |  24 |           0.4562 / 7.90 |          0.1575 / 22.89 |                        40 |
| F3  |     7019857 |  48 |           1.4909 / 4.49 |           1.9376 / 3.46 |                        43 |
| F4  |    12374057 |  48 |           2.0280 / 5.82 |          1.0322 / 11.43 |                        35 |
| F5  |     3972474 |  24 |           0.4868 / 7.78 |          0.2755 / 13.75 |                        42 |
| F6  |     3652608 |  24 |          0.1657 / 21.02 |          0.1492 / 23.35 |                        44 |
| F7  |     3750701 |  24 |          0.1789 / 20.00 |          0.2515 / 14.22 |                        39 |
| F8  |        6061 |   6 |           0.0055 / 1.06 |           0.0045 / 1.30 |                        43 |
| F9  |     5423488 |  32 |           0.7872 / 6.57 |           0.6544 / 7.90 |                        44 |

Sizes, selected matrix sizes, times, throughput, tabulated memory and overhead
match Table 7. Supplied ciphertext sizes/headers and main permutation
segments are consistent with the PM-BG implementation; entropy agrees with
the TXT after four-decimal rounding. All nine original–decrypted pairs are equal.
This does not independently authenticate the recorded timings or demonstrate
that those recovered files were produced from these ciphertexts in the
claimed original runs.

The report records one encryption/decryption result per file. The number of
original experiment repetitions is unknown. Five repetitions in the demo
pipeline are separate and cannot establish the original protocol.

Units: the notebook divides by `1024**2`, so its label MB/s means MiB/s.
Memory is `tracemalloc` traced allocation peak, not process RSS/total RAM.
The draft prose gives F8 decryption as 0.00045 s while Table 7/log give
0.0045 s; these are flagged for authors, not silently corrected in the paper.

## 4. Dataset identity

`docs/dataset_evidence.csv` records original/recovered paths, byte sizes,
full SHA-256 and pending provenance/redistribution decisions for F1–F9.
The nine triplets live under `results/analysis result/File 1-MP4` through
`File 9-EXE`. At audit time all 27 main files were untracked; the DOCX reports
were ignored by the Git `*.docx` rule. Local availability does not mean GitHub
availability or inclusion in an approved archive.

No source ownership or redistribution authorization is inferred from names,
file metadata, hash matches or the presence of encrypted copies.

## 5. UCEF and statistical discrepancies

Reports available under `results/analysis result/`:

- `1. [01.09.2026] Analisis Algoritma.docx`: UCEF-Code Security Analyzer
  v1.0, score 60.00/100, 1 PASS / 4 REVIEW / 1 WARNING. SHA-256:
  `9ac60a6d015e88f7194c3a0d475bd458afd314fe2eff3b5034408cc6622d63a4`.
- `3. [01.09.2026] Analisis Keamanan Data.docx`: UCEF v3.0, F9 statistics.
  SHA-256: `cffd5b0f7689c3734edcaed60f6fd958fef6ca75839f3f4984ecaa00bff9e029`.

The code report names the additional `ori` notebook and its 26920-byte size,
but does not supply a verified input hash. It reports zero detected Python
functions despite 16 function definitions across that notebook's two cells;
this is a detection limitation requiring interpretation, not evidence that
the notebook has no functions. The data report lists some generated files
with F4 PNG names despite naming F9 EXE as input. Neither report establishes
that all referenced CSV/XLSX/standalone figure exports are available.

UCEF source/binary, reproducible configuration, sampling/preprocessing rules
and original standalone exports have not been located.

### Independent current-file calculations

Whole-file bytes, 256-bin histogram; entropy base 2; chi-square
`sum((count - N/256)**2 / (N/256))`; Pearson between adjacent byte arrays
`x[:-1]` and `x[1:]`. Uses `src/pm_bg_aes/entropy.py` and `analysis.py`.
These are audit calculations, not recovered UCEF code.

| Metric                     |            UCEF report | Current complete file |
| -------------------------- | ---------------------: | --------------------: |
| Original entropy           |               6.910652 |           6.910779564 |
| Encrypted entropy          |               6.910008 |           6.910783258 |
| Original chi-square        | approximately 12436320 |       33766417.513488 |
| Encrypted chi-square       |        12468952.264704 |       33766723.685766 |
| Original adjacent Pearson  |               0.000921 |           0.289727740 |
| Encrypted adjacent Pearson | approximately 0.000917 |           0.289727746 |

Possible causes include input, sampling, alignment or preprocessing
differences; no cause is confirmed. Ask for run input hashes and evaluation
code before calling the report erroneous or the results reproduced.

Comparing original F9 with the first 5423488 bytes of its ciphertext,
**including the 12-byte header**, gives byte difference 89.417345443% and
bit difference 42.830370418%, matching the report. These are aligned-file
difference rates, not a controlled plaintext/key-perturbation avalanche test.

F9 has `n=32`, `len_hill=5423488` and zero plaintext residual bytes. Its AES
segment still contains an IV and a padding block. The report's Shift-128
residual entropy (6.208572, stated maximum 7) therefore cannot be identified
as the canonical pipeline's plaintext tail without another definition.

The data report records performance as NaN, differential testing/KPA as not
executed and CPA as not demonstrated. Do not describe these as passed tests.

OMML equation text can be extracted from the draft XML; earlier plain-text
extraction blanks are not proof that formulas are absent. The original
calculation code, parameter assumptions and numerical derivations for
Tables 8–9 remain unconfirmed.

## 6. Release and documentation boundaries

**Current license decision (2026-10-08):** the repository maintainer/user
explicitly confirmed "Lisensi kami gunakan MIT". MIT applies to
repository-owned code, documentation, and synthetic demonstration data.
This is the maintainer/user's confirmation, not verified approval from all
manuscript authors or every rights holder. Q6's license choice is closed.
MIT does not automatically grant rights to third-party F1–F9 (including
ciphertext/recovered copies), the manuscript, or UCEF/supplied reports.

**Historical finding, superseded for current repository licensing:** the
initial audit observed a pending-author-approval license placeholder granting
no public redistribution rights. That observation describes the earlier
state, not the current MIT decision. Per-artifact permissions, experimental
provenance, software contributors, repository/deposit identifiers, and written
release approval remain pending. MIT does not establish provenance or approve
publication. External publication services were not checked; local draft
metadata is not proof of publication or nonpublication.

The existing candidate manifest does not list `results/analysis result/`.
It is not a complete snapshot of the audited workspace, and was not rebuilt.
`scripts/build_release.py` collects the entire `results/` tree without a
per-artifact rights filter. Its assertion currently rejects collected
DOCX and `Zone.Identifier` paths. Removing those paths alone could still
package unapproved F1–F9. A reviewed inclusion policy and privacy/password
review are required before rebuilding or distributing any candidate,
including these documents and reported measurements.

The initial documentation update was limited to `docs/`. A subsequent wording
cleanup updated README and its package-description copy using this evidence.
The earlier local ZIP cleanup made wording-only substitutions in three
documents and revised checksums. The parent-managed archive was also
selectively updated for MIT wording; this docs-only change does not modify
archives, root files, data, scripts, or metadata. These selective updates
are not a full archive rebuild or synchronization with current documentation.
It remains an older candidate without newly supplied F1..F9 data or reports.
No release builder or publication was run for this docs-only update. MIT
and these wording edits do not constitute permission to publish the supplied
evidence.

## 7. Validation and claim boundaries

On 2026-10-08 the command below passed 64 tests with one RuntimeWarning from
empty-input entropy in the notebook reference:

```sh
PYTHONPATH=src python -m pytest -q -p no:cacheprovider
```

This validates exercised package/reference behavior, not all manuscript
numbers, cryptographic security, UCEF results, original-run provenance or
publication rights. No original benchmark rerun or archive rebuild was
performed for this audit.

## Ringkasan untuk tim

Bahan pendukung eksperimen tersedia sebagian dan telah diperiksa
konsistensinya. Angka Table 3 cocok dengan output notebook tersimpan dan
seluruh baris Table 7 cocok dengan laporan teks. F1–F9 tersedia lokal dan
sembilan pasangan original–decrypted identik. Namun, provenance eksperimen,
jumlah pengulangan, metode statistik UCEF, hubungan varian Shift128, serta
izin publikasi masih menunggu konfirmasi penanggung jawab. Hasil demo baru
tetap dipisahkan dari bahan penelitian; seluruh hasil paper belum dinyatakan
tereproduksi. Pengelola repositori/user mengonfirmasi "Lisensi kami gunakan
MIT" pada 8 Oktober 2026 untuk kode, dokumentasi, dan demo sintetis milik
repositori; persetujuan seluruh penulis belum diverifikasi. Temuan lisensi
pending sebelumnya bersifat historis dan telah digantikan oleh pilihan MIT.
MIT tidak otomatis mencakup F1–F9, manuskrip, atau laporan UCEF, serta tidak
mengonfirmasi provenance maupun persetujuan publikasi.
