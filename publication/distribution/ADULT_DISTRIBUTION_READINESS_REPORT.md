# Adult Distribution Readiness Report

**Status vocabulary (package):** `SCAFFOLD_ONLY` | `ARTIFACTS_BUILT` | `VALIDATED_LOCALLY` | `BLOCKED_OWNER_COVER` | `BLOCKED_OWNER_METADATA` | `BLOCKED_OWNER_ISBN` | `BLOCKED_HUMAN_REVIEW` | `READY_FOR_OWNER_UPLOAD`  
**Aggregate state:** `ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE`  
**Not:** `PUBLICATION_READY` / `READY_FOR_OWNER_UPLOAD` / Gate 3 PASS / retailer-approved  
**HUMAN_VALIDATED:** 0/31 · **PUBLICATION_READY:** 0/31  
**Date:** 2026-09-03  
**Base tip:** `cursor/publication-family-parallel-production-001` @ reviewed `c0ff99b`+

## Deliverable inventory

| # | Deliverable | Path | State |
| --- | --- | --- | --- |
| 1 | Platform requirements | `publication/distribution/platforms/PLATFORM_REQUIREMENTS.yaml` + `_REPORT.md` | Draft with 23-register sources |
| 2 | Free access policy | `publication/distribution/FREE_ACCESS_POLICY.md` | Draft |
| 3 | ISBN/imprint | `publication/distribution/identifiers/` | Placeholders only |
| 4 | Metadata schema + adult instance | `publication/metadata/` | Draft |
| 5 | ONIX mapping notes | `publication/metadata/ONIX_MAPPING.md` | Inspired; not certified |
| 6 | Print engineering + Quarto profiles | `publication/distribution/print/` + `_quarto-print-*.yml` | Rendered |
| 7 | Print profile results | `PRINT_PROFILE_RESULTS.yaml` + `.md` | Page counts + eligibility |
| 8 | Cover requirements + geometry tool | `publication/distribution/covers/` + `scripts/cover_geometry.py` | Draft + proof SVG; not final art |
| 9 | Release packages (8) | `release-packages/adult/*/` | Real EPUB/PDF where automatable; owner blocks remain |
| 10 | Library options | `publication/distribution/libraries/LIBRARY_DISTRIBUTION_OPTIONS.md` | Draft |
| 11 | Source register | `publication/distribution/PUBLISHING_SOURCE_REGISTER.yaml` | 23 sources |
| 12 | Aggregate state | `ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE.md` | Declared |
| 13 | This report | `ADULT_DISTRIBUTION_READINESS_REPORT.md` | — |

## Per-channel package readiness

| Channel | Readiness | Real artifacts | Remaining stubs / blocks |
| --- | --- | --- | --- |
| amazon-kindle | `BLOCKED_OWNER_COVER` | `manuscript.epub` | `cover.jpg.STUB`; `KINDLE_PREVIEWER_HUMAN_OR_EXTERNAL_PENDING` |
| amazon-paperback | `BLOCKED_OWNER_COVER` | `interior.pdf` (`PRINT_INTERIOR_PDF` 6×9) | `cover-wrap.pdf.STUB` + `LIVE_COVER_CALCULATOR_REQUIRED` |
| amazon-hardcover | `BLOCKED_OWNER_COVER` | `interior.pdf` (`PRINT_INTERIOR_PDF` 7×10; 6×9 over hardcover max) | `cover-wrap.pdf.STUB` + live calculator |
| apple-books | `BLOCKED_OWNER_COVER` | `book.epub` | `cover.jpg.STUB` |
| google-play-books | `BLOCKED_OWNER_COVER` | `book.epub` | `cover.jpg.STUB` |
| kobo | `BLOCKED_OWNER_COVER` | `book.epub` | `cover.jpg.STUB` |
| direct-free | `BLOCKED_OWNER_METADATA` | `book.epub` + `book.pdf` (`DIGITAL_ACCESS_PDF`) | Hosting/metadata owner decisions |
| libraries | `BLOCKED_OWNER_ISBN` | `book.epub` + `metadata.yaml` | ISBN purchase pending |

## Print profile results (summary)

| Profile | Pages | Measured | Paperback | Hardcover |
| --- | --- | --- | --- | --- |
| print-6x9 | 628 | 6.0×9.0 in | YES (24–828) | NO (75–550) |
| print-7x10 | 524 | 7.0×10.0 in | YES (24–828) | YES (75–550) |
| print-85x11 | 436 | 8.5×11.0 in | YES (24–590) | NO (not in hardcover table) |

Digital access reference PDF (`make full31-pdf`): **618** pages @ 8.5×11 — role `DIGITAL_ACCESS_PDF`, distinct from print interiors.

Spine/cover wrap: **`LIVE_COVER_CALCULATOR_REQUIRED`** (no invented spine).

## Platform source counts

- **PUBLISHING_SOURCE_REGISTER entries:** 23
- **Platforms covered in PLATFORM_REQUIREMENTS:** 8

## Remaining owner decisions

1. Legal imprint name + ISBN agency purchase (3 format slots).
2. BISAC/Thema subject codes.
3. Live KDP print cost + cover calculator for chosen trim/ink/page count.
4. Confirm Amazon price-match behavior for free-elsewhere strategy.
5. OverDrive (KWL) and/or IngramSpark commercial terms.
6. Direct hosting venue + reader-facing ARR free-access wording.
7. Whether hardcover ships in v1 (6×9 over limit → 7×10 candidate packaged).
8. Final cover art (technical proof is not marketing art).
9. Human Gate 3 evidence remains pending and blocks publication claims.
10. Kindle Previewer run (`KINDLE_PREVIEWER_HUMAN_OR_EXTERNAL_PENDING`).

## Integrator refresh (Track 1)

- Stubs replaced with real FULL31 EPUB/PDF / print interiors where automation allows.
- `adult-artifact-package-check` hard-fails stubs at `ARTIFACTS_BUILT+`; forbids `READY_FOR_OWNER_UPLOAD` while owner blocks remain.
- Ceiling is **`ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE`**, not `PUBLICATION_READY`.
- `HUMAN_VALIDATED 0/31` · `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`.
- No retailer submission; ISBN placeholders unchanged; secrets scan required in CI.
