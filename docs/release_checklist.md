# Release checklist — v1.0.0 (published 2026-10-08, DOI 10.5281/zenodo.23228132)

Baseline: commit `77cac3dd475f2999364ecd2f3c7d44e6ff6cb812` with local
modifications, committed as `1e3380d`, tagged `v1.0.0`. Candidate archive:
`dist/pm-bg-aes-supplementary-v1.0.0.zip`.
Evidence audit: `docs/evidence_audit.md` (2026-10-08). Approval:
`docs/release_approval.md` — team approval reported/confirmed by repository
maintainer Dwi Wijonarko on 2026-10-08; publication (tag, GitHub Release, Zenodo
DOI) completed by the maintainer on 2026-10-08 — see section C.

## A. Pre-release gates

| ID | Requirement | Status | Evidence | Verification command / date |
| --- | --- | --- | --- | --- |
| R1 | Release scope approved through maintainer's team confirmation | PASS | `docs/release_approval.md`; `configs/release_v1.0.0.yaml`; `docs/release_scope.md`. Conservative scope adopted; what approval does/does not establish recorded | Read approval record; 2026-10-08 |
| R2 | F1..F9 excluded from initial release unless exact rights-backed inclusion | PASS | `docs/exclusion_manifest.csv` (89 files: 37 under `results/analysis result/` incl. 27 F-payloads, 6 raw notebooks, 5 egg-info, 40 old-run files, 1 superseded ZIP); verified private backup `/tmp/pm-bg-aes-excluded-backup-20261008/` (89/89 SHA-256); ZIP has 160 members, zero `analysis result` entries; `dataset_distribution_review.csv` records exclusion for F1..F9 | `python3 scripts/build_release.py --root . --verify`; independent ZIP scan; 2026-10-08 |
| R3 | Public snapshot and archive privacy review completed | PASS | `docs/public_artifact_review.csv` (4 sanitized notebooks + demo payloads, `source_code_changed=false`); `docs/notebook_preservation_and_redaction.md`; 0 outputs remain in public notebooks; no user IDs/widgets; no experimental password values in included reports; archive scan clean (only doc/script self-mentions of redaction terms) | Builder review gate + `scripts/sanitize_notebooks.py` regeneration check vs private backup; 2026-10-08 |
| R4 | Contributors/metadata finalized without invented roles | PASS | 9 names in existing order in `CITATION.cff`, `.zenodo.json`, `pyproject.toml`; no ORCIDs/emails/affiliations/roles invented; MIT holder `PM-BG-AES contributors`; valid CFF mapping + valid JSON; agreed title/version/license across both files | `python3 -c` CFF/YAML + JSON parse; 2026-10-08 |
| R5 | All current version fields consistent with v1.0.0 | PASS | `pyproject.toml` 1.0.0, `__version__` 1.0.0, `CITATION.cff` 1.0.0 (+ `doi` + `date-released` 2026-10-08), `.zenodo.json` 1.0.0, README v1.0.0 + badge, builder `1.0.0`, ZIP `pm-bg-aes-supplementary-v1.0.0.zip`; no `0.1.0` in included scope; version DOI [10.5281/zenodo.23228132](https://doi.org/10.5281/zenodo.23228132) recorded after assignment (never invented) | `git grep 0\.1\.0` scoped to included paths; builder `validate_metadata`; 2026-10-08 |
| R6 | Builder scope filter implemented and tested | PASS | `scripts/build_release.py`: explicit config + allowlist + case-insensitive deny rules + fail-closed; 23 tests in `tests/test_release_builder.py` (denied-tree rejection, Zone.Identifier/DOCX skip, secret fixtures, dist recursion, deterministic manifest, entries==manifest, size/hash match, tamper rejection) | `pytest tests/test_release_builder.py` within full suite: 158 passed; 2026-10-08 |
| R7 | Full tests and actual demo pipeline pass | PASS | Full suite 158 passed, 0 failed; designated run `v1.0.0-demo-20261008T020017Z` completed exit 0 (11/11 roundtrips byte-identical, 110 measured + 22 warmups + 22 probes, summaries recomputed, MiB/s verified); independent fresh run to `/tmp/opencode/verify-run` exit 0; venv install 1.0.0 + CLI enc/dec smoke byte-identical | `pytest`, `scripts/reproduce_all.py`, deep verification script; 2026-10-08 |
| R8 | ZIP/manifest/checksum verified and extracted-package smoke test passes | PASS | ZIP 163 members == 164-line manifest (header + 163); size/SHA-256 in `dist/artifact_checksums.sha256`; all member size/SHA-256 match; extraction to `/tmp/opencode/extracted`: install 1.0.0, CLI help, DEMO-002 roundtrip MATCH, 17 representative tests passed | Builder `--verify` + independent scan + extraction script; 2026-10-08 |
| R9 | README/availability wording matches actual candidate content | PASS | `README.md`, `docs/availability_statement_draft.md`, `docs/reproducibility.md`, `results/README.md`, `data/README.md` describe the sanitized candidate, designated run, exclusions, and demo-vs-original distinction; 54/54 included doc links resolve inside the ZIP; no "available upon request" promise | Link check against ZIP members; 2026-10-08 |

## B. Accepted scientific / data limitations (not pre-release FAILs)

These are honestly documented and excluded or labelled; none is claimed as
reproduced. Statuses use ACCEPTED LIMITATION / UNRESOLVED, NOT CLAIMED AS
REPRODUCED.

- Original operator/date/hardware/software/repetitions: UNRESOLVED, NOT CLAIMED AS REPRODUCED (`docs/limitations.md` §6, `author_questions.md` Q1).
- Table 3 input (`FileAttachment.pdf_encrypted`, COMNET) missing: UNRESOLVED.
- Table 7 stored-report consistency vs fresh timing reproduction: ACCEPTED LIMITATION (consistency verified; run attribution unconfirmed).
- UCEF tool/config/exports: UNRESOLVED; reports report-only.
- F9 full-file statistics vs report values: UNRESOLVED discrepancy, documented.
- Shift128 variant linkage to Figure 7: UNRESOLVED.
- Difference rates as controlled avalanche experiments: NOT CLAIMED (labelled prefix comparison incl. header).
- No KPA/CPA/differential attack success demonstrated: NOT CLAIMED.
- Fixed main permutation publicly reconstructible; AES-CBC tail only, unauthenticated; not production cryptography: documented limitation.
- Third-party rights for excluded materials: UNRESOLVED by design — excluded, not redistributed; exclusion approval is not redistribution permission.

## C. Post-publication actions (completed 2026-10-08 except Zenodo record inspection)

- [x] Maintainer reviews final diff and candidate.
- [x] Maintainer commits approved state.
- [x] Verify clean intended tag snapshot.
- [x] Enable correct repository in Zenodo.
- [x] Create actual GitHub Release v1.0.0.
- [ ] Verify Zenodo record contents and metadata (maintainer to confirm
  against the published snapshot).
- [x] Record actual version DOI
  ([10.5281/zenodo.23228132](https://doi.org/10.5281/zenodo.23228132)).
- [ ] Update manuscript availability statement and citation as appropriate
  (repository statement done; manuscript-side update remains with authors).

Historical note: removing excluded files from a new snapshot does NOT erase
prior Git history. If sensitive content is found in tracked history, a scoped
history-cleanup decision belongs to the maintainer; no history rewrite was
performed in this task. Exact research test passwords observed in excluded
supplied reports are classified as research test credentials; they are excluded
from public artifacts, not published, rotated, or claimed as production secrets.
