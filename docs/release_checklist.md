# Release Checklist (local candidate v0.1.0 — NOT a public release)

- [ ] `python scripts/reproduce_all.py --config configs/demo.yaml` green
- [ ] `pytest` green; `results/logs/test_report.txt` stored
- [ ] `notebooks/original/*.ipynb` checksum-identical to workspace sources
- [ ] No fake DOI / repo URL / Zenodo URL anywhere (`grep DOI` → placeholders only)
- [ ] No passwords/keys in logs, CSVs, figures, notebooks
- [ ] No DOCX manuscript, `.venv`, `.git`, caches, secrets in `dist/`
- [ ] `dist/release_manifest.csv` lists every archived file with SHA-256
- [ ] `dist/artifact_checksums.sha256` verifies (`sha256sum -c`)
- [ ] `dist/pm-bg-aes-supplementary-v0.1.0.zip` exists, non-empty, content == manifest
- [ ] `CITATION.cff` + `.zenodo.json` marked draft; no invented ORCID/e-mail/license
- [ ] `docs/author_questions.md` open items acknowledged by authors
- [ ] LICENSE placeholder acknowledged (no rights claimed)
- [ ] Author approval obtained BEFORE any push/release/deposit (Q9)

Post-approval only: create GitHub repo → push → tag v0.1.0 → Zenodo deposit →
fill real URLs/DOI back into metadata (new commit, new archive).
