# Agent J — Terminology / glossary report

**Branch work:** `agent/quality-j-terminology` → merge into `cursor/full31-quality-convergence-001`  
**Base tip:** `2e440e43f89b61c112f088939f73440024283bbf`

## Deliverables

| Artifact | Path |
|---|---|
| Canonical terminology registry | `book/terminology.yaml` |
| Misconception matrix | `publication/full31/quality/MISCONCEPTION_MATRIX.md` |
| Alias strengthening | `glossary/aliases.yaml` |
| Acronym first-use policy | `glossary/acronym_registry.yaml` |
| Check target | `make full31-terminology-check` → `scripts/validate_terminology.py` |
| Glossary relation strengthening | scoped `not_the_same_as` / `reinforced_in` in `glossary/glossary.yaml` |

## Counts

- Terminology terms: **48** (45 high-risk + 3 supporting: portfolio-proof, measurement, identity)
- High-risk coverage: **45/45**
- Alias keys: **122**
- Alias collisions: **0**
- Glossary-linked terms: **29**
- Terminology-only (not yet glossary-promoted): **19**
- Living glossary entries (unchanged count): **91**
- Misconception matrix rows: **35**

## Constraints honored

- No wholesale chapter rewrites
- No Gate 3 / `publication/gates/gate-3/` changes
- Registry prevents contradiction; does not force identical sentences book-wide
- Familiar acronyms (CPU/GPU/RAM/API/AI) marked for sparse re-expansion

## Optional follow-on

- Promote terminology-only high-risk terms into `glossary/glossary.yaml` when chapter agents need reader-facing glossary links
- Agents A–C may cite matrix rows when filing `TERMINOLOGY` quality issues
