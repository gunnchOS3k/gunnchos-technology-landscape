# CE-6 Source Register (chapter-local)

**Chapter:** CE-6  
**Purpose:** Proposed sources for later drafting. **Not** merged into the global bibliography until integration validation.  
**Verification rule:** No invented DOI/ISBN/page numbers/years/revision status. Living standards marked as living.

**Audited project SHAs (this package):**

| Source | Repository | Branch | SHA | Role |
|---|---|---|---|---|
| Publication accepted main | `gunnchOS3k/gunnchos-technology-landscape` | `main` | `166e9544bc6e2aee344bc962ace76d49ee3e04e4` | Contains merged PR #2 |
| WAIKE (SRC-WAIKE) | `gunnchOS3k/waike-research-ops` | `main` | `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` | Curriculum adjacency audit |
| Prior publication audit note | same WAIKE repo | `main` | `8eb2827dc58ffa391842da1bfb1ee665c25a31a7` | Earlier CH02 audit SHA (superseded for CE-6 mapping) |

---

## Counts by source class

| Class | Count | IDs |
|---|---:|---|
| Standards / specifications | 4 | SRC-CE06-01 … 04 |
| Official technical documentation | 3 | SRC-CE06-05 … 07 |
| Peer-reviewed literature | 0 | — |
| Respected technical textbooks | 1 | SRC-CE06-08 |
| High-quality explanatory | 1 | SRC-CE06-09 |
| Project / accepted-main evidence | 3 | SRC-CE06-10 … 12 |
| Publication-internal pedagogy | 2 | SRC-CE06-13 … 14 |
| **Total verified entries** | **14** | |

Peer-reviewed QoE empirical papers are **deferred** (SOURCE_NEEDED for later full-book CH20 depth) rather than invented.

---

## Standards / specifications

### SRC-CE06-01 — ITU-T P.10/G.100
- **Title:** Vocabulary for performance, quality of service and quality of experience  
- **Type:** ITU-T Recommendation (living recommendation family; cite in-force text)  
- **URL:** https://www.itu.int/rec/T-REC-P.10/en  
- **Verified use:** QoE / QoS vocabulary distinction  
- **Do not:** invent page numbers; claim the book’s “Stability Contract” phrase is ITU terminology  

### SRC-CE06-02 — ITU-T G.1011 (07/2016)
- **Title:** Reference guide to quality of experience assessment methodologies  
- **Status verified:** In force (07/2016) per ITU recommendation page  
- **URL:** https://www.itu.int/rec/T-REC-G.1011  
- **Verified use:** Evidence hierarchy context (subjective vs objective estimation)  
- **Do not:** imply CE labs are formal G.1011 campaigns  

### SRC-CE06-03 — WCAG 2.2 (2024-12-12 Recommendation)
- **Citation key:** `wcag22-20241212`
- **Title:** Web Content Accessibility Guidelines (WCAG) 2.2  
- **Status:** W3C Recommendation 12 December 2024  
- **URL:** https://www.w3.org/TR/2024/REC-WCAG22-20241212/  
- **Note:** Distinct from CE-1 `wcag22-20231005` (5 October 2023). Undated shortcut `/TR/WCAG22/` currently resolves to this 2024 edition.  
- **Verified use:** Accessibility intent; non-certification framing  

### SRC-CE06-04 — WHATWG HTML (Living Standard) — event loop / scripting context
- **URL:** https://html.spec.whatwg.org/  
- **Verified use:** Reinforce that UI responsiveness depends on event-loop/scheduling conditions (synthesis with CE-2/CE-3)  
- **Mark:** Living Standard  

---

## Official technical documentation

### SRC-CE06-05 — MDN Performance API
- **URL:** https://developer.mozilla.org/en-US/docs/Web/API/Performance  
- **Use:** Commodity web timing instrumentation for Measure path  

### SRC-CE06-06 — OpenTelemetry Signals
- **URL:** https://opentelemetry.io/docs/concepts/signals/  
- **Use:** Conceptual observability (traces / metrics / logs) without mandating install for Explorer  

### SRC-CE06-07 — Linux kernel scheduler documentation (living)
- **URL:** https://docs.kernel.org/scheduler/  
- **Use:** Optional Engineer depth on scheduling as a contract condition (not required for Explorer)  

---

## Textbooks

### SRC-CE06-08 — Patterson & Hennessy, *Computer Organization and Design* (6th ed., 2020, Morgan Kaufmann)
- **Use:** Performance / bottleneck reasoning reinforcement when discussing compute/memory contract conditions  
- **Note:** Already present in publication `book/references/references.bib`; chapter-local cite OK  
- **Do not:** invent page citations in CE-6 preproduction  

---

## High-quality explanatory

### SRC-CE06-09 — Digital Regulation Platform overview citing ITU QoE/QoS vocabulary
- **URL:** https://digitalregulation.org/technical-regulation-quality-of-service/  
- **Use:** Secondary explanatory bridge for readers; **prefer primary ITU text** in manuscript claims  
- **Status:** explanatory adjunct only  

---

## Project / accepted-main evidence

### SRC-CE06-10 — WAIKE curriculum catalog + digital_rc packages
- **Repo:** `gunnchOS3k/waike-research-ops` @ `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`  
- **Paths:** `curriculum/catalog.yaml`; `curriculum/digital_rc/*`  
- **Verified:** 18 catalog `course_id` values; 16 digital_rc package directories including `CLOUD_DEVOPS`, `COMM_PD_ETHICS`, `COMPUTER_NETWORKING`, `EMBEDDED_PROTOTYPING`, `SOFTWARE_BUILDER`, `DATA_DASHBOARDS`, etc.  
- **Use:** Adjacent mappings only  

### SRC-CE06-11 — WAIKE accessibility & claims boundaries
- **Paths:** `ACCESSIBILITY_AND_LOW_COST.md`, `CLAIMS_TO_EVIDENCE.md` @ same SHA  
- **Use:** Phone-first / low-cost / incomplete checklist honesty  

### SRC-CE06-12 — WAIKE capstone / track materials (adjacency, not exact EMIT module)
- **Paths:** `capstones/`, `curriculum/7GC_CAPSTONE_GUIDE.md`, `digital_rc/COMM_PD_ETHICS/labs/lab_pd_capstone`, `digital_rc/CLOUD_DEVOPS/labs/lab_slo_budget`, `lab_incident_runbook`  
- **Use:** Adjacent teach-back / SLO / incident diagnosis competencies  
- **Explicit non-map:** No WAIKE ID named “Stability Contract” or “Explain Measure Improve Teach the Ecosystem”  

---

## Publication-internal

### SRC-CE06-13 — `PEDAGOGICAL_CONTRACT.md` (accepted main)
- Stability Contract definition; observation vs inference; pathway model; WAIKE evidence rule  

### SRC-CE06-14 — Chapter 2 prototype Stability Contract section + FIG-CH02-007
- Pattern reference for synthesis; **do not** copy mechanically into CE-6 canonical prose during this wave  

---

## Deferred / SOURCE_NEEDED (do not invent)

- Peer-reviewed empirical QoE web-browsing / MOS studies for CH20 depth  
- Specific carrier SLA datasets  
- Any gunnchOS measured field QoE campaign (none claimed)
