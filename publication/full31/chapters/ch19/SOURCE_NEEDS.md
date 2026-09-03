# CH19 Source Needs

**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

Prefer standards/specs, official docs, peer-reviewed, and textbooks. Do not invent DOIs/ISBNs/pages.

| Priority | Class | Candidate / link | Why needed |
|---|---|---|---|
| 1 | standards | 3GPP NTN-related specifications/study items — SOURCE_NEEDED exact IDs | NTN vocabulary |
| 2 | peer_reviewed_or_official | ITU/3GPP roadmap materials dated — SOURCE_NEEDED | Capability honesty |
| 3 | inherit | evidence/ACCEPTED_MAIN_SOURCE_AUDIT.md note on NTN repos | Do not fabricate |
| 4 | inherit | ce-04/ce-06 continuity language | Link |

## Verification rule

- `SOURCE_IDENTIFIED` only when a real accepted-main or packet-local bib/register entry exists.
- `SOURCE_NEEDED` for gaps above.
- `PROJECT_EVIDENCE_NEEDED` / `PHYSICAL_PENDING` for Quartet/project measurements.

## Remaining SOURCE_NEEDED (EVIDENCE-A)

| Claim / need | Next step |
|---|---|
| `CLM-CH19-001` NTN ≠ terrestrial 5G | `SOURCE_IDENTIFIED` via `threegpp-ts23501` (pin dated PDF before clause quotes) |
| `CLM-CH19-002` service continuity | `SOURCE_IDENTIFIED` via ITU-T QoE keys + TS 23.501 |
| `CLM-CH19-003` orbit delay regimes | Qualitative physics/standards cite without inventing product latency numbers. |
| `CLM-CH19-004` marketing capability class | Operator capability docs distinguishing messaging-only vs broadband modes. |
