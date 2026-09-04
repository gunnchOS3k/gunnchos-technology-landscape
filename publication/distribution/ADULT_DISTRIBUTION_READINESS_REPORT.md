# Adult Distribution Readiness Report

**Status vocabulary:** `READY_FOR_TRACK_REVIEW` (track-local)  
**Ceiling state:** `ADULT_SUBMISSION_PACKAGE_PREPARED`  
**Not:** `PUBLICATION_READY` / Gate 3 PASS / retailer-approved  
**Date:** 2026-09-03  
**Base:** `ce9cc419841fa0588e30d8d917b048c72f8cc2c0`

## Deliverable inventory

| # | Deliverable | Path | State |
| --- | --- | --- | --- |
| 1 | Platform requirements | `publication/distribution/platforms/PLATFORM_REQUIREMENTS.yaml` + `_REPORT.md` | Draft with 23-register sources |
| 2 | Free access policy | `publication/distribution/FREE_ACCESS_POLICY.md` | Draft |
| 3 | ISBN/imprint | `publication/distribution/identifiers/` | Placeholders only |
| 4 | Metadata schema + adult instance | `publication/metadata/` | Draft |
| 5 | ONIX mapping notes | `publication/metadata/ONIX_MAPPING.md` | Inspired; not certified |
| 6 | Print engineering + Quarto profiles | `publication/distribution/print/` + `_quarto-print-*.yml` | Profiles created |
| 7 | Cover requirements + geometry tool | `publication/distribution/covers/` + `scripts/cover_geometry.py` | Draft + proof SVG |
| 8 | Release packages (8) | `release-packages/adult/*/` | Stubs + checklists |
| 9 | Library options | `publication/distribution/libraries/LIBRARY_DISTRIBUTION_OPTIONS.md` | Draft |
| 10 | Source register | `publication/distribution/PUBLISHING_SOURCE_REGISTER.yaml` | 23 sources |
| 11 | This report | `publication/distribution/ADULT_DISTRIBUTION_READINESS_REPORT.md` | — |
| 12 | Ceiling state | `publication/distribution/ADULT_SUBMISSION_PACKAGE_PREPARED.md` | Declared |

## Platform source counts

- **PUBLISHING_SOURCE_REGISTER entries:** 23
- **Platforms covered in PLATFORM_REQUIREMENTS:** 8
- First-party retailer/help URLs dominate; project rights/toolchain/freeze included

## Print profile results

| Profile | Created | Notes |
| --- | --- | --- |
| `_quarto-print-6x9.yml` | Yes | Primary candidate |
| `_quarto-print-7x10.yml` | Yes | Large / figure-heavy alt |
| `_quarto-print-85x11.yml` | Yes | Handout alt only |
| Live cost calculator | Not run | `REQUIRES_LIVE_PRICE_CALCULATOR` |
| Review PDF path | Intact | root `_quarto.yml` / `make full31-pdf` unchanged |

## Package paths

```
release-packages/adult/amazon-kindle/
release-packages/adult/amazon-paperback/
release-packages/adult/amazon-hardcover/
release-packages/adult/apple-books/
release-packages/adult/google-play-books/
release-packages/adult/kobo/
release-packages/adult/direct-free/
release-packages/adult/libraries/
```

## Remaining owner decisions

1. Legal imprint name + ISBN agency purchase (3 format slots).
2. BISAC/Thema subject codes.
3. Live KDP print cost + cover calculator for chosen trim/ink/page count.
4. Confirm Amazon price-match behavior for free-elsewhere strategy.
5. OverDrive (KWL) and/or IngramSpark commercial terms.
6. Direct hosting venue + reader-facing ARR free-access wording.
7. Whether hardcover ships in v1.
8. Final cover art (technical proof is not marketing art).
9. Actual render + copy of FULL31 EPUB/PDF into package `artifacts/` before any upload.
10. Human Gate 3 evidence remains pending and blocks publication claims.

## Integrator refresh (2026-09-03)

- Shared family registries landed under `publication/family/`.
- Ceiling remains `ADULT_SUBMISSION_PACKAGE_PREPARED` — **not** `PUBLICATION_READY`.
- `HUMAN_VALIDATED 0/31` · `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`.
- No retailer submission; ISBN placeholders unchanged; secrets scan required in CI.
