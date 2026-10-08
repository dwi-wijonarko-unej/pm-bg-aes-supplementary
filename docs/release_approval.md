# v1.0.0 release approval record

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on 2026-10-08.

## Source and meaning

Source: repository maintainer Dwi Wijonarko's instruction for the current task
on 2026-10-08: **"Tim sudah setuju semua, tinggal konfirmasi di dokumen."**
This record adopts the initially proposed conservative scope. It reports the
maintainer's confirmation; it does not invent individual signatures, independent
third-party approvals, contributor roles or historical experiment provenance.
The earlier team-review proposal is retained by context in
[the decision record](team_review_draft.md); its pending approval status is superseded.

## Confirmed decisions

- Candidate version **1.0.0**, intended tag **v1.0.0**.
- Title **PM-BG-AES Supplementary Research Artifacts**.
- Repository https://github.com/dwi-wijonarko-unej/pm-bg-aes-supplementary.
- MIT for repository-owned code, documentation and synthetic demonstration
  data; preserve copyright holder **PM-BG-AES contributors**.
- The existing nine metadata names in the existing order: Samsul Arifin,
  Ade Kurniawan, Muhamad Totoh Muharam, Ansori, Tiawan, Merios Gusan Putra,
  Edwin Kristianto Sijabat, Dani Lukman Hakim, Dwi Wijonarko. No specific roles,
  ORCIDs, affiliations or contact details are assigned by this confirmation.
- Include repository-owned software/docs, DEMO-001..DEMO-011, clearly labelled
  new demo results, sanitized public notebooks and reviewed evidence summaries.
- Exclude every F1..F9 original/encrypted/decrypted payload and the **entire**
  `results/analysis result/` tree, including supplied reports, copied logs,
  raw additional notebooks and UCEF materials. Exclude DOCX manuscripts/reports,
  root/raw notebook originals, old distribution/results artifacts, tracked
  egg-info, `.git/`, attachment metadata, secrets and private content.
- Use sanitized copies in `notebooks/public/` with cell source unchanged and
  saved outputs/metadata stripped. Public files are not checksum-identical
  full-file originals. See [preservation/redaction](notebook_preservation_and_redaction.md)
  and [artifact review](public_artifact_review.csv).
- Designated new demonstration run: `v1.0.0-demo-20261008T020017Z`; its execution
  report and logs establish actual run completion/validation.

## Exclusion is not permission to distribute research data

For each F1..F9, the distribution register records:

- `team_decision_status`: `exclude from initial public release; confirmed by maintainer`
- `permission_evidence`: `maintainer-reported team approval for conservative release scope`

Source and rights holder remain unknown/not documented. The recorded evidence
supports the decision to **exclude**, not an affirmative redistribution license
for plaintext, ciphertext or decrypted copies. No request-only availability is
promised. Any later inclusion needs separate per-artifact rights/privacy review.

## Accepted scientific limitations

Approval does not authenticate the original operator, date, hardware/software,
repetitions or producing notebook version. Table 3's input remains missing;
Table 7 has stored-report consistency, not independently reproduced timing.
UCEF tool/configuration are unavailable; F9 full-file statistics disagree with
some report values; Shift128/Figure 7 linkage is unclear. The main permutation
is publicly reconstructible, AES covers the tail without authentication, and
this artifact is not production cryptography. These are retained limitations,
not resolved scientific claims. See [limitations](limitations.md) and
[evidence audit](evidence_audit.md).

## Candidate versus publication

Local candidate prepared; publication performed by maintainer after candidate validation.
That publication has now occurred: GitHub Release `v1.0.0` (commit `1e3380d`,
tag `v1.0.0`) on 2026-10-08, archived on Zenodo with version DOI
[10.5281/zenodo.23228132](https://doi.org/10.5281/zenodo.23228132). No other
release date or DOI is claimed. The v1.0.0 archive was a fresh candidate matching
the sanitized snapshot, not the earlier patched ZIP.

Excluded material is preserved as private evidence outside the public snapshot;
historical CSV paths/hashes remain identification records, not runnable inputs.
Deletion from the candidate's current tree does not erase previously tracked
public Git history or establish that prior exposure never happened. Final
candidate content, notebook redaction, archive and run validation must be checked
before the maintainer publishes.
