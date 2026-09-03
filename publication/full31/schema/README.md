# Full31 chapter-production schema contract

**schema_version:** `1.0.0`  
**Applies to:** `publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml` and `publication/full31/chapters/chNN/` packets  
**Does not apply to:** `publication/gates/gate-3/` (Gate 3 / CH02-REVIEW-R1 untouched)

## Purpose

Separate **packet completeness** (files exist and are semantically valid) from **chapter maturity**
(`current_state`). Reuse Concept Edition preproduction enums/fields wherever semantics match.

## Files in this directory

| File | Covers |
|---|---|
| `chapter_registry.schema.yaml` | `CHAPTER_PRODUCTION_REGISTRY.yaml` |
| `chapter_packet.schema.yaml` | Required packet file set + brief/markdown contracts |
| `full31_claim_plan.schema.yaml` | `CLAIM_PLAN.yaml` (aligned with CE claim schema) |
| `full31_concept_graph.schema.yaml` | `CONCEPT_GRAPH.yaml` |
| `full31_figure_plan.schema.yaml` | `FIGURE_PLAN.yaml` |
| `full31_glossary.schema.yaml` | `GLOSSARY_CANDIDATES.yaml` |
| `full31_dependency_map.schema.yaml` | `DEPENDENCY_MAP.yaml` |

## State model (integrator)

### `packet_state` (file/semantic presence only)

```text
PACKET_MISSING | PACKET_STARTED | PACKET_COMPLETE
```

### `current_state` (honest maturity)

```text
If canonical prose is under real human validation:
    HUMAN_VALIDATION_PENDING
Else if ALL required preproduction substates are PREPRODUCTION_COMPLETE:
    PREPRODUCTION_COMPLETE
Else if packet exists and ≥1 substantive preproduction dimension started:
    PREPRODUCTION_STARTED
Else:
    SCAFFOLD
```

Required preproduction substates:

- `concept_preproduction_state`
- `source_state`
- `claim_state`
- `figure_state`
- `lab_state`
- `glossary_state`
- `waike_state`

## Gate posture

`GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` — unchanged by this contract.
