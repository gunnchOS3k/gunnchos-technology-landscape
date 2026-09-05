# Review data governance (Adult + shared)

## Field classification
- `PUBLIC_SAFE` — sanitized structured findings OK in public repo
- `PRIVATE_REVIEW_DATA` — identifiable adult feedback stored outside public GitHub
- `CHILD_SENSITIVE_DO_NOT_COMMIT` — never commit child identifying data

## Defaults
- Pseudonymous reviewer IDs in-repo
- No real names required in public repo
- No child identifying data in repo
- No guardian contact info in repo
- Raw private feedback stored outside public GitHub if identifiable
- Repository receives sanitized structured findings only

## Retention
Owner-defined. Do not invent retention claims here.

## Related
Kids companion: `kids/reviews/KIDS_REVIEW_DATA_GOVERNANCE.md`
