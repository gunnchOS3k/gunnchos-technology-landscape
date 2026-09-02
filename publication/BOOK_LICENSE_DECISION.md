# Book / Artwork License Decision Record

**Status:** `AUTHOR_DECISION_PENDING`  
**Date opened:** 2026-09-02  
**Owner:** Edmund Gunn, Jr.

## Current truth

Wave 1 must **not** advertise a final publication-content license as approved.

Earlier draft text mentioned CC BY 4.0 for Chapter 2 prose and original figures. That statement is **withdrawn as an approved decision** until Edmund explicitly chooses a model.

## Separated license domains

| Domain | Candidate handling | Status |
|---|---|---|
| Runnable lab/code samples | May use a software license (for example MIT) if intentional | Documented as **proposed**, not final |
| Manuscript prose / instructor assets | Open, dual-license, or commercial/paid | **AUTHOR_DECISION_PENDING** |
| Original educational diagrams | Follow manuscript/artwork decision | **AUTHOR_DECISION_PENDING** |
| Upstream gunnchOS/WAIKE citations | Remain MIT-licensed upstream | unchanged |

## Candidate approaches (no selection made)

1. **Open book (e.g. CC BY 4.0)** — maximum redistribution; harder to later sell exclusive print/instructor packs without relicensing.
2. **Source-available / restricted commercial** — public reading of drafts; commercial rights reserved for print/instructor edition.
3. **Hybrid** — open companion repos + labs; commercial book/instructor materials.
4. **All-rights-reserved draft** until a public edition is declared.

Consequences differ for redistribution, classroom reuse, paid instructor guides, and storefront distribution. Edmund must choose.

## Publication wording rule

Until this record is updated with an approved decision:

- README and rights pages must say **license pending author decision**
- Do not badge or market the book as CC BY 4.0
- Do not treat repo `LICENSE` (if present for code/infra) as the book license
