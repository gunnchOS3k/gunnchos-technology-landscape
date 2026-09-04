# Technical review — Parts I–II (CH01–CH10)

**Agent:** `agent/quality-a-part12`  
**Accepted base:** `76bee2e67c35ff445f46c83af30809e5b307f06e` (PR #5 / main)  
**Preferred base** `cursor/full31-quality-convergence-001`: **absent** → fallback used  
**Ledger:** `TECHNICAL_PART_I_II.yaml`  
**Gate 3:** untouched (`publication/gates/gate-3/`)  
**CH02:** no broad rewrite (spot-check clean)

## Severity counts

| Severity | Before | After (open/deferred) |
|---|---:|---:|
| BLOCKER | 0 | 0 |
| MAJOR | 4 | 0 |
| MODERATE | 6 | 1 (deferred evidence) |
| MINOR | 4 | 2 (deferred) |
| EDITORIAL | 2 | 2 (confirm-and-preserve) |

Fixed this pass: TECH-P12-001…009, TECH-P12-012.

## Key fixes

- **CH05:** Explicit voltage / current / power separation (prose, card, glossary).
- **CH06:** Cores = execution engines (not “hardware contexts”); process vs thread card restored.
- **CH03:** Route C blocked-plate sentence repaired; responsiveness named; ISO 25010 retargeted.
- **CH08:** CLM-CH08-001 pointer replaces “see blockers”; compositor ≠ GPU in card.
- **CH01 / CH07:** Bottleneck foreshadow; registers wording aligned with RAM≠storage.

## Deferred

- TECH-P12-010 — display-deadline citation pin (CLM-CH08-001)
- TECH-P12-011 — CH09 electrochemistry / mechanical textbook pins
- TECH-P12-013 — CH05 SOURCE_NEEDS metadata sync
- TECH-P12-014 — CH02 (no change needed)
- TECH-P12-015/016 — CH04/CH10 positive confirmations
