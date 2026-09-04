# Validation stub — `amazon-hardcover`

Automated (repo-side) checks that may be wired later — **do not** treat as retailer approval:

1. `make distribution-requirements-check` — required distribution docs present
2. `make adult-release-package-check` — package layout + checksums
3. `make full31-epubcheck` — W3C EPUBCheck on rendered EPUB (when present)
4. `make full31-pre-review-check` — freeze candidacy labels (unchanged by this track)

Not included: live retailer ingestion, WCAG certification, human accessibility audit.
