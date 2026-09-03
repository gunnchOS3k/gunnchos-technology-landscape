# Source Integrity Report (Agent G)

**schema_version:** `1.0.0`  
**status:** `CANDIDATE_PREPRODUCTION`  
**gate_note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**scope:** Concept Edition CE-1/3/4/5/6 chapter-local bibliographies  
**global merge:** not authorized — candidate only

## Counts

| Metric | Prior (PR #3 index) | Current |
|---|---:|---:|
| Chapter source occurrences | 64 | 64 |
| Unique source records (bib keys) | 58 | 59 |

### Verification status (unique keys)

| verification_status | count |
|---|---:|
| `NEEDS_PRIMARY_VERIFICATION` | 1 |
| `PRIMARY_METADATA_VERIFIED` | 44 |
| `REPOSITORY_EVIDENCE_VERIFIED` | 7 |
| `SECONDARY_EXPLANATORY` | 7 |

### Classification (unique keys)

| source_class | count |
|---|---:|
| `official_technical_documentation` | 14 |
| `other_explanatory` | 5 |
| `peer_reviewed` | 3 |
| `project_accepted_main` | 7 |
| `standards_specifications` | 21 |
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

- 2020 | computer organization and design: the hardware/software interface -> ['patterson-hennessy', 'patterson-hennessy-ce06']
- 2026 | cpu scheduler -> ['linux-scheduler', 'linux-scheduler-ce06']
- 2026 | html standard -> ['whatwg-html', 'whatwg-html-ce06']
- 2026 | performance api -> ['mdn-performance', 'mdn-performance-ce06']

## Unique records

| bib_key | source_class | verification_status | chapter_usage | canonical_identifier | metadata_conflict_status |
|---|---|---|---|---|---|
| `digitalregulation-qos-qoe` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-06 | `url:https://digitalregulation.org/technical-regulation-quality-of-service/` | `NONE` |
| `goodfellow_deep_learning` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `url:https://www.deeplearningbook.org/` | `NONE` |
| `gunnchos-technology-landscape-ce06` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-06 | `url:https://github.com/gunnchOS3k/gunnchos-technology-landscape` | `NONE` |
| `ieee80211-2020` | `peer_reviewed` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://standards.ieee.org/standard/802_11-2020.html` | `NONE` |
| `ieee80211-wg` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.ieee802.org/11/` | `NONE` |
| `iso-iec-25010-2023` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://www.iso.org/standard/78176.html` | `NONE` |
| `itu-t-g1011` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://www.itu.int/rec/T-REC-G.1011` | `NONE` |
| `itu-t-p10-g100` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://www.itu.int/rec/T-REC-P.10/en` | `NONE` |
| `jedec-jesd79-4d` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://www.jedec.org/standards-documents/docs/jesd79-4a` | `NONE` |
| `khronos-vulkan-overview` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://www.khronos.org/vulkan/` | `NONE` |
| `kurose-ross-8` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `isbn:9780136681557` | `NONE` |
| `linux-cpu-freq` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://docs.kernel.org/admin-guide/pm/cpufreq.html` | `NONE` |
| `linux-memory` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `url:https://docs.kernel.org/admin-guide/mm/index.html` | `NONE` |
| `linux-scheduler` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-03 | `url:https://docs.kernel.org/scheduler/` | `NONE` |
| `linux-scheduler-ce06` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://docs.kernel.org/scheduler/` | `NONE` |
| `mdn-network-monitor` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor` | `NONE` |
| `mdn-performance` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-01,ce-03 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance` | `NONE` |
| `mdn-performance-ce06` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-06 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance` | `NONE` |
| `mdn-resource-timing` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/Resource_timing` | `NONE` |
| `nist-sp500-325` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://csrc.nist.gov/pubs/sp/500/325/final` | `NONE` |
| `nist-sp800-145` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://csrc.nist.gov/pubs/sp/800/145/final` | `NONE` |
| `nist_ai_rmf_100_1` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `doi:10.6028/NIST.AI.100-1` | `NONE` |
| `nist_sp_800_63_4` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `doi:10.6028/NIST.SP.800-63-4` | `NONE` |
| `nvme-base-spec` | `official_technical_documentation` | `SECONDARY_EXPLANATORY` | ce-03 | `url:https://nvmexpress.org/specifications/` | `NONE` |
| `otel-signals` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://opentelemetry.io/docs/concepts/signals/` | `NONE` |
| `patterson-hennessy` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `key:patterson-hennessy` | `NONE` |
| `patterson-hennessy-ce06` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `key:patterson-hennessy-ce06` | `NONE` |
| `patterson-hennessy-riscv` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `isbn:9780128203316` | `NONE` |
| `rfc1034` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc1034` | `NONE` |
| `rfc1035` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc1035` | `NONE` |
| `rfc1122` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc1122` | `NONE` |
| `rfc1918` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc1918` | `NONE` |
| `rfc3022` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc3022` | `NONE` |
| `rfc768` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc768` | `NONE` |
| `rfc791` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-04 | `url:https://www.rfc-editor.org/rfc/rfc791` | `NONE` |
| `rfc8200` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc8200` | `NONE` |
| `rfc8446` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc8446` | `NONE` |
| `rfc9000` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://www.rfc-editor.org/rfc/rfc9000` | `NONE` |
| `rfc9293` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-04 | `url:https://www.rfc-editor.org/rfc/rfc9293` | `NONE` |
| `russell_norvig_aima` | `textbooks` | `NEEDS_PRIMARY_VERIFICATION` | ce-05 | `key:russell_norvig_aima` | `NONE` |
| `saltzer-kaashoek` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `isbn:9780123749574` | `NONE` |
| `saltzer_schroeder_1975` | `peer_reviewed` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `doi:10.1109/PROC.1975.9939` | `NONE` |
| `silberschatz-galvin-gagne` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-03 | `isbn:9781119320913` | `NONE` |
| `solove_taxonomy_2006` | `peer_reviewed` | `PRIMARY_METADATA_VERIFIED` | ce-05 | `key:solove_taxonomy_2006` | `NONE` |
| `src-device-os-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03 | `url:https://github.com/gunnchOS3k/gunnchos-device-os` | `NONE` |
| `src-hardware-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03 | `url:https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design` | `NONE` |
| `src-hardware-quartet` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-01 | `url:https://github.com/gunnchOS3k/gunnchos-hardware-industrial-design` | `NONE` |
| `src-waike` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-01 | `url:https://github.com/gunnchOS3k/waike-research-ops` | `NONE` |
| `src-waike-ce3` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-03 | `url:https://github.com/gunnchOS3k/waike-research-ops` | `NONE` |
| `tanenbaum-bos` | `textbooks` | `PRIMARY_METADATA_VERIFIED` | ce-01,ce-03 | `key:tanenbaum-bos` | `NONE` |
| `threegpp-ts23501` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `url:https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=3144` | `NONE` |
| `waike-main-ce4-audit` | `other_explanatory` | `PRIMARY_METADATA_VERIFIED` | ce-04 | `howpublished:Git commit` | `NONE` |
| `waike-research-ops-ce06` | `project_accepted_main` | `REPOSITORY_EVIDENCE_VERIFIED` | ce-06 | `url:https://github.com/gunnchOS3k/waike-research-ops` | `NONE` |
| `wcag22-20231005` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://www.w3.org/TR/2023/REC-WCAG22-20231005/` | `NONE` |
| `wcag22-20241212` | `standards_specifications` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://www.w3.org/TR/2024/REC-WCAG22-20241212/` | `NONE` |
| `whatwg-dom` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://dom.spec.whatwg.org/` | `NONE` |
| `whatwg-html` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-01 | `url:https://html.spec.whatwg.org/` | `NONE` |
| `whatwg-html-ce06` | `official_technical_documentation` | `PRIMARY_METADATA_VERIFIED` | ce-06 | `url:https://html.spec.whatwg.org/` | `NONE` |
| `wifi-alliance-discover` | `other_explanatory` | `SECONDARY_EXPLANATORY` | ce-04 | `url:https://www.wi-fi.org/discover-wi-fi` | `NONE` |

## Artifacts

- `publication/preproduction/CANDIDATE_BIBLIOGRAPHY.bib`
- `publication/preproduction/CANDIDATE_SOURCE_INDEX.yaml` (regenerated + verification overlay)
- `publication/preproduction/SOURCE_INTEGRITY_REPORT.md` (this file)
- Validator: `scripts/validate_ce_sources.py`

## Non-goals

- No Gate 3 / CH02-REVIEW-R1 edits
- No Gate 3 PASS
- No merge into `book/references/references.bib`

