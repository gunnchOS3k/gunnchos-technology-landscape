# Full31 progress dimensions (normalized)

All Full31 progress reports, dashboards, and agent handoffs use these **seven dimensions**. Do not collapse them into a single “% complete.”

| Dimension | Meaning | Honest “done” signal |
|---|---|---|
| **architecture** | Chapter exists in canonical 31-chapter registry / book architecture | `31/31` registered |
| **packet** | Preproduction packet files present + semantically valid | `packet_state: PACKET_COMPLETE` |
| **substantive_preproduction** | Concepts, sources, claims, figures, labs, glossary, WAIKE planned | `current_state: PREPRODUCTION_COMPLETE` (or higher) |
| **working_draft** | Canonical chapter prose is a full working draft (not scaffold) | `canonical_prose_state: DRAFT_COMPLETE` |
| **technical_review** | Independent technical review complete for that chapter | Tracked separately; not claimed by packet completeness |
| **human_validation** | Real-reader evidence for the relevant review snapshot | Deferred until full manuscript (`DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT`) |
| **publication_readiness** | Editorial + rights + release gates satisfied for ship | Never inferred from Quarto success alone |

## Coverage block (required shape)

```text
architecture:              NN/31
packet:                    NN/31
substantive_preproduction: NN/31 complete (MM/31 started)
working_draft:             NN/31
technical_review:          NN/31
human_validation:          NN/31
publication_readiness:     NN/31
```

Legacy lines such as `31/31 architecture registered` and `1/31 canonical full drafts` remain acceptable synonyms in `FULL31_PROGRESS_REPORT.md` so existing validators stay truthful.

## Gate posture (always)

`GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

- CH02-REVIEW-R1 is historical chapter-prototype evidence, not full-manuscript validation.
- See `VALIDATION_SEQUENCE_DECISION.md`.
