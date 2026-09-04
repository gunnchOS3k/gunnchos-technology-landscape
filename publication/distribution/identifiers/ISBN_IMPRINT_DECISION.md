# ISBN + Imprint Decision — Adult Edition

**Status:** `DRAFT_INTERNAL` — placeholders only; **no fabricated ISBNs**  
**Date:** 2026-09-03  
**Owner decision required before any retailer upload**

## Imprint

| Field | Value |
| --- | --- |
| Working imprint name | `UNKNOWN_NEEDS_OWNER_REVIEW` (candidate: gunnchOS / author personal imprint) |
| Legal publisher entity | `UNKNOWN_NEEDS_OWNER_REVIEW` |
| Country of publication | `UNKNOWN_NEEDS_OWNER_REVIEW` (drives ISBN agency: Bowker US vs national agency) |
| Imprint registered with ISBN agency | No — not purchased |

US agency reference (existence only; no purchase): https://www.myidentifiers.com/  
(HTTP retrieval of agency site returned Cloudflare 403 on 2026-09-03 from automation; owner should use official Bowker MyIdentifiers in browser.)

## ISBN allocation plan (placeholders)

One ISBN per **product format** (ebook vs paperback vs hardcover). Do not reuse across formats.

| Slot ID | Format | ISBN-13 | Assignment status |
| --- | --- | --- | --- |
| `ISBN-ADULT-EBOOK` | Ebook (EPUB family) | `PENDING_OWNER_PURCHASE` | placeholder |
| `ISBN-ADULT-PAPERBACK` | Paperback POD | `PENDING_OWNER_PURCHASE` | placeholder |
| `ISBN-ADULT-HARDCOVER` | Hardcover POD | `PENDING_OWNER_PURCHASE` | placeholder |

Platform-assigned free identifiers (KDP free ISBN, Kobo auto-ID, Google GGKEY) may be used
**only** if owner accepts Amazon/Kobo channel imprint limits. For wide multi-retailer branding,
**own ISBNs are recommended**.

## Non-actions this track

- No ISBN purchased
- No barcode generated
- No retailer metadata submitted

## Related stubs

- `publication/ISBN_CHECKLIST.md` (foundation checklist; still open)
- Placeholder files in this directory
