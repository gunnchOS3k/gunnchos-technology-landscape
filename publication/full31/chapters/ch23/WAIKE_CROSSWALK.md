# CH23 — WAIKE Crosswalk

**Book object:** CH23 — Cybersecurity from Chip to Cloud  
**WAIKE repository:** `gunnchOS3k/waike-research-ops`  
**Audited SHA:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Map classes:** `exact` | `adjacent` | `proposed` | `no-map`  
**Rule:** Do not invent course/lab IDs. Dual ID systems (catalog `snake_case` vs digital_rc `SCREAMING_SNAKE`) are related but not interchangeable.

## Exact

_None. No exact WAIKE module equals this chapter._


## Adjacent

| WAIKE ID | ID system | Notes |
|---|---|---|
| `CYBERSECURITY` | digital_rc | Harbor SOC foundations |
| `lab_iam_rbac` | digital_rc lab | identity lifecycle / RBAC |
| `lab_incident_playbook` | digital_rc lab | detect→contain→recover |
| `lab_authz` | digital_rc lab under SOFTWARE_BUILDER | authz matrix |
| `lab_iam_secrets` | digital_rc lab under CLOUD_DEVOPS | secrets hygiene |
| `cybersecurity` | catalog | program-track pointer |


## Proposed

| Proposal | Notes |
|---|---|
| Optional joint fixture for UX-linked auth failure without offensive content |  |


## No-map

- No WAIKE module ID CH23 / LAB-TRUST-001
- Do not map offensive/exploit labs into book activities


## Counts (this chapter)

| Class | Count |
|---|---:|
| exact | 0 |
| adjacent | 6 |
| proposed | 1 |
| no-map | 2 |

## Integrator handoff

- Do not edit shared `waike/alignment.yaml` from this agent  
- Preserve SHA continuity note if shared registry still cites older CH02 SHA `8eb2827…`
