# Gate 2 — Visual prototype

**Evaluation (closure pass):** `GATE_2_PASS` pending rendered-output inspection in this commit; if inspection fails, downgrade to `GATE_2_IN_PROGRESS`.

## Requirements

- exploded view
- end-to-end experience map
- component-card set (in chapter prose)
- sequence diagram
- software stack
- network/local path comparison
- latency budget
- Stability Contract visual
- accessibility metadata matching visible art
- figures embedded in rendered chapter

## Evidence

- `figures/**/fig-ch02-00*.svg` redesigned as real visual types (v0.2.0)
- `figures/accessibility/fig-ch02-00*.yaml`
- Chapter embeds via Quarto figure constructs in `book/chapters/ch02/chapter.md`
- Validators: `validate_figures.py`, `validate_accessibility.py`

## Notes

Human visual review remains required before publication. Automated checks verify structure/metadata match, not pedagogical excellence.
