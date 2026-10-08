# Reproducibility

Updated 2026-10-08. Evidence details: `docs/evidence_audit.md`.

## Demo pipeline

```sh
pip install -r requirements.txt
python scripts/reproduce_all.py --config configs/demo.yaml
```

Steps: validate config → generate/verify seeded demo data against manifest
checksums → encrypt/decrypt and check integrity → write raw CSVs and summaries
→ generate demo figures → record environment/config → write execution report.
Each invocation creates `results/runs/<run_id>/`; the
`results/raw|summary|figures|logs` tree holds a copy of the latest run and
`.run_id` identifies it. The input manifest covers DEMO-001..011, not F1..F9.

Python ≥3.10; `requirements-lock.txt` records pinned versions.
`configs/demo.yaml` records warmup/repetition counts, demonstration password
and dataset sizes. `results/raw/environment.json` and `run_config.json`
provide provenance for these new local runs, not the original research runs.
Do not expect identical timings or random-IV ciphertexts across environments.

## Supplied experiment evidence

F1..F9 original/encrypted/decrypted triplets, a benchmark TXT/MD, additional
notebooks and UCEF reports are available locally under
`results/analysis result/`. See `docs/dataset_evidence.csv` for hashes and
`docs/manuscript_artifact_mapping.csv` for result mapping.

- Table 3 matches `ori` cell 1 saved stdout; the input is missing.
- Table 7 matches all nine supplied TXT/MD rows. File sizes/headers and
  permutation segments are consistent; 9/9 original–decrypted pairs match.
- UCEF reports provide stored results, not an executable evaluation tool.
- Shift128 is implemented in a different notebook family; its relation to
  the evaluated residual is unresolved.
- Whole-file F9 entropy/chi-square/adjacent Pearson calculations do not all
  agree with the UCEF report. Sampling and preprocessing remain unknown.

The provenance answer proposed for team discussion is **artifact consistency
verified; historical-run attribution unconfirmed**, rather than a blanket
absence of evidence. See `docs/team_review_draft.md`. The proposed initial
public release uses MIT code/docs/DEMO-001..011 and reviewed demo results;
it excludes the entire supplied research folder until per-artifact permission
and privacy review. This is not implemented in the builder or adopted by the
team, and the archive was not refreshed for this discussion draft.

The local demo command does not benchmark these F1..F9 files or regenerate
the original UCEF reports/figures. Their presence is not permission to release
them; at audit time the triplets were untracked and the DOCX reports ignored.

## Requirements before claiming manuscript reproduction

1. Obtain experimenter's input hashes, notebook/cell/version and run mapping.
2. Obtain original environment/dependencies, measurement settings, repetition
   counts and rule for selecting/aggregating table values.
3. Obtain FileAttachment/COMNET inputs or document their unavailability.
4. Obtain UCEF tool/configuration and input/segment/sampling definitions;
   explain the F9 discrepancies and Shift128 pipeline relationship.
5. Separate an approved rerun from supplied stored results and new demo runs.
   A newly matching run must not be labelled an original historical run.

## Validation

```sh
PYTHONPATH=src python -m pytest -q -p no:cacheprovider
```

The 2026-10-08 audit passed 64 tests, with one empty-input entropy warning in
the notebook reference. The test harness compares exercised package/reference
behavior, including fixed-IV ciphertext equality; it does not prove all
manuscript numerical results or cryptographic security.

## Wording to retain for demo results

> These are new local demonstration measurements, not reproductions of the
> manuscript's original numerical results.

This still applies to demo execution reports and measurements even though
additional experiment-supporting materials are now locally available. README
and its package-description copy now reflect this evidence. The existing ZIP
received three wording patches and updated checksums in the earlier cleanup.
The parent-managed archive was also selectively updated for MIT wording,
not fully rebuilt or synchronized with all current docs; archive/metadata edits
are outside this docs-only change. It contains no newly supplied F1..F9 files.

On 2026-10-08 the repository maintainer/user confirmed "Lisensi kami gunakan
MIT" for repository-owned code, documentation, and synthetic demo data, not
verified approval from all authors. MIT does not automatically grant rights
to third-party F1..F9, the manuscript, or UCEF/supplied reports. Provenance,
contributors, per-artifact permissions, and release/publication approval remain
pending; licensing does not validate reproduction. See author questions Q6/Q9.
