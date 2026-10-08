# Release notes — v1.0.0 (local candidate, not yet published)

**PM-BG-AES Supplementary Research Artifacts, version 1.0.0 (intended tag
`v1.0.0`).** Local candidate prepared 2026-10-08 on baseline
`77cac3dd475f2999364ecd2f3c7d44e6ff6cb812` with local modifications.
**No GitHub Release, Zenodo deposit, or DOI assignment has occurred.**
Publication remains with the maintainer after candidate validation.

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on
2026-10-08 (see `docs/release_approval.md`).

## Scope

Included (MIT, holder `PM-BG-AES contributors`):

- Archival Python implementation ported from the selected notebook cell,
  CLI, tests, configs, scripts, dependency specifications.
- Public documentation, including evidence summaries with limitations.
- Synthetic demonstration inputs DEMO-001..DEMO-011 and the new local
  demonstration run `v1.0.0-demo-20261008T020017Z` (raw measurements,
  summaries, `demo-*` figures, logs, execution report).
- Four sanitized public notebooks (`notebooks/public/`): cell source
  unchanged, saved outputs/metadata stripped.

Excluded from this release: all F1..F9 original/encrypted/decrypted payloads,
the entire `results/analysis result/` tree, raw/root notebook originals, DOCX
manuscripts/UCEF reports, old runs and distribution artifacts, tracked
build artifacts, `.git/`, and private content. Exclusion is a release-scope
decision, not a statement on the scientific validity of the original data.
Historical paths/hashes identify excluded private evidence, not runnable
public inputs.

## What changed since the 0.1.0 local candidate

- Version aligned to 1.0.0 across package, citation, and archival metadata.
- MIT adopted for repository-owned code/docs/synthetic demo data.
- Conservative inclusion policy enforced by `scripts/build_release.py`
  (allowlist + deny rules + fail-closed) with 23 builder tests.
- New designated demonstration run with full execution evidence.
- Reviewed evidence summaries retained with documented limitations.
- See `CHANGELOG.md` for the full list.

## Demo vs original results

The `results/` measurements are **new local demonstration measurements on
synthetic inputs, not reproductions of the manuscript's original numerical
results**. They do not regenerate the supplied TXT/MD reports, UCEF analyses,
or manuscript Figures 5–7 / S1–S8. Round-trip success, histograms, and byte
differences are not security proofs.

## Known limitations (accepted for release)

Original operator/date/environment/repetitions unconfirmed; Table 3 input
missing; Table 7 stored-report consistency is not fresh timing reproduction;
UCEF tool/config missing; F9 statistical discrepancy unresolved; Shift128 /
Figure 7 linkage unresolved; main permutation publicly reconstructible;
AES-CBC tail without authentication. **Not for production cryptography.**
Details: `docs/limitations.md`, `docs/author_questions.md`.

## Verification evidence

- Full test suite: 158 passed, 0 failed (2026-10-08).
- Designated run completed exit 0; 11/11 roundtrips byte-identical;
  summaries recomputed from raw CSV; MiB/s units verified.
- Archive `dist/pm-bg-aes-supplementary-v1.0.0.zip` (163 members;
  size/SHA-256 in `dist/artifact_checksums.sha256`): manifest/members/checksum verified;
  extracted-package install (1.0.0), CLI, and roundtrip smoke test pass.
- Pre-release gates R1–R9: PASS (see `docs/release_checklist.md`).
