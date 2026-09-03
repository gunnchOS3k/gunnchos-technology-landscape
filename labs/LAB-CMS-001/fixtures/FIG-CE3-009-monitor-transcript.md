# FIG-CE3-009 — Anonymized monitor transcript (fixture)

**Figure / fixture ID:** `FIG-CE3-009`  
**Status:** teaching illustration (`FIXTURE_VALIDATED`) — **not** a measurement of the learner’s device  
**Privacy:** filenames, account names, and thumbnails removed

## Scenario (synthetic)

Learner opens a medium local notes document and scrolls while a few background apps remain idle. Connectivity icon appears healthy.

## Before (idle baseline)

| Metric | Reading | Text equivalent |
|---|---|---|
| Timestamp | 2026-09-03T15:00:00Z | Before action |
| CPU (overall) | 8% | Low overall processor activity |
| Memory used | 6.2 GB of 16 GB | Moderate RAM use; headroom remains |
| Disk activity | Idle / near 0% | Little persistent-storage traffic |
| Top process (redacted) | `NotesApp` ~3% CPU | Foreground editor lightly active |

## During (scroll / open medium document)

| Metric | Reading | Text equivalent |
|---|---|---|
| Timestamp | 2026-09-03T15:00:25Z | During action |
| CPU (overall) | 41% | Clear rise versus baseline |
| Memory used | 6.9 GB of 16 GB | RAM rose; still below capacity |
| Disk activity | Brief spike then settle | Short storage burst, then quiet |
| Top process (redacted) | `NotesApp` ~28% CPU | Foreground editor dominates the rise |
| Qualitative feel | Brief stutter, then smooth | Human-experienced hitch |
| Heat / fans | Slightly warmer; fan audible once | Qualitative only — no °C claimed |

## Reading guide (teaching points)

1. **CPU activity rose** during the local action while connectivity looked fine → network is a weaker hypothesis *for this run*.  
2. **RAM ≠ storage:** memory used rose modestly; disk spiked briefly (save/cache), then settled.  
3. **Process/app state:** the redacted editor process accounts for much of the CPU rise — the OS scheduled it; the app still performed the work.  
4. **Bottleneck reasoning:** evidence is consistent with short CPU + brief storage work; it does **not** prove permanent thrashing or thermal throttle.  
5. **Claim upgrade needed** before causation: page-fault/swap evidence for thrashing; sensor logs for thermal claims; repeated timed runs for performance conclusions.

## Misconception probes

- Does higher CPU % always mean the CPU is the root cause? (**No** — could be waiting, sampling artifact, or concurrent work.)  
- If disk spiked once, is the device “out of storage”? (**Not from one spike alone.**)  
- Did the OS “write the essay for you”? (**No** — it scheduled and mediated; the app computed.)
