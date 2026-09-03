# CH21 — WAIKE Crosswalk

**Book object:** CH21 — Data, Machine Learning, and Generative AI  
**WAIKE repository:** `gunnchOS3k/waike-research-ops`  
**Audited SHA:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Map classes:** `exact` | `adjacent` | `proposed` | `no-map`  
**Rule:** Do not invent course/lab IDs. Dual ID systems (catalog `snake_case` vs digital_rc `SCREAMING_SNAKE`) are related but not interchangeable.

## Exact

_None. No exact WAIKE module equals this chapter._


## Adjacent

| WAIKE ID | ID system | Notes |
|---|---|---|
| `AI_ML_EDGE` | digital_rc | course package for inference/edge/RAG privacy |
| `lab_score_model` | digital_rc lab | inference scoring adjacency |
| `lab_rag_redact` | digital_rc lab | retrieval without leaking patrons |
| `lab_quantize_budget` | digital_rc lab | edge budget adjacency (also CH22) |
| `ai_ml_data` | catalog | program-track pointer; not identical to AI_ML_EDGE |


## Proposed

| Proposal | Notes |
|---|---|
| Shared eval fixture format bridging LAB-TRUST-001 and AI_ML_EDGE labs | integrator + WAIKE owners |


## No-map

- No WAIKE course/lab ID named CH21, CE-5, or LAB-TRUST-001


## Counts (this chapter)

| Class | Count |
|---|---:|
| exact | 0 |
| adjacent | 5 |
| proposed | 1 |
| no-map | 1 |

## Integrator handoff

- Do not edit shared `waike/alignment.yaml` from this agent  
- Preserve SHA continuity note if shared registry still cites older CH02 SHA `8eb2827…`
