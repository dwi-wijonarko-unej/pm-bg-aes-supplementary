# Release preparation report — v1.0.0 (published 2026-10-08; DOI 10.5281/zenodo.23228132)

This report records the candidate preparation. Publication has since
occurred: commit `1e3380d`, tag `v1.0.0`, GitHub Release `v1.0.0`, Zenodo
version DOI [10.5281/zenodo.23228132](https://doi.org/10.5281/zenodo.23228132).
Post-publication wording sync (badge, `doi`/`date-released`, released
statements) is recorded in `CHANGELOG.md`.

## 1. Baseline and dirty-state context

- Baseline commit: `77cac3dd475f2999364ecd2f3c7d44e6ff6cb812` (same as the
  previously inspected commit; verified with `git rev-parse HEAD`, branch
  `main`). No checkout/reset/rebase was performed.
- Workspace state at end of this task: 47 modified tracked files, 89
  unstaged deletions (all recorded in `docs/exclusion_manifest.csv`), 78
  untracked paths (candidate additions: sanitized notebooks, designated run,
  release config/docs, v1.0.0 ZIP + manifest + checksums, new tests/scripts).
- Nothing was staged, committed, pushed, tagged, released, or deposited.
  No Git history rewrite. Labelling follows the required convention:
  "v1.0.0 candidate workspace based on `77cac3d…`, with local modifications".

## 2. Approval recorded (exact)

"Team approval reported/confirmed by repository maintainer Dwi Wijonarko
on 2026-10-08." Source: maintainer instruction in this task
("Tim sudah setuju semua, tinggal konfirmasi di dokumen."). MIT adopted for
repository-owned code/docs/synthetic demo data. Approved conservative scope
adopted (repo-owned sources, docs, DEMO-001..011, new labelled demo results,
sanitized public notebooks, reviewed evidence summaries with limitations).
Approval does NOT establish third-party rights, historical run provenance,
UCEF reproduction, Shift128/Figure 7 mapping, or security claims. Remote
publication remains with the maintainer. Full record:
`docs/release_approval.md`; policy: `configs/release_v1.0.0.yaml`,
`docs/release_scope.md`.

## 3. Excluded materials and verified private backup

89 tracked files removed from the working tree (unstaged, for maintainer
commit), listed with SHA-256/sizes in `docs/exclusion_manifest.csv`:

- 37 files under `results/analysis result/` (27 F1..F9 payloads, TXT/MD
  reports, 2 notebooks, 6 `Zone.Identifier` streams).
- 6 raw/root notebooks (root ori/workshop, `notebooks/original/*`,
  `notebooks/analyze_results.ipynb`, `notebooks/demo_colab.ipynb`).
- 5 tracked `src/pm_bg_aes.egg-info/` files (regenerated once by
  `pip install` during smoke testing, then removed again).
- 40 files from old runs `20261007T042845Z` and `smoke01`.
- 1 superseded `dist/pm-bg-aes-supplementary-v0.1.0.zip`.

Private backup: `/tmp/pm-bg-aes-excluded-backup-20261008/` (outside repo,
not in git, not in ZIP), 89/89 SHA-256 verified before removal, plus the
manifest copy. Report to maintainer: preserve this backup; do not publish it.
`.gitignore` extended with precise rules against reintroduction.
EXE/MSI were not executed; exclusion implies no judgement on their content.

## 4. Public snapshot vs historical exposure

The future tag snapshot (after the maintainer commits the deletions) will
contain only approved scope. **Earlier tracked history still contains the
excluded materials** — removal from a new snapshot does not erase prior Git
exposure. No history rewrite was performed; any history cleanup is a separate
scoped maintainer decision. The old wording-patched v0.1.0 ZIP is superseded
and excluded from the new ZIP.

## 5. Metadata validation

`pyproject.toml` 1.0.0, `__version__` 1.0.0, `CITATION.cff` 1.0.0 (valid CFF
mapping, 9 authors, no `date-released`), `.zenodo.json` 1.0.0 (valid JSON,
software/mit, 9 creators, `isSupplementTo` repo URL; at preparation time the DOI
was pending and no fake DOI was used), README
candidate v1.0.0, builder 1.0.0, ZIP `pm-bg-aes-supplementary-v1.0.0.zip`.
Title/version/creators/license agree across CFF and Zenodo files. No `0.1.0`
remains in included scope; no DOI/URL placeholders remain; no fake DOI.

## 6. Tests (2026-10-08, Python 3.14.7, WSL2 x86_64, i7-1260P, 16 CPUs)

- Full suite: **158 passed, 0 failed, 0 skipped** (1 pre-existing
  empty-input entropy RuntimeWarning in notebook reference).
- Includes 23 release-builder tests + 6 reproducibility-pipeline tests.
- CLI `--help`, venv install (1.0.0), encrypt→decrypt→verify smoke:
  byte-identical.

## 7. Demo runs

- Designated run `v1.0.0-demo-20261008T020017Z` (executed 03:11:36Z, exit 0):
  11/11 roundtrips exact (recovered == manifest SHA-256), 110 measured +
  22 warmups + 22 notebook probes, 22-row summaries recomputed from raw
  (mean/median/stdev exact), throughput denominator `1024**2` verified,
  10 figure files + manifest with `demo-*` IDs, mirrors identical,
  `.run_id` points at the run, no demo password in logs/CSVs.
- Independent fresh run to `/tmp/opencode/verify-run` (outside repo):
  exit 0, all steps green — proves the pipeline genuinely executes here.

## 8. Archive and extraction

- `dist/pm-bg-aes-supplementary-v1.0.0.zip`: 163 members (authoritative
  size/SHA-256 in `dist/artifact_checksums.sha256`, outside the archive).
- `dist/release_manifest.csv` (160 entries, sorted, sizes/hashes match),
  `dist/artifact_checksums.sha256` match; builder `--verify` exit 0 plus an
  independent verification script: no absolute/traversal paths, no
  `analysis result`/DOCX/Zone.Identifier/dist recursion/private content, all
  expected artifacts present, 54/54 doc links resolve inside the ZIP.
- Extraction to `/tmp/opencode/extracted`: clean file list, venv install
  1.0.0, CLI help, DEMO-002 roundtrip MATCH, 17 representative tests passed.

## 9. Remaining scientific limitations (accepted, not claimed)

Operator/date/environment/repetitions unconfirmed; Table 3 input missing;
Table 7 is stored-report consistency, not fresh reproduction; UCEF
tool/config missing; F9 statistic discrepancy unresolved; Shift128/Figure 7
unresolved; differences are prefix comparisons, not avalanche tests; no
KPA/CPA/differential success demonstrated; permutation reconstructible;
unauthenticated AES-CBC tail; not production cryptography.

## 10. Checklist and remote status

Pre-release gates R1–R9: **all PASS** (`docs/release_checklist.md`).
Post-publication actions: release/tag/DOI done 2026-10-08; Zenodo record
inspection and manuscript-side citation update remain with the maintainer.
Exact maintainer actions: review diff → commit approved state (89
deletions) → verify clean `v1.0.0` snapshot → enable Zenodo → create GitHub
Release → verify Zenodo record → record version DOI → update manuscript
statement/citation. See `docs/zenodo_publication_handoff.md`.
Release notes: `docs/release_notes_v1.0.0.md`.
