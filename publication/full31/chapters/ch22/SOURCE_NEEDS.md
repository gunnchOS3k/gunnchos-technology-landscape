# CH22 — Source Needs

**Chapter:** CH22 — Edge AI, Sensors, and Embodied Interaction  
**WAIKE audit SHA (this packet):** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Publication accepted-main:** `0e694176652d4729c7f2b71df08b871a863afb8c`  
**Policy:** No fake citations. Prefer standards → official docs → peer-reviewed → textbooks. Mark gaps honestly.

## Status vocabulary

`SOURCE_IDENTIFIED` · `SOURCE_NEEDED` · `PROJECT_EVIDENCE_NEEDED` · `PHYSICAL_PENDING` · (`ILLUSTRATIVE_ONLY` for non-cited teaching aids)

## Planned sources

| Key / need | Status | Class | Notes |
|---|---|---|---|
| `SRC-HARDWARE` | PHYSICAL_PENDING | repository | gunnchos-hardware Device Quartet docs; no measured embodied AI |
| `SRC-WAIKE` | SOURCE_IDENTIFIED | repository | AI_ML_EDGE/lab_quantize_budget; EMBEDDED_PROTOTYPING labs @ e97e74fc9bfb44b1cdc26b272dc4848264f15fe0 |
| `edge_ml_sys_refs` | SOURCE_NEEDED | textbook/standards | Select official edge-ML / MCU-NN docs with verified metadata |
| `sensing_privacy_std` | SOURCE_NEEDED | standards | Primary sensing/privacy guidance TBD |

## Inheritance

Link deeper CE registers rather than copying:

- CE-5 local-vs-cloud / edge budget themes
- CE-3/CH08 sensor adjacency (link, do not re-teach catalog)

## Explicit non-sources

- Invented WAIKE module IDs for this chapter  
- Marketing pages as bibliography  
- Silent overwrite of conflicting WCAG dates (Ch24: keep `wcag22-20231005` and `wcag22-20241212`)  
- Illustrative EMIT examples as human evidence (Ch31)

## Integrator note

Do not merge candidates into global `book/references/references.bib` until promotion rules authorize it.

## Remaining SOURCE_NEEDED (QUALITY-E)

| Claim / need | Status / next step |
|---|---|
| `CLM-CH22-004` sensing / camera privacy | `SOURCE_IDENTIFIED` via `w3c-mediacapture-streams-20251009` + `w3c-permissions-20251006` (camera/mic permission mediation; no invented IMU-fusion ISO) |
