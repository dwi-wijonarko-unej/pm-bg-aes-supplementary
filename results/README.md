# Results

> These are new local demonstration measurements, not reproductions of the
> manuscript's original numerical results.

- `raw/benchmark_runs.csv` — one row per repetition (`warmup=true` rows are
  excluded from summaries). `len_tail` = AES-tail input length (residual
  bytes); `throughput_mib_s` denominator = phase input size.
- `raw/integrity_checks.csv` — dedicated encrypt→decrypt roundtrip per
  dataset (SHA-256 + MD5 + exact match).
- `raw/environment.json`, `raw/run_config.json` — provenance.
- `summary/performance_summary.csv` — count/mean/median/sample-stdev/min/max
  over measured runs only.
- `summary/integrity_summary.csv` — roundtrip status + decrypt match rate.
- `figures/` — PNG+SVG generated from raw CSVs (+`figure_manifest.csv`).
- `logs/experiment.log`, `logs/test_report.txt` — execution evidence.
- `runs/<run_id>/` — immutable per-run copies; the top-level
  `raw|summary|figures|logs` tree mirrors the latest run (see `.run_id`).
