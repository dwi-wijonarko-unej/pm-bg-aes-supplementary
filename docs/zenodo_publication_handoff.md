# Zenodo publication record (published 2026-10-08 — was handoff, now record)

Repository: https://github.com/dwi-wijonarko-unej/pm-bg-aes-supplementary
Tag: `v1.0.0` (commit `1e3380d`).
Version DOI: **[10.5281/zenodo.23228132](https://doi.org/10.5281/zenodo.23228132)**
(assigned 2026-10-08; reported by the maintainer).

## Which metadata file is used

`.zenodo.json` (legacy Zenodo–GitHub schema): title
`PM-BG-AES Supplementary Research Artifacts`, version `1.0.0`,
`upload_type` software, license `mit`, 9 creators in confirmed order,
related identifier `isSupplementTo` the repository URL. `CITATION.cff`
agrees on title/version/license/creators. **No DOI invented**; version-DOI
field stays pending until Zenodo assigns it.

## Candidate archive

`dist/pm-bg-aes-supplementary-v1.0.0.zip` — 163 members. Authoritative
size/SHA-256 (kept outside the archive so the archive stays deterministic):

```sh
cat dist/artifact_checksums.sha256
python scripts/build_release.py --root . --verify
```

Manifest `dist/release_manifest.csv` (163 entries + header) and
`dist/artifact_checksums.sha256` verify with
`python scripts/build_release.py --root . --verify`.

## Steps for the maintainer (completed 2026-10-08 unless noted)

1. [x] Review the final diff and this candidate.
2. [x] Commit the approved state (`1e3380d`, tag `v1.0.0`).
3. [x] Verify the clean tag snapshot contains only approved contents.
4. [x] Enable this repository in Zenodo.
5. [x] Create GitHub Release `v1.0.0`.
6. [ ] Inspect the Zenodo record: file list, title, version, creators,
   license, description (maintainer to confirm against the published
   snapshot).
7. [x] Record the assigned version DOI
   ([10.5281/zenodo.23228132](https://doi.org/10.5281/zenodo.23228132)) in
   metadata and the manuscript availability statement.

## Standing warnings

- A sanitized snapshot does not sanitize Git history. Excluded files removed
  from the `v1.0.0` tree remain in earlier commits; any history cleanup is a
  separate scoped maintainer decision (not performed).
- The GitHub automatic source snapshot is independent of the custom ZIP:
  both were checked for the candidate (steps 3 and 6).

- Zenodo DOI **assigned**: [10.5281/zenodo.23228132](https://doi.org/10.5281/zenodo.23228132).
  Cite it; the DOI-pending wording is retired.
