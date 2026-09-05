# Human Validation Owner Guide

```
NO_REVIEW_RESPONSES_YET
GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING
KIDS_CHILD_VALIDATION_PENDING
NOT CHILD-VALIDATED
NOT PUBLICATION-READY
```

Literal execution order:

## Step 1
Merge review-prep PR (this wave).

## Step 2
Download/fetch Adult `FULL31-REVIEW-R1` artifacts (and rebuild HTML/EPUB/PDF if manifests mark missing).

## Step 3
Recruit Adult reviewer cohorts using `publication/reviews/recruitment/` templates (manual send only).

## Step 4
Recruit Kids Stage 1 adult reviewers using `kids/reviews/recruitment/` templates.

## Step 5
Assign pseudonymous IDs; record assignments in coverage matrices (`ASSIGNED`, not `COMPLETE`).

## Step 6
Send correct artifact + form for each role.

## Step 7
Receive and sanitize responses (strip PRIVATE_REVIEW_DATA / CHILD_SENSITIVE).

## Step 8
Place structured findings in intake directories (`publication/reviews/responses/`, `kids/reviews/responses/`).

## Step 9
Run review-ingest tooling:
```bash
make review-response-schema-check
.venv/bin/python scripts/review_intake.py ingest <file> --family adult|kids
make review-coverage-report
make review-integrity-check
```

## Step 10
Triage BLOCKER/MAJOR first.

## Step 11
Run evidence-driven revision PR (do not mutate R1 freeze in place — create R2+ for content changes).

## Step 12
Regenerate Kids candidates after Stage 1 fixes.

## Step 13
Only then prepare Kids Stage 2 supervised child usability (complete `KIDS_STAGE2_OWNER_DECISIONS.md` + ethics gate).

## Step 14
After child findings, revise again (R2+/later).

## Step 15
Only after all required validation and print/owner gates consider publication freeze.
