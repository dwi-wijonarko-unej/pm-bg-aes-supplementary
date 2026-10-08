# Release Checklist (local candidate v0.1.0 — NOT an approved public release)

Audit reference: [evidence audit dated 2026-10-08](evidence_audit.md).
Status: **Assistant-authored evidence-based team-review draft, 2026-10-08**,
requested by the user for later discussion with the team. The MIT license-choice
gate is closed by the repository maintainer/user's 2026-10-08 confirmation.
Verified local consistency is listed separately below; original-run provenance,
per-artifact distribution decisions and team release approval remain unchecked.
This is not verified all-author approval or completion of release validation.
External publication has not been checked.

## Verified local consistency — facts, not completed approval gates

The 2026-10-08 audit records these findings; this docs-only turn does not rerun
the experiments:

- Table 3 matches ori cell 1 saved stdout: 0.0070 s, 14.27 MiB/s,
  1125.57 KB traced peak, 99.9%, and 104300 → 104267 bytes.
- All nine Table 7 rows match the supplied TXT report and identical MD copy.
  Input/matrix sizes, times, throughput, memory and overhead match; supplied
  ciphertext sizes/headers and main permutation segments are consistent with
  the selected PM-BG implementation.
- All nine original/decrypted SHA-256 comparisons match; sizes, paths and
  hashes are recorded in `docs/dataset_evidence.csv`.

These findings do not authenticate recorded timings, establish which historical
run produced each artifact, or grant distribution rights. UCEF remains
report-only with mixed/discrepant statistical evidence; Shift128 is a separate
pipeline, not a verified Figure 7 mapping.

## Original-run provenance and team confirmation — pending

- [ ] Authors acknowledge open items in `docs/author_questions.md`; available
      evidence is not treated as resolved confirmation.
- [ ] Confirm selected ori cell 1 provenance and mapping to Tables 3/7.
      Table 3 saved stdout matches 0.0070 s, 14.27 MiB/s, 1125.57 KB, 99.9%,
      and 104300 → 104267 bytes; `FileAttachment.pdf_encrypted` and
      `COMNET-S-26-08200.pdf` remain missing.
- [ ] Confirm Table 7 input/protocol mapping: all rows match
      `results/analysis result/2. File TXT - Paper PM-BG + AES_ori.txt`, with
      identical `File TXT - Paper PM-BG + AES_ori.md` content in that directory.
- [ ] Confirm the historical producing notebook/cell/version or commit,
      operator/author, run date, hardware/software environment, timing protocol
      and repetition counts; do not present DEMO-001..DEMO-011's five
      repetitions as the original protocol. The local audit date is not an
      authenticated original run date.
- [ ] Team accepts the evidence-based answers in `docs/author_questions.md`,
      including explicit limitations for historical details that cannot be
      recovered. Consider a fresh, separately labelled experiment if useful;
      it is not a demanded replacement or proof of the historical run.
- [ ] Confirm provenance, manuscript mapping, hashes, and per-file rights for
      F1..F9. The 27 local original/encrypted/decrypted files under
      `results/analysis result/File 1-MP4` through `File 9-EXE` were untracked;
      nine matching original/decrypted hashes do not establish release rights.
- [ ] Confirm additional notebook roles: additional ori source/output is
      identical to root ori (metadata differs), not an independent run. The
      additional Shift128 notebook uses ±128 modulo 256 in a different
      complete-graph/unimodular/AES-128 whole-payload pipeline, not the selected
      permutation/AES-256 tail pipeline.
- [ ] Resolve Figure 7 mapping, including F9 N = 5,423,488, n = 32, and zero
      plaintext residual; do not infer its Figure 7 role from local file presence.
- [ ] Obtain UCEF tool/configuration, CSV/XLSX exports, and figure workflow,
      or label scores report-only. Local DOCX reports v1.0 (score 60) and v3.0
      are not independent analyzer reproduction.
- [ ] Reconcile encrypted-F9 report statistics (entropy 6.910008, chi-square
      12468952.264704, adjacent r ≈ 0.000917) with full-file values
      (6.910783258, 33766723.685766, 0.289727746) using input hashes, sampling,
      segments, and preprocessing.
- [ ] Label divergence 89.417345% and bit difference 42.830370% as an
      original/ciphertext prefix comparison including the 12-byte header, not
      controlled avalanche testing. Differential/KPA were not executed and CPA
      resistance was not demonstrated; require evidence for any retained claims.
- [ ] Confirm original derivations and assumptions for Tables 8/9. OMML text
      is extracted; earlier plain-text blanks do not imply unavailable equations.

## Rights, privacy, and release scope — mandatory before rebuild

- [x] MIT license choice confirmed by the repository maintainer/user on
      2026-10-08: "Lisensi kami gunakan MIT" (Q6). Covers repository-owned
      code, documentation, and synthetic demo data; all-author approval is
      not verified. The earlier pending-license finding is historical and
      superseded, not the current licensing status.
- [ ] Review the preferred draft B scope in
      `docs/availability_statement_draft.md`: repository-owned code/docs,
      DEMO-001..DEMO-011 and clearly labelled new demo results under MIT after
      privacy and release review. F1–F9 metadata/hash summaries are candidates
      only after reviewing paths, filenames, hashes and disclosure risks.
- [ ] Team reviews `docs/team_review_draft.md` and fills actual decisions in
      `docs/dataset_distribution_review.csv`, using `docs/dataset_evidence.csv`
      as integrity evidence. These records have been prepared; every F1–F9
      distribution decision is still pending. Review-record existence is not
      permission or completion of this gate.
- [ ] Complete per-artifact ownership/redistribution review; MIT does not
      automatically cover third-party F1..F9, the manuscript, or UCEF/supplied
      reports. License choice does not establish provenance or publication
      approval.
- [ ] For every F1–F9 original/encrypted/decrypted file and other supplied
      artifact, record source/rights holder, evidence of permission, exact
      file/hash, decision-maker, date, permitted channel and conditions.
      All F1–F9 decisions remain pending. Team options are per-file public
      approval, restricted/request-only access with an established authorized
      contact/procedure, or exclusion. Do not promise "available upon request"
      without that mechanism; proposed exclusion is not proof of denied rights.
- [ ] Confirm contributors, citation metadata, contact, and optional ORCIDs;
      `CITATION.cff` and `.zenodo.json` remain draft until approved.
- [ ] Obtain explicit author approval BEFORE any push/release/deposit (Q9).
- [ ] Review the proposed exclusion of the **entire
      `results/analysis result/` folder**, including original/encrypted/decrypted
      payloads, supplied TXT/MD reports, copied logs, DOCX manuscripts/UCEF
      reports and raw additional notebooks, pending per-artifact permission
      and privacy review. This is a proposal, not a decision or implemented
      builder exclusion; exceptions need explicit per-file approval.
- [ ] Approve an explicit per-file inclusion allowlist and implement/enforce
      an inclusion filter before building. `scripts/build_release.py` currently
      collects all `results/` without rights gating. Its DOCX/`Zone.Identifier`
      assertion is insufficient: deleting those alone could package restricted
      files. Do not rebuild using that behavior as-is.
- [ ] Review notebook outputs/logs, CSVs, figures, and all included files for
      passwords, keys, private information, and unauthorized data. Do not copy
      existing experimental password values into public artifacts.
- [ ] Enforce the approved scope, including the proposed whole-folder
      exclusion if adopted; exclude `Zone.Identifier`, `.venv`, `.git`, caches,
      secrets and material without authorization for the release. Do not
      execute supplied MSI/EXE files during review; do not infer maliciousness
      merely from their file types.
- [ ] Verify README and its package-description copy remain consistent with
      the approved evidence and actual release scope; the wording cleanup
      does not imply provenance or publication approval.

## Validation of an approved candidate

- [ ] `python scripts/reproduce_all.py --config configs/demo.yaml` green;
      describe its output as demonstration validation, not full manuscript
      reproduction.
- [ ] `pytest` green; `results/logs/test_report.txt` stored and privacy-reviewed.
- [ ] `notebooks/original/*.ipynb` checksum-identical to intended workspace
      sources; distinguish whole-file checksums from source/output equivalence
      where metadata differs.
- [ ] No fake DOI / repository URL / Zenodo URL; placeholders remain until
      verified identifiers exist.
- [ ] Rebuild only after rights, inclusion-filter, privacy, and approval gates
      pass. The existing ZIP is a historical candidate, has no
      `results/analysis result/` folder in its manifest. The earlier wording-only
      patch updated three archived documents and checksums. The parent-managed
      archive was selectively updated for MIT wording, not fully rebuilt or
      synchronized with all current docs. No publication, archive or metadata
      updates occur in this turn; the older archive is not synchronized with
      these team-review drafts, and no supplied evidence files were added.
- [ ] `dist/release_manifest.csv` lists every approved archived file with
      SHA-256 and matches the approved inclusion list.
- [ ] `dist/artifact_checksums.sha256` verifies (`sha256sum -c`).
- [ ] `dist/pm-bg-aes-supplementary-v0.1.0.zip` exists, is non-empty, and its
      content equals the reviewed manifest; existence alone is not approval.
- [ ] Select an appropriate conditional availability statement and finalize
      it only after actual publication/availability is verified; never claim
      all manuscript results were reproduced on the basis of this audit.

Post-approval only: create the approved GitHub repository → push → tag the
approved release version → make the approved Zenodo deposit → record real
URLs/DOI in metadata and rebuild/revalidate the archive as needed. No step
here is authorized merely by editing this checklist.
