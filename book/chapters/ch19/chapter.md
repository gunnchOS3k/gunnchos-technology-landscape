---
status: draft
chapter_id: CH19
chapter_number: 19
title: "NTN and Service Continuity Across Ground, Air, and Space"
author: "Edmund Gunn, Jr."
part: IV
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-PKT-001, LAB-CE06-001]
figures:
  - FIG-CH19-001
  - FIG-CH19-002
  - FIG-CH19-003
---

# Chapter 19 — NTN and Service Continuity Across Ground, Air, and Space

**Status:** `draft` · **Chapter ID:** `CH19`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working full-manuscript draft · human validation pending · not publication-ready

---

## 1. The moment

You are somewhere the usual story breaks.

On a flight, the cabin mode flips and the familiar cellular bars go quiet. In a rural stretch, the map still draws roads while the phone reports no usable service. During an outage, a neighbor’s device still shows “connected” somewhere—but your message will not send. Then a satellite-messaging feature, an emergency-text path, or a marketing banner about space Internet appears. From the seat it feels like a simple question: *do I still have service?*

Underneath, the question is not one switch. It is a path-class change. A **terrestrial network**—ground-based access and core infrastructure—may be unavailable, degraded, or forbidden by policy (for example, airplane radio modes). A **non-terrestrial network (NTN)** path—space or airborne platforms such as satellites or high-altitude systems—may offer a different capability class entirely: sometimes short messages, sometimes constrained data, sometimes broadband-class service in specific products. Marketing language can blur those classes into one glowing icon [@threegpp-ts23501] (CLM-CH19-001; CLM-CH19-004 · **SOURCE_NEEDED** for operator capability-class documents).

This chapter’s governing question:

> When the ground path fails or changes, what actually continues for a human—and how do we refuse to confuse an icon with experience continuity across ground, air, and space?

Part IV already separated Wi-Fi, cellular, packets, and cloud placement. Concept Edition continuity language named the problem without dumping every NTN detail into CE-4/CE-6. Here we deepen **service continuity** as experience continuity across path classes—not as an always-on badge—and we stay humble about deployed capabilities and project evidence.

---

## 2. What you notice

Before vocabulary like *LEO*, *GEO*, or *multi-connectivity*, notice the human contracts you already expect.

You expect “connected” to mean the task you care about can finish—or fail with an honest reason. You expect a messaging-only satellite feature not to behave like home broadband. You expect handovers across networks not to silently drop the draft you were writing. You expect rural and flight stories to be teachable without requiring travel or unauthorized radio experiments. You expect marketing screenshots not to substitute for official capability descriptions.

Those expectations are not decorations. They *are* continuity, from the person’s point of view.

**Service continuity is about experience across changes—not merely keeping an icon lit** [@itu-t-p10-g100; @itu-t-g1011; @threegpp-ts23501] (CLM-CH19-002).

Notice the split timelines. A radio indicator can remain green while an application stalls. A satellite feature can accept a short text while blocking a video call. A coverage map can look complete at city scale while a valley remains a **coverage gap**—a region or time without usable terrestrial service. Optional comparison on devices you already own (no flights required): open a familiar messaging or sync action on Wi-Fi, then switch to cellular or airplane mode and watch how status text, send state, and human-visible progress diverge. Record observations separately from causal guesses. You are practicing continuity literacy, not collecting operator latency numbers.

---

## 3. Exploded ecosystem

A continuity moment is not a single radio. It is a path through cooperating layers. **FIG-CH19-001** is the first-minute map: human task → device → terrestrial and/or NTN path classes → core/service → human-visible outcome. Treat it as **Representative educational architecture**, not a claim that any one operator’s sky looks exactly like the diagram.

### Human

You form intent: send a status to family, keep a document syncing, reach emergency services, finish a class upload. Eyes and ears judge whether the experience continued.

### Device and local stack

Radios, modem firmware, OS connectivity managers, and apps interpret path availability. Icons summarize; they do not measure your task.

### Terrestrial path class

Towers, small cells, backhaul, and mobile core functions implement ground access. Wi-Fi may provide a local on-ramp; cellular may provide a mobile on-ramp; neither is “the Internet,” and neither is automatically identical to an NTN path [@threegpp-ts23501] (CLM-CH19-001).

### Air / space path class (NTN)

Satellites, high-altitude platform systems (HAPS), and related non-ground platforms can extend reach. NTN adds path classes; it does not automatically deliver the same delay, bandwidth, or application behavior as terrestrial 5G service [@threegpp-ts23501] (CLM-CH19-001). Exact NTN specification clause IDs beyond the 5G system-architecture frame remain a sourcing follow-up (see claim footnotes).

### Core, edge, and service placement

Even when a radio path exists, the service you need may live nearby (edge) or far (cloud). Continuity can fail in the radio, the transport path, or the service—CE-6’s connected-but-unusable lesson still applies.

### Operator policy and capability class

What a product *may* do (messaging-only, emergency text, constrained data, broadband-class) is a capability claim. Verify it from official operator or standards documentation before teaching it as fact (CLM-CH19-004 · **SOURCE_NEEDED**). Do not invent product feature matrices in this chapter.

### Evidence boundary (project)

WAIKE accepted `main` hosts a synthetic polar NTN teaching case study under a Graham Land / 7GC path. That fixture is for local teaching validation only. It is **not** field-validated twin evidence. Project NTN demo/twin claims remain **PHYSICAL_PENDING** (CLM-CH19-005) [@src-waike].

---

## 4. Follow the signal

Follow one human-visible action across a path change—without inventing sky telemetry.

1. **Intent forms.** You tap send, sync, or join.
2. **Local stack checks path class.** The device reports terrestrial availability, NTN/satellite feature availability, or neither.
3. **Capability gate.** The active path either supports the required class (for example short message vs bulk upload) or refuses.
4. **Delay and reliability regime.** Propagation and system delays differ by path class. Orbit *classes* (for example low Earth orbit vs geostationary) imply different qualitative delay regimes; **do not invent product latency numbers** here (CLM-CH19-003 · **SOURCE_NEEDED**) [@tanenbaum-bos].
5. **Handover / multi-path behavior.** The stack may stay on one path, fail over, or use more than one path (**multi-path continuity** / multi-connectivity ideas at survey depth).
6. **Human-visible state.** Progress, errors, and drafts either survive or silently break—**FIG-CH19-002** contrasts continuity of experience vs icon-lit status.

### Alternate paths (the honesty rule)

If you cannot observe an NTN radio, you can still practice the continuity method on terrestrial path changes (Wi-Fi ↔ cellular ↔ offline) using commodity devices or fixtures. That is adjacency to **LAB-PKT-001** and **LAB-CE06-001**, not a fake satellite measurement.

### Failure branch without drama

Common honest failures: no usable path for the required capability; path exists but delay/reliability outside task tolerance; handover drops application state; marketing implied broadband while the official class is messaging-only. None of these require inventing orbit milliseconds.

---

## 5. Component cards

### Non-terrestrial network (NTN)

- **Role.** Network components using space or airborne platforms.
- **Plain contract.** Extends path options beyond ground infrastructure.
- **Misread.** “NTN” means automatic full Internet everywhere.
- **Evidence note.** Architecture vocabulary via 5G system references [@threegpp-ts23501]; product claims need official docs (CLM-CH19-001; CLM-CH19-004 · SOURCE_NEEDED).

### Terrestrial network

- **Role.** Ground-based access and core infrastructure.
- **Plain contract.** The everyday cellular/Wi-Fi-adjacent world of towers, backhaul, and local wireless.
- **Misread.** Treating terrestrial and NTN as interchangeable synonyms for “bars.”

### Service continuity

- **Role.** Keeping the human experience working across path/access changes.
- **Plain contract.** Experience continuity ≠ icon continuity [@itu-t-p10-g100; @itu-t-g1011] (CLM-CH19-002).
- **Misread.** A lit satellite glyph proves the user’s task still works.

### Coverage gap

- **Role.** Space/time without usable terrestrial service.
- **Plain contract.** Gaps motivate alternate path classes; they do not specify which capability arrives.
- **Misread.** A map without hatching means no human has ever lost service there.

### Delay regime

- **Role.** Propagation and system delay classes that differ sharply across terrestrial vs orbit classes.
- **Plain contract.** Compare regimes qualitatively; refuse invented product latency tables (CLM-CH19-003 · SOURCE_NEEDED).
- **Misread.** One “satellite latency” number fits all orbits and operators.
- **Figure.** **FIG-CH19-003** may show comparative bars only when labeled illustrative—never as measured product data.

### Multi-path continuity

- **Role.** Using more than one access path to sustain experience.
- **Plain contract.** Extra paths help only if capability, delay, and state survival match the task.
- **Misread.** More radios automatically mean seamless broadband.

---

## 6. Stability contract

Definition retained from the book: a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

Chapter-focused concurrent conditions (qualitative; no invented numeric budgets):

1. **At least one usable path class** is available for the *required* capability (messaging vs broadband-class, and so on).
2. **Delay and reliability** of the active path stay within the task’s tolerance—judged by human-visible completion, not by icon color alone [@itu-t-g1011].
3. **Handover across domains** does not silently drop human-visible state (drafts, sessions, progress).
4. **Capability class matches expectation**—marketing language has been checked against official descriptions (CLM-CH19-004 · SOURCE_NEEDED).

A system can remain *icon-connected* while the human experience has already failed: send pending forever, sync looping, call setup impossible, emergency text succeeding while apps stall. Conversely, a constrained NTN path can preserve a narrow life-critical or messaging experience while “full Internet” remains unavailable. Stability is concurrent conditions—not a single sky emoji.

**Honesty bound for this edition:** Do not invent orbit delay numbers or operator capability matrices. Project NTN twin/demo evidence remains **PHYSICAL_PENDING** (CLM-CH19-005) [@src-waike]. Commodity continuity labs produce *your* observations on *your* devices or fixtures—not a satellite field trial.

---

## 7. Try it

### Continuity inheritance — LAB-PKT-001 and LAB-CE06-001

**Goal.** Practice continuity literacy on path and usability changes you can ethically observe—then extend the same worksheet logic toward public NTN/satellite *feature classification* using official documents only.

**WAIKE alignment note.** WAIKE accepted `main` maps advanced wireless coursework adjacently (`WIRELESS_6G`); it does **not** provide an exact NTN lab ID. Do not invent one. Publication continuity work inherits **LAB-PKT-001** (path/access framing) and **LAB-CE06-001** (connected-but-unusable diagnosis). A future continuity worksheet across CE-4/CE-6/CH19 remains **proposed**, not shipped as a new WAIKE course ID.

**Safety (hard stops).**

- No unauthorized satellite ground-station activity, no unlicensed transmitters, no aircraft-system interference.
- No Device Quartet or specialized RF TX required.
- No travel required; rural/flight stories may use fixtures, public docs, and terrestrial path-change analogs.
- Redact secrets, tokens, precise locations, and classmate PII from portfolio artifacts.

**Routes.**

- **Commodity route (terrestrial continuity analog).** Reproduce a connected-but-unusable or path-change moment on a phone/laptop you already own; follow LAB-CE06-001 / LAB-PKT-001 observation rules.
- **Fixture route.** Use lab fixtures when metered data, travel, or live networks are unavailable.
- **Document-only capability-class route (NTN-facing, no flight).** Pick one public consumer satellite/NTN feature. Using **official operator or standards documentation only**, classify: messaging-only, emergency-limited, constrained data, broadband-class, or “insufficient official evidence.” Record quotes/links; do not invent capabilities (CLM-CH19-004 · SOURCE_NEEDED until docs are pinned per feature).

**Explorer baseline (about 45–60 minutes).**

1. Predict whether your chosen task fails for path absence, delay/reliability, service placement, or capability-class mismatch.
2. Run one terrestrial continuity observation (LAB-PKT-001 or LAB-CE06-001 route) **or** complete the document-only capability-class card.
3. Fill observation-vs-inference columns. Icon state is an observation; “the satellite is 40 ms away” is an inference you are **not** allowed to invent (CLM-CH19-003 · SOURCE_NEEDED).
4. Write a five-sentence teach-back: NTN is an additional path class; continuity is experience; icons are not proof.

**Operator extension.** Compare two official feature descriptions (two products or two modes). Note where marketing pages and support docs disagree; prefer the more specific official capability statement.

**Builder extension.** Produce a one-page continuity checklist: path class → capability class → human-visible state survivors → evidence still needed.

**Engineer extension.** Sketch qualitative delay-regime comparison (terrestrial vs LEO-class vs GEO-class) with **no numeric product claims**; list what primary source would be required to promote CLM-CH19-003 out of SOURCE_NEEDED.

**Researcher extension.** Read the WAIKE synthetic polar NTN case-study boundary: teaching fixture, local validation needed, **PHYSICAL_PENDING** for field twin claims (CLM-CH19-005) [@src-waike]. Write what evidence would be required to change that label—and what still would not be proven.

**Evidence to keep.** Observation-vs-inference table; capability-class card with official-doc citations; scrubbed notes; teach-back paragraph.

---

## 8. Build it

Extend the Try-it routes without turning Part IV into a satellite product catalog.

### Explorer

Build a pocket card: four lines—(1) terrestrial path, (2) NTN path, (3) icon ≠ experience, (4) capability class must be verified.

### Operator

Build a “feature claim” checklist that starts with official docs and ends with “insufficient evidence”—never with a guessed broadband promise.

### Builder

Build a labeled continuity diagram for one task: human → device → path class(es) → service → outcome. Annotate what is observed vs inferred. Optional second diagram: messaging-only vs broadband-class as different contracts on the same sky metaphor.

### Engineer

Build a qualitative delay-regime brief: define LEO-class vs GEO-class as orbit *regimes* affecting propagation scale, cite only sources you actually have, and leave product milliseconds blank pending SOURCE_NEEDED closure (CLM-CH19-003). Pair with 5G system-architecture literacy [@threegpp-ts23501] without collapsing NTN into terrestrial 5G.

### Researcher

Build an evidence plan for promoting CLM-CH19-005: what physical/field measurements, ethics approvals, and replication packages would be required beyond a synthetic teaching fixture [@src-waike]. Explicitly forbid treating simulation screenshots as twin validation.

Educators can facilitate Section 11 teach-backs and keep classrooms on fixture/document routes when travel or RF gear is unavailable.

---

## 9. Secure and include it

### Security

NTN and satellite features expand the trust boundary: new radios, new intermediaries, new failure modes for spoofed status. Prefer official provisioning and user consent. Do not run unauthorized ground-station or uplink experiments as “labs.”

### Privacy

Location, flight paths, and message metadata can become sensitive identifiers. Portfolio artifacts must scrub precise coordinates, account identifiers, and private message content.

### Accessibility

Continuity status must not depend on color-only icons. Provide text equivalents for path/capability state. Document checklists in words so screen-reader users and print users can follow the same method [@wcag22-20241212].

### Equity

Rural gaps, flight constraints, and device/plan pricing shape who receives which capability class. Teach continuity without requiring students to buy satellite plans or travel to polar field sites. Fixtures and official docs are first-class.

### Safety

No interference with aviation systems, no unlicensed transmission, no improvised RF hardware. Continuity literacy is observational and documentary in this chapter.

### Ethics

Do not invent operator capabilities, orbit delay tables, or field-validated NTN twin results. Overclaiming sky coverage is still a form of false evidence. Keep PHYSICAL_PENDING and SOURCE_NEEDED labels visible where they belong.

---

## 10. Career lens

Roles that touch this chapter’s problems (publication career registry IDs where they exist; otherwise descriptive). **No employment guarantees.**

| Layer / concern | Role lens | Owns (example) | Classroom analogue |
|---|---|---|---|
| Radio / NTN path literacy | Wireless engineer (`ROLE-WIRELESS`) | Radio-performance analysis with honest limits | Weak-signal / path-class discussion; no fake drive tests |
| Path & timing diagnosis | Network engineer (`ROLE-NET`) | Packet/latency analysis on observable paths | LAB-PKT-001 timing table on commodity/fixture routes |
| Experience under change | SRE (`ROLE-SRE`) | Service reliability evidence; connected vs usable | LAB-CE06-001 continuity diagnosis |
| Mobile core / architecture | Mobile core engineer (descriptive) | Core functions that survive access changes | Architecture teach-back from TS 23.501 survey depth [@threegpp-ts23501] |
| Space systems | Satellite systems engineer (descriptive) | Orbit/link budgets in real programs | Qualitative regime literacy only here; no invented budgets |
| Policy / spectrum | Policy & spectrum roles (descriptive) | Rules that constrain who may transmit and where | Document-only capability and regulation reading |

Portfolio signal: a scrubbed continuity checklist plus an official-doc capability-class card beats a screenshot of a satellite marketing banner.

---

## 11. Check understanding

1. In one sentence, why is NTN not automatically identical to terrestrial 5G service?
2. What is the difference between an icon staying lit and service continuity?
3. Name two concurrent Stability Contract conditions for a cross-domain continuity moment.
4. Why does this chapter refuse to publish invented LEO/GEO product latency numbers?
5. What evidence class is required before teaching a consumer satellite feature as “broadband”?
6. What does **PHYSICAL_PENDING** mean for the WAIKE polar NTN case study?
7. Which existing labs inherit continuity practice without inventing an NTN flight lab?
8. Teach-back (Explorer): explain to a nontechnical person why a satellite-messaging feature can be valuable without being home Internet.

**Researcher prompt.** What primary sources would close CLM-CH19-003 and CLM-CH19-004, and what still could not be claimed without field measurements?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`), including 3GPP TS 23.501 family architecture vocabulary [@threegpp-ts23501] and ITU-T QoE vocabulary/assessment guidance [@itu-t-p10-g100; @itu-t-g1011]. Project-specific NTN twin status remains **PHYSICAL_PENDING** and is cited via [@src-waike], separately from external literature. Orbit-delay product numbers and operator capability-class documents remain **SOURCE_NEEDED** where marked.

---

## 12. Glossary links


| Term | Plain link |
|---|---|
| Non-terrestrial network (NTN) | Network components using space or airborne platforms |
| Terrestrial network | Ground-based access/core infrastructure |
| Service continuity | Keeping usable experience across path/access changes |
| Coverage gap | Absence of usable terrestrial service in space/time |
| Delay regime | Qualitative delay class tied to path/orbit regime |
| Multi-path continuity | Using more than one access path to sustain experience |
| LEO / GEO (qualitative) | Low Earth orbit vs geostationary orbit *regimes*—not product latency figures |
| Stability contract | Concurrent conditions that keep the experience alive |

Related earlier chapters: packets/Internet path literacy (CH16), Wi-Fi/cellular/5G survey (CH17), spectrum/radio conditions (CH18), CE-4/CE-6 continuity. Related later chapters: sensing and twin honesty (CH20+), publication/operations ethics (Part VI).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured evidence. No fabricated satellite telemetry.

### FIG-CH19-001 — Ground / air / space path classes to a device

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** System map.
- **Reader should notice.** Distinct terrestrial vs NTN path classes feeding one human task.
- **Truth class.** Conceptual / Representative educational architecture.
- **Alt text requirement.** Name human, device, terrestrial path, NTN path, service, outcome; state conceptual truth class.

### FIG-CH19-002 — Continuity vs icon-lit

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Comparative layers.
- **Reader should notice.** Icon can remain lit while human-visible task fails (or narrow messaging succeeds).
- **Truth class.** Conceptual.
- **Alt text requirement.** Contrast icon state vs task outcome; color not sole encoding.

### FIG-CH19-003 — Delay regime comparison (illustrative)

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Illustrative comparative bars.
- **Reader should notice.** Regime classes differ; bars are not product measurements.
- **Truth class.** Illustrative.
- **Alt text requirement.** State illustrative only; forbid reading numbers as operator guarantees; note CLM-CH19-003 SOURCE_NEEDED.

---

## Claim footnotes used in this chapter

| Claim ID | Text (short) | Status |
|---|---|---|
| CLM-CH19-001 | NTN adds non-ground path classes; not automatically identical to terrestrial 5G | SOURCE_IDENTIFIED (`threegpp-ts23501`) |
| CLM-CH19-002 | Service continuity is experience across changes—not merely an icon | SOURCE_IDENTIFIED (`itu-t-p10-g100`, `itu-t-g1011`, `threegpp-ts23501`) |
| CLM-CH19-003 | Satellite delay regimes differ by orbit class; do not invent product latency numbers | **SOURCE_NEEDED** (qualitative teaching only in this draft) |
| CLM-CH19-004 | Marketing satellite connectivity may mean messaging-only or limited modes—verify capability class | **SOURCE_NEEDED** (official operator docs per feature) |
| CLM-CH19-005 | Project NTN twin/demo remains PHYSICAL_PENDING; WAIKE polar NTN case study is synthetic teaching fixture only | **PHYSICAL_PENDING** (`src-waike` @ `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`) |
