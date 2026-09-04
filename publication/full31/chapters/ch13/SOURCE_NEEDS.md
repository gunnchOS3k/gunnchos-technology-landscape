# CH13 Source Needs

**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

Prefer standards/specs, official docs, peer-reviewed, and textbooks. Do not invent DOIs/ISBNs/pages.

| Priority | Class | Candidate / link | Why needed |
|---|---|---|---|
| 1 | textbook | Tanenbaum & Bos — filesystems | FS abstractions |
| 2 | textbook | Database system textbook TBD — SOURCE_NEEDED bib key | DB models |
| 3 | standards | ISO/IEC data quality / privacy frameworks as pointers — SOURCE_NEEDED specific cites | Lifecycle language |
| 4 | official_docs | SQLite / Postgres docs (living) as concrete examples | Not product endorsements |
| 5 | inherit | ce-05 SOURCE_REGISTER lifecycle/privacy sources | Link |

## Verification rule

- `SOURCE_IDENTIFIED` only when a real accepted-main or packet-local bib/register entry exists.
- `SOURCE_NEEDED` for gaps above.
- `PROJECT_EVIDENCE_NEEDED` / `PHYSICAL_PENDING` for Quartet/project measurements.

## Remaining SOURCE_NEEDED (QUALITY-E)

| Claim / need | Status / next step |
|---|---|
| `CLM-CH13-003` databases vs files | `SOURCE_IDENTIFIED` via `postgresql-mvcc` (official concurrency docs; no invented ACID slogans) |
| `CLM-CH13-004` cloud sync conflicts | Still `SOURCE_NEEDED` — select distributed-systems chapter and/or official sync-conflict docs |
| `CLM-CH13-005` deletion / replicas | `SOURCE_IDENTIFIED` via `nist-sp800-88r1` (sanitization vs recoverability; no exploit steps) |
