# Author Questions — [BUTUH INPUT PENULIS]

Status: **open, pending author confirmation**. Nothing here blocks the local
demo/benchmark pipeline; everything here blocks claims about the manuscript.

## Q1. Canonical implementation confirmation
`PM_BG_+_AES_(works)_ori.ipynb` cell 1 and
`PM_BG_+_AES_(works)_workshop.ipynb` cell 1 are byte-identical, and cell 0 of
both files is a simpler variant (no metrics, has `md5`). We selected **ori
cell 1 as the canonical archival implementation**. Please confirm:
(a) this is the cell that produced Tables 3/7, or (b) which cell/commit did.
Until confirmed, code is labelled "canonical archival implementation selected
from supplied notebook".

## Q2. Original datasets F1..F9
The workspace contains no F1..F9 files (`FileAttachment.pdf`,
`COMNET-S-26-08200.pdf`, MP4/MP3/JPG/PNG/PDF/MSI/ZIP/TXT/EXE). Can the
original files (or their SHA-256 checksums + sizes) be shared for a true
reproduction? If they are copyrighted/third-party, please state redistribution
restrictions so we record correct `license_status`/`redistribution_allowed`.

## Q3. Shift-128 definition
The manuscript discusses a "Shift-128 residual transformation" (Fig. 7, §
Results), but the notebooks implement only the AES-CBC residual tail. Please
provide the Shift-128 definition/implementation or confirm it is out of scope
for the code artifact (we currently record it as missing, no imitation made).

## Q4. UCEF-Code Security Analyzer
Table 6 cites UCEF v1.0 with score 60.00/100. The tool/spec is not in the
workspace. Is UCEF available (source, binary, or spec) for archiving, or
should Table 6 remain manuscript-reported-only (category F)? We will not build
a look-alike scorer.

## Q5. Missing formula details
Several equations extract as blanks from the DOCX (OMML): chi-square
statistic, Pearson correlation, key-space combinatorics, the exact F8/F9
entropy and χ² numbers, and the brute-force rate assumptions behind
Tables 8–9. Please confirm the formulae or point to the source commit that
generated them.

## Q6. License selection — [BUTUH INPUT PENULIS]
No license was found in the sources. `LICENSE` is a placeholder
("License selection pending author approval"). Options:
(a) MIT, (b) BSD-3-Clause, (c) Apache-2.0, (d) CC-BY-4.0 for
data/docs + code license, (e) all-rights-reserved (no public release).
**No open-source license is claimed until the authors confirm.**

## Q7. Authorship vs. contributorship
Manuscript authors (9 names) are recorded from the draft; software
contributors may differ. Please confirm the contributor list, corresponding
contact, affiliations/ORCIDs (optional), and the citation title exactly as it
should appear in `CITATION.cff`/`.zenodo.json` (both marked draft).

## Q8. "AI selector" terminology
The code is a deterministic rule table (file size × entropy thresholds), not a
trained ML model. May we describe it as "rule-based adaptive selector (called
'AI selector' in the notebook)" in all docs, or is there a trained model
behind the thresholds that should be archived?

## Q9. Release approval
Confirm before any public step: GitHub repository URL, Zenodo deposit,
release version, and whether the DOCX manuscript may be included in any
archive (currently excluded by default). No commit/push/release/deposit will
be made without explicit approval.

## Q10. Password policy
The notebook prompts say "digits only" but the code never validates digits
(any string works via `str(password2)`). Is the digits-only restriction
intended (→ enforce + document) or should the artifact document actual
behaviour (any string, UTF-8 encoded)? We currently document actual behaviour.
