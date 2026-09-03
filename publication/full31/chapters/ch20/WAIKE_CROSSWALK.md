# CH20 WAIKE Crosswalk (evidence-based)

**Publication chapter:** CH20 — Latency, Reliability, QoE, and the Stability Contract  
**WAIKE repository:** `gunnchOS3k/waike-research-ops`  
**Branch:** `main`  
**Accepted-main SHA used for this audit:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Method:** Inherit verified IDs from CE-3/CE-4/CE-5/CE-6 crosswalks at the same SHA; do not invent new course/lab IDs.

**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Mapping status legend

| Status | Meaning |
|---|---|
| **exact** | Same competency object exists and can be cited by ID |
| **adjacent** | Related course/lab exists; competency neighbor |
| **proposed** | Future alignment idea; not present as an ID |
| **no-map** | No honest mapping; do not invent |

## Book object → WAIKE map

| Book object | WAIKE ID | ID system | Status | Notes |
|---|---|---|---|---|
| CH20 / LAB-CE06-001 | `—` | — | **no-map** | Publication-owned |
| CH20 SLO intuition | `lab_slo_budget` | digital_rc lab | **adjacent** | Error budgets neighbor |
| CH20 networking | `COMPUTER_NETWORKING` | digital_rc | **adjacent** |  |
| CH20 observability | `SOFTWARE_BUILDER / lab_observability` | digital_rc lab | **adjacent** |  |
| CH20 ethics evidence language | `COMM_PD_ETHICS / lab_ethics_ladder` | digital_rc lab | **adjacent** | Observation before inference |
| Future shared continuity+QoE lab | `—` | — | **proposed** | Integrator |

## Dual ID reminder

Catalog snake_case and digital_rc SCREAMING_SNAKE IDs are related but not interchangeable exact IDs.

## Explicit non-mappings

1. Do not invent publication lab IDs inside WAIKE.  
2. Do not treat adjacency as certification equivalence.  
3. Re-verify SHA at integrator merge time.
