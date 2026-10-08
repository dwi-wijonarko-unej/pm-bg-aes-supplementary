# Benchmark Protocol

Two measurement layers are kept strictly separate — never compared as if
they shared a timing definition.

## A. Faithful notebook-compatible measurement

The adapted probe follows ori cell-1's read/transform/write timing scope:
`time.time()` around
read→transform→write, `tracemalloc` traced peak (KB), single
`psutil.Process().cpu_percent()` sample, throughput =
`input_size / 1024**2 / elapsed` (MiB/s), entropy before/after. Used only to
provide a separately labelled local measurement, not authenticate historical
Colab timings. Adapted calls/allocation behavior and hardware may differ;
equality of timings, traced peaks or CPU values is not established by
ciphertext equivalence tests.

## B. Structured local protocol (default; `configs/demo.yaml`)

- UTC timestamp, OS/arch, Python version, CPU model (when readable),
  logical CPU count, RAM, dependency versions, dataset SHA-256, config hash.
- `perf_counter()` around the crypto call **including** file read/write
  (disk I/O included — stated explicitly so readers do not mistake it for
  in-memory speed).
- 1 warmup run (excluded) + 5 measured runs per dataset per direction
  (configurable; any reduction is recorded with reason).
- Memory: `tracemalloc` traced-allocation peak, labelled as such (never
  "total RSS"); RSS is not sampled.
- Throughput denominator = phase input size (plaintext for encrypt,
  ciphertext for decrypt); unit MiB/s (`/1024**2`);
  manuscript tables say "MB/s" — a units note, not a restatement of values.
- Verbose matrix previews are excluded from the measured path.

## Supplied historical benchmark evidence (not protocols A/B reruns)

The Table 3 values match `ori` cell 1 saved stdout, but its
`FileAttachment.pdf_encrypted` input is not available. All Table 7 rows match
`results/analysis result/2. File TXT - Paper PM-BG + AES_ori.txt`; the F1..F9
triplets now exist locally. These stored values remain separate from new
measurements in `results/raw/`.

Original notebook/cell/version, environment, repetition count and aggregation
policy require experimenter confirmation. One listed result per direction
per file is not proof that only one run was performed. The demo's five
measured runs must not be attributed to the original study. See
`docs/evidence_audit.md` and author question Q1.

## Outputs

`results/raw/benchmark_runs.csv` (one row per repetition, warmup flagged),
`results/raw/integrity_checks.csv`, `results/raw/environment.json`,
`results/raw/run_config.json`, `results/logs/experiment.log`,
`results/summary/performance_summary.csv` (count/mean/median/sample-stdev/
min/max over measured runs only — no confidence intervals),
`results/summary/integrity_summary.csv`.
