# Publication Family — Parallel Production Wave

Scaffold for **publication-family parallel production** on
`cursor/publication-family-parallel-production-001`.

This tree coordinates adult / kids / distribution / metadata tracks **in
parallel** with Gate 3 reader-evidence work. It does **not** advance
publication gates or rewrite frozen FULL31-PRE-REVIEW-001 provenance.

## Preserved production state (do not invent progress)

```
31/31 WORKING_DRAFT_COMPLETE
FULL31_PRE_HUMAN_REVIEW_CANDIDATE_READY
HUMAN_VALIDATED = 0/31
PUBLICATION_READY = 0/31
GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING
```

## Parallel tracks

| Track | Path | Role |
| --- | --- | --- |
| Family coordination | `publication/family/` | Wave README, track status, non-claims |
| Distribution stubs | `publication/distribution/` | Channel / format packaging placeholders |
| Metadata stubs | `publication/metadata/` | Catalog / ISBN / rights metadata placeholders |
| Adult release packages | `release-packages/adult/` | Adult-edition package stubs |
| Kids | `kids/` | Kids-edition stubs (separate from adult FULL31) |

Tracks may proceed independently. Completing a stub or draft on one track
does **not** imply readiness on another.

## Non-claims

- Scaffold ≠ publication-ready product.
- Presence of directories or READMEs is **not** Gate advancement.
- Parallel family work does **not** change Gate 3 status or counts above.
- Do **not** modify `publication/gates/gate-3/` from this wave’s scaffold.
- Do **not** rewrite frozen `publication/review-candidates/FULL31-PRE-REVIEW-001/` provenance.
- Kids / adult stubs are **not** HUMAN_VALIDATED or PUBLICATION_READY evidence.

## Status vocabulary

Use these labels only; do not invent softer synonyms that imply gate progress.

| Status | Meaning |
| --- | --- |
| `SCAFFOLD_ONLY` | Empty or stub path; no deliverable content yet |
| `IN_PROGRESS` | Active drafting on this track; not reviewable as a release |
| `DRAFT_INTERNAL` | Internal draft exists; not human-validated for publication |
| `BLOCKED` | Waiting on dependency (e.g. Gate 3 reader evidence, rights) |
| `READY_FOR_TRACK_REVIEW` | Track-local review only — **not** PUBLICATION_READY |
| `PUBLICATION_READY` | Reserved; requires explicit gate/evidence criteria (currently 0/31) |

Wave bootstrap status (initial): **`SCAFFOLD_ONLY`**.

Adult distribution track update: see
`publication/distribution/ADULT_DISTRIBUTION_READINESS_REPORT.md` —
track-local **`READY_FOR_TRACK_REVIEW`** / ceiling
`ADULT_SUBMISSION_PACKAGE_PREPARED` (still **not** `PUBLICATION_READY`).

## Frozen references (read-only for this wave)

- FULL31 pre-human-review candidate: `publication/full31/FULL31_PRE_HUMAN_REVIEW_CANDIDATE.md`
- Review package: `publication/review-candidates/FULL31-PRE-REVIEW-001/`
- Gate 3: `publication/gates/gate-3/`

## Integrator status vocabulary (enforced)

| Edition | Ceiling this wave | Explicitly not claimed |
| --- | --- | --- |
| Adult | `ADULT_SUBMISSION_PACKAGE_PREPARED` | `PUBLICATION_READY`, retailer-approved, Gate 3 PASS |
| Kids | `KIDS_DEVELOPMENTAL_PROTOTYPE` / ready-for-human-review if justified | `PUBLICATION_READY`, child-validated, officially aligned |

Rights: ARR manuscript; MIT scoped to tooling/labs; **no blanket CC**. Free price ≠ open license.

See also: `PUBLICATION_FAMILY_REGISTRY.yaml`, `EXTERNAL_GATES.yaml`, `OWNER_DECISIONS_NEEDED.md`, `PARALLEL_PRODUCTION_STATUS.md`.
