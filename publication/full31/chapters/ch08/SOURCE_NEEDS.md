# CH08 Source Needs — Graphics, Displays, Audio, Cameras, and Sensors

**Chapter:** `CH08`  
**WAIKE SHA used for adjacency audits:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Rule:** Prefer standards, official docs, peer-reviewed, and textbooks. No invented facts.

## Needs table

| ID | Need | Preferred type | Status class | Notes |
|---|---|---|---|---|
| `SRC-CH08-01` | Computer graphics / multimedia systems survey text — identify edition. | textbook | `SOURCE_NEEDED` | Keep survey depth |
| `SRC-CH08-02` | Platform official docs for camera/microphone permission models (privacy tie-in). | official_docs | `SOURCE_NEEDED` | Pick representative docs; no OS encyclopedia |
| `SRC-CH08-03` | WCAG for non-visual alternatives and motion sensitivity. | standards | `SOURCE_IDENTIFIED` | Reuse WCAG citation discipline from CE-1 |

## Verification policy

- `SOURCE_IDENTIFIED` — concrete work exists or CE package already keyed it; still verify before prose.
- `SOURCE_NEEDED` — must locate primary citation before canonical drafting.
- `PROJECT_EVIDENCE_NEEDED` — publication/repo evidence required.
- `PHYSICAL_PENDING` — Device Quartet / EVT / fabrication claims.

## Non-sources

- Marketing pages as sole authority for technical laws.
- Invented DOIs/ISBNs/page numbers.
- Fabricated Gate 3 reader quotes.

## Remaining SOURCE_NEEDED (QUALITY-E)

| Claim / need | Status / next step |
|---|---|
| `CLM-CH08-001` display frame deadlines / hitching | `SOURCE_IDENTIFIED` via `mdn-requestanimationframe` + `whatwg-html` (qualitative frame timing only; no invented hitch thresholds) |
| Camera/mic sampling | `SOURCE_IDENTIFIED` via `w3c-mediacapture-streams-20251009` |
