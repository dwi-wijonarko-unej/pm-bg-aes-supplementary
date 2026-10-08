# Author Questions — Evidence and pending decisions

Status: **Assistant-authored evidence-based answers and release proposal for
team review, 2026-10-08; not team approval**. The user requested this draft
on 2026-10-08: "Aku percayakan padamu, untuk menjawab dan mengubah bagian
provenance eksperimen, dan izin distribusi dataset, hasil dari anda akan aku
diskusikan dengan tim nanti". Delegation to draft answers is not permission
to distribute supplied artifacts or confirmation of historical experiments.
MIT license choice for repository-owned code/docs/demo is confirmed by the
repository maintainer/user (Q6). Evidence is from the
[2026-10-08 audit](evidence_audit.md) and [dataset evidence](dataset_evidence.csv).
Provenance, per-artifact permissions, and team release approval remain pending.

The substantive Indonesian discussion draft is
[team review draft](team_review_draft.md). The
[distribution review register](dataset_distribution_review.csv) records the
proposed exclusion and pending team decision for every F1–F9, alongside
`docs/dataset_evidence.csv`. These are prepared review materials, not confirmed
rights-holder permissions or completed team decisions.

## Q1. Canonical implementation and original measurements

**Draft answer — verified local consistency, not authenticated run history.**
`PM_BG_+_AES_(works)_ori.ipynb` cell 1 remains the selected archival
implementation, pending confirmation that it produced Tables 3/7. The
additional `PM-BG + AES (works)_ori.ipynb` has identical source/output to the
root ori notebook but different metadata; this is not an independent run.

- Table 3 matches saved stdout from ori cell 1 exactly: 0.0070 s,
  14.27 MiB/s, 1125.57 KB, 99.9%, and 104300 → 104267 bytes. Its input
  `FileAttachment.pdf_encrypted` is missing; `COMNET-S-26-08200.pdf` is also
  missing. Matching saved output is not a fresh reproduction.
- All nine Table 7 rows match
  `results/analysis result/2. File TXT - Paper PM-BG + AES_ori.txt` (identical
  content in `File TXT - Paper PM-BG + AES_ori.md` in that directory).
  Input sizes, selected matrix sizes, times, throughput, memory and overhead
  match; supplied ciphertext sizes, headers and main permutation segments
  are consistent with the selected PM-BG implementation. All nine supplied
  original/decrypted pairs have matching SHA-256. This does not authenticate
  saved timings or establish that these ciphertexts produced those recovered
  files in the claimed historical runs.
- Original repetition counts and execution environment remain unknown.
  DEMO-001..DEMO-011 use five repetitions and are new demonstrations, not
  evidence of the original experimental protocol.

**Remaining factual confirmation:** ask the experimenter to identify the
producing notebook/cell/version or commit, operator/author and original run
date, input hashes and manuscript mapping, timing boundaries, repetition
counts, and hardware/software environment. The throughput computation uses
`1024**2` (MiB/s despite the notebook's MB/s label); memory is the
`tracemalloc` traced allocation peak, not RSS. Timing protocol and historical
execution details still require confirmation.

**Proposed handling:** retain Tables 3/7 as saved historical measurements with
an explicit artifact-consistency qualification, not as independently reproduced
results. Record unavailable historical details as limitations if the team
cannot recover them. Offer a fresh, separately dated experiment if the team
wants additional validation; do not require or relabel it as the original run.
Keep UCEF results report-only with the statistical discrepancies in Q11 and
unexecuted/undemonstrated tests in Q12 visible. Keep the separate Shift128
pipeline distinct (Q3), not evidence of this implementation's Figure 7.

## Q2. Original datasets F1..F9: local evidence, rights pending

**Draft answer — local integrity verified; distribution decisions pending.**
Original/encrypted/decrypted files are available locally under
`results/analysis result/File 1-MP4` through `File 9-EXE`. All nine original
versus decrypted SHA-256 comparisons match (sizes and paths in
`docs/dataset_evidence.csv`). All 27 files were untracked at
the audit date; local presence and original–decrypted file equality do not establish
provenance, manuscript identity, or redistribution rights.

**Remaining factual confirmation:** for each original, encrypted and decrypted
artifact, identify its source/creator, acquisition context, experiment mapping,
rights holder, license or written permission, privacy concerns, and allowed
release channel. The sizes and hashes are recorded evidence to confirm
against the historical inputs, not proof of ownership. The Table 3 input and
COMNET file noted in Q1 remain missing. Do not execute supplied MSI/EXE files
for this review; file type alone is not evidence that they are malicious.

**Concrete proposed handling (all decisions pending):**

| Dataset | Type | Original bytes | Rights/provenance decision | Proposed initial handling                     |
| ------- | ---- | -------------: | -------------------------- | --------------------------------------------- |
| F1      | MP4  |       19123560 | Pending                    | Exclude original/encrypted/decrypted payloads |
| F2      | MP3  |        3779324 | Pending                    | Exclude original/encrypted/decrypted payloads |
| F3      | JPG  |        7019857 | Pending                    | Exclude original/encrypted/decrypted payloads |
| F4      | PNG  |       12374057 | Pending                    | Exclude original/encrypted/decrypted payloads |
| F5      | PDF  |        3972474 | Pending                    | Exclude original/encrypted/decrypted payloads |
| F6      | MSI  |        3652608 | Pending                    | Exclude original/encrypted/decrypted payloads |
| F7      | ZIP  |        3750701 | Pending                    | Exclude original/encrypted/decrypted payloads |
| F8      | TXT  |           6061 | Pending                    | Exclude original/encrypted/decrypted payloads |
| F9      | EXE  |        5423488 | Pending                    | Exclude original/encrypted/decrypted payloads |

Prefer a release of repository-owned code/docs, DEMO-001..DEMO-011 and clearly
labelled new demo results under MIT after privacy and release review. Include
only reviewed F1–F9 metadata/hash summaries, based on `docs/dataset_evidence.csv`,
after checking filenames, paths, hashes and other metadata for disclosure risks.
Do not automatically publish the current CSV unchanged.

Propose exclusion of the **entire `results/analysis result/` folder**, including
all original/encrypted/decrypted payloads, supplied TXT/MD reports, copied logs,
DOCX manuscripts/UCEF reports and raw additional notebooks, pending per-artifact
permission and privacy review. Encryption is not a redistribution exemption.
This is a conservative release recommendation, not proof that rights are denied
or granted, and not an implemented packaging filter.

The team may approve individual files for public distribution, choose restricted
or request-only access if a rights-compliant contact/procedure is established,
or exclude them. Record the responsible decision-maker, evidence, date, exact
file/hash, permitted channel and conditions in the proposed
`docs/dataset_distribution_review.csv`; every F1–F9 decision starts pending.
Do not promise "available upon request" without an approved contact and procedure.

## Q3. Shift-128 definition and Figure 7 mapping

The additional `PM-BG + AES (works).ipynb` implements Shift128 as ±128
modulo 256. However, it uses a different complete-graph/unimodular/AES-128
whole-payload pipeline, not the selected permutation/AES-256 residual-tail
pipeline. Its existence does not establish the canonical implementation's
Figure 7 behavior.

For F9, N = 5,423,488 and n = 32 give zero residual; its relationship to
Figure 7 remains unclear. Please identify the intended pipeline, input,
residual definition, and exact Figure 7 generation procedure.

## Q4. UCEF-Code Security Analyzer

Reports are locally available as `1. [01.09.2026] Analisis Algoritma.docx`
(UCEF v1.0, score 60) and
`3. [01.09.2026] Analisis Keamanan Data.docx` (v3.0). The analyzer tool,
configuration, CSV/XLSX exports, and figure-generation artifacts are missing.
These reports are evidence of reported analysis, not an independently
reproduced score.

Please supply the tool/version, configuration, inputs and hashes, exports,
and figure workflow, or confirm that these results must remain
report-only. We will not build a look-alike scorer.

## Q5. Equations, derivations, and Tables 8/9 assumptions

OMML equation text has now been extracted. Formula availability must not be
inferred from earlier blank plain-text extraction. Original derivations and
assumptions for Tables 8/9 remain pending, including key-space counting and
brute-force rate assumptions. Please confirm these derivations, units,
constraints, and source calculations; extracted equations alone do not
validate the numerical or security claims.

## Q6. License choice — closed: MIT confirmed; artifact rights review remains

On 2026-10-08 the repository maintainer/user explicitly confirmed:
**"Lisensi kami gunakan MIT"**. This closes the repository license-choice
question: MIT applies to repository-owned code, documentation, and synthetic
demonstration data. This records the maintainer/user's confirmation, not
verified approval from all manuscript authors or every rights holder.

The earlier pending-license/no-rights finding is historical and superseded
by this MIT confirmation. MIT does not automatically grant rights to
third-party F1..F9 files (including encrypted/decrypted copies), the manuscript,
or UCEF/supplied reports. Their ownership, permissions, and per-artifact
redistribution review remain pending. License choice does not confirm
experimental provenance, contributors, release scope, or publication approval
(see Q2, Q7, and Q9).

## Q7. Authorship vs. contributorship

Manuscript authors (9 names) are recorded from the draft; software
contributors may differ. Please confirm the contributor list, corresponding
contact, affiliations/ORCIDs (optional), and exact citation title for
`CITATION.cff`/`.zenodo.json` (both draft). Contributor confirmation and
approval remain pending.

## Q8. "AI selector" terminology

The selected code uses a deterministic rule table (file size × entropy
thresholds), not a trained ML model. May we describe it as "rule-based
adaptive selector (called 'AI selector' in the notebook)", or is there a
trained model behind the thresholds that should be archived?

## Q9. Release approval and artifact inclusion

The repository manager can organize evidence, but technical confirmation must
come from the developer/experimenter and permissions from the relevant rights
holders. Record each answer with responsible person, evidence path, date,
status (known / pending / unavailable), and publication permission. A missing
artifact may be closed as unavailable with a documented limitation, not as
reproduced. Do not relabel a new rerun as an original historical result.

Please explicitly approve the release scope, contributors,
per-file inclusion allowlist, repository/deposit destination, and version
before any public push/release/deposit. External publication has not been
checked; no verified public URL or DOI is available from this audit.
MIT license choice is confirmed in Q6, but does not close these release gates.

`scripts/build_release.py` currently collects all `results/` without rights
gating. Its assertion rejects DOCX and `Zone.Identifier` files, but deleting
those alone could still package restricted data. An explicit inclusion
allowlist/filter and privacy/password review of notebook outputs and logs
are required before rebuilding. Existing experimental password values must
not be copied into public documentation or artifacts.

The existing ZIP remains an older local candidate: its manifest has no
`results/analysis result/` folder. The earlier wording-only cleanup changed
three archived documents and their checksums without adding evidence files.
The parent-managed archive was also selectively updated for MIT wording;
this docs-only change does not edit the archive or its metadata. Selective
updates are not a full rebuild or synchronization with all current docs.
README and its package-description copy describe the audited local evidence.
Review an approved candidate before release; these edits imply neither
provenance nor publication approval.

## Q10. Password policy

The selected notebook prompts say "digits only" but do not validate digits
(any string works via `str(password2)`). Is that restriction intended, or
should the artifact document actual behavior (any string, UTF-8 encoded)?
Policy confirmation does not replace the output/log privacy review in Q9.

## Q11. Statistical input and sampling provenance

For encrypted F9, the report gives entropy 6.910008, chi-square
12468952.264704, and adjacent r ≈ 0.000917. The current full encrypted file
gives entropy 6.910783258, chi-square 33766723.685766, and adjacent r
0.289727746. These are not matching measurements.

Please provide the exact input hashes, sampled segment/length, header
handling, preprocessing, and statistical definitions needed to explain the
difference. Do not substitute the full-file results for the reported
experiment or claim the report has been reproduced.

## Q12. Divergence and attack claims

Divergence 89.417345% and bit difference 42.830370% match an original-versus-
ciphertext **prefix** comparison including the 12-byte ciphertext header.
This is not a controlled avalanche experiment. Differential and
known-plaintext attacks (KPA) were not executed; chosen-plaintext attack
(CPA) resistance was not demonstrated in the available UCEF report.

Please confirm the intended interpretation and provide controlled
experiments/protocols for any retained avalanche, differential, KPA, or CPA
claims. Otherwise distinguish report claims from demonstrated evidence.

## Ready-to-send team discussion draft (Indonesian)

Tim, berikut usulan jawaban berbasis audit lokal 8 Oktober 2026 untuk kita
diskusikan, bukan keputusan izin atau persetujuan publikasi. Tabel 3 cocok
dengan stdout tersimpan pada ori cell 1. Sembilan baris Tabel 7 cocok dengan
laporan TXT/MD; ukuran, header ciphertext dan segmen permutasi konsisten
dengan implementasi PM-BG yang dipilih. Hash original dan decrypted cocok
untuk seluruh F1–F9. Jadi kita dapat menyatakan konsistensi artefak lokal,
bukan bahwa eksperimen historis telah direproduksi atau diautentikasi.

Identitas pelaksana, tanggal eksperimen, versi notebook yang benar-benar
dijalankan, lingkungan/hardware dan jumlah pengulangan masih perlu konfirmasi
pengembang/pelaksana. Input Tabel 3 dan COMNET belum ditemukan. Jika catatan
historis tidak dapat dipulihkan, usulan saya adalah mencatat keterbatasannya.
Eksperimen baru dapat dipertimbangkan sebagai validasi tambahan berlabel baru,
bukan syarat wajib atau pengganti hasil historis. UCEF tetap report-only karena
tool/config/export belum ditemukan dan statistik F9 tidak sama dengan hitungan
full-file; penyebabnya belum terkonfirmasi. Shift128 berasal dari pipeline
terpisah dan belum membuktikan pemetaan Gambar 7. Metrik divergence yang cocok
adalah perbandingan prefix termasuk header, bukan uji avalanche terkontrol;
klaim serangan dan derivasi Tabel 8/9 juga masih perlu bukti.

Usulan rilis awal: kode/dokumentasi milik repositori, DEMO-001..DEMO-011 dan
hasil demo baru yang diberi label jelas, menggunakan MIT yang telah
dikonfirmasi pengelola/user pada 8 Oktober 2026, setelah review privasi dan
persetujuan rilis. Ringkasan metadata/hash F1–F9 dapat dipertimbangkan setelah
review pengungkapan informasi. Usulkan mengecualikan seluruh folder
`results/analysis result/`, termasuk payload original/encrypted/decrypted,
TXT/MD laporan, log salinan, DOCX/UCEF dan notebook tambahan mentah, sampai
izin dan privasi tiap artefak ditinjau. Ini bukan kesimpulan bahwa izin ditolak
atau diberikan; filter builder juga belum diterapkan.

Untuk setiap F1–F9, keputusan masih pending. Tim dapat menyetujui file tertentu,
menetapkan akses terbatas/berdasarkan permintaan bila kontak dan prosedur yang
sah sudah tersedia, atau mengecualikannya. Jangan menjanjikan "available upon
request" sebelum mekanismenya disepakati. Catat sumber, pemilik hak, bukti
izin, file/hash, penanggung jawab, tanggal dan kanal distribusi. Bahan diskusi
sudah disiapkan dalam `docs/team_review_draft.md` dan
`docs/dataset_distribution_review.csv`; keputusan distribusi sembilan dataset
masih menunggu tim. Mohon diskusikan opsi tersebut, kontributor dan daftar file
rilis; jangan masukkan password/kunci ke dokumen publik. Belum ada persetujuan
tim, push/deposit, pembaruan arsip, atau URL/DOI publik yang diverifikasi.
