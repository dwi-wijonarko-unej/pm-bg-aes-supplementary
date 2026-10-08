# Demonstration results — v1.0.0 candidate

> These are new local demonstration measurements, not reproductions of the
> manuscript's original numerical results.

The designated candidate run is **`v1.0.0-demo-20261008T020017Z`**, under
`results/runs/v1.0.0-demo-20261008T020017Z/`. Consult its `EXECUTION_REPORT.md`
and logs for actual completion and validation. Each run has its own evidence;
the top-level `raw/`, `summary/`, `figures/` and `logs/` mirror the latest run
identified by `.run_id`, and are not an independent replication.

Paths below are relative to the run directory (or its top-level latest copy):

- `raw/benchmark_runs.csv`: per-repetition measurements; `warmup=true` rows are
  excluded from summaries. `len_tail` is AES-tail input length, and
  `throughput_mib_s` uses phase input size as denominator.
- `raw/integrity_checks.csv`: dedicated encrypt→decrypt roundtrip checks
  (SHA-256, MD5 and exact byte equality).
- `raw/environment.json`, `raw/run_config.json`: actual environment/config
  and demonstration provenance, not the original research environment.
- `summary/performance_summary.csv`: measured count, mean, median, sample
  standard deviation, minimum and maximum, excluding warmups.
- `summary/integrity_summary.csv`: roundtrip status and decryption match rate.
- `figures/figure_manifest.csv`: figure IDs, paths, inputs and generation notes;
  PNG and SVG outputs use the demo IDs below.
- `logs/experiment.log`, `logs/test_report.txt`: execution and test evidence.

| Figure ID               | PNG file (SVG has the same stem) | Interpretation                                               |
| ----------------------- | -------------------------------- | ------------------------------------------------------------ |
| `demo-throughput`       | `demo_throughput.png`            | Mean measured throughput by demo dataset                     |
| `demo-elapsed`          | `demo_elapsed.png`               | Mean measured elapsed time, log scale                        |
| `demo-entropy`          | `demo_entropy.png`               | Input/ciphertext/recovered demo entropy                      |
| `demo-hist-DEMO-005`    | `demo_hist_DEMO-005.png`         | DEMO-005 original and fresh-encryption whole-file histograms |
| `demo-scatter-DEMO-004` | `demo_scatter_DEMO-004.png`      | DEMO-004 original/fresh ciphertext adjacent-byte subsamples  |

Histogram/scatter ciphertext is generated separately for the figures; it need
not equal a benchmark repetition's random-IV ciphertext. Demo IDs must never
be relabelled as manuscript Figures 5–7 or S1–S8. Roundtrip success and these
statistics do not prove cryptographic security.

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on 2026-10-08.
The entire historical `results/analysis result/` tree, all F1..F9 payloads,
reports and raw notebooks are excluded from the initial public scope. Old runs
and old distribution artifacts are not candidate validation evidence. Historical
paths/hashes in `docs/dataset_evidence.csv` identify excluded private evidence,
not files to load from this package. Source/rights holders remain not documented;
approval to exclude is not permission to redistribute. Earlier tracked public
Git history is not erased by candidate-tree deletion.

See [reproducibility](../docs/reproducibility.md),
[limitations](../docs/limitations.md) and [approval](../docs/release_approval.md).
Published as GitHub Release `v1.0.0` on 2026-10-08; version DOI
[10.5281/zenodo.23228132](https://doi.org/10.5281/zenodo.23228132).
