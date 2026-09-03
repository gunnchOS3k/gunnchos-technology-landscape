# CE-5 — AI, Security, Privacy and Trust

**Package status:** `preproduction`  
**Manuscript status:** scaffold (no canonical chapter prose in this wave)  
**Concept Edition ID:** CE-5  
**Maps to full-book chapters:** CH21, CH23, CH24  
**Accepted-main base:** `166e9544bc6e2aee344bc962ace76d49ee3e04e4` (PR #2)  
**Agent:** D (`agent-d/ce-05-preproduction`)  
**Gate note:** Gate 3 remains `GATE_3_IN_PROGRESS` — `READER_EVIDENCE_PENDING`. This package does not claim Gate 3 PASS.

---

## Human question

When an AI feature answers me, a login succeeds, or a permission prompt appears—what actually has to stay true for that experience to remain usable, private enough, and trustworthy enough to keep using?

---

## Anchor experience (universal)

A learner asks a familiar assistant (on-device or in-browser) a practical question while logged into an ordinary account—then notices one of: a confidence hedge, a wrong-but-fluent answer, a permission or privacy notice, or a “sign in again” / verification step.

This is **not** Chapter 2’s one-tap stack tour. The visible moment is *judgment under uncertainty + access control + data leaving (or not leaving) the device*.

---

## Teaching model

`Human experience → system → component → code → network → society`

Every technical idea must reconnect to something a reader can notice: latency of an answer, where data went, who was authenticated, what was encrypted in transit, what remained uncertain, and whether the experience still felt usable.

---

## Scope (Concept Edition)

Prepare systems-level literacy for:

1. **Data → model → inference/output** (accessible ML/generative AI; no mythology of “understanding”).
2. **Local vs cloud AI** (latency, energy, privacy, dependency, update/control).
3. **Uncertainty and errors** (fluency ≠ correctness; observation vs interpretation).
4. **Attack surfaces tied to UX** (prompts, permissions, sessions, supply of models/data—not a detached scare-list).
5. **Identity / authentication / authorization**.
6. **Encryption concepts** (goals and limits; not a crypto course).
7. **Privacy and data lifecycle** (collect → use → retain → share → delete/redact).
8. **Human trust vs technical trust** (feeling safe vs controls/evidence).
9. **Responsible use** (disclosure, consent, equity, accessibility).

### Editorial constraints (hard)

- Do **not** anthropomorphize models as knowing/understanding unless carefully explained as metaphor with limits.
- Do **not** frame AI as inherently trustworthy or untrustworthy.
- Do **not** present cybersecurity as a scare-list detached from user experience.
- Do **not** invent measurements, WAIKE module IDs, DOIs, or hardware validation.

---

## Twelve-section anatomy (prep only)

| # | Section | CE-5 prep intent |
|---|---|---|
| 1 | The moment | Assistant answer + login/permission friction |
| 2 | What you notice | Fluency, delay, hedges, prompts, lockouts |
| 3 | Exploded ecosystem | Sensor/UI → app → model runtime → identity → network → cloud/policy |
| 4 | Follow the signal | Prompt/data → features/tokens → inference → output → logging/retention |
| 5 | Component cards | Model, inference runtime, identity provider, crypto boundary, consent/log store |
| 6 | Stability contract | Bounds for correctness-usable, privacy-usable, auth-usable trust |
| 7 | Try it | Proposed `LAB-TRUST-001` (local vs remote AI + consent card) |
| 8 | Build it | Redaction/consent config or authz matrix toy extension |
| 9 | Secure and include it | Threats + privacy + a11y + equity together |
| 10 | Career lens | Security, ML/AI, privacy, SRE, a11y, TPM analogues |
| 11 | Check understanding | Misconceptions: “AI knows”; “HTTPS = private forever”; “login = authorization” |
| 12 | Glossary links | Terms + CH21/23/24 + WAIKE adjacencies |

---

## Reader pathways (Explorer → Educator)

| Pathway | CE-5 expectation |
|---|---|
| Explorer | Trace what they saw/felt; separate answer fluency from correctness |
| Operator | Read permission/consent prompts; distinguish authn vs authz symptoms |
| Builder | Configure a consent/redaction or authz matrix artifact |
| Engineer | Reason about local vs cloud inference tradeoffs and attack-surface boundaries |
| Researcher | State uncertainty; design a small evaluation with limitations |
| Educator | Facilitate misconceptions; offer no-device and low-bandwidth adaptations |

---

## Non-goals this wave

- Full canonical chapter prose
- Shared registry edits (`claim_registry`, `source_registry`, `waike/alignment.yaml`, shared `.bib`)
- Chapter 2 / `CH02-REVIEW-R1` / Gate 3 response fabrication
- Product marketing for Device Quartet or “finished AI platform” claims

---

## Downstream full-book links

- **CH21** — Data, Machine Learning, and Generative AI  
- **CH23** — Cybersecurity from Chip to Cloud  
- **CH24** — Privacy, Identity, Safety, Accessibility, and Ethics  

Device Quartet appears only as **future learning-lab context**, labeled research form factor / `PHYSICAL_PENDING` when project-specific.
