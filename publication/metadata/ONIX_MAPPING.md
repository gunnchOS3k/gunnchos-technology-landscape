# ONIX Mapping Notes (inspired by EDItEUR ONIX)

**Status:** `DRAFT_INTERNAL`  
**Non-claim:** This is **not** EDItEUR-certified ONIX compliance and not a validated ONIX feed.

Reference overview (first-party standards body):  
https://www.editeur.org/83/Overview/ and https://www.editeur.org/8/ONIX/  
(HTTP 200 retrieved 2026-09-03).

## Purpose

Crosswalk internal `adult-book.yaml` fields to common ONIX 3.x *concepts* so a future
human/aggregator export is less ad hoc. Actual ONIX XML generation is out of scope here.

## Field crosswalk (conceptual)

| Internal field | ONIX-inspired concept | Notes |
| --- | --- | --- |
| `title.main` | Title Detail / Title Element | Required |
| `title.subtitle` | Subtitle | Optional |
| `contributors[].name` + `role` | Contributor | Map role codes later (`UNKNOWN_NEEDS_OWNER_REVIEW` for exact List 17 codes) |
| `language` | Language | ISO 639 |
| `identifiers.isbn13_*` | Product Identifier (ISBN-13) | One ISBN per product record |
| `products[].form` | Product Form | Separate Product records per format |
| `rights_statement` | Publishing detail / rights | ARR must not be mis-coded as open license |
| `subjects[]` | Subject | BISAC/Thema codes pending owner |
| `audience` | Audience | Adult; reading age optional |
| Free $0 price | Price / Price Type | Google ONIX free coding exists (List 57) — use only when exporting; do not invent feed |
| Accessibility | Product Form Feature / a11y metadata | Automated checks ≠ certification |

## Explicit gaps

- No ONIX XML artifact generated.
- No codelist version pin beyond “inspired by ONIX 3.x”.
- Aggregator-specific required composites: `UNKNOWN_NEEDS_OWNER_REVIEW`.
