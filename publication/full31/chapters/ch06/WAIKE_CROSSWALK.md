# CH06 WAIKE Crosswalk — CPU, Instructions, and Parallel Work

**Chapter:** `CH06`  
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
| scheduling / latency adjacency | `EMBEDDED_PROTOTYPING / lab_ep_isr_vs_poll` | digital_rc lab | `adjacent` | Who runs when |
| QEMU/OS adjacency | `HARDWARE_ENGINEERING / lab_zephyr_qemu` | digital_rc lab | `adjacent` | Runtime exposure |
| observability | `SOFTWARE_BUILDER / lab_observability` | digital_rc lab | `adjacent` | Evidence habits |
| catalog hardware/software tracks | `hardware_engineering / software_engineering` | catalog | `adjacent` | Dual ID systems |
| exact CH06 module | `—` | — | `no-map` | No exact title match |
| LAB-CPU-001 as WAIKE ID | `—` | — | `proposed` | Do not mint |

## Dual ID reminder

WAIKE maintains catalog snake_case and digital_rc SCREAMING_SNAKE IDs. Prefer **digital_rc** lab IDs for runnable adjacency.

## Shared alignment note

Publication `waike/alignment.yaml` may still record older CH02 audit SHA `8eb2827…`. This packet audits `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`. Integrator may refresh shared alignment; this agent does **not** edit it.
