# Concept Edition Integration Report

**Branch:** `cursor/concept-edition-preproduction-001`  
**Wave:** Concept Edition evidence-first preproduction (CE-1/3/4/5/6)  
**Gate status (unchanged):** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Integrator rule:** Chapter packages merged as-is; shared live registries (glossary, claims, figures, labs, WAIKE, CH02-REVIEW-R1) were **not** rewritten. Candidate indexes live under `publication/preproduction/CANDIDATE_*.yaml`.

---

## A. Accepted-main SHA

| Item | Value |
|---|---|
| Accepted `origin/main` | `166e9544bc6e2aee344bc962ace76d49ee3e04e4` |
| Tip commit | Merge pull request **#2** (`cursor/gate3-reader-validation-prep`) |
| Contains PR #2 | **Yes** (verified via `git fetch --all --prune` + `git log`) |
| Advanced beyond brief? | No — matches wave brief SHA |

Integration branch was created from this accepted-main tip. Local stale `main` pointers were reset to `origin/main` before branching.

---

## B. Five chapter package status

All five packages were brought in with `git checkout <agent-branch> -- publication/preproduction/ce-0N/`. **No merge conflicts.** Each package has all **13** required artifacts.

| CE | Agent branch | Commit | Artifacts | Concepts | Claims | Figures | Anchor lab |
|---|---|---|---:|---:|---:|---:|---|
| CE-1 | `agent-a/ce-01-preproduction` | `17461af` | 13/13 | 12 | 10 | 7 | `LAB-SYS-001` |
| CE-3 | `agent-b/ce-03-preproduction` | `05852b1` | 13/13 | 16 | 14 | 9 | `LAB-CMS-001` |
| CE-4 | `agent-c/ce-04-preproduction` | `3bb563d` | 13/13 | 18 | 15 | 8 | `LAB-PKT-001` |
| CE-5 | `agent-d/ce-05-preproduction` | `5d4a74b` | 13/13 | 15 | 9 | 7 | `LAB-TRUST-001` |
| CE-6 | `agent-e/ce-06-preproduction` | `864de4d` | 13/13 | 14 | 14 | 10 | `LAB-CE06-001` |

Schema note (honest): packages use slightly different YAML field names (`concepts` vs `nodes`; `truth_classification` vs `truth_class` vs `conceptual_vs_measured`; CE-5 claim statuses `verified`/`planned`). Validator accepts these variants. Candidate indexes normalize IDs without rewriting chapter-local files.

`scripts/validate_ce_preproduction.py` + `tests/test_ce_preproduction.py` **PASS**.

---

## C. Cross-chapter prerequisite graph

```text
CE-1 (systems lens; no prior CE deps)
  └─► CE-2 / CH02 (prototype; under R1 — do not modify)
        ├─► CE-3 (local CPU/memory/storage/OS)
        │     └─► CE-4 (packets / access / edge-cloud)
        │           └─► CE-5 (AI / security / privacy / trust)
        └─► CE-6 (Stability Contract + EMIT capstone synthesizes CE-1…CE-5)
```

| Chapter | Declared priors | Feeds |
|---|---|---|
| CE-1 | None (entry) | CE-2 method; CE-3–6 ecosystem lens |
| CE-3 | CE-1 systems lens; CE-2 experience method (light CPU/RAM terms) | CE-4 local-vs-network; CE-5 local AI; CE-6 bottlenecks |
| CE-4 | CE-1 optional network branch; CE-2 packet named; CE-3 local machine | CE-5 placement/trust; CE-6 path conditions |
| CE-5 | CE-1–4 ecosystem + path + local machine | CE-6 trust/privacy as contract conditions |
| CE-6 | All prior CE + CE-2 Stability Contract intro | Full-book CH20/CH25/CH30/CH31 depth |

Canonical drafting of CE-1/3/4/5/6 prose should wait on CH02 human feedback shaping tone/depth/example density.

---

## D. Glossary collisions

Candidate index: `publication/preproduction/CANDIDATE_GLOSSARY.yaml` (**75** glossary-leaning entries). Live `glossary/glossary.yaml` **not** modified.

| Finding | Detail |
|---|---|
| Exact cross-CE term collisions | **None** found on normalized `canonical_term` / `name` |
| Conflicting definitions | No same-term multi-CE conflicts requiring immediate rewrite |
| Aliases / schema drift | CE-3/4 use `nodes` + `plain_language`; CE-1/6 use `concepts` + `plain_language_definition`; CE-5 uses `name` / `plain_language` — integrator should canonicalize later |
| Terms introduced early | CE-1 foreshadows Device Quartet, failure domains, optional network — intentional. CE-3 reinforces CPU/RAM/storage lightly introduced in CH02 (`reinforced_here` / `prior_intro: CH02`) |
| CH02 compatibility later | Live glossary already defines **stability contract** (CE-6 reinforces). Packet / process / latency terms from CH02 should be aligned post-R1 without editing R1 snapshot materials now |
| Do-not-touch | `CH02-REVIEW-R1`, live glossary, open Gate 3 responses |

---

## E. Citation / source overlap

Candidate index: `CANDIDATE_SOURCE_INDEX.yaml`. Canonical `book/references/references.bib` and live `evidence/source_registry.yaml` **not** modified.

### Reusable across chapters (bib key overlaps observed)

| Key / theme | Appears in |
|---|---|
| `rfc791`, `rfc9293` | CE-1, CE-4 |
| `tanenbaum-bos`, `linux-scheduler`, `mdn-performance` | CE-1, CE-3 |
| `wcag22` | CE-1, CE-6 |
| WAIKE / hardware / device-os SHAs | CE-1, CE-3, CE-4, CE-5, CE-6 |

### Conflicting metadata

| Topic | Finding |
|---|---|
| WAIKE accepted-main SHA | Chapter audits agree on `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`; live shared registry still records CH02 audit `8eb2827…`. **Candidate note only** — defer live refresh until after R1 |
| Hardware / device-os SHAs | Consistent with publication audit (`9ee0ef2…`, `28562a8…`) |

### Weak / deferred sources (not inflated)

- Peer-reviewed journals largely deferred (CE-1/3/4/6 = **0** peer-reviewed entries by design; CE-5 has **2**)
- 3GPP / NVMe revision pins left living / `SOURCE_NEEDED` rather than invented
- Marketing / undated blogs explicitly rejected in chapter registers

Exact class counts: see section J in the parent final report / `CANDIDATE_SOURCE_INDEX.yaml`.

---

## F. Figure system

Candidate index: `CANDIDATE_FIGURE_INDEX.yaml` (**41** proposed figures).

### Repeated templates (should become shared visual patterns)

1. **System map / exploded ecosystem** — CE-1, CE-3, CE-4, CE-6  
2. **Comparative layers / scopes** — CE-1 app cards; CE-3 memory hierarchy; CE-4 local/LAN/Internet; CE-5 local vs cloud AI  
3. **Sequence / path diagrams** — CE-3 instruction path; CE-4 packet path; CE-6 diagnosis path  
4. **Status vs usable experience** — CE-1 readiness; CE-4 connectivity; CE-6 chrome vs outcome  
5. **Failure-domain / trust-boundary maps** — CE-1, CE-5, CE-6  

### Unique / chapter-specific

- CE-3 Device Quartet compute callout (`PHYSICAL_PENDING` only)  
- CE-4 Wi-Fi vs cellular on-ramps (must not synonymize)  
- CE-5 identity ladder + privacy lifecycle  
- CE-6 EMIT / Stability Contract hub-and-spoke + rubric visualization  

### Workload

~41 planned Concept Edition figures (not drawn). Production should prioritize templates above before one-off art. No decorative-as-evidence proposals accepted.

---

## G. Lab progression

| Stage | Lab | Role |
|---|---|---|
| Observe | `LAB-SYS-001` (CE-1) | Name system behind a familiar “open”; chrome vs usable |
| Inspect | `LAB-CMS-001` (CE-3) | Local lag with healthy connectivity icon; hierarchy inspection |
| Build / path | `LAB-PKT-001` (CE-4) | Packet/connectivity path across scopes with fixture fallback |
| Measure / diagnose trust | `LAB-TRUST-001` (CE-5) | Local vs remote AI + identity/privacy boundaries |
| Synthesize | `LAB-CE06-001` (CE-6) | EMIT capstone — explain, measure, improve, teach |

All five lab plans include evidence/portfolio language and offline/fixture fallback. None require Device Quartet hardware. Depth ladders cover Explorer → Operator → Builder → Engineer → Researcher (Educator facilitation where present). Progression intentionally avoids duplicating `LAB-TAP-001` as the CE-1/3/4/5/6 primary lab.

---

## H. WAIKE crosswalk (CE-wide)

Candidate index: `CANDIDATE_WAIKE_CROSSWALK.yaml`.

| Package | Relationship vocabulary | Known courses cited (examples) |
|---|---|---|
| CE-1 | exact / adjacent / proposed / no-map | `GENERAL_IT`, `SOFTWARE_BUILDER`, … |
| CE-3 | exact / adjacent / proposed / no-map | `EMBEDDED_PROTOTYPING`, `HARDWARE_ENGINEERING`, … |
| CE-4 | exact / adjacent / proposed / no-map | `COMPUTER_NETWORKING`, `CLOUD_DEVOPS`, `WIRELESS_6G` |
| CE-5 | exact / adjacent / proposed / no-map | `AI_ML_EDGE`, `CYBERSECURITY`, `COMM_PD_ETHICS` |
| CE-6 | exact / adjacent / proposed / no-map | multi-course adjacency; **no exact** Stability Contract / EMIT module |

Shared findings:

- Preferred audit SHA across chapter packages: `e97e74f…`  
- Publication-owned labs (`LAB-SYS-001`, `LAB-CMS-001`, `LAB-PKT-001`, `LAB-TRUST-001`, `LAB-CE06-001`) are **no-map / proposed** as WAIKE IDs — not invented upstream module IDs  
- Live `waike/alignment.yaml` left untouched

---

## I. Device Quartet use balance

| Form factor | Intended learning role | CE coverage (honest) |
|---|---|---|
| Student 14.5″ | Sustained learning/work | Named in CE-1 foreshadow; CE-3 representative compute/storage; not forced elsewhere |
| Handheld Hybrid | Mobile / docked interaction | CE-1 foreshadow; CE-3 form-factor contrast |
| DS-XL Coder | Strongest learn-to-build form | CE-1 foreshadow; CE-3 builder adjacency |
| Edge IO Wearables | Embodied sensing / haptics / HUD / safety | CE-1 foreshadow; light CE-5/6 analogy only |

Balance check:

- **CE-1:** Introduces Quartet as future lab spine — **non-marketing**, labs on commodity devices  
- **CE-3:** Optional figure/callout with `PHYSICAL_PENDING`  
- **CE-4:** Explicit non-requirement (commodity connectivity)  
- **CE-5 / CE-6:** Research form factor / analogy only; capstone must not require Quartet SKUs  

No chapter forces a device into every section. All project-specific Quartet claims remain `PHYSICAL_PENDING`.

---

## J. Gate 3 dependency — waits for CH02 human feedback

Do **not** close Gate 3. Do **not** alter `CH02-REVIEW-R1`.

Must wait on real Explorer / Builder / Engineer (/ optional Educator) feedback before:

1. Final chapter **tone, depth, and example density** for CE-1/3/4/5/6 canonical prose  
2. Whether CE anatomy section lengths should match CH02 mechanically or adapt  
3. Figure density / reading-order preferences validated by humans  
4. Lab friction and portfolio rigor calibrated to CH02 `LAB-TAP-001` results  
5. Glossary term plain-language finalization where CH02 terms overlap  
6. Any promotion of chapter-local claims/figures/labs into **live** shared registries  
7. Refresh of live WAIKE SHA in `evidence/source_registry.yaml` (candidate note only for now)

Allowed now (and done in this PR): source research, concept graphs, claim plans, figure briefs, lab plans, WAIKE adjacency maps, career maps, SEA planning, candidate indexes, validators.

---

## Integrator deliverables in this PR

- `publication/preproduction/ce-0{1,3,4,5,6}/` — five complete packages  
- `publication/preproduction/CANDIDATE_*.yaml` — six candidate indexes  
- `scripts/validate_ce_preproduction.py` + `tests/test_ce_preproduction.py`  
- Makefile `validate` target includes CE preproduction check  
- This report
