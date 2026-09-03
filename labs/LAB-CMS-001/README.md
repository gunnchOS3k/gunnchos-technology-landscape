# LAB-CMS-001 — Make Local Slowness Visible

**Chapter:** CE-3 (CPU, Memory, Storage, and the OS)  
**Package status:** `IMPLEMENTED_DIGITAL` + `FIXTURE_VALIDATED` + `PHYSICAL_PENDING`  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this lab does **not** claim Gate 3 PASS)

## Observable question

> When a familiar local app feels slow but the connectivity icon looks fine, what evidence can I gather—using only commodity tools—to separate **CPU**, **memory**, **storage**, and **scheduling/thermal** hypotheses?

## What this lab teaches (accessible depth)

| Idea | Plain language |
|---|---|
| CPU activity | The processor is busy executing instructions; high % can mean work *or* waiting patterns depending on what else you see. |
| Memory (RAM) | Working space for live data; not the same as disk/SSD storage. |
| Persistent storage | Files that survive quit/reopen; saves and disk activity relate here. |
| Process / app state | An app runs as one or more OS-managed processes/threads with their own memory and open files. |
| Scheduling / bottlenecks | The OS shares CPU time; many waiters can make a UI stutter even when Wi-Fi looks fine. |

## Safety (read first)

- Do **not** capture personal document contents; redact filenames before sharing.
- Do **not** install “PC cleaner” / optimizer tools, disable security software, or load kernel modules.
- Use **mild** load only (a few extra documents or tabs). **Stop** if the device warns about heat or becomes uncomfortably hot.
- No specialized hardware, Device Quartet units, or invented WAIKE module IDs are required.

## Time estimate

About 45 minutes for Explorer + Operator baseline. Builder/Engineer/Researcher extensions are optional.

## Prediction (required)

Before measuring, write which hidden part you expect to dominate during your action:

1. CPU activity  
2. Memory pressure  
3. Persistent storage / disk I/O  
4. Scheduling contention / thermal or power limits  

## Routes

### Route A — Commodity computer (baseline)

Follow `routes/commodity_computer.md`:

1. Open your built-in OS monitor (Task Manager / Activity Monitor / `top`).  
2. Record **before** CPU, memory, and disk/storage activity.  
3. Perform one controlled local action (open a medium document, scroll, or save).  
4. Record **during** readings and wall-clock feel.  
5. Optional Experience B: save → quit → reopen; note whether the file content returned.  
6. Fill observation vs inference columns.

Platform-neutral: the *concepts* are the same; UI labels differ by OS. Do not claim vendor-specific sensors you cannot see.

### Route B — Safe CLI snapshot (optional aid)

```bash
python3 labs/LAB-CMS-001/local_app/safe_snapshot.py
```

Read-only, non-destructive sampling of coarse CPU/memory/disk stats where the OS exposes them. If a metric is unavailable, the script reports `unavailable`—never invents hardware claims.

### Route C — Fixture fallback (offline / no admin)

Use `fixtures/` when monitors are inaccessible or you must avoid personal screenshots:

- `FIG-CE3-009-monitor-transcript.md` — anonymized before/during readings  
- `sample_top_transcript.txt` — text-only `top`-style transcript  
- `sample_observation_table.csv` — completed teaching table  

Fixtures reproduce **teaching points**, not a claim about your personal device.

## Pathway depths

| Path | Do this |
|---|---|
| Explorer | One controlled action; write what you felt; label ≥3 hidden parts. |
| Operator | Before/during snapshots; idle vs mild load; observation vs inference columns. |
| Builder | Change one variable; re-run table; produce hierarchy + process map. |
| Engineer | Order: connectivity rule-out → CPU → memory → disk → qualitative thermal/power; state claim-upgrade criteria. |
| Researcher | Hypothesis, variables, planned runs, confounders (thermal, battery, other processes). |
| Educator | Misconception probes + fixture facilitation (`portfolio/facilitation_sheet.md`). |

## Observation vs inference

| Observation (allowed) | Inference (must label) |
|---|---|
| CPU % rose from A to B | “CPU-bound root cause” |
| Memory used rose; disk active | “Thrashing” without page-fault evidence |
| Save completed; reopen succeeded | “All future autosaves are durable” |
| Device felt warmer | “Thermal throttle at X °C” |

## Evidence artifacts

Minimum:

- observation table (`portfolio/observation_table.csv` template)  
- two snapshots or fixture IDs with timestamps (`portfolio/evidence/NOTE.md`)  
- teach-back (`portfolio/teach_back.md`)

## Limits

- Classroom N is small; no published benchmark claims.  
- Monitor samples are coarse; they do not measure every physical stage.  
- Thermal and power effects are **qualitative** unless you have disclosed sensor evidence.  
- No unsupported hardware timing budgets.

## Portfolio

Use `labs/LAB-CMS-001/portfolio/` as the artifact folder.

## Privacy / accessibility

See `lab.yaml` (`privacy_boundary`, `safety_boundary`, `accessibility_notes`). Keyboard paths and text equivalents are required for shared evidence; fixtures cover equity when live monitors differ.
