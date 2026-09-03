# Full31 draft check — modes for Batch 0 / Batch 1+

Target command:

```bash
make full31-draft-check
# or
python scripts/validate_full31_draft.py --mode infra|strict
```

Environment override: `FULL31_DRAFT_CHECK_MODE=infra|strict` (default **`infra`**).

---

## Mode `infra` (Batch 0 / current)

**Purpose:** Authoring infrastructure is ready; chapters **may still be scaffolds**.

Pass criteria (errors fail the check):

- 31 chapter files exist under `book/chapters/chNN/chapter.md`
- Titles match `book/chapter_registry.yaml` / Full31 registry
- Root `_quarto.yml` lists all 31 chapters + required front/back matter
- Publication status banner present in working manuscript metadata/front matter
- Forbidden publication claims absent (`GATE_3_PASS`, “publication-ready” as a claim of readiness)
- No secrets / credential patterns in chapter prose
- No synthetic “human reader evidence” presented as completed Gate 3 / FULL31 review

Warn / status only (do **not** fail `infra`):

- Chapter still scaffold / outline
- Missing 12 anatomy anchors on non-CH02 chapters
- Unresolved refs on unfinished chapters

Exit code: **0** when infrastructure is ready (warnings printed).

---

## Mode `strict` (`WORKING_DRAFT_COMPLETE`)

**Purpose:** Claim that the full working manuscript draft is complete. Use only when Batch 1+ authoring is finished.

Additional fail criteria:

- All 31 chapters **non-scaffold**
- Titles match registry
- All 12 anatomy anchors present in each chapter
- Citations / figures / labs / glossary refs resolve where referenced
- No reader-facing placeholders: `TODO`, `TBD`, `[INSERT]`, etc.
- No agent meta-text in reader prose
- No `vscode-file://` or local filesystem paths in reader text
- No secrets
- No synthetic evidence labeled as human validation
- Status banner still present; still **not** Gate 3 PASS / publication-ready

Exit code: **1** until all 31 chapters meet working-draft completeness.

---

## What this is not

- Not Gate 3 PASS
- Not human validation complete (`DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT`)
- Not permission to create `FULL31-REVIEW-R1` yet
- Does not modify `publication/gates/gate-3/`
