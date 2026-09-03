# Route A — Commodity computer OS monitor

**Lab:** LAB-CMS-001  
**Specialized hardware:** none  
**Goal:** Separate local bottleneck *hypotheses* using tools already on a personal computer.

## Platform-neutral map

| Concept | Windows | macOS | Linux (typical) |
|---|---|---|---|
| Open monitor | Ctrl+Shift+Esc → Task Manager | Spotlight → Activity Monitor (or Cmd+Space) | Terminal → `top` or system monitor app |
| CPU activity | Performance → CPU | CPU tab | `%Cpu` / per-process `%CPU` |
| Memory (RAM) | Performance → Memory | Memory tab | `MiB Mem` / process `RES` |
| Persistent storage I/O | Performance → Disk | Disk tab (or `iostat` if already installed) | `wa` wait / disk columns if shown |
| Process / app | Processes list | Process Name | process rows in `top` |

Keyboard-first: prefer documented shortcuts above; avoid requiring mouse-only vendor gadgets.

## Procedure

### 1. Environment note (reproducibility)

Record without personal content:

- device class (laptop / desktop / tablet-as-computer)  
- OS name (no serial numbers)  
- app under test (generic: “notes editor”, not a private filename)  
- battery vs plugged  
- approximate ambient (optional: cool room / warm room)

### 2. Connectivity rule-out (light)

Glance at the connectivity icon. Optionally toggle airplane mode for a **local-only** action. If lag continues offline, network is a weaker hypothesis for *this* action—not a proof that networks never matter.

### 3. Before snapshot

With the target app open but idle:

- CPU % (overall)  
- Memory used / available (RAM)  
- Disk/storage activity if shown  
- Timestamp  

### 4. Controlled action

Choose **one**:

- open a medium local document, **or**  
- scroll a long local document, **or**  
- save a local file  

Optional mild load: open a few extra documents or browser tabs. Do not run stress/burn tools.

### 5. During snapshot

While the action is in progress (or immediately after a short hang):

- same metrics as before  
- wall-clock feel (smooth / stutter / hang)  
- qualitative heat/fan notes only if obvious—**no invented °C claims**

### 6. Optional Experience B — persistence

Save → quit app → reopen file. Observation: did the expected content return? Inference about “all future autosaves” must stay labeled.

### 7. Observation vs inference table

Copy rows into `portfolio/observation_table.csv`.

## Stop rules

- Device thermal warning or uncomfortable heat → stop, close extra load, cool down.  
- Unexpected permission prompts for kernel extensions / security disable → cancel.  
- Accidental personal content in a screenshot → delete or redact before portfolio use.

## What not to claim

- More cores always make this action faster.  
- RAM and storage are the same.  
- The OS “does the app’s thinking” rather than scheduling and mediating.  
- A single high CPU sample proves root cause.  
- Any Device Quartet or specialized lab bench measurement.
