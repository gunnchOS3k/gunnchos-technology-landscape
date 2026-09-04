# Adult release package — `amazon-kindle`

**Package readiness:** `BLOCKED_OWNER_COVER`  
**Aggregate track state (when packaging complete):** `ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE`  
**Not:** `PUBLICATION_READY` · `READY_FOR_OWNER_UPLOAD` · not uploaded · no credentials · not Gate 3 PASS  
**HUMAN_VALIDATED:** 0/31

## Provenance (frozen; do not rewrite)

- FULL31 pre-review content SHA: `dd7f0003beae5c56d5ee8b5050aff151ef67d803`
- Candidate package: `publication/review-candidates/FULL31-PRE-REVIEW-001/`
- Gate 3: `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Contents

| Path | Role |
| --- | --- |
| `MANIFEST.yaml` | Declared package files + readiness |
| `CHECKSUMS.sha256` | Hashes for present files |
| `validation-stub.md` | Automated checks that *could* run later |
| `HUMAN_CHECKLIST.md` | Human-only upload checklist — no secrets |
| `artifacts/` | Typed artifacts and/or owner-blocked stubs |

## Channel notes

- Manuscript EPUB copied from canonical FULL31 render.
- Cover remains owner-blocked; do not treat SVG technical proof as final.
- `KINDLE_PREVIEWER_HUMAN_OR_EXTERNAL_PENDING` — not automatable in this environment.
- Also blocked: ISBN purchase, human Gate 3 review.

## Non-claims

- Do not actually upload from this package without owner approval.
- Cover technical proofs are **not** final marketing art.
- ISBN placeholders remain `PENDING_OWNER_PURCHASE`.
- Kindle Previewer is not automated here (`KINDLE_PREVIEWER_HUMAN_OR_EXTERNAL_PENDING` when applicable).
