# Adult Cover Requirements

**Status:** `DRAFT_INTERNAL`  
**Retrieved:** 2026-09-03  
**Non-claim:** Neutral technical proof ≠ final marketing cover; not retailer-approved.

## Ebook front cover

| Platform | Spec (official) | Source |
| --- | --- | --- |
| KDP Kindle | TIFF/JPEG; ideal 2560×1600; min 1000×625; RGB; ≥300 PPI; ~1.6:1 ratio | https://kdp.amazon.com/help/topic/G200645690 |
| Apple Books | PNG/JPEG; RGB; ≥1400 px shortest side | https://itunespartner.apple.com/books/support/9-prepare-book |
| Google Play | jpeg/png/tiff/pdf; ≥640 px; ≤7200 edge | https://support.google.com/books/partner/answer/3424254 |
| Kobo | Cover upload required in KWL flow | KWL new eBook help |

**Working master recommendation:** RGB JPEG **1600×2560** (meets KDP ideal ratio and Apple ≥1400).

## Print wrap (paperback / hardcover)

- Single continuous PDF: back + spine + front (+ bleed).
- Bleed required on covers (KDP).
- Spine width from live Cover Calculator after page count known.
- Hardcover = **case laminate** (no dust jacket) — https://kdp.amazon.com/help/topic/GKYZRXFBZH2LDXAK

## Content constraints (project)

- Title + subtitle readable at thumbnail.
- No fabricated awards, reviews, or “Gate 3 PASS” badges.
- Accessibility: avoid conveying meaning by color alone on cover text.

## Tooling

- `scripts/cover_geometry.py` — compute ebook canvas and print wrap placeholder dimensions.
- Optional neutral SVG proof: `publication/distribution/covers/proofs/adult-cover-technical-proof.svg`
