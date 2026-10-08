# PM-BG-AES Supplementary Research Artifacts

**Version 1.0.0 · intended tag `v1.0.0` · local release candidate**

Supplementary research software for _Graph-Based Permutation Matrix Generation
and Intelligent Dynamic Block Optimization for Hybrid Hill Cipher–AES Enterprise
Data Protection_ (manuscript draft dated 12 Sept 2026).

Repository: https://github.com/dwi-wijonarko-unej/pm-bg-aes-supplementary

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on 2026-10-08.

The approved initial scope is repository-owned code, documentation, synthetic
inputs and clearly labelled new demonstration results under MIT, plus sanitized
public notebooks and reviewed evidence summaries. Approval is reported by the
maintainer, not individual signatures, third-party redistribution permission or
confirmation of historical experiments. See [release approval](docs/release_approval.md).
Local candidate prepared; publication performed by maintainer after candidate
validation. No release date, publication action or DOI assignment is claimed.

> These are new local demonstration measurements, not reproductions of the
> manuscript's original numerical results. **Not for production cryptography.**

## Scope and evidence

- **Selected implementation:** faithful Python port of `ori` cell 1, with Colab
  I/O adapted to local files; see `docs/source_traceability.csv` and
  [algorithm](docs/algorithm.md). Selection does not establish the historical
  producing version for every manuscript result.
- **Public notebooks:** sanitized copies under `notebooks/public/`:
  `PM_BG_+_AES_(works)_ori.ipynb`, `PM_BG_+_AES_(works)_workshop.ipynb`,
  `demo_colab.ipynb`, and `analyze_results.ipynb`. Cell source is preserved;
  saved outputs and metadata are stripped. These are not checksum-identical
  full-file originals. See [preservation and redaction](docs/notebook_preservation_and_redaction.md)
  and [public artifact review](docs/public_artifact_review.csv).
- **New demonstrations:** seeded DEMO-001..DEMO-011 inputs, repeated measurements,
  integrity checks, derived analysis and `demo-*` figures; not F1..F9 replacements.
- **Historical evidence summaries:** the earlier audit found Table 3 matching
  saved notebook stdout, all nine Table 7 rows matching the supplied TXT/MD,
  and 9/9 original–decrypted hash matches. Historical operator, run date,
  hardware/software and repetitions remain unconfirmed. These comparisons
  establish artifact consistency, not timing reproduction.
- **Excluded:** F1..F9 original/encrypted/decrypted payloads, the entire
  `results/analysis result/` folder, root and raw original notebooks, DOCX
  manuscripts/UCEF reports, old runs/distribution artifacts, tracked egg-info,
  `.git/` and private attachment metadata. Historical paths in evidence records
  identify excluded private evidence, not executable inputs in the public package.
  Removing tracked files from a new snapshot does not erase prior Git history.

## Quick start

From the repository root, with Python 3.10 or newer:

```sh
pip install -r requirements.txt
python scripts/reproduce_all.py --config configs/demo.yaml
PYTHONPATH=src python -m pytest -q -p no:cacheprovider
```

`requirements-lock.txt` records pinned dependencies. The pipeline records the
actual environment and configuration; timings and random-IV ciphertexts vary.
For installation as a package, use `pip install .` (analysis/test dependencies
are also provided through the project's optional extras).

## CLI

```sh
python -m pm_bg_aes.cli encrypt INPUT --output OUT
python -m pm_bg_aes.cli decrypt INPUT --output OUT
python -m pm_bg_aes.cli verify ORIGINAL RECOVERED
python -m pm_bg_aes.cli inspect CIPHERTEXT
```

Encryption/decryption prompt for a password. Noninteractive demonstrations use
an explicitly demonstration-only password, never a real secret. The public
Colab entry point is `notebooks/public/demo_colab.ipynb`.

## Candidate demonstration results

The designated v1.0.0 demonstration run is
`v1.0.0-demo-20261008T020017Z`. Its execution report and evidence belong under
`results/runs/v1.0.0-demo-20261008T020017Z/`; consult its `EXECUTION_REPORT.md`,
`raw/environment.json`, `raw/run_config.json`, and `logs/test_report.txt` for
actual completion and validation, rather than inferring success from this README.
The top-level `results/raw/`, `summary/`, `figures/`, and `logs/` are latest-run
copies identified by `results/.run_id`.

Figure IDs are `demo-throughput`, `demo-elapsed`, `demo-entropy`,
`demo-hist-DEMO-005`, and `demo-scatter-DEMO-004`, with PNG/SVG outputs. They are
not manuscript Figures 5–7 or S1–S8. See [results](results/README.md) and
[reproducibility](docs/reproducibility.md).

## Documentation, citation and license

- [Source inventory](docs/source_inventory.md), [file format](docs/file_format.md),
  [benchmark protocol](docs/benchmark_protocol.md), [equivalence report](docs/equivalence_report.md).
- [Evidence audit](docs/evidence_audit.md), [dataset hashes](docs/dataset_evidence.csv),
  [distribution decisions](docs/dataset_distribution_review.csv),
  [manuscript mapping](docs/manuscript_artifact_mapping.csv).
- [Approval record](docs/release_approval.md), [team decision record](docs/team_review_draft.md),
  [author questions](docs/author_questions.md), [availability statement](docs/availability_statement_draft.md),
  [limitations](docs/limitations.md).

`CITATION.cff` and `.zenodo.json` use the confirmed nine metadata names in their
existing order, without assigning contributor roles. Version is `1.0.0`; tag is
`v1.0.0`. DOI and actual release date will be recorded only after publication.

[MIT](LICENSE) covers repository-owned code, documentation and synthetic demo
inputs. The accepted holder is **PM-BG-AES contributors**. It does not grant
rights to excluded third-party inputs or reports. The fixed main permutation is
publicly reconstructible; AES-CBC protects only the residual tail, without
authentication and with single-pass SHA-256 password derivation. Round-trip
success, histograms and byte differences are not security proofs.
