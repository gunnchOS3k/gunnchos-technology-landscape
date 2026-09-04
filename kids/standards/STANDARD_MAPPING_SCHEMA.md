# Standard Mapping Schema — Kids Global Standards Atlas

**Track:** Kids Global Standards Atlas (K2–K7 / B5–B10 / B8–B10)  
**Publication family:** Technology Landscape Kids Edition foundation  
**Status vocabulary for this track:** `DRAFT_INTERNAL` (not PUBLICATION_READY)

## Purpose

Machine-readable architecture for **crosswalking** early-years / primary technology-and-STEM learning expectations across world jurisdictions — without claiming official alignment, certification, or wholesale reproduction of copyrighted standards text.

## Hard rules

1. **Official sources only** for standards identity (authority landing page, statutory instrument, ministry curriculum portal).
2. Every source row carries: `retrieved_on`, `version` (or `SOURCE_VERSION_UNCLEAR`), `url`, `authority`.
3. Prefer relationship verbs: `CROSSWALKED_AGAINST` | `MAPPED_TO` | `INFORMED_BY`.  
   **Never** claim: officially aligned, certified, endorsed, or adopted by the authority unless the authority’s own document states that fact — and even then record it as a *jurisdiction adoption claim*, not a Kids Edition certification.
4. Do **not** paste copyrighted standards wholesale. Summarize at domain / strand / competency-family grain only.
5. Honest gaps beat fabricated maps: `TRANSLATION_REQUIRED`, `ACCESS_BLOCKED`, `NOT_YET_RESEARCHED`, `SOURCE_VERSION_UNCLEAR`.

## Artifact set

| File | Role |
| --- | --- |
| `GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml` | Exhaustive jurisdiction census (national + key subnational education authorities) |
| `GLOBAL_STANDARDS_SOURCE_REGISTER.yaml` | Official framework / curriculum sources with retrieval metadata |
| `GLOBAL_STANDARDS_ATLAS.yaml` | Crosswalk nodes + mapping edges to Kids Edition learning targets |
| `GLOBAL_STANDARDS_COVERAGE_REPORT.md` | Metrics + mandatory framework status + honest gaps |
| `regional/*.yaml` | Region-scoped notes / priority queues (optional detail) |

## Enumerations

### Jurisdiction research status

| Code | Meaning |
| --- | --- |
| `OFFICIAL_SOURCE_VERIFIED` | Official source URL retrieved; version/date recorded (Track 2 preferred) |
| `OFFICIAL_VERIFIED` | Legacy alias of `OFFICIAL_SOURCE_VERIFIED` (still counted) |
| `OFFICIAL_PORTAL_IDENTIFIED` | Official education authority portal confirmed; framework PDF/edition pin may remain pending |
| `IDENTIFIED` | Legacy lighter identification (prefer `OFFICIAL_PORTAL_IDENTIFIED` going forward) |
| `TRANSLATION_REQUIRED` | Official source exists primarily in non-English; translation/review needed |
| `ACCESS_BLOCKED` | Known official source behind paywall, geo-block, or login |
| `NOT_YET_RESEARCHED` | Jurisdiction listed for coverage architecture; research not started |
| `SOURCE_VERSION_UNCLEAR` | Source found but edition/effective date ambiguous |
| `NO_CENTRAL_NATIONAL_CURRICULUM` | Education authority is primarily subnational; no single national K–12 curriculum |
| `SUBNATIONAL_RESEARCH_REQUIRED` | National instrument exists but provinces/states/networks still need row-level research |

### Mapping fidelity

| Code | Meaning |
| --- | --- |
| `EXACT` | Same observable competency family at comparable age band (still not “certified”) |
| `ADJACENT` | Related domain; age band or grain differs |
| `PROPOSED` | Working hypothesis for editorial use; needs SME review |
| `NO_MAP` | Explicitly no sensible map after review |
| `NOT_YET_MAPPED` | Source may exist; mapping work not done |

### Relationship type

| Code | Meaning |
| --- | --- |
| `CROSSWALKED_AGAINST` | Bidirectional editorial comparison table exists or is planned |
| `MAPPED_TO` | One-way map from jurisdiction node → Kids Edition target |
| `INFORMED_BY` | Kids Edition design drew high-level inspiration; not a claim of congruence |

### Framework class

`EARLY_YEARS` | `PRIMARY` | `K12_CS` | `K12_SCIENCE` | `DIGITAL_COMPETENCE` | `AI_COMPETENCE` | `TRANSVERSAL` | `OTHER`

### Age / stage bands (Kids Edition)

Approximate editorial bands (not jurisdiction labels):

| Band | Approx. ages | Notes |
| --- | --- | --- |
| `K2` | ~2–3 | Toddler / very early |
| `K3` | ~3–4 | Preschool |
| `K4` | ~4–5 | Pre-K / reception-adjacent |
| `K5` | ~5–6 | Kindergarten / Year 1 entry |
| `K6` | ~6–7 | Early primary |
| `K7` | ~7–8 | Early primary |
| `B5`–`B10` | ~5–10 | Bridge primary STEM/CS |
| `B8`–`B10` | ~8–10 | Upper early-primary CS/digital |

## YAML shapes

### Jurisdiction registry entry

```yaml
jurisdiction_id: "JUR-CA-ON"          # stable ID
iso3166_1: "CA"                       # null for purely subnational without country? always set parent
iso3166_2: "CA-ON"                    # optional
name: "Ontario"
name_local: null
level: national | subnational | transnational | institutional
parent_jurisdiction_id: "JUR-CA"      # optional
region: americas | europe | africa | middle_east | asia_pacific | global
education_authority: "Ontario Ministry of Education"
research_status: OFFICIAL_VERIFIED
notes: "..."
framework_ids: ["FW-CA-ON-KINDERGARTEN-2016"]
last_reviewed_on: "2026-09-03"
```

### Source register entry

```yaml
framework_id: "FW-UNESCO-AI-STUDENTS-2024"
title: "AI competency framework for students"
authority: "UNESCO"
framework_class: AI_COMPETENCE
version: "2024"
effective_from: "2024-08-08"
url: "https://www.unesco.org/en/articles/ai-competency-framework-students"
license_note: "UNESCO copyright; do not paste wholesale"
retrieved_on: "2026-09-03"
verification: OFFICIAL_VERIFIED
jurisdiction_ids: ["JUR-GLOBAL-UNESCO"]
language: ["en"]
age_relevance: ["K5", "K6", "K7", "B5", "B6", "B7", "B8", "B9", "B10"]
summary_domains: ["human-centred mindset", "ethics of AI", "..."]
gaps: []
```

### Atlas mapping edge

```yaml
mapping_id: "MAP-CSTA2026-ALGO-K5"
relationship: CROSSWALKED_AGAINST
fidelity: ADJACENT
from_framework_id: "FW-CSTA-PK12-2026"
from_node: "Algorithms & Design (PK/K–early primary grain)"
to_kids_target_id: "KE-TARGET-ALGO-FOUNDATIONS"
kids_bands: ["K5", "K6"]
notes: "Editorial crosswalk only; not CSTA-certified."
reviewed_on: "2026-09-03"
```

### Kids Edition target (atlas node)

```yaml
kids_target_id: "KE-TARGET-ALGO-FOUNDATIONS"
label: "Algorithmic thinking foundations"
bands: ["K4", "K5", "K6", "K7"]
description: "Sequences, patterns, stepwise instructions in play — not formal CS theory."
```

## Validation invariants

1. Every `framework_id` referenced by a jurisdiction or mapping exists in the source register.
2. Every `jurisdiction_id` referenced by a framework exists in the jurisdiction registry.
3. `OFFICIAL_VERIFIED` rows must have non-empty `url`, `authority`, `retrieved_on`, and `version` **or** explicit `SOURCE_VERSION_UNCLEAR` in `gaps`.
4. Mapping `fidelity` must be one of the enum values; `EXACT`/`ADJACENT`/`PROPOSED` require a non-empty `notes` disclaiming certification.
5. Forbidden claim tokens in notes/titles: `officially aligned`, `certified against`, `accredited to` (case-insensitive) unless preceded by `AUTHORITY_CLAIMS:` quote stub (still no wholesale paste).

## Make target

```bash
make kids-standards-check
```

Runs `scripts/validate_kids_standards.py` and unit tests under `tests/test_kids_standards.py`.
