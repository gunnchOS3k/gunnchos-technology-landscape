# Project Evidence Closure — Agent EVIDENCE-B

**Branch:** `agent/evidence-b-project`  
**Accepted publication main:** `18ec58005529bd16d680ee7419e4dea13150e9c6` (PR #4 merge)  
**Audit date:** 2026-09-03  
**Scope:** Resolve `PROJECT_EVIDENCE_NEEDED` against accepted-main repository truth only.  
**Gate 3:** Not modified (`publication/gates/gate-3/` untouched).

## Audited repository SHAs (current `origin/main`)

| Repository | Branch | Commit SHA |
|---|---|---|
| `gunnchOS3k/gunnchos-technology-landscape` | main | `18ec58005529bd16d680ee7419e4dea13150e9c6` |
| `gunnchOS3k/waike-research-ops` | main | `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` |
| `gunnchOS3k/gunnchos-device-os` | main | `28562a8456207540c205a1c8a6434a491b0a4771` |
| `gunnchOS3k/gunnchos-hardware-industrial-design` | main | `9ee0ef2f688b2c18428bfabc316b23687a02988d` |

## Starting count

- `PROJECT_EVIDENCE_NEEDED` claim statuses in `publication/**/CLAIM_PLAN.yaml`: **16**
- Candidate index CE subset: **7**
- `PHYSICAL_PENDING` claim statuses (unchanged policy for unvalidated physical attributes): **28** starting

## Resolutions

| Claim ID | New status | Evidence (repo @ SHA → path) |
|---|---|---|
| CLM-CH02-001 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `book/chapters/ch02/`, `labs/LAB-TAP-001/`, `figures/source/ch02/` |
| CLM-CH02-004 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `publication/gates/gate-3/REVIEW_SNAPSHOT.yaml` (`OPEN_FOR_REVIEW`), `evidence.yaml`, `checklist.md` (**read-only cite; Gate 3 not edited**) |
| CLM-CH03-005 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `labs/LAB-TAP-001/lab.yaml`, `labs/LAB-TAP-001/README.md` (one run ≠ benchmark) |
| CLM-CH04-001 | SOURCE_IDENTIFIED | hardware @ `9ee0ef2…` → `docs/device-quartet/README.md`, `DIGITAL_MANUFACTURING_READINESS.md`; publication → `devices/quartet.yaml` |
| CLM-CH04-004 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `evidence/ACCEPTED_MAIN_SOURCE_AUDIT.md` (safe: learning without custom hardware purchase); `devices/quartet.yaml`; Wave-1 labs `equipment: []` / no Quartet required |
| CLM-CH19-005 | PHYSICAL_PENDING | waike @ `e97e74f…` → `case_studies/7gc/graham_land/polar_ntn_simulation/` is synthetic teaching fixture with `local_validation_needed.md`; **no physical/field twin validation** |
| CLM-CH21-004 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `labs/LAB-TRUST-001/lab.yaml` (`publication_side: true`, `waike_map_class: adjacent`) |
| CLM-CH27-004 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `labs/LAB-CE06-001/lab.yaml` (`status: FIXTURE_VALIDATED`), `validate_portfolio.py` (forbids Gate 3 human PASS from fixtures) |
| CLM-CH31-001 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `labs/LAB-CE06-001/` (EMIT template/example/rubric/validator/tests; FIXTURE_VALIDATED on accepted main — not Gate 3 PASS) |
| CLM-CE1-010 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `labs/LAB-SYS-001/lab.yaml`, `README.md` (chrome-visible vs content-usable; observation vs inference; not publication benchmarks) |
| CLM-CE3-010 | SOURCE_IDENTIFIED | hardware @ `9ee0ef2…` → `docs/device-quartet/README.md`, `DIGITAL_MANUFACTURING_READINESS.md` (`PHYSICAL_EVT` / `PHYSICAL_PENDING`) |
| CLM-CE3-011 | SOURCE_IDENTIFIED | device-os @ `28562a8…` → `docs/WHAT_IS_REAL_TODAY.md`, `product/CLAIM_BOUNDARY.md`, `beta_gate/beta_gate_status.yaml` (`beta_ready: false`) |
| CLM-CE4-012 | SOURCE_IDENTIFIED | waike @ `e97e74f…` → `curriculum/digital_rc/COMPUTER_NETWORKING/course.json`, `…/labs/lab_datapath/README.md` |
| CLM-CE5-009 | SOURCE_IDENTIFIED | publication @ `18ec580…` → `labs/LAB-TRUST-001/`; waike catalog/digital_rc have **no** `LAB-TRUST-001` module ID |
| CLM-CE06-009 | SOURCE_IDENTIFIED | waike @ `e97e74f…` → `curriculum/catalog.yaml` + `curriculum/digital_rc/`; no EMIT / Stability Contract / TECHNOLOGY_LANDSCAPE_CAPSTONE module ID |
| CLM-CE06-010 | SOURCE_IDENTIFIED | waike @ `e97e74f…` → `ACCESSIBILITY_AND_LOW_COST.md` (phone-first/offline/low-cost principles; checklist items unchecked) |

## Remaining `PROJECT_EVIDENCE_NEEDED`

None in `CLAIM_PLAN.yaml` after this pass (0).

## PHYSICAL_PENDING note

Device Quartet unvalidated physical attributes remain `PHYSICAL_PENDING` (including CLM-CH19-005 after reclassification). No invented physical measurements. Starting PHYSICAL_PENDING count **28**; after this pass **29** (+CLM-CH19-005).

## Gaps explicitly accepted

- No field-validated NTN twin/demo; only synthetic WAIKE case-study fixtures.
- Hardware EVT / fabrication / certification remain `PHYSICAL_PENDING`.
- Gate 3 reader evidence still pending (`OPEN_FOR_REVIEW`); citing Gate 3 files does not change them.
