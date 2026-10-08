# Data Availability — Conditional Draft Statements

Status: **Assistant-authored team-review draft, 2026-10-08**, prepared at the
user's request to draft provenance and dataset-distribution answers for later
team discussion. These are proposals, not confirmed permissions, historical-run
approval, team approval, or assertions of publication/approved availability. The [2026-10-08 evidence audit](evidence_audit.md) establishes
local evidence only; external publication was not checked. On 2026-10-08
the repository maintainer/user confirmed "Lisensi kami gunakan MIT". MIT
applies to repository-owned code, documentation, and synthetic demonstration
data; this is not verified approval from all authors. Provenance, per-artifact
third-party redistribution rights, contributors, and release approval remain
pending. MIT does not automatically cover F1..F9, the manuscript, or UCEF/
supplied reports, and does not approve provenance or publication. Use a
public availability statement only after its conditions are satisfied and actual
publication identifiers are verified. No public repository URL, release version
or DOI is asserted here. The code-license choice is MIT.

## Current LOCAL evidence statement — usable for team review now

> The inspected workspace contains the selected archival implementation,
> synthetic demonstration inputs, and supplied experiment artifacts. Table 3
> matches the saved ori cell 1 stdout. All nine Table 7 rows match the supplied
> TXT/MD report; input sizes, ciphertext sizes/headers and main permutation
> segments are consistent with the selected PM-BG implementation. All nine
> original/decrypted SHA-256 comparisons match, as recorded in
> `docs/dataset_evidence.csv`. These are affirmative local artifact-consistency
> findings, not authentication of recorded timings, original run history or
> full manuscript reproduction. Historical notebook version, operator/author,
> run date, hardware/software and repetitions remain unconfirmed. Original
> inputs for Table 3 and the COMNET run are missing. MIT is confirmed for
> repository-owned code/docs/synthetic demo data; F1–F9 distribution decisions
> and team release approval remain pending. Local presence does not establish
> public availability or permission to distribute supplied files.

Review materials: [team discussion draft](team_review_draft.md) and
[distribution review register](dataset_distribution_review.csv), with all
F1–F9 decisions pending, alongside `docs/dataset_evidence.csv`. These records
are available locally for discussion; they do not record permission granted
or denied. See also the answers in [author questions](author_questions.md).

## A. Code-only availability (if only code is approved)

> Proposed fallback: release only approved repository-owned code and
> documentation under MIT after privacy and release review. Do not include
> supplied experiment inputs or reports in this scope. Selection of archival
> code does not establish the historical producing version or reproduction of
> all manuscript results. A final public statement must name only the actual,
> verified publication destination/version after release, not an assumed URL
> or DOI.

Pending: code provenance, contributors, inclusion list, privacy review and
team approval. This is an option, not an assertion that release has occurred.

## B. Preferred proposal — code/docs plus synthetic demonstrations (if approved)

> The proposed initial release consists of repository-owned code and
> documentation, synthetic inputs DEMO-001..DEMO-011 and clearly labelled new
> demonstration results under MIT, following privacy and team release review.
> Demo inputs are identified by SHA-256 in `data/manifest.csv`. Their five
> repetitions belong to new demonstrations, not to the historical manuscript
> protocol. Reviewed F1–F9 metadata/hash summaries may be included after a
> disclosure/privacy review; they are not the original dataset payloads.
> The entire `results/analysis result/` folder is proposed for exclusion,
> including original/encrypted/decrypted files, supplied TXT/MD reports,
> copied logs, DOCX manuscripts/UCEF reports and raw additional notebooks,
> pending per-artifact permission and privacy review. Artifact consistency
> does not establish historical provenance, authenticate timings, or reproduce
> UCEF analysis. This scope is a recommendation for team discussion, not
> approval or a statement of public availability.

Pending: contributors, exact inclusion allowlist, code/historical provenance
qualification, privacy review, per-artifact decisions and team release approval.
The proposed exclusion is **not implemented in `scripts/build_release.py`**.
An approved final statement must describe the actual published contents and
verified destination/version; no URL or DOI is invented in this draft.

## C. Code plus original experiment data (only if provenance + rights approved)

> If the team verifies provenance, manuscript mapping, hashes and
> redistribution authorization for particular artifacts, those exact files
> may be added to an approved release under their documented permissions.
> Repository-owned code remains under MIT; supplied data must not be labelled
> MIT without a valid rights basis. The inclusion list must identify each
> approved file and SHA-256, and distinguish omitted or missing inputs.
> Availability of files and original/decrypted equality alone do not establish
> historical experimental reproduction.

Every F1–F9 decision remains pending, including permission for encrypted and
decrypted copies. The team may approve files individually, arrange restricted
or request-only access if an authorized contact and procedure are established,
or exclude files. These options do not mean rights have been denied or granted.
Do not promise "available upon request" without that mechanism. Pending:
per-file evidence/conditions, privacy review, provenance, contributors,
inclusion list, team release approval and verified publication identifiers.

## Evidence limits to preserve in any final statement

- F1..F9 original/encrypted/decrypted files are locally available under
  `results/analysis result/File 1-MP4` through `File 9-EXE`. All nine
  original/decrypted hashes match; all 27 files were untracked on the audit
  date. Provenance and redistribution rights remain pending.
- Table 3 matches saved ori cell 1 stdout, but
  `FileAttachment.pdf_encrypted` and `COMNET-S-26-08200.pdf` are missing.
  Table 7 matches the saved TXT report (and its identical MD counterpart).
  These matches are evidence comparisons, not fresh experimental runs.
- Historical producing notebook version, operator/author, run date and original
  hardware/software environment/repetitions are unconfirmed. Additional ori notebook
  source/output equality is not an independent replication. The additional
  Shift128 notebook uses a different pipeline; its Figure 7 mapping is
  unconfirmed.
- UCEF v1.0/v3.0 DOCX reports are available locally, but the tool,
  configuration and standalone CSV/XLSX/figure exports have not been located;
  embedded figures do not establish a reproducible plotting pipeline.
  Reported encrypted-F9 statistics differ from current full-file statistics;
  input hashes, sampling/segments, and preprocessing need confirmation.
- The reported divergence/bit-difference values describe a prefix comparison
  including a 12-byte header, not controlled avalanche testing. Differential
  and KPA tests were not executed; CPA resistance was not demonstrated.
- OMML equation text has been extracted; original derivations and assumptions
  for Tables 8/9 still need confirmation.

## Release conditions and fixed rules

- MIT license choice is confirmed by the repository maintainer/user on
  2026-10-08; the earlier blanket placeholder/no-rights statement is historical
  and superseded. MIT covers repository-owned code/docs/synthetic demo data,
  not automatic rights to third-party F1..F9, the manuscript, or UCEF reports.
  Per-artifact permissions and release approval remain separate requirements.
- Never invent repository URLs, version identifiers, DOI, licenses, or
  contributor approvals; never claim publication or complete reproduction
  without verification.
- Require an explicit inclusion allowlist/filter before packaging.
  `scripts/build_release.py` collects all `results/` without rights gating;
  its DOCX/`Zone.Identifier` assertion is not a rights/privacy safeguard.
  Removing those files alone could still include restricted material.
- Implement the proposed whole-folder exclusion of `results/analysis result/`
  if approved; permit exceptions only through documented per-artifact review.
  This includes payloads, supplied TXT/MD reports, copied logs, DOCX/UCEF and
  raw additional notebooks, not merely DOCX files. Metadata/hash summaries
  also require disclosure review. Do not execute supplied MSI/EXE files during
  review; this precaution is not a finding that they are malicious.
- Review notebook outputs and logs for passwords/keys and private data;
  exclude secrets and material not authorized for the approved release.
  Do not reproduce existing experimental password values.
- The existing ZIP is a historical local candidate, with no
  `results/analysis result/` folder in its manifest. The earlier wording-only
  patch updated three member documents and checksums without adding research
  evidence. The parent-managed archive was selectively updated for MIT wording,
  not fully rebuilt with all current docs. No publication, archive or metadata
  updates occur in this turn; the older archive is not synchronized with this
  draft. Its existence does not establish approved release scope.
- README and the package-description copy now describe the audited local
  evidence. Verify their consistency with the approved scope before release.
