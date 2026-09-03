# CH11 WAIKE Crosswalk (evidence-based)

**Publication chapter:** CH11 — Firmware, Boot, and Trust  
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
| CH11 boot/firmware themes | `EMBEDDED_PROTOTYPING` | digital_rc | **adjacent** | lab_ep_zephyr_qemu / bring-up adjacency |
| CH11 QEMU/OS bring-up neighbor | `HARDWARE_ENGINEERING / lab_zephyr_qemu` | digital_rc lab | **adjacent** | Digital boot before hardware |
| CH11 trust adjacency | `CYBERSECURITY` | digital_rc | **adjacent** | Hardening/incident neighbors—not secure-boot identity |
| CH11 catalog tracks | `hardware_engineering, edge_ai_embedded, cybersecurity` | catalog | **adjacent** | Track pointers only |
| LAB-BOOT-OBS-001 as WAIKE ID | `—` | — | **no-map** | Do not invent |
| Exact CH11 WAIKE module | `—` | — | **no-map** | Book-side chapter only |
| Future shared secure-boot literacy micro-lab | `—` | — | **proposed** | Integrator + WAIKE owners |

## Dual ID reminder

Catalog snake_case and digital_rc SCREAMING_SNAKE IDs are related but not interchangeable exact IDs.

## Explicit non-mappings

1. Do not invent publication lab IDs inside WAIKE.  
2. Do not treat adjacency as certification equivalence.  
3. Re-verify SHA at integrator merge time.
