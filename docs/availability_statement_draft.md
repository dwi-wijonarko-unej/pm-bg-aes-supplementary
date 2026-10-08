# Availability statement — approved scope, publication pending

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on 2026-10-08.

The filename is retained for existing links. The conservative initial scope is
now adopted, not merely proposed. Source: the maintainer's instruction for this
task, "Tim sudah setuju semua, tinggal konfirmasi di dokumen." This is not a
record of individual signatures, independent third-party permissions or
historical-run authentication. See [release approval](release_approval.md).

## Current candidate statement

> PM-BG-AES Supplementary Research Artifacts, version 1.0.0 (intended tag
> v1.0.0), is prepared as a local candidate for
> https://github.com/dwi-wijonarko-unej/pm-bg-aes-supplementary. The approved
> conservative scope comprises repository-owned code and documentation,
> synthetic inputs DEMO-001..DEMO-011, sanitized public notebooks and clearly
> labelled newly measured demo results under MIT, with reviewed historical
> evidence summaries. The nine metadata names and their existing order are
> confirmed without assigning specific contributor roles. Publication and DOI
> assignment remain with the maintainer after candidate validation; no release
> date or DOI is asserted here.
>
> All F1..F9 original/encrypted/decrypted payloads, the entire historical
> results/analysis result/ folder, raw/root notebook originals, DOCX
> manuscripts/UCEF reports and old distribution/results artifacts are excluded.
> Public notebooks preserve cell source while stripping saved outputs and
> metadata; they are not checksum-identical full-file originals. Historical
> paths and hashes identify excluded private evidence, not executable public
> inputs. No request-only access mechanism is promised.
>
> The earlier audit found Table 3 matching saved notebook stdout, all nine
> Table 7 rows matching the supplied TXT/MD report, and nine matching
> original–decrypted hashes. These establish artifact consistency, not
> authenticated historical timings or complete manuscript reproduction.
> Original producing version, operator, date, hardware/software and repetitions
> remain unconfirmed; Table 3/COMNET inputs are unavailable. UCEF tool/config,
> original figure workflow, F9 sampling discrepancies and Shift128/Figure 7
> mapping remain unresolved. New demo results are not reproductions of the
> manuscript's original numerical results. The artifact is not production
> cryptography.

Local candidate prepared; publication performed by maintainer after candidate validation.

## Scope and evidence records

- [Dataset evidence](dataset_evidence.csv) retains historical paths, sizes and
  hashes; [distribution register](dataset_distribution_review.csv) confirms
  exclusion for every F1..F9. Source/rights holder remain not documented.
- Maintainer-reported approval supports the conservative exclusion decision,
  not affirmative permission to redistribute excluded plaintext, encrypted or
  recovered materials. MIT is not a blanket license for third-party inputs.
- [Public notebook preservation/redaction](notebook_preservation_and_redaction.md)
  and [artifact review](public_artifact_review.csv) document sanitized copies.
- [Reproducibility](reproducibility.md) identifies the designated new run
  `v1.0.0-demo-20261008T020017Z` and its report/logs; these establish actual
  completion and validation rather than this statement alone.
- [Evidence audit](evidence_audit.md) and [limitations](limitations.md) retain
  scientific uncertainties accepted for the conservative release.

## Publication wording after validation

Only after the maintainer publishes the validated candidate should this
statement change from "local candidate" to "released" and identify the actual
release/archive and verified DOI, if assigned. The current archive must match
v1.0.0, not the historical wording-patched ZIP. No publication action is implied
by the repository URL or metadata. Excluding files from a new tracked snapshot
does not erase their earlier public Git history.
