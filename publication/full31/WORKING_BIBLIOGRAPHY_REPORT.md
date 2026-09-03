# Working Full-Book Bibliography Report (Agent EVIDENCE-C)

**schema_version:** `1.0.0`  
**status:** `WORKING_FULL31_BIBLIOGRAPHY`  
**gate_note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**scope:** Full31 manuscript-wave working bibliography (CE candidate truth + accepted-main book/references gaps + Full31 chapter overlay)  
**global merge:** not authorized — working set only (see Integrator merge notes)

## Counts (report separately)

| Metric | Value |
|---|---:|
| CE chapter-local source occurrences | 64 |
| Full31 citation-token occurrences (CLAIM_PLAN + SOURCE_NEEDS) | 116 |
| Unique bib keys (working set) | 63 |
| Unique canonical works | 55 |
| Same-work alias groups | 7 |

Canonical-work grouping priority: DOI → ISBN+edition → dated standards/RFC → URL+dated edition → repo+commit+role → title/author/year uncertain fallback. The two WCAG dated Recommendations remain distinct works.

### Verification status (unique keys)

| verification_status | count |
|---|---:|
| `NEEDS_PRIMARY_VERIFICATION` | 1 |
| `PRIMARY_METADATA_VERIFIED` | 47 |
| `REPOSITORY_EVIDENCE_VERIFIED` | 8 |
| `SECONDARY_EXPLANATORY` | 7 |

### Classification (unique keys)

| source_class | count |
|---|---:|
| `official_technical_documentation` | 14 |
| `other_explanatory` | 5 |
| `peer_reviewed` | 2 |
| `project_accepted_main` | 8 |
| `standards_specifications` | 25 |
| `textbooks` | 9 |

## WCAG 2.2 confirmation

Working bibliography preserves **two** dated Recommendation records:

| Bib key | Year | Dated TR URL | In working set |
|---|---|---|---|
| `wcag22-20231005` | 2023 | https://www.w3.org/TR/2023/REC-WCAG22-20231005/ | yes |
| `wcag22-20241212` | 2024 | https://www.w3.org/TR/2024/REC-WCAG22-20241212/ | yes |

Blocked undated key `wcag22` occurrences in Full31 packets: **1** (must remap to dated keys before prose cite).
- `ch14` via `claim_plan.citation_keys` token `wcag22`

## Same-work aliases

- `title:computer organization and design: the hardware/software interface|author:patterson, david a. and hennessy, john l.|year:2020` → ['patterson-hennessy', 'patterson-hennessy-ce06']
- `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance|year:2026` → ['mdn-performance', 'mdn-performance-ce06']
- `url:https://docs.kernel.org/scheduler/|year:2026` → ['linux-scheduler', 'linux-scheduler-ce06']
- `url:https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design|year:2026` → ['src-hardware-ce3', 'src-hardware-quartet']
- `url:https://github.com/gunnchOS3k/gunnchos-technology-landscape|year:2026` → ['gunnchos-technology-landscape-ce06', 'gunnchosTechnologyLandscape2026']
- `url:https://github.com/gunnchOS3k/waike-research-ops|year:2026` → ['src-waike', 'src-waike-ce3', 'waike-research-ops-ce06']
- `url:https://html.spec.whatwg.org/|year:2026` → ['whatwg-html', 'whatwg-html-ce06']

## Unresolved / non-bib tokens

- Non-bib project/gate tokens: **4** (not promoted as bibliography entries)
- Unresolved citation tokens (no working bib key): **16**
  - `ch21` `peer_eval_methods` (bib_key_not_in_working_set; source_needs.table)
  - `ch22` `edge_ml_sys_refs` (bib_key_not_in_working_set; source_needs.table)
  - `ch22` `sensing_privacy_std` (bib_key_not_in_working_set; source_needs.table)
  - `ch23` `owasp_living` (bib_key_not_in_working_set; source_needs.table)
  - `ch24` `safety_std_selection` (bib_key_not_in_working_set; source_needs.table)
  - `ch25` `ict_access_stats` (bib_key_not_in_working_set; source_needs.table)
  - `ch26` `git_official_docs` (bib_key_not_in_working_set; source_needs.table)
  - `ch26` `semver_or_conventional_commits` (bib_key_not_in_working_set; source_needs.table)
  - `ch27` `otel_docs` (bib_key_not_in_working_set; source_needs.table)
  - `ch27` `LAB-CE06-001` (bib_key_not_in_working_set; source_needs.table)
  - `ch28` `digital_twin_std` (bib_key_not_in_working_set; source_needs.table)
  - `ch28` `repro_research_guide` (bib_key_not_in_working_set; source_needs.table)
  - `ch29` `product_design_refs` (bib_key_not_in_working_set; source_needs.table)
  - `ch30` `bls_or_equivalent` (bib_key_not_in_working_set; source_needs.table)
  - `ch31` `LAB-CE06-001` (bib_key_not_in_working_set; source_needs.table)
  - `ch31` `SRC-CE06-01` (bib_key_not_in_working_set; source_needs.table)

## Unique records

| bib_key | source_class | verification_status | chapter_usage | canonical_identifier | origin |
|---|---|---|---|---|---|
| `digitalregulation-qos-qoe` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-06 | `url:https://digitalregulation.org/technical-regulation-quality-of-service/|year:2024` | `ce_candidate` |
| `goodfellow_deep_learning` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-05,ch21,ch22 | `url:https://www.deeplearningbook.org/|year:2016` | `ce_candidate` |
| `gunnchos-technology-landscape-ce06` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-06 | `url:https://github.com/gunnchOS3k/gunnchos-technology-landscape|year:2026` | `ce_candidate` |
| `gunnchosTechnologyLandscape2026` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | book/references,ch02 | `url:https://github.com/gunnchOS3k/gunnchos-technology-landscape|year:2026` | `book_references_accepted_main` |
| `ieee80211-2020` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:ieee80211-2020|dated:2020` | `ce_candidate` |
| `ieee80211-wg` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.ieee802.org/11/|year:2026` | `ce_candidate` |
| `iso-iec-25010-2023` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://www.iso.org/standard/78176.html|year:2023` | `ce_candidate` |
| `itu-t-g1011` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06,ch27 | `url:https://www.itu.int/rec/T-REC-G.1011|year:2016` | `ce_candidate` |
| `itu-t-p10-g100` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://www.itu.int/rec/T-REC-P.10/en` | `ce_candidate` |
| `jedec-jesd79-4d` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://www.jedec.org/standards-documents/docs/jesd79-4a|year:2021` | `ce_candidate` |
| `khronos-vulkan-overview` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://www.khronos.org/vulkan/|year:2026` | `ce_candidate` |
| `kurose-ross-8` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `isbn:9780136681557|edition:8` | `ce_candidate` |
| `linux-cpu-freq` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://docs.kernel.org/admin-guide/pm/cpufreq.html|year:2026` | `ce_candidate` |
| `linux-input` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | book/references,ch02 | `url:https://docs.kernel.org/input/input.html|year:2026` | `book_references_accepted_main` |
| `linux-memory` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://docs.kernel.org/admin-guide/mm/index.html|year:2026` | `ce_candidate` |
| `linux-scheduler` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-03,ch12 | `url:https://docs.kernel.org/scheduler/|year:2026` | `ce_candidate` |
| `linux-scheduler-ce06` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://docs.kernel.org/scheduler/|year:2026` | `ce_candidate` |
| `mdn-network-monitor` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor|year:2026` | `ce_candidate` |
| `mdn-performance` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-01,ce-03,ch14 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance|year:2026` | `ce_candidate` |
| `mdn-performance-ce06` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-06 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance|year:2026` | `ce_candidate` |
| `mdn-resource-timing` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/Resource_timing|year:2026` | `ce_candidate` |
| `nist-sp500-325` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://csrc.nist.gov/pubs/sp/500/325/final|year:2018` | `ce_candidate` |
| `nist-sp800-145` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://csrc.nist.gov/pubs/sp/800/145/final|year:2011` | `ce_candidate` |
| `nist_ai_rmf_100_1` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-05,ch21 | `doi:10.6028/nist.ai.100-1` | `ce_candidate` |
| `nist_sp_800_63_4` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-05,ch23,ch24 | `doi:10.6028/nist.sp.800-63-4` | `ce_candidate` |
| `nvme-base-spec` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-03 | `url:https://nvmexpress.org/specifications/|year:2026` | `ce_candidate` |
| `otel-signals` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://opentelemetry.io/docs/concepts/signals/|year:2026` | `ce_candidate` |
| `patterson-hennessy` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01,ch12 | `title:computer organization and design: the hardware/software interface|author:patterson, david a. and hennessy, john l.|year:2020` | `ce_candidate` |
| `patterson-hennessy-ce06` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `title:computer organization and design: the hardware/software interface|author:patterson, david a. and hennessy, john l.|year:2020` | `ce_candidate` |
| `patterson-hennessy-riscv` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `isbn:9780128203316|edition:2` | `ce_candidate` |
| `rfc1034` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc1034|dated:1987` | `ce_candidate` |
| `rfc1035` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc1035|dated:1987` | `ce_candidate` |
| `rfc1122` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc1122|dated:1989` | `ce_candidate` |
| `rfc1918` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc1918|dated:1996` | `ce_candidate` |
| `rfc3022` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc3022|dated:2001` | `ce_candidate` |
| `rfc768` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc768|dated:1980` | `ce_candidate` |
| `rfc791` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-04,ch16 | `standard:rfc791|dated:1981` | `ce_candidate` |
| `rfc8200` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc8200|dated:2017` | `ce_candidate` |
| `rfc8446` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc8446|dated:2018` | `ce_candidate` |
| `rfc9000` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc9000|dated:2021` | `ce_candidate` |
| `rfc9293` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-04,ch16 | `standard:rfc9293|dated:2022` | `ce_candidate` |
| `russell_norvig_aima` | `textbooks` | `NEEDS_PRIMARY_VERIFICATION` | ce-05,ch21 | `title:artificial intelligence: a modern approach|author:russell, stuart and norvig, peter|year:unknown` | `ce_candidate` |
| `saltzer-kaashoek` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01,ch01,ch11,ch13,ch14 | `isbn:9780123749574|edition:2009` | `ce_candidate` |
| `saltzer_schroeder_1975` | `peer_reviewed` | `PRIMARY_METADATA_VERIFIED` | ce-05,ch23 | `doi:10.1109/proc.1975.9939` | `ce_candidate` |
| `silberschatz-galvin-gagne` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-03,ch12 | `isbn:9781119320913|edition:10` | `ce_candidate` |
| `solove_taxonomy_2006` | `peer_reviewed` | `PRIMARY_METADATA_VERIFIED` | ce-05,ch24 | `title:a taxonomy of privacy|author:solove, daniel j.|year:2006` | `ce_candidate` |
| `src-device-os-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03,ch23,ch29 | `url:https://github.com/gunnchOS3k/gunnchos-device-os|year:2026` | `ce_candidate` |
| `src-hardware-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03,ch22,ch23,ch25,ch26,ch28,ch29 | `url:https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design|year:2026` | `ce_candidate` |
| `src-hardware-quartet` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-01,ch01,ch03,ch04,ch05,ch06,ch07,ch08,ch09,ch10,ch22,ch23,ch25,ch26,ch28,ch29 | `url:https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design|year:2026` | `ce_candidate` |
| `src-waike` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-01,ch02,ch21,ch22,ch23,ch24,ch25,ch26,ch27,ch28,ch30,ch31 | `url:https://github.com/gunnchOS3k/waike-research-ops|year:2026` | `ce_candidate` |
| `src-waike-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03,ch21,ch22,ch23,ch24,ch25,ch26,ch27,ch28,ch30,ch31 | `url:https://github.com/gunnchOS3k/waike-research-ops|year:2026` | `ce_candidate` |
| `tanenbaum-bos` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-03,ch01,ch03,ch06,ch07,ch08,ch11,ch12,ch13 | `title:modern operating systems|author:tanenbaum, andrew s. and bos, herbert|year:2022` | `ce_candidate` |
| `threegpp-ts23501` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:threegpp-ts23501|dated:2026` | `ce_candidate` |
| `w3c-pointerevents` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | book/references,ch02 | `url:https://www.w3.org/TR/pointerevents3/|year:2026` | `book_references_accepted_main` |
| `w3c-uievents` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | book/references,ch02 | `url:https://www.w3.org/TR/uievents/|year:2026` | `book_references_accepted_main` |
| `waike-main-ce4-audit` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `title:waike research-ops accepted main audit for ce-4 crosswalk|author:|year:2026` | `ce_candidate` |
| `waike-research-ops-ce06` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-06,ch21,ch22,ch23,ch24,ch25,ch26,ch27,ch28,ch30,ch31 | `url:https://github.com/gunnchOS3k/waike-research-ops|year:2026` | `ce_candidate` |
| `wcag22-20231005` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01,ch24 | `standard:wcag22-20231005|dated:2023` | `ce_candidate` |
| `wcag22-20241212` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06,ch24,ch25 | `standard:wcag22-20241212|dated:2024` | `ce_candidate` |
| `whatwg-dom` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01,ch01 | `url:https://dom.spec.whatwg.org/|year:2026` | `ce_candidate` |
| `whatwg-html` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01,ch01,ch14 | `url:https://html.spec.whatwg.org/|year:2026` | `ce_candidate` |
| `whatwg-html-ce06` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://html.spec.whatwg.org/|year:2026` | `ce_candidate` |
| `wifi-alliance-discover` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://www.wi-fi.org/discover-wi-fi|year:2026` | `ce_candidate` |

## Integrator merge notes (EVIDENCE-A/B coordination)

- **This agent (EVIDENCE-C)** owns `publication/full31/WORKING_BIBLIOGRAPHY.*` and `scripts/build_full31_working_bibliography.py`. Commits stay focused there.
- **Do not** edit `publication/gates/gate-3/` from this wave.
- **Do not** silently overwrite `book/references/references.bib`. Promotion into the live book bib requires integrator authorization after EVIDENCE-A/B source audits settle.
- **CE candidate** (`publication/preproduction/CANDIDATE_*`, `scripts/validate_ce_sources.py`) remains the Concept Edition integrity truth; regenerate CE artifacts with Agent G tooling before regenerating this working set if CE local bibs change.
- **EVIDENCE-A** (standards / accepted-main source audit under `evidence/`) may add or reclassify standards metadata — merge by regenerating CE candidate first, then re-run this builder; prefer additive updates to `WORKING_BIBLIOGRAPHY_INDEX.yaml` verification fields over hand-editing the `.bib` body.
- **EVIDENCE-B** (if touching chapter SOURCE_NEEDS / CLAIM_PLAN citation_keys): keep dated WCAG keys distinct; never introduce undated `wcag22` as a cite key; map `SRC-*` register IDs via `source_register_alias_map` rather than inventing parallel bib entries.
- **`russell_norvig_aima`** remains `NEEDS_PRIMARY_VERIFICATION` until a primary edition/ISBN/year is verified — do not invent metadata to clear the flag.
- **Quarto integration path:** manuscript chapters may temporarily set `bibliography: ../../publication/full31/WORKING_BIBLIOGRAPHY.bib` (adjust relative path) or cite from a merged live bib once promoted.

## Artifacts

- `publication/full31/WORKING_BIBLIOGRAPHY.bib`
- `publication/full31/WORKING_BIBLIOGRAPHY_INDEX.yaml`
- `publication/full31/WORKING_BIBLIOGRAPHY_REPORT.md` (this file)
- Builder: `scripts/build_full31_working_bibliography.py`
- Upstream validator: `scripts/validate_ce_sources.py`

## Non-goals

- No Gate 3 / CH02-REVIEW-R1 edits
- No Gate 3 PASS
- No unauthorized merge into `book/references/references.bib`
- No invented DOI/ISBN/page/year

