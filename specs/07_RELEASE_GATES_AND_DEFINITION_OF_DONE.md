# Release Gates and Definition of Done

This file converts the publication roadmap into explicit gates.

No gate may be claimed because a checklist file exists.

Evidence must exist.

---

# Gate 0 — Charter

## Completion evidence

- title approved,
- audience defined,
- book promise defined,
- scope defined,
- voice defined,
- status language defined,
- licensing policy defined,
- author/contributor policy defined.

## Automatable?

Mostly.

Final editorial approval remains an author decision.

---

# Gate 1 — Content architecture

## Completion evidence

- full table of contents,
- 31 chapter registry,
- Concept Edition definition,
- prerequisite graph,
- Device Quartet map,
- WAIKE map,
- glossary schema,
- chapter schema,
- lab schema,
- source-of-truth rules reviewed.

## Automatable?

Mostly.

Exact WAIKE mappings must be evidence-based.

---

# Gate 2 — Visual prototype

## Completion evidence

At minimum:

- one exploded view,
- one end-to-end experience map,
- one component-card set,
- accessibility check pass.

Additional preferred prototype assets:

- sequence diagram,
- software stack,
- network path,
- Stability Contract visual.

## Automatable?

Asset generation and checks may be automated.

Human visual review still required before publication.

---

# Gate 3 — Chapter prototype

## Completion evidence

- one complete chapter,
- real prose rather than outline,
- integrated figures,
- integrated glossary,
- integrated WAIKE lab,
- lab works on baseline route,
- at least three reader levels meaningfully represented,
- evidence/citations integrated,
- technical review checklist complete.

Canonical chapter:

> Chapter 2 — Follow One Tap Through the Entire Stack

## Automatable?

Much of the build can be automated.

Real reader-level testing and final editorial acceptance are human gates.

---

# Gate 4 — Concept Edition

## Completion evidence

All six modules complete:

1. Technology Is a System, Not a Screen
2. Follow One Tap Through the Entire Stack
3. CPU, Memory, Storage, and the OS
4. Packets, Wi-Fi/Cellular, Edge and Cloud
5. AI, Security, Privacy and Trust
6. The Stability Contract + Capstone

Also requires:

- integrated glossary,
- lab pack,
- source register,
- technical review,
- copy edit,
- PDF,
- EPUB,
- accessible preview.

## Automatable?

Large portion.

Technical review and copy-edit acceptance require humans.

---

# Gate 5 — Field validation

## Completion evidence

Documented evidence for:

- learner comprehension,
- lab completion,
- educator usability,
- revision decisions.

Test groups should include multiple reader types.

## Automatable?

No.

Cursor can create test protocols and data forms.

It cannot fabricate reader evidence.

---

# Gate 6 — Full manuscript

## Completion evidence

- all planned chapters substantive,
- citations complete,
- permissions complete,
- figures complete,
- index complete,
- appendices complete,
- glossary complete,
- errata workflow operational.

## Automatable?

Large portions can be assisted.

Editorial/technical acceptance remains human.

---

# Gate 7 — Production

## Completion evidence

- ISBN/imprint decision,
- trim specification,
- color specification,
- print proof,
- EPUB accessibility review,
- distribution metadata,
- release metadata,
- final cover approval.

## Automatable?

Preparation can be automated.

ISBN registration, physical proof approval, and distribution submissions are external actions.

---

# Publication status vocabulary

Use exact language.

Recommended overall statuses:

- `ARCHITECTURE_IN_PROGRESS`
- `GATE_0_READY_FOR_AUTHOR_APPROVAL`
- `GATE_1_PASS`
- `GATE_2_PASS`
- `GATE_3_PASS`
- `CONCEPT_EDITION_IN_PROGRESS`
- `GATE_4_PASS`
- `FIELD_VALIDATION_PENDING`
- `GATE_5_PASS`
- `FULL_MANUSCRIPT_IN_PROGRESS`
- `GATE_6_PASS`
- `PRODUCTION_PREP`
- `GATE_7_PASS`
- `PUBLISHED`

Do not use `PUBLISHED` before a real edition is actually published.

---

# First-wave expected ceiling

The first Cursor implementation wave should aim for:

- Gate 0 artifacts,
- Gate 1 infrastructure,
- Gate 2 visual prototype,
- substantial progress toward Gate 3,
- ideally Gate 3 if the chapter and baseline lab are genuinely complete.

Do **not** force a Gate 3 PASS.

A truthful:

`GATE_2_PASS — GATE_3_IN_PROGRESS`

is better than a fabricated PASS.

---

# Gate evidence storage

Recommended:

```text
publication/gates/
  gate-0/
    checklist.md
    evidence.yaml
  gate-1/
    checklist.md
    evidence.yaml
  ...
```

`evidence.yaml` should identify exact artifacts satisfying each requirement.

---

# CI gate checks

Automate what can be automated.

Examples:

## Gate 1 automated checks

- all 31 chapter records exist,
- Concept Edition registry valid,
- chapter schema valid,
- glossary schema valid,
- Device Quartet records valid.

## Gate 2 automated checks

- required prototype figure assets exist,
- editable sources exist,
- alt text exists,
- long description exists.

## Gate 3 automated checks

- Chapter 2 file exists,
- required 12 sections detected,
- lab record valid,
- glossary references resolve,
- figure refs resolve,
- citations resolve,
- claim registry passes.

Do not let automation claim that prose is pedagogically excellent.

That requires review.

---

# External/owner gate categories

Cursor should only stop for real non-automatable dependencies.

Examples:

- author approves title/subtitle changes,
- author approves editorial voice changes,
- physical device measurement,
- independent technical review,
- learner study,
- educator usability study,
- permission from third-party rights holder,
- ISBN purchase/assignment,
- imprint decision,
- print proof inspection,
- distributor/storefront registration.

Do not misclassify ordinary coding or writing as an owner blocker.

---

# Definition of release candidate

A build artifact is not a release candidate merely because PDF generation succeeds.

A publication candidate requires:

- reviewed content,
- reviewed visuals,
- valid citations,
- evidence integrity,
- accessibility,
- permissions,
- consistent metadata,
- no unresolved critical placeholders,
- reproducible build.

---

# Errata system

Before public release, establish:

- issue template for errors,
- edition/version identifier,
- chapter mapping,
- correction severity,
- correction log,
- release-note policy.

The project is intended to evolve with technology.

Versioning is a feature, not an admission of failure.
