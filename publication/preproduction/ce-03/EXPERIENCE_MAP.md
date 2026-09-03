# CE-3 Experience Map

**Module:** CE-3 — CPU, Memory, Storage, and the OS  
**Status:** `preproduction`  
**Teaching model:** Human experience → system → component → code → network → society

At least three teachable human experiences are defined below. One is selected as the **canonical anchor**.

---

## Experience A — Canonical anchor: Local lag with a healthy connectivity icon

### Human moment
You work in a familiar local app. The network icon still looks fine. Scrolling stutters, a save hangs, or the UI freezes briefly while the device warms or the fan spins.

### Observable behavior
- UI redraw becomes uneven; clicks queue up; progress indicators linger.
- Commodity monitors may show elevated CPU, memory, or disk activity (or “waiting”).
- Optional: device temperature feel / power mode change (qualitative).

### Hidden systems
- Application threads doing computation or waiting on I/O.
- OS scheduler multiplexing CPU time across processes/threads.
- Memory hierarchy (registers → cache → RAM) under pressure; possible paging.
- Storage stack persisting files (or failing to complete writes).
- Optional accelerator/GPU work for UI composition or media.
- Power/thermal governors reducing clocks when budgets tighten.

### Likely failure modes
- CPU saturation by foreground or background work.
- Memory pressure causing thrash or aggressive cache eviction.
- Storage I/O backlog (large save, sync, indexer).
- Lock/contention making CPU look busy while progress stalls.
- Thermal/power throttling reducing available performance.
- Mis-attribution: blaming Wi-Fi because “internet culture” defaults there.

### Measurement or inspection opportunity
- Before/during snapshots of CPU, memory, disk with OS monitors.
- Wall-clock timing of a controlled action (open, scroll, save, export).
- Quit+reopen check for persistence vs volatility.
- **Not yet:** silicon-level counters, EVT thermal curves, or invented latency budgets.

### Career / system connection
Performance engineering, OS/kernel, SRE-style local diagnosis, embedded resource budgeting, IT support triage (power → storage → memory → OS).

### Why this is the canonical anchor
It is universal, requires no specialized hardware, forces the RAM≠storage and CPU≠network distinctions, and lets every pathway depth (observe → diagnose → hypothesize) hang from one story without duplicating CE-2’s tap path.

---

## Experience B — Save, quit, reopen: persistence vs volatility

### Human moment
You type notes, save (or think you saved), quit the app, reopen later—or the device restarts.

### Observable behavior
- Content present, partially present, or gone.
- “Recovered documents” / autosave dialogs.
- Storage space warnings vs “app still open in memory” confusion.

### Hidden systems
- Volatile working set in RAM vs durable bytes on storage.
- File system, caches, write-back buffers, crash consistency.
- OS process lifetime vs file lifetime.

### Likely failure modes
- User never completed a durable write.
- App crash before flush.
- Storage full / permission denied.
- Confusing “still on screen” with “saved to disk.”

### Measurement or inspection opportunity
- Controlled save/quit/reopen checklist.
- File timestamp / size observation in a file manager.
- Compare unsaved buffer vs on-disk file (ordinary UI evidence).

### Career / system connection
Storage/FS engineering, IT backup literacy, application durability design, digital evidence hygiene (without turning CE-3 into forensics training).

---

## Experience C — Heat and slowdown during heavy local work

### Human moment
Video export, large photo batch, local ML demo, or a demanding game: device becomes hot; after a while the same action feels slower.

### Observable behavior
- Sustained high CPU/GPU activity early; later slowdown with heat/fan.
- Battery percentage drop accelerates (qualitative observation only).

### Hidden systems
- Dynamic voltage/frequency scaling; thermal policy.
- CPU vs GPU/accelerator division of labor.
- Shared memory bandwidth contention.

### Likely failure modes
- Thermal throttle misread as “software bug.”
- Assuming more cores would eliminate heat-limited slowdowns.
- Ignoring ambient temperature / surface blocking vents (confounders).

### Measurement or inspection opportunity
- Time a fixed export at start vs after sustained load (wall clock).
- Note qualitative thermal state; do **not** invent °C thresholds.
- Optional OS energy/thermal pages where present—label as platform-specific.

### Career / system connection
Hardware/thermal design (full-book CH09), embedded power budgets (WAIKE adjacency), mobile performance engineering.

---

## Experience D — Optional classroom variant: “Too many tabs”

### Human moment
Browser or editor with many documents open; switching becomes sticky.

### Why optional
Useful Explorer hook, but easy to over-blame “RAM” without inspection. Prefer as a Builder/Educator variant under Experience A rather than a second anchor.

---

## Pathway coverage across experiences

| Pathway | Primary use of experiences |
|---|---|
| Explorer | A + B teach-back (feel → parts; RAM vs storage) |
| Operator | A monitor snapshots; B reopen checklist |
| Builder | A/B personal maps; controlled load change |
| Engineer | A diagnosis plan; C confounders |
| Researcher | A/C hypothesis + limits |
| Educator | A misconception lab; fixture screenshots of monitors |

## Device Quartet note

Form-factor differences (laptop-adjacent vs handheld vs dual-screen coder vs wearables) may be cited only as **representative educational architecture** from the hardware industrial-design accepted-main audit. Do not present comparison-matrix RAM/storage numbers as measured shipping results (`PHYSICAL_PENDING`).
