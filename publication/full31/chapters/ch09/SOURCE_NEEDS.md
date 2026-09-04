# CH09 Source Needs — Power, Batteries, Thermals, and Mechanical Design

**Chapter:** `CH09`  
**WAIKE SHA used for adjacency audits:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Rule:** Prefer standards, official docs, peer-reviewed, and textbooks. No invented facts.

## Needs table

| ID | Need | Preferred type | Status class | Notes |
|---|---|---|---|---|
| `SRC-CH09-01` | Embedded/mobile systems or electronics text covering power/thermal design survey. | textbook | `SOURCE_NEEDED` | Identify edition |
| `SRC-CH09-02` | Battery safety standards overview (cite specific IEC/UL docs carefully; no DIY abuse labs). | standards | `SOURCE_NEEDED` | Safety-first |
| `SRC-CH09-03` | WAIKE lab_power_budget / lab_ep_sleep_mode as adjacency. | repository | `SOURCE_IDENTIFIED` | SHA e97e74fc9bfb44b1cdc26b272dc4848264f15fe0 |

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
| `CLM-CH09-001` power/thermal budgets | `SOURCE_IDENTIFIED` via `linux-cpu-freq` |
| `CLM-CH09-002` batteries | `SOURCE_IDENTIFIED` via `iec-62133-2` + `ul-2054` (safety posture only; no DIY abuse labs) |
| `CLM-CH09-003` mechanical design | Reframed `ILLUSTRATIVE_ONLY` — qualitative teaching model; no pinned industrial-design textbook this wave |
