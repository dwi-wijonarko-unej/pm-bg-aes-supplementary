# Author questions — confirmed release decisions and scientific limitations

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on 2026-10-08.

Source: maintainer instruction for this task, "Tim sudah setuju semua, tinggal
konfirmasi di dokumen." The earlier team-review proposal is superseded by the
[conservative decision record](team_review_draft.md) and
[release approval](release_approval.md). Confirmation is maintainer-reported,
not individual signatures, third-party permissions or historical-run evidence.
Scientific questions below remain accepted limitations of the initial release,
not blanket approval blockers or claims of reproduced results.

Historical paths identify excluded private evidence; they are not runnable
inputs in the public package. See [evidence audit](evidence_audit.md),
[dataset evidence](dataset_evidence.csv) and
[distribution register](dataset_distribution_review.csv).

## Q1. Canonical implementation and original measurements — unresolved

`ori` cell 1 (`7495Mw2mNX3t`) is the selected archival reference. The additional
ori notebook had identical source/output but different metadata, not an
independent replication. Historical producing cell/version/commit, operator,
run date, hardware/software, repetitions and aggregation remain unconfirmed.

- Table 3 matched saved stdout: 0.0070 s, 14.27 MiB/s, 1125.57 KB, 99.9%,
  104300 → 104267 bytes. `FileAttachment.pdf_encrypted` remains missing;
  `COMNET-S-26-08200.pdf` is also unavailable. This is not a fresh rerun.
- All nine Table 7 rows matched the supplied TXT/MD report. Sizes, headers
  and main permutation segments were consistent; 9/9 original–decrypted
  hashes matched. These comparisons do not authenticate saved timings or
  prove that the recovered files came from the claimed historical runs.
- The new demo's five measured repetitions do not establish the original
  experimental protocol. Notebook MB/s is MiB/s; memory is `tracemalloc`
  traced allocation peak, not RSS. F8 prose 0.00045 s differs from the
  Table 7/log value 0.0045 s; the manuscript was not silently corrected.

Retain stored-result qualifications. Any later rerun must be separately dated
and must not be relabelled as an original historical run.

## Q2. Original F1..F9 — exclusion confirmed; source/rights unresolved

All nine original/encrypted/decrypted triplets and the entire
`results/analysis result/` folder are excluded from the initial public release.
The register records `exclude from initial public release; confirmed by maintainer`
and `maintainer-reported team approval for conservative release scope` for each.

Original acquisition sources, rights holders and redistribution terms remain
not documented. Approval supports exclusion, not affirmative permission to
redistribute plaintext, ciphertext or recovered copies. Later inclusion needs
per-artifact source/rights evidence, allowed channel and privacy review.
No request-only availability is promised. EXE/MSI were not executed during the
audit; their formats alone do not imply maliciousness or distribution rights.

The recorded sizes/hashes are historical identifiers, not proof of ownership.
The earlier audit's untracked-file finding is historical; the supplied baseline
later tracked research material in public Git history. Current-tree deletion
does not erase prior exposure.

## Q3. Shift128 and Figure 7 — unresolved

The excluded additional notebook implements ±128 modulo 256 in a distinct
complete-graph/unimodular/AES-128 whole-payload pipeline. It is not the
canonical permutation/AES-256 residual-tail pipeline. For canonical F9,
5423488 bytes with `n=32` gives zero plaintext residual. The intended pipeline,
input, residual definition and Figure 7 procedure remain unclear.

## Q4. UCEF analyzer — report-only, not reproduced

The earlier audit inspected UCEF v1.0 code analysis (score 60.00/100) and
v3.0 data analysis DOCX reports. These reports are excluded. Tool/source/binary,
configuration, verified input hashes, standalone CSV/XLSX exports and original
figure workflow remain unavailable. No look-alike scorer is provided.

## Q5. Equations and Tables 8/9 — unresolved

OMML mathematical text was extracted; earlier plain-text blanks did not mean
formulas were absent. Original derivations, calculation scripts, key-space
counting, attack rates, units and assumptions remain unconfirmed. The fixed
implemented permutation does not provide `n!` implemented key diversity.

## Q6. License — closed for approved repository-owned scope

MIT was confirmed by the maintainer on 2026-10-08 and retained in the adopted
team scope for repository-owned code/docs/synthetic demo data. Copyright holder
remains PM-BG-AES contributors. The earlier license placeholder is superseded.
MIT does not automatically cover excluded F1..F9, manuscripts or UCEF reports,
and does not authenticate experiments.

## Q7. Metadata names/order/title — confirmed; roles unspecified

The existing nine names in their existing order are confirmed: Samsul Arifin,
Ade Kurniawan, Muhamad Totoh Muharam, Ansori, Tiawan, Merios Gusan Putra,
Edwin Kristianto Sijabat, Dani Lukman Hakim, Dwi Wijonarko.
The title is PM-BG-AES Supplementary Research Artifacts.
`CITATION.cff`, `.zenodo.json` and `pyproject.toml` use this list; no specific
contributor roles, ORCIDs, emails or affiliations are inferred. The supplied
repository URL is https://github.com/dwi-wijonarko-unej/pm-bg-aes-supplementary.

## Q8. "AI selector" terminology — documented implementation limitation

The selected code uses deterministic file-size/entropy thresholds, not a
trained model. Public documentation describes a rule-based adaptive selector;
no trained model was found or invented.

## Q9. Initial release approval — confirmed; publication pending

The conservative v1.0.0 scope is adopted; tag is `v1.0.0`. Public notebooks are
sanitized copies in `notebooks/public/`, with source unchanged and saved
outputs/metadata stripped, not checksum-identical full-file originals. See
[notebook preservation/redaction](notebook_preservation_and_redaction.md) and
[public artifact review](public_artifact_review.csv).

Local candidate prepared; publication performed by maintainer after candidate validation.
The candidate archive must be a fresh v1.0.0 package matching the sanitized
snapshot, not the earlier selectively patched ZIP. Final scope/redaction and
run validation remain necessary. No release date or DOI is claimed.

## Q10. Password policy — implementation behavior documented

The notebook prompts say "digits only" but do not enforce that restriction;
the implementation accepts strings via UTF-8 encoding. Historical intended
policy remains unconfirmed. This does not fix the unsalted single-pass SHA-256
KDF or unauthenticated CBC. Existing experimental passwords must not appear
in public outputs/logs; demo passwords are explicitly non-secret.

## Q11. F9 statistical input/sampling — unresolved discrepancy

The report's encrypted F9 entropy 6.910008, chi-square 12468952.264704 and
adjacent r ≈ 0.000917 differ from the earlier full-file audit values
6.910783258, 33766723.685766 and 0.289727746. Input hashes, segment/length,
header handling, sampling and preprocessing remain unconfirmed. Do not
substitute audit calculations for the reported experiment or claim UCEF
reproduction. The detailed comparison remains in `docs/evidence_audit.md`.

## Q12. Divergence and attack claims — not security proofs

The reported 89.417345% byte and 42.830370% bit difference matched a ciphertext
prefix comparison including the 12-byte header, not controlled avalanche
experiments. Differential/KPA tests were not executed; CPA resistance was not
demonstrated. Retain these qualifications. Original figure mappings and
standalone exports remain incomplete; `demo-*` figures are not manuscript
Figures 5–7 or S1–S8. Round-trip success and permutation histograms are not
security proofs; the artifact is not production cryptography.
