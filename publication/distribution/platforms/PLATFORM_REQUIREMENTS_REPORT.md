# Platform Requirements Report — Adult Distribution

**Status:** `DRAFT_INTERNAL`  
**Ceiling claimed:** none beyond research / package prep  
**Non-claims:** not retailer-approved · not WCAG certified · not Gate 3 PASS · not `PUBLICATION_READY`  
**Integration base:** `ce9cc419841fa0588e30d8d917b048c72f8cc2c0`  
**Retrieved:** 2026-09-03

## Scope

Research-only requirements for wide adult distribution of *The Technology Landscape*
across Amazon KDP (Kindle / paperback / hardcover), Apple Books, Google Play Books,
Kobo Writing Life, direct web, and a library/distributor pathway.

No retailer accounts were created. No ISBNs purchased. No uploads performed.

## Platform matrix (honest)

| Platform | Primary asset | Free $0 list? | ISBN | Key gate |
| --- | --- | --- | --- | --- |
| KDP Kindle | EPUB / DOCX / KPF | No permanent $0 (Select free promo conflicts with wide) | Optional; free KDP ISBN Amazon-tied | Min price tiers; avoid Select under wide-access |
| KDP Paperback | PDF interior + PDF wrap | Cost floor | Free or own | Trim/bleed/margins; live cost calculator |
| KDP Hardcover | PDF interior + case-laminate wrap | Cost floor | Free or own | Limited trims; unsupported JP |
| Apple Books | EPUB + cover | Yes (Free Books Agreement) | Optional UUID/ISBN | EPUBCheck pass |
| Google Play Books | EPUB and/or PDF | Yes (price 0) | Recommended identifiers | EpubCheck; preview settings |
| Kobo Writing Life | EPUB (or convertible) | Yes (price 0) | Optional; partners may need | Pre-order cannot be free |
| Direct web | HTML/PDF/EPUB | Yes (publisher-controlled) | N/A | ARR ≠ free license |
| Library pathway | EPUB/PDF via distributor | Model TBD | Usually required | OverDrive via KWL / IngramSpark TBD |

## Source counts

- **Unique first-party / project source URLs registered:** 18 (see YAML `source_count_summary`)
- **Platforms with ≥1 retrieved official help URL:** 8/8
- Gaps marked `UNKNOWN_NEEDS_OWNER_REVIEW` or `REQUIRES_LIVE_PRICE_CALCULATOR` where live calculators / blocked pages apply

## Print engineering (summary)

Evaluated KDP trim candidates **6×9** (regular, primary), **7×10** (large, figure-heavy alt),
and **8.5×11** (handout/large alt only). Bleed = 0.125". Gutter scales with page count
(0.375"–0.875"). Exact print list prices: **`REQUIRES_LIVE_PRICE_CALCULATOR`**.

Quarto print overlay profiles: `_quarto-print-6x9.yml`, `_quarto-print-7x10.yml`,
`_quarto-print-85x11.yml` (do not replace review PDF path).

## Owner actions still required

1. Imprint legal name + Bowker (or national agency) ISBN purchase — placeholders only.
2. Live KDP printing-cost / royalty calculator runs for chosen trim + ink + page count.
3. Confirm Amazon price-match pathway for free-elsewhere strategy (no Select).
4. Library commercial terms (OverDrive via KWL; IngramSpark) — account decisions deferred.
5. Direct-web hosting + reader-facing rights wording (ARR vs free access).
