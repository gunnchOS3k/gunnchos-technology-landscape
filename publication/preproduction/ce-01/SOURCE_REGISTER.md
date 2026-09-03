# CE-1 Source Register (chapter-local)

**Chapter:** CE-1 / CH01  
**Purpose:** Proposed sources for Concept Edition preproduction.  
**Rule:** Verified entries only. Do **not** copy into `book/references/references.bib` until the integrator validates.  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Verification method

- Standards: official publisher / RFC Editor / W3C / ISO catalog pages checked 2026-09-03 (agent local date context: session 2026-09-02 evening CT; sources re-checked during package authoring).
- Textbooks: publisher/ISBN confirmed via Elsevier/OCW/prior publication bibliography already verified on accepted main where reused.
- Project repos: accepted-main SHAs recorded below; chapter agent does not edit shared `evidence/source_registry.yaml`.

## Preferred hierarchy used

1. Standards / specifications  
2. Official technical documentation  
3. Peer-reviewed literature (none required for CE-1 core claims in this wave)  
4. Respected technical textbooks  
5. High-quality explanatory sources only when needed for learner-facing timing APIs

---

## A. Standards / specifications

| Local ID | Citation key | Work | Status / edition | Class | CE-1 use |
|---|---|---|---|---|---|
| SRC-CE1-S1 | `iso-iec-25010-2023` | ISO/IEC 25010:2023 Product quality model | International Standard, published 2023-11 | standard | Multi-property quality vocabulary (not certification) |
| SRC-CE1-S2 | `rfc791` | Internet Protocol | IETF RFC 791 (1981) | standard | Optional remote branch / packet concept foreshadow |
| SRC-CE1-S3 | `rfc9293` | TCP | IETF RFC 9293 (2022) | standard | Reliable transport foreshadow for remote branch |
| SRC-CE1-S4 | `whatwg-html` | HTML Living Standard | Living Standard | standard | Event loop / scripting context (accessible depth) |
| SRC-CE1-S5 | `whatwg-dom` | DOM Living Standard | Living Standard | standard | Events / dispatch model |
| SRC-CE1-S6 | `wcag22-20231005` | W3C WCAG 2.2 | W3C Recommendation (2023-10-05) dated TR | standard | Accessibility obligations for readiness UI; distinct from CE-6 `wcag22-20241212` |

**Living vs fixed:** WHATWG HTML/DOM are living standards (no single frozen year as authority). RFCs and ISO 25010:2023 are fixed publications. WCAG 2.2 is a dated W3C Recommendation.

## B. Official technical documentation

| Local ID | Citation key | Work | Notes | CE-1 use |
|---|---|---|---|---|
| SRC-CE1-D1 | `linux-scheduler` | Linux kernel scheduler docs (kernel.org) | Living documentation | Optional OS scheduling dependency language |
| SRC-CE1-D2 | `mdn-performance` | MDN Performance API | Explanatory + API docs | Optional operator timing instrumentation later |

## C. Textbooks

| Local ID | Citation key | Work | Edition / year | ISBN (verified) | CE-1 use |
|---|---|---|---|---|---|
| SRC-CE1-T1 | `saltzer-kaashoek` | Saltzer & Kaashoek, *Principles of Computer System Design: An Introduction* | Morgan Kaufmann, 2009 | 978-0-12-374957-4 | Systems abstractions / layered design |
| SRC-CE1-T2 | `tanenbaum-bos` | Tanenbaum & Bos, *Modern Operating Systems* | 5th ed., Pearson, 2022 | (reuse accepted-main bib note; do not invent pages) | Processes/OS abstractions |
| SRC-CE1-T3 | `patterson-hennessy` | Patterson & Hennessy, *Computer Organization and Design* | 6th ed. MIPS, Morgan Kaufmann, 2020 | (reuse accepted-main bib) | RAM vs storage distinction |

## D. Project / repository evidence (accepted main)

| Local ID | Citation key | Repository | Branch | SHA used | CE-1 use |
|---|---|---|---|---|---|
| SRC-CE1-P1 | `src-waike` | `gunnchOS3k/waike-research-ops` | `main` | `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` | Curriculum adjacency audit |
| SRC-CE1-P2 | `src-hardware-quartet` | `gunnchOS3k/gunnchos-hardware-industrial-design` | `main` | `9ee0ef2f688b2c18428bfabc316b23687a02988d` (from publication accepted-main audit dated 2026-09-02; PHYSICAL_PENDING) | Device Quartet research form factors |
| SRC-CE1-P3 | `src-device-os` | `gunnchOS3k/gunnchos-device-os` | `main` | `28562a8456207540c205a1c8a6434a491b0a4771` (audit 2026-09-02) | Optional later cross-ref only; **not** required for CE-1 lab |

**WAIKE note:** Shared registry on publication main still lists older WAIKE SHA `8eb2827…`. This chapter-local audit records newer accepted `main` `e97e74f…` via `git ls-remote` + local clone HEAD agreement. Integrator should reconcile shared registry.

## E. Sources considered but not used as CE-1 authority

- Marketing pages for consumer devices (brand endorsement risk).
- Undated blog posts inventing “average app launch times.”
- Any claim requiring Device Quartet physical EVT data (PHYSICAL_PENDING).

## F. Integrity checklist

- [x] No invented DOI/ISBN/pages for new entries  
- [x] Living standards labeled as living  
- [x] Project claims tied to SHAs  
- [x] Chapter-local bib only (`references.local.bib`)

## Project evidence closure (2026-09-03)

See `evidence/PROJECT_EVIDENCE_CLOSURE_B.md` for accepted-main SHA citations resolving prior `PROJECT_EVIDENCE_NEEDED` claims in this package.
