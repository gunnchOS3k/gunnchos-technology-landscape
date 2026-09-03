# CE-3 Lab Plan — LAB-CMS-001

**Proposed lab ID:** `LAB-CMS-001`  
**Title (working):** Make Local Slowness Visible  
**Chapter:** CE-3  
**Status:** `preproduction` (plan only — not a runnable lab package yet)  
**Ownership:** Publication-owned commodity lab (do **not** invent a WAIKE module ID with this name)

---

## Question

When a familiar local app feels slow but the connectivity icon looks fine, what evidence can I gather—using only commodity tools—to separate **CPU**, **memory**, **storage**, and **scheduling/thermal** hypotheses?

## Anchor experience

Local lag with a healthy connectivity icon (Experience A), with an optional save/quit/reopen persistence check (Experience B).

## Pathway depths

### Explorer — observe / identify
- Perform one controlled local action (open a medium document, scroll, or save).
- Write what you felt (stutter, hang, heat).
- Label at least three hidden parts that might be involved.

### Operator — inspect / compare
- Capture **before** and **during** snapshots of CPU, memory, and disk from the OS monitor.
- Compare idle baseline vs intentional mild load (open extra documents / export).
- Fill observation vs inference columns.

### Builder — modify / create
- Change one variable (document count, export quality, background sync toggle, browser tab count).
- Re-run the observation table.
- Produce a personal hierarchy + process map for the chosen experience.

### Engineer — measure / diagnose
- Order inspections: connectivity check (rule-out) → CPU → memory → disk → qualitative thermal/power mode.
- State what additional evidence would be required before claiming causation.
- Optional: capture wall-clock durations for a fixed action under two conditions (N small; disclose confounders).

### Researcher — hypothesize / controlled comparison
- Write a hypothesis (e.g., “Adding background CPU load increases scroll hitch rate more than adding idle tabs”).
- Define variables, planned runs, and limits.
- Explicitly list thermal state, battery mode, and other processes as confounders—not as proven mediators without evidence.

### Educator — facilitate
- Run misconception probes (RAM≠storage; cores≠always-faster; OS schedules ≠ OS does app work).
- Provide fixture screenshots for learners without admin rights or accessible devices.

---

## Required devices / software

| Item | Requirement |
|---|---|
| Device | Any personal computer or tablet/laptop the learner already uses |
| OS monitor | Task Manager (Windows), Activity Monitor (macOS), or `top`/`htop` (Linux) / equivalent |
| App under test | Any local editor, notes, office, photo, or IDE app |
| Network | Optional airplane-mode control for rule-out; not required for primary path |
| Specialized hardware | **None** |

## Lowest-friction route

1. Open OS monitor.  
2. Note baseline CPU/memory/disk.  
3. Perform one local action.  
4. Note during-action readings + wall-clock feel.  
5. Optional: save / quit / reopen persistence check.  
6. Write observation vs inference.

## Offline / fixture fallback

- Instructor-supplied **anonymized screenshots** of monitors (FIG-CE3-009) with reading guides.
- Printed or Markdown observation sheet.
- No cloud account required.
- If monitor UI is inaccessible, use a text-only `top` transcript fixture.

## Expected evidence artifacts

- Observation table (CSV or Markdown).
- Two monitor snapshots (or fixture IDs) with timestamps.
- Short teach-back: RAM vs storage + “OS schedules / apps still compute.”
- Optional Builder map file.
- Portfolio folder proposal: `labs/LAB-CMS-001/portfolio/` (to be created in a later implementation wave—not in this preproduction commit unless integrator requests).

## Observation vs inference boundary

| Observation (allowed) | Inference (must label) |
|---|---|
| CPU % rose from A to B during action | “CPU-bound root cause” |
| Memory used rose; disk active | “Thrashing” without page-fault evidence |
| Save completed and file reopen succeeded | “All future autosaves are durable” |
| Device felt warmer | “Thermal throttle at X °C” |

## Privacy / safety boundary

- Do not capture personal document contents; blur filenames if screenshots leave the device.
- Do not enable kernel debug modes, disable security software, or run untrusted “optimizer” tools.
- Do not stress devices to unsafe temperatures; stop if the device warns or becomes uncomfortably hot.
- No requirement to install kernel modules or custom firmware.

## Accessibility considerations

- Provide keyboard-only paths to OS monitors where possible.
- Color-independent reading of charts (patterns/labels).
- Text equivalents for all screenshots.
- Allow verbal/dictated observation tables.
- Low-bandwidth/offline fixtures for equity.

## Reproducibility strategy

- Record: device class (personal laptop/phone/desktop), OS name, app name, battery/plugged, approximate ambient notes.
- Use small N classroom runs; no published benchmark claims.
- Fixture route must reproduce the **teaching points** even when live monitors differ.

## Portfolio artifact produced

| Artifact | Pathway |
|---|---|
| Observation table + teach-back | Explorer/Operator |
| Hierarchy/process map | Builder |
| Diagnosis plan with claim-upgrade criteria | Engineer |
| Hypothesis + confounders note | Researcher |
| Facilitation sheet | Educator |

## Explicit non-dependencies

- No Device Quartet physical units.
- No gunnchOS device-os shipping kernel.
- No invented WAIKE `lab_cms_001` course ID—adjacency only (see `WAIKE_CROSSWALK.md`).
