# Errata workflow (stub)

**Status:** Stub for working full-manuscript draft  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Does not mean:** Gate 3 PASS, publication-ready, or fabricated human validation

## Intake

1. Prefer GitHub issues filed with `.github/ISSUE_TEMPLATE/errata.yml` (label `errata`).
2. Required fields: edition/version, chapter ID, severity (`critical` / `major` / `minor` / `typo`), description.
3. Reject or redact submissions that include secrets, private messages, device serials, or precise location.

## Triage

| Severity | Expected handling |
|---|---|
| `critical` | Safety, rights, or major factual error — prioritize fix + dated note |
| `major` | Teaching-impacting error — fix in next draft pass |
| `minor` | Clarity / consistency — batch with related edits |
| `typo` | Orthography — batch |

## Resolution record (minimum)

When accepting a fix, record:

- date (ISO)
- chapter / asset ID
- brief description of the error
- brief description of the fix
- link to issue or commit SHA

Store dated notes under `publication/full31/quality/errata/` when the first accepted erratum lands (directory created on first use). Do not invent a populated errata log.

## Non-claims

- Errata intake ≠ reader validation cohort.
- Fixture-validated labs ≠ human-validated claims.
- Do not add reviewer names, institutional seals, or endorsements via errata responses.
