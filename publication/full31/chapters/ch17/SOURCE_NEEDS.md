# CH17 Source Needs

**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

Prefer standards/specs, official docs, peer-reviewed, and textbooks. Do not invent DOIs/ISBNs/pages.

| Priority | Class | Candidate / link | Why needed |
|---|---|---|---|
| 1 | standards | IEEE 802.11 family overview — SOURCE_NEEDED edition | Wi-Fi |
| 2 | standards | 3GPP TS 23.501 (system architecture) — SOURCE_NEEDED | 5G survey |
| 3 | inherit | ce-04 sources for Wi-Fi/cellular separation | Link |
| 4 | official_docs | Operator/OS UI docs for icon meanings — SOURCE_NEEDED | Bars literacy |

## Verification rule

- `SOURCE_IDENTIFIED` only when a real accepted-main or packet-local bib/register entry exists.
- `SOURCE_NEEDED` for gaps above.
- `PROJECT_EVIDENCE_NEEDED` / `PHYSICAL_PENDING` for Quartet/project measurements.

## Remaining SOURCE_NEEDED (EVIDENCE-A)

| Claim / need | Next step |
|---|---|
| Wi-Fi vs cellular / 5G icon literacy | `SOURCE_IDENTIFIED` via `ieee80211-2020`, `threegpp-ts23501`, `kurose-ross-8` |
| `CLM-CH17-003` 6G | Cite 3GPP study-item / roadmap primary only; keep “not deployed consumer fact” boundary. |
