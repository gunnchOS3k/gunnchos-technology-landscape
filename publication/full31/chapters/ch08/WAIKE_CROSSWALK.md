# CH08 WAIKE Crosswalk — Graphics, Displays, Audio, Cameras, and Sensors

**Chapter:** `CH08`  
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
| sensor noise adjacency | `ROBOTICS_CONTROL / lab_sensor_noise` | digital_rc lab | `adjacent` | Sensing uncertainty neighbor |
| game loop / frame adjacency | `GAME_DEV_INTERACTIVE / lab_game_loop` | digital_rc lab | `adjacent` | Keep Ch8 non-game-only |
| game a11y adjacency | `GAME_DEV_INTERACTIVE / lab_game_a11y` | digital_rc lab | `adjacent` | Inclusive media |
| ADC scale adjacency | `EMBEDDED_PROTOTYPING / lab_ep_adc_scale` | digital_rc lab | `adjacent` | Sampling neighbor |
| exact CH08 module | `—` | — | `no-map` | No exact title |
| LAB-IO-001 as WAIKE ID | `—` | — | `proposed` | Do not mint |

## Dual ID reminder

WAIKE maintains catalog snake_case and digital_rc SCREAMING_SNAKE IDs. Prefer **digital_rc** lab IDs for runnable adjacency.

## Shared alignment note

Publication `waike/alignment.yaml` may still record older CH02 audit SHA `8eb2827…`. This packet audits `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`. Integrator may refresh shared alignment; this agent does **not** edit it.
