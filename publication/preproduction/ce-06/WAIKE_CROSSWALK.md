# CE-6 WAIKE Crosswalk (evidence-backed)

**Publication object:** CE-6 / `LAB-CE06-001`  
**WAIKE repository:** `gunnchOS3k/waike-research-ops`  
**Accepted-main SHA audited for this package:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Audit date:** 2026-09-03 (America/Chicago session; user_info day 2026-09-02 environment)  
**Method:** GitHub API listing of `curriculum/catalog.yaml`, `curriculum/digital_rc/*`, selected lab paths, `ACCESSIBILITY_AND_LOW_COST.md`, `capstones/*`  
**Rule:** No invented WAIKE module/course IDs. Relationship must be `exact` | `adjacent` | `proposed` | `no-map`.

**Note on prior SHA:** Publication CH02 materials cite `8eb2827dc58ffa391842da1bfb1ee665c25a31a7`. CE-6 remaps against the newer accepted main above. Dual ID systems remain: catalog `snake_case` (18 courses) and digital_rc `SCREAMING_SNAKE` (16 packages verified at this SHA).

---

## Explicit non-mappings (no-map)

| Book object | Invented ID rejected | Status | Evidence |
|---|---|---|---|
| Stability Contract teaching model | any `STABILITY_CONTRACT` course/lab ID | **no-map** | No matching path/name in tree at audited SHA |
| Explain–Measure–Improve–Teach capstone | any `EMIT` / `TECHNOLOGY_LANDSCAPE_CAPSTONE` module ID | **no-map** | No such digital_rc course; publication-owned lab |
| `LAB-CE06-001` | treating it as upstream WAIKE lab | **no-map** | Lab ID is publication-owned |

---

## Exact alignments

None.

There is **no** exact WAIKE course or lab whose ID and scope equal CE-6’s Stability Contract formal model or EMIT ecosystem capstone.

---

## Adjacent alignments (competency neighbors)

| Book object | WAIKE ID (exact existing) | ID system | Relationship | Competency link | Evidence path (at SHA) |
|---|---|---|---|---|---|
| CE-6 diagnosis / reliability thinking | `CLOUD_DEVOPS` / `lab_slo_budget` | digital_rc | **adjacent** | SLO/error-budget literacy as analogy for “good enough” bounds | `curriculum/digital_rc/CLOUD_DEVOPS/labs/lab_slo_budget/` |
| CE-6 cross-layer incident style triage | `CLOUD_DEVOPS` / `lab_incident_runbook` | digital_rc | **adjacent** | Incident runbook structure | `curriculum/digital_rc/CLOUD_DEVOPS/labs/lab_incident_runbook/` |
| CE-6 teach-back / professional communication | `COMM_PD_ETHICS` / `lab_pd_capstone` | digital_rc | **adjacent** | Capstone communication artifact pattern | `curriculum/digital_rc/COMM_PD_ETHICS/labs/lab_pd_capstone/` |
| CE-6 rubric / feedback practice | `COMM_PD_ETHICS` / `lab_feedback_rubric` | digital_rc | **adjacent** | Rubric feedback lab | `curriculum/digital_rc/COMM_PD_ETHICS/labs/lab_feedback_rubric/` |
| CE-6 accessibility communication | `COMM_PD_ETHICS` / `lab_accessibility_comm` | digital_rc | **adjacent** | Accessibility communication competency | `curriculum/digital_rc/COMM_PD_ETHICS/labs/lab_accessibility_comm/` |
| CE-6 network-path branch of diagnosis | `COMPUTER_NETWORKING` / `lab_datapath` | digital_rc | **adjacent** | Datapath tracing adjacency (also used by CH02) | `curriculum/digital_rc/COMPUTER_NETWORKING/labs/lab_datapath/` |
| CE-6 latency-budget thinking | `EMBEDDED_PROTOTYPING` / `lab_ep_isr_vs_poll` | digital_rc | **adjacent** | Fixture latency-budget adjacency | `curriculum/digital_rc/EMBEDDED_PROTOTYPING/labs/lab_ep_isr_vs_poll/` |
| CE-6 builder instrumentation | `SOFTWARE_BUILDER` | digital_rc | **adjacent** | Builder/event instrumentation adjacency | `curriculum/digital_rc/SOFTWARE_BUILDER/` |
| CE-6 input-path symptoms | `GAME_DEV_INTERACTIVE` / `lab_input_actions` | digital_rc | **adjacent** | Input-action competency neighbor | Present in prior CH02 audit; package remains in digital_rc set at new SHA |
| CE-6 evidence / dashboard debugging analogy | `DATA_DASHBOARDS` / `lab_debug_pipeline`, `lab_freshness_sla` | digital_rc | **adjacent** | Pipeline debug + freshness/SLA analogies | `curriculum/digital_rc/DATA_DASHBOARDS/labs/` |
| CE-6 operator triage habits | `GENERAL_IT` / `lab_ticket_queue`, `lab_services` | digital_rc | **adjacent** | Service/ticket operational hygiene | `curriculum/digital_rc/GENERAL_IT/labs/` |
| CE-6 security evidence discipline | `CYBERSECURITY` / `lab_incident_playbook`, `lab_forensics_timeline` | digital_rc | **adjacent** | Timeline/playbook discipline — **not** offensive labs | `curriculum/digital_rc/CYBERSECURITY/labs/` |
| CE-6 portfolio / site capstone culture | `capstones/` + catalog `reproducible_research` | capstones + catalog | **adjacent** | Capstone culture & reproducible research track exist; not EMIT-equivalent | `capstones/`, catalog course_id `reproducible_research` |
| CE-6 phone-first equity intent | WAIKE accessibility principles | docs | **adjacent** | Phone-first, offline-friendly, low-cost intent; checklist incomplete | `ACCESSIBILITY_AND_LOW_COST.md` |

Catalog snake_case neighbors (same courses, alternate ID system): `cloud_devops`, `communication_ethics_professional_dev`, `networking`, `edge_ai_embedded`, `software_engineering`, `game_development_interactive_media`, `data_visualization_bi`, `general_it`, `cybersecurity`, `reproducible_research`.

---

## Proposed future alignments (not present today)

| Proposal | Status | Notes |
|---|---|---|
| Optional WAIKE digital_rc lab explicitly practicing “connected vs usable” with fixture traces | **proposed** | Would still remain distinct from publication `LAB-CE06-001` unless formally adopted |
| Shared rubric fields bridging WAIKE `capstone_readiness_rubric` and EMIT dimensions | **proposed** | Current `capstones/capstone_readiness_rubric.md` is a stub pointing at `rubrics/master_rubric.yaml` — do not overclaim content |
| Joint portfolio validator rejecting bare `PASS` for CE-6 artifacts | **proposed** | Matches WAIKE validator ethos; not implemented in this publication package |

---

## Mapping summary counts

| Relationship | Count |
|---|---:|
| exact | 0 |
| adjacent | 14 rows (table above) |
| proposed | 3 |
| no-map (explicit) | 3 |

---

## Integrator handoff

- Do **not** edit shared `waike/alignment.yaml` from this agent.  
- Promote only after verifying SHA still matches accepted main.  
- Keep `LAB-CE06-001` publication-owned in any merged crosswalk.
