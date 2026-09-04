# Full31 Continuity Report

**Generated:** 2026-09-03  
**Base SHA:** `3264321e0f878e16fb4d6b0f84cd189ac4538532`  
**Tool:** `scripts/audit_full31_continuity.py` (audit aid; not auto-rewrite)

## Scope

- All 31 manuscript chapters under `book/chapters/ch*/chapter.md`
- Flags: repeated blocks, near-duplicates, templated filler, contradictions,
  term-before-explain, bad transitions, identity collisions
- Whitelist: Stability Contract canonical sentence, status/gate banners, safety
  boundaries, glossary boilerplate, pedagogical scaffolds, Device Quartet caveats

## Counts

| Metric | Count |
|---|---:|
| Total findings | 360 |
| FIX_CANDIDATE | 0 |
| INTENTIONAL_RETAIN | 268 |
| OPEN | 92 |
| FIXED (post Phase 2) | 0 |

### By kind

| Kind | Count |
|---|---:|
| `bad_transition` | 28 |
| `contradiction` | 1 |
| `near_duplicate` | 282 |
| `repeated_block` | 30 |
| `templated_filler` | 1 |
| `term_before_explain` | 18 |

### By severity

| Severity | Count |
|---|---:|
| MODERATE | 48 |
| MINOR | 18 |
| EDITORIAL | 294 |

## Chapter identity matrix

Canonical machine-readable matrix:
`publication/full31/quality/CHAPTER_IDENTITY_MATRIX.yaml`

Human-readable companion:
`publication/full31/quality/CHAPTER_IDENTITY_MATRIX.md`

Identity-clear chapters: **31 / 31**

## Highest-priority fix candidates

_No FIX_CANDIDATE items._

## Intentional retained samples

- **CONT-REPEATED_BLO-001** CH01, CH14 — Exact normalized paragraph repeated across chapters.
- **CONT-REPEATED_BLO-002** CH01, CH14 — Exact normalized paragraph repeated across chapters.
- **CONT-REPEATED_BLO-003** CH01, CH14 — Whitelisted deliberate repeated construct.
- **CONT-REPEATED_BLO-004** CH01, CH02, CH07, CH14 — Whitelisted deliberate repeated construct.
- **CONT-REPEATED_BLO-005** CH02, CH03, CH04, CH05, CH06, CH07, CH08, CH12, CH14, CH16, CH23 — Whitelisted deliberate repeated construct.
- **CONT-REPEATED_BLO-007** CH03, CH07 — Whitelisted deliberate repeated construct.
- **CONT-REPEATED_BLO-008** CH06, CH12 — Exact normalized paragraph repeated across chapters.
- **CONT-REPEATED_BLO-009** CH06, CH07, CH12 — Exact normalized paragraph repeated across chapters.
- **CONT-REPEATED_BLO-010** CH06, CH12 — Exact normalized paragraph repeated across chapters.
- **CONT-REPEATED_BLO-011** CH06, CH12 — Exact normalized paragraph repeated across chapters.
- **CONT-REPEATED_BLO-012** CH06, CH12 — Exact normalized paragraph repeated across chapters.
- **CONT-REPEATED_BLO-013** CH06, CH12 — Whitelisted deliberate repeated construct.
- … 256 more retained (see ledger)

## Phase 2 resolutions (this wave)

Scoped prose edits only; chapters not merged; Gate 3 untouched.

### Fixed (harmful duplication / identity collision)

- **CH31** — Distinct EMIT/portfolio anchor moment; notice + Try It reframed to inherit CH20/CE-6 instead of re-teaching connected≠usable; career/check prompts capstone-specific.
- **CH12** — LAB-CMS-001 observable question + prediction + misconception probe reframed to process/thread/scheduler (no longer a CH06 CPU clone).
- **CH07** — LAB-CMS-001 observable question reframed to memory/storage/hierarchy.
- **CH14** — LAB-SYS-001 observable question reframed to UI/runtime/libraries/APIs.
- **CH06** — OS-vs-app misconception probe points forward to CH12 instead of cloning CH12 wording.

### Intentional retained

- Canonical Stability Contract sentence and local elaborations.
- Status / Gate banners; safety / privacy / redaction boundaries.
- Shared lab packet scaffolding (LAB-CMS-001, LAB-CE06-001) where chapters deliberately inherit.
- Pedagogical scaffold headings (moment → notice → …) and glossary boilerplate.

## Phase 2 policy

- Fix only clear harmful duplication / contradictions.
- Do not remove helpful reinforcement.
- Do not merge chapters.
- Do not touch Gate 3 / CH02-REVIEW-R1.

## Method notes

- Exact match: SHA1 of normalized paragraph (citations/markup stripped).
- Near match: 5-token shingle Jaccard ≥ 0.55 with inverted-index candidates.
- Identity collision: token Jaccard ≥ 0.72 on anchor moments; exact central questions.
- Whitelist patterns live in `scripts/audit_full31_continuity.py`.

