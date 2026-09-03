# CE-5 WAIKE Crosswalk (evidence-based)

**Book object:** CE-5 — AI, Security, Privacy and Trust  
**Proposed publication lab:** `LAB-TRUST-001` (not a WAIKE ID)  
**WAIKE repository:** `gunnchOS3k/waike-research-ops`  
**Branch:** `main`  
**Audited SHA:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Audited at:** 2026-09-02  
**Method:** `gh api` inspection of `curriculum/catalog.yaml`, `curriculum/digital_rc/*/course.json`, and lab paths under the tree at that SHA  

**Map classes used:** `exact` | `adjacent` | `proposed` | `no-map`

---

## Dual ID systems (do not collapse)

| System | Examples relevant to CE-5 |
|---|---|
| Catalog (`course_id` snake_case) | `ai_ml_data`, `cybersecurity`, `communication_ethics_professional_dev`, `cloud_devops`, `edge_ai_embedded` |
| digital_rc (`course_id` SCREAMING_SNAKE) | `AI_ML_EDGE`, `CYBERSECURITY`, `COMM_PD_ETHICS`, `CLOUD_DEVOPS`, `SOFTWARE_BUILDER`, `EMBEDDED_PROTOTYPING` |

---

## Crosswalk table

| Book object | WAIKE ID | ID system | Relationship | Map class | Competency link | Notes |
|---|---|---|---|---|---|---|
| CE-5 / LAB-TRUST-001 | `AI_ML_EDGE` | digital_rc | Course package hosts inference, edge budget, RAG privacy labs | adjacent | data→model→score; local/edge budget; redaction | Exact labs below |
| CE-5 inference path | `lab_score_model` | digital_rc lab under `AI_ML_EDGE` | Deploy/inference scoring adjacency | adjacent | inference output as scored artifact | Path: `curriculum/digital_rc/AI_ML_EDGE/labs/lab_score_model/` |
| CE-5 local vs cloud | `lab_quantize_budget` | digital_rc lab under `AI_ML_EDGE` | Edge latency/budget tradeoff adjacency | adjacent | on-device/edge constraints | Not a measured gunnchOS benchmark |
| CE-5 privacy in generative retrieval | `lab_rag_redact` | digital_rc lab under `AI_ML_EDGE` | Retrieve without leaking patrons | adjacent | redaction / responsible retrieval | Strong privacy teaching adjacency |
| CE-5 identity/authz | `CYBERSECURITY` | digital_rc | Harbor SOC foundations | adjacent | IAM/RBAC, hardening, incident | |
| CE-5 authn/authz UX | `lab_iam_rbac` | digital_rc lab under `CYBERSECURITY` | Identity lifecycle / RBAC | adjacent | human vs bot privileges | |
| CE-5 trust restore | `lab_incident_playbook` | digital_rc lab under `CYBERSECURITY` | Detect→contain→recover narrative | adjacent | restore usable trust after incident | Keep UX-linked; no scare dump |
| CE-5 consent/privacy | `COMM_PD_ETHICS` | digital_rc | Harbor Desk Voice ethics/PD | adjacent | consent, disclosure, ethics ladder | |
| CE-5 consent card | `lab_consent_disclosure` | digital_rc lab under `COMM_PD_ETHICS` | Audience/purpose/classes/retention/opt-out | adjacent | consent card fields | |
| CE-5 responsible AI use | `lab_ai_disclosure_modes` | digital_rc lab under `COMM_PD_ETHICS` | AI disclosure modes | adjacent | disclosure without key leakage | |
| CE-5 observation vs inference | `lab_ethics_ladder` | digital_rc lab under `COMM_PD_ETHICS` | Observation before inference | adjacent | evidence language | |
| CE-5 builder authz | `lab_authz` | digital_rc lab under `SOFTWARE_BUILDER` | Authz matrix desk/reader/bot | adjacent | authorization ≠ authentication | |
| CE-5 secrets/least privilege | `lab_iam_secrets` | digital_rc lab under `CLOUD_DEVOPS` | IAM + secrets hygiene | adjacent | least privilege for cloud AI deps | |
| CE-5 catalog AI track | `ai_ml_data` | catalog | Catalog title “AI, ML, and Data Foundations” | adjacent | program-track pointer | Not identical to `AI_ML_EDGE` package |
| CE-5 catalog cyber track | `cybersecurity` | catalog | Catalog title “Cybersecurity Foundations and SOC Readiness” | adjacent | program-track pointer | Pair with digital_rc `CYBERSECURITY` |
| CE-5 catalog ethics track | `communication_ethics_professional_dev` | catalog | Catalog ethics/PD course | adjacent | program-track pointer | Pair with `COMM_PD_ETHICS` |
| LAB-TRUST-001 as WAIKE module | — | — | No course/lab ID with this name on accepted main | no-map | — | **Do not invent** |
| Exact CE-5 chapter module in WAIKE | — | — | No WAIKE module ID `CE-5` / `CE5` found in audited digital_rc listing | no-map | — | Book-side ID only |
| Future integrated lab packaging | `LAB-TRUST-001` ↔ WAIKE export | — | Publication may later package fixtures that call WAIKE validators | proposed | shared evidence format | Requires integrator + WAIKE owners |

---

## Explicit non-mappings

1. No WAIKE course or lab ID named `LAB-TRUST-001`, `CE-5`, `Trace Trust`, or `Compare Local Remote AI` exists on audited accepted main.  
2. `WIRELESS_6G` / AI-RAN research courses are **not** mapped into CE-5 baseline claims (out of Concept Edition scope for this package).  
3. Catalog snake_case IDs and digital_rc SCREAMING_SNAKE IDs are related but **not** interchangeable exact IDs.

---

## Portfolio evidence (planned)

| Learner artifact | WAIKE adjacency |
|---|---|
| Comparison table (local vs remote) | `AI_ML_EDGE` inference/edge labs |
| Consent/trust card | `COMM_PD_ETHICS` `lab_consent_disclosure` |
| Authn/authz decision card | `CYBERSECURITY` `lab_iam_rbac` / `SOFTWARE_BUILDER` `lab_authz` |
| Dual-ledger trust note | ethics ladder + incident restore narrative |

---

## SHA continuity note

Chapter 2 publication audit previously recorded WAIKE SHA `8eb2827dc58ffa391842da1bfb1ee665c25a31a7`.  
CE-5 re-audited `main` at `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` (includes PR #56 taxonomy contract merge). Shared `evidence/source_registry.yaml` was **not** modified by Agent D.
