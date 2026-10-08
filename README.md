# PM-BG-AES — Supplementary Research Artifacts (local candidate v0.1.0)

Archival supplementary package for the paper _"Graph-Based Permutation
Matrix Generation and Intelligent Dynamic Block Optimization for Hybrid
Hill Cipher–AES Enterprise Data Protection"_ (draft 12 Sept 2026).
**Status: local review candidate; release approval and publication identifiers
are not confirmed by the repository. External publication was not checked.**

> These are new local demonstration measurements, not reproductions of the
> manuscript's original numerical results. F1..F9 triplets and supporting
> reports are available locally: artifact consistency is verified, while
> historical-run attribution is unconfirmed. Initial public-release exclusion
> of supplied research files is proposed for team review, not yet approved
> or enforced (see `docs/team_review_draft.md`).

## Scope

- **Preserved**: original notebooks byte-identical in `notebooks/original/`
  (checksums in `docs/source_inventory.md`).
- **Faithful port**: canonical notebook cell → `src/pm_bg_aes/` (Colab I/O
  adapted to local files; zero semantic changes in archival mode; see
  `docs/source_traceability.csv`, `docs/algorithm.md`).
- **Added transparently**: CLI, seeded demo dataset (DEMO-001..011),
  structured benchmarks, derived analyses, figures — all labelled as new.
- **Supplied local evidence**: F1..F9 triplets (9/9 original–decrypted hash
  matches), a Table 7 benchmark report, and UCEF v1.0/v3.0 reports under
  `results/analysis result/`. Table 3 matches saved notebook output; these
  comparisons do not establish original-run provenance or timing reproduction.
- **Separate variant**: Shift128 exists in an additional graph/unimodular/
  whole-payload AES notebook, not the canonical PM-BG/AES-tail pipeline.
  Its relationship to the paper's residual analysis remains unconfirmed.
- **Not reproduced / not approved for release**: UCEF tool/configuration,
  original evaluation/figure pipeline, and redistribution of supplied data
  or DOCX reports. No replacement scorer or missing-method imitation was built.

## Quick start

```
pip install -r requirements.txt
python scripts/reproduce_all.py --config configs/demo.yaml
pytest
```

## CLI

```
python -m pm_bg_aes.cli encrypt INPUT --output OUT   # password via getpass
python -m pm_bg_aes.cli decrypt INPUT --output OUT
python -m pm_bg_aes.cli verify ORIGINAL RECOVERED
python -m pm_bg_aes.cli inspect CIPHERTEXT
PM_BG_AES_DEMO_PASSWORD=... python -m pm_bg_aes.cli encrypt ... --demo-password ...
```

Non-interactive runs use an explicitly demonstration-only password (never a
secret; never logged). Colab users: see `notebooks/demo_colab.ipynb`.

## Results

`results/raw/` (per-repetition measurements + provenance),
`results/summary/`, `results/figures/` (PNG+SVG), `results/logs/`,
per-run dirs under `results/runs/`. Latest run report:
`results/runs/<id>/EXECUTION_REPORT.md`.

## Docs

`docs/source_inventory.md` · `source_traceability.csv` ·
`algorithm.md` · `file_format.md` · `benchmark_protocol.md` ·
`reproducibility.md` · `limitations.md` · `equivalence_report.md` ·
`manuscript_artifact_mapping.csv` · `author_questions.md`
(evidence-backed questions; provenance and approvals pending) ·
`availability_statement_draft.md` · `release_checklist.md` ·
`docs/evidence_audit.md` · `docs/dataset_evidence.csv` ·
`docs/team_review_draft.md` · `docs/dataset_distribution_review.csv`.

## Limitations & license

Research artifact. **Not for production use** (unauthenticated,
SHA-256 single-pass key derivation — see `docs/limitations.md`).
Repository-owned code, documentation, and synthetic demonstration data are
licensed under **MIT** (see `LICENSE`), as confirmed by the repository
maintainer on 2026-10-08. This does not grant rights to third-party F1..F9
inputs, manuscript/UCEF reports, or other externally owned materials.
Experimental provenance and per-artifact redistribution permissions remain
separate from the code license. Citation metadata (`CITATION.cff`,
`.zenodo.json`) is draft; contributor confirmation, release approval, and
DOI/URLs remain pending.
