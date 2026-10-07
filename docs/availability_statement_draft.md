# Data Availability — Draft Statements (nothing published; placeholders only)

## A. Code-only availability (use if demo data cannot be released)

> The archival implementation supporting this study is available for review
> at [GITHUB_REPOSITORY_URL] (release [RELEASE_VERSION], archived at
> [ZENODO_VERSION_DOI]). Original experiment inputs (F1..F9) are not
> redistributed. [BUTUH INPUT PENULIS: confirm repository URL, version, DOI,
> license.]

## B. Code plus demonstration dataset (current default)

> The archival implementation, demonstration dataset (DEMO-001..DEMO-007,
> synthetic and clearly labelled, `data/manifest.csv` with SHA-256), and
> actual local measurements (`results/raw/`, `results/summary/`,
> `results/figures/`, `results/logs/`) are available for review at
> [GITHUB_REPOSITORY_URL] (release [RELEASE_VERSION], archived at
> [ZENODO_VERSION_DOI]). These are new local demonstration measurements, not
> reproductions of the manuscript's original numerical results. The original
> F1..F9 experiment files are not included. [BUTUH INPUT PENULIS: confirm
> URL, version, DOI, license.]

## C. Code plus original experiment data (ONLY if authors supply + approve)

> [BUTUH INPUT PENULIS — do not use unless original data and redistribution
> rights are confirmed.] The original experiment files (F1..F9, checksums
> …, license …, redistribution …) are archived at [ZENODO_VERSION_DOI]
> under [LICENSE].

## Fixed rules

- Never replace `[GITHUB_REPOSITORY_URL]`, `[ZENODO_VERSION_DOI]`, or
  `[RELEASE_VERSION]` with invented values.
- Never write "published" until publication actually happened (current
  status: local only).
- Never include the DOCX manuscript, secrets, or non-redistributable data
  in any archive.
