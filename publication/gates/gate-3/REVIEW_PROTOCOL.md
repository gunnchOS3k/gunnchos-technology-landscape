# Gate 3 Review Protocol — Chapter 2

**Status:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Review snapshot:** `CH02-REVIEW-R1` (see `REVIEW_SNAPSHOT.yaml`)

## Purpose

Prepare real human prototype validation of Chapter 2 with the least friction possible.
Readers must **not** need to clone the repository or install Quarto.

## Required reader levels

| Level | Audience | Form |
|---|---|---|
| Explorer | Nontechnical reader | Form A |
| Builder | Undergraduate / maker | Form B |
| Engineer | Technical reader | Form C |
| Educator (optional) | Teacher / mentor | Form D |

## Reader task (fixed)

1. Read Chapter 2 — *Follow One Tap Through the Entire Stack*
2. Inspect the seven figures
3. Complete LAB-TAP-001 baseline **browser** route **or** supplied **fixture** route
4. Complete the feedback form for your reader level
5. Complete the teach-back prompt

## Time expectation (realistic)

| Activity | Typical range |
|---|---|
| Read Chapter 2 + figures | 35–55 minutes |
| LAB-TAP-001 browser or fixture route | 20–45 minutes |
| Feedback form + teach-back | 15–25 minutes |
| **Total** | **about 75–120 minutes** |

Do not advertise this as a “15-minute skim.” Rushing defeats Gate 3.

## Privacy

Forms accept a **reviewer code / pseudonym** or an **optional name**.

Do **not** collect: passwords, tokens, private messages, device serial numbers,
precise location, or unrelated personal data.

## Delivery channels

1. **GitHub Pages** (preferred for HTML + lab): `docs/` site once Pages is enabled
2. **GitHub Actions artifact** `reader-preview-bundle` (HTML, PDF, EPUB, figures, lab, forms)
3. Direct download of PDF/EPUB from the artifact

## Evidence intake

Completed responses belong only in:

`publication/gates/gate-3/responses/`

Rules:

- Only real human feedback
- No synthetic / fabricated responses
- Redact unnecessary personal information
- Keep raw responses separate from analysis summaries

## Gate 3 closure criteria (authoritative)

Gate 3 may close **only** after **all** of the following:

1. At least one real **Explorer** review for snapshot `CH02-REVIEW-R1` (or a later superseding snapshot)
2. At least one real **Builder** review
3. At least one real **Engineer** review
4. Chapter 2 is reviewed against the resulting feedback
5. Material issues are addressed **or** explicitly documented
6. Lab successfully completed by reviewers **or** limitations documented
7. Final revision build passes (`make all` / hosted CI)
8. **Author/editorial judgment** still affirms PASS

An Educator review is **strongly preferred** but **not required** unless the governing blueprint is updated.

**Three form submissions do not automatically equal Gate 3 PASS.**

## Explicit non-claims

- This prep wave does **not** claim Gate 3 PASS
- Empty `responses/` means `NO_READER_EVIDENCE`
- Broader field validation remains Gate 5
