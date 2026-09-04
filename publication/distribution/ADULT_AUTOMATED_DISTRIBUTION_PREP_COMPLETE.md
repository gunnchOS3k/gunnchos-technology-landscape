# State: ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE

**Declared:** 2026-09-03  
**Track:** Adult Publication + Distribution (PR #7 Track 1)  
**Integration base tip:** `cursor/publication-family-parallel-production-001`

## Meaning (allowed aggregate)

Automatable packaging and print-profile rendering for the Adult FULL31 edition are complete:

- Canonical FULL31 EPUB/PDF bytes landed in channel `artifacts/` (typed; hashed).
- Print profiles `print-6x9` / `print-7x10` / `print-85x11` rendered; results recorded under
  `publication/distribution/print/PRINT_PROFILE_RESULTS.*`.
- Package readiness vocabulary enforced by `adult-artifact-package-check`.
- Per-channel states remain honest owner/human blocks (cover, ISBN, metadata, review).

## Package readiness vocabulary

`SCAFFOLD_ONLY` | `ARTIFACTS_BUILT` | `VALIDATED_LOCALLY` | `BLOCKED_OWNER_COVER` |
`BLOCKED_OWNER_METADATA` | `BLOCKED_OWNER_ISBN` | `BLOCKED_HUMAN_REVIEW` | `READY_FOR_OWNER_UPLOAD`

## Explicitly NOT claimed

- `PUBLICATION_READY`
- `READY_FOR_OWNER_UPLOAD` (owner cover / ISBN / human review still blocked)
- Retailer-approved / live listing / uploaded
- WCAG certified
- Gate 3 PASS
- HUMAN_VALIDATED beyond freeze record (**still 0/31**)
- ISBN purchase / account creation / KDP Select enrollment
- Invented spine inches (cover wraps: `LIVE_COVER_CALCULATOR_REQUIRED`)
- Automated Kindle Previewer (`KINDLE_PREVIEWER_HUMAN_OR_EXTERNAL_PENDING`)

## Frozen provenance preserved

- `verified_candidate_content_sha`: `dd7f0003beae5c56d5ee8b5050aff151ef67d803`
- Package: `publication/review-candidates/FULL31-PRE-REVIEW-001/`
- Gate 3 remains `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`
