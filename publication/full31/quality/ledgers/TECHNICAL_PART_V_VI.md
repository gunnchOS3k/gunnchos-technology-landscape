# Technical review — Parts V–VI (CH21–CH31)

**Agent:** `agent/quality-c-part56`  
**Accepted main:** `76bee2e67c35ff445f46c83af30809e5b307f06e` (PR #5)  
**Preferred base** `cursor/full31-quality-convergence-001`: **present** @ `2e440e4`  
**Ledger:** `TECHNICAL_PART_V_VI.yaml`  
**Gate 3:** untouched (`git diff` empty vs accepted main)

## Severity counts

| Severity | Before | After (open) |
|---|---:|---:|
| BLOCKER | 0 | 0 |
| MAJOR | 4 | 0 |
| MODERATE | 4 | 0 |
| MINOR | 3 | 3 deferred |
| EDITORIAL | 2 | 2 confirm-and-preserve |

Open after scoped fixes: **BLOCKER 0 · MAJOR 0**. Remaining open items are deferred MINOR/EDITORIAL (draft-blocked meta, SOURCE_NEEDED pin, preserve notes).

## Fixes applied

1. **CH26** — Explicit **version control ≠ backup** in opening + component card + glossary.
2. **CH26** — Relabeled FIG-CH26-003 SVG/a11y to secrets hygiene (was employment diagram).
3. **CH21** — Relabeled FIG-CH21-003 SVG/a11y to fluency/correctness/evaluation evidence.
4. **CH27** — Retensed stale “Chapter 26 (when drafted)” to completed history.
5. **CH21** — Explicit ML ⊃ generative distinction.
6. **CH23** — Named CIA (confidentiality/integrity/availability) beside encryption limits.
7. **CH24** — Explicit **safety ≠ censorship** rule + card/glossary.
8. **CH29** — Aligned FIG-CH29-003 prose to live one-pager fields asset; claim-boundary badges stay in written packet.

## Deferred

- Bulk `draft-blocked` figure-status refresh (Agent F)
- CH28 reproducibility guide SOURCE_NEEDED (Evidence)
- Confirm-and-preserve AuthN / equity / EMIT honesty (no change)

## Gate posture (unchanged)

```text
GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING
0 fabricated reader evidence
no Gate 3 PASS claim
```
