# CH14 WAIKE Crosswalk (evidence-based)

**Publication chapter:** CH14 — Applications, APIs, Runtimes, and User Interfaces  
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
| CH14 app building | `SOFTWARE_BUILDER` | digital_rc | **adjacent** | Builder track |
| CH14 input/UI adjacency | `GAME_DEV_INTERACTIVE / lab_input_actions` | digital_rc lab | **adjacent** | Input-layer neighbor from CH02 crosswalk |
| CH14 catalog | `software_engineering` | catalog | **adjacent** |  |
| LAB-API-OBS-001 | `—` | — | **no-map** |  |
| Exact CH14 module | `—` | — | **no-map** |  |

## Dual ID reminder

Catalog snake_case and digital_rc SCREAMING_SNAKE IDs are related but not interchangeable exact IDs.

## Explicit non-mappings

1. Do not invent publication lab IDs inside WAIKE.  
2. Do not treat adjacency as certification equivalence.  
3. Re-verify SHA at integrator merge time.
