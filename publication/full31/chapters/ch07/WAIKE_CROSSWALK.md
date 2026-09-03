# CH07 WAIKE Crosswalk — Memory, Cache, and Storage

**Chapter:** `CH07`  
**WAIKE repository:** `gunnchOS3k/waike-research-ops`  
**Branch:** `main`  
**WAIKE SHA used:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Verification:** Local clone HEAD and `origin/main` agreed on this SHA during Agent H preproduction (2026-09-03).  
**Rule:** Evidence-backed adjacency only. **No invented module/course IDs.**  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Mapping vocabulary

| Status | Meaning |
|---|---|
| `exact` | Literally the same competency object / matching ID-title |
| `adjacent` | Existing WAIKE artifact teaches a neighboring competency |
| `proposed` | Useful future alignment; **not** present as a named module today |
| `no-map` | No responsible mapping without invention |

## Mapping counts (this chapter)

| Class | Count |
|---|---:|
| exact | 0 |
| adjacent | 4 |
| proposed | 1 |
| no-map | 1 |

## Book object → WAIKE

| Book object | WAIKE ID | ID system | Relationship | Notes |
|---|---|---|---|---|
| MCU memory map adjacency | `EMBEDDED_PROTOTYPING / lab_ep_memory_map` | digital_rc lab | `adjacent` | Flash vs SRAM neighbor—not identical to AP RAM vs SSD |
| storage triage | `GENERAL_IT / lab_storage` | digital_rc lab | `adjacent` | Operator adjacency |
| backup/persistence culture | `GENERAL_IT / lab_backup` | digital_rc lab | `adjacent` | Durability culture |
| SPI flash adjacency | `EMBEDDED_PROTOTYPING / lab_ep_spi_flash` | digital_rc lab | `adjacent` | Persistent medium neighbor |
| exact CH07 module | `—` | — | `no-map` | No exact title |
| LAB-MEM-001 as WAIKE ID | `—` | — | `proposed` | Do not mint |

## Dual ID reminder

WAIKE maintains catalog snake_case and digital_rc SCREAMING_SNAKE IDs. Prefer **digital_rc** lab IDs for runnable adjacency.

## Shared alignment note

Publication `waike/alignment.yaml` may still record older CH02 audit SHA `8eb2827…`. This packet audits `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`. Integrator may refresh shared alignment; this agent does **not** edit it.
