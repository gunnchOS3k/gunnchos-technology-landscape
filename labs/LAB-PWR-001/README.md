# LAB-PWR-001 — Budget Collapse Observation

**Chapter:** CH09  
**Status:** `IMPLEMENTED_DIGITAL` (fixture available; commodity observation; not a human-learning PASS)  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Observable question

> What visible battery-mode and thermal cues appear when I compare a light local workload with a heavier local workload on a device I already own—without unsafe heating or battery abuse?

## Safety (mandatory non-goals)

- Do **not** open, puncture, crush, overcharge, freeze, microwave, or externally heat batteries or packs.
- Do **not** block vents to force throttle, bake devices, or defeat thermal protections.
- Stop on warnings, unusual odor, swelling, or painful heat.
- Prefer ambient room conditions only.
- Scrub passwords, tokens, and personal content from evidence.

## Time estimate

About 45–75 minutes including write-up.

## Prediction

Write whether you expect smoothness, warmth, battery drop, or OS cues to change first under the heavier load.

## Routes

### Route A — Commodity device (baseline)

1. Record device class, OS, plugged vs battery, room comfort band (cool / comfortable / warm)—no invented °C.
2. Light local task for a few minutes.
3. Heavier local task (still prefer local-only).
4. Fill the observation table: observed vs inferred.

### Route B — OS status pages (optional)

Note qualitative battery/energy fields the platform exposes. Do not claim hidden vendor telemetry.

### Route C — Offline fixture (required fallback)

Open `fixtures/budget_collapse_card.md` and complete the table using labeled **fixture / illustrative** scenarios.

## Depth ladder

| Pathway | Ask |
|---|---|
| Explorer | What cues changed? |
| Operator | Plugged vs battery confounders? |
| Builder | Draw energy → heat → throttle map (no invented watts). |
| Engineer | Diagnosis tree before blaming the app. |
| Researcher | PHYSICAL_PENDING measurement plan only—no fabricated results. |
| Educator | Lead with safety non-goals; use fixture when needed. |

## Evidence (minimum)

- scrubbed screenshot or written status list
- light vs heavier observation table
- observation vs inference paragraph
- safety confirmation checkbox in your README

## Limits

- Warmth ≠ precise junction temperature.
- One session ≠ product thermal qualification.
- Device Quartet watt/°C curves remain PHYSICAL_PENDING.
- WAIKE `lab_power_budget` / `lab_ep_sleep_mode` are adjacency only (SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`).

## Portfolio output

README, observation table, one evidence artifact, reflection, teach-back paragraph.
