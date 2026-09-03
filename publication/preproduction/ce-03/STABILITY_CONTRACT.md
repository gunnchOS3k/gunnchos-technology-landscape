# CE-3 Stability Contract — Local lag with healthy connectivity

**Anchor experience:** Local lag / stutter / hang while the connectivity icon still looks fine.  
**Status:** `preproduction` — qualitative conditions only. **No invented performance budgets.**

---

## Contract statement (chapter application)

A smooth local interaction exists only while multiple hidden conditions remain within acceptable bounds at once: runnable work can obtain CPU (or accelerator) time, memory capacity/bandwidth remains adequate, durable or working storage I/O completes when required, the OS scheduler continues to allocate attention fairly enough for the interactive path, and power/thermal policy still permits the needed performance—regardless of whether a network icon appears healthy.

A device can remain **technically powered on and connected** while the **human experience has already failed**.

---

## Hidden technical conditions (qualitative)

| Condition | Why it matters to the human |
|---|---|
| Interactive threads become runnable and obtain CPU time | Clicks/scrolls do not queue indefinitely |
| Working set fits reasonably in RAM (or paging stays mild) | Switching and editing stay responsive |
| Needed file/storage operations complete | Saves and opens finish |
| Scheduler does not starve the interactive path under contention | Background work does not erase foreground usability |
| Memory hierarchy delivers data without pathological miss/thrash behavior | “Simple” actions do not feel randomly stuck |
| Power/thermal policy allows sufficient clocks | Sustained work does not silently crawl |
| Optional accelerators complete UI/media work when relied upon | Composition/export does not stall the seat experience |

## Failure domains

1. **CPU / accelerator contention or saturation**  
2. **Memory pressure / reclaim / thrash**  
3. **Storage I/O backlog or durability failure**  
4. **Scheduler / lock contention** (busy yet not progressing)  
5. **Power / thermal limiting**  
6. **Mis-attributed network domain** (icon healthy; local cause)  
7. **Application logic bugs** (infinite loop, main-thread block)—still local, still not “the internet”

## Dependencies

- Hardware: CPU/accelerator, RAM, storage device, power/thermal sensors & governors.  
- Software: app threads, OS abstractions (process/thread/file/VM), drivers.  
- Human: expectations about what “saved” and “responsive” mean.  
- Optional remote services: out of scope for the anchor except as a **ruled-out** explanation when connectivity appears fine and the workload is local.

## Locally observable symptoms

- Stuttering scroll; delayed key echoes; beachball/spinner.  
- Fan noise; device warmth (qualitative).  
- OS monitor: high CPU, climbing memory, disk activity spikes.  
- Save dialog lingering; recovered-files prompt after crash.  
- Connectivity icon still showing connected / strong signal.

## Measurements that would support diagnosis (commodity)

- Before/during CPU%, memory used, disk active time (OS monitor).  
- Wall-clock duration of a fixed local action under two loads.  
- Quit+reopen persistence checklist.  
- Airplane-mode rule-out when the workload is local.

## Measurements we cannot yet obtain (honest gaps)

- Silicon performance-counter attribution on arbitrary reader devices as a required lab step.  
- Validated EVT thermal curves or battery drain watts for Device Quartet (`PHYSICAL_PENDING`).  
- Universal numeric “good UX” latency budgets for all apps/devices.  
- Proof that gunnchOS device-os alpha digital services equal production OS scheduling on hardware.

## Human consequence

When the contract fails, people lose time, trust, and sometimes work product (unsaved state). They may blame the wrong layer (network, “the app,” themselves), buy unnecessary upgrades, or disable safety features. Teaching the contract restores agency: **inspect before you accuse**.

## Wording rules for prose drafting

- Prefer “within acceptable bounds” over fake thresholds.  
- Label illustrations as illustrative.  
- Never upgrade LAB-CMS-001 classroom observations to fleet-wide measured claims without a measurement bundle.
