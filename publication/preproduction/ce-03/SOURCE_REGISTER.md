# CE-3 Source Register (chapter-local proposal)

**Module:** CE-3  
**Status:** `preproduction` — do **not** copy into canonical `book/references/references.bib` until integrator validation.  
**Verification rule:** No invented DOI/ISBN/pages/years/revision numbers. Living standards marked as living.

Audited project SHAs for this package:

| Source ID | Repository | Branch | SHA | Audited |
|---|---|---|---|---|
| SRC-WAIKE | gunnchOS3k/waike-research-ops | main | `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` | 2026-09-02 |
| SRC-DEVICE-OS | gunnchOS3k/gunnchos-device-os | main | `28562a8456207540c205a1c8a6434a491b0a4771` | 2026-09-02 |
| SRC-HARDWARE | gunnchOS3k/gunnchos-hardware-industrial-design | main | `9ee0ef2f688b2c18428bfabc316b23687a02988d` | 2026-09-02 |

Note: WAIKE SHA advanced relative to the Chapter 2 publication audit (`8eb2827…`). CE-3 crosswalk uses the newer accepted-main tip above.

---

## Preferred hierarchy used

1. Standards / specifications  
2. Official technical documentation  
3. Peer-reviewed literature (none required for CE-3 baseline claims)  
4. Respected technical textbooks  
5. High-quality explanatory sources only when primary material is unsuitable for audience

---

## A. Standards / specifications

| Local key | Work | Verification | Class | CE-3 use |
|---|---|---|---|---|
| `jedec-jesd79-4d` | JEDEC **JESD79-4D** DDR4 SDRAM Standard | JEDEC listing: published **Jul 2021**, document JESD79-4D (supersedes earlier 79-4 revisions). Paywalled full text; bibliographic identity verified via jedec.org. | Fixed publication (revisioned standard) | Main-memory device example behind RAM layer |
| `nvme-base-spec` | NVM Express Base Specification family | Standards home: https://nvmexpress.org/specifications/ — **revision pin SOURCE_NEEDED** before citing a specific version number in prose | Living family / revisioned docs | SSD/storage interface naming |
| `khronos-vulkan-overview` | Vulkan overview / API family (Khronos) | Living docs hub: https://www.khronos.org/vulkan/ — treat as living; do not invent extension versions | Living | Accessible GPU/API mediation pointer |

---

## B. Official technical documentation (living)

| Local key | Work | URL | Notes |
|---|---|---|---|
| `linux-scheduler` | Linux CPU Scheduler documentation | https://docs.kernel.org/scheduler/ | Living kernel docs; already cited in global bib for CH02 |
| `linux-cpu-freq` | CPU Performance Scaling | https://docs.kernel.org/admin-guide/pm/cpufreq.html | Living; power/perf governors |
| `linux-memory` | Memory Management docs index | https://docs.kernel.org/admin-guide/mm/index.html | Living; virtual memory / reclaim concepts at Engineer depth |

---

## C. Textbooks (verified bibliographic identity)

| Local key | Work | Verified identity | Notes |
|---|---|---|---|
| `patterson-hennessy-riscv` | Patterson & Hennessy, *Computer Organization and Design RISC-V Edition: The Hardware/Software Interface*, **2nd ed.** | Elsevier/Morgan Kaufmann, published **Dec 2020**; ISBN **978-0-12-820331-6** (also listed 978-0-12-824558-3 for related format). Verified via Elsevier shop / Google Books metadata. | Preferred CE-3 architecture text (hierarchy, parallelism, DSA) |
| `tanenbaum-bos` | Tanenbaum & Bos, *Modern Operating Systems*, **5th ed.** | Pearson, published **2022** (© 2023); ISBN **978-0-13-761888-0** (Pearson+); print ISBN also listed **978-0-13-761887-3**. Matches global bib note. | Processes, threads, FS, scheduling |
| `silberschatz-galvin-gagne` | Silberschatz, Galvin, Gagne, *Operating System Concepts*, **10th ed.** | Wiley; e-text ISBN **978-1-119-32091-3** (Apr 2018 listing); loose-leaf ISBN **978-1-119-80036-1** (Feb 2021). Author site os-book.com/OS10/. | Alternate OS reference; pick one primary in prose to avoid duplicate dumps |

**Do not invent page numbers** in chapter-local claims. Cite edition + concept, not fake pages.

---

## D. Project / repository evidence

| Local key | Artifact | SHA | Use boundary |
|---|---|---|---|
| `src-waike` | curriculum/catalog.yaml; digital_rc `{EMBEDDED_PROTOTYPING,GENERAL_IT,HARDWARE_ENGINEERING,SOFTWARE_BUILDER}` | `e97e74f…` | Adjacent lab mapping only |
| `src-device-os` | docs/WHAT_IS_REAL_TODAY.md; claim boundaries | `28562a8…` | Alpha/digital only; not shipping OS proof |
| `src-hardware` | docs/device-quartet/*; architecture/DEVICE_COMPARISON_MATRIX.md; POWER_TREE.md | `9ee0ef2…` | Representative form factors; PHYSICAL_PENDING |

---

## E. Explanatory / lab-owned

| Local key | Work | Notes |
|---|---|---|
| `lab-cms-001-plan` | Publication-owned LAB-CMS-001 plan in this package | Not external authority; observation protocol only |
| `mdn-performance` | MDN Performance API | Optional if Builder path instruments a tiny web workload; living docs |

---

## Explicit non-sources / rejected for CE-3 baseline

- Invented vendor whitepapers with fake peak TOPS/GHz as “measured.”  
- NDA COM-HPC / dock pin maps.  
- Unpinned “NVMe 2.x” claims without document revision.  
- Chat transcripts / open PRs as capability evidence.

---

## Integrator handoff

Propose promoting to global bibliography after review: `patterson-hennessy-riscv` (if distinct from existing MIPS entry), `silberschatz-galvin-gagne`, `jedec-jesd79-4d`, `linux-cpu-freq`, `linux-memory`. Keep project SHAs in evidence registries—not as BibTeX pseudo-standards.

## Project evidence closure (2026-09-03)

See `evidence/PROJECT_EVIDENCE_CLOSURE_B.md` for accepted-main SHA citations resolving prior `PROJECT_EVIDENCE_NEEDED` claims in this package.
