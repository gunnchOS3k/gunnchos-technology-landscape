# CH13 WAIKE Crosswalk (evidence-based)

**Publication chapter:** CH13 — Files, Databases, and Data Lifecycles  
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
| CH13 storage triage | `GENERAL_IT / lab_storage` | digital_rc lab | **adjacent** | Operator adjacency |
| CH13 backup culture | `GENERAL_IT / lab_backup` | digital_rc lab | **adjacent** | Persistence ops neighbor |
| CH13 privacy lifecycle | `COMM_PD_ETHICS / lab_consent_disclosure` | digital_rc lab | **adjacent** | Retain/share language |
| CH13 cloud costed storage | `CLOUD_DEVOPS / lab_cloud_cost` | digital_rc lab | **adjacent** | Storage as costed block |
| LAB-DATA-LIFE-001 | `—` | — | **no-map** | Publication-owned proposal only |
| Exact CH13 module | `—` | — | **no-map** |  |

## Dual ID reminder

Catalog snake_case and digital_rc SCREAMING_SNAKE IDs are related but not interchangeable exact IDs.

## Explicit non-mappings

1. Do not invent publication lab IDs inside WAIKE.  
2. Do not treat adjacency as certification equivalence.  
3. Re-verify SHA at integrator merge time.
