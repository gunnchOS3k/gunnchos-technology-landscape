# Validation sequence decision (owner)

**Scope:** Full 31-chapter working manuscript — **outside** Gate 3 / CH02-REVIEW-R1.  
**Accepted main (infra branch base):** `18ec58005529bd16d680ee7419e4dea13150e9c6`  
**Decision status:** RECORDED  
**Does not mean Gate 3 PASS.**

---

## Owner decision

1. **Complete the entire 31-chapter working manuscript first** before recruiting a new full-book reader cohort.
2. **Recruit real readers only after** a full working manuscript draft exists (`WORKING_DRAFT_COMPLETE` for all 31 chapters under `make full31-draft-check --mode strict`).
3. **Then revise** using that feedback (technical/editorial + human validation loops).

## Human validation posture

| Field | Value |
|---|---|
| Human validation | `DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT` |
| Gate posture (unchanged) | `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` |
| Gate 3 PASS? | **No** — this decision does **not** claim Gate 3 PASS |

## Relationship to CH02-REVIEW-R1

- `CH02-REVIEW-R1` and `publication/gates/gate-3/` remain **historical** Gate 3 chapter-prototype evidence.
- They are **not** current full-manuscript validation.
- Do **not** alter gate-3 content or artifact hashes for this decision.
- Do **not** treat CH02 reader responses as substitute evidence for a full-book pass.

## Future full-book review snapshot

- A future review id will likely be `FULL31-REVIEW-R1` (or successor).
- **Do not create** that snapshot, packet, or response tree in this authoring-infra wave.
- Create it only after the full working manuscript exists and owner opens recruitment.

## Working-draft milestone (Batch 3 integrator)

As of the full-manuscript draft branch tip that completes CH01–CH31 working prose:

- `WORKING_DRAFT_COMPLETE = 31` (honest manuscript structure under `make full31-draft-check --mode strict`).
- `HUMAN_VALIDATED = 0` and `PUBLICATION_READY = 0` remain true.
- Recruitment for full-book readers remains **owner-gated**.
- `publication/full31/FULL_MANUSCRIPT_REVIEW_PLAN.md` is plan-only; **Do not create** `FULL31-REVIEW-R1` snapshot/response trees until the owner opens recruitment.
- This milestone does **not** claim Gate 3 PASS.

## Implications for Batch 1+ chapter agents

- Author all 31 chapters to working-draft quality under the publication status banner.
- Keep Gate 3 / CH02-REVIEW-R1 untouched.
- Use `make full31-draft-check` (`infra` now; `strict` when claiming manuscript-complete).
- Progress reporting uses the normalized dimensions in `PROGRESS_DIMENSIONS.md`.
