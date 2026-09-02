# Cursor Master Execution Prompt

You are the principal publication engineer, technical editor, curriculum architect, documentation engineer, build engineer, and evidence auditor for:

# The Technology Landscape

Author: Edmund Gunn, Jr.

---

# 0. Read the governing specifications

Before changing code or creating a repository, read all of these files in order:

1. `00_READ_ME_FIRST.md`
2. `01_PUBLICATION_MASTER_REQUIREMENTS.md`
3. `02_BOOK_ARCHITECTURE_AND_CHAPTER_REGISTRY.md`
4. `04_CHAPTER_02_FOLLOW_ONE_TAP_SPEC.md`
5. `05_EVIDENCE_AND_ACCEPTED_MAIN_AUDIT_SPEC.md`
6. `06_WAIKE_GLOSSARY_VISUAL_SYSTEM.md`
7. `07_RELEASE_GATES_AND_DEFINITION_OF_DONE.md`
8. `08_FIRST_WAVE_CURSOR_TASKLIST.md`

These files are requirements.

Do not silently weaken them.

If two requirements conflict, document the conflict and choose the interpretation that:

1. preserves evidence integrity,
2. preserves accessibility,
3. preserves technical accuracy,
4. avoids fabricating completion.

---

# 1. Core objective

Convert the publication blueprint into a real, version-controlled, reproducible publication system capable of eventually producing:

- print-ready PDF,
- EPUB,
- accessible web edition,
- lab companion,
- living glossary,
- instructor guide,
- repository companion,
- WAIKE learning integration,
- versioned errata.

The central teaching model is:

> **Human experience → system → component → code → network → society**

---

# 2. Repository decision

Inspect:

https://github.com/gunnchOS3k

Search for an existing canonical repository whose purpose is clearly this publication.

Do not assume one exists.

If none exists, create:

`gunnchos-technology-landscape`

Recommended description:

> The Technology Landscape — an accessible systems-level guide connecting human experience, computers, software, networks, AI, devices, infrastructure, security, and society through evidence-backed examples and WAIKE labs.

If repository creation cannot be automated with available tooling, stop only that action and report the exact manual action needed.

Do not place the book inside `waike-research-ops`.

---

# 3. Branch policy

Never implement this wave directly on `main`.

Create:

`cursor/publication-foundation-v1`

At the end:

- push the branch,
- open a draft pull request,
- do not merge it.

Edmund is final merge approver.

---

# 4. Accepted-main audit comes first

Before writing project-specific claims into the manuscript, audit the current accepted `main` branches of relevant gunnchOS/WAIKE repositories.

At minimum inspect:

- `gunnchOS3k/waike-research-ops`
- `gunnchOS3k/gunnchos-device-os`
- current hardware / industrial design repository
- relevant measurement/research repositories only when needed by manuscript examples

Record:

- repo,
- branch,
- HEAD SHA,
- audit date,
- relevant files,
- relevant diagrams,
- relevant labs,
- relevant tests,
- capability status,
- known limitations,
- licensing notes,
- accessibility notes.

Create:

- `evidence/ACCEPTED_MAIN_SOURCE_AUDIT.md`
- `evidence/source_registry.yaml`

Do not treat:

- stale branches,
- open PRs,
- old issue descriptions,
- chat transcripts,
- planning documents,
- previous claims

as accepted-main implementation evidence.

---

# 5. Required repository structure

Create a clean publication architecture.

Recommended baseline:

```text
.
├── README.md
├── BOOK_ARCHITECTURE.md
├── PEDAGOGICAL_CONTRACT.md
├── PUBLICATION_TOOLCHAIN.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── CHANGELOG.md
├── CITATION.cff
├── Makefile
├── pyproject.toml
│
├── book/
│   ├── metadata.yaml
│   ├── frontmatter/
│   ├── chapters/
│   ├── appendices/
│   └── references/
│
├── concept-edition/
│
├── concepts/
│   ├── concept_registry.yaml
│   ├── prerequisites.yaml
│   └── stability-contract.md
│
├── glossary/
│   ├── glossary.yaml
│   ├── aliases.yaml
│   └── acronym_registry.yaml
│
├── figures/
│   ├── source/
│   ├── generated/
│   ├── exploded-views/
│   ├── ecosystem/
│   ├── sequence/
│   ├── architecture/
│   └── accessibility/
│
├── labs/
│   ├── README.md
│   ├── lab_registry.yaml
│   ├── explorer/
│   ├── operator/
│   ├── builder/
│   ├── engineer/
│   └── researcher/
│
├── waike/
│   ├── alignment.yaml
│   ├── course_crosswalk.md
│   ├── assessment_crosswalk.md
│   └── portfolio_evidence.md
│
├── devices/
│   ├── quartet.yaml
│   ├── student-14-5/
│   ├── handheld-hybrid/
│   ├── ds-xl-coder/
│   └── edge-io-wearables/
│
├── evidence/
│   ├── ACCEPTED_MAIN_SOURCE_AUDIT.md
│   ├── source_registry.yaml
│   ├── claim_registry.yaml
│   ├── publication_claims.md
│   └── unresolved_claims.md
│
├── careers/
│   ├── role_registry.yaml
│   ├── skill_map.yaml
│   └── chapter_role_map.md
│
├── educator/
│   ├── instructor_guide.md
│   ├── lesson_plans/
│   ├── assessments/
│   └── answer_guidance/
│
├── scripts/
│   ├── validate_book.py
│   ├── validate_claims.py
│   ├── validate_glossary.py
│   ├── validate_links.py
│   ├── validate_labs.py
│   ├── validate_figures.py
│   └── validate_accessibility.py
│
├── tests/
│
├── publication/
│   ├── RELEASE_CHECKLIST.md
│   ├── ISBN_CHECKLIST.md
│   ├── PRINT_REQUIREMENTS.md
│   ├── EPUB_REQUIREMENTS.md
│   ├── ACCESSIBILITY_REQUIREMENTS.md
│   ├── DISTRIBUTION_OPTIONS.md
│   └── RIGHTS_AND_PERMISSIONS.md
│
└── .github/
    ├── workflows/
    └── ISSUE_TEMPLATE/
```

Adjust only when a better architecture is clearly justified.

---

# 6. Canonical architecture files

Create:

- `BOOK_ARCHITECTURE.md`
- `PEDAGOGICAL_CONTRACT.md`
- `STYLE_BIBLE.md`
- `PUBLICATION_TOOLCHAIN.md`

`BOOK_ARCHITECTURE.md` must preserve all 31 canonical chapters.

`PEDAGOGICAL_CONTRACT.md` must codify:

- experience-first teaching,
- six reader pathways,
- 12-section chapter anatomy,
- Stability Contract,
- observation-vs-inference rules,
- WAIKE evidence rules.

`STYLE_BIBLE.md` must codify:

- warm/direct/curious voice,
- middle-school-accessible baseline,
- progressive technical depth,
- analogy labeling,
- status-language rules,
- diagram grammar,
- accessibility.

---

# 7. Select publication toolchain deliberately

Evaluate suitable open/reproducible options.

Candidates may include:

- Quarto,
- Pandoc,
- Typst,
- LaTeX,
- Sphinx,
- mdBook.

Selection criteria:

- Markdown-first authoring,
- PDF quality,
- EPUB support,
- cross-references,
- citations,
- figure handling,
- accessibility,
- reproducibility,
- automation,
- contributor usability.

Document the decision.

Do not select a tool solely because it is already installed.

---

# 8. Build commands

Target simple commands:

```bash
make setup
make validate
make test
make preview
make pdf
make epub
make all
```

If a specific toolchain makes different command names more appropriate, retain aliases for the above wherever practical.

---

# 9. Semantic validation

Do not limit validation to "file exists."

Implement validators for:

- malformed YAML,
- duplicate IDs,
- missing chapter metadata,
- invalid chapter references,
- missing glossary concepts,
- orphan glossary entries,
- invalid lab references,
- missing lab sections,
- missing no-hardware route,
- missing lab evidence requirements,
- figure missing alt text,
- figure missing text equivalent,
- orphan figure,
- invalid claim status,
- project-specific claim with no source,
- project-specific claim using non-main evidence without explicit label,
- invalid citation key,
- broken local link,
- chapter missing pathway coverage,
- WAIKE reference mismatch,
- invalid truth-status language.

Tests must fail honestly.

---

# 10. Prototype chapter

The primary manuscript deliverable is:

# Chapter 2 — Follow One Tap Through the Entire Stack

Follow `04_CHAPTER_02_FOLLOW_ONE_TAP_SPEC.md`.

This must be real chapter prose, not a detailed outline.

The chapter is the publication's canonical design prototype.

Do not claim Gate 3 until it is complete enough to review as a real book chapter.

---

# 11. Required prototype figures

Create, at minimum:

1. Human-to-system overview
2. Cross-layer sequence
3. Representative physical exploded view
4. Software stack
5. Network path
6. Latency/stability budget
7. Stability Contract diagram

Use editable source.

Prefer SVG.

Conceptual diagrams must say they are conceptual.

Do not fabricate exact gunnchOS hardware details.

---

# 12. Prototype WAIKE lab

Create:

# LAB-TAP-001 — Trace and Measure One Tap

Required baseline routes:

### Route A — Browser

Use developer tools to inspect:

- input event,
- event handler,
- network request where relevant,
- response,
- rendering.

### Route B — Local application

A small local application that timestamps:

- input,
- processing,
- visible/output response.

### Route C — Android-compatible extension

Where available:

- app logs,
- input event,
- frame timing,
- network request.

No proprietary gunnchOS device may be required for baseline completion.

Create portfolio output requirements.

---

# 13. Glossary prototype

Create structured entries for terms introduced by Chapter 2.

At minimum consider:

- event,
- touch digitizer,
- interrupt,
- device driver,
- kernel,
- process,
- thread,
- scheduler,
- event loop,
- API,
- CPU,
- GPU,
- RAM,
- storage,
- packet,
- protocol,
- radio,
- router,
- latency,
- jitter,
- rendering,
- frame,
- cache,
- service,
- edge computing,
- cloud computing,
- haptic feedback.

Do not force terms that the chapter does not actually use.

---

# 14. Career map prototype

Chapter 2 should map real responsibilities across the stack.

Potential roles:

- UX designer
- HCI engineer
- embedded engineer
- firmware engineer
- device-driver engineer
- kernel engineer
- OS engineer
- application developer
- frontend engineer
- backend engineer
- SRE
- cloud engineer
- network engineer
- wireless engineer
- cybersecurity engineer
- performance engineer
- computer architect
- silicon engineer
- accessibility engineer
- researcher
- technical program manager

For each included role, record:

- what they own,
- which layer(s) they touch,
- representative tools,
- professional artifact,
- learner portfolio analogue.

Do not promise employment outcomes.

---

# 15. Concept Edition

Create scaffolding for all six Concept Edition modules, but do not manufacture full prose merely to call them complete.

Status must remain explicit.

Allowed examples:

```text
CE-1 scaffold
CE-2 full prototype
CE-3 scaffold
CE-4 scaffold
CE-5 scaffold
CE-6 scaffold
```

Only upgrade status when the content satisfies the gate.

---

# 16. Evidence language

For project-specific statements, use the claim registry.

Allowed classifications include:

- general-knowledge
- textbook
- standard
- peer-reviewed
- repository-implemented
- repository-tested
- measured
- simulated
- illustrative
- planned
- hypothesis

Do not render:

`planned`

as:

`implemented`

Do not render:

`simulated`

as:

`deployed`

Do not render:

`repository-tested`

as:

`independently validated`

---

# 17. Rights and permissions

Create a rights register.

Prefer original diagrams.

Record third-party materials before inclusion.

Do not copy:

- textbook figures,
- proprietary architecture diagrams,
- substantial copyrighted prose,
- copyrighted screenshots where permission/license is unclear.

Trademarks may be discussed factually but should not imply endorsement.

---

# 18. Accessibility

A build should fail where practical when a figure lacks required accessibility metadata.

At minimum validate:

- alt text,
- text equivalent,
- reading order for complex diagrams,
- link descriptions,
- heading hierarchy,
- table semantics in source representation.

Document limitations of automated accessibility checks.

---

# 19. README

The first screen of the README must explain:

- What is this?
- Who is it for?
- What will I understand?
- What makes it different?
- How do I read it?
- How do I run the labs?

Show:

> Human experience → system → component → code → network → society

Explain the six reader pathways.

Explain the Device Quartet.

Show status truthfully.

Avoid badge spam.

---

# 20. Draft PR

Create a draft PR.

Suggested title:

> Publication foundation + Chapter 2 canonical prototype

PR description should contain:

- achieved gate,
- not-yet-achieved gates,
- build results,
- evidence audit summary,
- chapter status,
- diagram status,
- lab status,
- known limitations,
- owner/external actions.

Do not merge.

---

# 21. Final execution report

Return:

## A. Executive status

State the highest legitimately achieved publication gate.

## B. Repository state

- repository
- branch
- commit
- draft PR
- merge status

## C. Accepted-main audit

For every audited source repo:

- repo
- branch
- SHA
- relevant evidence
- limitations

## D. Files created/changed

Group by:

- manuscript
- figures
- glossary
- labs
- WAIKE
- Device Quartet
- evidence
- careers
- publication
- automation/tests

## E. Chapter 2

Report:

- word count
- section count
- figure count
- glossary count
- lab status
- career roles
- citations
- accessibility status
- unresolved content

## F. Build results

Report exact commands and exit results.

Do not write PASS if a command did not pass.

## G. Evidence integrity

Count:

- verified
- repository-implemented
- repository-tested
- measured
- simulated
- illustrative
- planned
- unresolved

## H. Concept Edition

List exact status of all six modules.

## I. Remaining automatable work

List work Cursor can still perform without Edmund.

## J. Owner/external gates

List only actions that genuinely require:

- author decision,
- physical hardware,
- human reader testing,
- external reviewer,
- rights holder,
- ISBN authority,
- printer,
- distributor,
- storefront.

## K. Blockers

Every blocker requires:

- blocker,
- reason,
- evidence,
- dependency,
- next action.

## L. Draft PR URL

Return the URL.

---

# 22. Execution rule

Do the work.

Do not merely describe a hypothetical implementation.

Do not race to 31 low-quality chapters.

First prove the publication system with one exceptional canonical chapter.
