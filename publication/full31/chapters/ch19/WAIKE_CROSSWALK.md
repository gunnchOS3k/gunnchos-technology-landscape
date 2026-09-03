# CH19 WAIKE Crosswalk (evidence-based)

**Publication chapter:** CH19 — NTN and Service Continuity Across Ground, Air, and Space  
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
| CH19 wireless advanced | `WIRELESS_6G` | digital_rc | **adjacent** | Advanced radio; not NTN-identical |
| CH19 continuity proposed | `—` | — | **proposed** | Future continuity micro-lab across CE-4/CE-6/CH19 |
| Exact NTN WAIKE lab | `—` | — | **no-map** | Do not invent NTN lab IDs |
| LAB-CONT-001 | `—` | — | **no-map** |  |

## Dual ID reminder

Catalog snake_case and digital_rc SCREAMING_SNAKE IDs are related but not interchangeable exact IDs.

## Explicit non-mappings

1. Do not invent publication lab IDs inside WAIKE.  
2. Do not treat adjacency as certification equivalence.  
3. Re-verify SHA at integrator merge time.
