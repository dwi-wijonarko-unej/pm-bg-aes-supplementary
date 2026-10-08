# Zenodo publication handoff (for the maintainer — no remote action taken)

Repository: https://github.com/dwi-wijonarko-unej/pm-bg-aes-supplementary
Intended tag: `v1.0.0` (not created in this task).
Final commit SHA: **pending maintainer commit** (candidate prepared on
`77cac3dd475f2999364ecd2f3c7d44e6ff6cb812` with local modifications listed
in `docs/release_preparation_report.md`).

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

## Steps for the maintainer

1. Review the final diff and this candidate (`docs/release_checklist.md`
   gates R1–R9 must stay PASS; section C stays unchecked until done).
2. Commit the approved state — including the 89 currently unstaged deletions
   recorded in `docs/exclusion_manifest.csv`.
3. Verify the clean intended tag snapshot contains only approved contents
   (compare `git archive v1.0.0` file list against `dist/release_manifest.csv`).
4. Enable this repository in Zenodo (GitHub → Zenodo integration).
5. Create GitHub Release `v1.0.0` from the verified tag. Zenodo will archive
   the tag snapshot automatically.
6. Inspect the Zenodo record: file list, title, version, creators, license,
   description. Confirm the archived snapshot matches the reviewed scope.
7. Record the assigned version DOI in metadata and the manuscript
   availability statement; keep the DOI-pending wording until then.

## Warnings

- A sanitized ZIP does not sanitize Git history. Excluded files removed from
  the new snapshot remain in earlier commits; if the maintainer requires full
  history hygiene, a scoped history-cleanup decision is needed (not performed
  here, and never automatic).
- The GitHub automatic source snapshot is independent of the custom ZIP:
  both must be checked (step 3 and step 6).
- Zenodo DOI: **pending assignment**. Do not cite a DOI until step 7.
- No commit, push, tag, release, or deposit was performed in this task.
