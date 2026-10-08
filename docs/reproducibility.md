# Reproducibility

## Reproduce the synthetic demonstration

From the repository root, using Python ≥3.10:

```sh
pip install -r requirements.txt
python scripts/reproduce_all.py --config configs/demo.yaml
```

The pipeline validates configuration, generates/verifies seeded inputs against
`data/manifest.csv`, encrypts/decrypts, checks integrity, writes raw measurements
and summaries, produces demo figures, records environment/configuration, runs
tests and CLI smoke checks, and writes an execution report. The manifest covers
DEMO-001..DEMO-011, not the excluded manuscript inputs F1..F9.

`requirements-lock.txt` records pinned versions. `configs/demo.yaml` defines
warmup/measured repetitions, demo password and sizes. Random-IV ciphertexts,
timing and environment-dependent measurements need not be identical across runs.

## v1.0.0 candidate run

The designated full demonstration run is **`v1.0.0-demo-20261008T020017Z`**.
Its evidence belongs under:

```text
results/runs/v1.0.0-demo-20261008T020017Z/
  EXECUTION_REPORT.md
  raw/benchmark_runs.csv
  raw/integrity_checks.csv
  raw/environment.json
  raw/run_config.json
  summary/
  figures/figure_manifest.csv
  logs/experiment.log
  logs/test_report.txt
```

Consult those files for actual execution status, counts and validation results;
this document does not independently assert a successful run. Top-level
`results/raw/`, `summary/`, `figures/` and `logs/` mirror the latest run;
`results/.run_id` identifies it. Preserve per-run provenance; use a new unique
`--run-id` for subsequent runs rather than reusing the designated candidate ID.

Figure IDs are `demo-throughput`, `demo-elapsed`, `demo-entropy`,
`demo-hist-DEMO-005` and `demo-scatter-DEMO-004`, each with PNG/SVG outputs.
Histogram/scatter ciphertext is freshly generated for plotting, not necessarily
the benchmark repetition's ciphertext. These are not manuscript Figures 5–7
or S1–S8. See [results README](../results/README.md).

## Notebook preservation

Public notebooks are `notebooks/public/PM_BG_+_AES_(works)_ori.ipynb`,
`PM_BG_+_AES_(works)_workshop.ipynb`, `demo_colab.ipynb` and
`analyze_results.ipynb`. Their cell source is unchanged, while saved outputs
and metadata are stripped. Full-file original checksums in the historical
inventory do not apply to these sanitized files. Colab dependencies/interactive
I/O in original cell source remain; sanitized copies are not automatically
noninteractive local executables. See
[notebook preservation/redaction](notebook_preservation_and_redaction.md) and
[public artifact review](public_artifact_review.csv).

## Historical experiment evidence is excluded

The earlier audit inspected F1..F9 triplets, TXT/MD benchmark reports, additional
notebooks and UCEF DOCX reports. These are excluded private evidence, not inputs
shipped in the public candidate. [Dataset evidence](dataset_evidence.csv)
retains historical paths and hashes; [manuscript mapping](manuscript_artifact_mapping.csv)
records correspondence and gaps.

- Table 3 matched saved `ori` cell 1 stdout; its input remains missing.
- All nine Table 7 rows matched supplied TXT/MD. Sizes/headers/permutation
  segments were consistent, and 9/9 original–decrypted pairs matched.
- Historical producing version, operator, run date, environment and original
  repetitions/aggregation remain unconfirmed. Five demo repetitions do not
  establish the historical protocol.
- UCEF reports are report-only; the tool/config/input-run hashes and original
  standalone figure workflow remain unavailable. F9 full-file statistics do
  not all agree with the report; sampling/preprocessing are unknown.
- Shift128 belongs to another notebook pipeline; Figure 7/residual linkage is
  unresolved. Missing FileAttachment/COMNET inputs remain unavailable.

These findings establish **artifact consistency verified; historical-run
attribution unconfirmed**, not complete numerical reproduction. The demo
command does not regenerate those reports or benchmark excluded research data.

## Release decision and future reproduction claims

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on 2026-10-08.

The conservative MIT code/docs/synthetic demo scope is adopted; all F1..F9
payloads and `results/analysis result/` are excluded. Source/rights holders are
not documented; approval to exclude is not third-party redistribution permission.
Scientific gaps are accepted release limitations, not resolved findings.
Local candidate prepared; publication performed by maintainer after candidate validation.
Version is `1.0.0`, intended tag `v1.0.0`; no release date or DOI is claimed.

Before claiming original manuscript reproduction, recover input hashes/version
mapping, historical environment/protocol, missing inputs, UCEF definitions and
figure sources, and explain F9/Shift128 discrepancies. Separately date any new
rerun; never label it an original historical run. Deleting excluded files from
a candidate snapshot does not erase prior public Git history.

## Validation boundaries

```sh
PYTHONPATH=src python -m pytest -q -p no:cacheprovider
```

The earlier 2026-10-08 evidence audit recorded 64 passing tests and one
empty-input entropy warning in the notebook reference. That is a historical
audit result, not a fresh v1.0.0 validation claim. Candidate validation is
recorded in the designated run's execution report and logs. Tests exercise
reference/package behavior, including fixed-IV equivalence, not every malformed
input/password outcome, manuscript statistic or cryptographic security claim.

> These are new local demonstration measurements, not reproductions of the
> manuscript's original numerical results.
