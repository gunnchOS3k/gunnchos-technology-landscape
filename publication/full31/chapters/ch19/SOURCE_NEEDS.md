# CH19 Source Needs

**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Publication accepted-main:** `18ec58005529bd16d680ee7419e4dea13150e9c6`  
**WAIKE accepted-main:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`

Prefer standards/specs, official docs, peer-reviewed, and textbooks. Do not invent DOIs/ISBNs/pages.

| Priority | Class | Candidate / link | Why needed |
|---|---|---|---|
| 1 | standards | 3GPP NTN-related specifications/study items — SOURCE_NEEDED exact IDs | NTN vocabulary |
| 2 | peer_reviewed_or_official | ITU/3GPP roadmap materials dated — SOURCE_NEEDED | Capability honesty |
| 3 | project | waike `case_studies/7gc/graham_land/polar_ntn_simulation/` @ e97e74f… | Synthetic teaching fixture only; CLM-CH19-005 = PHYSICAL_PENDING |
| 4 | inherit | ce-04/ce-06 continuity language | Link |

## Verification rule

- `SOURCE_IDENTIFIED` only when a real accepted-main or packet-local bib/register entry exists.
- `SOURCE_NEEDED` for gaps above.
- `PROJECT_EVIDENCE_NEEDED` / `PHYSICAL_PENDING` for Quartet/project measurements.
- Do not treat synthetic NTN case studies as field-validated twin evidence.

## Evidence updates (Batch 0)

| Claim / need | Status / next step |
|---|---|
| `CLM-CH19-001` NTN ≠ terrestrial 5G | `SOURCE_IDENTIFIED` via `threegpp-ts23501` (pin dated PDF before clause quotes) |
| `CLM-CH19-002` service continuity | `SOURCE_IDENTIFIED` via ITU-T QoE keys + TS 23.501 |
| `CLM-CH19-003` orbit delay regimes | `SOURCE_NEEDED` — qualitative physics/standards cite without inventing product latency numbers |
| `CLM-CH19-004` marketing capability class | `SOURCE_NEEDED` — operator capability docs distinguishing messaging-only vs broadband modes |
| `CLM-CH19-005` | `PHYSICAL_PENDING` — synthetic NTN case study is teaching fixture only |
