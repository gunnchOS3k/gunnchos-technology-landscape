# CH22 — WAIKE Crosswalk

**Book object:** CH22 — Edge AI, Sensors, and Embodied Interaction  
**WAIKE repository:** `gunnchOS3k/waike-research-ops`  
**Audited SHA:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Map classes:** `exact` | `adjacent` | `proposed` | `no-map`  
**Rule:** Do not invent course/lab IDs. Dual ID systems (catalog `snake_case` vs digital_rc `SCREAMING_SNAKE`) are related but not interchangeable.

## Exact

_None. No exact WAIKE module equals this chapter._


## Adjacent

| WAIKE ID | ID system | Notes |
|---|---|---|
| `AI_ML_EDGE` | digital_rc | edge budget / inference labs |
| `lab_quantize_budget` | digital_rc lab | latency/budget tradeoff |
| `EMBEDDED_PROTOTYPING` | digital_rc | ISR/poll latency-budget adjacency |
| `edge_ai_embedded` | catalog | catalog track pointer |


## Proposed

| Proposal | Notes |
|---|---|
| Publication fixture for embodied interaction without physical Device Quartet | keep PHYSICAL_PENDING explicit |


## No-map

- No WAIKE ID for Edge IO Wearables product module
- No WAIKE lab_id LAB-CH22-SENSE-001


## Counts (this chapter)

| Class | Count |
|---|---:|
| exact | 0 |
| adjacent | 4 |
| proposed | 1 |
| no-map | 2 |

## Integrator handoff

- Do not edit shared `waike/alignment.yaml` from this agent  
- Preserve SHA continuity note if shared registry still cites older CH02 SHA `8eb2827…`
