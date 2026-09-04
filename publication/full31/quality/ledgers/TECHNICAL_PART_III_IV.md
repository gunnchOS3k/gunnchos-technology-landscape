# Technical review — Parts III–IV (CH11–CH20)

**Agent:** B · **Branch:** `agent/quality-b-part34`  
**Base:** `cursor/full31-quality-convergence-001` @ `76bee2e67c35ff445f46c83af30809e5b307f06e`  
**Ledger:** `TECHNICAL_PART_III_IV.yaml`  
**Gate 3:** unchanged

## Verdict

Parts III–IV are generally careful on the hard disambiguations (secure boot ≠ lock screen; process ≠ thread; concurrency ≠ parallelism; VM ≠ container; placement ≠ access radio; Wi-Fi ≠ cellular ≠ Internet; 6G = roadmap; latency ≠ reliability ≠ QoE). No BLOCKERs. Phase 2 closes **7 MAJORs**.

## Severity (before → after)

| Severity | Before | After (open) |
|---|---:|---:|
| BLOCKER | 0 | 0 |
| MAJOR | 7 | 0 |
| MODERATE | 6 | 6 (mostly deferred SOURCE_NEEDED) |
| MINOR | 3 | 3 |
| EDITORIAL | 2 | 2 |

## MAJOR fixes applied

1. **CH12** — Replace opaque “blocked CMS measured plate” wording with clear LAB-CMS-001 fixture language (no banned figure ID).
2. **CH19** — Drop wrong `@tanenbaum-bos` cite on orbit delay regimes; keep SOURCE_NEEDED honesty / Part IV networking cite where appropriate.
3. **CH18** — Crisp spectrum vs channel + SISO baseline beside MIMO.
4. **CH16** — Name Ethernet under LAN vs Internet scopes.
5. **CH11/CH13/CH14/CH17–CH20** — Correct false `draft-blocked` figure status and embed registered `figures/full31/...` SVGs at first teaching mentions.

## Deferred

- DB textbook pin (CH13), 6G/IMT-2030 primary (CH17), NTN delay/capability docs (CH19), Quartet PHYSICAL_PENDING items — Agent E / human evidence.
- Routing vs forwarding polish, orchestration depth, Gate banner consistency, registry `CH1-` typo — MODERATE/MINOR.

## Gate 3

`publication/gates/gate-3/` not modified.
