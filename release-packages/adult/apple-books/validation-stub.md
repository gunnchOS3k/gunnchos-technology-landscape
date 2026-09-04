# Validation notes — `apple-books`

Automated (repo-side) checks:

1. `make adult-release-package-check` / `make adult-artifact-package-check`
2. `make distribution-requirements-check`
3. `make full31-epubcheck` (when EPUB present)
4. `make full31-pre-review-check` — freeze candidacy unchanged

Not included: live retailer ingestion, WCAG certification, Kindle Previewer automation,
human accessibility audit, ISBN purchase.
