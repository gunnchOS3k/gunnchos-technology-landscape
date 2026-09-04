# Accessibility + publication QA (full31)

- **Generated:** 2026-09-04T00:42:01Z
- **Git SHA:** `6da419826c70c4f19657b68bf6ffe55dd7675029`
- **Agent:** agent-h-publication-qa

## Certification posture

This report records **automated checks only**.
It does **not** certify WCAG conformance, EPUB accessibility,
or human print quality.

## Toolchain

- Quarto: `/Users/gunnchos/Downloads/gunnchos-technology-landscape/.worktrees/full31-quality-convergence-001/tools/quarto/bin/quarto`
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
- Status: `NEEDS_HUMAN`
- Finding: Front/back matter may still appear as arabic-numbered chapters in the PDF TOC despite number: false; body LaTeX headers max=40. Human print QA should confirm unnumbered frontmatter styling.

## Human follow-ups

- See `HUMAN_PRINT_VISUAL_CHECKLIST.md` (stub; not executed).
- Acronym expansion quality handed to terminology/glossary owners when registry is identity-only.
