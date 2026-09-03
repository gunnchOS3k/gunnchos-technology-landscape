# CE-6 Lab Plan — Capstone

**Proposed lab ID:** `LAB-CE06-001`  
**Title:** Explain, Measure, Improve, and Teach One Real Technology Experience  
**Chapter:** CE-6  
**Ownership:** Publication-owned (not a WAIKE module ID)  
**Hardware rule:** No unowned specialized lab hardware. Accessible fallback required.

---

## Observable question

Using the book’s full model, what evidence can I gather—on devices and tools I already have—to explain a real experience, measure what is actually observable, propose one improvement, and teach the ecosystem to someone else?

## Anchor experience binding

Default: **Connected but unusable** send/submit/sync (see `EXPERIENCE_MAP.md`).  
Allowed substitutes: any real experience the learner can access ethically (stream quality, assistive-path divergence, local-vs-cloud AI feature, etc.), as long as the EMIT spine is completed.

---

## Required devices / software

| Item | Required? | Notes |
|---|---|---|
| Phone, tablet, or computer the learner may use | Yes | Already owned |
| Modern browser with developer tools **or** OS status UI | Baseline preferred | Explorer may use status UI + notebook only |
| Text editor / markdown | Yes | Portfolio artifacts |
| Local Python (optional) | No | Builder extension |
| Specialized RF / silicon / EVT gear | **No** | Forbidden as requirement |
| Device Quartet hardware | **No** | Optional analogy only |

---

## Pathway depth levels

### Explorer — observe / identify
1. Choose one real experience.  
2. Write the human moment and what was noticed.  
3. List ≥4 concurrent Stability Contract conditions that *might* matter.  
4. Mark each as observed vs guessed.  
5. Draw human → system → component → code → network → society.  
6. Teach-back paragraph to a peer/family member (or written as if to them).

### Operator — inspect / compare
1. Complete Explorer.  
2. Capture ≥3 inspection artifacts (status screenshot redacted, timing, log line, DevTools entry).  
3. Run one comparison (e.g., Wi‑Fi vs cellular, local-only vs network action, fresh vs cached).  
4. Produce failure-domain shortlist with one under-determined domain.

### Builder — modify / create
1. Complete Operator.  
2. Build a reusable checklist, worksheet, or tiny local instrumentation helper that makes one condition more inspectable.  
3. Document one tradeoff introduced by that helper (privacy, overhead, complexity).  
4. Write Improve plan with success criteria (no fake numbers).

### Engineer — measure / diagnose
1. Complete Builder or Operator+.  
2. Produce cross-layer diagnosis tree tied to observations.  
3. Place two claims on the evidence hierarchy and state what would escalate them.  
4. State instrumentation limitations (clock granularity, missing kernel visibility, etc.).

### Researcher — hypothesis / controlled comparison
1. State a falsifiable hypothesis about one contract condition.  
2. Design controlled comparison with ≥3 confounders.  
3. If running trials: report repeats and uncertainty; **do not invent statistics**.  
4. Fixture/offline path allowed when live network is unavailable.

### Educator — facilitate / adapt
1. Prepare facilitation plan covering Explorer baseline + fallback.  
2. List three misconception prompts.  
3. Score a portfolio (own, peer, or supplied fixture) with the rubric concept below.

---

## Lowest-friction route (baseline)

**Route A — Notebook + status UI + optional browser DevTools (45–90 minutes)**  
1. Predict which domain will dominate the failure/degradation.  
2. Reproduce the experience once.  
3. Capture observations.  
4. Optional: open DevTools Network/Performance for a web experience.  
5. Write EMIT portfolio sections.

## Offline / fixture fallback (mandatory)

**Route F — Supplied fixture packet**  
When live reproduction is unsafe, offline, or inaccessible:

- Use publication-supplied sample observation notes + sample result table (to be authored with CH02-style fixtures; **do not fabricate measured product claims**).  
- Learner still must: label observation vs inference, complete diagnosis shortlist, Improve plan, and teach-back.  
- Clearly mark fixture-derived rows as `fixture` in the result table.

**Route B (optional)** — Local HTML/Python demo that intentionally stalls a network call while updating local UI (commodity only).

---

## Expected evidence artifacts

| Artifact | Required |
|---|---|
| Experience statement + prediction | Yes |
| Ecosystem diagram | Yes |
| Concurrent conditions list (observed vs guessed) | Yes |
| Result / inspection table | Yes (Explorer may be qualitative) |
| Redacted evidence excerpt OR fixture citation | Yes |
| Improve plan with evidence criteria | Yes |
| Reflection (limits & uncertainty) | Yes |
| Teach-back paragraph | Yes |
| Builder helper (checklist/tool) | Builder+ |
| Diagnosis tree | Engineer+ |
| Hypothesis protocol | Researcher |

---

## Observation vs inference boundary

- **Observation:** timestamps, status strings, HTTP codes, visible stalls, AT announcements heard, etc.  
- **Inference:** “DNS is broken,” “CPU thermal throttle,” “server overloaded” without supporting signals.  
- **Causal claim:** requires boundary evidence and explicit remaining alternatives.

## Privacy / safety boundary

- No passwords, tokens, private messages, health data, or classmate PII in portfolio.  
- Prefer local demos or benign public endpoints.  
- No rooting, jailbreaking, unauthorized scanning, or attacking systems.  
- Metered-data warning: throttle/fixture route available.  
- Do not capture others’ screens without consent.

## Accessibility considerations

- Keyboard-only and screen-reader users may choose Experience C as primary.  
- All figure/table portfolio pieces need text equivalents.  
- Timing tasks must allow extended time; no flicker-heavy demos.  
- Phone-first path documented (status UI without DevTools is valid for Explorer).

## Reproducibility strategy

- Record device class (phone/laptop), OS name, browser name if used — **not** serial numbers.  
- Record date/time window and network class (Wi‑Fi/cellular/offline/fixture).  
- One run ≠ benchmark; label illustrative vs measured.  
- Fixture route must be completable without network.

## Portfolio artifact produced

`labs/LAB-CE06-001/portfolio/` (planned structure; implementation may follow Gate 3):

- `README.md` — experience + EMIT index  
- `diagram.md` — ecosystem map  
- `result_table.csv` — inspections  
- `evidence/` — redacted excerpts or fixture pointers  
- `improve_plan.md`  
- `reflection.md`  
- `teach_back.md`

---

## Capstone prompt (learner-facing concept)

> Choose a real technology experience you can access. **Explain** its ecosystem with the book’s model. **Measure** what you can on commodity tools (or fixtures). **Improve** one bounded aspect and state how you would know it worked. **Teach** the Stability Contract for that experience to another person.

## Rubric concept (not final gradebook)

| Dimension | Emerging | Meeting | Strong |
|---|---|---|---|
| **Explain** | Lists parts without path | Clear human→…→society path | Path + ownership/failure domains |
| **Measure** | No artifacts / unlabeled guesses | Artifacts with obs/inference labels | Comparison + limitations |
| **Improve** | Vague wish | Bounded change + evidence criteria | Tradeoffs + equity check |
| **Teach** | Slogan copy | Accurate teach-back | Adapts depth to audience + checks understanding |
| **Integrity** | Overclaims / invented numbers | Honest labels | Explicit non-claims + fixture honesty |

**Automatic fail conditions:** invented measurements; secrets in evidence; claiming Gate/product certification; requiring specialized hardware without using fallback.
