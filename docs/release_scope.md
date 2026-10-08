# v1.0.0 public release scope

The repository maintainer/user Dwi approved this scope on 2026-10-08.
This is a local builder policy, not evidence of publication, all-author approval,
or reproduction of historical manuscript experiments. Nothing here authorizes
pushes, tags, deposits, or remote releases.

## Included material

`configs/release_v1.0.0.yaml` is the explicit inclusion policy. The builder also
imposes a non-configurable scope ceiling and deny rules:

- Root `LICENSE`, `README.md`, `CITATION.cff`, `.zenodo.json`, `CHANGELOG.md`,
  `pyproject.toml`, `requirements.txt`, `requirements-lock.txt`, `.gitignore`.
- Public reviewed repository sources, tests, scripts, configs and docs beneath
  `src/`, `tests/`, `scripts/`, `configs/`, `docs/`.
- `data/README.md`, `data/manifest.csv`, and **only** the eleven synthetic
  DEMO-001..DEMO-011 payloads named by that manifest under `data/demo/`.
  Each payload must match manifest size/SHA-256 and permit redistribution.
  Unlisted demo files never enter the archive.
- Exactly four parent-sanitized notebooks under `notebooks/public/`:
  `PM_BG_+_AES_(works)_ori.ipynb`,
  `PM_BG_+_AES_(works)_workshop.ipynb`, `demo_colab.ipynb`,
  `analyze_results.ipynb`. Raw/original notebooks are not included.
- `results/README.md`, `results/.run_id`, and selected run
  `results/runs/v1.0.0-demo-20261008T020017Z/`'s `raw/`, `summary/`,
  `figures/`, `logs/`, and `EXECUTION_REPORT.md`. Other runs, extra run-root
  artifacts and scratch are excluded.
- Latest `results/raw/`, `summary/`, `figures/`, `logs/` mirrors are deliberately
  included because existing documentation uses those paths. Every permitted
  mirror member must equal its selected-run counterpart byte-for-byte, with
  identical member sets. `.run_id` must identify the selected run. This
  duplicates result payloads in the ZIP to preserve documented figure links.
  Set `include_latest: false` only after changing such links; it disables the
  latest tree permissions, not the run pointer requirement.

Missing required files, trees, or metadata versions fail before output creation.
`pyproject.toml`, `CITATION.cff`, `.zenodo.json` must identify 1.0.0 (Zenodo may
use `v1.0.0`); `CHANGELOG.md` must have a 1.0.0 heading. Legitimate URLs and
DOIs are not rejected by a blanket identifier regex.

## Denials and approval gate

The entire `results/analysis result/` tree, root raw notebooks,
`notebooks/original/`, all other notebooks, manuscript DOCX files,
`Zone.Identifier` streams, `.git`, virtual environments, caches, bytecode,
`.egg-info`, build/dist directories at any depth, scratch, backups, and
secret-like paths (`.env*`, `*.pem`, `*.key`, `private*`, `token*`,
`secrets/`, `credentials/`) are excluded. Denials are case-insensitive and
component-based. Explicitly requesting a denied or out-of-scope file/tree
raises `ReleaseError`; discovering denied members under an allowed tree skips
and prunes them. Symlinks encountered in selected paths or traversed trees
always fail, including links whose names would otherwise be denied. Absolute,
traversal, backslash, drive/colon and non-canonical relative paths fail.

`docs/public_artifact_review.csv` must exist with these columns:

```text
artifact_path,artifact_type,source_sha256,public_sha256,review_status,action,redaction_categories,source_code_changed,notes
```

Every included public notebook and result payload (including the selected run's
execution report and every latest mirror file) needs its own unique row.
`review_status` accepts `approved`, `approved_public`, or `public`;
`action` accepts `include`, `keep`, `sanitized`, `redacted`, or `redact`
(case-insensitive). `public_sha256` must match the current public bytes;
`source_sha256` must be a lowercase 64-character hexadecimal SHA-256. Notebook
`source_code_changed` must be `false` or `no`. Other columns retain the
parent's human review evidence, not automated semantic/privacy assertions.
Rows for excluded artifacts may record other decisions; they do not authorize
inclusion. Duplicate artifact paths fail. Docs describing the review and the
review CSV itself need no self-hash review entry, avoiding cyclic hashes.
`results/README.md` and `.run_id` are also outside the hash approval gate.

The parent performs source preservation, notebook sanitization, privacy review,
and the actual full demonstration. This builder checks approval records and
integrity; it is **not** a content-level secret scanner or rights assessor.
Broadly allowed code/docs trees must be reviewed before invocation. The
builder does not execute notebooks, experiments, or supplied binaries.

## Builder API and validation

Run from any directory with a literal repository root:

```sh
python scripts/build_release.py --root . --config configs/release_v1.0.0.yaml
python scripts/build_release.py --root . --verify
```

`--verify` is read-only: it rechecks policy, metadata, demo integrity, approvals,
mirrors, ZIP, checksum, and manifest against the current approved workspace.
It does not build missing outputs. Python callers can use
`load_config(root, config)`, `collect(root, policy)`,
`build_release(root, config, verify_only=False)`, and
`verify_archive(archive, manifest, checksums=None)`. `build_release` returns a
`Path`; validation failures raise `ReleaseError` (CLI exits 1).

Outputs are external to the archive under `dist/`:

- `pm-bg-aes-supplementary-v1.0.0.zip`
- `release_manifest.csv`: sorted unique POSIX paths, SHA-256, and byte sizes
- `artifact_checksums.sha256`: ZIP SHA-256 and basename

No manifest/checksum/archive recursively hashes or contains itself. ZIP members
must exactly equal the manifest in sorted order, without duplicates, directory,
encrypted or symlink entries. Validation checks each member's uncompressed
size, SHA-256 and CRC, and optionally the archive checksum. ZIP timestamps,
permissions, compression level and member order are fixed; repeat builds with
identical inputs and compression implementation are byte-identical. Temporary
outputs are validated before replacing existing outputs. Replacement of the
three output files is sequential, not a cross-file atomic transaction; verify
after interruption. Verification against the workspace additionally detects
policy/input changes since build.

Fixture-only tests in `tests/test_release_builder.py` construct tiny dummy
sources, notebooks, demo data and secrets in pytest temporary directories;
they do not read real source notebook payloads or build the repository release.
