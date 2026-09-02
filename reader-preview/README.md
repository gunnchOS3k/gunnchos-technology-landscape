# Reader preview package

Assembles a no-clone, no-Quarto package for Gate 3 human reviews.

## Contents

- Chapter 2 HTML / PDF / EPUB
- Seven CH02 figures
- LAB-TAP-001 browser + fixture routes
- Landing page + instructions + feedback forms

## Build

```bash
make reader-preview
```

This runs chapter renders (when Quarto/TeX available), copies assets into `docs/`,
and updates SHA-256 hashes in `publication/gates/gate-3/REVIEW_SNAPSHOT.yaml`.

## Delivery

| Channel | Role |
|---|---|
| `docs/` + GitHub Pages | HTML + lab + figures + forms |
| Actions artifact `reader-preview-bundle` | Full bundle including PDF/EPUB |
| Forms in `reader-preview/forms/` | Source copies mirrored into `docs/forms/` |

Readers must cite snapshot **CH02-REVIEW-R1**.
