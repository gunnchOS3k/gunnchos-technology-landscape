---
status: draft
chapter_id: CH24
chapter_number: 24
title: "Privacy, Identity, Safety, Accessibility, and Ethics"
author: "Edmund Gunn, Jr."
part: V
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-TRUST-001]
figures:
  - FIG-CH24-001
  - FIG-CH24-002
  - FIG-CH24-003
---

# Chapter 24 — Privacy, Identity, Safety, Accessibility, and Ethics

**Status:** `draft` · **Chapter ID:** `CH24`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working draft complete · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does **not** claim Gate 3 PASS; fixtures and illustrative portfolios are teaching infrastructure, not human reader evidence).

Part V has already named models, inference paths, and chip-to-cloud security language. This chapter refuses the appendix treatment: privacy, identity, safety, accessibility, and ethics are concurrent conditions of usable technology. It inherits Concept Edition **CE-5** (privacy/lifecycle/responsible-use) and publication lab **LAB-TRUST-001**, with CE-6 adjacency for accessibility-as-contract-condition—without duplicating CH21’s ML depth or CH23’s full attack-surface tour.

Two non-collapse rules govern the prose:

1. **Privacy ≠ security.** Encryption, authentication, and least privilege can hold while collection, retention, sharing, or deletion still fail the person.
2. **Accessibility ≠ convenience.** A path that is faster for one body/tool is not automatically usable for another; alternate routes are success conditions, not polish.
3. **Safety ≠ censorship.** Safety limits aim to reduce harm from fluent or actionable outputs; they are not the same as viewpoint-censorship claims, and over-refusal is a distinct failure mode to name honestly.

---

## 1. The moment {#sec-ch24-moment}

You need to finish something ordinary: reset access after a lockout, accept a permission or privacy notice, recover an account, or complete a verify step so a familiar feature will run. The app looks modern. A classmate finishes in seconds. Your path stalls—CAPTCHA that never announces, SMS you cannot receive, a privacy wall of text you cannot act on, or a recovery flow that exists only as a vision-only selfie.

From the seat: exclusion dressed as “just a security step,” or surprise reuse of something you thought you deleted.

Underneath: concurrent conditions. A **permission notice** is not proof of informed control. An **authenticated session** is not authorization for every button on the screen. A **padlock** is not a privacy lifecycle. An **accessible path** is not a nice-to-have theme.

The governing question for this chapter:

> When a permission, recovery, or accessibility path decides whether someone can finish a task others complete easily—which conditions broke, and what evidence do I actually have?

This is CE-5’s responsible-use spine expanded for full-book depth. It is not a scare-list, not legal advice, and not a claim that citing WCAG or NIST certifies any product in this book.

---

## 2. What you notice {#sec-ch24-notice}

Before naming Solove harms or assurance levels, notice the human contract that broke.

You expected a familiar task to remain *doable*. Instead you notice a consent prompt you cannot parse into actions, a “verify it’s you” loop that excludes your assistive path, a fluent assistant answer that sounds finished while you still do not know where the prompt went, or a delete request that leaves history resurfacing later. A peer on a different device, network, or body may finish while you do not. That divergence is part of the technical story—not a character flaw in the user.

**Privacy symptoms and security symptoms can diverge.** HTTPS can succeed while retention exceeds disclosure. Login can succeed while authorization silently blocks. Status chrome can say “secured” while the person cannot recover access with their tools [@saltzer_schroeder_1975].

**Accessibility failure is experience failure.** If the only recovery path requires a modality you cannot use, the Stability Contract already broke—even if the backend “worked” for other users [@wcag22-20241212].

Optional commodity notice (no specialized gear): open one familiar app’s privacy/permission surface *or* an account-recovery entry point you already own. Write two columns—*what the UI claimed* and *what you could actually do*—before inventing a cause. If live capture is unsafe, inequitable, or metered, use LAB-TRUST-001 fixtures and mark rows `fixture`. Fixture transcripts are illustrative teaching data, not your measured evidence and not Gate validation.

---

## 3. Exploded ecosystem {#sec-ch24-ecosystem}

A stuck recovery or opaque consent is not a single object. It is a path through an ecosystem. **FIG-CH24-001** is the first-minute map: human experience at the center, with concurrent spokes for collect → use → retain → share → delete/redact. Treat it as **Representative educational architecture**, not a claim that every app shares one vendor topology.

Walk the layers in ordinary language.

### Human and context

Intent, stigma of being locked out, literacy load of legal text, and who is watching over the shoulder set what “private enough” and “usable enough” mean *for this person now*.

### Interaction and alternate path

Keyboard, pointer, voice, switch, or screen reader must deliver intent and receive equivalent feedback. Accessibility is a path through the ecosystem—not a post-hoc theme [@wcag22-20231005; @wcag22-20241212]. Cite both dated WCAG 2.2 Recommendation editions when referring to the standard family; do not silently collapse dates into one undated `/TR/WCAG22/` shortcut.

### Application / policy / consent UI

Handlers assemble prompts, show disclosures, and gate features. Psychological acceptability of controls matters as much as their existence [@saltzer_schroeder_1975].

### Identity provider and session state

Claims about who you are (or which service is speaking) unlock experiences. Proofing and authentication are not the same as authorization of a specific action [@nist_sp_800_63_4].

### Data stores and logs

History, backups, analytics queues, moderation review, and fine-tune candidates are where lifecycle decisions become durable. Delete UI without residual-copy honesty is a privacy failure even when disks are encrypted.

### Inference / remote services (when AI is in play)

Local vs cloud path changes who can observe prompts and outputs (CE-5 adjacency). Fluency is not correctness; disclosure modes belong in the consent story [@src-waike].

### Network and crypto boundary

Transit protections can be real while endpoints still process plaintext for the service. Padlock ≠ private forever.

### Organizational / societal layer

Vendors, reviewers, regulators, and equity of private compute shape who can complete labs and who is surveilled by default. Fixtures exist so unpaid API credits do not gate Explorer completion.

**FIG-CH24-002** separates accessible recovery/auth paths from blocked ones so readers stop treating “security worked” as “everyone could finish.”

---

## 4. Follow the signal {#sec-ch24-signal}

Here the “signal” is a person trying to keep usable control of access and data—not a single TLS handshake. Read the sequence as a logical journey. Alternate paths exist; open questions stay labeled undetermined.

1. **Intent.** A person tries to use, recover, consent, refuse, or delete.
2. **Input delivery.** OS and app receive the intent—including along assistive paths—or do not.
3. **Identity claim.** Session, token, or proof step asserts who/what is acting [@nist_sp_800_63_4].
4. **Authorization / policy gate.** Role, attribute, risk, or feature flag allows or denies.
5. **Data movement.** Collect / use for the stated purpose; optional off-device send.
6. **Side effects.** Retain, share with vendors/reviewers, or queue for later training—disclosed or not.
7. **Feedback.** Visual, haptic, audio, or AT announcement of success, denial, or uncertainty.
8. **Human judgment.** Finished, locked out, surprised by reuse, or “works for them / not for me.”

### Lifecycle stages without collapse

| Stage | Everyday question | Typical mis-use |
|---|---|---|
| **Collect** | What entered the prompt, form, sensor, or log? | Treating “I typed it” as voluntary forever |
| **Use** | What purpose is happening now? | Purpose creep without new disclosure |
| **Retain** | What still exists after the screen clears? | Equating logout with deletion |
| **Share** | Who else can see copies? | Assuming encryption forbids all sharing |
| **Delete/redact** | What residual copies remain? | Calling UI “deleted” without residual honesty |

Solove’s taxonomy supplies peer-reviewed vocabulary for naming privacy *harms* carefully; do not invent page numbers in this draft [@solove_taxonomy_2006]. Harm language is not a substitute for lifecycle controls.

### Evidence hierarchy (climb only as far as tools and ethics allow)

1. Illustrative teaching aid (labeled)
2. Commodity observation (UI claims, wall-clock, what you could/couldn’t do)
3. Config / disclosure text you can actually read
4. Correlated multi-signal inspection (still not proof)
5. Controlled comparison under ethical constraints (LAB-TRUST-001 Route L vs Route C)
6. Formal assurance or conformance assessment—**not** required for classroom completion and **not** claimed for this book [@nist_sp_800_63_4; @wcag22-20231005; @wcag22-20241212]

### Failure branch without drama

Prefer failure *domains* over confident blame: disclosure/consent, identity proofing, authentication session, authorization, retention/share, accessibility path, safety filter UX, network/crypto boundary. Outside observation rarely distinguishes them cleanly. That limitation is literacy.

---

## 5. Component cards {#sec-ch24-components}

For each idea: plain language, analogy (labeled), technical function, constraints, common symptoms.

### Privacy / data lifecycle

- **Plain language.** Rules and practices for collect, use, retain, share, delete/redact.
- **Analogy (labeled).** Like a library checkout slip that must say what was borrowed, for how long, and who else may see it—not merely that the building has a lock.
- **Technical function.** Names data fate across systems that security controls alone do not settle.
- **Constraints.** Residual copies; vendor subprocessors; backup lag; UI delete ≠ cryptographic erase.
- **Symptoms.** Surprise recall of old prompts; “deleted” history resurfacing; consent text that cannot be acted on.

### Identity (human systems)

- **Plain language.** Claims about people or services that unlock experiences.
- **Analogy (labeled).** Like a name badge that is not the same thing as a key to every room.
- **Technical function.** Separates identity proofing / authentication from authorization decisions [@nist_sp_800_63_4].
- **Constraints.** Assurance levels are context-dependent; this book does not certify products.
- **Symptoms.** Mystery re-auth loops; recovery that excludes AT; login success with silent feature deny.

### Authentication vs authorization

- **Plain language.** Authn: proving a claim. Authz: deciding what that claim may do.
- **Analogy (labeled).** Like showing ID at the door versus being allowed into the lab fridge.
- **Technical function.** Prevents collapsing “signed in” with “permitted.”
- **Constraints.** Visible buttons can still be unauthorized; error copy may lie by omission.
- **Symptoms.** Feature visible but blocked; admin UI for non-admins; session valid while scope insufficient.

### Safety constraints

- **Plain language.** Limits that keep harmful outcomes from being easy to enact—especially fluent outputs that look actionable.
- **Analogy (labeled).** Like a power tool’s guard: it does not make the tool “moral”; it changes what is easy.
- **Technical function.** Bounds deployment and reliance practices; NIST AI RMF vocabulary is useful without declaring AI itself good or bad [@nist_ai_rmf_100_1].
- **Constraints.** Safety ≠ censorship: filters can over-refuse without becoming a free-speech slogan; fluency can still mislead; humans remain accountable for reliance.
- **Symptoms.** Confident wrong answer treated as fact; unexplained refusal storms; tool actions without disclosure.

### Accessibility path

- **Plain language.** Alternate routes so the experience succeeds for diverse bodies and tools.
- **Analogy (labeled).** Like a building that needs a ramp *and* stairs—speed on the stairs is not the ramp.
- **Technical function.** Equivalent perception, operable controls, understandable feedback, robust AT names [@wcag22-20241212].
- **Constraints.** Automated checkers do not certify conformance; dated WCAG editions must not be silently overwritten [@wcag22-20231005; @wcag22-20241212].
- **Symptoms.** CAPTCHA-only verify; focus traps; status by color alone; completion never announced.

### Ethics ladder

- **Plain language.** Observation before inference; disclosure and responsible use before confident blame.
- **Analogy (labeled).** Like a lab notebook: write what you saw before what you guess.
- **Technical function.** Keeps portfolios and reviews from laundering speculation as evidence [@src-waike].
- **Constraints.** Feeling safe ≠ technical control; disclosure modes are practices, not magic.
- **Symptoms.** “The AI knows”; fixture numbers presented as human evidence; Gate status inflated.

### Consent / trust card

- **Plain language.** A compact artifact: audience, purpose, data classes, retention, opt-out, AI disclosure.
- **Analogy (labeled).** Like a nutrition label for a data path—incomplete if any required field is missing.
- **Technical function.** Forces lifecycle and disclosure decisions into inspectable form (LAB-TRUST-001 / WAIKE `lab_consent_disclosure` adjacency).
- **Constraints.** A filled card is pedagogy, not legal compliance.
- **Symptoms.** Vague “improve the product” checkboxes; no retention bound; no opt-out path.

---

## 6. Stability contract {#sec-ch24-stability}

**Definition (publication teaching model):** a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

**Signature distinction for this chapter:** a system can remain technically **secured** or **online** while the human experience has already **failed** on privacy, recovery, or accessibility.

### Concurrent conditions (qualitative anchor)

For a successful permission / recovery / trust-usable experience, conditions such as the following must remain *good enough together* (CE-5 inheritance + CH24 packet):

| ID | Hidden condition |
|---|---|
| SC-CH24-C | Consent/disclosure understandable and actionable |
| SC-CH24-I | Identity recovery usable without excluding assistive paths |
| SC-CH24-Z | Authorization matches what the UI implies |
| SC-CH24-P | Data lifecycle controls (retain/delete/redact) operable as disclosed |
| SC-CH24-A | Accessibility path remains concurrent with other success conditions |
| SC-CH24-S | Safety constraints prevent harmful fluent outputs from being actionable blindly |
| SC-CH24-L | Path locality (local vs cloud) knowable at a usable level when AI is involved |
| SC-CH24-E | Equity of completion—fixtures available when live paths are gated by cost or hardware |

**Numeric / legal humility rule:** this teaching contract is **not** GDPR/CCPA compliance, **not** WCAG certification of the book or any gunnchOS product, and **not** NIST product assurance. Cite standards for vocabulary and teaching intent only [@nist_sp_800_63_4; @wcag22-20231005; @wcag22-20241212].

### CE-5 + LAB-TRUST-001 linkage

- **CE-5 preproduction** (`publication/preproduction/ce-05/`) is the primary inheritance package: lifecycle, local-vs-cloud trust, authn/authz, consent card, ethics ladder.
- **LAB-TRUST-001** is publication-owned. Status tags include **`IMPLEMENTED_DIGITAL`** and **`FIXTURE_VALIDATED`**. Those tags mean worksheets, validators, and synthetic Route L / Route C transcripts exist. They do **not** mean Gate 3 PASS. They do **not** mean fixtures are human evidence. They do **not** mean Device Quartet on-device measurements (**PHYSICAL_PENDING**).

WAIKE accepted `main` (SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`) hosts adjacent `COMM_PD_ETHICS` labs (`lab_consent_disclosure`, `lab_ai_disclosure_modes`, `lab_ethics_ladder`, `lab_accessibility_comm`). Those are adjacencies—not renamed as CH24 course IDs [@src-waike].

---

## 7. Try it {#sec-ch24-try}

### LAB-TRUST-001 — Compare local vs remote AI paths and write a consent/trust card

**Goal.** Observe the same practical question on a local-capable path vs a remote path (or fixtures), then produce a consent/trust card and a dual-ledger note (one human-trust feeling + one technical-trust control)—without treating the model as a person who “knows.”

**WAIKE alignment note.** Adjacent only at audited SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`. **LAB-TRUST-001** is publication-owned; do not invent a WAIKE ID with that name.

**Safety (hard stops).**

- Non-sensitive prompts only; no secrets, health records, private messages, or precise location.
- No exploit steps, credential harvesting, unauthorized scanning, or capture of others’ private data.
- Redact account identifiers before portfolio share.
- No Device Quartet / specialized hardware required.

**Routes.**

- **Route L — Local / offline-capable (or fixture).** Use on-device/local runtime if available; otherwise `fixtures/` labeled `FIXTURE`.
- **Route C — Cloud / browser assistant (or fixture).** Network required when live; otherwise supplied remote transcript.
- **Route F — Fixture fallback (mandatory equitable path).** Complete with synthetic transcripts when live paths are unavailable, unsafe, or costly.

**Explorer baseline.**

1. Predict which route requires network and which (claimed) sends prompt text off-device.
2. Fill observation columns only (time if measured by you; hedges; errors).
3. Complete consent/trust card: audience, purpose, data classes, retention, opt-out, AI disclosure.
4. Dual-ledger: one feeling + one control.
5. Uncertainty note: one fluent-but-wrong or unverifiable claim—or “none observed” with what was checked.
6. Mark fixture-derived rows as `fixture`.

**Operator extension.** Classify one friction symptom as identity, authorization, network, model quality, privacy disclosure, or accessibility.

**Builder extension.** Add one redaction rule for a sample log/prompt line; document utility vs exposure.

**Engineer extension.** Sketch trust boundaries crossed by Route C; name which SC-CH24 conditions you observed vs inferred.

**Researcher extension.** State a hypothesis about leakage or overrefusal; list ≥3 confounders; no invented statistics.

**Educator facilitation.** Prefer Route F when live capture is inequitable; run misconception drill from Section 11.

**Evidence to keep.** Comparison table, consent card, dual-ledger, scrubbed notes, teach-back. Completion means artifact-backed claims—not a bare exit code and not Gate PASS.

---

## 8. Build it {#sec-ch24-build}

Extend LAB-TRUST-001 without turning Part V into a fake compliance certificate.

### Explorer

Build a pocket card: *privacy ≠ security*, *a11y ≠ convenience*, plus the five lifecycle stages in plain sentences.

### Operator

Build a two-column sheet: UI claims | actions you could complete. Add a third column only for inferences, each with “evidence still needed.”

### Builder

Build a consent-card template plus one redaction config for a toy log line—or a minimal authz matrix (desk / reader / bot) that shows authn ≠ authz.

### Engineer

Build a recovery-path decision tree that ends in “inaccessible for AT / keyboard / SMS-unavailable users” as a first-class failure—not an afterthought. Cite identity guidance vocabulary honestly without product certification claims [@nist_sp_800_63_4]. Map at least one blocked path against WCAG-informed operable/perceivable failure language using a **dated** key [@wcag22-20241212].

### Researcher

Build an evidence plan for a claim you are *not* allowed to make yet—for example, “this app is WCAG 2.2 conformant” or “this IdP meets a NIST assurance level.” Specify what audit artifacts would be required; keep book posture non-certifying. Note both WCAG dated Recommendation editions exist and must not be silently merged [@wcag22-20231005; @wcag22-20241212].

Educators can facilitate Section 11 teach-backs and keep Route F first-class.

---

## 9. Secure and include it {#sec-ch24-secure-include}

This section is the chapter’s core—not an appendix. Keep threats attached to user experience.

### Security (UX-linked)

Permission dialogs, verify steps, and session emails are where Saltzer & Schroeder’s least privilege and psychological acceptability meet real screens [@saltzer_schroeder_1975]. Teach boundaries: phishing as experience failure; prompt/document text as untrusted context for models. Out of scope: exploit development, credential-stuffing how-tos, live social-engineering against third parties.

### Privacy

Lifecycle stages with decision owners (Section 4). Security controls can succeed while privacy fails—name that split explicitly. Solove-style harm vocabulary may label issues carefully without invented pages [@solove_taxonomy_2006].

### Identity

Separate proofing/authentication from authorization [@nist_sp_800_63_4]. Recovery must remain concurrent with accessibility conditions (SC-CH24-I + SC-CH24-A).

### Accessibility

Accessibility is a Stability Contract condition. Figures and labs: alt text, text equivalents, reading order; color never sole cue. Auth flows: keyboard operable; screen-reader names for verify steps. Automated checkers do **not** certify WCAG conformance. When citing WCAG 2.2, keep dual dated keys: Recommendation 5 October 2023 and Recommendation 12 December 2024 [@wcag22-20231005; @wcag22-20241212].

### Equity

Private compute gap, language/dialect quality gaps, SMS/CAPTCHA/selfie exclusion, unpaid data labor myths, and API cost gates. Fixtures are equity infrastructure.

### Safety

Prevent harmful fluent outputs from being treated as automatically actionable [@nist_ai_rmf_100_1]. Trauma-aware optional examples; proportionate account-takeover stories.

### Ethics

Observation before inference (**FIG-CH24-003** ethics ladder). Disclose AI assistance where learners present work. Do not anthropomorphize models as moral agents. Do not present `FIXTURE_VALIDATED` as Gate 3 PASS. Do not invent WAIKE ethics course IDs for CH24 [@src-waike].

---

## 10. Career lens {#sec-ch24-career}

One blocked recovery crosses many ownership domains. No table promises employment; roles vary by organization. LAB-TRUST-001 artifacts resemble early professional evidence in miniature: labeled observations, consent cards, and explicit uncertainty.

| Role family | Typical artifacts | Review questions |
|---|---|---|
| Privacy engineer | Lifecycle map + consent card | Did retain/share/delete match disclosure? |
| Identity engineer | Authn vs authz notes; recovery path writeup | Was login confused with permission? |
| Accessibility engineer | WCAG-informed review note (dated key cited) | Was equivalent feedback present—not “nice UI”? |
| Trust & safety / ethics facilitator | Ethics ladder + AI disclosure mode note | Observation before inference? |
| Security engineer (UX-linked) | Least-privilege / acceptability note | Did controls exclude assistive paths? |
| Educator / facilitator | Rubric; misconception drill; Route F plan | Were fixtures labeled correctly? |

Portfolio hint: a scrubbed consent card with `fixture` labels beats a vibes-based “it’s private because HTTPS” claim.

---

## 11. Check understanding {#sec-ch24-check}

**Concept.** In one sentence, distinguish *privacy* from *security* so neither swallows the other.

**Concept.** In one sentence, distinguish *accessibility* from *convenience*.

**Concept.** In one sentence each, distinguish *authentication* from *authorization*.

**System tracing.** Trace a familiar permission, recovery, or delete request from intent to human feedback in numbered steps. Mark observed vs inferred. Name ≥4 SC-CH24 conditions that had to hold together.

**Misconception check.** Why can TLS succeed while a privacy lifecycle still fails?

**Misconception check.** Why must this chapter refuse collapsing WCAG 2.2 into a single undated citation key?

**Evidence ethics.** What is the difference between LAB-TRUST-001 `FIXTURE_VALIDATED` infrastructure and Gate 3 human reader validation?

**Teach-it-back.** Explain to a family member—using only LAB-TRUST-001 vocabulary—why a smooth AI answer can still be unsafe to act on, and what one control (technical or social) would make the experience more trustworthy for more people.

**Researcher prompt.** What additional evidence would be required to move from a classroom consent card toward a formal identity-assurance or accessibility-conformance claim—and what remains out of scope for this lab [@nist_sp_800_63_4; @wcag22-20241212]?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). CE-5 chapter-local proposals and the full31 working bibliography informed key use of dual WCAG dated Recommendations, NIST SP 800-63-4, Solove (pages deferred), and WAIKE adjacency at SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`. Safety/responsible-use vocabulary may reference NIST AI RMF without product certification claims. Gate 3 reader evidence remains pending; this working draft is not publication-ready.

Inline citations used in this chapter include @wcag22-20231005, @wcag22-20241212, @nist_sp_800_63_4, @solove_taxonomy_2006, @src-waike, @saltzer_schroeder_1975, and @nist_ai_rmf_100_1.

Primary inheritance (link, prefer over duplication): `publication/preproduction/ce-05/`, CE-6 accessibility-as-contract adjacency, and `labs/LAB-TRUST-001/`.

---

## 12. Glossary links {#sec-ch24-glossary}

Candidate terms introduced or reinforced here (see also `publication/full31/chapters/ch24/GLOSSARY_CANDIDATES.yaml`; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Privacy / data lifecycle | Collect → use → retain → share → delete/redact |
| Identity (human systems) | Claims about people/services that unlock experiences |
| Authentication | Proving an identity claim |
| Authorization | Deciding what a proven claim may do |
| Safety constraints | Limits that keep harmful outcomes from being easy to enact |
| Accessibility path | Alternate routes so experience succeeds for diverse bodies/tools |
| Ethics ladder | Observation before inference; disclosure and responsible use |
| WCAG as guidance | W3C accessibility guidelines; cite dated editions, not silent merges |
| Consent / trust card | Audience, purpose, classes, retention, opt-out, AI disclosure |
| Privacy ≠ security | Controls can hold while lifecycle still fails the person |
| Accessibility ≠ convenience | Faster for one path is not usable for all paths |
| Safety ≠ censorship | Harm-reduction limits ≠ viewpoint-censorship claims; over-refusal is a named failure |
| Stability Contract | Concurrent hidden conditions that keep an experience alive (book teaching model) |

Related earlier chapters: CE-5 / CH21 inference and disclosure adjacency; CH23 security boundaries without replacing privacy. Related later chapters: equity deepening (CH25), evidence practice (CH27), responsibility synthesis (CH30/CH31).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured learner or lab evidence. No fabricated telemetry. No product certification claims.

### FIG-CH24-001 — Privacy data lifecycle wheel with owners

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Lifecycle / wheel.
- **Reader should notice.** Collect → use → retain → share → delete/redact with decision owners.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name each stage and that owners differ by stage; color never sole cue; deny legal-compliance claim.

### FIG-CH24-002 — Accessible vs blocked recovery/auth paths

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Comparative paths.
- **Reader should notice.** Security can “succeed” for one path while another body/tool is locked out.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name accessible path vs blocked path; state a11y ≠ convenience; deny WCAG certification of products.

### FIG-CH24-003 — Ethics ladder (observation → inference → disclosure)

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Ladder.
- **Reader should notice.** Observation before inference; disclosure as a practice step.
- **Truth class.** Conceptual.
- **Alt text requirement.** Order the three rungs; state fixtures are not human evidence; deny Gate 3 PASS.
