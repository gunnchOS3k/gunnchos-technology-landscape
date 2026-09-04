---
status: draft
chapter_id: CH25
chapter_number: 25
author: "Edmund Gunn, Jr."
part: V
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-CE06-001]
figures:
  - FIG-CH25-001
  - FIG-CH25-002
  - FIG-CH25-003
---

# Chapter 25 — Digital Equity: Who Benefits, Who Is Excluded, and What We Can Measure

**Status:** `draft` · **Chapter ID:** `CH25`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working draft complete · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does **not** claim Gate 3 PASS; EMIT fixtures and illustrative portfolios are teaching infrastructure, not human reader evidence).

Part V asks who is protected, who is served, and who is quietly left out. Chapter 20 already treated accessibility and equity as Stability Contract conditions. Chapter 24 widens privacy, identity, safety, and ethics. This chapter makes **digital equity** the primary measurement problem: who can complete an experience, who cannot, and which claims are observed versus assumed. It inherits CE-6 equity/accessibility seeds and LAB-CE06-001 portfolio fields—deepening measurement discipline without fabricating population studies (CLM-CH25-001).

---

## 1. The moment {#sec-ch25-moment}

Two peers attempt the same task. One finishes on a strong device and a stable link. The other stalls: cheaper hardware, metered cellular, shared computer time, denser language, or an assistive path that never announces “done.” From the author’s seat the product looks fine. From the second seat the experience never existed.

That divergence is not a personality flaw. It is a systems fact.

**Digital equity**, in this book’s teaching sense, means asking who can benefit from a technology experience and who is excluded—then separating what we measured from what we merely hoped. Marketing “inclusive for everyone” language is not evidence. A green connected icon is not evidence that *this person* completed *this action* under *these constraints*.

The governing question for this chapter:

> Who can complete this experience—and who is excluded—and what evidence do we actually have?

This is not a census chapter, not a WCAG certification course, and not a Device Quartet marketing sheet. Official ICT access statistics exist and matter [@itu-facts-figures-2025]; classroom portfolios still cannot invent national percentages. Accessibility standards inform intent [@wcag22-20241212]; labs do not certify products.

---

## 2. What you notice {#sec-ch25-notice}

Before naming “digital divide” numbers, notice the human contract that broke for one person and held for another.

You expected a familiar action to finish for both peers. Instead you notice: spinner longevity on one device only; success toast without durable effect on a weaker link; keyboard or screen-reader silence while the pointer path looks busy; a download that burns a metered plan; a disclosure wall written above the literacy the lab assumes; or a “required” specialized tool that one learner cannot afford.

**Works-for-me is not a Stability Contract.**

That distinction is the chapter’s first systems skill (CE-6 equity seed). Status chrome, author demos, and privileged lab setups answer narrow questions. Completion under declared constraints answers a different question. Collapsing them produces confident wrong inclusion claims: “everyone can do this,” “the lab is accessible,” “offline is just for beginners,” as if those were measured.

Optional commodity notice (no specialized gear): pick one familiar send/submit/sync or lab step. Attempt it once under your usual setup, then once under a *declared* constraint you already have access to—phone-only, throttled/metered link, keyboard-only, or fixture fallback. Write three columns before you invent a cause: *who completed*, *what differed in the visible experience*, *what remains unobserved*. If live comparison is unsafe, inequitable, or metered-expensive, use LAB-CE06-001 Route F and mark rows `fixture`. Fixture rows are teaching practice, not human equity evidence and not Gate validation.

---

## 3. Exploded ecosystem {#sec-ch25-ecosystem}

Exclusion is rarely a single broken widget. It is a path through an ecosystem where one privileged configuration can hide concurrent failures. **FIG-CH25-001** is the first-minute map: same task, divergent completion across constraints. Treat it as **Representative educational architecture**, not a claim that every product fails the same way.

Walk the layers in ordinary language.

### Human and context

Intent, time available, language, literacy, caregiving load, and classroom power shape what “acceptable” means *for this person now*. A peer who finishes quickly may simply have been granted a softer contract.

### Device and form factor

Screen size, CPU/memory headroom, battery state, and input modalities change which paths are usable. Device Quartet form factors may appear as learning lenses only; multi-form-factor equity benches remain **PHYSICAL_PENDING** (CLM-CH25-004) [@src-hardware-quartet].

### Cost and ownership

Shared devices, prepaid data, no paid cloud account, and no specialized lab kit are first-class conditions—not excuses. Offline/fixture completion is an **equity feature**, not a lesser path (CE-6).

### Network path

Association can look fine while bandwidth, latency, captive portals, or intermittent campus Wi‑Fi break completion. Metered cellular changes which “just refresh” advice is ethical.

### Application / service assumptions

Pointer-first UI, English-dense disclosures, DevTools-only diagnosis, always-on broadband, and “bring your laptop” are design choices with exclusion consequences.

### Accessibility / alternate path

Equivalent feedback along keyboard, switch, captions, or screen-reader paths is a Stability Contract condition (SC-10), not a garnish [@wcag22-20241212].

### Evidence and governance

How teams label observations, what they publish as “inclusive,” and what privacy they demand from comparative notes all shape who can safely participate in measurement itself.

**FIG-CH25-003** groups exclusion mechanism cards—device, cost, bandwidth, accessibility, language/literacy, policy—so readers stop treating “Wi‑Fi” as a synonym for every exclusion.

---

## 4. Follow the signal {#sec-ch25-signal}

Here the “signal” is the human task’s fate across privileged and constrained seats—not a single ping. Read the sequence as a logical equity-diagnosis story. Alternate paths exist; open questions stay labeled undetermined.

1. **Declare the task.** What counts as completion for a person (not for a status icon)?
2. **Declare the route.** Strong-device / strong-link; phone-first; low-bandwidth; assistive; fixture/offline.
3. **Observe seat A.** Record status chrome *and* human outcome separately.
4. **Observe seat B (or constrained self-run).** Same task; different declared constraints.
5. **Diff the experience.** What diverged: device class, connectivity class, assistive-path status, cost/time pressure, language load?
6. **Assign exclusion mechanisms** without over-causal certainty.
7. **Label every datum.** Observed / inferred / illustrative / fixture / population-claim (blocked unless sourced).
8. **Decide the next honest move.** Measure more, qualify the claim, or redesign a constrained completion route.

### Evidence labels for equity claims

**FIG-CH25-002** and CE-6’s evidence ladder teach the same honesty:

| Label | Means | Equity misuse to refuse |
|---|---|---|
| **Observed** | You saw/heard/recorded it under declared conditions | Promoting one seat into “everyone” |
| **Inferred** | A plausible explanation still needing evidence | Treating inference as measured inclusion |
| **Illustrative** | Teaching aid, not learner or population evidence | Pasting into “our users can…” |
| **Fixture** | Supplied lab data for offline/equity routes | Claiming fixture timings as peer study results |
| **Population-claim** | National/global statistical assertion | Inventing census percentages (CLM-CH25-003) |

Official ICT access statistics are the right class of source for population claims when you later cite **specific tables** from a verified edition [@itu-facts-figures-2025]. Until those table citations are in hand, keep population claims blocked in portfolios. Classroom n=1 or n=2 peer notes are *local observations*, not digital-divide epidemiology.

### Failure branch without humiliation

Prefer exclusion *mechanisms* over blaming individuals: device class, cost, bandwidth/metering, skill/tooling assumptions, language/literacy load, disability/AT path gaps, policy/account requirements. Outside observation rarely isolates one mechanism cleanly. That limitation is literacy.

---

## 5. Component cards {#sec-ch25-components}

For each idea: plain language, analogy (labeled), technical function, constraints, common symptoms.

### Digital equity

- **Plain language.** Who can benefit from a technology experience and who is excluded.
- **Analogy (labeled).** Like asking whether a bridge works for walkers, wheelchairs, and night travelers—not only for the designer’s car at noon.
- **Technical function.** Centers completion and exclusion as first-class systems questions alongside latency and security.
- **Constraints.** Not a synonym for “be nice”; not automatic proof from marketing copy.
- **Symptoms.** Peer divergence; works-for-me blindness; inclusive claims without labeled evidence.

### Exclusion mechanism

- **Plain language.** A concrete barrier family—device, cost, bandwidth, skill/tooling, language, disability/AT path, policy.
- **Analogy (labeled).** Like locked doors with different keys—naming the lock beats shouting “access problem.”
- **Technical function.** Gives diagnosis vocabulary so Improve plans target a barrier, not a stereotype.
- **Constraints.** Multiple mechanisms often co-occur; one lab run ≠ mechanism census.
- **Symptoms.** Task impossible without paid API, laptop, DevTools, fluent English disclosure, or pointer-only UI.

### Measurable inclusion signals

- **Plain language.** Observations you can collect without inventing population statistics.
- **Analogy (labeled).** Like a checklist of whether the door opened for *these* people *today*—not a national housing survey.
- **Technical function.** Operationalizes equity as recordable fields: completion yes/no, device/connectivity class, assistive-path status, route used, evidence labels.
- **Constraints.** Local signals ≠ national ICT indicators [@itu-facts-figures-2025].
- **Symptoms.** Portfolios full of vibes (“pretty inclusive”) with no completion rows.

### Constrained completion route

- **Plain language.** A path that works without specialized hardware or paid APIs—often phone-first, low-bandwidth, or fixture/offline.
- **Analogy (labeled).** Like a marked accessible entrance—not a service elevator treated as second-class.
- **Technical function.** Makes equity actionable in labs: Route F / fixture fallback is first-class (CE-6; CLM-CH25-002 adjacency to WAIKE phone-first / low-cost intent) [@src-waike; @waike-research-ops-ce06].
- **Constraints.** A route’s existence is not WCAG certification [@wcag22-20241212].
- **Symptoms.** “Optional offline” framed as failure; labs that cannot finish without paid cloud.

### Honest evidence labeling

- **Plain language.** Distinguishing observed / inferred / illustrative / fixture / population-claim so equity language cannot launder uncertainty.
- **Analogy (labeled).** Like food labels—ingredients listed beat “probably healthy.”
- **Technical function.** Extends observation-vs-inference craft into inclusion claims (CLM-CH25-001).
- **Constraints.** Labels do not replace ethics; redaction still required for peer comparisons.
- **Symptoms.** Fixture examples cited as human validation; Gate infrastructure confused with Gate PASS.

### Accessibility path (contract condition)

- **Plain language.** Equivalent feedback and completion along non-pointer / assistive routes.
- **Analogy (labeled).** Like captions that carry the same punchline—not a silent film for some seats.
- **Technical function.** SC-10 in the Stability Contract list; WCAG 2.2 informs teaching intent only [@wcag22-20241212].
- **Constraints.** Intent ≠ product certification; Explorer path must work without DevTools (CE-6).
- **Symptoms.** Color-only status; completion never announced to AT; timing tasks with no extended-time option.

---

## 6. Stability contract {#sec-ch25-stability}

**Definition (publication teaching model):** a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

**Signature distinction for this chapter:** a system can remain “fine on the author’s setup” while the human experience has already **failed for someone else**.

### Equity-specific contract conditions (chapter focus)

Inherit CE-6 concurrent conditions (SC-01…SC-11), then emphasize these measurable inclusion conditions for CH25:

| Condition | Honest test question |
|---|---|
| Task completion under constrained device/network/assistive conditions | Did a declared constrained route finish for a person? |
| Cost and bandwidth barriers within declared lab routes | Was paid cloud / specialized kit / heavy download required? |
| Language/literacy of disclosures usable | Could a newcomer act on the disclosure without decoding jargon walls? |
| Evidence labels prevent overclaiming “inclusive for all” | Is every inclusion sentence tagged observed / inferred / illustrative / fixture? |
| Accessibility path equivalent feedback | Was completion perceivable without pointer-only cues [@wcag22-20241212]? |
| Privacy of comparative evidence | Are peer identifiers redacted before share? |

**Numeric humility rule:** do **not** invent inclusion percentages, “accessibility scores,” or Device Quartet marketing curves. Official statistics belong only with verified table citations [@itu-facts-figures-2025]. Qualitative language is required where unmeasured.

### CE-6 + LAB-CE06-001 linkage

- **CE-6 preproduction** (`publication/preproduction/ce-06/`), especially `SECURITY_EQUITY_ACCESSIBILITY.md` and the Stability Contract model, is the primary inheritance package: equity as contract condition, offline/fixture as equity feature, phone-first Explorer routes, and Improve-plan “who benefits / who is left out?” checks.
- **LAB-CE06-001** supplies publication-owned EMIT portfolio fields including `portfolio/equity_societal_impact.md`. Status on accepted infrastructure: **`FIXTURE_VALIDATED`**. That means structural templates and validators exist. It does **not** mean Gate 3 PASS. It does **not** mean illustrative EMIT examples are human equity evidence (CLM-CH25-001).

**Honesty bound for this edition:** Device Quartet multi-form-factor equity measurements remain **PHYSICAL_PENDING** (CLM-CH25-004) [@src-hardware-quartet]. WAIKE `ACCESSIBILITY_AND_LOW_COST.md` is adjacent intent evidence—not a11y certification and not checklist-complete proof (CLM-CH25-002) [@src-waike; @waike-research-ops-ce06].

---

## 7. Try it {#sec-ch25-try}

### LAB-CE06-001 — Equity fields inside EMIT (inherit)

**Goal.** Reuse the publication-owned EMIT capstone to practice equity measurement: explain who completed, measure what is observable under declared constraints, propose one inclusion-minded Improve, and teach the difference between observed exclusion and assumed universality.

**Proposed pair lab.** `LAB-CH25-PAIR-001` (paired constrained-route worksheet) remains **proposed** in the chapter packet—do not invent a WAIKE ID for it. Until authored, complete equity practice inside LAB-CE06-001.

**WAIKE alignment note.** WAIKE accepted `main` (SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`) includes adjacent docs and labs (`ACCESSIBILITY_AND_LOW_COST.md`, `COMM_PD_ETHICS` / `lab_accessibility_comm`, capstone portfolio culture). Those are adjacencies. There is **no** exact WAIKE module named DIGITAL_EQUITY / CH25.

**Safety (hard stops).**

- No passwords, tokens, private messages, health data, or classmate PII in portfolios; redact peer comparisons.
- No rooting, jailbreaking, unauthorized scanning, social-engineering classmates, or attacking systems.
- Prefer owned devices, benign demos, or supplied fixtures; heed metered-data warnings.
- No Device Quartet / specialized RF / EVT hardware required or requested.

**Routes.**

- **Route A — Dual-seat notice.** Same task; two constraint classes you already can access (or self + one constrained re-run). Log device class, connectivity class, assistive-path status, completion yes/no.
- **Route B — Status vs outcome.** Keep CH20 discipline: OS/connectivity chrome *separate* from human completion.
- **Route F — Fixture fallback (mandatory offline/equity path).** Use LAB-CE06-001 fixtures; mark `fixture`. Study illustrative examples only as **ILLUSTRATIVE ONLY — not human evidence**.

**Explorer baseline.**

1. Name who succeeded/failed and what differed in the visible experience.
2. Fill `equity_societal_impact.md`: assumption → who might be excluded → mitigation idea.
3. Label every row observed / inferred / fixture.
4. Refuse any invented population percentage.
5. Produce teach-back a peer could use: “works on my machine ≠ inclusive.”

**Operator extension.** Log device class, connectivity class, and assistive-path status as observations for ≥2 declared routes; add one comparison table.

**Builder extension.** Add or document one low-bandwidth / no-specialized-hardware completion route for a toy step; note tradeoffs.

**Engineer extension.** Propose one measurable inclusion metric with explicit limitations (no fake benchmarks); place it on the evidence hierarchy.

**Researcher extension.** Design a small comparative study plan separating observation from inference; list confounders; cite what official ICT statistics would require that this lab does not provide [@itu-facts-figures-2025]. Keep Quartet claims PHYSICAL_PENDING.

**Educator facilitation.** Prefer Route F when live dual-seat capture is inequitable or unsafe; treat fixture completion as first-class.

**Evidence to keep.** Equity portfolio fields; scrubbed comparison notes; teach-back. Validator discipline from LAB-CE06-001 applies. Completion means artifact-backed claims—not a bare exit code and not the string PASS.

---

## 8. Build it {#sec-ch25-build}

Extend equity practice without turning Part V into invented benchmarks.

### Explorer

Build a pocket card: *works-for-me ≠ inclusive*, plus five exclusion mechanism names in plain sentences.

### Operator

Build a three-column sheet: constraint class | completion observation | evidence label. No fourth column for vibes.

### Builder

Build a one-page constrained-route stub: phone-first or fixture steps, predicted who benefits / who is still left out, and qualitative success criteria you could observe without specialized kit. Align with WAIKE phone-first / low-cost *intent* without claiming certification [@src-waike].

### Engineer

Build an inclusion-metric proposal that ends in limitations: sample size, selection bias, AT coverage gaps, and “needs official statistics / specific ITU table citation before population language” [@itu-facts-figures-2025]. Optional: map metric to SC-10 / cost / bandwidth conditions.

### Researcher

Build an evidence plan for a claim you are *not* allowed to make yet—for example, “this lab is accessible to all students nationwide” or “Device Quartet proves inclusive hardware.” Specify what physical or statistical evidence would be required; keep Quartet **PHYSICAL_PENDING** (CLM-CH25-004). Do not invent DOIs or census numbers.

Educators can facilitate Section 11 teach-backs and keep Route F as a first-class equitable path—not a lesser path.

---

## 9. Secure and include it {#sec-ch25-secure-include}

### Security

Comparative screenshots, HAR exports, and retry logs can leak tokens and identifiers. Prefer fixtures and redaction. Do not capture others’ screens without consent. Unauthorized scanning is out of scope.

### Privacy

Peer equity comparisons are sensitive. Scrub names, faces, handle strings, message previews, and precise location. Distinguish measurement-for-learning from surveillance. Metered-link learners must not be forced into expensive live captures—Route F exists for equity and privacy together.

### Accessibility

Document whether completion was announced along assistive paths; do not rely on color-only status. WCAG 2.2 informs teaching intent—not a claim that this book, LAB-CE06-001, or any gunnchOS product is certified [@wcag22-20241212]. Timing tasks allow extended time; avoid flicker-heavy demos. Explorer diagnosis must work without DevTools (CE-6).

### Equity (primary depth)

Strong-device / strong-link authors can falsely conclude the contract is fine. Metered data, shared devices, older hardware, intermittent connectivity, language load, and missing AT equivalence change acceptable bounds. Offline/fixture fallback is an equity feature. Improve plans that boost an author’s metrics while excluding people fail the inclusion test even if a spinner got shorter. Name who benefits and who is left out when “optimization” assumes one privileged setup. Device Quartet analogies stay optional and non-required (PHYSICAL_PENDING).

### Safety

Commodity devices only. No RF transmit experiments, no battery abuse, no jailbreaks, no social-engineering classmates “to test equity.”

### Ethics

Do not present illustrative fixture numbers as measured human evidence. Do not present `FIXTURE_VALIDATED` as Gate 3 PASS. Do not invent inclusion percentages, a11y certification badges, or Quartet EVT inclusivity curves. Overclaiming measurement is still false evidence—and it harms the people your claim pretended to include.

---

## 10. Career lens {#sec-ch25-career}

Equity work crosses product, research, policy, and education. No table promises employment; roles vary by organization. LAB-CE06-001 equity fields resemble early professional evidence in miniature: labeled observations, constrained-route notes, and explicit uncertainty.

| Role lens | Typical artifacts | Review questions |
|---|---|---|
| Digital equity researcher / policy analyst | Exclusion measurement plan; sourced statistical citations | Are population claims table-cited or blocked? |
| Product inclusion lead | Constrained-route completion evidence; Improve tradeoff notes | Did “ship faster” erase a route? |
| Accessibility specialist | AT pathway writeup; SC-10 evidence | Equivalent feedback—or color-only chrome? |
| SRE / performance | Connected≠usable notes under multiple constraint classes | Whose latency budget was optimized? |
| Educator / facilitator | No-device / fixture adaptation note; misconception prompts | Is Route F treated as first-class? |
| Trust & safety / privacy | Redaction checklist for comparative studies | Did measurement become surveillance? |

Portfolio hint: a scrubbed two-seat completion table with evidence labels is more honest than a vibes-based “our product is inclusive” claim.

---

## 11. Check understanding {#sec-ch25-check}

**Concept.** In one sentence, define *digital equity* so that it requires asking who is excluded—not only who is delighted.

**Concept.** Name three *exclusion mechanisms* and one measurable signal you could record for each without inventing population statistics.

**System tracing.** Trace the same task for two constraint classes in numbered steps. Mark observed vs inferred. Name ≥4 Stability Contract / inclusion conditions that had to hold together.

**Misconception check.** Why is “it works on my laptop on fast Wi‑Fi” not evidence that a lab is inclusive?

**Misconception check.** Why must this chapter refuse invented census percentages even while pointing readers at ITU Facts and Figures [@itu-facts-figures-2025]?

**Evidence ethics.** What is the difference between LAB-CE06-001 `FIXTURE_VALIDATED` infrastructure and Gate 3 human reader validation? Why are illustrative EMIT portfolios not human equity evidence?

**Teach-it-back.** Explain to a newcomer why a constrained completion route (fixture/offline/phone-first) is an equity feature, not a lesser path.

**Researcher prompt.** What additional evidence would be required to move from a two-seat classroom observation to a responsible population-level ICT access claim—and what remains out of scope for this lab [@itu-facts-figures-2025]?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). CE-6 chapter-local proposals informed promotion of `itu-facts-figures-2025` for CH25. Project-specific Device Quartet equity status remains **PHYSICAL_PENDING** in the chapter claim plan (CLM-CH25-004). Gate 3 reader evidence remains pending; this working draft is not publication-ready.

Inline citations used in this chapter include @itu-facts-figures-2025, @wcag22-20241212, @src-waike, @waike-research-ops-ce06, and @src-hardware-quartet.

Primary inheritance (link, prefer over duplication): `publication/preproduction/ce-06/` (especially `SECURITY_EQUITY_ACCESSIBILITY.md`, `STABILITY_CONTRACT.md`) and `labs/LAB-CE06-001/` (especially `portfolio/equity_societal_impact.md`).

---

## 12. Glossary links {#sec-ch25-glossary}

Candidate terms introduced or reinforced here (see also chapter glossary candidates; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Digital equity | Who can benefit from a technology experience and who is excluded |
| Exclusion mechanism | Device, cost, bandwidth, skill, language, disability, or policy barrier |
| Measurable inclusion signals | Observations collectable without inventing population stats |
| Constrained completion route | Path that works without specialized hardware or paid APIs |
| Honest evidence labeling | Observed / inferred / illustrative / fixture / population-claim distinctions |
| Accessibility path | Equivalent feedback/completion along assistive or non-pointer routes |
| Stability Contract | Concurrent hidden conditions that keep an experience alive (book teaching model) |
| Works-for-me ≠ inclusive | Author-seat success does not entail completion for others |
| Fixture as equity feature | Offline/supplied-data routes that keep constrained learners included |
| Observation vs inference | What happened vs what may explain it |

Related earlier chapters: experience-first observation craft (CH02/CH03), QoE and Stability Contract depth (CH20), privacy/identity/safety/accessibility ethics (CH24), CE-6 Concept Edition seeds. Related later chapters: evidence practice (CH27), careers and contribution (CH30), EMIT / responsibility capstone (CH31).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured learner or lab evidence. No fabricated telemetry. No invented inclusion percentages. No Device Quartet marketing curves.

### FIG-CH25-001 — Same task; divergent completion

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Comparative (planned).
- **Reader should notice.** Same task; divergent completion across constraints.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name both seats and at least one differing constraint; state conceptual truth class; deny population statistics.

### FIG-CH25-002 — Evidence labels for equity claims

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Hierarchy (planned).
- **Reader should notice.** Observed / inferred / illustrative / fixture / population-claim ladder.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name each label and one misuse to refuse; color never sole cue.

### FIG-CH25-003 — Exclusion mechanism cards

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Map / card set (planned).
- **Reader should notice.** Device, cost, bandwidth, accessibility, language (and related) mechanism families.
- **Truth class.** Illustrative.
- **Alt text requirement.** List mechanism card titles in text; deny that the set is exhaustive census evidence.

---

## Claim footnotes used in this chapter (project-specific)

- **CLM-CH25-001.** CE-6 / LAB-CE06-001 plant equity and accessibility as Stability Contract conditions; CH25 deepens measurement without fabricating population studies—do not treat illustrative EMIT examples as human equity evidence.
- **CLM-CH25-002.** WAIKE `ACCESSIBILITY_AND_LOW_COST.md` documents phone-first / low-cost intent (adjacency); checklist completeness and a11y certification must not be overclaimed [@src-waike; @waike-research-ops-ce06].
- **CLM-CH25-003.** Primary digital-divide / ICT access statistics for national or global claims require verified official sources; cite specific ITU Facts and Figures tables before quoting numbers—do not invent census percentages [@itu-facts-figures-2025].
- **CLM-CH25-004.** Device Quartet multi-form-factor equity measurements are **PHYSICAL_PENDING**; form factors may be learning lenses only—not shipping inclusivity marketing [@src-hardware-quartet].
