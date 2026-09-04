# CH11 Source Needs

**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

Prefer standards/specs, official docs, peer-reviewed, and textbooks. Do not invent DOIs/ISBNs/pages.

| Priority | Class | Candidate / link | Why needed |
|---|---|---|---|
| 1 | textbook | Tanenbaum & Bos, Modern Operating Systems (tanenbaum-bos) | Boot/OS handoff, privilege |
| 2 | textbook | Saltzer & Kaashoek (saltzer-kaashoek) | Names/protection/trust boundaries |
| 3 | standards | UEFI Forum Secure Boot / UEFI Specification (official) | Secure boot policy model — SOURCE_NEEDED exact edition cite |
| 4 | standards | Trusted Computing Group / attestation overview materials | Measured boot/attestation vocabulary — SOURCE_NEEDED |
| 5 | official_docs | Linux kernel / platform vendor boot documentation (living) | Concrete examples without universalizing |
| 6 | project | devices/quartet.yaml + hardware-repo evidence | PHYSICAL_PENDING for Quartet-specific claims |

## Verification rule

- `SOURCE_IDENTIFIED` only when a real accepted-main or packet-local bib/register entry exists.
- `SOURCE_NEEDED` for gaps above.
- `PROJECT_EVIDENCE_NEEDED` / `PHYSICAL_PENDING` for Quartet/project measurements.

## Remaining SOURCE_NEEDED (QUALITY-E)

| Claim / need | Status / next step |
|---|---|
| Secure Boot | `SOURCE_IDENTIFIED` via `uefi-secure-boot-2.10` |
| Attestation / measured boot | `SOURCE_IDENTIFIED` via `tcg-pc-client-pfp-1.06` |
| `CLM-CH11-006` interrupted firmware updates | `SOURCE_IDENTIFIED` via `android-ab-ota` (AOSP A/B seamless updates; living docs; representative example) |
