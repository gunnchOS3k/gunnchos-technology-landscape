# LAB-PERF-001 — Make Feel Visible

**Chapter:** CH03 — Performance: Why Technology Feels Fast, Slow, Smooth, or Unstable  
**Package status:** `IMPLEMENTED_DIGITAL` (lean) + fixture fallback via **LAB-CMS-001** + `PHYSICAL_PENDING`  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this lab does **not** claim Gate 3 PASS)

## Observable question

> Under two load conditions on a device I already own, what wall-clock and commodity observations can I record so that “felt slow / felt smooth” becomes evidence instead of vibes?

## Neighbor labs

| Lab | Relationship |
|---|---|
| LAB-TAP-001 | Chapter 2 tap-path timings; prototype evidence, not universal SLOs |
| LAB-CMS-001 | Local CPU/memory/storage/scheduler diagnosis when connectivity looks fine |

## Safety (read first)

- Do **not** capture secrets or personal document contents; redact filenames.
- Mild load only. **Stop** on heat warnings or uncomfortable warmth.
- No untrusted “optimizer” tools, no disabling security software, no rooting.

## Prediction (required)

Before measuring, write which axis you expect to dominate under load:

1. Latency  
2. Jitter / stalls  
3. Throughput limits  
4. Availability / errors  

…and whether you expect the branch to look **local**, **network**, or **unclear**.

## Routes

### Route A — Browser feel timeline (baseline)

Follow `routes/browser_feel.md`.

### Route B — LAB-CMS-001 neighbor

Use `labs/LAB-CMS-001/routes/commodity_computer.md` when the feel problem appears with a healthy connectivity icon.

### Route C — Fixture fallback

Use `labs/LAB-CMS-001/fixtures/` when monitors are inaccessible. Fixture numbers are teaching illustrations only.

**FIG-CE3-009** remains `BLOCKED_EVIDENCE_REQUIRED`. Synthetic fixtures do not unblock the measured figure.

## Evidence (minimum)

- feel log (`portfolio/feel_log.md`)
- two-condition observation table (`portfolio/observation_table.csv`)
- feel→candidate-cause map (`portfolio/feel_cause_map.md`)
- evidence note (`portfolio/evidence/NOTE.md`)
- teach-back (`portfolio/teach_back.md`)

## Limits

- One run is not a benchmark.
- No invented Device Quartet performance budgets (`PHYSICAL_PENDING`).
- Software timestamps do not measure every physical stage.
