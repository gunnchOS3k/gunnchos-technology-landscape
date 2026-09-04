# Full31 quality convergence

Working area for manuscript quality convergence on branch
`cursor/full31-quality-convergence-001`.

## Constraints (unchanged)

- Gate posture remains `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`.
- Do **not** fabricate reader evidence.
- Do **not** alter `CH02-REVIEW-R1` or `publication/gates/gate-3/`.
- Do **not** claim Gate 3 PASS or publication-ready.

## Base

Agents A–J may base work from the tip of this branch after bootstrap.

## Publication / accessibility QA (Agent H)

- `PUBLICATION_QA.yaml` — machine-readable automated QA results
- `ACCESSIBILITY_QA.md` — human-readable summary (not a WCAG/EPUB certification)
- `HUMAN_PRINT_VISUAL_CHECKLIST.md` — stub for later human print review

```bash
make full31-publication-qa
```

Coordinates with `make validate` (source validators) but focuses on rendered
full31 HTML/EPUB/PDF artifacts plus manuscript semantics.
