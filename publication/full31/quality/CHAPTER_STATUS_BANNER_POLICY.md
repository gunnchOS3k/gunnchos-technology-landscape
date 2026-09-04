# Chapter status / banner policy (canonical)

**Status:** ACTIVE for Full31 working drafts  
**Closes:** TECH-B-CH17-002

## Canonical sources of truth (prefer these)

1. **Book-level manuscript status** — `book/frontmatter/status.qmd` and the title `index.qmd` callout.
2. **Per-chapter YAML fields** (metadata.yaml and chapter.md YAML header), which must remain:

```yaml
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
```

3. **Generic chapter `status:`** — use `draft` for all Full31 working chapters (cosmetic consistency). Do not invent a second parallel vocabulary (`working_draft` vs `draft`).

4. **Gate posture** — book-level only unless a chapter has a *local* evidence exception that must be stated for honesty:

```text
GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING
```

Do **not** require every chapter to repeat a Gate 3 boilerplate banner in reader prose when the book-level status page already communicates the gate. Optional one-line reminders in chapter inheritance/closing sections remain allowed where they add local clarity.

## Not required

- Matching Gate 3 one-liners in every chapter opening status block.
- Reader-facing repetition of full Gate 3 protocol text.

## Forbidden

- Claiming Gate 3 PASS, HUMAN_VALIDATED completion, or PUBLICATION_READY in chapter banners.
- Fabricating reader evidence.
