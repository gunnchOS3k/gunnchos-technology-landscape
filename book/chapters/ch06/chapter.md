---
status: working_draft
chapter_id: CH06
chapter_number: 6
title: "CPU, Instructions, and Parallel Work"
author: "Edmund Gunn, Jr."
part: II
concept_edition: false
inherits_from: [CE-3]
labs: [LAB-CMS-001]
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
gate_note: "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING (no Gate 3 PASS claimed)"
figures:
  - FIG-CH06-001
  - FIG-CH06-002
  - FIG-CH06-003
---

# Chapter 6 — CPU, Instructions, and Parallel Work {#ch06}

**Status:** `working_draft` · **Chapter ID:** `CH06`  
**Author:** Edmund Gunn, Jr.  
**Inheritance:** CE-3 CPU / instruction / parallel slices (not a full OS encyclopedia)  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does **not** claim Gate 3 PASS)

---

## 1. The moment {#ch06-moment}

You open a local app you already know—notes, a photo editor, an IDE, a spreadsheet—while other work is already running. The connectivity icon still looks fine. The window still draws. Scroll still tries. Yet the interface stutters, a save hangs a beat too long, fans spin up, or the chassis warms under your wrists.

From the seat it feels like “the CPU is bad,” or “this computer is dying,” or “something is broken.” Underneath, **instruction streams** are competing for limited processor time. An **operating system scheduler** is deciding who runs next. Some work is busy executing; some work is waiting. Extra cores may help—or may sit idle while a single dependent chain blocks the path your fingers care about.

This chapter stays with that inside-the-device story. It does not re-trace Chapter 2’s one-tap network path. It inherits Concept Edition CE-3’s compute focus and leaves memory hierarchy depth, file durability, and full OS internals for neighboring chapters. The governing question is ordinary and honest:

> When my device feels slow while the network icon looks fine, what is the CPU actually doing—and why doesn’t “more cores” always fix the feeling?

---

## 2. What you notice {#ch06-notice}

Before jargon, notice the human contract you already expect from local compute.

You expect typing and scrolling to stay responsive enough that the machine feels present. You expect a save or export to finish, or to fail in a way you can understand. You expect background downloads, sync, antivirus scans, or other apps not to erase the foreground for minutes without explanation. You expect the device not to become unusably hot for ordinary editing. You expect that a healthy Wi-Fi icon does not guarantee a smooth local experience—because local work was never only a network story.

Those expectations are not decorations. They *are* the product from the person’s point of view.

**Responsiveness is a human perception produced by competing instruction streams under scheduling, memory, storage, and power constraints.**

What you may notice, without opening a monitor yet:

- stuttering scroll or delayed key echoes,
- a spinning cursor while the window still redraws sometimes,
- fan noise or warmth during “simple” actions,
- one app lagging while another still feels snappy,
- recovery after you close heavy background work.

What those symptoms do **not** prove by themselves: a single root cause named “CPU.” High activity and poor feel can travel together or apart. A machine can feel sluggish while average CPU percent looks modest, if the interactive thread keeps missing its turn. It can also show a dramatic CPU spike during work that still finishes cleanly. Chapter 3 taught performance *feel*; here we name the compute machinery behind one family of causes—and practice separating observation from inference.

Optional comparison on almost any computer you already own: open a light text note and scroll. Then open a second heavy document, start a mild export or compile if you have one, and scroll the first note again. The first path often stays calm. The second often reveals contention. Write one sentence about what changed in feel before you look at any graph. That comparison is a teaching experience, not a universal benchmark—and not a Device Quartet EVT result.

---

## 3. Exploded ecosystem {#ch06-ecosystem}

Local lag is not a single object. It is a path through an inside-the-device ecosystem. @fig-ch06-001 is the first-minute map for this chapter: app experience → process/threads → scheduler → CPU cores → optional accelerator. Treat it as **conceptual / Representative educational architecture**—not a claim that any specific manufactured revision looks exactly like the diagram.

![Conceptual map from app experience through process/threads and scheduler to CPU cores and optional accelerator.](../../../figures/architecture/fig-ch06-001-app-to-cores.svg){#fig-ch06-001 fig-cap="App → process/threads → scheduler → cores/accelerator. Conceptual educational map; OS mediates while instructions still execute on hardware."}

The Device Quartet used elsewhere in this series—Student 14.5-inch, Handheld Hybrid, DS-XL Coder, and Edge IO Wearables—are research form factors and learning benchmarks. Physical fabrication and EVT CPU measurements remain **PHYSICAL_PENDING**; do not treat comparison-matrix core counts or clock stories as shipping product facts [@src-hardware-quartet].

Walk the layers in ordinary language.

### Human

You form intent: scroll this page, export this image, save this file. Muscles move. Eyes and hands judge whether the result arrived soon enough to trust.

### Application

Your app holds state and code. When you act, software prepares work: update a document model, render a frame, encode media, search an index. That work will eventually become **instructions**—discrete operations a processor can execute [@patterson-hennessy-riscv].

### Process and threads

The operating system does not usually “become” your app. It creates and manages **processes** and **threads**: abstractions for concurrent work units with their own scheduling identity and (for processes) memory/address-space boundaries [@tanenbaum-bos]. Your UI thread, a background save thread, and a helper process can all be “the app” from the seat while remaining distinct to the OS.

### Scheduler and OS mediation

A **scheduler** decides which runnable thread obtains CPU time next [@tanenbaum-bos; @linux-scheduler]. The OS mediates access to processors, memory, and devices. It provides services. It does **not** replace application computation: your logic still runs as instructions on hardware under that mediation [@tanenbaum-bos].

### CPU cores

A **CPU** fetches, decodes, and executes instructions. Modern packages often expose multiple **cores**—hardware contexts that can progress different instruction streams when work is available [@patterson-hennessy-riscv]. “The CPU is at 90%” in a monitor is a coarse summary, not a biography of every instruction.

### Accelerators (survey depth)

A **GPU** or other **accelerator** can execute specialized parallel workloads—graphics, some media, some ML kernels—while host software and OS/device interfaces still orchestrate submission and sharing [@patterson-hennessy-riscv; @khronos-vulkan-overview]. Accelerators are not mystical second brains; they are optional helpers for suited work.

### Adjacent layers (named, not encyclopedized)

Working **memory**, **storage** I/O, and **power/thermal** policy sit beside compute. They can starve or throttle the same human moment. Chapter 7 and Chapter 9 deepen those layers; CE-3 already warned that local lag with a healthy network icon is a multi-domain hypothesis set, not a single villain.

---

## 4. Follow the signal {#ch06-signal}

Follow one ordinary local action—say, scrolling a document while another export runs—as a logical story. Platforms differ; the teaching sequence is orientation, not brand loyalty.

1. **Intent becomes software work.** A scroll or key event reaches the application’s event path (Chapter 2 named that arrival). The app decides what to recompute or redraw.
2. **Work becomes runnable.** One or more threads become **runnable**: ready to execute if a core is free [@tanenbaum-bos].
3. **Scheduler chooses.** The OS scheduler selects among runnable entities on available cores [@linux-scheduler; @tanenbaum-bos]. Interactive threads can be delayed when contention is high—even if they are “important” from your seat.
4. **Instructions execute.** On a chosen core, the CPU advances the instruction stream: arithmetic, branches, memory references, and calls into libraries or system services [@patterson-hennessy-riscv].
5. **Waits appear.** A thread may stop being runnable while it waits for memory, storage, a lock, or a reply from another thread. Busy and waiting can both feel like “frozen” from the seat.
6. **Optional offload.** Some frames or kernels may be submitted to an accelerator; completion still has to rejoin the UI story [@khronos-vulkan-overview].
7. **Feedback returns.** Pixels update, a progress indicator moves, or the cursor finally stops spinning. Your nervous system judges the combined timeline.

@fig-ch06-002 contrasts a mostly serial dependency chain with work that splits into independent chunks. Extra cores help the second pattern more than the first. The bar lengths are **illustrative** teaching aids—not measured speedups, IPC claims, or Device Quartet EVT results.

![Illustrative timelines comparing a serial dependency chain with parallelizable chunks across cores.](../../../figures/architecture/fig-ch06-002-serial-vs-parallel.svg){#fig-ch06-002 fig-cap="Single-thread vs parallelizable work. Illustrative teaching timelines; not measured benchmarks."}

### Parallelism without fairy tales

Computer organization teaching has long stressed that useful speedup depends on how much work can actually overlap, and on other bottlenecks that remain serial [@patterson-hennessy-riscv]. In plain language for this book:

- **More cores can improve throughput** when independent work is ready.
- **More cores do not guarantee lower latency** for every click, scroll, or save.
- Contention, waiting, thermal limits, and single-threaded critical paths can erase the brochure promise.

A practical seat-test: if one thread must finish step A before step B can start, a second core cannot teleport B into the past. If three photo thumbnails truly need independent decoding, three cores may finish the set sooner—until storage or memory bandwidth becomes the new line at the door. Naming that shift is systems literacy; inventing a percentage speedup without a measurement bundle is not.

That is the CE-3 inheritance this chapter keeps central: parallel hardware is real; universal UX speedup is not. Full-book Chapter 12 will deepen OS policy; Chapter 7 will deepen hierarchy waits. Here we keep the compute promise small enough to inspect.

### Honesty branches

- A UI can redraw while a background export still holds locks or fills disks.
- A monitor can show high CPU % while the interactive thread is mostly waiting.
- Closing a window may stop some work and leave other helper processes running.
- Airplane mode can rule out the network for a *local* workload without proving the CPU is healthy.

---

## 5. Component cards {#ch06-components}

These cards are a first toolkit—not a bill of materials for every SoC.

### Instruction

**Plain definition.** A discrete operation a CPU (or similar processor) can execute.

**Experience benefit.** Software progress becomes physical work on silicon.

**Failure symptom.** Endless busy-work, livelock feelings, or progress that never reaches the UI.

### CPU

**Plain definition.** Hardware that fetches, decodes, and executes instructions.

**Experience benefit.** General application logic can run.

**Failure symptom.** Saturation, contention, or thermal/power limits that shrink available performance [@linux-cpu-freq].

### Process / thread

**Plain definition.** OS abstractions for concurrent work units [@tanenbaum-bos].

**Experience benefit.** Multiple activities can progress without being one single frozen program counter from the person’s point of view.

**Failure symptom.** Too many competing units; a stuck UI thread; unclear which process owns the lag.

### Scheduler

**Plain definition.** OS mechanism that allocates processor time among runnable work [@linux-scheduler; @tanenbaum-bos].

**Experience benefit.** Interactive work can share the machine with background tasks.

**Failure symptom.** Foreground starvation; fair-looking averages that still feel awful in the seat.

### Parallel work

**Plain definition.** Overlapping execution across cores or accelerators when the workload allows [@patterson-hennessy-riscv].

**Experience benefit.** Throughput rises for suited tasks (exports, builds, some renders).

**Failure symptom.** “I bought more cores and my typing still stutters”—often a serial or waiting path.

### Accelerator / GPU (survey)

**Plain definition.** Specialized hardware for some parallel workloads, orchestrated by host software [@patterson-hennessy-riscv; @khronos-vulkan-overview].

**Experience benefit.** Frames, filters, or kernels finish without blocking every CPU core the same way.

**Failure symptom.** Submission stalls, driver waits, or assuming “GPU” means games only.

### CPU-bound vs waiting

**Plain definition.** Busy executing useful instructions versus blocked on memory, I/O, locks, or scheduling.

**Experience benefit.** Diagnosis language that prevents buying the wrong upgrade.

**Failure symptom.** Treating a single CPU % number as a courtroom verdict (**illustrative teaching caution**—see Section 11 and LAB-CMS-001).

---

## 6. Stability contract {#ch06-stability}

The **Stability Contract** is a signature idea across this book:

> A user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

For Chapter 6, a smooth local interactive experience may require all of the following to stay “good enough” at once—qualitative bounds only; no invented numeric budgets:

- interactive threads become runnable and obtain CPU (or needed accelerator) time,
- competing background work stays bounded enough not to erase the foreground,
- needed memory and storage paths do not turn every action into a wait storm (deepened in Chapter 7),
- the scheduler continues to serve the interactive path under contention [@linux-scheduler],
- power/thermal policy still permits adequate performance rather than silently collapsing clocks [@linux-cpu-freq],
- the person can still tell progress from failure.

A device can remain **powered on and connected** while the **human experience has already failed**.

@fig-ch06-003 separates **CPU-bound** patterns from **waiting** patterns as conceptual diagnosis branches. High CPU percent in a monitor is not always proof the CPU is the root cause of poor feel—that caution is an **illustrative teaching claim** for lab practice, not a fleet-wide measured distribution.

![Conceptual comparison of CPU-bound versus waiting symptom checks.](../../../figures/architecture/fig-ch06-003-cpu-bound-vs-waiting.svg){#fig-ch06-003 fig-cap="CPU-bound vs waiting-on-I/O symptoms. Conceptual diagnosis aid for observation vs inference."}

Three separations matter here:

1. **Busy executing** versus **busy waiting** can look similar in the seat.
2. **More cores** versus **more useful parallel work** are different purchases.
3. **Healthy network icon** versus **healthy local Stability Contract** are different stories.

Commodity observations you collect in **LAB-CMS-001** are *your* evidence for *your* device and session—not universal EVT curves, and not Gate 3 reader validation.

---

## 7. Try it {#ch06-try}

### LAB-CMS-001 — Make Local Slowness Visible

**Observable question.** When a familiar local app feels slow but the connectivity icon looks fine, what evidence can I gather—using only commodity tools—to separate **CPU**, **memory**, **storage**, and **scheduling/thermal** hypotheses?

This chapter’s Try It **inherits and links** the publication-owned CE-3 lab rather than inventing a duplicate CPU-focused lab package. Follow the full lab packet at `labs/LAB-CMS-001/` (README, routes, fixtures, portfolio templates). Focus your write-up on the **CPU / scheduler / parallel-work** columns of the diagnosis; neighboring chapters reuse the same lab for memory and storage emphasis.

**WAIKE alignment note.** WAIKE accepted `main` (audit SHA recorded in the CH06 packet) hosts adjacent labs on observability and “who runs when,” but there is **no** exact WAIKE module ID for this publication lab. Do not mint one.

**Prerequisites.** A computer you may use for learning; built-in OS monitor (Task Manager / Activity Monitor / `top` or equivalent); a familiar local app.

**Safety.**

- Do not capture personal document contents; redact filenames before sharing.
- Do not install “optimizer” tools, disable security software, or load kernel modules.
- Use **mild** load only. **Stop** if the device warns about heat or becomes uncomfortably hot.
- No Device Quartet hardware is required. No invented EVT numbers.

**Time estimate.** About 45 minutes for Explorer + Operator baseline.

#### Prediction

Before measuring, write which hidden part you expect to dominate during your controlled action: CPU activity, memory pressure, storage I/O, or scheduling/thermal contention.

#### Route A — Commodity OS monitor (baseline)

1. Record **before** CPU, memory, and disk/storage activity.
2. Perform one controlled local action (open a medium document, scroll, or save).
3. Record **during** readings and wall-clock feel.
4. Fill observation vs inference columns in the lab portfolio table.

#### Route B — Safe CLI snapshot (optional)

```bash
python3 labs/LAB-CMS-001/local_app/safe_snapshot.py
```

Read-only sampling where the OS exposes coarse stats. If a metric is unavailable, the script reports `unavailable`—never invent hardware claims.

#### Route C — Fixture fallback

Use `labs/LAB-CMS-001/fixtures/` when monitors are inaccessible or you must avoid personal screenshots. Fixtures teach concepts; they are not claims about your personal device.

#### Evidence (minimum)

- observation table,
- two snapshots or fixture IDs with timestamps,
- teach-back: “OS schedules; apps still compute,” plus one sentence on when more cores might not help.

#### Interpretation labels

| Observation (allowed) | Inference (must label) |
|---|---|
| CPU % rose from A to B | “CPU-bound root cause” |
| Fans spun; device felt warmer | “Thermal throttle at X °C” |
| Scroll stuttered under extra load | “Need N more cores” |

#### Limits (say them out loud)

- OS monitors are coarse; they are not silicon performance-counter labs.
- One run is not a benchmark.
- This lab does not close Gate 3 and does not validate Device Quartet EVT CPU claims (**PHYSICAL_PENDING**).

---

## 8. Build it {#ch06-build}

Use the same local-lag story at the depth that matches your pathway. Prefer commodity tools and LAB-CMS-001 artifacts.

### Explorer

Draw @fig-ch06-001 from memory with three labels: process/thread, scheduler, CPU. Teach a nontechnical person: “The OS decides who runs; the app’s work still happens as instructions.”

### Operator

Capture before/during monitor snapshots under idle vs mild load. Mark each row observation or inference. Note whether connectivity looked fine the whole time.

### Builder

Change **one** variable (extra documents, a background export, fewer tabs). Re-run the observation table. Produce a process map: which processes/threads appeared, which core activity moved, what you did *not* measure.

### Engineer

Order a diagnosis plan: connectivity rule-out (if the workload is local) → CPU activity → memory → disk → qualitative thermal/power. State what additional evidence would be required before claiming causation. Distinguish CPU-bound from waiting using @fig-ch06-003 language without inventing counter values.

### Researcher

Propose a controlled load comparison: hypothesis, variables, planned runs, confounders (thermal state, battery mode, other processes), and uncertainty. Report that Device Quartet physical CPU claims remain **PHYSICAL_PENDING** [@src-hardware-quartet]. Do not invent IPC, GHz product claims, or Gate 3 PASS language.

Educators can facilitate misconception probes from Section 11 and use LAB-CMS-001 fixtures for learners without admin rights.

---

## 9. Secure and include it {#ch06-secure-include}

### Security

Process isolation is an intent you can already name at survey depth: separate processes limit how much damage one buggy or malicious program can do to another’s memory and credentials [@tanenbaum-bos]. Scheduling and privilege boundaries are part of that story. This chapter does not teach exploitation—only the literacy that “apps share a CPU” is not the same claim as “apps share all secrets.”

### Privacy

Monitor screenshots can leak filenames, thumbnails, account names, and open document titles. Redact before sharing. Prefer fixtures when portfolio evidence must leave the device. LAB-CMS-001 forbids capturing personal document contents as a requirement.

### Accessibility

Activity visualizations and color-coded monitor graphs are not equally readable. Prefer labeled columns, patterns, and text tables. Keyboard-reachable OS monitors matter; fixture transcripts exist when GUIs are hostile. Dictate observation tables if needed. Do not make “see the red spike” the only teaching channel—@fig-ch06-001 through @fig-ch06-003 encode meaning with shape, order, and stroke pattern as well as text.

### Equity

Not every learner has a new multi-core laptop, admin rights, or a quiet thermal environment. Commodity routes and offline fixtures are the baseline. Device Quartet form factors are learning analogies here, not admission tickets [@src-hardware-quartet]. Avoid shaming older hardware; teach diagnosis that works with the machine in front of you.

Shared family or school machines raise another equity edge: “just open Activity Monitor” may require permissions a learner does not hold. Fixture transcripts and verbal observation tables keep the pathway open without forcing privilege escalation. The Stability Contract fails for people first; pedagogy should not add a second failure by assuming identical tools.

---

## 10. Career lens {#ch06-career}

Literacy from this chapter shows up in several neighboring roles—without employment promises:

- **Performance engineering / SRE-adjacent local diagnosis** — separate CPU-bound from waiting; treat monitors as evidence, not folklore.
- **Operating systems and embedded** — processes, threads, schedulers, and interrupt-time vs process-time thinking.
- **Compiler-lite literacy** — instructions and parallelizable work as something compilers and runtimes try to expose to hardware [@patterson-hennessy-riscv].
- **Graphics / media systems** — when accelerators help and when host orchestration still dominates [@khronos-vulkan-overview].
- **Educator / mentor** — teach observation vs inference so people stop buying the wrong upgrade story.

Day-one habits transfer across those roles: write a prediction before you open a monitor; label every causal sentence; refuse product-brochure numbers without a method. Power and frequency scaling policies can shrink available performance to protect the device [@linux-cpu-freq]—so “the CPU got worse overnight” sometimes means policy and heat, not a mysterious hardware betrayal.

Career growth here means better questions: “Is this runnable work, waiting, or thermal policy?”—not a guaranteed job title.

---

## 11. Check understanding {#ch06-check}

### Misconception probes

1. **“More CPU cores always make everything faster.”**  
   Counter: useful overlap and non-CPU bottlenecks decide; serial and waiting paths remain [@patterson-hennessy-riscv].

2. **“The operating system runs my app’s logic for me.”**  
   Counter: the OS schedules and mediates; instructions still execute on processors [@tanenbaum-bos].

3. **“If Wi-Fi is connected, lag must be the network.”**  
   Counter: local contention can fail the Stability Contract while the icon stays polite (LAB-CMS-001 hypothesis set; illustrative until *you* measure).

4. **“High CPU % always means the CPU is the root cause.”**  
   Counter: waiting, sampling artifacts, and mixed threads confuse percent alone—label inferences (illustrative teaching caution).

5. **“GPUs only matter for games.”**  
   Counter: accelerators appear in UI composition, media, and other parallel kernels [@patterson-hennessy-riscv].

6. **“Device Quartet core counts are measured shipping specs.”**  
   Counter: research form factors; physical EVT remains **PHYSICAL_PENDING** [@src-hardware-quartet].

### Teach-back (say it out loud)

> Programs become instruction streams. The CPU executes them. The OS decides who runs when. Extra cores help when work can overlap usefully. A healthy network icon does not prove local compute is fine.

### Pathway self-check

| Pathway | You can… |
|---|---|
| Explorer | Name instruction, CPU, process/thread, scheduler in one local lag story. |
| Operator | Capture before/during CPU activity and separate observation from inference. |
| Builder | Map one experience to process/threads/CPU (optional accelerator) without claiming root cause. |
| Engineer | Distinguish CPU-bound vs waiting; explain why more cores are not universal speedups. |
| Researcher | Propose a controlled load comparison; report uncertainty; avoid invented IPC/GHz claims. |

---

## References {#ch06-references}

Inline citations used in this chapter include @tanenbaum-bos, @patterson-hennessy-riscv, @linux-scheduler, @linux-cpu-freq, @khronos-vulkan-overview, and @src-hardware-quartet.

CE-3 preproduction packets (`publication/preproduction/ce-03/`) supply the inherited claim and stability wording this chapter adapts. Full bibliography entries live in the active Quarto project bibliography (including `publication/full31/WORKING_BIBLIOGRAPHY.bib`).

---

## 12. Glossary links {#ch06-glossary}


| Term | Plain link |
|---|---|
| instruction | Discrete CPU-executable operation |
| CPU | Hardware that executes instructions |
| process / thread | OS abstractions for concurrent work |
| scheduler | OS decision of what runs when |
| parallel work | Overlapping execution when the workload allows |
| accelerator | Specialized hardware for some workloads |
| CPU-bound vs waiting | Busy executing vs blocked on other resources |
| Stability Contract | Experience depends on hidden conditions staying acceptable |

See also Chapter 2 (process/thread/scheduler naming), Chapter 3 (performance feel), Chapter 7 (memory/storage), Chapter 9 (power/thermal), and Chapter 12 (OS depth).

---

## Figure references (embedded above; accessibility metadata) {#ch06-figure-refs}

### FIG-CH06-001 — App → process/threads → scheduler → cores/accelerator

- **File:** `figures/architecture/fig-ch06-001-app-to-cores.svg`
- **Truth:** conceptual
- **A11y:** `figures/preproduction/accessibility/fig-ch06-001.yaml`

### FIG-CH06-002 — Single-thread vs parallelizable work

- **File:** `figures/architecture/fig-ch06-002-serial-vs-parallel.svg`
- **Truth:** illustrative
- **A11y:** `figures/preproduction/accessibility/fig-ch06-002.yaml`

### FIG-CH06-003 — CPU-bound vs waiting-on-I/O symptoms

- **File:** `figures/architecture/fig-ch06-003-cpu-bound-vs-waiting.svg`
- **Truth:** conceptual
- **A11y:** `figures/preproduction/accessibility/fig-ch06-003.yaml`

Related CE-3 maps (optional cross-read, not required embeds): `figures/preproduction/ce-03/fig-ce3-001.svg`, `fig-ce3-003.svg`.

---

## Claim footnotes used in this chapter {#ch06-claims}

| Claim | Status handling in prose |
|---|---|
| CLM-CH06-001 — apps execute as instructions under OS mediation | Taught with @tanenbaum-bos (and CE-3 CLM-CE3-001 inheritance) |
| CLM-CH06-002 — more cores help only when work parallelizes usefully | Taught via CE-3 CLM-CE3-005 inheritance with @patterson-hennessy-riscv (no invented sources) |
| CLM-CH06-003 — high CPU % ≠ automatic root cause | Framed **illustrative** + LAB-CMS-001 observation/inference practice |
| CLM-CH06-004 — Quartet CPU/core EVT claims | **PHYSICAL_PENDING** with @src-hardware-quartet |

**Explicit non-claims:** Gate 3 PASS; measured Device Quartet CPU EVT; invented IPC/GHz product numbers; a minted WAIKE CPU lab ID as if published.
