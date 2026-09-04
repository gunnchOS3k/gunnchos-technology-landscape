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

## Terminology (Agent J)

- Canonical registry: `book/terminology.yaml`
- Misconception matrix: `publication/full31/quality/MISCONCEPTION_MATRIX.md`
- Check: `make full31-terminology-check`
- Report: `publication/full31/quality/AGENT_J_TERMINOLOGY_REPORT.md`

## Agent I (front/back + nav + indexes)

- Audit: `FRONTMATTER_NAV_AUDIT.yaml`
- Report: `FRONTMATTER_NAV_REPORT.md`
- Errata stub: `ERRATA_WORKFLOW.md`

## Continuity / duplication (Agent D)

- Tool: `scripts/audit_full31_continuity.py` (audit aid; not auto-rewrite)
- Ledger: `CONTINUITY_LEDGER.yaml`
- Report: `CONTINUITY_REPORT.md`
- Identity matrix: `CHAPTER_IDENTITY_MATRIX.yaml` (+ `.md`)

## Publication / accessibility QA (Agent H)

- `PUBLICATION_QA.yaml` — machine-readable automated QA results
- `ACCESSIBILITY_QA.md` — human-readable summary (not a WCAG/EPUB certification)
- `HUMAN_PRINT_VISUAL_CHECKLIST.md` — stub for later human print review

```bash
make full31-publication-qa
```

Coordinates with `make validate` (source validators) but focuses on rendered
full31 HTML/EPUB/PDF artifacts plus manuscript semantics.

## Integrator (central registry + pre-review)

- Central registry: `QUALITY_ISSUES.yaml` (`make full31-quality-audit`)
- Continuity check: `make full31-continuity-check`
- Terminology check: `make full31-terminology-check`
- Publication QA: `make full31-publication-qa`
- Pre-review gates: `make full31-pre-review-check`
- Candidate package: `publication/review-candidates/FULL31-PRE-REVIEW-001/`

Pre-review requires open BLOCKER=0 and open MAJOR=0. Gate 3 remains unchanged.
