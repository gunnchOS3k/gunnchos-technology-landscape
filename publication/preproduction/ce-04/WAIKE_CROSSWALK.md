# CE-4 WAIKE Crosswalk (evidence-based)

**Publication module:** CE-4 — Packets, Wi-Fi/Cellular, Edge and Cloud  
**Publication lab (owned here):** `LAB-PKT-001`  
**WAIKE repository:** `gunnchOS3k/waike-research-ops`  
**Branch:** `main`  
**Accepted-main SHA used for this audit:** `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
**Audited:** 2026-09-02  

**Rule:** Exact course/lab IDs only as they exist on accepted main. No invented WAIKE module IDs.  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

### SHA relationship note

Publication Wave-1 audit previously recorded WAIKE SHA `8eb2827dc58ffa391842da1bfb1ee665c25a31a7`. That commit is an **ancestor** of current `main`. CE-4 uses the **newer** accepted-main SHA above. Core digital_rc IDs cited below (`COMPUTER_NETWORKING`, `WIRELESS_6G`, `CLOUD_DEVOPS`, `GENERAL_IT`) were confirmed present at this SHA.

---

## Mapping status legend

| Status | Meaning |
|---|---|
| **exact** | Same competency object exists and can be cited by ID for the book object |
| **adjacent** | Related course/lab exists; useful competency neighbor; not the same lab/module |
| **proposed** | Future alignment idea; **not** present as an ID on accepted main |
| **no-map** | No honest mapping; do not invent |

---

## Book object → WAIKE map

| Book object | WAIKE ID | ID system | Relationship | Status | Notes |
|---|---|---|---|---|---|
| CE-4 chapter themes (packets, path) | `COMPUTER_NETWORKING` | digital_rc | Course-level networking path | **adjacent** | Title on disk: “Computer Networking — Packets to Campus Edge” |
| CE-4 / LAB-PKT-001 datapath reasoning | `lab_datapath` | digital_rc lab under `COMPUTER_NETWORKING` | Crafted Ethernet+IPv4 parse / LPM / TTL | **adjacent** | Strongest packet-path neighbor; LAB-PKT-001 remains publication-owned |
| CE-4 addressing (CIDR intuition) | `lab_cidr_math` | digital_rc lab | Addressing math fixture | **adjacent** | Optional Builder stretch pointer |
| CE-4 routing story | `lab_spf_routing` | digital_rc lab | SPF on fixture topology | **adjacent** | Not required for Explorer baseline |
| CE-4 DNS dependency | `lab_dns_resolution` | digital_rc lab (`COMPUTER_NETWORKING`) | DNS/NAT service story | **adjacent** | |
| CE-4 DNS on LAN (operator desk) | `lab_dns_hosts` | digital_rc lab (`GENERAL_IT`) | Hosts/LAN naming | **adjacent** | Good Operator/Support adjacency |
| CE-4 catalog networking track label | `networking` | catalog `course_id` | Catalog snake_case twin of networking track | **adjacent** | Dual ID systems; do not collapse with digital_rc ID |
| CE-4 Wi-Fi ≠ cellular survey | `WIRELESS_6G` | digital_rc | Advanced radio track | **adjacent** | Use sparingly; avoid turning CE-4 into 6G course |
| CE-4 qualitative radio conditions | `lab_fspl_budget` | digital_rc lab | Free-space path loss fixture | **adjacent** | Conceptual radio budget only |
| CE-4 delay/spread intuition (optional) | `lab_delay_spread` | digital_rc lab | Channel tap / delay-spread toy | **adjacent** | “Tap” ≠ UI tap; keep CH02 distinction |
| CE-4 edge/cloud placement | `CLOUD_DEVOPS` | digital_rc | Cloud primitives / ops | **adjacent** | Placement & reliability neighbors |
| CE-4 costed cloud blocks | `lab_cloud_cost` | digital_rc lab | Compute/storage/network as costed blocks | **adjacent** | |
| CE-4 reliability/error-budget intuition | `lab_slo_budget` | digital_rc lab | Observability / error budgets | **adjacent** | Forward link to CE-6 |
| CE-4 catalog cloud track | `cloud_devops` | catalog `course_id` | Catalog twin | **adjacent** | |
| CE-4 catalog wireless track | `wireless_dsp_6g` | catalog `course_id` | Catalog twin for wireless | **adjacent** | Name is 6G-oriented; CE-4 must not over-claim |
| LAB-PKT-001 as WAIKE module ID | — | — | No course/lab named LAB-PKT-001 | **no-map** | Explicit non-mapping |
| CE-4 “official Wi-Fi certification module” | — | — | Not present | **no-map** | |
| CE-4 commercial 6G field lab | — | — | Not present / non-claim in WAIKE culture | **no-map** | |
| Future shared “connectivity continuity” micro-lab across CE-4/CE-6 | — | — | Idea only | **proposed** | Integrator may propose; do not mint ID now |

---

## Exact alignments

**None** for LAB-PKT-001. There is no WAIKE course or lab ID that *is* LAB-PKT-001.

Course/lab IDs listed above are **real** on accepted main; their relationship to CE-4 objects is competency **adjacency**, not identity. Treat “exact” only if a future integrator intentionally adopts a WAIKE lab as the chapter lab without renaming fictionally—**not done here**.

---

## Explicit non-mappings

1. Do not invent `LAB-PKT-001` inside WAIKE.  
2. Do not rename `lab_datapath` to “Trace One Tap” or “CE-4 lab.”  
3. Do not claim CE-4 completion equals CCNA or cloud certification (WAIKE `COMPUTER_NETWORKING` itself states CCNA is not granted).  
4. Do not treat `WIRELESS_6G` as required CE-4 core curriculum.

---

## Portfolio evidence link (proposed)

| Publication artifact | WAIKE portfolio adjacency |
|---|---|
| LAB-PKT-001 path diagram + timing table | Similar evidence hygiene to `COMPUTER_NETWORKING` datapath JSON artifacts (validator rejects empty/`PASS`) |
| Teach-back: Wi-Fi≠Internet≠cellular≠cloud | Educator pathway; no WAIKE quiz ID claimed |

---

## Integrator checklist

- [ ] Confirm SHA still current at merge time (`git rev-parse origin/main` on waike-research-ops)  
- [ ] Keep dual catalog vs digital_rc IDs distinct in shared crosswalk  
- [ ] Prevent glossary collision on “tap” (UI tap vs channel tap)
