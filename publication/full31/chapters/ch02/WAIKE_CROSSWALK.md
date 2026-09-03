# CH02 WAIKE Crosswalk — Follow One Tap Through the Entire Stack

**Chapter:** `CH02`  
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
| proposed | 0 |
| no-map | 1 |

## Book object → WAIKE

| Book object | WAIKE ID | ID system | Relationship | Notes |
|---|---|---|---|---|
| LAB-TAP-001 themes | `SOFTWARE_BUILDER` | digital_rc | `adjacent` | Event handling / instrumentation |
| input adjacency | `GAME_DEV_INTERACTIVE / lab_input_actions` | digital_rc lab | `adjacent` | Not a UI-tap clone |
| packet adjacency | `COMPUTER_NETWORKING` | digital_rc | `adjacent` | Datapath neighbor |
| latency-budget adjacency | `EMBEDDED_PROTOTYPING / lab_ep_isr_vs_poll` | digital_rc lab | `adjacent` | ISR vs poll neighbor |
| exact LAB-TAP-001 module | `—` | — | `no-map` | Explicit non-mapping |

## Dual ID reminder

WAIKE maintains catalog snake_case and digital_rc SCREAMING_SNAKE IDs. Prefer **digital_rc** lab IDs for runnable adjacency.

## Shared alignment note

Publication `waike/alignment.yaml` may still record older CH02 audit SHA `8eb2827…`. This packet audits `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`. Integrator may refresh shared alignment; this agent does **not** edit it.
