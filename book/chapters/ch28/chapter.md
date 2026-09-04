---
status: draft
chapter_id: CH28
chapter_number: 28
author: "Edmund Gunn, Jr."
part: VI
concept_edition: false
inherits_from: [CE-6]
labs: [LAB-CE06-001]
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
gate_note: "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING (no Gate 3 PASS claimed)"
figures:
  - FIG-CH28-001
  - FIG-CH28-002
  - FIG-CH28-003
---

# Chapter 28 — Digital Twins, Simulation, and Reproducible Research {#ch28}

**Status:** `draft` · **Chapter ID:** `CH28`  
**Author:** Edmund Gunn, Jr.  
**Inheritance:** CE-6 measurement and limitation habits; WAIKE `reproducible_research` catalog adjacency  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does **not** claim Gate 3 PASS; fixtures and illustrative portfolios are never human reader validation)

Part VI asks you to build, prove, and contribute. Chapter 27 named testing, observability, and evidence. This chapter refuses two quiet upgrades that break research honesty: treating any computational stand-in as if it were the measured world, and treating a one-machine result as if peers could regenerate it without pinned inputs. The governing skill is **bounded stand-ins plus declared reproduction**.

---

## 1. The moment {#ch28-moment}

A simulation says the design is fine. The team ships confidence. Then the real device path, network path, or classroom fixture disagrees—timeouts, thermal throttling, a sensor that never arrives, a peer who cannot regenerate the table you published in the shared notebook.

Or the opposite seat: everything “worked on my laptop.” No SHA. No seed. No fixture ID. A classmate opens the same repo a week later and gets a different plot. Nobody lied on purpose. The environment was never declared.

From the seat: contradiction between a model story and a lived outcome—or between a claimed result and a failed regeneration.

Underneath: a **simulation** is a computational stand-in for *selected* real behaviors. A **digital twin**, in the teaching sense used here, is not “any model with a fancy name.” It is a maintained pairing between a model and a real or planned system, with update rules and **validity bounds**—where the stand-in is trusted, and where it is not. Standards language for manufacturing digital-twin frameworks exists; this book cites ISO 23247-1 as an overview of that framework family without inventing clause-level fidelity scores or product twin grades [@iso-23247-1-2021].

The governing question for this chapter:

> When a stand-in says “fine” while the world (or a peer’s regeneration) says otherwise—what kind of stand-in were we using, what bounds did we declare, and what SHA, fixture, and seed would make the claim reproducible?

This is not a CAD marketing chapter, not a Device Quartet product-twin validation report, and not permission to promote teaching fixtures into physical proof.

---

## 2. What you notice {#ch28-notice}

Before twin vocabulary or reproducibility cards, notice the human contract that broke.

You expected the model’s green light to predict the experience you can feel—or you expected a classmate to regenerate your table from what you shared. Instead you notice: a demo that only works on one machine; a plot that changes when someone else runs it; a “digital twin” slide that never states how often the model is updated from the real system; a fixture CSV treated as if a sensor farm measured it; assistive or commodity paths that never appear in the simulated story.

**A simulation can be useful and still wrong for the decision you are making. A twin is not an ordinary static model with better branding. A fixture is a teaching or measurement stand-in unless labeled otherwise.**

Notice the evidence split. Outside observation: the simulation printed “pass,” the spinner finished, the notebook rendered a table. Inference: “therefore the physical unit will pass,” or “therefore anyone can reproduce this.” Those inferences need declared bounds, inputs, and environment—or they stay labeled guesses (CLM-CH28-004).

Optional commodity notice (no specialized twin platform required): pick one small computational experiment you already have—a script, a notebook cell, or a CE lab fixture route. Write three columns before you upgrade language: (1) what the stand-in claimed, (2) what a human could observe without trusting the claim, (3) what is still unpinned (code SHA, data fixture ID, seed, OS/runtime). If you use LAB-CE06-001 fixture timings, mark rows `fixture`. Fixture outputs are illustrative teaching data unless a later measured label applies—they never become Gate evidence by themselves.

---

## 3. Exploded ecosystem {#ch28-ecosystem}

A disputed simulation or a failed reproduction is not a single object. It is a path through an ecosystem. **FIG-CH28-001** separates the simulated/twin story from the measured world. Treat it as **Representative educational architecture**, not a claim that every lab or plant looks like the diagram.

Walk the layers in ordinary language.

### Human and decision context

Someone is trying to learn, design, debug, or publish. Acceptable risk depends on the decision: classroom teach-back is not plant commissioning. Validity bounds are decision-relative; inventing universal twin “fidelity percentages” as gunnchOS truth is forbidden.

### Question and claim

What is being asked of the stand-in? Predict latency? Check a thermal envelope? Regenerate a table? Vague questions produce vague upgrades from illustrative to “proven.”

### Model / simulation

Code and assumptions that approximate selected behaviors. Useful when the selected behaviors match the decision. Dangerous when the omitted behaviors are exactly the ones that break the human experience.

### Twin pairing and update path (when claimed)

If you say **digital twin**, you imply a maintained relationship to a real or planned system—not a one-shot offline sketch. Manufacturing-oriented twin frameworks discuss overview principles for that relationship; cite the standard family’s overview carefully and do not invent unimplemented update rates or accuracy grades [@iso-23247-1-2021]. Teaching twins of Device Quartet research form factors remain conceptual / **PHYSICAL_PENDING** until measured validation exists [@src-hardware-quartet] (CLM-CH28-003).

### Inputs, fixtures, and seeds

Data files, synthetic traces, random seeds, and lab fixtures. Deterministic teaching aids are allowed—and must be labeled. CE lab fixtures across the publication are illustrative or deterministic teaching aids unless explicitly labeled measured (CLM-CH28-004).

### Compute and runtime environment

Language version, libraries, OS, container image digest, hardware class. “Works on my laptop” is an environment claim, not a result claim.

### Observation and instrumentation

Logs, plots, status chrome, assistive announcements. Observation vs inference remains CE-6 / CH27 craft: what happened is not automatically why it happened [@gunnchos-technology-landscape-ce06].

### Peer regeneration path

Another person (or future you) with the declared inputs. Reproducible research, in the teaching sense here, means others can regenerate results from declared inputs and environment—not that every paper in the wild already meets a guide we have not yet pinned (`repro_research_guide` remains **SOURCE_NEEDED**; do not invent a peer-reviewed citation).

### Society / equity / access

Who can run the stand-in? Who is excluded by specialized software, paid twin platforms, or unlabeled personal data inside a “demo”? Commodity and fixture routes are equity conditions, not optional garnish.

**FIG-CH28-003** is the validity-bounds annulus: trusted inside a declared ring; unlabeled outside.

---

## 4. Follow the signal {#ch28-signal}

Here the “signal” is the fate of a claim that travels from human question through stand-in to peer regeneration—not a single radio packet. Read the sequence as a logical honesty path. Alternate routes exist; open questions stay undetermined.

1. **Intent.** A person asks a decision-shaped question (will this stall? can a peer regenerate this table?).
2. **Stand-in choice.** Simulation, twin-paired model, fixture, or live measurement—named honestly.
3. **Bounds declaration.** Where the stand-in is trusted; where it is not.
4. **Input pin.** Code SHA, fixture ID, seed, config hashes—as applicable.
5. **Execution.** Compute runs; outputs appear.
6. **Labeling.** Illustrative / fixture / commodity observation / measured—chosen to match evidence.
7. **Comparison (optional).** Live path or second environment—if ethically and practically available.
8. **Peer attempt.** Another seat regenerates from the card—or fails, which is also evidence.
9. **Human judgment.** Decision allowed, deferred, or rejected; language upgraded only as far as evidence reaches.

### Stand-in families without collapse

| Family | Everyday question | Typical mis-use |
|---|---|---|
| **Ordinary model** | What simplified story helps me think? | Calling every model a twin |
| **Simulation** | What happens under selected assumed behaviors? | Treating selected behaviors as the whole world |
| **Digital twin (teaching sense)** | What maintained pairing + update/validity rules bind model to system? | Inventing fidelity scores; skipping update rules [@iso-23247-1-2021] |
| **Fixture** | What deterministic stand-in keeps the lab fair? | Promoting fixture rows to physical proof |
| **Measured run** | What did this instrumented attempt observe? | One n=1 run as universal product truth |
| **Reproducible package** | Can a peer regenerate from declared pins? | Sharing plots without SHA/fixture/seed |

A digital twin is not an ordinary model. The difference is the maintained pairing and the declared bounds—not the marketing adjective (CLM-CH28-002).

### Evidence hierarchy (climb only as far as tools and ethics allow)

1. Illustrative teaching aid (labeled)
2. Fixture / deterministic lab stand-in (labeled `fixture`)
3. Commodity observation on a device you already own
4. Instrumented local run with pinned SHA and seeds
5. Peer regeneration from the reproducibility card
6. Standards-aligned twin or measurement practice in a real domain—**not** required for classroom completion; manufacturing twin framework overview is vocabulary, not a classroom certification [@iso-23247-1-2021]

Learner labs sit mid-ladder. Invented twin fidelity dashboards and fake Gate validation do not belong in Explorer portfolios.

---

## 5. Component cards {#ch28-components}

For each idea: plain language, analogy (labeled), technical function, constraints, common symptoms.

### Simulation

- **Plain language.** A computational stand-in for selected real behaviors.
- **Analogy (labeled).** Like a flight-training scenario that practices some weather—not a claim that every real storm was flown.
- **Technical function.** Explores consequences under declared assumptions.
- **Constraints.** Omitted physics, policy, or human paths can be exactly what fails later.
- **Symptoms.** Green sim / failed live path; overconfident “proved in simulation” language.

### Digital twin (teaching sense)

- **Plain language.** A maintained model paired to a real or planned system with update and validity rules.
- **Analogy (labeled).** Like a living map that must be redrawn when the city changes—not a postcard from last summer.
- **Technical function.** Names pairing, update expectations, and bounds; manufacturing twin framework overviews exist in standards literature [@iso-23247-1-2021].
- **Constraints.** No invented fidelity percentages; Quartet product twins **PHYSICAL_PENDING** [@src-hardware-quartet].
- **Symptoms.** “Twin” slides with no update story; twin language for a one-shot CAD export.

### Validity bounds

- **Plain language.** Where the model is trusted—and where it is not.
- **Analogy (labeled).** Like a trail map marked “maintained to the ranger station; beyond that, unmarked.”
- **Technical function.** Prevents silent promotion of stand-in outputs into decisions they cannot support.
- **Constraints.** Bounds are decision- and context-relative; universal numeric twin grades are out of scope here.
- **Symptoms.** Arguments that never state the out-of-bounds region.

### Fixture

- **Plain language.** A deterministic teaching or measurement stand-in when live systems vary.
- **Analogy (labeled).** Like a practice exam with a published answer key—useful, not the live contest.
- **Technical function.** Keeps labs fair and accessible across networks and hardware.
- **Constraints.** Fixtures ≠ human evidence; fixtures ≠ physical proof unless a measured label is earned (CLM-CH28-004).
- **Symptoms.** Portfolio claiming “measured on Device Quartet” from a CSV in the repo.

### Reproducible research (teaching sense)

- **Plain language.** Others can regenerate results from declared inputs and environment.
- **Analogy (labeled).** Like a recipe that lists brand, batch, oven, and timer—not a photo of plated food alone.
- **Technical function.** Pins code, data, seeds, and runtime so regeneration is a testable claim.
- **Constraints.** A peer-reviewed reproducibility guide citation remains **SOURCE_NEEDED** for later depth; WAIKE offers an adjacent catalog track, not an exact CH28 twin module [@src-waike] (CLM-CH28-001).
- **Symptoms.** “Run this somehow” README; plots without SHA; environment drift blamed on classmates.

### Reproducibility card

- **Plain language.** A short declared package: question, inputs, code SHA, fixture/seed, runtime, limitations, label.
- **Analogy (labeled).** Like a packing list taped to a box—so the next person is not guessing.
- **Technical function.** Makes regeneration attemptable; shared schema intent with CH31 (proposed).
- **Constraints.** Card completeness ≠ Gate validation; card ≠ product certification.
- **Symptoms.** Beautiful notebooks that omit the one pin a peer needed.

### Observation vs inference

- **Plain language.** What happened versus what may explain it.
- **Analogy (labeled).** Like hearing a thud—then guessing which shelf fell, before you look.
- **Technical function.** Protects Stability Contract diagnosis inherited from CE-6 [@gunnchos-technology-landscape-ce06; @iso-iec-25010-2023].
- **Constraints.** Simulation pass is an observation about the simulation.
- **Symptoms.** Causal language (“proves the device is fine”) from sim-only outputs.

---

## 6. Stability contract {#ch28-stability}

**Definition (book-wide):** a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

**Chapter lens:** a research or design claim that depends on a stand-in remains honest only while model validity bounds stay explicit, seeds/fixtures/SHAs stay pinned for any claimed regeneration, simulated outputs keep observation/inference labels, and nobody silently promotes simulation or fixture results into physical proof.

A system can remain technically “green” in a simulator while the human experience—or a peer’s regeneration—has already failed.

### Concurrent conditions (qualitative; no invented twin fidelity)

| Condition | Why it matters |
|---|---|
| Stand-in type named | Simulation ≠ twin ≠ fixture ≠ measured |
| Validity bounds explicit | Decisions need an out-of-bounds region |
| Inputs pinned | SHA, fixture ID, seed, config as applicable |
| Runtime declared | Language/OS/image drift breaks regeneration |
| Labels honest | Illustrative / fixture / measured—chosen to match evidence |
| Update story (if twin claimed) | Pairing without update rules is ordinary model language |
| Peer path possible | Commodity/fixture routes so regeneration is not elite-only |
| Accessibility of artifacts | Notebooks and cards usable with assistive tech [@wcag22-20241212] |

### Failure domains

1. **Model mismatch** — omitted behavior is the one that fails live.  
2. **Twin overclaim** — “twin” without pairing/update/bounds.  
3. **Fixture promotion** — teaching CSV treated as plant measurement.  
4. **Environment drift** — unpinned runtime; “works on my machine.”  
5. **Seed / data drift** — stochastic or swapped inputs without declaration.  
6. **Human/process** — publishing plots without a regeneration card.

### Measurements we can seek (when available)

- Code commit SHA and fixture identifiers on a reproducibility card  
- Seed values for stochastic runs  
- Fixture-route completion on LAB-CE06-001 with `fixture` labels  
- Peer regeneration attempt notes (pass/fail + missing pin)

### Measurements we cannot invent

- Device Quartet twin fidelity scores or measured product-twin validation (**PHYSICAL_PENDING**, CLM-CH28-003) [@src-hardware-quartet]  
- Universal numeric “twin accuracy” grades as gunnchOS truth  
- Fake ISO clause citations beyond the verified 23247-1 overview metadata [@iso-23247-1-2021]  
- Peer-reviewed reproducibility-guide page cites while `repro_research_guide` is **SOURCE_NEEDED**

---

## 7. Try it {#ch28-try}

Primary inheritance: **LAB-CE06-001** — keep EMIT discipline and honest labels; use fixture routes when live paths are unsafe, offline, or unfair. Adjacent: existing CE lab fixtures with explicit illustrative/fixture labels. WAIKE `reproducible_research` is an **adjacent** catalog track pointer, not an exact CH28 twin module [@src-waike].

### Baseline (all pathways)

1. Choose one small computational artifact (script, notebook cell, or CE fixture table).  
2. Fill a draft reproducibility card: question, inputs, code SHA (or “unpinned”), fixture/seed, runtime, limitations, truth label.  
3. Change exactly one pin (seed, fixture file, or declare a different SHA) and regenerate. Record observation vs inference.  
4. Do not capture secrets, others’ private data, or real personal traces in simulated “people” datasets—use synthetic data only.

### Pathway notes

| Pathway | Emphasis |
|---|---|
| Explorer | Teach-back: simulation ≠ measured world; twin ≠ ordinary model. |
| Operator | Run a fixture route; label outputs illustrative vs measured. |
| Builder | Produce the filled card artifact with at least one real SHA or honest “unpinned.” |
| Engineer | State validity bounds and one failure mode the stand-in cannot see. |
| Researcher | Attempt peer regeneration instructions; list missing pins. |
| Educator | Prefer fixture routes; require text labels, never color alone [@wcag22-20241212]. |

Proposed-only (not live): `LAB-CH28-REPRO-001` (pin SHA + fixture + seed; regenerate table) remains a packet opportunity name—do **not** treat it as an implemented publication lab ID yet.

---

## 8. Build it {#ch28-build}

Extend the try-it card into a shareable one-pager a peer could use without asking you informal questions.

### Minimum build

1. **Question** — one decision-shaped sentence.  
2. **Stand-in type** — simulation / teaching twin / fixture / measured (pick one primary).  
3. **Validity bounds** — three bullets: trusted / untrusted / unknown.  
4. **Pins** — code SHA, fixture ID, seed, runtime note.  
5. **Truth label** — illustrative, fixture, commodity observation, or measured.  
6. **Limitations** — what a peer must not infer.  
7. **Accessibility note** — how a non-pointer or screen-reader path can read the card [@wcag22-20241212].

### Stretch (optional)

- Pair the card with a second environment regeneration (classmate machine or clean container) and attach a short diff of outcomes.  
- Draft shared field names intended for CH31 portfolio reuse—schema proposal only; not a WAIKE course ID.  
- If you discuss Device Quartet form factors, keep language conceptual / **PHYSICAL_PENDING**; never paste invented twin fidelity [@src-hardware-quartet].

### What not to build

- Dashboards that imply measured twin accuracy without instruments  
- Marketing “digital twin” badges for ordinary offline models  
- Invented WAIKE `DIGITAL_TWIN` module IDs

---

## 9. Secure and include it {#ch28-secure-include}

Security, equity, and accessibility are contract conditions—not an appendix.

### Secure

- Simulated personal data must be synthetic. Do not record classmates’ messages, locations, biometrics, or credentials “for realism.”  
- Pin artifacts without embedding secrets in notebooks or screenshots.  
- Treat model outputs that influence safety-critical decisions as bounded advice, not silent authority.

### Include

- Commodity computers and fixture routes are first-class—not consolation prizes. Equity means a peer without a twin vendor license can still practice regeneration.  
- WAIKE adjacency for reproducible research culture is a track pointer, not a paywall story [@src-waike].  
- Research notebooks and reproducibility cards need text structure, meaningful headings, and alternatives to color-only status [@wcag22-20241212].

### Failure symptoms to watch

- “Demo users” that are lightly anonymized real people  
- Twin platforms required for a baseline Explorer outcome  
- Cards that only make sense as a screenshot of a green UI

---

## 10. Career lens {#ch28-career}

Portfolio evidence beats vibes. Employment is **not** guaranteed by completing artifacts.

| Role family | Portfolio evidence from this chapter |
|---|---|
| Research engineer | Reproducibility card with SHA, fixture/seed, limitations, peer regeneration note |
| Simulation / digital twin engineer | Validity-bounds worksheet; clear simulation-vs-twin wording; no invented fidelity |
| Metrologist / measurement scientist (adjacency) | Uncertainty and label note separating fixture, simulation, and measured |
| Educator / lab lead | Fixture-first lab adaptation with observation vs inference columns |
| Security-minded builder | Synthetic-data checklist for simulated people and redaction before share |

Relate claims to quality-characteristic vocabulary only as literacy—not as ISO product certification [@iso-iec-25010-2023].

---

## 11. Check understanding {#ch28-check}

### Misconceptions to retire

1. **“Any model is a digital twin.”** — Twin language requires maintained pairing, update expectations, and validity bounds—not branding.  
2. **“Simulation pass proves the device.”** — Simulation pass proves something about the simulation under its assumptions.  
3. **“Fixtures are measured twins.”** — Fixtures are teaching/deterministic stand-ins unless labeled measured (CLM-CH28-004).  
4. **“My notebook is reproducible because I shared the file.”** — Without pins, peers are guessing the environment.  
5. **“ISO twin standards let us invent fidelity scores.”** — Catalogue-verified overview citations are not a license to fabricate grades [@iso-23247-1-2021].

### Quick checks

- Name one difference between an ordinary model and a teaching-sense digital twin.  
- Given a green simulation and a failed live path, what labels belong on each observation?  
- What four pins belong on a minimal reproducibility card?  
- Why is Device Quartet twin validation still **PHYSICAL_PENDING** here [@src-hardware-quartet]?

**Teach-it-back.** Explain to a newcomer—without saying “kernel,” “hypervisor,” or “ISO clause”—why a simulation can be useful and still not be a twin, and why a classmate needs your SHA and fixture ID.

**Researcher prompt.** What evidence would be required to move a teaching twin claim toward measured validation—and what remains out of scope while Quartet twin benches are **PHYSICAL_PENDING** and while `repro_research_guide` is **SOURCE_NEEDED**?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). ISO 23247-1 overview metadata was verified for manufacturing digital-twin framework vocabulary; do not invent clause/page fidelity citations [@iso-23247-1-2021]. WAIKE adjacency uses the accepted-main audit SHA recorded for `reproducible_research` [@src-waike]. Device Quartet twin validation remains **PHYSICAL_PENDING** [@src-hardware-quartet]. A peer-reviewed reproducibility guide remains **SOURCE_NEEDED**.

Inline citations used in this chapter include @iso-23247-1-2021, @src-waike, @src-hardware-quartet, @iso-iec-25010-2023, @wcag22-20241212, and @gunnchos-technology-landscape-ce06.

Primary inheritance (link, prefer over duplication): `publication/preproduction/ce-06/`, `labs/LAB-CE06-001/`, and `publication/full31/chapters/ch28/`.

---

## 12. Glossary links {#ch28-glossary}

Candidate terms introduced or reinforced here (see also chapter glossary candidates; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Simulation | Computational stand-in for selected real behaviors |
| Digital twin (teaching sense) | Maintained model paired to a real or planned system with update/validity rules |
| Validity bounds | Where the model is trusted—and where it is not |
| Fixture | Deterministic teaching/measurement stand-in when live systems vary |
| Reproducible research | Others can regenerate results from declared inputs and environment |
| Reproducibility card | Declared pins + limitations + truth label for regeneration |
| Observation vs inference | What happened vs what may explain it |
| Stability Contract | Concurrent hidden conditions that keep an experience (or honest claim) alive |
| PHYSICAL_PENDING | Project evidence not yet measured for claimed physical twin validation |
| SOURCE_NEEDED | Required external source not yet pinned with verified metadata |

Related earlier chapters: measurement and Stability Contract habits (CH20 / CE-6), evidence practice (CH27). Related later chapters: embodied/physical contribution honesty (CH29), portfolio and EMIT synthesis (CH31).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured learner or lab evidence. No fabricated twin fidelity. No product accuracy curves.

### FIG-CH28-001 — Simulation/twin vs measured world

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Conceptual comparison.
- **Reader should notice.** Stand-in story and measured world are different evidence classes.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name both sides; state conceptual truth class; deny invented fidelity scores.

### FIG-CH28-002 — Reproducibility card fields

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Conceptual checklist.
- **Reader should notice.** Question, pins (SHA/fixture/seed/runtime), label, limitations.
- **Truth class.** Conceptual.
- **Alt text requirement.** List required fields in reading order; color never sole cue.

### FIG-CH28-003 — Validity bounds annulus

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Conceptual boundary.
- **Reader should notice.** Trusted inside declared bounds; unlabeled outside.
- **Truth class.** Conceptual.
- **Alt text requirement.** Describe inner trusted region and outer unknown/untrusted region without numeric fake grades.

---

## Claim footnotes used in this chapter (project-specific)

- **CLM-CH28-001.** WAIKE catalog `reproducible_research` exists as an adjacent track—not an exact CH28 twin module [@src-waike].
- **CLM-CH28-002.** Digital-twin standards vocabulary cites ISO 23247-1 overview metadata; no fake ISO numbers; no invented fidelity [@iso-23247-1-2021].
- **CLM-CH28-003.** Device Quartet digital twins as measured validation of physical units remain **PHYSICAL_PENDING** [@src-hardware-quartet].
- **CLM-CH28-004.** Publication fixtures across CE labs are illustrative/deterministic teaching aids unless labeled measured—fixtures are never silent physical proof.
