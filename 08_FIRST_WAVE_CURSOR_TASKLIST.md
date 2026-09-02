# First-Wave Cursor Task List

# Mission

Build the publication foundation and prove the design with one excellent chapter.

Do not attempt to complete all 31 chapters.

---

# Phase 1 — Workspace and repository discovery

## Tasks

- [ ] Read all publication specification files.
- [ ] Inspect `gunnchOS3k` repositories.
- [ ] Determine whether a canonical publication repo exists.
- [ ] If absent and tooling permits, create `gunnchos-technology-landscape`.
- [ ] Create branch `cursor/publication-foundation-v1`.
- [ ] Record starting repo/branch/commit state.

## Do not

- [ ] modify upstream projects,
- [ ] merge PRs,
- [ ] rewrite accepted-main history.

---

# Phase 2 — Accepted-main source audit

## Tasks

- [ ] Audit `waike-research-ops`.
- [ ] Audit `gunnchos-device-os`.
- [ ] Locate and audit canonical hardware repository.
- [ ] Identify only those research repos directly relevant to Chapter 2.
- [ ] Record SHAs.
- [ ] Create source registry.
- [ ] Create accepted-main audit report.
- [ ] Record unsupported claims.

## Required outputs

- `evidence/ACCEPTED_MAIN_SOURCE_AUDIT.md`
- `evidence/source_registry.yaml`
- `evidence/unresolved_claims.md`

---

# Phase 3 — Publication foundation

## Tasks

- [ ] Create repository directory structure.
- [ ] Create README.
- [ ] Create BOOK_ARCHITECTURE.
- [ ] Create PEDAGOGICAL_CONTRACT.
- [ ] Create STYLE_BIBLE.
- [ ] Create PUBLICATION_TOOLCHAIN.
- [ ] Add contribution rules.
- [ ] Add citation metadata.
- [ ] Add rights/permissions register.
- [ ] Add accessibility requirements.
- [ ] Add release checklist.

---

# Phase 4 — Structured registries

## Tasks

- [ ] Create 31-chapter registry.
- [ ] Create Concept Edition registry.
- [ ] Create concept registry.
- [ ] Create prerequisite graph.
- [ ] Create glossary registry.
- [ ] Create acronym registry.
- [ ] Create lab registry.
- [ ] Create Device Quartet registry.
- [ ] Create career role registry.
- [ ] Create evidence claim registry.
- [ ] Create WAIKE mapping schema.

---

# Phase 5 — Validators

## Tasks

- [ ] YAML validator.
- [ ] Unique-ID validator.
- [ ] Chapter-reference validator.
- [ ] Glossary-reference validator.
- [ ] Lab-schema validator.
- [ ] Figure-metadata validator.
- [ ] Accessibility-metadata validator.
- [ ] Claim-status validator.
- [ ] Link validator.
- [ ] WAIKE mapping validator.
- [ ] Citation-key validator.

## Tests

Create meaningful tests for each validator.

Include invalid fixtures.

A validator that has never been observed failing is not adequately tested.

---

# Phase 6 — Publication toolchain

## Tasks

- [ ] Evaluate Markdown-first toolchain.
- [ ] Document selection rationale.
- [ ] Implement setup.
- [ ] Implement preview.
- [ ] Implement PDF build.
- [ ] Implement EPUB build.
- [ ] Implement bibliography/citation support.
- [ ] Implement cross-reference support.
- [ ] Add CI build.

## Commands

Target:

```bash
make setup
make validate
make test
make preview
make pdf
make epub
make all
```

---

# Phase 7 — Chapter 2 manuscript

## Task

Write the actual chapter:

> Follow One Tap Through the Entire Stack

## Required sections

- [ ] The moment
- [ ] What you notice
- [ ] Exploded ecosystem
- [ ] Follow the signal
- [ ] Component cards
- [ ] Stability contract
- [ ] Try it
- [ ] Build it
- [ ] Secure and include it
- [ ] Career lens
- [ ] Check understanding
- [ ] Glossary links

## Quality

The text must serve:

- Explorer,
- Operator,
- Builder,
- Engineer,
- Researcher,
- Educator.

---

# Phase 8 — Chapter 2 visuals

## Required

- [ ] Human-to-system overview
- [ ] Cross-layer sequence
- [ ] Representative exploded view
- [ ] Software stack
- [ ] Network/local-path comparison
- [ ] Latency budget
- [ ] Stability Contract figure

For every figure:

- [ ] editable source
- [ ] exported SVG
- [ ] caption
- [ ] alt text
- [ ] long description
- [ ] reading order
- [ ] conceptual/implementation label

---

# Phase 9 — LAB-TAP-001

## Tasks

- [ ] Browser route.
- [ ] Local application route.
- [ ] Android extension instructions.
- [ ] Prediction.
- [ ] Evidence capture.
- [ ] Result table.
- [ ] Observation vs inference.
- [ ] Limitations.
- [ ] Builder extension.
- [ ] Researcher extension.
- [ ] Teach-back.
- [ ] Portfolio template.

## Baseline constraint

No proprietary or unreleased gunnchOS hardware required.

---

# Phase 10 — Prototype glossary

## Tasks

- [ ] Register actual terms used by Chapter 2.
- [ ] Add plain definitions.
- [ ] Add technical definitions.
- [ ] Add experience benefit.
- [ ] Add analogy.
- [ ] Add "not the same as".
- [ ] Add failure symptom.
- [ ] Add measurement idea.
- [ ] Add related terms.
- [ ] Add chapter/lab links.

Run glossary validation.

---

# Phase 11 — Career mapping

## Tasks

- [ ] Identify roles involved in tap-to-response stack.
- [ ] Map ownership.
- [ ] Map professional artifacts.
- [ ] Map tools.
- [ ] Map learner portfolio analogue.
- [ ] Avoid employment guarantees.

---

# Phase 12 — WAIKE alignment

## Tasks

- [ ] Audit actual accepted-main WAIKE structure.
- [ ] Map Chapter 2 where evidence supports a mapping.
- [ ] Map LAB-TAP-001.
- [ ] Create portfolio evidence mapping.
- [ ] Do not invent course IDs/modules.

---

# Phase 13 — Concept Edition scaffold

Create intentional scaffolds for:

- [ ] CE-1 Technology Is a System, Not a Screen
- [ ] CE-2 Follow One Tap Through the Entire Stack
- [ ] CE-3 CPU, Memory, Storage, and the OS
- [ ] CE-4 Packets, Wi-Fi/Cellular, Edge and Cloud
- [ ] CE-5 AI, Security, Privacy and Trust
- [ ] CE-6 The Stability Contract + Capstone

Only CE-2 is expected to be manuscript-complete in Wave 1.

---

# Phase 14 — Release gates

## Tasks

- [ ] Create gate evidence files.
- [ ] Evaluate Gate 0 truthfully.
- [ ] Evaluate Gate 1 truthfully.
- [ ] Evaluate Gate 2 truthfully.
- [ ] Evaluate Gate 3 truthfully.
- [ ] Do not evaluate later gates as complete.

---

# Phase 15 — CI and reproducibility

## CI should run

- [ ] validation,
- [ ] tests,
- [ ] link checks,
- [ ] preview build,
- [ ] optionally PDF/EPUB build if environment permits.

## CI should not

- [ ] hide failures,
- [ ] mark missing dependencies as PASS,
- [ ] fabricate external validation.

---

# Phase 16 — Draft PR

## Required

- [ ] Commit work.
- [ ] Push branch.
- [ ] Open draft PR.
- [ ] Do not merge.

## PR body

Include:

- highest achieved gate,
- accepted-main SHAs,
- build results,
- Chapter 2 status,
- lab status,
- figure status,
- evidence status,
- accessibility status,
- unresolved claims,
- remaining automatable tasks,
- owner/external gates.

---

# Phase 17 — Stop condition

Stop only after:

- automatable failures have been fixed,
- remaining blockers genuinely require outside action,
- draft PR exists,
- report is complete.

Do not stop because:

- a file is long,
- a diagram takes effort,
- a validator needs implementation,
- a build dependency needs configuration,
- manuscript drafting is substantial.

These are part of the task.

---

# Expected first-wave final report

Use this exact structure.

## A. Executive Status

## B. Repository / Branch / Commit / PR

## C. Accepted-Main Source Audit

## D. Files Created / Changed

## E. Chapter 2 Status

## F. Figure Status

## G. LAB-TAP-001 Status

## H. Glossary Status

## I. WAIKE Alignment

## J. Build / Test Results

## K. Evidence Integrity

## L. Gate Evaluation

## M. Remaining Automatable Work

## N. Owner / External Actions

## O. Blockers

## P. Draft PR URL
