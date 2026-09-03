# Accepted-Main Source Audit

**Publication:** The Technology Landscape  
**Auditor:** cursor-agent  
**Audit date:** 2026-09-02  
**Policy:** `05_EVIDENCE_AND_ACCEPTED_MAIN_AUDIT_SPEC.md`  
**Rule:** Only accepted `main` is implementation evidence. Stale branches, open PRs, chat transcripts, and planning documents are not present capability.

---

## Audit scope

Inspect current accepted `main` for publication-useful evidence before writing project-specific claims into manuscript prose.

### Minimum targets

| Source ID | Repository | Role |
|---|---|---|
| SRC-WAIKE | `gunnchOS3k/waike-research-ops` | Curriculum, labs, assessment, accessibility, portfolio |
| SRC-DEVICE-OS | `gunnchOS3k/gunnchos-device-os` | Device OS architecture, input pipeline, runtime services |
| SRC-HARDWARE | `gunnchOS3k/gunnchos-hardware-industrial-design` | Device Quartet, industrial design, physical architecture |

### Chapter 2 relevance filter

Advanced measurement/research repos (Edge IO measurement, beam selection, spectrum/AI-RAN, NTN, 7GC twin) were **not** pulled into Chapter 2 prose claims. Chapter 2 baseline labs use commodity browser/local routes; project-specific claims stay limited to audited evidence below.

---

## Repositories audited

### 1. WAIKE — `gunnchOS3k/waike-research-ops`

| Field | Value |
|---|---|
| Branch | `main` |
| HEAD SHA | `8eb2827dc58ffa391842da1bfb1ee665c25a31a7` |
| Audited at | 2026-09-02 |
| License | MIT |
| Default description | Education/ops curriculum with file-backed courses and validators |

#### Publication-useful artifacts

- `curriculum/catalog.yaml` — 18 catalog `course_id` values
- `curriculum/digital_rc/*/course.json` — 16 digital RC packages
- `curriculum/taxonomy/eighteen_tracks.json` — track/academy IDs
- `schema/waike_*.v1.json` — course/pathway schemas
- `ACCESSIBILITY_AND_LOW_COST.md` — phone-first / low-cost / offline-first principles
- `CLAIMS_TO_EVIDENCE.md` — claim boundary table
- Lab validators under `src/waike_course_ready/`
- Offline packs under `curriculum/digital_rc/*/offline_pack/`

#### Current capabilities (safe wording)

- Dual curriculum ID systems exist and are file-backed on accepted main.
- Runnable JSON lab validators reject empty submissions and bare `PASS` strings.
- Accessibility and low-cost are documented design principles; checklist items are largely unchecked.
- Explicit non-claims include commercial 6G, certified hardware, and finished console.

#### Current limitations

- No literal UI “trace one tap” lab.
- Many portfolio/syllabus stubs remain thin; depth concentrates in `curriculum/digital_rc/`.
- README “14 digital-RC” text is stale versus on-disk count of 16.
- Localization/accessibility implementation incomplete.

#### Candidate labs / patterns (not renamed into false IDs)

| Pattern | Evidence | Book use |
|---|---|---|
| Trace one packet | `COMPUTER_NETWORKING` week 10 / `lab_datapath` | Network-path teaching analogy |
| Channel taps / delay | `lab_delay_spread` (`WIRELESS_6G`) | Latency math; “tap” ≠ touch |
| Input actions | `lab_input_actions` (`GAME_DEV_INTERACTIVE`) | Input remapping competency |
| ISR vs poll latency budget | `lab_ep_isr_vs_poll` (`EMBEDDED_PROTOTYPING`) | Fixture latency budget |

#### Claims triage

- **Safe:** MIT curriculum ops repo; 18 catalog + 16 digital_rc packages; synthetic lab fixtures with honesty flags.
- **Qualified:** phone-first/low-cost/accessible as intent; 6G-aligned foresight as research framing.
- **Unsupported:** measured phone tap-to-response stack; commercial 6G; accredited degree; field deployment outcomes.

---

### 2. Device OS — `gunnchOS3k/gunnchos-device-os`

| Field | Value |
|---|---|
| Branch | `main` |
| HEAD SHA | `28562a8456207540c205a1c8a6434a491b0a4771` |
| Audited at | 2026-09-02 |
| License | MIT |

#### Publication-useful artifacts

- `gunnchos_device_os/runtime/catalog.py` — 18 digital runtime service IDs
- `gunnchos_device_os/shell/input_routing.py` — touch/controller/keyboard/ring sources; remaps
- `gunnchos_device_os/device_lab/input_router.py` — confidence-gated virtual delivery
- `ring_input/` — software-simulated ring adapter; physical not claimed
- `docs/WHAT_IS_REAL_TODAY.md`, `docs/USER_FOCUSED_OS_ARCHITECTURE.md`
- `beta_gate/beta_gate_status.yaml` — `beta_ready: false`
- Claim boundaries: `CLAIMS_TO_EVIDENCE.md`, `product/CLAIM_BOUNDARY.md`, service `CLAIM_BOUNDARY`

#### Current capabilities (safe wording)

- Device OS **alpha**: config-driven experience layer, launcher mock, in-process digital runtime services, CI smoke validation.
- Software-simulated input routing for touch/ring/controller/keyboard_mouse.
- Accessibility manager and related contracts exist; WCAG certification is not claimed.
- Telemetry is opt-in consent modeling; default off.

#### Current limitations

- Not a shipping OS; not systemd/kernel init; not bootable ISO with hardware boot evidence.
- Physical ring / silicon input stack pending.
- Production MDM, secure boot completion, streaming certification unsupported.

#### Candidate Chapter 2 excerpts (must label SOFTWARE_SIMULATED / digital)

- `DEFAULT_REMAPS` / `INPUT_SOURCES` in `shell/input_routing.py`
- Runtime start order tests (`hal → input → ring`)
- `ring_input/STATUS.yaml` honesty fields
- Architecture Mermaid under `docs/diagrams/` and UML `docs/uml/current/`

#### Claims triage

- **Safe:** alpha digital OS experience + simulated I/O runtime with claim boundaries.
- **Qualified:** installable bundle prototype; accessibility-first intent; firmware/hardware compatibility harnesses.
- **Unsupported:** finished OS; boots on reference hardware; physical ring; production telemetry/fleet; beta/GA.

---

### 3. Hardware / industrial design — `gunnchOS3k/gunnchos-hardware-industrial-design`

| Field | Value |
|---|---|
| Branch | `main` |
| HEAD SHA | `9ee0ef2f688b2c18428bfabc316b23687a02988d` |
| Audited at | 2026-09-02 |
| License | MIT |
| Canonical hardware repo? | **Yes** — selected as the current canonical hardware/industrial-design source |

#### Publication-useful artifacts

- `docs/device-quartet/` — Student 14.5, Handheld Hybrid, DS-XL Coder, Edge IO Wearables
- `device_designs/{student_14_5,handheld_hybrid,ds_xl_coder,edge_io_rings,dock}/`
- `architecture/SYSTEM_BLOCK_DIAGRAM.md`, `DEVICE_COMPARISON_MATRIX.md`, `POWER_TREE.md`
- `DIGITAL_MANUFACTURING_READINESS.md` — `DIGITAL_FABRICATION_PASS=FALSE`
- `physical_evidence/README.md` — HARDWARE_PROTOTYPE_PENDING
- Exploded-view placeholders under `cad/openscad/` and `exports/renders/`

#### Current capabilities (safe wording)

- Device Quartet defined as **research form factors / learning benchmarks**, concept-complete with simulation substitutes.
- Digital industrial-design packets exist (BOM/CAD/KiCad/validators) under physical freeze.
- Candidate MPNs frozen for design (not purchase authorization).

#### Current limitations

- `PHYSICAL_PENDING`; no fab/send RFQ/certification marks.
- NDA blocks exact COM-HPC / some dock pin maps; do not invent pinouts.
- Latency/battery numbers in research specs are targets, not measured results.
- Naming split: Quartet “Edge IO Wearables” vs design package `edge_io_rings` vs folder `wearables_arena_set`.

#### Candidate Chapter 2 figures

All must be labeled **Representative educational architecture** / conceptual unless a specific validated revision is cited (none available for physical EVT).

#### Claims triage

- **Safe:** digital industrial-design SoT; Quartet research roles; MIT docs; learning without custom hardware purchase.
- **Qualified:** design-release candidate / Cont IX “ready” tokens subordinate to front-door PHYSICAL_PENDING.
- **Unsupported:** certified hardware; assembled EVT units; measured battery/thermal/RF; commercial 6G modem; Thunderbolt 5 dock.

---

## Accepted-main SHAs

| Repo | Branch | SHA |
|---|---|---|
| waike-research-ops | main | `8eb2827dc58ffa391842da1bfb1ee665c25a31a7` |
| gunnchos-device-os | main | `28562a8456207540c205a1c8a6434a491b0a4771` |
| gunnchos-hardware-industrial-design | main | `9ee0ef2f688b2c18428bfabc316b23687a02988d` |

---

## Licensing considerations

All three audited sources are **MIT**. This publication repository uses a **hybrid development-stage rights model**: manuscript prose, original artwork/figures, and instructor-only assets are **All Rights Reserved** during development; publication infrastructure/scripts and identified runnable lab code may use **MIT**. There is **no** blanket Creative Commons license for the book at this stage. Upstream WAIKE/gunnchOS materials retain their upstream licenses. See `publication/BOOK_LICENSE_DECISION.md`. Do not copy NDA vendor collateral. Prefer original educational diagrams.

---

## Accessibility notes from audit

Upstream accessibility documents emphasize phone-first, offline-first, low-cost, and plain language. Automated WCAG certification evidence is absent. Publication figures must carry alt text, long descriptions, and reading order independently.

---

## Claims safe to use in Chapter 2 (project-specific)

1. WAIKE maintains file-backed curriculum packages and lab validators on accepted main (cite SRC-WAIKE SHA).
2. gunnchOS device OS exposes a software-simulated input routing path and digital runtime service catalog on accepted main (cite SRC-DEVICE-OS SHA).
3. Device Quartet research form factors are defined in the hardware industrial-design repo as concept-complete learning benchmarks (cite SRC-HARDWARE SHA).

## Claims requiring qualification

1. Any “OS” wording → alpha / digital / not shipping.
2. Any device exploded view tied to gunnchOS → representative educational architecture.
3. Any WAIKE mapping → use exact catalog/digital_rc IDs; do not invent a tap-lab module ID.
4. Any latency numbers without a measurement bundle → illustrative or inferred only.

## Claims not currently supported

See `evidence/unresolved_claims.md`.

## Upstream gaps

| Gap | Dependency | Publication response |
|---|---|---|
| No commodity-free tap-to-photon measurement on proprietary hardware | Physical devices + method | LAB-TAP-001 uses browser/local commodity routes |
| No WAIKE course module literally named for UI tap tracing | Curriculum design decision | Align competencies without inventing IDs |
| Physical EVT validation | Manufacturing / lab | Keep PHYSICAL_PENDING labels |

---

## Audit integrity statement

This audit did not modify upstream repositories. Where the book needs a capability that is not implemented, the claim is registered as planned/future/illustrative rather than silently “fixed” in product source.

---

## Refresh note — Agent EVIDENCE-B (2026-09-03)

Re-fetched current `origin/main` SHAs for project-evidence closure:

| Repo | Branch | Commit SHA |
|---|---|---|
| gunnchos-technology-landscape | main | `18ec58005529bd16d680ee7419e4dea13150e9c6` |
| waike-research-ops | main | `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` |
| gunnchos-device-os | main | `28562a8456207540c205a1c8a6434a491b0a4771` |
| gunnchos-hardware-industrial-design | main | `9ee0ef2f688b2c18428bfabc316b23687a02988d` |

See `evidence/PROJECT_EVIDENCE_CLOSURE_B.md` for claim-level citations. Prior table rows above may retain older audit-day SHAs for history; use this refresh block for current main.
