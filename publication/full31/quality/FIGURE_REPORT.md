# Figure audit report (normalized)

## AUDIT_STATE_BEFORE (Phase 1)

| State | Count |
|---|---:|
| KEEP | 60 |
| POLISH | 62 |
| REDESIGN | 3 |
| REMOVE | 0 |
| BLOCKED_EVIDENCE_REQUIRED | 1 (`FIG-CE3-009`) |

Phase-1 REDESIGN list (then unresolved): `FIG-CH11-004`, `FIG-CH26-003`, `FIG-CH30-003`.

## Changes made (Phase 2)

- Redesigned (IDs preserved): `FIG-CH11-004`, `FIG-CH26-003`, `FIG-CH30-003`
- Polished / repaired: glyph/mojibake, operators, `data-figure-id`, CH23 registration, plus later integrity fixes (e.g. FIG-CH12-004 truth-class normalization)
- Figures touched in Phase 2 wave: **39** (includes polish + 3 redesigns + registration assets)

## FINAL_STATE_AFTER

| State | Count | Notes |
|---|---:|---|
| KEEP | 60 | unchanged keep-set from Phase 1 |
| REDESIGN remaining | **0** | all 3 Phase-1 REDESIGN items completed |
| POLISH actually applied | subset of 62 | glyph/id/operator/truth-class repairs landed |
| POLISH remaining human visual-review candidates | remainder of Phase-1 POLISH | **not** open correctness defects; deferred visual/print judgment |
| REMOVE | 0 | |
| BLOCKED_EVIDENCE_REQUIRED | **1** | `FIG-CE3-009` remains blocked |

### Accessibility / refs

- a11y failures: **0**
- unresolved reader refs: **0**

Do not treat Phase-1 POLISH/REDESIGN counts as unresolved defects after Phase 2.
