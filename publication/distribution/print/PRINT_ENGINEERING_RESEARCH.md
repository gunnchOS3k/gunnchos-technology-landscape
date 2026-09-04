# Print Engineering Research — Adult FULL31

**Status:** `DRAFT_INTERNAL`  
**Retrieved:** 2026-09-03  
**Primary source:** Amazon KDP Help — Set Trim Size, Bleed, and Margins  
`https://kdp.amazon.com/help/topic/GVBQ3CMEQW3W2VL6`

## Non-claims

- Not printer-approved. Not PUBLICATION_READY.
- Page count of the adult book is **not frozen** here; gutter band depends on final PDF page count.
- List prices: **`REQUIRES_LIVE_PRICE_CALCULATOR`**.

## Trim candidates evaluated

| Trim | KDP class | Paperback B&W white page range | Hardcover B&W white | Recommendation |
| --- | --- | --- | --- | --- |
| 6×9 in | Regular (most common US) | 24–828 | 75–550 | **PRIMARY** for adult text+figures |
| 7×10 in | Large (>6.12" W or >9" H) | 24–828 | 75–550 | **ALT** if figures need more real estate |
| 8.5×11 in | Large | 24–590 | Not in hardcover table as 8.5×11 | Labs/handouts only — not primary trade book |

Notes from KDP: books >6.12" width or >9" height are **large trim** (different printing costs). Hardcover unsupported in JP. Case laminate only (no dust jacket).

## Ink / paper

| Option | Use case |
| --- | --- |
| Black ink + white paper | Default cost-conscious interior |
| Black ink + cream paper | Softer reading; page-count max slightly lower |
| Standard / Premium color + white | Only if color encoding is essential; cost ↑ — owner confirm |
| Groundwood | Available on some trims; aesthetic/cost tradeoff — owner confirm |

Figures already require non-color encodings per `publication/PRINT_REQUIREMENTS.md`; B&W-first remains compatible.

## Bleed

- Cover wraps: bleed **required**.
- Interior bleed: only if objects reach trim edge.
- Bleed amount: **0.125 in (3.2 mm)** top/bottom/outside.
- With-bleed page size example for 6×9: **6.125 × 9.25 in**.

## Margins (minimums)

| Page count | Inside (gutter) | Outside (no bleed) | Outside (with bleed) |
| --- | --- | --- | --- |
| 24–150 | 0.375" | ≥0.25" | ≥0.375" |
| 151–300 | 0.5" | ≥0.25" | ≥0.375" |
| 301–500 | 0.625" | ≥0.25" | ≥0.375" |
| 501–700 | 0.75" | ≥0.25" | ≥0.375" |
| 701–828 | 0.875" | ≥0.25" | ≥0.375" |

Adult FULL31 is likely mid/high page count → plan for **≥0.625" gutter** until final PDF counted.

## Spine

Spine width = f(page count, paper type). Use KDP **Cover Calculator** at upload time — do not invent spine inches here (`REQUIRES_LIVE_PRICE_CALCULATOR` / live cover calculator).

## Quarto profiles

Created overlay configs (do **not** rename/replace root `_quarto.yml`; review PDF path intact):

- `_quarto-print-6x9.yml`
- `_quarto-print-7x10.yml`
- `_quarto-print-85x11.yml`

Usage (experimental; owner/CI optional):

```bash
# Example — does not replace make full31-pdf review artifact naming
quarto render --profile print-6x9
```

Profiles set PDF geometry only. HTML/EPUB formats remain available via default project.

## Decision draft (not final)

1. **Primary print:** 6×9, B&W white, no interior bleed unless needed, own ISBN paperback.
2. **Optional hardcover:** 6×9 case laminate if page count ∈ [75,550].
3. **Figure-heavy contingency:** 7×10 large trim after cost calculator comparison.
