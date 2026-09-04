# Source Integrity Report (Agent G)

**schema_version:** `1.0.0`  
**status:** `CANDIDATE_PREPRODUCTION`  
**gate_note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**scope:** Concept Edition CE-1/3/4/5/6 chapter-local bibliographies  
**global merge:** not authorized — candidate only

## Counts

| Metric | Prior (PR #3 index) | Current |
|---|---:|---:|
| Chapter source occurrences | 64 | 81 |
| Unique bib keys | 58 | 76 |
| Unique canonical works | — | 69 |
| Same-work aliases (canonical grouping) | — | 10 |

Canonical-work grouping priority: DOI → ISBN+edition → dated standards/RFC → URL+dated edition → repo+commit+role → title/author/year uncertain fallback. The two WCAG dated Recommendations remain distinct works.

### Verification status (unique keys)

| verification_status | count |
|---|---:|
| `NEEDS_PRIMARY_VERIFICATION` | 1 |
| `PRIMARY_METADATA_VERIFIED` | 61 |
| `REPOSITORY_EVIDENCE_VERIFIED` | 7 |
| `SECONDARY_EXPLANATORY` | 7 |

### Classification (unique keys)

| source_class | count |
|---|---:|
| `official_technical_documentation` | 17 |
| `other_explanatory` | 13 |
| `peer_reviewed` | 2 |
| `project_accepted_main` | 7 |
| `standards_specifications` | 28 |
| `textbooks` | 9 |

## WCAG 2.2 conflict resolution

PR #3 flagged `wcag22` with year `2023` (CE-1) vs `2024` (CE-6) sharing `https://www.w3.org/TR/WCAG22/`.

W3C primary history ([WCAG22 publication history](https://www.w3.org/standards/history/WCAG22/)) lists two Recommendation editions:

| Edition date | Status | Dated TR URL | Bib key |
|---|---|---|---|
| 5 October 2023 | Recommendation | https://www.w3.org/TR/2023/REC-WCAG22-20231005/ | `wcag22-20231005` |
| 12 December 2024 | Recommendation | https://www.w3.org/TR/2024/REC-WCAG22-20241212/ | `wcag22-20241212` |

**Resolution:** two explicit bib keys (not a silent overwrite). The undated shortcut `/TR/WCAG22/` is the “latest published version” pointer and currently resolves to the 2024-12-12 Recommendation; it must not be used as the sole canonical URL when chapters intentionally cite different dated editions.

## Conflicts

### Resolved

- `wcag22` year 2023 vs 2024 → split into `wcag22-20231005` (CE-1) and `wcag22-20241212` (CE-6) with dated TR URLs.
- `rfc9293` title brace variance (`{TCP}` vs `TCP`) treated as non-semantic (normalized titles match); no separate keys required.

### Remaining / informational

- Duplicate key + conflicting metadata: **none**
- Duplicate DOI across keys: **none**
- Duplicate ISBN across keys: **none**
- Same URL with conflicting date across unique keys: **none** (after WCAG split)
- Same URL with chapter-local title aliases (informational, not hard conflicts):
  - https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design: keys=['src-hardware-ce3', 'src-hardware-quartet'] titles=['gunnchos-hardware-industrial-design accepted main (ce-3 audit)', 'gunnchos-hardware-industrial-design device quartet docs']
  - https://github.com/gunnchOS3k/waike-research-ops: keys=['src-waike', 'src-waike-ce3', 'waike-research-ops-ce06'] titles=['waike-research-ops accepted main (ce-3 audit)', 'waike-research-ops accepted main audit for ce-1 adjacency', 'waike-research-ops accepted main curriculum evidence']
- Missing verification state: **none**

### Same-work chapter-local aliases (not conflicts)

- title:computer organization and design: the hardware/software interface|author:patterson, david a. and hennessy, john l.|year:2020 -> ['patterson-hennessy', 'patterson-hennessy-ce06']
- url:https://developer.mozilla.org/en-US/docs/Web/API/Performance|year:2026 -> ['mdn-performance', 'mdn-performance-ce06']
- url:https://docs.kernel.org/scheduler/|year:2026 -> ['linux-scheduler', 'linux-scheduler-ce06']
- url:https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design|year:2026 -> ['src-hardware-ce3', 'src-hardware-quartet']
- url:https://github.com/gunnchOS3k/waike-research-ops|year:2026 -> ['src-waike', 'src-waike-ce3', 'waike-research-ops-ce06']
- url:https://html.spec.whatwg.org/|year:2026 -> ['whatwg-html', 'whatwg-html-ce06']
- 2020 | computer organization and design: the hardware/software interface -> ['patterson-hennessy', 'patterson-hennessy-ce06']
- 2026 | cpu scheduler -> ['linux-scheduler', 'linux-scheduler-ce06']
- 2026 | html standard -> ['whatwg-html', 'whatwg-html-ce06']
- 2026 | performance api -> ['mdn-performance', 'mdn-performance-ce06']

## Unique records

| bib_key | source_class | verification_status | chapter_usage | canonical_identifier | metadata_conflict_status |
|---|---|---|---|---|---|
| `android-ab-ota` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `url:https://source.android.com/docs/core/ota/ab|year:2026` | `NONE` |
| `digitalregulation-qos-qoe` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-06 | `url:https://digitalregulation.org/technical-regulation-quality-of-service/|year:2024` | `NONE` |
| `git-scm-docs` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://git-scm.com/docs|year:2026` | `NONE` |
| `goodfellow_deep_learning` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `url:https://www.deeplearningbook.org/|year:2016` | `NONE` |
| `gunnchos-technology-landscape-ce06` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-06 | `url:https://github.com/gunnchOS3k/gunnchos-technology-landscape|year:2026` | `NONE` |
| `iec-62133-2` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://webstore.iec.ch/en/publication/70017|year:2017` | `NONE` |
| `ieee80211-2020` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:ieee80211-2020|dated:2020` | `NONE` |
| `ieee80211-wg` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.ieee802.org/11/|year:2026` | `NONE` |
| `iso-23247-1-2021` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://www.iso.org/standard/75066.html|year:2021` | `NONE` |
| `iso-iec-25010-2023` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://www.iso.org/standard/78176.html|year:2023` | `NONE` |
| `itu-facts-figures-2025` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://www.itu.int/en/ITU-D/Statistics/Pages/facts/default.aspx|year:2025` | `NONE` |
| `itu-r-m2160-2023` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.itu.int/rec/R-REC-M.2160-0-202311-I/en|year:2023` | `NONE` |
| `itu-t-g1011` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://www.itu.int/rec/T-REC-G.1011|year:2016` | `NONE` |
| `itu-t-p10-g100` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://www.itu.int/rec/T-REC-P.10/en` | `NONE` |
| `jedec-jesd79-4d` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://www.jedec.org/standards-documents/docs/jesd79-4a|year:2021` | `NONE` |
| `khronos-vulkan-overview` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://www.khronos.org/vulkan/|year:2026` | `NONE` |
| `kurose-ross-8` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `isbn:9780136681557|edition:8` | `NONE` |
| `linux-cpu-freq` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://docs.kernel.org/admin-guide/pm/cpufreq.html|year:2026` | `NONE` |
| `linux-memory` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://docs.kernel.org/admin-guide/mm/index.html|year:2026` | `NONE` |
| `linux-scheduler` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-03 | `url:https://docs.kernel.org/scheduler/|year:2026` | `NONE` |
| `linux-scheduler-ce06` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://docs.kernel.org/scheduler/|year:2026` | `NONE` |
| `mdn-network-monitor` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor|year:2026` | `NONE` |
| `mdn-performance` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-01,ce-03 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance|year:2026` | `NONE` |
| `mdn-performance-ce06` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-06 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance|year:2026` | `NONE` |
| `mdn-requestanimationframe` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame|year:2026` | `NONE` |
| `mdn-resource-timing` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/Resource_timing|year:2026` | `NONE` |
| `nist-sp500-325` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://csrc.nist.gov/pubs/sp/500/325/final|year:2018` | `NONE` |
| `nist-sp800-145` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://csrc.nist.gov/pubs/sp/800/145/final|year:2011` | `NONE` |
| `nist-sp800-88r1` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `url:https://csrc.nist.gov/pubs/sp/800/88/r1/final|year:2014` | `NONE` |
| `nist_ai_rmf_100_1` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `doi:10.6028/nist.ai.100-1` | `NONE` |
| `nist_sp_800_63_4` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `doi:10.6028/nist.sp.800-63-4` | `NONE` |
| `nvme-base-spec` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-03 | `url:https://nvmexpress.org/specifications/|year:2026` | `NONE` |
| `oci-runtime-spec` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://raw.githubusercontent.com/opencontainers/runtime-spec/main/spec.md|year:2026` | `NONE` |
| `otel-signals` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://opentelemetry.io/docs/concepts/signals/|year:2026` | `NONE` |
| `patterson-hennessy` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `title:computer organization and design: the hardware/software interface|author:patterson, david a. and hennessy, john l.|year:2020` | `NONE` |
| `patterson-hennessy-ce06` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `title:computer organization and design: the hardware/software interface|author:patterson, david a. and hennessy, john l.|year:2020` | `NONE` |
| `patterson-hennessy-riscv` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `isbn:9780128203316|edition:2` | `NONE` |
| `postgresql-mvcc` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `url:https://www.postgresql.org/docs/current/mvcc.html|year:2026` | `NONE` |
| `rfc1034` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc1034|dated:1987` | `NONE` |
| `rfc1035` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc1035|dated:1987` | `NONE` |
| `rfc1122` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc1122|dated:1989` | `NONE` |
| `rfc1918` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc1918|dated:1996` | `NONE` |
| `rfc3022` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc3022|dated:2001` | `NONE` |
| `rfc768` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc768|dated:1980` | `NONE` |
| `rfc791` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-04 | `standard:rfc791|dated:1981` | `NONE` |
| `rfc8200` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc8200|dated:2017` | `NONE` |
| `rfc8446` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc8446|dated:2018` | `NONE` |
| `rfc9000` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:rfc9000|dated:2021` | `NONE` |
| `rfc9293` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-04 | `standard:rfc9293|dated:2022` | `NONE` |
| `russell_norvig_aima` | `textbooks` | `NEEDS_PRIMARY_VERIFICATION` | ce-05 | `title:artificial intelligence: a modern approach|author:russell, stuart and norvig, peter|year:unknown` | `NONE` |
| `saltzer-kaashoek` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `isbn:9780123749574|edition:2009` | `NONE` |
| `saltzer_schroeder_1975` | `peer_reviewed` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `doi:10.1109/proc.1975.9939` | `NONE` |
| `semver-2.0.0` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://semver.org/spec/v2.0.0.html` | `NONE` |
| `silberschatz-galvin-gagne` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `isbn:9781119320913|edition:10` | `NONE` |
| `solove_taxonomy_2006` | `peer_reviewed` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `title:a taxonomy of privacy|author:solove, daniel j.|year:2006` | `NONE` |
| `src-device-os-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03 | `url:https://github.com/gunnchOS3k/gunnchos-device-os|year:2026` | `NONE` |
| `src-hardware-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03 | `url:https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design|year:2026` | `NONE` |
| `src-hardware-quartet` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-01 | `url:https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design|year:2026` | `NONE` |
| `src-waike` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-01 | `url:https://github.com/gunnchOS3k/waike-research-ops|year:2026` | `NONE` |
| `src-waike-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03 | `url:https://github.com/gunnchOS3k/waike-research-ops|year:2026` | `NONE` |
| `tanenbaum-bos` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-03 | `title:modern operating systems|author:tanenbaum, andrew s. and bos, herbert|year:2022` | `NONE` |
| `tcg-pc-client-pfp-1.06` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `url:https://trustedcomputinggroup.org/wp-content/uploads/TCG-PC-Client-Platform-Firmware-Profile-Version-1.06-Revision-52_pub-3.pdf|year:2023` | `NONE` |
| `threegpp-tr38821` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:threegpp-tr38821|dated:2023` | `NONE` |
| `threegpp-ts23501` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `standard:threegpp-ts23501|dated:2026` | `NONE` |
| `uefi-secure-boot-2.10` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `url:https://uefi.org/specs/UEFI/2.10/32_Secure_Boot_and_Driver_Signing.html` | `NONE` |
| `ul-2054` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://www.shopulstandards.com/ProductDetail.aspx?productId=UL2054|year:2021` | `NONE` |
| `w3c-mediacapture-streams-20251009` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://www.w3.org/TR/mediacapture-streams/|year:2025` | `NONE` |
| `w3c-permissions-20251006` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://www.w3.org/TR/2025/WD-permissions-20251006/|year:2025` | `NONE` |
| `waike-main-ce4-audit` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `title:waike research-ops accepted main audit for ce-4 crosswalk|author:|year:2026` | `NONE` |
| `waike-research-ops-ce06` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-06 | `url:https://github.com/gunnchOS3k/waike-research-ops|year:2026` | `NONE` |
| `wcag22-20231005` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `standard:wcag22-20231005|dated:2023` | `NONE` |
| `wcag22-20241212` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `standard:wcag22-20241212|dated:2024` | `NONE` |
| `whatwg-dom` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://dom.spec.whatwg.org/|year:2026` | `NONE` |
| `whatwg-html` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://html.spec.whatwg.org/|year:2026` | `NONE` |
| `whatwg-html-ce06` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://html.spec.whatwg.org/|year:2026` | `NONE` |
| `wifi-alliance-discover` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://www.wi-fi.org/discover-wi-fi|year:2026` | `NONE` |

## Artifacts

- `publication/preproduction/CANDIDATE_BIBLIOGRAPHY.bib`
- `publication/preproduction/CANDIDATE_SOURCE_INDEX.yaml` (regenerated + verification overlay)
- `publication/preproduction/SOURCE_INTEGRITY_REPORT.md` (this file)
- Validator: `scripts/validate_ce_sources.py`

## Non-goals

- No Gate 3 / CH02-REVIEW-R1 edits
- No Gate 3 PASS
- No merge into `book/references/references.bib`

