---
status: draft
chapter_id: CH22
chapter_number: 22
title: "Edge AI, Sensors, and Embodied Interaction"
author: "Edmund Gunn, Jr."
part: V
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-TRUST-001]
figures:
  - FIG-CH22-001
  - FIG-CH22-002
  - FIG-CH22-003
---

# Chapter 22 — Edge AI, Sensors, and Embodied Interaction

**Status:** `draft` · **Chapter ID:** `CH22`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working full-manuscript draft · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does **not** claim Gate 3 PASS; fixtures and illustrative budgets are teaching infrastructure, not human reader evidence).

Part V opens the intelligence arc. Chapter 21 names data, models, and generative outputs. This chapter asks what changes when sensing and inference move *near the body*—on a phone, a laptop, or a wearable learning form factor—so a gesture, glance, or haptic cue can close a loop without waiting on a distant API. Concept Edition CE-5 already framed local-vs-cloud latency and privacy tradeoffs; here we deepen **embodied interaction** without claiming shipping Device Quartet AI performance.

---

## 1. The moment

You raise a hand, glance at a camera preview, or feel a short haptic pulse meant to confirm an assistive action. Sometimes the feedback arrives while you are still mid-gesture—offline, private, immediate. Sometimes nothing happens: the preview is black because a permission was denied; the model stalls while the device thermally throttles; a sleeve occludes the sensor; the cloud path is unreachable and there is no honest local fallback.

From the seat: either the body and the machine felt *together*, or the loop broke in a way a green “AI ready” badge cannot explain.

Underneath, the question is not “did the model understand me?” It is a path: physical signal → features → on-device or edge inference → actuator or UI feedback under human timing [@goodfellow_deep_learning] (CLM-CH22-001). Running inference near the sensor can reduce round-trip dependency compared with remote APIs—at the cost of device resource budgets. That is a systems tradeoff, not a product FPS or milliwatt claim for Edge IO Wearables.

This chapter’s governing question:

> When sensing plus on-device inference tries to close an embodied loop, which concurrent conditions keep the experience alive—and which privacy, budget, and fallback failures make the body and the machine fall out of sync?

---

## 2. What you notice

Before vocabulary like *quantization*, *NPU*, or *sensor fusion*, notice the human contracts you already expect.

You expect a gesture-triggered assist to work offline when the network is gone—or to fail with an honest reason. You expect a camera or microphone prompt to mean something: consent before continuous capture, not silent recording of classmates [@w3c-mediacapture-streams-20251009]. You expect a haptic or spoken cue soon enough that it still feels like a reply to *this* motion. You expect occlusion (hand over lens, sleeve over IMU), low light, and battery saver modes to produce recognizable symptoms—not mysterious “AI broken” blame. You expect portfolio screenshots not to contain other people’s faces, voices, or private spaces.

Those expectations *are* embodied interaction literacy.

**Embodied features fail as human timing and consent problems before they fail as model trivia.**

Optional commodity notice (no specialized wearables): on a device you already own, open a familiar camera or motion-assisted feature you are allowed to use. Write two columns—*permission/status shown* and *body-visible outcome*—then stop. If live capture is unsafe, unethical, or unavailable, use a fixture route (Section 7) and mark rows `fixture`. You are practicing observation vs inference, not collecting Device Quartet benchmarks.

---

## 3. Exploded ecosystem

An embodied assist is not “the model.” It is a path through cooperating layers. **FIG-CH22-001** (planned conceptual embed) is the first-minute map: sense → feature → edge inference → haptic/UI feedback. Treat it as **Representative educational architecture**, not a wiring diagram for any shipping wearable SKU.

### Human and context

Intent, attention, posture, clothing, and lighting set what “usable sensing” means *now*. A classroom demos gesture and a private assistive cue do not share one universal latency tolerance.

### Sensors and local capture path

Cameras, microphones, IMUs, touch, and proximity convert physical events into samples. CH08 already taught sensor pipelines; here we *use* them as inputs to an embodied loop, not re-teach the catalog. On the web platform, camera and microphone access is mediated capture under a permission model—not unmediated truth about the room [@w3c-mediacapture-streams-20251009].

### Features and on-device / edge inference

Raw samples become features; a model’s parameters are applied at inference time to produce outputs—an accessible systems framing, not a claim that networks “understand” intent [@goodfellow_deep_learning] (CLM-CH22-001). Placement may be fully on-device, on a nearby edge node, or hybrid. CE-5’s local-vs-cloud contrast still applies: locality can improve latency and shrink what leaves the device, while cloud offload can buy capacity at privacy and round-trip cost (illustrative teaching contrast unless a measurement bundle is attached).

### Actuators, haptics, and UI feedback

Motors, speakers, displays, and assistive announcements close the loop. Feedback that arrives after the gesture’s meaning has passed is a failed embodiment even if the logits were correct.

### Budgets and thermal/power managers

Latency, energy, memory, and heat bound what the local path may do. **FIG-CH22-002** (illustrative budget bands) may show qualitative bands only when labeled illustrative—never as measured Edge IO Wearables EVT.

### Policy, identity, and privacy boundary

Continuous sensing expands what may be exposed beyond the visible UI: faces in the background, overheard speech, precise motion patterns. Organizational AI risk language such as NIST AI RMF remains voluntary guidance for trustworthy-system characteristics—not a certificate that “edge AI is safe” [@nist_ai_rmf_100_1].

### Evidence boundary (Device Quartet)

Edge IO Wearables appear here as the primary Device Quartet *learning* form factor for embodied edge themes. Physical fabrication and measured AI/sensing benchmarks remain **PHYSICAL_PENDING** (CLM-CH22-002) [@src-hardware-quartet]. **FIG-CH22-003** must carry that badge whenever the Wearables context is drawn.

---

## 4. Follow the signal

Follow one human-visible embodied action without inventing wearable telemetry.

1. **Intent forms.** You gesture, glance, speak a wake phrase you are allowed to use, or wait for a haptic confirm.
2. **Permission / consent gate.** The stack asks—or should ask—whether this app may use the sensor *now* [@w3c-mediacapture-streams-20251009].
3. **Sense.** Samples arrive with noise, occlusion, or adequate quality.
4. **Feature.** Local code turns samples into a representation the model expects.
5. **Edge / on-device inference.** Parameters apply near the device, reducing remote round-trip dependency when the local budget holds [@goodfellow_deep_learning] (CLM-CH22-001).
6. **Actuate / feedback.** Haptic, audio, or UI state answers under human timing—**FIG-CH22-001**.
7. **Fallback.** If the local model is unavailable, thermally throttled, or out of memory, an honest degraded path (cloud offload with disclosure, offline refusal, or simpler heuristic) must exist—or the experience fails openly.

### Alternate paths (the honesty rule)

If you lack a wearable or NPU, you can still practice the loop on commodity camera/mic permission flows, fixture occlusion worksheets, and CE-5 **LAB-TRUST-001** local-vs-remote path comparison. That is adjacency—not a fake Edge IO Wearables measurement (CLM-CH22-002) [@src-hardware-quartet].

### Failure branch without drama

Common honest failures: permission denied; sensor occluded; thermal/power budget exceeded; model file missing; cloud fallback unreachable without disclosure; feedback too late for the gesture. None of these require inventing milliwatts or FPS.

---

## 5. Component cards

### Embodied sensing

- **Role.** Capturing physical-world signals for interaction.
- **Plain contract.** Turns motion, light, sound, or touch into samples the rest of the loop can use.
- **Misread.** Treating the sensor reading as ground truth about people or intent.
- **Failure symptoms.** Black preview, silent mic, flat IMU under occlusion, noisy samples in motion.

### Edge / on-device inference

- **Role.** Running models near the sensor or actuator.
- **Plain contract.** Can reduce remote round-trip dependency when device budgets allow [@goodfellow_deep_learning] (CLM-CH22-001).
- **Misread.** “On-device” means unlimited intelligence with zero energy cost.
- **Failure symptoms.** Stalls, thermal throttle, out-of-memory, missing model artifact.

### Edge resource budget

- **Role.** Latency, energy, memory, and thermal limits that bound experience.
- **Plain contract.** Embodiment lives inside a budget envelope—**FIG-CH22-002** (illustrative).
- **Misread.** One universal millisecond table fits every assistive cue.
- **Evidence note.** Measured Device Quartet budgets remain **PHYSICAL_PENDING** (CLM-CH22-002).

### Embodied interaction loop

- **Role.** Sense → infer → actuate/feedback under human timing.
- **Plain contract.** Correct logits with late haptics still feel broken.
- **Misread.** Collapsing the loop into “the AI decided.”

### Sensing privacy boundary

- **Role.** What continuous capture may expose beyond the visible UI.
- **Plain contract.** Background faces, overheard speech, and motion patterns can leave the intended subject.
- **Misread.** A local model automatically makes capture ethical.
- **Citation posture.** Concrete IMU/camera privacy *standards* selection for this chapter remains unresolved; this draft teaches boundary literacy and platform permission mediation without inventing ISO/IEEE designations. Claim CLM-CH22-004 is **omitted** (SOURCE_NEEDED).

### Edge / cloud fallback

- **Role.** Degraded path when local inference cannot complete.
- **Plain contract.** Disclose offload; refuse silently inventing success.
- **Misread.** Fallback is free capacity with identical privacy.

---

## 6. Stability contract

Definition retained from the book: a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

Chapter-focused concurrent conditions (qualitative; no invented numeric Device Quartet budgets):

1. **Sensor signal quality** stays within usable bounds (occlusion, lighting, contact).
2. **On-device compute / thermal / power budget** can finish inference in time for the gesture.
3. **Permission and privacy boundary** for continuous sensing remains respected—consent before capture; no unauthorized recording of others [@w3c-mediacapture-streams-20251009].
4. **Haptic / UI feedback latency** remains acceptable for embodiment (human timing, not logo timing).
5. **Fallback** exists when the edge model is unavailable—cloud with disclosure, offline refusal, or simpler local heuristic.

A device can remain “AI enabled” in settings while the embodied experience has already failed: permission denied, model thermally stalled, haptic late, or cloud path silently substituted without consent. Stability is concurrent conditions—not a single neural badge.

**Honesty bound for this edition:** Do not invent Edge IO Wearables FPS, milliwatts, or fusion accuracy. Physical AI/sensing evidence remains **PHYSICAL_PENDING** (CLM-CH22-002) [@src-hardware-quartet]. Commodity and fixture labs produce *your* observations—not shipping-product EVT, and not Gate 3 validation.

---

## 7. Try it

### Local-path adjacency — LAB-TRUST-001

**Goal.** Rehearse locality, privacy exposure, and consent using the publication-owned CE-5 lab, then extend the same observation discipline toward embodied sensing *without* unauthorized capture.

**WAIKE alignment note.** WAIKE accepted `main` maps edge-budget and embedded latency labs adjacently (`AI_ML_EDGE`, `lab_quantize_budget`, `EMBEDDED_PROTOTYPING`, catalog `edge_ai_embedded`). Those are competency neighbors—not CH22 module IDs (CLM-CH22-003) [@src-waike]. Do not invent `edge_ai_ch22` or claim LAB-TRUST-001 is a WAIKE course ID.

**Safety (hard stops).**

- No unauthorized camera/mic capture of other people, classrooms, or private spaces.
- No covert recording, no credential harvesting, no exploit steps, no keyloggers or clipboard monitors.
- Use only prompts and fixtures that contain non-sensitive content; never paste secrets, health records, or private messages.
- Redact faces, voices, account IDs, and precise locations before portfolio share.
- No Device Quartet hardware required; no invented wearable measurements.

**Routes.**

- **LAB-TRUST-001 commodity/fixture route.** Complete Route L vs Route C comparison and one consent/trust card per that lab’s contract (browser, local simulator, or supplied fixtures). Mark live cloud attempts optional; fixtures are first-class for equity.
- **Proposed sensing worksheet (`LAB-CH22-SENSE-001` — proposed, not a shipped WAIKE ID).** Using *your own* device or a still-image/fixture only: (1) record the permission dialog outcome (allow / deny / not prompted); (2) simulate occlusion with a lens cover or fixture note; (3) write observation-vs-inference rows for “feature unavailable.” Do **not** aim the camera at other people.

**Explorer baseline (about 45–60 minutes).**

1. Predict which Stability Contract bound breaks first under denial, occlusion, or offline mode.
2. Run LAB-TRUST-001 local vs remote comparison **or** the proposed sensing permission/occlusion card.
3. Fill observation-vs-inference columns. “Permission denied” is an observation; “the NPU is 3 TOPS” is an inference you are **not** allowed to invent here.
4. Write a five-sentence teach-back: sense → feature → edge infer → feedback; privacy boundary; PHYSICAL_PENDING for Wearables.

**Operator extension.** Compare symptoms: permission deny vs occlusion vs airplane mode. Note which UI text is honest.

**Builder extension.** Sketch a privacy-preserving sampling config for a *toy* gesture detector: sample rate intent, on-device-only checkbox, retention “discard after inference,” and an explicit “no cloud upload” line. Fixture-only is fine.

**Engineer extension.** Draft a qualitative edge budget worksheet (latency / energy / memory / thermal) with blank measured cells labeled **PHYSICAL_PENDING** for Quartet hardware (CLM-CH22-002). Cite CE-5 illustrative local-vs-cloud contrast as teaching-only unless you attach your own measurements.

**Researcher extension.** Propose a measurement plan that would be required to promote Wearables AI/sensing claims out of PHYSICAL_PENDING: instruments, ethics/consent protocol, stop criteria, and what still would not be proven by a classroom n=1 [@src-hardware-quartet]. Reference WAIKE adjacent labs only as curriculum neighbors (CLM-CH22-003) [@src-waike].

**Evidence to keep.** Scrubbed observation table; consent/trust card; teach-back paragraph; budget worksheet with honest blanks.

---

## 8. Build it

Extend Try-it without turning Part V into a wearable product catalog.

### Explorer

Build a pocket card: four lines—(1) sense, (2) on-device infer, (3) feedback under human timing, (4) permission before capture.

### Operator

Build a symptom card: permission / occlusion / thermal / offline / late haptic—each with one human-visible clue and one next check.

### Builder

Build a labeled loop diagram for one assistive action: human → sensor → feature → edge model → actuator. Annotate what is observed vs inferred. Optional second diagram: local-only vs disclosed cloud fallback.

### Engineer

Build an edge budget brief: define qualitative bands, list what primary MCU-NN or official edge-ML documentation would be required to deepen `edge_ml_sys_refs` (still SOURCE_NEEDED for promotion), and leave product milliwatts blank [@goodfellow_deep_learning].

### Researcher

Build an evidence plan for CLM-CH22-002: fabrication status, ethics for continuous sensing studies, replication package, and explicit forbid on treating concept renders as EVT [@src-hardware-quartet]. Separately note that sensing-privacy standards promotion (omitted CLM-CH22-004) still needs primary designation—do not invent ISO numbers.

Educators can facilitate Section 11 teach-backs and keep classrooms on fixture / self-capture-only / no-camera routes whenever shared spaces make live sensing unsafe.

---

## 9. Secure and include it

### Security

Edge models and sensor daemons expand the trust boundary: new binaries, new permissions, new failure modes for spoofed “local success.” Prefer least privilege and fail-safe defaults in design language; keep this chapter at concepts and UX symptoms—no offensive capture tooling [@nist_ai_rmf_100_1].

### Privacy

Continuous sensing is a privacy surface. Local inference reduces some egress but does not erase on-device retention risk. Portfolio artifacts must scrub bystander faces, voices, and precise locations. Unauthorized capture of others is out of scope for every lab route.

### Accessibility

Embodied feedback must not depend on vision-only or color-only cues. Provide haptic and text alternatives; describe permission and occlusion states in words so screen-reader and print users follow the same method [@wcag22-20241212].

### Equity

Not every learner owns a wearable, NPU laptop, or quiet lab. Commodity phones, fixture transcripts, and offline worksheets are first-class. Edge IO Wearables are learning context with **PHYSICAL_PENDING** status—not an admission ticket [@src-hardware-quartet].

### Safety

No covert recording, no interfering with others’ devices, no improvised body-worn electrical experiments in this chapter’s labs. Embodied literacy is observational, consensual, and fixture-friendly.

### Ethics

Do not invent Wearables AI benchmarks, fake privacy-standard citations, or Gate 3 PASS language. Overclaiming on-device magic is still a form of false evidence. Keep PHYSICAL_PENDING and omitted SOURCE_NEEDED labels visible where they belong.

---

## 10. Career lens

Roles that touch this chapter’s problems. **No employment guarantees.**

| Layer / concern | Role lens | Portfolio evidence (classroom analogue) |
|---|---|---|
| On-device / edge ML | Embedded / edge ML engineer | Edge budget worksheet with honest blanks; LAB-TRUST-001 locality card |
| Sensing systems | Sensor systems engineer | Occlusion / permission / noise symptom card (self or fixture only) |
| Human factors / safety | Safety / HF engineer | Embodied timing risk note—no product claims |
| Privacy engineering | Privacy engineer (descriptive) | Consent card + retention “discard after inference” sketch |
| Responsible AI | Trustworthy-AI / GRC adjacency | NIST AI RMF-informed risk note for continuous sensing [@nist_ai_rmf_100_1] |
| Accessibility | Accessibility specialist | Non-visual feedback checklist [@wcag22-20241212] |

Portfolio signal: a scrubbed permission/occlusion card plus an honest PHYSICAL_PENDING measurement plan beats a marketing screenshot of a glowing wearable.

---

## 11. Check understanding

1. In one sentence, why can on-device inference reduce round-trip dependency *and* still fail the human experience?
2. Name the sense → feature → infer → feedback path and one failure at each hop.
3. What does **PHYSICAL_PENDING** mean for Device Quartet Edge IO Wearables in this chapter?
4. Why is LAB-TRUST-001 adjacent rather than a WAIKE “CH22 module”?
5. What is the difference between a sensing privacy *boundary* and a claim that local AI is automatically ethical?
6. Name two Stability Contract conditions specific to embodied loops.
7. What hard stop applies to camera/mic labs in shared spaces?
8. Teach-back (Explorer): explain to a nontechnical person why a late haptic can make a “correct” model feel broken.

**Researcher prompt.** What primary sources would be required to (a) promote Wearables sensing/AI claims out of PHYSICAL_PENDING and (b) close the omitted sensing-privacy standards gap—without inventing designations?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`), including systems framing for models and inference [@goodfellow_deep_learning], platform-mediated capture permissions [@w3c-mediacapture-streams-20251009], voluntary AI risk-management guidance [@nist_ai_rmf_100_1], and accessibility feedback requirements [@wcag22-20241212]. Project-specific Device Quartet and WAIKE adjacency evidence is cited via [@src-hardware-quartet] and [@src-waike], separately from external literature. Concrete sensing/IMU/camera privacy *standards* designations remain **SOURCE_NEEDED** and are **omitted** from claim promotion in this draft (CLM-CH22-004). Official MCU-NN / edge-ML system references (`edge_ml_sys_refs`) likewise remain SOURCE_NEEDED for later depth.

---

## 12. Glossary links

Chapter-local candidates (integrator merge required; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Embodied sensing | Capturing physical-world signals for interaction |
| Edge / on-device inference | Running models near the sensor/actuator |
| Edge resource budget | Latency, energy, memory, thermal limits that bound experience |
| Embodied interaction loop | Sense → infer → actuate/feedback under human timing |
| Sensing privacy boundary | What continuous capture may expose beyond the visible UI |
| Edge / cloud fallback | Degraded path when local inference cannot complete |
| Stability contract | Concurrent conditions that keep the experience alive |
| PHYSICAL_PENDING | Claim awaiting physical fabrication or measured validation |

Related earlier chapters: sensors/IO (CH08), power/thermal budgets (CH09), cloud/edge placement (CH15), data/ML framing (CH21), CE-5 local-vs-cloud trust. Related later chapters: chip-to-cloud security (CH23), privacy/responsibility deepening (CH24), twin honesty (CH29/CH31).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured evidence. No fabricated wearable telemetry.

### FIG-CH22-001 — Sense → feature → edge inference → haptic/UI feedback

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Sequence.
- **Reader should notice.** Embodied loop hops and where human timing attaches.
- **Truth class.** Conceptual / Representative educational architecture.
- **Alt text requirement.** Name sense, feature, inference, feedback; state conceptual truth class; color never sole cue.

### FIG-CH22-002 — Edge resource budget bands (illustrative)

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Budget.
- **Reader should notice.** Qualitative latency/energy/memory/thermal bands.
- **Truth class.** Illustrative.
- **Alt text requirement.** State illustrative only; forbid reading bands as Device Quartet EVT.

### FIG-CH22-003 — Edge IO Wearables learning context

- **Production status.** `draft-blocked` (no SVG embed in this draft); **PHYSICAL_PENDING** badge required.
- **Type.** Ecosystem / form-factor context.
- **Truth class.** Conceptual with qualification **PHYSICAL_PENDING** (CLM-CH22-002).
- **Alt text requirement.** Name Wearables as research/learning form factor; state physical fabrication and measured AI/sensing pending; color never sole cue.

---

## Claim footnotes used in this chapter

| Claim ID | Text (short) | Status |
|---|---|---|
| CLM-CH22-001 | On-device/edge inference can reduce round-trip dependency vs remote APIs, at device budget cost | SOURCE_IDENTIFIED (`goodfellow_deep_learning`) |
| CLM-CH22-002 | Device Quartet Edge IO Wearables remain research/learning form factors; physical AI/sensing benchmarks pending | **PHYSICAL_PENDING** (`src-hardware-quartet`) |
| CLM-CH22-003 | WAIKE `AI_ML_EDGE` / `lab_quantize_budget` / `EMBEDDED_PROTOTYPING` are adjacent, not CH22 module IDs | SOURCE_IDENTIFIED (`src-waike` @ `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`) |
| CLM-CH22-004 | Sensing/IMU/camera privacy standards citations | **OMITTED** (SOURCE_NEEDED — unresolved; no invented designations) |
