# Accessibility + publication QA (full31)

- **Generated:** 2026-09-04T00:19:30Z
- **Git SHA:** `51e36228a7152e3423bc867a74ca0f9825aa023b`
- **Agent:** agent-h-publication-qa

## Certification posture

This report records **automated checks only**.
It does **not** certify WCAG conformance, EPUB accessibility,
or human print quality.

## Toolchain

- Quarto: `/Users/gunnchos/Downloads/gunnchos-technology-landscape/.worktrees/agent-h-publication-qa-001/tools/quarto/bin/quarto`
- LOCAL_RENDER_TOOLCHAIN_UNAVAILABLE: **False**

## Severity counts

- BLOCKER: 0
- MAJOR: 1
- MODERATE: 1
- MINOR: 0
- EDITORIAL: 0

## Artifacts

- **html:** `preview/full31/technology-landscape-full31-html`
- **epub:** `preview/full31/technology-landscape-full31-epub.epub`
- **pdf:** `preview/full31/technology-landscape-full31-pdf.pdf`
- **print_checklist:** `publication/full31/quality/HUMAN_PRINT_VISUAL_CHECKLIST.md`

## Findings

### A11Y-ACRO-IDENTITY (MODERATE / acronyms)

- Location: `glossary/acronym_registry.yaml`
- Status: `HANDOFF_AGENT_J`
- Finding: Acronym registry entries expand to themselves (4): first-use expansion not machine-checkable.
- Evidence: API, CPU, GPU, RAM

### PDF-CHAPTER-COUNTER (MAJOR / pdf_structure)

- Location: `preview/full31/technology-landscape-full31-pdf.pdf`
- Status: `NEEDS_HUMAN`
- Finding: PDF text shows chapter numbers up to 441 (666 pages). Expected ~31 body chapters; likely LaTeX chapter-counter inflation — needs human print QA.

## Human follow-ups

- See `HUMAN_PRINT_VISUAL_CHECKLIST.md` (stub; not executed).
- Acronym expansion quality handed to terminology/glossary owners when registry is identity-only.
