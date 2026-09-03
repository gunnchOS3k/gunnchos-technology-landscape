# PR #5 — Full 31-chapter working manuscript draft

## Meaning

This PR turns the 31-chapter Technology Landscape architecture into a complete working manuscript draft. Reader validation has been deliberately deferred by the owner until the full manuscript exists. This PR does not fabricate reader evidence, claim Gate 3 PASS, or declare the book publication-ready.

**Asset/reference closure (this update):** every reader-facing `FIG-*` reference now resolves to a registered asset with accessibility metadata; production/meta-text was removed from reader prose; strict asset/reference CI checks added. `FIG-CE3-009` remains `BLOCKED_EVIDENCE_REQUIRED` and is not a live reader-facing figure ref.

## Truth anchors

| Item | Value |
|---|---|
| Accepted `main` | `18ec58005529bd16d680ee7419e4dea13150e9c6` |
| Branch | `cursor/full31-manuscript-draft-001` |
| Validation sequence | `READER_VALIDATION_DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT` |
| Gate posture | `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` |
| Working drafts | **31/31** |
| Human validated | **0/31** |
| Publication ready | **0/31** |
| CH02-REVIEW-R1 | **UNCHANGED** |

## Manuscript words (deterministic inventory)

See `publication/full31/FULL31_MANUSCRIPT_INVENTORY.md`.

- total ≈ **120,089**
- min / max / mean / median from inventory generator
- no chapter `<2500` words

## Citations / sources

- Reader-facing citations resolve against `book/references/references.bib`
- Internal `SOURCE_NEEDED` remaining: **13** (omitted/reframed from prose)
- `PROJECT_EVIDENCE_NEEDED`: **0**
- `PHYSICAL_PENDING`: **25**
- Unsupported `SOURCE_NEEDED` in reader prose: **0**
- WCAG dated Recommendations kept distinct (`wcag22-20231005`, `wcag22-20241212`)

## Figures

- Reader-facing figure refs resolve (strict `make full31-assets-check`)
- Implemented conceptual/illustrative Full31 SVGs for previously dangling CH11/13–14/17–22/24–31 refs
- `FIG-CH24-001/002/003` assets present under `figures/full31/ch24/`
- `FIG-CE3-009` remains **BLOCKED_EVIDENCE_REQUIRED** (not a live reader ref)
- Accessibility sidecars required; malformed SVG / missing title/desc fail CI

## Labs / activities

- Try It **31/31** · Build It **31/31**
- Full lab packages under `labs/`
- Proposed-only `LAB-*` IDs allowed only with explicit proposed context

## Glossary / WAIKE / Quartet

- Glossary promotion retained; deterministic checks remain
- WAIKE SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` — exact 0 / adjacent 122 / proposed 24 / no-map 43
- Device Quartet physical claims remain `PHYSICAL_PENDING`

## Checks

```text
make validate
make test
make full31-draft-check FULL31_DRAFT_CHECK_MODE=strict
make full31-assets-check
make full31-reference-check
make full31-inventory
```

Hosted CI must be green on the exact final HEAD (validation, tests, strict draft + assets, NO_READER_EVIDENCE, CH02 + full31 HTML/EPUB/PDF, artifacts).

## Remaining human work

- Explorer / Builder / Engineer / Educator reviews after owner recruitment
- Technical/editorial review
- Human visual/print QA
- Physical Device Quartet validation where claims require it

## Merge recommendation (owner only)

`PR5_FULL31_DRAFT_READY_FOR_OWNER_MERGE` when hosted CI is green on final HEAD.

Does **not** mean human-validated or publication-ready. Do not auto-merge.
