---
status: draft
chapter_id: CH27
chapter_number: 27
title: "Testing, Observability, and Evidence"
author: "Edmund Gunn, Jr."
part: VI
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-CE06-001]
figures:
  - FIG-CH27-001
  - FIG-CH27-002
  - FIG-CH27-003
---

# Chapter 27 — Testing, Observability, and Evidence

**Status:** `draft` · **Chapter ID:** `CH27`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working draft complete · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does **not** claim Gate 3 PASS; fixtures, simulations, and illustrative portfolios are teaching infrastructure, not human reader evidence).

Part VI asks builders to prove what they claim. Chapter 20 already taught concurrent conditions and an evidence hierarchy. Chapter 26 (when drafted) will cover change history. This chapter names the remaining honesty problem: **a green test, a green dashboard, and a green simulation can all be true while the human experience is still false—or unmeasured.** Simulation is not measurement. A fixture is not a reader study. An OpenTelemetry signal vocabulary is not a fake product SLO.

The signature distinction for this chapter:

> **Simulation ≠ measurement.** Tests check claimed behavior under deliberate cases. Observability lets you ask new questions of a running system. Evidence is what remains after you label what was observed, what was inferred, and what was only illustrated.

---

## 1. The moment {#sec-moment}

A feature “passes” locally. Unit tests are green. The staging checklist is checked. Status dashboards look calm—until a classmate, a customer, or you on a slower link see stalls, silent failures, or a success toast that never finished the remote work.

From the seat: contradiction between **test theater** and **lived outcome**.

Underneath: mismatched oracles, missing signals, and over-promoted simulations. A test that asserts “HTTP 200” does not assert “the person finished with acceptable delay and feedback.” A dashboard panel that plots a synthetic load profile does not measure your classroom device. A fixture portfolio that trains observation/inference labeling is teaching infrastructure—not Gate 3 human validation (CLM-CH27-004).

The governing question:

> When tests and dashboards look fine while people still suffer, what was tested, what was observed, and what was only simulated or inferred?

This chapter expands CE-6’s evidence hierarchy and observation-vs-inference craft into full-book testing and observability literacy. It is not an observability product manual, not a carrier QoE campaign, and not a license to invent benchmarks as human evidence [@itu-t-g1011].

---

## 2. What you notice {#sec-notice}

Before naming traces or assertion libraries, notice the human contract that broke.

You expected a change to be safe because something “passed.” Instead you notice: local green / remote red; green metrics beside abandoned actions; a replay or demo that works while live traffic does not; a log flood that still fails to answer “did this person finish?”; or a portfolio that copies fixture timings as if they were measured on your device.

**A test result is an observation about the test.**  
**A log line or metric sample is an observation about a signal.**  
**A causal story is an inference until more evidence arrives.**

Collapsing those three produces confident wrong blame: “tests prove it works,” “the dashboard proves users are fine,” “the simulation proves the design.” Each may be useful; none automatically becomes the others.

Optional commodity notice (no specialized gear): pick one recent change you made—or one familiar send/submit/sync. Write three columns—*test or checklist outcome*, *signal or status observed*, *human outcome*—before you invent a cause. If live capture is unsafe, offline, or metered, use LAB-CE06-001 Route F and mark rows `fixture`. Fixture timings are illustrative teaching data, not your measured evidence and not Gate validation.

---

## 3. Exploded ecosystem {#sec-ecosystem}

Evidence about an experience is not a single object. It is a path through layers that produce tests, signals, and claims. **FIG-CH27-001** (planned conceptual) is the evidence hierarchy ladder: illustrative aid → commodity observation → instrumentation → correlated multi-signal inspection → controlled comparison → standards-aligned QoE methods. Treat the ladder as **Representative educational architecture**. Learner labs sit mid-ladder; they are not ITU-T G.1011 assessment campaigns (CLM-CH27-001) [@itu-t-g1011].

Walk the layers in ordinary language.

### Human experience and claim

What success means for a person—finished, correct, announced, acceptable. Every test oracle and every dashboard tile should eventually answer a human question, or admit it does not.

### Deliberate cases (tests)

Checks run under chosen inputs and environments. They answer narrow questions well and overclaim when treated as the whole world.

### Oracles

How we decide pass/fail. An oracle that matches HTTP codes but ignores usable completion is a mismatched oracle—not “proof the experience works.”

### Runtime signals

Traces, metrics, and logs (and related events) as observability vocabulary. OpenTelemetry’s conceptual documentation describes these as distinct **signals**—useful shared language, not a version pin or mandatory install for Explorer readers [@otel-signals].

### Aggregation and views

Dashboards, alerts, and summaries. A green panel is an observation about the panel’s query—not automatically about every user’s session.

### Simulation / fixture / replay

Teaching and engineering tools that approximate behavior. Powerful for practice and regression; dishonest when silently upgraded to field measurement.

### Inference and narrative

Stories that explain observations. Allowed—and required to stay labeled until extra evidence arrives.

### Redaction and sharing

Secrets and PII in traces/logs/screenshots. Portfolio literacy includes what you must remove before share.

**FIG-CH27-002** (planned comparative) separates *test pass* from *usable experience* so readers stop treating a green suite as QoE.

---

## 4. Follow the signal {#sec-signal}

Here the “signal” is the chain from human claim → test or observation → labeled inference. Read it as a diagnosis story. Alternate paths exist; open questions stay undetermined.

1. **Human claim.** “Send finishes with coherent feedback for this person in this context.”
2. **Oracle choice.** What would count as evidence for that claim—not merely for a proxy?
3. **Deliberate case.** A test, checklist, or lab route exercises a bounded situation.
4. **Runtime observation (if live).** Status UI, commodity timing, log/metric/trace excerpt—ethically captured [@otel-signals].
5. **Label.** Observed / inferred / illustrative / fixture / simulated.
6. **Inference gate.** Causal story only with named extra evidence still needed.
7. **Share decision.** Redact before portfolio or incident notes leave the machine.
8. **Honesty close.** State what the artifact proves—and what it does not.

### Signal families without collapse

| Family | Everyday question | Typical mis-use |
|---|---|---|
| **Test result** | Did this deliberate case meet its oracle? | Treating the suite as the whole user population |
| **Metric** | What did this numeric signal sample or aggregate show? | Promoting one KPI into a Stability Contract |
| **Log** | What event text was recorded? | Reading a log flood as root-cause certainty |
| **Trace** | What spans/path did this request (or demo) follow? | Claiming complete visibility from one partial trace [@otel-signals] |
| **Simulation / fixture** | What did the teaching or synthetic setup show? | Silent upgrade to measured human evidence |
| **Inference** | What may explain the observations? | Writing inference in the observation column |

**FIG-CH27-003** (planned sequence) is the observation → inference gate: signals enter; labels are required; causal claims need extra evidence.

### Evidence hierarchy (climb only as far as tools and ethics allow)

Inherited from CE-6 / CH20 and restated here for testing/observability depth (CLM-CH27-001) [@itu-t-g1011]:

1. Illustrative teaching aid (labeled)
2. Commodity observation (status UI, wall-clock, visible stalls)
3. Browser / OS / app instrumentation where exposed
4. Correlated multi-signal inspection (still not proof)
5. Controlled comparison under ethical constraints
6. Standards-aligned subjective / objective QoE methods—**not** required for classroom completion

**Simulation and fixtures belong on the lower rungs unless independently measured and labeled otherwise.** That is the chapter’s non-negotiable honesty rule.

### Adjacent practice (not invented CH27 WAIKE modules)

WAIKE accepted `main` (SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`) includes adjacent CLOUD_DEVOPS labs such as `lab_slo_budget` and `lab_incident_runbook`, plus DATA_DASHBOARDS debug/freshness labs. Those are **adjacent** competencies—not renamed as publication lab IDs and not an invented “observability course for CH27” (CLM-CH27-002) [@waike-research-ops-ce06].

---

## 5. Component cards {#sec-components}

For each idea: plain language, analogy (labeled), technical function, constraints, common symptoms.

### Testing

- **Plain language.** Checking claimed behavior with deliberate cases.
- **Analogy (labeled).** Like a fire drill—useful rehearsal, not proof every real fire will go the same way.
- **Technical function.** Produces pass/fail under chosen oracles and environments.
- **Constraints.** Coverage gaps; oracle mismatch; local ≠ production; one run ≠ reliability study.
- **Symptoms.** Green suite beside failed human outcomes; flaky cases treated as “random” without evidence.

### Test oracle

- **Plain language.** How we know a test outcome matches the experience claim.
- **Analogy (labeled).** Like a referee’s rulebook—if the rulebook measures the wrong game, the whistle misleads.
- **Technical function.** Binds assertions to the human question (or admits it only binds a proxy).
- **Constraints.** Proxies (status codes, unit purity) can be necessary and still insufficient for QoE.
- **Symptoms.** “All tests passed” while send stalls for users.

### Observability

- **Plain language.** Ability to ask new questions of a running system via signals.
- **Analogy (labeled).** Like being able to inspect a living city with multiple instrument types—not only replaying yesterday’s drill.
- **Technical function.** Traces, metrics, logs (and related signals) as inspectable evidence channels [@otel-signals].
- **Constraints.** Instrumentation coverage gaps; cost; privacy; Explorer pathway does not require installing OpenTelemetry.
- **Symptoms.** Dashboards green while the question you need was never instrumented.

### Evidence hierarchy

- **Plain language.** From illustrative aid to stronger measurement methods without faking rungs.
- **Analogy (labeled).** Like climbing a ladder—skipping rungs by renaming simulation as measurement is falling with style.
- **Technical function.** Pedagogical ancestor from CE-6; aligns classroom honesty with G.1011-aware vocabulary without claiming lab = formal QoE study (CLM-CH27-001) [@itu-t-g1011].
- **Constraints.** Tools, ethics, and access limit how far a reader can climb.
- **Symptoms.** Fixture numbers pasted as “our benchmark.”

### Observation vs inference

- **Plain language.** What happened vs what may explain it.
- **Analogy (labeled).** Like a notebook that separates “saw the light blink” from “the pump must be broken.”
- **Technical function.** Portfolio and incident discipline; LAB-CE06-001 field split.
- **Constraints.** Outside observation rarely distinguishes failure domains cleanly.
- **Symptoms.** Causal certainty in the observation column.

### Evidence redaction

- **Plain language.** Removing secrets/PII before sharing artifacts.
- **Analogy (labeled).** Like blanking account numbers on a photocopy before you pin it on a board.
- **Technical function.** Makes observability artifacts shareable without leaking tokens, messages, or identifiers.
- **Constraints.** Over-redaction can destroy needed evidence; under-redaction harms people.
- **Symptoms.** Screenshots with emails, auth headers, or chat previews in portfolios.

---

## 6. Stability contract {#sec-stability}

**Definition (publication teaching model, inherited):** a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

For this chapter, add evidence conditions to that contract:

| ID | Evidence condition |
|---|---|
| EV-01 | Signals available at the depth the claim requires |
| EV-02 | Test oracles match the human experience claims (or admit proxy limits) |
| EV-03 | Observation / inference / fixture / simulation boundaries enforced in artifacts |
| EV-04 | PII / secrets redacted before portfolio or external share |
| EV-05 | Simulations and fixtures never silently upgraded to measured human evidence |
| EV-06 | Uncertainty and instrumentation limits stated explicitly |

**Signature distinctions:**

- Connected ≠ usable (CH20 / CE-6).
- **Test-pass ≠ experience-pass.**
- **Simulation ≠ measurement.**
- **`FIXTURE_VALIDATED` ≠ Gate 3 PASS** (CLM-CH27-004).

### How to teach and apply it (eight moves)

1. **Name the human experience claim** in one sentence.
2. **Name the oracle or signal** that could support it.
3. **Separate** test outcomes, runtime observations, and inferences.
4. **Place the datum on the evidence hierarchy** [@itu-t-g1011].
5. **Label** fixture / simulated / illustrative when applicable.
6. **Redact** before share.
7. **State limits**—what commodity tools cannot see.
8. **Close with teach-back**—can another person apply the same labels?

### LAB-CE06-001 linkage

**LAB-CE06-001** remains the publication-owned EMIT practice surface for evidence fields (`observations`, `inferences`, `measurements`, `evidence_limitations`, and related portfolio templates). Status on accepted infrastructure: **`FIXTURE_VALIDATED`**. The lab’s `validate_portfolio.py` checks package structure and forbids treating fixtures as Gate 3 human PASS. That status means validators, blank templates, and illustrative fixtures exist and pass structural checks. It does **not** mean Gate 3 PASS. It does **not** mean illustrative example portfolios are human evidence (CLM-CH27-004).

---

## 7. Try it {#sec-try}

### LAB-CE06-001 — evidence practice (inherit)

**Goal.** Practice observation vs inference, evidence limitations, and honest labeling on a real or fixture experience—without inventing benchmarks.

**Routes (summary; full procedure in lab README).**

- **Route A — Notebook + status UI.** Reproduce a connected-but-unusable (or allowed) experience once; separate status chrome from human outcome.
- **Route B — Local stall demo.** Optional `browser/index.html`; label timings observed vs inferred.
- **Route F — Fixture fallback.** Use supplied fixtures; mark `fixture`; study `fixtures/illustrative_example/` only as **ILLUSTRATIVE — not human evidence**.

**Explorer baseline for CH27 emphasis.**

1. Predict whether failure will show up first in a *test oracle gap*, a *missing signal*, or a *mis-labeled inference*.
2. Fill observation vs inference; no causal claim without naming extra evidence needed.
3. Place two claims on the evidence hierarchy (for example: commodity status UI vs “would need G.1011-aligned study”).
4. Redact any accidental identifiers.
5. Produce teach-back: explain simulation ≠ measurement to a peer.

**Operator extension.** Add one metric/log/trace *concept* note using OpenTelemetry signal vocabulary—without requiring a full OTel install [@otel-signals]. Label what you could and could not observe.

**Builder extension.** Add one assertion or checklist item whose oracle names the human outcome (not only a proxy), plus one observability note on the change.

**Engineer extension.** Design a minimal signal set for one failure domain; list coverage gaps; cite signal concepts without invented version pins (CLM-CH27-003) [@otel-signals].

**Researcher extension.** State what would be required to move a classroom claim toward standards-aligned QoE methods—and what this lab does not provide [@itu-t-g1011]. No invented statistics.

**Educator facilitation.** Keep Route F first-class. Reject portfolios that paste fixture numbers as personal measurements.

### Proposed worksheet (not a WAIKE ID)

`proposed: LAB-CH27-SIGNAL-001` — redacted fixture-trace labeling worksheet (observation / inference / redact / hierarchy rung). Until published as a lab package, complete the same discipline inside LAB-CE06-001 portfolio fields.

**WAIKE alignment note.** Adjacent only: CLOUD_DEVOPS `lab_slo_budget` / `lab_incident_runbook` and DATA_DASHBOARDS debug/freshness labs at SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`. No exact WAIKE module equals CH27 (CLM-CH27-002) [@waike-research-ops-ce06].

---

## 8. Build it {#sec-build}

Extend evidence discipline without shipping a fake benchmark catalog.

### Explorer

Build a pocket card: *test result ≠ human outcome ≠ causal story*, plus the line **simulation ≠ measurement**.

### Operator

Build a three-column sheet: *test/checklist* | *signal observed* | *inference (evidence still needed)*. Add a fourth mark for `fixture` / `simulated` when applicable.

### Builder

Build one change note that includes: (1) one assertion or manual check tied to a human-visible outcome; (2) one observability note (what signal would reveal regression); (3) redaction checklist for any screenshot or log snippet.

### Engineer

Build a minimal signal map for one failure domain (which questions need metrics vs logs vs traces) using OpenTelemetry conceptual vocabulary without version theater [@otel-signals]. End more branches in “needs more evidence” than in fake certainty.

### Researcher

Build an evidence plan for a claim you are *not* allowed to make yet—for example, a MOS score or product SLO from classroom fixtures. Specify what methodology and physical/human evidence would be required; keep Gate 3 and Quartet claims honest and pending where applicable [@itu-t-g1011].

Educators can facilitate Section 11 teach-backs and treat Route F as equitable completion—not a lesser path.

---

## 9. Secure and include it {#sec-secure-include}

### Security

Traces, logs, HAR exports, and test dumps can leak tokens, session cookies, and internal hosts. Prefer fixtures and redaction. Unauthorized scanning and credential harvesting are out of scope.

### Privacy

Portfolio artifacts must scrub account names, emails, message previews, and precise location. Metered-link learners should not be forced onto expensive live captures—Route F exists for equity and privacy together.

### Accessibility

Evidence tooling must have text equivalents. Do not rely on color-only dashboard states. Timing and labeling tasks allow extended time. WCAG 2.2 informs teaching intent—not a claim that this book or any product is certified [@wcag22-20241212].

### Equity

“Works in CI on a fast runner” is not a Stability Contract for humans on weaker devices, metered cellular, shared computers, or assistive paths. Fixture routes keep learning accessible without requiring production access. Name who is excluded when “proof” assumes one privileged setup.

### Safety

Commodity devices only. No exploit steps, no capture of others’ private data, no jailbreaks.

### Ethics

Do not present illustrative fixture numbers as measured human evidence. Do not present `FIXTURE_VALIDATED` as Gate 3 PASS. Do not invent observability product benchmarks or OTel version pins. **Overclaiming measurement is still false evidence.**

---

## 10. Career lens {#sec-career}

Testing and observability cross ownership domains. No table promises employment; roles vary by organization. LAB-CE06-001 artifacts resemble early professional evidence in miniature: labeled observations, oracle notes, and explicit uncertainty.

| Role lens | Typical artifacts | Review questions |
|---|---|---|
| SRE / observability | Signal map; redacted trace note | Did we confuse dashboard green with user completion? |
| QA / test engineer | Oracle vs experience mismatch writeup | What human claim does this assertion actually bind? |
| Security-minded developer | Log redaction checklist | What would leak if this screenshot were shared? |
| Performance engineer | Segmented delay hypotheses with labels | Which segments are observed vs inferred? |
| Data / dashboard practitioner | Debug/freshness notes (WAIKE-adjacent habits) | Is a synthetic series being read as field truth? |
| Educator / facilitator | Rubric scores; misconception prompts | Did learners label fixtures and simulations correctly? |

Portfolio hint: a scrubbed result table with observation / inference / `fixture` labels is more honest than a vibes-based “tests passed so we’re done” claim.

---

## 11. Check understanding {#sec-check}

**Concept.** In one sentence each, distinguish *testing*, *observability*, and *evidence hierarchy*.

**Concept.** In one sentence, explain why **simulation ≠ measurement**.

**System tracing.** Trace a familiar change or send/submit from human claim → oracle/test → signal → labeled inference. Mark observed vs inferred. Name ≥2 evidence conditions (EV-01…EV-06) that had to hold.

**Misconception check.** Why can a full green test suite coexist with a broken human experience?

**Misconception check.** Why must OpenTelemetry be cited as conceptual signal vocabulary here without invented version pins (CLM-CH27-003)?

**Evidence ethics.** What is the difference between LAB-CE06-001 `FIXTURE_VALIDATED` infrastructure and Gate 3 human reader validation? Why are illustrative fixture portfolios not human evidence (CLM-CH27-004)?

**Teach-it-back.** Explain to a newcomer—using LAB-CE06-001 vocabulary—why a green dashboard panel is not automatically a Stability Contract.

**Researcher prompt.** What additional evidence would be required to move a claim from commodity observation toward ITU-T G.1011-aligned assessment—and what remains out of scope for this classroom lab [@itu-t-g1011]?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). CE-6 / CH20 inheritance supplies the evidence hierarchy teaching model; OpenTelemetry conceptual docs supply signal vocabulary; WAIKE adjacency is repository-audited, not invented.

Inline citations used in this chapter include @otel-signals, @itu-t-g1011, @waike-research-ops-ce06, and @wcag22-20241212.

Primary inheritance (link, prefer over duplication): `publication/preproduction/ce-06/`, `publication/full31/chapters/ch27/`, and `labs/LAB-CE06-001/`.

Project-specific honesty: Gate 3 reader evidence remains pending; this working draft is not publication-ready. No Gate 3 files were modified for this draft.

---

## 12. Glossary links {#sec-glossary}

Candidate terms introduced or reinforced here (see also `publication/full31/chapters/ch27/GLOSSARY_CANDIDATES.yaml`; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Testing | Checking claimed behavior with deliberate cases |
| Test oracle | How we know a test outcome matches the experience claim |
| Observability | Ability to ask new questions of a running system via signals |
| Evidence hierarchy | From illustrative aid to stronger measurement methods |
| Observation vs inference | What happened vs what may explain it |
| Evidence redaction | Removing secrets/PII before sharing artifacts |
| Simulation ≠ measurement | Synthetic/teaching setups are not automatically field evidence |
| Signal (OTel sense) | Conceptual family such as traces, metrics, logs [@otel-signals] |
| FIXTURE_VALIDATED | Lab package structurally validated—not Gate 3 human PASS |

Related earlier chapters: observation craft (CH02/CH03), Stability Contract and evidence ladder (CH20 / CE-6), trust and uncertainty (CH23/CH24). Related later chapters: simulation and reproducible research (CH28), portfolio proof (CH30), EMIT capstone expansion (CH31).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured learner or lab evidence. No fabricated telemetry. No product SLO curves. No fake benchmarks as human evidence.

### FIG-CH27-001 — Evidence hierarchy ladder

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Conceptual hierarchy (inherit CE-6 evidence ladder intent).
- **Reader should notice.** Rungs from illustrative aid toward stronger methods; learner labs mid-ladder.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name each rung; deny that classroom fixtures equal G.1011 campaigns.

### FIG-CH27-002 — Test pass vs usable experience

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Comparative.
- **Reader should notice.** Green suite can diverge from human completion.
- **Truth class.** Conceptual.
- **Alt text requirement.** State non-entailment: test pass does not guarantee usable experience.

### FIG-CH27-003 — Signal → observation → inference gate

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Sequence.
- **Reader should notice.** Labels required before causal claims; fixtures marked.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name the gate; forbid reading simulation as measurement.

---

## Claim footnotes used in this chapter (project-specific)

- **CLM-CH27-001.** CE-6 evidence hierarchy is the pedagogical ancestor; learner labs are not ITU-T G.1011 campaigns [@itu-t-g1011].
- **CLM-CH27-002.** WAIKE CLOUD_DEVOPS / DATA_DASHBOARDS labs are adjacent only at audited SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`—do not invent a CH27 observability course ID [@waike-research-ops-ce06].
- **CLM-CH27-003.** Cite OpenTelemetry signals conceptually via `@otel-signals`; no fake version pins [@otel-signals].
- **CLM-CH27-004.** LAB-CE06-001 `FIXTURE_VALIDATED` supports evidence practice; fixtures are not Gate 3 human validation (publication paths under `labs/LAB-CE06-001/` @ accepted-main evidence closure).
