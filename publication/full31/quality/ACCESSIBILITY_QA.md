# Accessibility + publication QA (full31)

- **Generated:** 2026-09-04T02:11:29Z
- **Git SHA:** `a03d9c03dcc665b5f5ade53d0016afe9e15f1f20`
- **Agent:** agent-h-publication-qa

## Certification posture

This report records **automated checks only**.
It does **not** certify WCAG conformance, EPUB accessibility,
or human print quality.

## Toolchain

- Quarto: `/Users/gunnchos/Downloads/gunnchos-technology-landscape/tools/quarto/bin/quarto`
- LOCAL_RENDER_TOOLCHAIN_UNAVAILABLE: **False**

## Severity counts

- BLOCKER: 0
- MAJOR: 0
- MODERATE: 1
- MINOR: 0
- EDITORIAL: 0

## Artifacts

- **html:** `preview/full31/technology-landscape-full31-html`
- **epub:** `preview/full31/technology-landscape-full31-epub.epub`
- **pdf:** `preview/full31/technology-landscape-full31-pdf.pdf`
- **print_checklist:** `publication/full31/quality/HUMAN_PRINT_VISUAL_CHECKLIST.md`

## Findings

### PDF-FRONTMATTER-NUMBERING (MODERATE / pdf_structure)

- Location: `preview/full31/technology-landscape-full31-pdf.pdf`
- Status: `FIXED`
- Finding: PDF body LaTeX CHAPTER headers are within 1..31 (max=23); no Chapter 32+ backmatter inflation after \frontmatter/\mainmatter/\backmatter. Residual TOC cosmetics are human print review only.
- Evidence: body_headers_sample=[1, 2, 4, 7, 11, 23]; count=6; backmatter_numeric=[]

## Human follow-ups

- See `HUMAN_PRINT_VISUAL_CHECKLIST.md` (stub; not executed).
- Acronym expansion quality handed to terminology/glossary owners when registry is identity-only.
