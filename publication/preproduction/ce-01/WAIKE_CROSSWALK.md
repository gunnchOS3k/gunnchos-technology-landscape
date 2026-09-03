# CE-1 WAIKE Crosswalk

**Chapter:** CE-1 / CH01 — Technology Is a System, Not a Screen  
**Audit target:** `gunnchOS3k/waike-research-ops` accepted `main`  
**WAIKE SHA used:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Verification:** `git ls-remote origin refs/heads/main` and local clone HEAD agreed on this SHA during CE-1 preproduction.  
**Rule:** Evidence-backed adjacency only. **No invented module/course IDs.**  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Mapping status vocabulary

| Status | Meaning |
|---|---|
| `exact` | A WAIKE course/lab literally teaches this CE-1 outcome under a matching ID/title |
| `adjacent` | Existing WAIKE artifacts teach a closely related competency usable for CE-1 |
| `proposed` | Useful future alignment; **not** present as a named module today |
| `no-map` | No responsible mapping without invention |

## Explicit non-mapping

- There is **no** WAIKE `course_id` or lab ID named `CE-1`, `CH01`, or “Technology Is a System, Not a Screen” on accepted main.  
- Therefore **exact alignment = none** for the chapter as a whole.

## Evidence-backed adjacency

| CE-1 concept / lab need | WAIKE ID (real) | Alignment | Evidence on accepted main | Notes |
|---|---|---|---|---|
| Observation vs inference; machine as remember/calculate/talk | `GENERAL_IT` week 1 / `lab_ticket_queue` | `adjacent` | `curriculum/digital_rc/GENERAL_IT/course.json` | Strong pedagogical adjacency for system lens + triage honesty |
| Operator triage / failure naming | `GENERAL_IT` weeks 5–6 / `lab_ticket_queue`, hardware triage lessons | `adjacent` | same package | Do not rename WAIKE labs into LAB-SYS-001 |
| Layered hardware failure diagnosis | `HARDWARE_ENGINEERING` / `lab_failure_diagnosis` | `adjacent` | `curriculum/digital_rc/HARDWARE_ENGINEERING/labs/` | Hardware-leaning; use carefully so CE-1 stays experience-first |
| Software as composed systems; observability | `SOFTWARE_BUILDER` / `lab_observability`, `lab_frontend_ui` | `adjacent` | `curriculum/digital_rc/SOFTWARE_BUILDER/labs/` | Adjacent to “app is not one thing,” not a readiness lab clone |
| Optional network path literacy | `COMPUTER_NETWORKING` / `lab_datapath` | `adjacent` | `curriculum/digital_rc/COMPUTER_NETWORKING/labs/` | Foreshadow CE-4; do not expand CE-1 into packet deep-dive |
| Accessibility communication | `COMM_PD_ETHICS` / `lab_accessibility_comm` | `adjacent` | `curriculum/digital_rc/COMM_PD_ETHICS/labs/` | Supports inclusive “ready/busy” communication |
| Interactive system state / loops | `GAME_DEV_INTERACTIVE` / `lab_game_loop`, `lab_entity_fsm` | `adjacent` | `curriculum/digital_rc/GAME_DEV_INTERACTIVE/labs/` | Light adjacency only; avoid turning CE-1 into game-dev |
| Product/system composition language | `GUNNCHOS_PRODUCT_LAB` / `lab_gpl_product_charter` | `adjacent` | `curriculum/digital_rc/GUNNCHOS_PRODUCT_LAB/labs/` | Optional later; not required for CE-1 baseline |
| Phone-first / low-cost / offline-first principles | repo root `ACCESSIBILITY_AND_LOW_COST.md` | `adjacent` | file present on accepted main | Design principles; checklist items may remain unchecked |
| Literal CE-1 course module | — | `no-map` | catalog + digital_rc inventory | Do not invent |
| Device Quartet physical lab modules in WAIKE | — | `no-map` | Quartet lives in hardware industrial-design repo | Cross-repo foreshadow only |
| LAB-SYS-001 identical WAIKE lab | — | `proposed` | — | Future: contribute readiness observation fixture without claiming it exists now |

## Catalog dual-ID reminder

WAIKE maintains dual ID systems on accepted main (snake_case catalog courses and `digital_rc` SCREAMING_SNAKE packages). This crosswalk uses **digital_rc `course_id` values that exist on disk**. Catalog aliases such as `general_it` / `software_engineering` are related naming systems—not additional invented modules.

## Safe wording for manuscript later

> CE-1 aligns adjacently with WAIKE `GENERAL_IT` observation/inference and ticket-triage practice, and can point learners toward related `SOFTWARE_BUILDER` and `COMPUTER_NETWORKING` competencies. WAIKE accepted main (`e97e74f…`) does not host a module literally titled Technology Is a System, Not a Screen.

## Integrator handoff

- Reconcile shared `waike/alignment.yaml` (currently CH02-focused; older SHA `8eb2827…`) with this newer SHA if still accurate at integration time.  
- Chapter agent does **not** edit shared WAIKE alignment files.
