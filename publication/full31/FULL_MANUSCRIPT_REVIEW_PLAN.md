# Full-manuscript review plan

**Status:** PLAN ONLY — no reviews executed; no responses fabricated.  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Human validation:** `DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT` (draft now complete; recruitment still owner-gated)  
**Does not claim Gate 3 PASS or publication-ready.**

---

## Purpose

Prepare the next validation wave after all 31 chapters reached `WORKING_DRAFT_COMPLETE`. This file is a recruitment and review checklist only. It does **not**:

- open `FULL31-REVIEW-R1` response trees or snapshot packages
- invent Explorer/Builder/Engineer/Educator feedback
- alter `publication/gates/gate-3/` or rewrite `CH02-REVIEW-R1`

Prefer keeping the full-book snapshot closed until the owner confirms manuscript stability and recruitment readiness (Gate 3 confusion risk remains high while CH02-REVIEW-R1 is historical-only).

---

## Reader pathways (recruit after owner approval)

| Pathway | Focus questions (examples) | Artifact expectation |
|---|---|---|
| **Explorer** | Can a non-CS/EE reader follow experience → system → component without jargon walls? | Teach-back notes; confusion points; glossary misses |
| **Builder** | Are Try It / Build It actionable with commodity tools or fixtures? | Completed worksheets; blocker list |
| **Engineer** | Are AuthN≠AuthZ, privacy≠security, sim≠measurement, twin≠ordinary model, and claim boundaries technically credible? | Errata candidates; claim/citation issues |
| **Educator** (recommended) | Can the chapter sequence support a course or lab module without fake credentials? | Sequencing notes; equity/access notes |

Do **not** treat EMIT fixtures, synthetic labs, or CE portfolio templates as human reader evidence.

---

## Subject-matter review by part

| Part | Chapters | SME emphasis |
|---|---|---|
| I | CH01–CH04 | Systems literacy; Device Quartet as lab (PHYSICAL_PENDING honesty) |
| II | CH05–CH10 | Hardware foundations; no invented measurements |
| III | CH11–CH15 | Firmware/OS/data/apps/cloud-edge placement |
| IV | CH16–CH20 | Packets → radio → NTN → QoE; 6G roadmap-only |
| V | CH21–CH25 | AI non-anthropomorphic; security/privacy/a11y/equity measured & qualified |
| VI | CH26–CH31 | Dev/VCS; observability; twins/sim; product; portfolio≠employment; EMIT≠human evidence |

---

## Cross-cutting reviews (after pathway + SME)

1. **Whole-book accessibility review** — WCAG dual bibliography keys respected; a11y ≠ convenience; keyboard/SR paths in labs.
2. **Figure / print review** — draft-blocked figures explicit; SVG + a11y sidecars for implemented figures; print contrast and caption QA.
3. **Editorial / copy pass** — voice consistency; banner accuracy; no publication-ready claims.
4. **Physical validation** — any retained PHYSICAL_PENDING Device Quartet claims stay labeled until measured.

---

## Sequencing (owner-controlled)

1. Freeze a review HEAD (SHA) after integrator green CI.
2. Owner opens recruitment; only then create `FULL31-REVIEW-R1` (or successor) packet **outside** Gate 3.
3. Collect real YAML/markdown responses under a dedicated full31 review tree (not gate-3).
4. Triage → revise → re-verify; never auto-claim PASS.

---

## Integrity constraints

- `READER_VALIDATION_DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT` remains the sequencing truth until real full-book responses exist.
- Successful HTML/PDF/EPUB builds are **not** human validation.
- CH02 historical R1 evidence is **not** a substitute for full-manuscript review.
