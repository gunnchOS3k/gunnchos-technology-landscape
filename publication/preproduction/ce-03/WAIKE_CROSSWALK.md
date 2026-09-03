# CE-3 WAIKE Crosswalk

**Publication module:** CE-3 — CPU, Memory, Storage, and the OS  
**Publication-owned lab proposal:** `LAB-CMS-001` (Make Local Slowness Visible)  
**Audit date:** 2026-09-02  

## Accepted-main WAIKE SHA

`e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
Repository: `gunnchOS3k/waike-research-ops` · branch `main`

**Note:** This SHA is newer than the Chapter 2 publication audit tip (`8eb2827dc58ffa391842da1bfb1ee665c25a31a7`). CE-3 mappings below were checked against the newer tip. Do not invent course/module IDs absent from catalog/digital_rc.

---

## Mapping classes used

| Class | Meaning |
|---|---|
| `exact` | Same competency object / lab ID exists for this chapter’s lab |
| `adjacent` | Existing course/lab teaches a neighboring competency |
| `proposed` | Future alignment idea—not present on accepted main |
| `no-map` | No responsible mapping without invention |

---

## Results

| Book object | WAIKE ID (exact string on accepted main) | ID system | Class | Relationship / evidence |
|---|---|---|---|---|
| CE-3 / LAB-CMS-001 | — | — | **no-map** (exact) | No digital_rc or catalog course/lab titled for “local lag,” “CMS,” or LAB-CMS-001. |
| CE-3 memory hierarchy teaching | `EMBEDDED_PROTOTYPING` / `lab_ep_memory_map` | digital_rc lab | **adjacent** | Week 1 title: “MCU memory map — flash vs SRAM before first boot.” Neighbor for volatile vs durable intuition—not identical to AP RAM vs SSD story. |
| CE-3 scheduling / latency budgets | `EMBEDDED_PROTOTYPING` / `lab_ep_isr_vs_poll` | digital_rc lab | **adjacent** | ISR vs polling latency-budget fixture; adjacent to “who runs when,” not a desktop scheduler lab. |
| CE-3 power/sleep adjacency | `EMBEDDED_PROTOTYPING` / `lab_ep_sleep_mode` | digital_rc lab | **adjacent** | Sleep/power mode lab exists in package listing; useful neighbor for power limits—do not equate to laptop thermal curves. |
| CE-3 storage / triage | `GENERAL_IT` / `lab_storage` | digital_rc lab | **adjacent** | Week 6: “Hardware triage — power, then storage, then memory, then OS.” Strong Operator adjacency. |
| CE-3 OS users / multi-OS literacy | `GENERAL_IT` / `lab_os_users` | digital_rc lab | **adjacent** | OS user/admin literacy; not process-scheduler depth. |
| CE-3 backup / persistence culture | `GENERAL_IT` / `lab_backup` | digital_rc lab | **adjacent** | Persistence/ops neighbor for Experience B themes. |
| CE-3 power budget (hardware) | `HARDWARE_ENGINEERING` / `lab_power_budget` | digital_rc lab | **adjacent** | Power budget with real MPNs—hardware-energy neighbor; not CE-3 required equipment. |
| CE-3 QEMU/OS bring-up adjacency | `HARDWARE_ENGINEERING` / `lab_zephyr_qemu` · `EMBEDDED_PROTOTYPING` / `lab_ep_zephyr_qemu` | digital_rc lab | **adjacent** | Digital boot before hardware; adjacent OS/runtime exposure—not commodity Task Manager lab. |
| CE-3 observability adjacency | `SOFTWARE_BUILDER` / `lab_observability` | digital_rc lab | **adjacent** | Observability practices; competency neighbor for Engineer pathway evidence habits. |
| CE-3 catalog track pointers | `hardware_engineering`, `software_engineering`, `general_it`, `edge_ai_embedded` | catalog `course_id` | **adjacent** | Catalog snake_case IDs coexist with digital_rc SCREAMING_SNAKE packages (dual ID systems on accepted main). |
| CE-3 × gunnchOS product lab | `GUNNCHOS_PRODUCT_LAB` | digital_rc | **adjacent** (weak) | Product-lab course exists; does **not** substitute for commodity OS internals teaching. Use sparingly. |
| Exact CE-3 desktop OS internals course | — | — | **proposed** | Future WAIKE module could align to LAB-CMS-001 competencies; **not present** now—do not mint IDs. |

---

## Explicit non-mapping statement

There is **no** WAIKE course module ID on accepted main named `LAB-CMS-001`, `Make Local Slowness Visible`, `CE-3`, or equivalent. Publication must keep LAB-CMS-001 publication-owned and cite only the adjacent IDs above.

---

## Dual ID reminder (ops honesty)

WAIKE maintains dual curriculum ID systems on accepted main (catalog snake_case and digital_rc SCREAMING_SNAKE). Crosswalk entries above prefer **digital_rc** lab IDs when citing runnable lab adjacency, and mention catalog IDs only as track pointers.

---

## Integrator handoff

- Record SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` in any shared WAIKE alignment update.  
- Do not overwrite CH02 mappings; append CE-3 adjacency rows only.  
- Reject any PR that invents a tap- or CMS-named WAIKE module ID.
