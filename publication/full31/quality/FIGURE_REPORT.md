# Figure audit report (Agent F)

Base: `2e440e43f89b61c112f088939f73440024283bbf` on `full31-quality-convergence-001`.

## Counts

- **KEEP**: 60
- **POLISH**: 62
- **REDESIGN**: 3
- **REMOVE**: 0
- **BLOCKED_EVIDENCE_REQUIRED**: 1
- **a11y failures**: 0
- **unresolved reader refs**: 0 (expect 0)
- **empty “see figure” refs**: 0

## High-priority REDESIGN

- `FIG-CH11-004` — Concentric stamp template does not match the claimed concept; needs concept-appropriate structure.
- `FIG-CH26-003` — Concentric stamp template does not match the claimed concept; needs concept-appropriate structure.
- `FIG-CH30-003` — Concentric stamp template does not match the claimed concept; needs concept-appropriate structure.

## BLOCKED

- `FIG-CE3-009` — BLOCKED_EVIDENCE_REQUIRED (unchanged)

## Phase 2 plan

1. Fix C1 mojibake / backtick operators in affected SVGs.
2. Add missing `data-figure-id` on CH02/CH04/CH05/CH09 assets.
3. Register CH23 figures in `figures/figure_registry.yaml` + accessibility paths.
4. Redesign high-priority stamp figures listed above (preserve IDs).
5. Do **not** redesign all scaffolds wholesale.


## Phase 2 completed

| Metric | Value |
|---|---|
| KEEP (Phase 1) | 60 |
| POLISH (Phase 1) | 62 |
| REDESIGN (Phase 1) | 3 |
| REMOVE (Phase 1) | 0 |
| BLOCKED_EVIDENCE_REQUIRED | 1 |
| Figures changed | 39 (incl. glyph/id polish + 3 redesigns + CH23 registration assets) |
| a11y failures | 0 |
| unresolved reader refs | 0 |

Redesigned (IDs preserved): `FIG-CH11-004`, `FIG-CH26-003`, `FIG-CH30-003`.

`FIG-CE3-009` remains **BLOCKED_EVIDENCE_REQUIRED**.
