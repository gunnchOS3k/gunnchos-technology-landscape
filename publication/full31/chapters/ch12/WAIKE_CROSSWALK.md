# CH12 WAIKE Crosswalk (evidence-based)

**Publication chapter:** CH12 — Operating Systems, Processes, Threads, and Scheduling  
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
| CH12 / LAB-CMS-001 | `—` | — | **no-map** | No WAIKE ID named LAB-CMS-001 |
| CH12 scheduling adjacency | `EMBEDDED_PROTOTYPING / lab_ep_isr_vs_poll` | digital_rc lab | **adjacent** | Latency-budget neighbor |
| CH12 OS literacy | `GENERAL_IT / lab_os_users` | digital_rc lab | **adjacent** | Operator adjacency |
| CH12 observability | `SOFTWARE_BUILDER / lab_observability` | digital_rc lab | **adjacent** | Evidence habits |
| CH12 catalog | `software_engineering, general_it` | catalog | **adjacent** | Track pointers |
| Future desktop scheduler literacy module | `—` | — | **proposed** | Not present on accepted main |

## Dual ID reminder

Catalog snake_case and digital_rc SCREAMING_SNAKE IDs are related but not interchangeable exact IDs.

## Explicit non-mappings

1. Do not invent publication lab IDs inside WAIKE.  
2. Do not treat adjacency as certification equivalence.  
3. Re-verify SHA at integrator merge time.
