# Concept Edition preproduction schema contract

**schema_version:** `1.0.0`  
**Applies to:** `publication/preproduction/ce-01|ce-03|ce-04|ce-05|ce-06/` structured YAML  
**Does not apply to:** `publication/gates/gate-3/` (Gate 3 / CH02-REVIEW-R1 untouched)

## Purpose

One constrained vocabulary for claims, concepts, figures, learning objectives,
career maps, and candidate indexes so drafting/promotion/tooling can rely on
stable field names and enums.

Agent-specific synonyms (`nodes`, `verified`/`planned`, `truth_class`, …) are
**not** accepted by validators after this contract.

## Files in this directory

| File | Covers |
|---|---|
| `concept_graph.schema.yaml` | `CONCEPT_GRAPH.yaml` |
| `claim_plan.schema.yaml` | `CLAIM_PLAN.yaml` |
| `figure_plan.schema.yaml` | `FIGURE_PLAN.yaml` |
| `learning_objectives.schema.yaml` | `LEARNING_OBJECTIVES.yaml` |
| `career_map.schema.yaml` | `CAREER_MAP.yaml` |
| `candidate_indexes.schema.yaml` | `CANDIDATE_*.yaml` |

## Alias migrations (this pass)

| Drift | Canonical |
|---|---|
| `nodes:` | `concepts:` |
| `plain_language` / `name` / `id` | `plain_language_definition` / `canonical_term` / `concept_id` |
| `status: verified` / `planned` | Wave-13 evidence statuses (mapped by meaning) |
| `truth_class` / `conceptual_vs_measured` | `truth_classification` |
| `project_specific_conceptual` / `conceptual_project_qualified` / `measured_later_fixture` | base enum + optional `qualification` |
| `claim_text` / `claim_id` | `text` / `provisional_id` |
| `general technical` / `standards-based` / … | snake_case claim_class enum |
| `figure_id` / `type` / `data_evidence_source` / `geometry_layout` | `provisional_id` / `figure_type` / `data_or_evidence_source` / `expected_geometry` |
| `roles:` (career) | `careers:` |

## Gate posture

`GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` — unchanged by this contract.
