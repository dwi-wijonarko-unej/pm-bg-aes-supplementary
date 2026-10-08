# Source Inventory — PM-BG-AES Supplementary Artifacts

> Evidence categories used in this repository:
> **A.** Supplied implementation · **B.** Supplied saved output/report ·
> **C.** New local execution of faithful implementation ·
> **D.** Newly generated demonstration dataset · **E.** Derived analysis added
> for transparency · **F.** Manuscript-reported value, not independently reproduced.
> Category **F** values never enter category **C** raw measurements.
> A/B describe supplied artifacts, not independently authenticated original-run
> provenance. The 2026-10-08 update is documented in `docs/evidence_audit.md`.

## 1. Initial workspace inventory (2026-10-07; updated 2026-10-08)

| File in workspace root                  | SHA-256                                                            | Size       | Role                                                                               |
| --------------------------------------- | ------------------------------------------------------------------ | ---------- | ---------------------------------------------------------------------------------- |
| `Draft Paper PM_BG_AES 12Sept2026.docx` | `6db94b5cbe1e037f1835c07f9345c911ddbde09f629e3fad3cc05210c5f3af5b` | 1004.0 KiB | Manuscript draft (read-only source, never modified, excluded from release archive) |
| `PM_BG_+_AES_(works)_ori.ipynb`         | `7c226d4fe3c9fa124c6dcc78564cb13138584ead112b1bc7e055cfeb580fb8b5` | 34.6 KiB   | Source notebook, 2 code cells (category A)                                         |
| `PM_BG_+_AES_(works)_workshop.ipynb`    | `6bf294a5388bb7f1a24f17640a788836d887572ec6a0c02d3b647e83289740ca` | 57.9 KiB   | Source notebook, 3 code cells (category A)                                         |
| `*.Zone.Identifier` (×2)                | —                                                                  | 25 B       | Windows attachment metadata, not a source                                          |

The initial inspection found no F1..F9 inputs. The 2026-10-08 audit now finds
nine original/encrypted/decrypted triplets, two additional notebooks, a TXT/MD
benchmark report and two UCEF DOCX reports under `results/analysis result/`.
Their arrival date and original-run provenance are not established. Full
F1..F9 sizes/checksums and pending rights are in `docs/dataset_evidence.csv`;
notebook/report identities and findings are in `docs/evidence_audit.md`.
`FileAttachment.pdf_encrypted` and the `COMNET-S-26-08200.pdf` input remain
unavailable. UCEF reports are available, but the evaluation tool is not.

## 2. Notebook cell map

Read as JSON (nbformat 4). Neither notebook was executed wholesale before
inspection (cells contain `!pip install`, `input()`, `google.colab.files`
upload/download).

### `PM_BG_+_AES_(works)_ori.ipynb` — 2 cells

| cell_index | cell_id        | type | src chars | saved outputs          | functions defined                                                                                                                                                                                                                                |
| ---------- | -------------- | ---- | --------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0          | `pzmk8lalNUbQ` | code | 6203      | none                   | `hitung_entropy`, `pilih_matriks_ai`, `kunci_permutasi`, `aes_encrypt`, `aes_decrypt`, `md5`, `enkripsi`, `dekripsi` (+ Colab main-menu block with `input()`/`files.upload()`/`files.download()`)                                                |
| 1          | `7495Mw2mNX3t` | code | 8227      | 5 (category B, see §4) | `hitung_entropy`, `cetak_laporan_performa`, `pilih_matriks_ai`, `kunci_permutasi`, `aes_encrypt`, `aes_decrypt`, `enkripsi` (with tracemalloc/psutil/`time.time()` metrics), `dekripsi` (idem) (+ Colab main-menu block). No `md5` in this cell. |

### `PM_BG_+_AES_(works)_workshop.ipynb` — 3 cells

| cell_index | cell_id        | type | src chars                                 | saved outputs          | functions defined                                                                                                                                                                                                                                    |
| ---------- | -------------- | ---- | ----------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0          | `pzmk8lalNUbQ` | code | 6203                                      | none                   | byte-identical to ori cell 0                                                                                                                                                                                                                         |
| 1          | `7495Mw2mNX3t` | code | 8227                                      | none (outputs cleared) | byte-identical to ori cell 1                                                                                                                                                                                                                         |
| 2          | `QCUa6hQsvSCO` | code | 13614 (13648 on disk w/ trailing newline) | 5 (category B, see §4) | `print_array_preview`, `hitung_entropy`, `cetak_laporan_performa`, `pilih_matriks_ai`, `kunci_permutasi`, `aes_encrypt`, `aes_decrypt`, `enkripsi` (step-by-step visualisation), `dekripsi` (idem) (+ Colab main-menu block). No `md5` in this cell. |

Byte-identity verified: ori cell 0 == workshop cell 0; ori cell 1 ==
workshop cell 1 (compared after JSON `source` join).

## 3. Canonical implementation selection

**Canonical: ori cell index 1 (`7495Mw2mNX3t`)** — the metrics-instrumented
`enkripsi`/`dekripsi` pair (identical copy in workshop cell 1).

Reasons:

1. It is the only variant whose measurement boundaries (`time.time()`,
   `tracemalloc`, `psutil.Process().cpu_percent()`, `cetak_laporan_performa`
   with `orig_size/(1024*1024)/elapsed`) match the manuscript's reported
   performance tables (Tables 3 and 7, category F).
2. Core cryptographic semantics are identical across all three variants
   (same entropy formula, selector thresholds, permutation swaps, split rule,
   reshape/`dot`/`mod 256` pipeline, `"0."+password+"1"`/SHA-256/AES-CBC
   tail, 4-byte + 8-byte big-endian header). The only semantic-adjacent
   difference is `kunci_permutasi(..., 'e')` returning `(P, 0)` in cells 0–1
   vs `(P_permuted, P_identity)` in workshop cell 2 — the second element is
   discarded by every caller (`kunciku, _ = ...`), so behaviour is identical.
3. Workshop cell 2 is retained as the documented visualisation/demo variant,
   not the canonical one, because its console previews would pollute
   benchmark timings if included in the measured path.

This is a **canonical archival implementation selected from the supplied
notebook**, not a "verified manuscript implementation". F1..F9 artifacts and
matching Table 7 logs are now available, but do not prove which cell/version
produced the recorded timings. Author confirmation is still required (see
`docs/author_questions.md` Q1 and Q11). The additional Shift128 notebook is a
different implementation family, not covered by this canonical selection.

## 4. Supplied saved outputs (category B; provenance pending)

- **ori cell 1**: a decryption run. Input `FileAttachment.pdf_encrypted` (104300 bytes,
  entropy 7.3843) → output 104267 bytes (entropy 7.3840), elapsed 0.0070 s,
  throughput 14.27 MB/s (MiB/s units, see `docs/limitations.md`), peak
  1125.57 KB, CPU 99.9 %. Input file **not in workspace**. These numbers
  match Table 3 exactly; stored-output correspondence is not a benchmark rerun.
- **workshop cell 2**: an encryption run. Input `COMNET-S-26-08200.pdf`
  (2006753 bytes, entropy 7.9861) → n=24, len_shift=17, len_hill=2006736,
  Matrix preview shows the top-left 6×6 block is still the
  identity (expected: swaps occur at rows 12–15 for n=24, outside the shown
  window). Input file **not in workspace**.

## 5. Manuscript draft (read-only reference)

`Draft Paper PM_BG_AES 12Sept2026.docx` — 180 paragraphs, 9 tables, ~47 k
characters of text. Title: _Graph-Based Permutation Matrix Generation and
Intelligent Dynamic Block Optimization for Hybrid Hill Cipher–AES Enterprise
Data Protection_. Authors (9): Samsul Arifin, Ade Kurniawan,
Muhamad Totoh Muharam, Ansori, Tiawan, Merios Gusan Putra,
Edwin Kristianto Sijabat, Dani Lukman Hakim, Dwi Wijonarko (affiliations and
corresponding-author e-mail as in the draft; no ORCID/e-mail per author given).
Many equations are OMML objects and initially extracted as blanks with
plain-text `python-docx` extraction. The audit recovered mathematical text
from DOCX XML; extraction blanks must not be described as absent formulas.
Original derivation scripts and assumptions still require confirmation.

Manuscript tables mapped to code (detail in
`docs/manuscript_artifact_mapping.csv`):
Table 1 taxonomy, Table 2 SOTA, Table 3 Colab decrypt benchmark (matches ori
cell-1 saved output: 0.0070 s / 14.27 / 1125.57 KB / 99.9 % / 104300→104267),
Table 4 methodology, Table 5 SOTA synthesis, Table 6 UCEF static assessment
(score 60.00/100 — report available, tool missing), Table 7 F1..F9 metrics
(matching supplied TXT/MD, original-run provenance pending), Table 8 key-space,
Table 9 dictionary attacks; Figures 1–7 and
supplementary S1–S8 (partially derivable as new demo figures, never labelled
as manuscript figures).

## 6. Dependencies found in sources

`numpy`, `pycryptodome` (`Crypto.Cipher.AES`, `Crypto.Util.Padding`),
`psutil`, `tracemalloc` (stdlib), `hashlib` (stdlib), `google.colab.files`
(Colab-only; adapted to local file I/O), `!pip install` lines (not executed).

## 7. Additional evidence and unresolved requirements (2026-10-08)

- All nine original–decrypted pairs have identical full SHA-256. File sizes,
  headers and main permutation segments are consistent with supplied logs
  and the PM-BG code. This does not authenticate original-run timings or rights.
- `results/analysis result/PM-BG + AES (works)_ori.ipynb` has source/output
  identical to root `ori`, with different execution metadata.
- `results/analysis result/PM-BG + AES (works).ipynb` implements Shift128
  (`+128/-128 mod 256`) in a different graph/unimodular/full-AES pipeline.
  Its relationship to Figure 7 and the evaluated residual remains unclear.
- Table 7 matches the TXT/MD report. Repetitions, original environment,
  experimenter's version mapping and input provenance remain unconfirmed.
- UCEF code-analysis v1.0 and data-analysis v3.0 reports are available.
  Tool source/binary, configuration, run input hashes and standalone exports
  have not been located. Several whole-file F9 statistics differ from the
  report; sampling/segment/preprocessing definitions are required.
- `FileAttachment.pdf_encrypted` and `COMNET-S-26-08200.pdf` remain missing.
- Tables 8–9 calculation code, numerical derivations and rate assumptions
  remain unconfirmed; OMML extraction alone cannot resolve these questions.
- MIT license choice was confirmed by the repository maintainer/user on
  2026-10-08: "Lisensi kami gunakan MIT". It covers repository-owned code,
  documentation, and synthetic demo data, not verified approval from all
  authors or automatic rights to third-party F1..F9, the manuscript, or UCEF/
  supplied reports. Earlier pending-license findings are historical and
  superseded. Per-artifact ownership/redistribution, provenance, software
  contributors, and release approval remain pending. See
  `docs/evidence_audit.md` and author questions Q6/Q9.

The initial docs-only revision did not update README or the local candidate.
A subsequent wording cleanup updated README and its package-description copy;
the ZIP received three wording-only document patches and revised checksums.
The parent-managed archive was also selectively updated for MIT wording,
not fully rebuilt with current evidence or all current docs. Archive/metadata
changes are outside this docs-only update. This inventory describes the
workspace, not the candidate's contents. See `docs/evidence_audit.md`.
