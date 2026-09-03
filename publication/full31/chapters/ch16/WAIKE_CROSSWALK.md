# CH16 WAIKE Crosswalk (evidence-based)

**Publication chapter:** CH16 — Packets, Protocols, Routing, and the Internet  
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
| CH16 / LAB-PKT-001 | `—` | — | **no-map** | No WAIKE ID LAB-PKT-001 |
| CH16 themes | `COMPUTER_NETWORKING` | digital_rc | **adjacent** | Packets to campus edge |
| CH16 datapath | `lab_datapath` | digital_rc lab | **adjacent** | Strongest neighbor |
| CH16 CIDR | `lab_cidr_math` | digital_rc lab | **adjacent** |  |
| CH16 SPF | `lab_spf_routing` | digital_rc lab | **adjacent** | Optional stretch |
| CH16 DNS | `lab_dns_resolution` | digital_rc lab | **adjacent** |  |
| CH16 DNS LAN | `lab_dns_hosts` | digital_rc lab | **adjacent** | GENERAL_IT |
| CH16 catalog | `networking` | catalog | **adjacent** | Dual ID systems |

## Dual ID reminder

Catalog snake_case and digital_rc SCREAMING_SNAKE IDs are related but not interchangeable exact IDs.

## Explicit non-mappings

1. Do not invent publication lab IDs inside WAIKE.  
2. Do not treat adjacency as certification equivalence.  
3. Re-verify SHA at integrator merge time.
