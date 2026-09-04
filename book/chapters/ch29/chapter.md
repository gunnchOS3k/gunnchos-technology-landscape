---
status: draft
chapter_id: CH29
chapter_number: 29
title: "Designing a Complete Technology Product"
author: "Edmund Gunn, Jr."
part: VI
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-CH29-ONEPAGER-001, LAB-CE06-001, LAB-TRUST-001]
figures:
  - FIG-CH29-001
  - FIG-CH29-002
  - FIG-CH29-003
---

# Chapter 29 — Designing a Complete Technology Product

**Status:** `draft` · **Chapter ID:** `CH29`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working draft complete · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does **not** claim Gate 3 PASS; EMIT fixtures and illustrative portfolios are teaching infrastructure, not human reader evidence).

Part VI asks you to build, prove, and contribute. Earlier chapters taught layers in isolation and in pairs: experience maps, stacks, evidence ladders, security/privacy/accessibility gates, and career artifacts. This chapter assembles those pieces into one **complete technology product** story—experience + stack + evidence + responsibility—without marketing language and without inventing shipping claims.

---

## 1. The moment {#sec-ch29-moment}

The demo works. The slide looks finished. The feature lights up on the presenter’s laptop on fast Wi‑Fi. Applause. Then a classmate on a weaker phone, a metered cellular link, or an assistive path tries the same flow. The spinner never resolves. Privacy wording is vague. Accessibility feedback is missing. There is no evidence packet—only confidence.

From the seat: a product that “worked in the demo” failed the **Stability Contract** for real users.

Underneath: incomplete product design. UI chrome was treated as the product. Concurrent conditions, claim boundaries, and inclusion routes were optional garnish.

The governing question for this chapter:

> What must a complete technology product keep true—experience, stack, evidence, security/inclusion, and honest claims—before anyone may say it is usable?

This is not a pitch deck chapter, not a Device Quartet SKU catalog, and not a PMI certification course. Product-management body-of-knowledge citations that would require unverified ISBNs are omitted here (**CLM-CH29-003** remains `SOURCE_NEEDED`; do not invent PMI/ISBN cites). Systems and quality vocabulary come from standards and textbooks already in the bibliography [@iso-iec-25010-2023; @saltzer-kaashoek].

---

## 2. What you notice {#sec-ch29-notice}

Before naming architectures or gates, notice what broke for a person.

You expected a familiar action to finish with clear feedback, understandable privacy, and a path that works on more than the demo machine. Instead you notice: success toast without durable effect; “works here” divergence across devices; a permission prompt that never explains retention; an assistive path that never announces completion; a claim (“ready,” “secure,” “private”) with no evidence plan behind it.

**A polished demo is not a Stability Contract.**

That distinction is the chapter’s first product skill. Demo success is an observation about *one privileged setup*. Usable product experience is a different observation: concurrent conditions hold for the people you claim to serve, and claims stay inside the evidence you actually have.

Optional commodity notice (no specialized gear): pick one feature you already use or built in a prior lab. Write three columns—*demo claim*, *human outcome on your ordinary device*, *evidence you actually hold*. If you cannot reproduce safely, use fixture routes from prior labs (LAB-CE06-001 / LAB-TRUST-001) and mark rows `fixture`. Fixture rows are teaching practice, not Gate validation and not product certification.

---

## 3. Exploded ecosystem {#sec-ch29-ecosystem}

A “complete product” is not a single screen. It is a stack of cooperating layers under a Stability Contract. **FIG-CH29-001** is the first-minute map: human experience at the center; surrounding rings for interaction, application/code, local resources, network path, services/identity, evidence/observability, and society (privacy, equity, accessibility). Treat it as **Representative educational architecture**, not a claim that every product shares one topology [@saltzer-kaashoek].

Walk the layers in ordinary language.

### Human experience and context

Intent, expectation, attention, device class, bandwidth, language, and assistive needs set what “acceptable” means *for this person now*. Software product quality models name characteristics such as usability, performance efficiency, reliability, security, and accessibility-related concerns as related but distinct lenses—useful vocabulary, not a certification of this book or any gunnchOS artifact [@iso-iec-25010-2023].

### Interaction and feedback path

Taps, keys, voice, or assistive technology must be recognized and must produce coherent feedback. A silent AT path can fail the product even when sighted chrome looks finished [@wcag22-20241212].

### Application / code / local state

Handlers, storage, and caches must keep the intended effect durable when the product claims durability. Local success without remote confirmation is a known failure family (CH20 adjacency).

### Network and placement (if remote work is required)

Association, DNS, routing, transport, and cloud placement are different failure domains. Do not collapse them into “the network” as one synonym.

### Identity, authorization, and privacy lifecycle

Who is authenticated, what is authorized, what is collected/retained/shared/deleted. Consent chrome without a lifecycle story is incomplete product design (CE-5 / CH23–CH24 adjacency) [@solove_taxonomy_2006; @nist_sp_800_63_4].

### Evidence and observability

What can be measured, logged (ethically), reproduced, and shown in a portfolio or design review before a ship claim. No evidence plan → no honest “ready.”

### Society and responsibility

Who is excluded when “works on the author’s laptop” is the only gate. Equity and accessibility are product conditions, not appendices [@wcag22-20241212].

**Device Quartet form factors** may appear only as research/learning laboratory lenses across commodity-like form factors. They are **not** commercial product SKUs on accepted evidence (**CLM-CH29-001**; **PHYSICAL_PENDING**) [@src-hardware-quartet].

---

## 4. Follow the signal {#sec-ch29-signal}

Here the “signal” is the product claim’s fate across design gates—not a single demo click. Read the sequence as a logical assembly story. Alternate paths exist; open questions stay labeled undetermined.

1. **Name the human experience.** What does success look like for a person (not for a slide)?
2. **List concurrent conditions.** Which hidden conditions must hold together (Stability Contract)?
3. **Map the stack.** Interaction → code → local resources → path/service → identity/privacy → feedback.
4. **Assign failure domains.** For each fragile step, who owns diagnosis when it breaks?
5. **Write design gates.** Checks that must pass before “ship/usable” language (**FIG-CH29-002**).
6. **Attach an evidence plan.** What will be observed, measured, or fixture-labeled—and what remains unknown?
7. **Draw the claim boundary.** What may the product assert given current evidence (**FIG-CH29-003**)?
8. **Name tradeoffs.** Latency, cost, privacy, power, inclusion—together, not one hero metric.
9. **Secure and include.** Threat, privacy, a11y, equity routes integrated—not bolted on last.
10. **Portfolio handoff.** One-pager + evidence + inclusion routes someone else can review.

### Product assembly without marketing collapse

| Lens | Everyday question | Typical mis-use |
|---|---|---|
| **Experience** | Did the person’s intended action finish with usable feedback? | Treating demo applause as usability |
| **Stack** | Which layers must cooperate for that experience? | Calling UI “the product” |
| **Evidence plan** | What will be tested/measured before claims? | Shipping on vibes |
| **Design gates** | Which checks block “usable/ship” language? | Optional checklists after marketing copy |
| **Claim boundary** | What may we assert given evidence state? | Upgrading planned → implemented silently |
| **Explicit tradeoffs** | What did we sacrifice, and who is excluded? | Optimizing only the presenter laptop |

Layered system design literacy—naming interfaces, dependencies, and failure containment—is older than any one product fashion; use it as discipline, not branding [@saltzer-kaashoek]. Quality-characteristic language helps separate reliability, security, usability, and performance stories so one green demo cannot swallow the rest [@iso-iec-25010-2023].

### Failure branch without drama

Prefer failure *domains* over confident blame: interaction/AT, compute/schedule, memory/storage, network path, service/backend, identity/authz, privacy lifecycle, render/feedback, power/thermal, equity/access. Outside observation rarely distinguishes them cleanly. That limitation belongs on the claim boundary board.

---

## 5. Component cards {#sec-ch29-components}

For each idea: plain language, analogy (labeled), technical function, constraints, common symptoms.

### Complete technology product

- **Plain language.** Experience + stack + evidence + responsibility—not UI alone.
- **Analogy (labeled).** Like a bridge that includes foundations, load rating, inspection records, and who may safely cross—not only a fresh coat of paint.
- **Technical function.** Assembles human outcome, cooperating layers, and honest claims into one design object.
- **Constraints.** Demo success ≠ product completeness; no Device Quartet marketing [@src-hardware-quartet].
- **Symptoms.** “Works in the demo” divergence; missing evidence packet; chrome without durable effect.

### Design gates

- **Plain language.** Checks that must pass before claiming ship/usable.
- **Analogy (labeled).** Like preflight checks—not a promise that the flight will be pleasant, but a refusal to roll without the list.
- **Technical function.** Binds experience acceptance, security/privacy/a11y, and evidence readiness into go/no-go language.
- **Constraints.** Gates are teaching/process tools here—not legal compliance certificates.
- **Symptoms.** Marketing language ahead of gate results; optional “we’ll fix a11y later.”

### Evidence plan

- **Plain language.** What will be measured or tested before claims.
- **Analogy (labeled).** Like a lab notebook outline written *before* the experiment—not a story invented after the poster is printed.
- **Technical function.** Separates observed / inferred / illustrative / fixture / PHYSICAL_PENDING.
- **Constraints.** Fixture-validated lab infrastructure ≠ Gate 3 human validation; n=1 classroom runs ≠ fleet proof.
- **Symptoms.** Empty “metrics” slides; unlabeled illustrative numbers.

### Explicit tradeoffs

- **Plain language.** Latency, cost, privacy, power, and inclusion named together.
- **Analogy (labeled).** Like packing a bag with a fixed volume—each choice displaces another.
- **Technical function.** Forces multi-objective honesty when tuning a product experience [@iso-iec-25010-2023].
- **Constraints.** One hero KPI can hide exclusion; write who loses when you optimize.
- **Symptoms.** “Faster” that breaks AT timing; “cheaper” that forces cloud-only with no fixture route.

### Claim boundary

- **Plain language.** What the product may assert given evidence state.
- **Analogy (labeled).** Like a map legend that marks surveyed roads vs sketched trails.
- **Technical function.** Prevents silent upgrades (planned → implemented; simulated → deployed; alpha → shipping OS).
- **Constraints.** gunnchOS device OS documents claim boundaries and is not a finished shipping OS (`beta_ready` false per project audit language) (**CLM-CH29-002**) [@src-device-os-ce3].
- **Symptoms.** “Production-ready” wording without evidence; Device Quartet described as shipping SKUs (**CLM-CH29-001**).

---

## 6. Stability contract {#sec-ch29-stability}

**Definition (publication teaching model):** a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

**Signature distinction:** a system can remain technically **demo-successful** while the human experience has already **failed** for the people you claim to serve.

This section binds Part VI product assembly to the CE-5/CE-6 responsibility + contract inheritance without inventing numeric product SLOs or marketing Device Quartet readiness.

### How to teach and apply it (eight moves)

1. **Name the human experience** — what success looks like for a person.
2. **List concurrent conditions** — not a single villain metric.
3. **Separate demo chrome from experience outcomes.**
4. **Assign symptoms to failure domains** with evidence gates.
5. **Label every datum** observed / inferred / illustrative / fixture / PHYSICAL_PENDING.
6. **Climb the evidence hierarchy** only as far as tools and ethics allow.
7. **State tradeoffs and who is excluded** when conditions are tuned.
8. **Close with teach-back** — can another person use the one-pager and claim boundary?

### Concurrent conditions (qualitative product anchor)

For a successful product experience under classroom/portfolio scope, conditions such as the following must remain *good enough together* (inherit CE-6 style; qualitative only):

| ID | Hidden condition |
|---|---|
| SC-P01 | Intended human action completable with coherent feedback |
| SC-P02 | Interaction / AT path equivalent enough for claimed users |
| SC-P03 | Local compute/storage responsive enough for claimed durability |
| SC-P04 | Network/service path usable *if* remote work is required |
| SC-P05 | Identity/authorization matches the risk of the action |
| SC-P06 | Privacy lifecycle matches disclosed consent |
| SC-P07 | Security posture matches claim boundary (no silent overclaim) |
| SC-P08 | Evidence plan exists before “usable/ship” language |
| SC-P09 | Explicit tradeoffs named (latency/cost/privacy/power/inclusion) |
| SC-P10 | Equity route exists (fixture / low-bandwidth / no specialized hardware) |

**Numeric humility rule:** use qualitative language where no measured threshold exists. Do **not** invent product SLOs, MOS scores, or Quartet EVT curves as gunnchOS truth.

### CE + lab linkage (link — do not duplicate depth)

- **Whole-book ecosystem model** and **CE-5/CE-6** packages supply responsibility, trust, and Stability Contract inheritance (`publication/preproduction/ce-05/`, `publication/preproduction/ce-06/`).
- **LAB-CE06-001** and **LAB-TRUST-001** remain publication-owned prior artifacts learners may synthesize into a product one-pager. Fixture-validated status on agent branches is **not** Gate 3 PASS.
- **Device Quartet** remains learning-laboratory context only (**PHYSICAL_PENDING**) [@src-hardware-quartet].

**Honesty bound for this edition:** shipping OS / finished product claims for gunnchOS device OS remain out of bounds (`beta_ready` false; claim-boundary teaching only) (**CLM-CH29-002**) [@src-device-os-ce3].

---

## 7. Try it {#sec-ch29-try}

### Proposed LAB-CH29-ONEPAGER-001 — Product one-pager + evidence/inclusion gates

**Goal.** Assemble prior lab artifacts into a non-marketing **product one-pager** that names the experience, stack layers, Stability Contract conditions, design gates (including secure/include), evidence plan, claim boundary, and explicit tradeoffs.

**Status.** `proposed` (publication-owned proposal). Prefer inheriting real prior lab IDs. Do **not** invent WAIKE course/lab IDs. WAIKE accepted `main` (SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`) offers only **adjacent** culture (`capstones/`, `COMM_PD_ETHICS` / `lab_pd_capstone`, `CLOUD_DEVOPS`)—not an exact CH29 module [@src-waike].

**Safety (hard stops).**

- No passwords, tokens, private messages, health data, or classmate PII in portfolios.
- No rooting, jailbreaking, unauthorized scanning, or attacking systems.
- No Device Quartet / specialized RF / EVT hardware required or requested.
- Redact identifiers before any portfolio share.

**Routes.**

- **Route A — Synthesize prior labs.** Pull scrubbed artifacts from LAB-CE06-001 and/or LAB-TRUST-001 (or earlier Part labs you already completed). Build the one-pager fields below.
- **Route F — Fixture fallback (mandatory offline path).** Use illustrative prior-lab fixtures labeled `fixture`. Fixture synthesis is teaching practice, not human evidence and not Gate validation.

**One-pager field set (minimum).**

1. Human experience (one sentence) + who must be able to complete it  
2. Stack layers (5–9 bullets) mapped to failure domains  
3. ≥5 Stability Contract conditions (observed vs guessed)  
4. Design gates checklist including security, privacy, accessibility, equity  
5. Evidence plan (what measured / fixture / still unknown)  
6. Claim boundary (allowed / forbidden wording; PHYSICAL_PENDING badges where needed)  
7. Explicit tradeoffs (name at least two tensions and who might be excluded)  
8. Career artifact note (TPM / systems designer / a11y+privacy co-owner lens)—employment **not** guaranteed  

**Explorer baseline.** Complete fields 1–7 in plain language; teach-back to a peer.

**Operator extension.** Add inspection notes: which gate would fail first on a weaker device or AT path.

**Builder extension.** Turn gates into a reusable checklist someone else can run.

**Engineer extension.** Failure-domain map with test/observability needs per domain; mark instrumentation limits.

**Researcher extension.** List unknowns and PHYSICAL_PENDING items explicitly; state what would move a claim up the evidence hierarchy—without inventing measurements.

**Educator facilitation.** Keep Route F first-class. Score honesty of labels over theatrical demo language.

**Evidence to keep.** One-pager document; scrubbed source artifacts; claim-boundary board; teach-back notes. Completion means artifact-backed claims—not the string PASS.

---

## 8. Build it {#sec-ch29-build}

Extend the one-pager without turning Part VI into a fake product catalog.

### Explorer

Build a pocket card: *demo ≠ usable product*, plus five contract conditions in plain sentences.

### Operator

Build a two-column gate sheet: *claim on the slide* | *evidence we hold*. Add a third column only for inferences, each with “evidence still needed.”

### Builder

Build the full one-pager template filled once for a familiar feature. Optional: a tiny local checklist file (markdown/YAML) that blocks “ready” wording unless evidence-plan and inclusion-route fields are non-empty—never a claim of commercial readiness.

### Engineer

Build a failure-domain map (interaction, compute, storage, path, service, identity, privacy, a11y/equity) with one test or observability need each. Cite quality-characteristic separation so reliability/security/usability do not collapse [@iso-iec-25010-2023].

### Researcher

Build an evidence plan for a claim you are *not* allowed to make yet—for example, Device Quartet physical validation or production OS certification. Keep those **PHYSICAL_PENDING** / claim-boundary limited (**CLM-CH29-001**, **CLM-CH29-002**). Do not invent PMI BoK ISBNs to fill **CLM-CH29-003**.

Educators can facilitate Section 11 teach-backs and keep Route F equitable—not lesser.

---

## 9. Secure and include it {#sec-ch29-secure-include}

**FIG-CH29-002** places secure/include *inside* design gates, not in an appendix after the pitch.

### Security

Threat routes belong in the gate list: spoofed “success,” session confusion, over-broad tokens in screenshots, supply of models/configs. Prefer fixtures and redaction. Unauthorized scanning is out of scope. Do not claim production MDM / certified secure boot for gunnchOS from this chapter’s evidence [@src-device-os-ce3].

### Privacy

Portfolio artifacts must scrub account names, emails, message previews, and location breadcrumbs. Name collect → use → retain → share → delete/redact at product level; a padlock icon is not a lifecycle [@solove_taxonomy_2006]. Identity assurance language, when used, stays within standards vocabulary—not a claim that your classroom app meets a federal profile [@nist_sp_800_63_4].

### Accessibility

Equivalent feedback along assistive or non-pointer paths is a Stability Contract condition. WCAG 2.2 informs teaching intent—not a claim that this book or any gunnchOS product is certified [@wcag22-20241212]. Timing tasks allow extended time; avoid color-only status and flicker-heavy demos.

### Equity

“Works on the author’s laptop on fast Wi‑Fi” is not a product gate. Weaker devices, metered cellular, shared computers, offline contexts, and assistive paths change which concurrent conditions hold. Name who is excluded when optimization assumes one privileged setup. Device Quartet form factors are optional research analogies only—never required lab hardware (**PHYSICAL_PENDING**) [@src-hardware-quartet].

### Safety

Commodity devices only. No RF transmit experiments, no battery abuse, no jailbreaks.

### Ethics

Do not present illustrative fixture numbers as measured human evidence. Do not present fixture-validated lab infrastructure as Gate 3 PASS. Do not invent SLOs, shipping SKUs, or finished-OS claims. Overclaiming measurement is still false evidence. **CLM-CH29-003** product-management BoK cites stay omitted until a verified edition/ISBN is selected.

---

## 10. Career lens {#sec-ch29-career}

One “works in the demo” failure crosses many ownership domains. No table promises employment; roles vary by organization. The product one-pager resembles early professional evidence in miniature: labeled claims, gates, and explicit uncertainty.

| Role family | Typical portfolio evidence | Review questions |
|---|---|---|
| TPM / product engineer | Product one-pager + evidence plan | Did we separate demo from usable outcomes? |
| Systems designer | Failure-domain map | Which layers own which breaks? |
| Accessibility + privacy co-owners | Inclusion/privacy gate checklist | Is a11y/privacy a gate or an appendix? |
| Security engineer (adjacency) | Threat routes on the gate list | What claims exceed evidence? |
| SRE / reliability adjacency | Concurrent-condition notes | Connected/demo-green ≠ usable? |
| Educator / facilitator | Rubric for honest labels | Did learners mark fixture vs observed? |

Portfolio hint: a scrubbed one-pager with claim-boundary badges is more honest than a vibes-based “we’re ready to ship” paragraph. Employment is **not** guaranteed by completing artifacts.

---

## 11. Check understanding {#sec-ch29-check}

**Concept.** In one sentence, define a *complete technology product* so that UI alone cannot satisfy the definition.

**Concept.** In one sentence each, distinguish *design gates*, *evidence plan*, and *claim boundary*.

**System tracing.** Trace a familiar feature from human intent to feedback in numbered steps. Mark observed vs inferred. Name ≥5 Stability Contract conditions that had to hold together for a non-demo user.

**Misconception check.** Why can a feature “work in the demo” while failing real users on weaker devices or AT paths?

**Misconception check.** Why must this chapter refuse Device Quartet shipping-SKU language and finished gunnchOS OS certification language?

**Evidence ethics.** What is the difference between proposed LAB-CH29-ONEPAGER-001 fixture synthesis and Gate 3 human reader validation? Why are illustrative EMIT examples not human evidence?

**Teach-it-back.** Explain to a newcomer—using only this chapter’s vocabulary—why a polished demo is not a Stability Contract.

**Researcher prompt.** What additional evidence would be required to move a Device Quartet or production-OS claim out of PHYSICAL_PENDING / claim-boundary limits—and what remains out of scope for this classroom one-pager?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). Project-specific Device Quartet and device-OS statuses remain constrained by the chapter claim plan (**CLM-CH29-001** PHYSICAL_PENDING; **CLM-CH29-002** claim-boundary teaching). **CLM-CH29-003** (PM BoK) is omitted pending a verified edition/ISBN—no invented PMI cites. Gate 3 reader evidence remains pending; this working draft is not publication-ready.

Inline citations used in this chapter include @iso-iec-25010-2023, @saltzer-kaashoek, @wcag22-20241212, @solove_taxonomy_2006, @nist_sp_800_63_4, @src-hardware-quartet, @src-device-os-ce3, and @src-waike.

Primary inheritance (link, prefer over duplication): `publication/preproduction/ce-05/`, `publication/preproduction/ce-06/`, `labs/LAB-CE06-001/`, `labs/LAB-TRUST-001/`.

---

## 12. Glossary links {#sec-ch29-glossary}

Candidate terms introduced or reinforced here (see also `publication/full31/chapters/ch29/GLOSSARY_CANDIDATES.yaml`; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Complete technology product | Experience + stack + evidence + responsibility, not UI alone |
| Design gates | Checks that must pass before claiming ship/usable |
| Evidence plan | What will be measured/tested before claims |
| Explicit tradeoffs | Latency, cost, privacy, power, inclusion named together |
| Claim boundary | What the product may assert given evidence state |
| Stability Contract | Concurrent hidden conditions that keep an experience alive (book teaching model) |
| Demo ≠ usable | Privileged demo success can coexist with failed real-user outcomes |
| PHYSICAL_PENDING | Physical/hardware validation not yet available—do not upgrade wording |
| Observation vs inference | What happened vs what may explain it |

Related earlier chapters: ecosystem literacy (CH01/CH04), stacks and contracts (CH10/CH20), AI/trust and privacy/a11y (CH21/CH23/CH24), evidence practice (CH26/CH27). Related later chapters: contribution/portfolio (CH30), capstone synthesis (CH31).

---

## Figure references (planned embeds; accessibility metadata)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured learner or lab evidence. No fabricated telemetry. No product SLO curves. **PHYSICAL_PENDING** badges are mandatory where hardware/OS shipping claims would otherwise be implied.

### FIG-CH29-001 — Complete product layers under Stability Contract

- **Type.** Conceptual ecosystem / layered rings (educational original).
- **Reader should notice.** Experience at center; stack + evidence + responsibility rings; not UI alone.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name center and each ring; state conceptual truth class; deny shipping-SKU reading; color never sole cue.

### FIG-CH29-002 — Design gates including secure/include

- **Type.** Conceptual checklist flow.
- **Reader should notice.** Security, privacy, accessibility, and equity sit inside gates—not after marketing copy.
- **Truth class.** Conceptual.
- **Alt text requirement.** List gate families in reading order; state that gates are teaching tools, not legal certification.

### FIG-CH29-003 — Claim boundary board with PHYSICAL_PENDING badges

- **Type.** Conceptual boundary board.
- **Reader should notice.** Allowed vs forbidden wording; PHYSICAL_PENDING for Device Quartet / unfinished OS claims.
- **Truth class.** Conceptual; qualification **PHYSICAL_PENDING** where hardware/OS shipping would be implied.
- **Alt text requirement.** State allowed/forbidden columns and badge meaning; forbid reading the board as a shipping certificate.

---

## Claim footnotes used in this chapter (project-specific)

- **CLM-CH29-001.** Device Quartet form factors are research/learning benchmarks, not commercial product SKUs—**PHYSICAL_PENDING** [@src-hardware-quartet].
- **CLM-CH29-002.** gunnchOS device OS documents claim boundaries and is not a finished shipping OS (`beta_ready` false per CE-5 audit language)—claim-boundary teaching only [@src-device-os-ce3].
- **CLM-CH29-003.** Product-management BoK citations need selection/verification if used beyond pedagogy—**SOURCE_NEEDED**; omitted in this draft (no invented PMI/ISBN).
