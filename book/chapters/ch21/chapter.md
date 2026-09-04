---
status: draft
chapter_id: CH21
chapter_number: 21
author: "Edmund Gunn, Jr."
part: V
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-TRUST-001]
figures:
  - FIG-CH21-001
  - FIG-CH21-002
  - FIG-CH21-003
---

# Chapter 21 — Data, Machine Learning, and Generative AI

**Status:** `draft` · **Chapter ID:** `CH21`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working full-manuscript draft · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter never claims Gate 3 completion; fixtures are teaching infrastructure, not human reader evidence).

Part V opens the intelligence, security, and responsibility arc. This chapter inherits Concept Edition **CE-5** AI slices—data, model, inference, generative systems, uncertainty, and local-versus-cloud deployment—then expands them for full-book depth. The publication-owned lab **LAB-TRUST-001** is the primary Try/Build surface. Deeper identity, encryption, and privacy-lifecycle chapters follow (CH23–CH24); here the job is to keep AI features readable as systems under a Stability Contract, not as minds.

---

## 1. The moment {#sec-ch21-moment}

You ask a practical question of an on-device or in-browser assistant. The reply arrives quickly. The sentences are smooth. The tone sounds certain—or it hedges, or it refuses, or it changes style after an app update you barely noticed.

From the seat: an answer that feels like conversation.

Underneath: **data** conditioned a **model**; that model’s stored parameters were applied at **inference** to new inputs; an **output** was rendered into the interface you can see or hear. Fluency is a property of the generated surface. Correctness is a separate question. Logging, retention, and whether the path stayed local or crossed a network can change what left the device even when the screen still looks like “just chat” [@goodfellow_deep_learning] (CLM-CH21-001).

The governing question for this chapter:

> When an assistant answer appears, what path produced it—and where do uncertainty, logging, and deployment choice change the experience?

This is not a product review of any named assistant, not a course in training large models from scratch, and not permission to treat fluent text as proof that a system “understands.”

---

## 2. What you notice {#sec-ch21-notice}

Before naming parameters or cloud regions, notice what broke or felt strange in human terms.

You expected a usable answer or a clear refusal. Instead you notice a confident-sounding wrong claim, a hedge that never names what is uncertain, a different tone after an update, a permission or privacy prompt, a spinner that lasts longer than the sentence that finally appears, or an assistive path that never announces the reply. A classmate on another device may get a different boundary: local path on theirs, remote path on yours, or the reverse.

**Fluent output can fail the experience even when the interface looks successful.**

That distinction is the chapter’s first systems skill (CE-5 signature, carried into CH21). An HTTP 200, a green “online” badge, or a polished paragraph is an observation about *delivery and surface*. Usefulness, honesty about uncertainty, and privacy posture are different observations. Collapsing them produces confident wrong blame: “the AI lied,” “the AI knows me,” or “the cloud is smart,” as if one cartoon agent owned data, model, network, and logging at once.

Optional commodity notice (no specialized gear): ask one non-sensitive practical question of an assistant you already use—or open the LAB-TRUST-001 fixture transcripts if live use is unsafe, offline, or inequitable. Write two columns—*what appeared* and *what you would need in order to trust it for a real decision*—before you invent a cause. Mark fixture rows `fixture`. Fixture text is illustrative teaching data, not your measured product evidence and not Gate validation.

---

## 3. Exploded ecosystem {#sec-ch21-ecosystem}

An assistant answer is not a single object. It is a path through an ecosystem. **FIG-CH21-001** is the first-minute map: human experience at the center, with cooperating layers—not a cartoon brain. Treat it as **representative educational architecture**, not a claim that every product wires the same stack.

Walk the layers in ordinary language.

### Human and context

Intent, stakes, language, and situation set what “good enough” means *for this person now*. A homework hint and a medical-adjacent guess do not share one acceptable uncertainty bound. Acceptable bounds are context-dependent; inventing universal accuracy percentages as gunnchOS product truth is forbidden.

### Input and interaction path

Keys, voice, images, or assistive technology must be recognized and delivered into the software path. A silent assistive failure can break the experience while sighted chrome looks busy [@wcag22-20241212].

### Application / prompt assembly

The app builds a request: user text, UI state, optional retrieved documents, account claims, and policy flags. Code choices here decide what the model ever “sees” as input—still not a mind, still a pipeline.

### Model parameters and runtime

Stored parameters shape how inputs map to outputs. Deep-learning teaching vocabulary treats learning as fitting parameters and inference as applying a trained model to new examples [@goodfellow_deep_learning]. Runtime availability, version pinning, and quantization choices (foreshadowed in CH22) condition latency and energy.

### Local vs remote placement

Inference may run on-device, on a nearby edge box, or on remote computers. That deployment choice changes privacy exposure, dependency, update control, and often delay. **FIG-CH21-002** keeps those boundaries visible.

### Network and service (when remote)

DNS, TLS, API gateways, regional endpoints, and retries. A network stall can look like “the assistant is thinking” even when no inference has started. Part IV’s connected-versus-usable lesson still applies.

### Logging, retention, and side effects

Prompts, outputs, and metadata may be retained, shared with vendors, or queued for review. Side effects can outlive the on-screen reply. Disclosure posture is part of the experience, not an appendix.

### Render / announce

Text, speech, or UI actions must reach the human—including keyboard and assistive paths. Color-only “confidence” meters fail accessibility teaching rules [@wcag22-20241212].

### Society and equity

Who can complete the lab without paid APIs or GPUs? Who is harmed by fluent errors presented as fact? NIST AI RMF 1.0 frames organizational risk management for AI systems without treating “trust” as a binary property of AI itself [@nist_ai_rmf_100_1] (CLM-CH21-002).

---

## 4. Follow the signal {#sec-ch21-signal}

Here the “signal” is the fate of one practical question—from input to human judgment—not a mystical spark of understanding. Read the sequence as a logical path. Alternate product paths exist; open questions stay labeled undetermined.

1. **Intent.** A person asks, dictates, pastes, or uploads.
2. **Input capture.** Sensors, IME, or files deliver bits into the app.
3. **Context assembly.** Prompt text, optional retrieval, account/session claims, and UI state combine.
4. **Policy gate.** Session valid? Feature allowed? Consent cover this purpose?
5. **Inference placement.** Local runtime or remote API applies model parameters to the assembled input [@goodfellow_deep_learning].
6. **Output generation.** Predicted tokens, classifications, rankings, or tool-call proposals return.
7. **Side effects.** Logs, analytics, abuse review, or fine-tune queues may record more than the screen shows.
8. **Render / announce.** Visual, audio, or assistive feedback reaches (or fails to reach) the human.
9. **Human judgment.** Useful, wrong-but-fluent, hedged, refused, or “works for them / not for me.”

### Generative systems without mythology

**Machine learning** is the broader practice of fitting model parameters from data and applying them at inference—classification, ranking, detection, and generation all sit under that umbrella when they learn from examples [@goodfellow_deep_learning]. **Generative AI**, in this book’s systems view, means systems that produce new text, images, code, or similar media by predicting likely continuations under a model and decoding procedure. Generative systems are one family of ML applications, not a synonym for all machine learning. Prediction of likely tokens is not comprehension. The pedagogical firewall is deliberate: speak of inputs, parameters, inference, and outputs—not beliefs or intentions (CLM-CH21-001 wording boundary).

### Local versus cloud as a path fork

| Path class | Everyday question | Typical mis-read |
|---|---|---|
| **Local / on-device** | Did sensitive content stay on this device? | Treating a UI badge as proof of zero telemetry |
| **Remote / cloud** | Which org received the prompt, and under what retention? | Treating TLS as “private forever at every endpoint” |
| **Hybrid** | Which stages left the device? | Collapsing retrieval, inference, and logging into one word—“AI” |

Illustrative comparison tables for latency, energy, privacy, and control are **teaching aids** unless a measurement bundle is attached (CLM-CH21-005). Do not promote classroom wall-clock samples into Device Quartet product benchmarks (**PHYSICAL_PENDING** when project SKUs are mentioned).

### Uncertainty families without collapse

**FIG-CH21-003** separates three families readers must not collapse:

| Family | Everyday question | Typical mis-use |
|---|---|---|
| **Fluency** | Does the output sound coherent? | Treating polish as truth |
| **Correctness** | Is the claim accurate for this task? | One lucky correct answer as “reliable” |
| **Evaluation evidence** | What labeled checks support usefulness claims? | Inventing metrics or citing fixtures as human validation |

---

## 5. Component cards {#sec-ch21-components}

Plain-language cards for the objects that cooperate. Each card names constraints and human-visible failure symptoms. None of these components is a person.

### Training and input data

**What it is.** Examples and records used to fit a model, plus the live inputs that enter inference (prompts, files, sensor snippets, retrieved passages).

**Constraints.** Quality, coverage, consent, and retention bounds. Missing or skewed data produce systematic failures that look like “personality.”

**Failure symptoms.** Confident wrong answers on underrepresented topics; leakage of sensitive training-like content; retrieval that surfaces the wrong document.

### Model parameters

**What they are.** Stored numbers (and associated architecture/code) that shape how inputs map to outputs [@goodfellow_deep_learning].

**Constraints.** Version consistency, license/policy limits, size versus device memory, update authenticity.

**Failure symptoms.** Sudden style or quality shifts after an update; offline feature when weights are missing; incompatible runtime after an OS upgrade.

### Inference runtime / output path

**What it is.** The engine that applies parameters to new inputs and returns predictions or generations.

**Constraints.** Latency and energy budgets for interactive use; thermal/power policy on commodity devices; decoding settings that change verbosity and risk.

**Failure symptoms.** Spinners with no output; truncated answers; “connected” UI while the runtime is stalled or unreachable.

### Retrieval / tool adapters (optional)

**What they are.** Components that fetch documents or call tools before or after generation.

**Constraints.** Access control on corpora; redaction; tool permission scopes.

**Failure symptoms.** Answers that cite absent sources; leaked patron or classmate data in a shared corpus demo; tool actions the user did not authorize.

### Logging and disclosure store

**What it is.** Records of prompts, outputs, metadata, and consent state.

**Constraints.** Purpose limitation, retention clocks, export/delete pathways, accessible disclosure language.

**Failure symptoms.** History resurfacing after a delete request; portfolio screenshots that still contain identifiers; disclosure text the learner cannot operate with keyboard or assistive technology.

### Identity and authorization adjacency

**What they are.** Session proof and allow/deny decisions that gate the AI feature. Full depth lives in later chapters; CH21 only needs the UX-linked split: signed-in ≠ entitled to every action.

**Failure symptoms.** Feature visible but silently blocked; mystery re-auth loops; verify steps that exclude assistive paths.

---

## 6. Stability contract {#sec-ch21-stability}

**Definition (publication teaching model):** a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

For assistant answers in this chapter, the contract is not “the model is trustworthy.” It is a set of concurrent conditions on data, runtime, deployment honesty, and human-catchable uncertainty—aligned with CE-5 teaching bounds and NIST AI RMF’s organizational risk-management posture [@nist_ai_rmf_100_1].

| Bound (teaching ID) | Within bounds means | Out of bounds (human-visible) |
|---|---|---|
| **SC-CH21-Q** Answer usability | Output is actionable or clearly refused/hedged | Fluent wrong answer treated as fact |
| **SC-CH21-U** Uncertainty honesty | Uncertainty is visible enough for the stakes | Confident fabrication; unexplained refusal storms |
| **SC-CH21-D** Data fitness | Inputs/retrieval quality within acceptable bounds | Garbage-in presented as expert-out |
| **SC-CH21-M** Model/runtime consistency | Version and availability match what the UI implies | Silent model swap; offline while chrome claims ready |
| **SC-CH21-L** Path locality disclosure | Learner can tell local vs remote at a usable level | Unexpected off-device send |
| **SC-CH21-T** Latency/energy budget | Interactive delay acceptable in context | Spinners that erase trust faster than the sentence helps |
| **SC-CH21-P** Disclosure/logging posture | Retention/share match consent card | Prompt history reused beyond disclosure |
| **SC-CH21-A** Accessible trust path | Answer and disclosure work with AT / keyboard | Vision-only confidence chrome; unspoken reply |
| **SC-CH21-E** Equity of completion | Fixtures allow completion without paid APIs/GPUs | Lab gated on cloud credits |

Observation versus inference rule (lab and prose):

- **Observation** — on-screen text, network-required Y/N, fixture versus live, wall-clock if measured and labeled `n=1`
- **Interpretation** — “probably cloud latency,” “probably retrieval miss”
- **Causal claim** — needs extra evidence (config, logs, controlled comparison)

Connected-versus-usable instances for this chapter: API returns 200 while the answer is wrong and authoritative-looking; model loaded while output never reaches the accessibility tree; TLS established while the endpoint operator can still read plaintext after decryption.

Non-claims: no numeric product SLOs for gunnchOS AI features; no assertion that meeting this teaching contract equals legal compliance; no labeling of AI as inherently inside or outside trust—only systems and practices are.

---

## 7. Try it {#sec-ch21-try}

**Primary lab:** **LAB-TRUST-001** — Compare local versus remote AI paths and write a consent/trust card.

**Publication ownership.** LAB-TRUST-001 is a book-side lab design inheriting CE-5 themes. It is **not** a WAIKE course module ID (CLM-CH21-004). Status tags on the lab package include `IMPLEMENTED_DIGITAL` and `FIXTURE_VALIDATED` for synthetic Route L / Route C transcripts—teaching infrastructure, never Gate 3 human validation.

**WAIKE adjacency (not exact map).** At audited WAIKE SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`, the digital_rc package **AI_ML_EDGE** hosts file-backed labs on scoring/inference, edge budgets, and RAG redaction. Catalog/track pointers such as `ai_ml_data` are related program language, not interchangeable IDs. Cite adjacency honestly; do not invent a WAIKE module named LAB-TRUST-001 or CH21 [@src-waike] (CLM-CH21-003).

### Procedure spine (Explorer baseline)

1. **Predict** which path exposes more data leaving the device, and which Stability Contract bound (locality, privacy lifecycle, uncertainty honesty) is most likely to break first.
2. **Route L** — local / offline-capable simulator or fixture transcript.
3. **Route C** — remote assistant path (live optional) or fixture transcript.
4. **Compare** with observations only: what appeared, network required Y/N, disclosed retention cues.
5. **Consent/trust card** — audience, purpose, data classes, retention, opt-out, AI disclosure.
6. **Dual ledger** — human-trust feeling versus technical-trust controls/evidence.
7. **Uncertainty note** — fluent-but-wrong / unverifiable / none observed *with checks named*.

Safety: use only non-sensitive prompts; never paste real secrets, health records, or private messages; redact identifiers before portfolio share; no exploit steps or credential harvesting.

### Pathway extensions

**Operator.** Locate permission, account, and privacy surfaces; separate symptoms that look like identity, authorization, network, or model quality.

**Builder.** Add one redaction rule for a sample prompt/log line; document utility-versus-exposure tradeoff.

**Engineer.** Sketch trust boundaries crossed by one prompt; compare local versus remote for latency, energy, privacy, and control—label illustrative rows unless measured.

**Researcher.** State an evaluation question with labeled limitations; do not invent peer-reviewed metrics. Accessible ML evaluation methods literature remains **SOURCE_NEEDED** for later depth (`peer_eval_methods` in the chapter source register)—do not invent DOIs.

**Educator.** Keep Route Paper / fixtures first-class for equity; facilitate “feeling versus control” teach-backs.

**Evidence to keep.** Comparison table, consent/trust card, dual ledger, uncertainty note, scrubbed reflection, teach-back. Completion means artifact-backed claims—not a vibes-based “the AI is trustworthy” slogan.

---

## 8. Build it {#sec-ch21-build}

Extend LAB-TRUST-001 without turning Part V into a fake benchmark catalog.

### Explorer

Build a pocket card: *fluency ≠ correctness*, plus the data→model→inference chain in one plain sentence.

### Operator

Build a three-column inspection sheet: observations | inferences | evidence still needed. Add one row for “where did this prompt go?”

### Builder

Build a one-page disclosure note for a toy retrieval path: what is collected, why, how long, who can see it, how to opt out, and how AI assistance is named. Optional: a tiny redaction helper on synthetic log lines—never live capture of others’ private data.

### Engineer

Build a local-versus-cloud decision tree that ends in “needs more evidence” whenever UI copy claims locality without proof. List energy and latency as first-class tradeoffs alongside privacy and control (CLM-CH21-005 illustrative discipline).

### Researcher

Build an evidence plan for a claim you are *not* allowed to make yet—for example, a published accuracy number for a named assistant on a homework corpus. Specify what labeled evaluation and confounder control would require; keep peer-eval depth **SOURCE_NEEDED**. A future publication-owned toy eval worksheet (labeling observed versus inferred model errors) remains **proposed** until implemented—do not invent a WAIKE module id for it.

Educators can facilitate Section 11 teach-backs and keep fixture routes as equitable defaults—not lesser paths.

---

## 9. Secure and include it {#sec-ch21-secure-include}

### Security (UX-linked, not a scare-list)

Prompts, pasted documents, and retrieved files are attack surface because they enter model context. Permission dialogs and update badges are trust boundaries learners can see. Classical protection principles such as least privilege and psychological acceptability still connect controls to usable experience [@saltzer_schroeder_1975]. Stay at concepts and symptoms: no exploit recipes, no credential harvesting, no unauthorized scanning.

### Privacy

Teach lifecycle stages with decision owners: collect → use → retain → share → delete/redact. Portfolio artifacts must scrub account names, emails, and message previews. Metered-link and offline learners should not be forced onto live cloud assistants—LAB-TRUST-001 fixtures exist for equity and privacy together.

### Accessibility

Accessible disclosure language and operable verify/answer paths are Stability Contract conditions, not garnish. Do not rely on color-only confidence meters; provide text hedges. Timing tasks allow extended time; avoid seizure-risk “thinking” animations. WCAG 2.2 informs teaching intent—not a claim that this book or any gunnchOS product is certified [@wcag22-20241212].

### Equity

Local GPUs and paid APIs are unevenly available. Fixtures and recorded transcripts are required for fair completion (SC-CH21-E). Language and dialect gaps in generative outputs are quality and equity issues, not user failure. Device Quartet form factors may appear only as optional future learning-lab context—**PHYSICAL_PENDING** for product-specific AI benchmarks; never required lab hardware.

### Safety

Commodity devices only. Non-sensitive prompts only. No attempts to extract others’ private data “for the lab.”

### Ethics and responsible use

Do not anthropomorphize models as moral agents; humans remain accountable for deployment and reliance. Prefer organizational risk-management language from NIST AI RMF over slogans that AI is inherently safe or unsafe [@nist_ai_rmf_100_1]. Do not present `FIXTURE_VALIDATED` as Gate validation. Do not invent evaluation scores. Overclaiming measurement is still false evidence.

---

## 10. Career lens {#sec-ch21-career}

One assistant answer crosses many ownership domains. No table promises employment; roles vary by organization. LAB-TRUST-001 artifacts resemble early professional evidence in miniature: labeled observations, disclosure notes, and explicit uncertainty.

| Role family | Typical artifacts | Review questions |
|---|---|---|
| Applied ML / AI engineer | Eval note with limitations; model-card style summary | What was measured vs inferred? |
| Privacy / responsible AI analyst | Data-path + retention note; consent card | Does disclosure match logging? |
| Security engineer | Trust-boundary sketch on one prompt | Which UX symptom maps to which control? |
| SRE / platform | Runtime version and dependency notes | Did we confuse uptime with answer usability? |
| Accessibility specialist | AT pathway writeup for answer + disclosure | Was equivalent feedback present? |
| Educator / facilitator | Misconception checklist: fluency ≠ correctness | Did learners label fixtures correctly? |

Portfolio hint: a scrubbed consent card plus an uncertainty note beats a vibes-based claim that “the model understands the user.”

---

## 11. Check understanding {#sec-ch21-check}

**Concept.** In one sentence, frame a familiar AI feature as data conditioning a model applied at inference to produce outputs—without saying the system understands.

**Concept.** In one sentence each, distinguish *fluency*, *correctness*, and *evaluation evidence*.

**System tracing.** Trace one practical question from input to human judgment in numbered steps. Mark observed versus inferred. Name ≥4 Stability Contract conditions that had to hold together.

**Misconception check.** Why can a polished paragraph still fail the experience?

**Misconception check.** Why must this chapter refuse to treat AI as inherently trustworthy or untrustworthy?

**Deployment check.** Name one privacy, one latency/energy, and one control tradeoff between local and remote inference—label illustrative unless you measured.

**Evidence ethics.** What is the difference between LAB-TRUST-001 `FIXTURE_VALIDATED` infrastructure and Gate 3 human reader validation? Why must WAIKE `AI_ML_EDGE` adjacency never be renamed as LAB-TRUST-001?

**Teach-it-back.** Explain to a newcomer—using only CE-5 / LAB-TRUST-001 vocabulary—why fluency is not correctness.

**Researcher prompt.** What additional evidence would be required to move from a classroom uncertainty note toward a labeled evaluation study—and what remains **SOURCE_NEEDED** for this chapter?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). Deep Learning (Goodfellow et al.) supplies parameters/inference vocabulary; NIST AI RMF 1.0 supplies organizational risk-management language without binary trust slogans [@goodfellow_deep_learning; @nist_ai_rmf_100_1]. The textbook key `russell_norvig_aima` remains **NEEDS_PRIMARY_VERIFICATION** (edition/ISBN deferred) and is **omitted** from inline citation in this working draft until primary shelf verification closes.

Project-specific WAIKE adjacency uses audited SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` via `@src-waike` (CLM-CH21-003). LAB-TRUST-001 evidence lives under `labs/LAB-TRUST-001/` on the publication repository (CLM-CH21-004). Peer-reviewed accessible evaluation-methods depth remains **SOURCE_NEEDED**. Gate 3 reader evidence remains pending; this working draft is not publication-ready.

Inline citations used in this chapter include @goodfellow_deep_learning, @nist_ai_rmf_100_1, @src-waike, @saltzer_schroeder_1975, and @wcag22-20241212.

Primary inheritance (link, prefer over duplication): Concept Edition CE-5 under the publication preproduction tree, and `labs/LAB-TRUST-001/`.

---

## 12. Glossary links {#sec-ch21-glossary}

Candidate terms introduced or reinforced here (see also chapter glossary candidates; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Training and input data | Examples/records used to fit a model or answer a question |
| Machine learning | Broader practice of fitting models from data and applying them at inference (not only generative systems) |
| Model parameters | Stored numbers shaping inputs→outputs; not a mind |
| Inference / output | Running a model on new inputs to produce a prediction or generation |
| Generative AI (systems view) | One ML family: systems that produce new text/images/code by predicting likely continuations (not all ML) |
| Uncertainty and errors | Outputs can be wrong or incomplete even when fluent |
| Local vs cloud AI | Whether inference runs on-device or on remote computers |
| Evaluation under uncertainty | Checking usefulness with labeled observations and limits |
| Fluency ≠ correctness | Coherent surface text is not proof of accuracy |
| Stability Contract | Concurrent hidden conditions that keep an experience alive (book teaching model) |
| Observation vs inference | What happened vs what may explain it |
| Consent / trust card | Disclosure artifact: audience, purpose, data classes, retention, opt-out, AI notice |
| Dual ledger | Human-trust feeling recorded beside technical controls and evidence |

Related earlier chapters: experience-first observation craft (CH02), memory/storage lifecycles (CH07), apps/APIs (CH14), placement and cloud/edge (CH15). Related later chapters: acceleration and edge budgets (CH22), cybersecurity (CH23), privacy/identity/ethics (CH24), evidence practice (CH27), capstone synthesis (CH31).

---

## Figure references (planned embeds; accessibility metadata)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured learner or lab evidence. No fabricated telemetry. No product accuracy curves.

### FIG-CH21-001 — Data → model → inference → output

- **Type.** Conceptual flowchart (inherit CE-5 FIG-CE5-001 intent).
- **Reader should notice.** Data conditions a model; parameters apply at inference; output is not understanding.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name each stage in order; state conceptual truth class; forbid mind metaphors as literal claims.

### FIG-CH21-002 — Local vs cloud AI boundaries

- **Type.** Layered comparison (inherit CE-5 FIG-CE5-002 intent).
- **Reader should notice.** Same question, different privacy/latency/control boundaries.
- **Truth class.** Illustrative unless a measurement bundle is attached.
- **Alt text requirement.** Name both paths and at least one differing bound (privacy, latency, or control); deny product SKU timings without evidence.

### FIG-CH21-003 — Fluency vs correctness vs evaluation evidence

- **Type.** Conceptual hierarchy / separation.
- **Reader should notice.** Three families that must not collapse into “the AI was right.”
- **Truth class.** Conceptual.
- **Alt text requirement.** Name all three families and one everyday question each; state that fixtures are not human validation.

---

## Claim footnotes used in this chapter (project-specific)

- **CLM-CH21-001.** Accessible systems teaching can frame many AI features as data conditioning a model applied at inference—cited via [@goodfellow_deep_learning]; `russell_norvig_aima` omitted pending primary verification. Prohibited wording: the model understands/knows.
- **CLM-CH21-002.** NIST AI RMF 1.0 provides voluntary organizational guidance for managing AI risks without treating trust as a binary property of AI itself [@nist_ai_rmf_100_1].
- **CLM-CH21-003.** WAIKE digital_rc `AI_ML_EDGE` hosts adjacent file-backed labs at audited SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` [@src-waike]—adjacency only; no invented WAIKE module LAB-TRUST-001 / CH21.
- **CLM-CH21-004.** Publication LAB-TRUST-001 is a book-side lab inheriting CE-5 themes; not a WAIKE course ID.
- **CLM-CH21-005.** Illustrative local-vs-cloud comparison tables are teaching aids unless a measurement bundle is attached—no measured gunnchOS SKU latency without evidence.
