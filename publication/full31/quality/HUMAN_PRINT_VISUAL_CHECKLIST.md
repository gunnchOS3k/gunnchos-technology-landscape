# Human visual / print checklist (stub)

**Status:** NOT RUN — human review required later.  
**Do not treat this file as print-quality approval.**

Use after automated `make full31-publication-qa` is green or findings are triaged.

## Setup

- [ ] Print or soft-proof the current full31 PDF on target trim/paper
- [ ] Compare color and grayscale proofs for non-color encodings
- [ ] Confirm correct PDF build SHA recorded in `PUBLICATION_QA.yaml`

## First-pass visual

- [ ] Title page / status banner readable and truthful
- [ ] TOC page numbers match chapter openings
- [ ] No obviously blank spread where content was expected
- [ ] Running heads / folios present and not colliding with content
- [ ] Chapter-opening orphans/widows acceptable

## Figures

- [ ] Every figure present; no missing-image boxes
- [ ] Captions and figure IDs present and match narrative references
- [ ] Labels legible at print size (no tiny unreadable text)
- [ ] No clipped SVG/path edges at trim
- [ ] Color is not the sole encoding (labels, line style, or pattern)

## Tables / code

- [ ] Wide tables do not spill past margins
- [ ] Code blocks remain readable (wrapping vs overflow intentional)

## Accessibility spot-check (human)

- [ ] Sample screen-reader pass on HTML edition (2–3 chapters)
- [ ] Keyboard-only pass on lab browser routes
- [ ] Acronym first-use expansions sound natural in prose

## Sign-off

- Reviewer:
- Date:
- Build SHA:
- Result: PASS / FAIL / DEFER (never auto-claimed by CI)
