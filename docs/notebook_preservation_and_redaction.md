# Notebook preservation and redaction

Original notebooks were inspected as JSON before any execution. Whole source
notebooks were never executed blindly: cells contain `input()`,
`google.colab.files.upload()/download()` and `!pip install` lines.

## Two classes

**A. Original evidence, retained privately.** The four source notebooks are
excluded from the v1.0.0 public snapshot and preserved outside the public
tree with their original SHA-256 (see `docs/exclusion_manifest.csv` for the
excluded-file record and `docs/public_artifact_review.csv` for per-artifact
source hashes):

| Source (private original) | Original SHA-256 |
| --- | --- |
| `PM_BG_+_AES_(works)_ori.ipynb` (root) | `7c226d4f…fb8b5` (full value in review CSV) |
| `PM_BG_+_AES_(works)_workshop.ipynb` (root) | `6bf294a5…9740ca` |
| `notebooks/demo_colab.ipynb` | `f7f78c74…5bc7ccc` |
| `notebooks/analyze_results.ipynb` | `1bb6b55a…73cfbd4` |

Private backup location (outside the repository, not in git, not in the
release ZIP): `/tmp/pm-bg-aes-excluded-backup-20261008/`. All 89 excluded
files were backup-verified by SHA-256 before removal from the working tree.
Originals must stay out of the public snapshot; any regeneration of public
copies uses `scripts/sanitize_notebooks.py` from the private backup.

**B. Sanitized public copies** under `notebooks/public/` (the only notebooks
in the release scope):

| Public copy | Public SHA-256 (review CSV) | Cells | Saved outputs removed |
| --- | --- | --- | --- |
| `PM_BG_+_AES_(works)_ori.ipynb` | `6a203068…4371a5f2e71` | 2 code (`pzmk8lalNUbQ`, `7495Mw2mNX3t`) | 5 outputs from cell 1 |
| `PM_BG_+_AES_(works)_workshop.ipynb` | `6544a5f0…23188febb4c` | 3 code | 5 outputs from cell 2 |
| `demo_colab.ipynb` | `c7257b49…0096680c803` | 4 markdown + 4 code | 5 outputs |
| `analyze_results.ipynb` | `6f084b92…7a0096680c803` | 1 markdown + 3 code | 7 outputs |

## Redaction applied (by category, no secret values reproduced)

- `saved_outputs_removed`: all cell `outputs` (stdout with saved metrics,
  echoed password prompts, widget HTML/JS, document previews) replaced with
  `[]`. Verified: 0 outputs remain in every public code cell.
- `saved_metadata_removed`: cell `metadata` cleared (Colab widget ids,
  `execution`/`executionInfo`, `base_uri`, `outputId`); notebook metadata
  reduced to `kernelspec` (+ `language_info` where present); `colab`
  provenance block removed. No `executionInfo`, user IDs, display names,
  local preview paths, or tokens remain in public files (verified by scan
  on 2026-10-08).
- `execution_count_removed`: all code-cell counts set to `null`.

## Source preservation

Joined code/markdown-cell `source` is byte-identical between each original
and its public copy (verified 2026-10-08 by regenerating with
`scripts/sanitize_notebooks.py` from the private backup and comparing).
`source_code_changed` is `false` for all four rows in
`docs/public_artifact_review.csv`. Public files are therefore **not**
checksum-identical full-file originals: use the public SHA-256, never the
historical original hash, to identify them.

`google.colab` import lines remain in cell *source* by design (source is
unchanged); only saved *outputs*/metadata were stripped. Sanitized copies
are not automatically non-interactive local executables.

## Credentials

No experimental password values are carried into public artifacts. The only
password present in the public tree is the fixed demonstration-only value
in `configs/demo.yaml` / recorded run configs
(`results/.../raw/run_config.json`), explicitly labelled non-secret and
never a user-entered real password. Third-party widget/notice outputs were
removed with the outputs; no third-party code requiring license-notice
retention is kept in stripped form.

## Re-verification

```sh
python scripts/sanitize_notebooks.py --check   # from a tree holding sources
```

Note: sources are excluded from the candidate tree, so `--check` is run
against the private backup. `docs/public_artifact_review.csv`
`public_sha256` values match current public bytes (enforced by
`scripts/build_release.py` at build time).
