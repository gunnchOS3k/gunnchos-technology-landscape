# Lab / Try It / Build It audit report (Agent G)

**Branch:** `cursor/full31-quality-convergence-001`  
**Base:** `2e440e43f89b61c112f088939f73440024283bbf`  
**Ledger:** `publication/full31/quality/LAB_ACTIVITY_AUDIT.yaml`  
**Gate:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (unchanged)

## Counts

| Class | Count |
|---|---|
| Try It preserved | **31/31** |
| Build It preserved | **31/31** |
| FULL_LAB (under `labs/`) | **14** |
| Primary INLINE_ACTIVITY chapters | **4** (CH26, CH29, CH30; CH19 NTN doc route) |
| PROPOSED_LAB IDs audited | **17** |
| Proposed → full lab implemented this wave | **0** (no new low-value `labs/` dirs) |
| Proposed → inline | **10** (CPU, MEM, SCHED, AUTH→TRUST, PLACE, CONT, CH26, CH29, CH30, ACCESS→RADIO/PKT) |
| Proposed kept pending | **7** (DATA-LIFE, API-OBS, CH21-EVAL, CH22-SENSE, CH25-PAIR, CH27-SIGNAL, CH28-REPRO) |
| Physical-pending surfaces | **6** |

## Scoped fixes applied after ledger

- Corrected CH11 “proposed” mislabel; refreshed CH11/CH18 opportunities to FULL_LAB status for BOOT/RADIO.
- Added portfolio stubs + `A11Y_PRIVACY_SAFETY.md` for thin FULL labs.
- Promoted `LAB-IO-001` to `IMPLEMENTED_DIGITAL`.
- Converted worth-it proposed worksheets to INLINE_ACTIVITY dispositions without new lab directories.
- Clarified CH29/CH30 metadata so proposed IDs are not listed as if `labs/` packages exist.

## FULL_LAB packets

Implemented digital packages: `LAB-SYS-001`, `LAB-TAP-001`, `LAB-PERF-001`, `LAB-QUARTET-001`, `LAB-SIG-001`, `LAB-CMS-001`, `LAB-IO-001`, `LAB-PWR-001`, `LAB-BUS-001`, `LAB-BOOT-OBS-001`, `LAB-PKT-001`, `LAB-RADIO-OBS-001`, `LAB-TRUST-001`, `LAB-CE06-001`.

Pre-fix packet gaps (claimed paths / thin scaffolding): QUARTET, SIG, IO, PWR, BUS, BOOT, RADIO. Strong packets already: SYS, CMS, PKT, TRUST, CE06.

## Proposed dispositions (honest)

**→ inline (do not mint `labs/` dirs):** CPU, MEM, SCHED (inherit CMS); PLACE (CH15 placement via PKT); CONT (CH19 doc-only NTN class); CH26 git worksheet; CH29 one-pager; CH30 portfolio index; AUTH (must not mint — use TRUST).

**→ superseded:** ACCESS-OBS (covered by RADIO-OBS + PKT access labeling).

**→ keep proposed/pending:** DATA-LIFE, API-OBS, CH21-EVAL, CH22-SENSE, CH25-PAIR, CH27-SIGNAL, CH28-REPRO.

## Physical pending (not fabricated)

Quartet EVT measures; calibrated RF; boot attestation/PCR; on-device Quartet AI / wearables; NTN field twins; watt/°C product curves.

## Try It / Build It quality

Across 31 chapters: observe/build prompts, evidence retention, mistaken-inference guards, fixture/fallback routes, and Explorer→Builder/Engineer depth are present. No primary activity is naked “search the web.”

## Scoped fixes after this ledger

1. Correct stale “proposed” labels for implemented BOOT/RADIO.
2. Add missing portfolio stubs + compact a11y/privacy notes for thin FULL labs.
3. Update `LAB_OPPORTUNITIES` dispositions to match this ledger.
4. Clarify CH29/CH30 metadata as INLINE_ACTIVITY (proposed IDs ≠ implemented packages).
5. Promote `LAB-IO-001` to `IMPLEMENTED_DIGITAL` once portfolio stubs exist.
