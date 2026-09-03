# CH10 Source Needs — Ports, Buses, Boards, Packaging, and Manufacturing

**Chapter:** `CH10`  
**WAIKE SHA used for adjacency audits:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Rule:** Prefer standards, official docs, peer-reviewed, and textbooks. No invented facts.

## Needs table

| ID | Need | Preferred type | Status class | Notes |
|---|---|---|---|---|
| `SRC-CH10-01` | Digital design / computer engineering text covering buses and interconnect survey. | textbook | `SOURCE_NEEDED` | Identify edition |
| `SRC-CH10-02` | Selected interface standards only when making specific protocol claims (USB-IF, JEDEC, etc.). | standards | `SOURCE_NEEDED` | Cite specific docs; avoid catalog dump |
| `SRC-CH10-03` | WAIKE lab_bus_protocol / lab_pcb_erc_drc adjacency. | repository | `SOURCE_IDENTIFIED` | SHA e97e74fc9bfb44b1cdc26b272dc4848264f15fe0 |
| `SRC-CH10-04` | IPC or equivalent PCB/DFM overview references for manufacturing literacy. | standards_or_textbook | `SOURCE_NEEDED` | Survey depth |

## Verification policy

- `SOURCE_IDENTIFIED` — concrete work exists or CE package already keyed it; still verify before prose.
- `SOURCE_NEEDED` — must locate primary citation before canonical drafting.
- `PROJECT_EVIDENCE_NEEDED` — publication/repo evidence required.
- `PHYSICAL_PENDING` — Device Quartet / EVT / fabrication claims.

## Non-sources

- Marketing pages as sole authority for technical laws.
- Invented DOIs/ISBNs/page numbers.
- Fabricated Gate 3 reader quotes.
