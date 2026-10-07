# Reproducibility

## One command

```
python scripts/reproduce_all.py --config configs/demo.yaml
```

Steps: validate config → generate/verify demo data (seeded; manifest
checksums) → run experiments (encrypt+decrypt, integrity) → verify roundtrip
→ write raw CSVs → write summaries → generate figures → write
environment/provenance → write execution report. Existing results are never
overwritten silently: each invocation creates `results/runs/<run_id>/`; the
`results/raw|summary|figures|logs` tree holds a copy of the latest run plus
`.run_id` pointer.

## Environment

Python ≥3.10; `pip install -r requirements.txt`
(`requirements-lock.txt` pins the validated set).
`configs/demo.yaml` records warmup/repetition counts, demo password label,
and dataset sizes. `results/raw/environment.json` + `run_config.json`
capture everything needed to re-run.

## Scope honesty

Original F1..F9 inputs are unavailable, so this repository demonstrates and
measures a faithful implementation on **new synthetic data**. The sentence
below appears in the README, the execution report, and every summary CSV
header comment:

> "These are new local demonstration measurements, not reproductions of the
> manuscript's original numerical results."
