---
status: WORKING_DRAFT_COMPLETE
manuscript_review: PENDING_FULL_MANUSCRIPT_REVIEW
publication_readiness: NOT_PUBLICATION_READY
gate_posture: "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING"
human_validation: DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT
chapter_id: CH03
chapter_number: 3
title: "Performance: Why Technology Feels Fast, Slow, Smooth, or Unstable"
author: "Edmund Gunn, Jr."
part: I
concept_edition: false
labs: [LAB-PERF-001, LAB-CMS-001]
figures:
  - FIG-CH03-001
  - FIG-CH03-002
  - FIG-CH03-003
  - FIG-CH03-004
blocked_figures:
  - the blocked CMS measured plate
---

# Chapter 3 — Performance: Why Technology Feels Fast, Slow, Smooth, or Unstable

**Status:** `WORKING_DRAFT_COMPLETE` · **Manuscript review:** `PENDING_FULL_MANUSCRIPT_REVIEW` · **Publication readiness:** `NOT_PUBLICATION_READY`  
**Chapter ID:** `CH03` · **Author:** Edmund Gunn, Jr.  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does not claim Gate 3 PASS)

---

## 1. The moment

You scroll a feed. You scrub a video scrubber. You switch apps. Sometimes motion is continuous enough that your attention stays on the content. Sometimes the same gesture hitches, freezes, then recovers unevenly—even when the network icon still looks fine, or the device is relatively new.

From your seat, the complaint is ordinary language: *fast*, *slow*, *smooth*, *janky*, *unstable*. Those words are not decorations around the product. They *are* the product’s first report card.

Chapter 2 followed one tap through layers and taught an honesty rule: immediate feedback and later content are related timelines, not one magic clock [@w3c-uievents; @mdn-performance]. This chapter stays with the human report card and asks a sharper question:

> What system behaviors make an ordinary experience feel fast, slow, smooth, or unstable—and how can I separate observation from guessed cause without inventing numbers?

We will not invent Device Quartet performance budgets, EVT thermal curves, or fleet-wide SLOs. Numeric hardware claims for those research form factors remain **PHYSICAL_PENDING** (CLM-CH03-004) [@src-hardware-quartet]. Classroom timings you collect later are *your* evidence for *your* conditions—not universal product law (CLM-CH03-005).

---

## 2. What you notice

Before jargon, name the feel.

**Fast** usually means a response arrives soon enough that waiting does not become the story. **Slow** means waiting *is* the story—progress indicators linger, key echoes trail fingers, lists fill late. **Smooth** means motion and updates feel continuous enough that your attention stays on intent. **Unstable** means the same action is sometimes fine and sometimes not: hitch, stall, recovery, surprise.

Those words mix several technical stories. A device can move a lot of data per second (**throughput**) while still feeling unresponsive if the *first* useful response is delayed (**latency**) or if delay wanders unpredictably (**jitter**) [@saltzer-kaashoek; @iso-iec-25010-2023]. A screen can look “busy” while the interactive path is starved. A connectivity icon can look healthy while local contention is the real seat problem [@tanenbaum-bos].

**Perceived performance is a human judgment produced by multiple measurable behaviors—not a single score.**

Notice three traps early:

1. Treating peak throughput (“this is a fast chip / fast link”) as proof of a responsive seat experience.
2. Treating “Wi-Fi connected” as proof that slowness is not local.
3. Treating one lucky run—or one CH02 lab timing—as a universal SLO for every chapter and device (CLM-CH03-005).

Optional comparison on a device you already own: scroll a mostly local document, then scrub a video that must fetch remote segments, then switch apps while several tabs or documents are open. Do not yet claim root cause. Only write what you felt and what visible clues appeared (spinner, hitch, fan sound, warmth, monitor percentages if you open them).

---

## 3. Exploded ecosystem

Feel is not a single object. It is a path through an ecosystem. **FIG-CH03-001** maps everyday feel words onto diagnostic axes: latency, jitter, throughput, stall/hitch, and availability. Read it as orientation, not as a measured scoreboard.

Walk the teaching model used across this book:

> Human experience → system → component → code → network → society

### Human

You intend a continuous action: keep scrolling, keep scrubbing, keep switching. Eyes and hands judge whether the system kept up. Vestibular and cognitive load rise when motion stutters; that is already an accessibility concern, not only an aesthetics note.

### Application and runtime

An app updates state, lays out content, asks for frames, and may start local or remote work. An **event loop** that blocks on heavy work can make a fast network look slow [@whatwg-html; @mdn-performance].

### Operating system

A **scheduler** decides when runnable work gets CPU time [@linux-scheduler; @tanenbaum-bos]. Memory managers reclaim under pressure. Storage stacks complete (or delay) durable writes. The OS mediates; it does not replace the app’s computation.

### Compute and memory hardware

CPU, optional GPU/accelerators, caches, and RAM form a hierarchy with different roles [@patterson-hennessy]. Storage is the ordinary durable home for files—not interchangeable with RAM. Contended bandwidth or a working set that no longer fits can turn “simple” motion into hitch.

### Network (optional)

Packets, queues, loss, and retransmission matter when the action depends on remote bytes. Many feel failures never enter this layer. Teaching that optional branch is part of the honesty rule from Chapter 2.

### Power and thermal policy

Sustained work can reduce available performance to protect the device and stay within energy budgets [@linux-cpu-freq]. Heat and slowdown can be policy, not a mysterious software “bug.”

### Society and equity

Fragile networks, shared school devices, older hardware, and locked-down monitors change what “try it” can mean. Fixture routes exist so diagnosis literacy is not gated on admin rights or high-end laptops.

Device Quartet silhouettes, when shown elsewhere, remain **representative educational architecture** / learning benchmarks—not shipping SKUs and not fabricated timing tables (CLM-CH03-004) [@src-hardware-quartet].

---

## 4. Follow the signal

**FIG-CH03-002** is the causal spine for this chapter:

> Action → work → contention or wait → perceptible hitch or delay → human judgment

Read the numbered story as logic, not as a claim that hardware executes exactly one step at a time with no overlap.

1. **Human action.** Scroll, scrub, switch, save, export.
2. **Input becomes events.** Pointer, keyboard, or assistive path enters software [@w3c-pointerevents].
3. **Interactive work is scheduled.** Threads become runnable; the scheduler allocates time [@linux-scheduler].
4. **Computation and data movement.** Instructions execute; caches and RAM serve a working set [@patterson-hennessy].
5. **Optional storage I/O.** Saves, opens, indexes, or write-back compete for the disk path [@tanenbaum-bos].
6. **Optional network I/O.** Remote bytes are requested; waiting begins if needed [@mdn-resource-timing].
7. **Rendering / composition.** Frames must complete often enough for motion to feel continuous.
8. **Power/thermal feedback.** Governors may reduce clocks under sustained load [@linux-cpu-freq].
9. **Perception.** You experience combined latency, variability, stalls, and progress—not layers in isolation.

### Four diagnostic axes (keep them separate)

| Axis | Plain question | Feel word it often colors |
|---|---|---|
| **Latency** | How long until a useful response? | Fast / slow |
| **Jitter** | How much does that timing wander? | Smooth / unstable |
| **Throughput** | How much work completes per time? | “Powerful” yet still sluggish if latency dominates |
| **Availability / errors** | Did the needed path work at all? | Broken / unreliable (distinct from “merely slow”) |

Quality models for systems and software treat characteristics such as performance efficiency and reliability as related but not identical vocabulary [@iso-iec-25010-2023]. Telecommunications vocabulary likewise separates performance, quality of service, and quality of experience as related families of terms—not one interchangeable slogan [@itu-t-p10-g100]. This chapter uses that separation pedagogically: **do not collapse every complaint into “the network” or “the CPU.”**

**FIG-CH03-003** shows the teaching point: two traces can share a similar *average* latency while one has calm spacing and the other has clusters of long gaps. The second often feels unstable even when a single average looks “fine.” Labels on that plate remain **illustrative**—not measured gunnchOS benchmarks.

**FIG-CH03-004** contrasts local contributors (CPU/memory/storage/scheduler/thermal) with optional network contributors. Use it to ask “which branch has evidence?”—not to declare a villain from habit.

### Local contention with a healthy icon

Local resource contention—CPU time, memory pressure, storage I/O wait, scheduler competition—can produce “slowness” while connectivity still looks fine (CLM-CH03-003) [@tanenbaum-bos]. That is the adjacent vocabulary inherited carefully from Concept Edition CE-3 (which maps primarily to later full-book systems chapters, not as a title twin of CH03). Chapter 3 owns *feel ↔ measure*; CE-3/CH06–CH12 deepen the inside-the-device machine.

---

## 5. Component cards

Component cards answer: What is it? What does it do for the person? What fails when it misbehaves?

### Perceived performance

**Plain definition.** How fast, smooth, and stable the experience feels to a person.

**Experience benefit.** Trust that the system is keeping up with intent.

**Failure symptom.** Frustration, repeated taps, abandoned tasks, wrong-layer blame.

### Latency

**Plain definition.** Time from an action to a perceptible useful response [@saltzer-kaashoek; @mdn-performance].

**Experience benefit.** Waiting does not become the main story.

**Failure symptom.** Spinners dominate; echoes trail; “did it hear me?”

### Jitter

**Plain definition.** Variability in timing; uneven gaps between responses or frames.

**Experience benefit.** Motion and turn-taking feel predictable enough to trust.

**Failure symptom.** Hitching, surging, “sometimes fine, sometimes awful.”

### Throughput

**Plain definition.** How much work completes per unit time [@saltzer-kaashoek; @patterson-hennessy].

**Experience benefit.** Large jobs finish; bulk transfers progress.

**Failure symptom.** Big exports crawl—or, conversely, high throughput with poor interactive latency (“busy but unresponsive”).

### Stall / hitch

**Plain definition.** A visible interruption of expected continuous motion or progress.

**Experience benefit.** Continuity supports comprehension and motor planning.

**Failure symptom.** Frozen frames, queued clicks, beachballs, scrubber jumps.

### Contention

**Plain definition.** Competing work for limited CPU, memory, storage, GPU, or radio budget [@tanenbaum-bos].

**Experience benefit.** Sharing resources fairly enough that interactive paths stay usable.

**Failure symptom.** Everything feels heavy under mild multitasking; monitors show crowded run queues or disk storms.

### Thermal / power limit (qualitative)

**Plain definition.** Energy and heat constraints that can reduce available performance [@linux-cpu-freq].

**Experience benefit.** The device survives sustained work without unsafe heat.

**Failure symptom.** The same action feels slower after prolonged load; fans rise; progress decelerates without a new “bug” appearing in the UI copy.

These cards are a diagnosis toolkit, not a complete bill of materials.

---

## 6. Stability contract

The **Stability Contract** is a signature idea across this book:

> A user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

For Chapter 3’s performance lens, a smooth usable feel may require several conditions at once:

- interactive work becomes runnable soon enough,
- latency to first useful feedback stays within what the person will tolerate for that task,
- timing variability stays calm enough that motion does not feel random,
- needed throughput for the foreground job remains adequate,
- memory and storage paths do not thrash the interactive thread into waits,
- optional network/service dependencies succeed *if* the action needs them,
- rendering completes coherent frames often enough,
- power/thermal policy still permits the needed performance,
- errors remain recoverable instead of silent half-states.

Qualitative wording is intentional. This chapter does **not** mint universal numeric SLOs for all apps and devices. CH02’s latency-budget figure and LAB-TAP-001 timings are method precedent and prototype evidence—not product law for Chapter 3 (CLM-CH03-005).

Three separations matter here:

1. High throughput can coexist with poor interactive latency.
2. Healthy connectivity can coexist with local contention.
3. A polite spinner can coexist with a failed request or a blocked UI thread.

You experience the combined result. Later chapters (including formal QoE/stability synthesis) deepen measurement design; here the contract restores agency: **inspect before you accuse.**

---

## 7. Try it

### LAB-PERF-001 — Make Feel Visible

**Observable question.** Under two load conditions on a device I already own, what wall-clock and commodity observations can I record so that “felt slow / felt smooth” becomes evidence instead of vibes?

**Relationship to other labs.** Chapter 2’s **LAB-TAP-001** traces one tap path. Concept Edition CE-3’s **LAB-CMS-001** makes *local* bottleneck symptoms visible with OS monitors. **LAB-PERF-001** is the publication-owned feel→measure lab for this chapter: same honesty rules, different emphasis (feel words ↔ axes), with LAB-CMS-001 as the preferred deep local-diagnosis neighbor.

**WAIKE alignment note.** WAIKE accepted `main` offers adjacent competencies (observability habits, storage triage, playtest metrics, embedded latency-budget thinking)—not a literal CH03 performance module ID. Do not invent one.

**Prerequisites.** A computer or phone you may use for learning; a modern browser and/or built-in OS monitor; optional local Python.

**Safety.** Do not capture passwords, tokens, private messages, or personal document contents. Prefer synthetic pages and redacted filenames. Mild load only. Stop if the device warns about heat or becomes uncomfortably hot. No rooting, no untrusted “optimizer” tools, no disabling security software.

**Time estimate.** About 45–90 minutes including write-up.

#### Prediction

Before measuring, write which axis you expect to dominate under load: latency, jitter/stalls, throughput limits, or availability/errors—and whether you expect the cause branch to look local, network, or unclear.

#### Route A — Browser feel timeline (baseline)

Use a simple local page or benign demo:

- perform one continuous interaction (scroll a long local page, or repeatedly trigger a local visual update),
- then add a mild second load (extra tabs or a second local task),
- capture what browser performance tools expose (user timestamps, long tasks, resource timing where applicable) [@mdn-performance; @mdn-resource-timing],
- record wall-clock duration for a fixed action count (for example, “time to finish 10 deliberate scrolls”) with a phone timer if needed.

#### Route B — OS monitor neighbor (LAB-CMS-001)

Follow **LAB-CMS-001** Route A or fixture fallback: before/during CPU, memory, and disk snapshots during one controlled local action. Use this when the feel problem appears while connectivity looks fine.

#### Route C — Offline / fixture fallback

If monitors are inaccessible, use LAB-CMS-001 fixtures for local-diagnosis literacy. Treat fixture numbers as **teaching illustrations**, not measurements of your device. a measured CMS monitor plate (still blocked pending qualifying evidence) (measured annotated monitor snapshot) remains **`BLOCKED_EVIDENCE_REQUIRED`**; synthetic fixtures labeled with that ID do **not** unblock the measured figure.

#### Evidence (minimum)

- a feel log (fast/slow/smooth/unstable words + timestamps),
- a two-condition observation table (idle/light vs mild load),
- one scrubbed screenshot, log excerpt, or fixture ID,
- labels: **directly observed** vs **inferred**.

#### Interpretation rules

| Allowed observation | Inference that must be labeled |
|---|---|
| Wall-clock for action X rose from A to B | “Root cause is CPU” |
| Long gaps between frames in a tool | Exact physical display deadline miss without more evidence |
| Resource timing shows waiting on network | “Wi-Fi is broken” without path evidence |
| Device felt warmer | Specific throttle temperature |

#### Limits (say them out loud)

- One run is not a benchmark.
- Software timestamps do not measure every physical stage from muscle to photon.
- Browser instrumentation is not kernel-level truth.
- CH02 / LAB-TAP-001 timings are not universal SLOs for this chapter (CLM-CH03-005).

#### Portfolio output

1. `README.md` (question, method, limits),
2. feel→axis map for your experience,
3. observation table,
4. one evidence artifact,
5. reflection separating observation from inference,
6. teach-back paragraph for a nontechnical person.

---

## 8. Build it

Use the same feel story at the depth that matches your pathway.

### Explorer

Name the feel words you noticed. Point to at least three possible contributing factors (for example: waiting on content, local hitch, thermal slowdown) **without** claiming root cause.

### Operator

Record wall-clock and simple OS/browser observations under two load conditions. Keep observation and inference columns honest. Prefer LAB-PERF-001 Route A plus LAB-CMS-001 when the icon looks fine.

### Builder

Build a labeled **feel → candidate cause** map for one experience. Show local vs optional network branches. Change one variable (fewer tabs, airplane mode for a local-only task, shorter scroll distance) and note what changed.

### Engineer

Separate latency, jitter, throughput, and availability as distinct diagnostic axes for one incident write-up. List next evidence you would need before upgrading a hypothesis to a cause claim.

### Researcher

Propose a small controlled comparison: repetitions, environment controls, a summary statistic, a variability measure, and explicit instrument limits. State what would falsify your leading hypothesis. Do not fabricate significance from a classroom N.

Educators can facilitate misconception probes from Section 11 and use LAB-CMS-001 fixtures when live monitors are inequitable across a classroom.

---

## 9. Secure and include it

### Security

Performance panic is a social-engineering surface. “PC cleaner” and miracle optimizer downloads often market themselves at exactly the symptoms this chapter names. Teach inspection with built-in tools before trust of unknown utilities. Labs must not require disabling security software, loading untrusted kernel modules, or capturing privileged sessions.

### Privacy

Timing logs, monitor screenshots, and portfolio artifacts can leak filenames, account names, thumbnails, and location-correlated habits. Redact. Prefer synthetic workloads. Do not require cloud sync of lab evidence.

### Accessibility

Stutter and lag are accessibility failures for many motor, cognitive, and vestibular profiles—not merely polish defects. Motion is not the only feedback channel: provide text status, keyboard-operable controls, and non-color encodings in figures and lab sheets. Equivalent input paths (keyboard, switch, assistive pointer) must still become schedulable work the interactive path can handle [@wcag22-20241212].

### Equity

Low-cost devices, shared machines, data caps, and locked-down school images are normal learning contexts. “Buy more RAM” is not the moral of the chapter. Diagnosis, workload control, and fixture routes come first. Device Quartet form factors are learning benchmarks, not purchase requirements (CLM-CH03-004).

---

## 10. Career lens

Performance work crosses ownership domains. No table promises employment; roles vary by organization. LAB-PERF-001 and LAB-CMS-001 artifacts resemble early professional evidence in miniature.

| Concern | Example role | Professional artifact | Lab resemblance |
|---|---|---|---|
| Feel language ↔ metrics | UX researcher / HCI practitioner | Study notes separating subjective report from instrument | Feel log + axis labels |
| Interactive latency | Performance engineer | Trace bundle with measured vs inferred spans | Timestamp table with honesty labels |
| Local contention | OS / systems engineer | Scheduler / memory / I/O analysis notes | LAB-CMS-001 observation vs inference columns |
| Runtime health | Application engineer | Main-thread / event-loop profile | Blocked-loop hypothesis with evidence plan |
| Capacity vs speed | SRE / reliability engineer | Error budget and latency percentile discussion | Availability separated from “merely slow” |
| Sustained load | Embedded / power engineer | Thermal/power policy notes (qualitative or measured) | Warmth as labeled inference, not fake °C claims |
| Inclusive performance | Accessibility specialist | Motion/status alternatives review | Keyboard path + text equivalent checks |
| Classroom diagnosis | Educator / lab facilitator | Facilitation sheet with fixture fallback | LAB-CMS-001 facilitation artifacts |

When later chapters deepen QoE, networking, or hardware budgets, keep the same discipline: **evidence scope travels with the sentence.**

---

## 11. Check understanding

Answer with reasoning. Prefer short paragraphs over one-word guesses.

1. Why can a system with high throughput still feel slow at the seat?
2. What is the difference between latency and jitter in everyday feel language?
3. Why is “Wi-Fi connected” insufficient proof that a hitch is a network problem?
4. Give one example where local contention could produce instability while a connectivity icon looks healthy.
5. What evidence would you need before blaming thermal limits—and what must stay labeled inference without sensors?
6. Why are CH02 / LAB-TAP-001 timings not universal product SLOs for this chapter?
7. How should a classroom treat the blocked CMS measured plate while it remains blocked?
8. **Teach-back.** Explain to a family member why “fast chip” and “feels fast” are not the same sentence—without using the words *throughput*, *jitter*, or *scheduler*. Then introduce those three terms one at a time, tying each to something already understood.

Educator note: successful teach-backs show at least two axes and one alternate cause branch (local vs network), not memorized vocabulary lists.

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`), with working Full31 harvest keys aligned to `publication/full31/WORKING_BIBLIOGRAPHY.bib`. Project-specific repository evidence is cited by claim ID where needed and kept distinct from external literature.

Inline citations used in this chapter include @saltzer-kaashoek, @iso-iec-25010-2023, @itu-t-p10-g100, @tanenbaum-bos, @patterson-hennessy, @linux-scheduler, @linux-cpu-freq, @mdn-performance, @mdn-resource-timing, @src-hardware-quartet, and @wcag22-20241212.

Unresolved evidence gaps from the chapter packet (including classic HCI response-time category thresholds pending exact edition binding) are **omitted** from reader prose rather than filled with invented numbers.

## 12. Glossary links

Terms introduced or relied on as formal vocabulary in this chapter should resolve in the living glossary registry. This section lists them for linking—not as a dump of free-standing encyclopedia entries.

| Term | Role in this chapter |
|---|---|
| Perceived performance | How the experience feels to a person |
| Latency | Time to a perceptible useful response |
| Jitter | Variability in timing |
| Throughput | Work completed per time |
| Stall / hitch | Visible break in expected continuity |
| Contention | Competition for limited resources |
| Availability | Whether a needed path works at all |
| Scheduler | OS mechanism allocating CPU time |
| Event loop | Wait-and-dispatch structure in apps |
| RAM | Fast working memory |
| Storage | Durable data holding |
| Frame / rendering | Preparing and presenting visual output |
| Thermal / power limit | Energy/heat policy that can reduce performance |
| Quality of experience (QoE) | Experience-centered quality vocabulary (pointer; deeper later) |
| Stability Contract | Experience depends on hidden conditions staying acceptable |

Deeper entries and “not the same as” warnings live in the glossary network.

---

## Figure references (conceptual plates; accessibility metadata)

All figures below are **conceptual** or **illustrative** unless a future revision cites a dated measurement bundle. SVG production may follow; absence of a rendered file does not authorize invented telemetry. Source preference: editable SVG in the publication repository.

### FIG-CH03-001 — Feel Words to Diagnostic Axes

- **Caption.** Everyday feel words mapped to latency, jitter, throughput, stall/hitch, and availability axes.
- **Alt text.** Diagram linking fast/slow/smooth/unstable language to distinct diagnostic axes; conceptual, not measured.
- **Reading order.** Feel words → axis definitions → reminder that one feel word can involve multiple axes.
- **Status.** Conceptual educational diagram (planned).
- **Source.** Publication-owned original (preproduction intent).

### FIG-CH03-002 — Action to Hitch Causal Flow

- **Caption.** Action → work → contention/wait → perceptible hitch → human judgment.
- **Alt text.** Left-to-right causal flow from human action to perceived hitch with optional local and network wait branches.
- **Reading order.** Follow Section 4 steps; mark optional network and thermal feedback.
- **Status.** Conceptual.
- **Source.** Publication-owned original (preproduction intent).

### FIG-CH03-003 — Same Average, Different Jitter

- **Caption.** Two illustrative timelines with similar average latency and different gap variability.
- **Alt text.** Twin timelines showing calm versus clustered delays; labeled illustrative teaching aid.
- **Status.** Illustrative—not measured gunnchOS benchmarks.
- **Source.** Publication-owned original (preproduction intent).

### FIG-CH03-004 — Local vs Network Contributors to Feel

- **Caption.** Side-by-side local and network contributor map for performance feel without deep network-chapter detail.
- **Alt text.** Comparison plate of local contention domains versus optional network/service domains.
- **Reading order.** Local column complete; then optional network column; then “evidence?” checkpoint.
- **Status.** Conceptual.
- **Source.** Publication-owned original (preproduction intent).

### the blocked CMS measured plate — Annotated commodity monitor snapshot (**BLOCKED**)

- **Status.** `BLOCKED_EVIDENCE_REQUIRED`.
- **Note.** LAB-CMS-001 ships synthetic teaching fixtures that may carry this ID for offline literacy. Those fixtures do **not** unblock a measured figure. Do not present fixture numbers as Device Quartet or fleet evidence.

---

## Claim footnotes used in this chapter

| Claim ID | Approved gist | Status / class |
|---|---|---|
| CLM-CH03-001 | Perceived responsiveness depends on latency and variability, not only peak throughput | SOURCE_IDENTIFIED (general technical) |
| CLM-CH03-002 | Latency, reliability/availability, and throughput are distinct failure/feel axes | SOURCE_IDENTIFIED (general technical) |
| CLM-CH03-003 | Local contention can produce slowness while connectivity looks healthy | SOURCE_IDENTIFIED (general technical) |
| CLM-CH03-004 | Numeric Device Quartet performance budgets remain PHYSICAL_PENDING | PHYSICAL_PENDING (project-specific) |
| CLM-CH03-005 | CH02 / LAB-TAP-001 timings are prototype evidence, not universal product SLOs | SOURCE_IDENTIFIED (publication internal) |

General statements about schedulers, memory hierarchy, and browser timing APIs are treated as general technical knowledge scoped to the cited works. Latency numbers, when shown in learner tables, must carry **illustrative**, **measured**, or **inferred** labels.

---

*End of Chapter 3 working draft manuscript. Pending full-manuscript review. Not publication-ready. Gate 3 remains in progress with reader evidence pending.*
