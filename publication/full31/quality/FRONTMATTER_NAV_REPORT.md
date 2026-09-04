# Front/back matter + navigation audit report (Agent I)

**Wave:** `full31-quality-convergence-001`  
**Base SHA:** `2e440e43f89b61c112f088939f73440024283bbf`  
**Machine audit:** `publication/full31/quality/FRONTMATTER_NAV_AUDIT.yaml`

## Verdict

Front/back matter is **structurally present and Gate-honest**. Navigability was weak (stubs without cross-links; incomplete lab/figure/role lists). This pass improves **indexes and hubs** without fabricating acknowledgments, endorsements, or human validation.

**Still not publication-ready.** Gate posture unchanged: `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`.

## Checklist

| Item | Result |
|---|---|
| Title / status | Pass — working-draft banner + Gate 3 posture |
| Preface | Pass — short; status retained |
| How to use | Improved — navigation hub |
| Know first | Added |
| Pathways | Pass |
| Device Quartet | Pass — research form factors / PHYSICAL_PENDING |
| WAIKE | Pass — not credentialing / not Gate 3 |
| Evidence/status legend | Improved — lab maturity labels clarified |
| Rights | Added reader-facing notice (ARR © 2026; MIT scoped; no blanket CC) |
| Acknowledgments | Placeholder only |
| Glossary index | Improved — 91 term IDs from `glossary/glossary.yaml` |
| References | Improved — bib + working bibliography pointers |
| Key standards | Added — 25 `standards_specifications` keys |
| Figure index | Improved — 107 figures; chapter from `figure_id` |
| Lab index | Improved — 14 registry labs (was 6) |
| Career-role map | Improved — 18 roles; no employment guarantee |
| Parts/chapters | Added — 31 chapters / 6 canonical parts |
| Errata | Issue template existed; workflow stub + reader page added |
| Subject index | Explicitly **not** claimed as publication-grade |

## Notable finding

`figures/figure_registry.yaml` has **55** truncated `chapter:` values (`CH1-`, `CH0-`, …). Figure index derives chapter from `figure_id`. Registry rewrite left to visuals/registry owner to avoid clash.

## Files touched (summary)

- `_quarto.yml` — wired new front/back pages
- `index.qmd`, `book/frontmatter/*`, `book/appendices/*`
- `publication/full31/quality/FRONTMATTER_NAV_AUDIT.yaml`
- `publication/full31/quality/ERRATA_WORKFLOW.md`
- `publication/full31/quality/FRONTMATTER_NAV_REPORT.md` (this file)

## Non-claims

No Gate 3 PASS. No fabricated reviewers/endorsements. No blanket CC. Traditional subject index remains editorial.
