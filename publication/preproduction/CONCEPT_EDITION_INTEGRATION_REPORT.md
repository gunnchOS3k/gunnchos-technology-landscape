# Concept Edition Integration Report

**schema_version:** `1.0.0`  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Integration branch:** `cursor/concept-edition-preproduction-001`  
**CH02 review snapshot:** `CH02-REVIEW-R1` — **untouched**

---

## A. Accepted-main SHA

`166e9544bc6e2aee344bc962ace76d49ee3e04e4` (contains merged PR #2)

## B. Five chapter package status

| Package | Required artifacts | Structured YAML contract |
|---|---|---|
| `ce-01` | 13/13 | Normalized to schema 1.0.0 |
| `ce-03` | 13/13 | Normalized to schema 1.0.0 |
| `ce-04` | 13/13 | Normalized to schema 1.0.0 |
| `ce-05` | 13/13 | Normalized to schema 1.0.0 |
| `ce-06` | 13/13 | Normalized to schema 1.0.0 |

No full canonical prose drafts. No Gate 3 PASS claims.

## C. Cross-chapter prerequisite graph (summary)

CE-1 (systems lens) → CE-2 open prototype (tap path; R1) → CE-3 (compute/storage/OS) → CE-4 (packets/access/edge-cloud) → CE-5 (AI/security/privacy/trust) → CE-6 (Stability Contract synthesis / EMIT capstone).

Chapter-local `depends_on` edges live in each `CONCEPT_GRAPH.yaml` under canonical `concepts:`.

## D. Glossary collisions

Candidate glossary rebuilt from normalized concepts with `glossary_candidate: true`.

- Exact cross-CE canonical-term collisions: **none detected in candidate rebuild**
- Alias / schema drift from Wave-13 agents: **migrated** (`nodes`→`concepts`, `plain_language`→`plain_language_definition`, …)
- CH02 compatibility: “Stability Contract” already taught in CH02 — align wording **after** R1 closes; do **not** edit R1 now
- Live `glossary/glossary.yaml` **not** modified

## E. Citation / source overlap

From regenerated `CANDIDATE_SOURCE_INDEX.yaml` (deterministic):

| Metric | Count |
|---|---:|
| Chapter source occurrences | 64 |
| Unique source records (by bib key) | 58 |
| standards/specifications | 18 |
| official technical documentation | 13 |
| peer-reviewed | 3 |
| textbooks | 9 |
| project accepted-main evidence | 7 |
| other explanatory | 8 |

**Metadata conflicts flagged:**

- `wcag22`: year `2023` (CE-1; W3C Recommendation 05 Oct 2023 note) vs `2024` (CE-6; cites 12 Dec 2024 Recommendation update) — same URL `https://www.w3.org/TR/WCAG22/`. Canonical dated-edition choice deferred; do not invent a third year.

Verification statuses used in the source index are truthful classes (`PRIMARY_METADATA_VERIFIED`, `REPOSITORY_EVIDENCE_VERIFIED`, `NEEDS_PRIMARY_VERIFICATION`) — **not** a blanket “verified because URL exists.”

Local bibs remain chapter-local; global `book/references/references.bib` not auto-merged.

## F. Figure system

**41** proposed figures after normalization.

| `truth_classification` | Count |
|---|---:|
| conceptual | 30 |
| illustrative | 9 |
| project_specific | 1 |
| measured | 1 |
| mixed | 0 |

Compound enums (`conceptual_project_qualified`, `project_specific_conceptual`, `measured_later_fixture`) migrated to base enum + optional `qualification`.

Shared visual templates still: system maps, sequences, comparative layers, status-vs-usable, failure/trust maps. None drawn yet.

## G. Lab progression

| Lab | Chapter | Role in progression |
|---|---|---|
| `LAB-SYS-001` | CE-1 | Observe / identify |
| `LAB-TAP-001` | CE-2 (live; R1) | Prototype measure (out of this PR’s CE-1/3–6 set) |
| `LAB-CMS-001` | CE-3 | Inspect hierarchy |
| `LAB-PKT-001` | CE-4 | Build/inspect path |
| `LAB-TRUST-001` | CE-5 | Measure/diagnose trust |
| `LAB-CE06-001` | CE-6 | Synthesize EMIT |

All CE-1/3/4/5/6 labs plan evidence artifacts + offline/fixture fallbacks. Distinct from `LAB-TAP-001`.

## H. WAIKE crosswalk

Accepted `gunnchOS3k/waike-research-ops/main` SHA reconfirmed:

`e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`

Relationship vocabulary retained: **exact / adjacent / proposed / no-map**.  
Publication lab IDs remain no-map/proposed as WAIKE modules. Live `waike/alignment.yaml` / CH02 R1 evidence **not** rewritten solely to refresh SHA.

## I. Device Quartet use

Foreshadow / `PHYSICAL_PENDING` only where claims require it. Labs do not require Quartet hardware. Balanced mentions: Student 14.5", Handheld Hybrid, DS-XL Coder, Edge IO Wearables — not forced into every chapter.

## J. Gate 3 dependency (waits on CH02 human feedback)

Before canonical CE prose drafting:

1. Real Explorer / Builder / Engineer reviews of `CH02-REVIEW-R1`
2. Optional Educator review
3. Editorial judgment on tone/depth/figure readability from R1
4. Promote selected candidates into live registries only after R1

This PR may merge as **preproduction research/contracts** while Gate 3 remains open.

---

## Schema migrations performed (this closure)

| Drift | Canonical action |
|---|---|
| `verified` / `planned` claim statuses | Mapped by meaning → Wave-13 statuses |
| `nodes:` | → `concepts:` |
| `plain_language` / `name` / `id` | → `plain_language_definition` / `canonical_term` / `concept_id` |
| `truth_class` / `conceptual_vs_measured` | → `truth_classification` |
| Compound truth enums | → base enum + `qualification` |
| `claim_text` / `claim_id` | → `text` / `provisional_id` |
| Claim class hyphen/space variants | → snake_case enum |
| Pathway-keyed learning objectives | → flat `objectives[]` with `reader_pathways` |
| `roles:` career collections | → `careers:` |
| Candidate indexes | Regenerated deterministically (`--check` clean) |

Contract path: `publication/preproduction/schema/` (`schema_version: "1.0.0"`).

Validator: `scripts/validate_ce_preproduction.py` **rejects** legacy drift (no longer tolerates variants).

## Exact claim counts by canonical status

| Status | Count |
|---|---:|
| SOURCE_IDENTIFIED | 43 |
| ILLUSTRATIVE_ONLY | 7 |
| PROJECT_EVIDENCE_NEEDED | 7 |
| PHYSICAL_PENDING | 4 |
| SOURCE_NEEDED | 1 |
| **Total** | **62** |

## Remaining automatable work

- Promote candidates into live registries **after** R1
- Implement runnable labs / draw figures from plans
- Resolve WCAG dated-edition preference when promoting global bib
- Optional: refresh live WAIKE SHA note in `evidence/source_registry.yaml` post-R1
