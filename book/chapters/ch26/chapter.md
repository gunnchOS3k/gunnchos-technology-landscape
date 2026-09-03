---
status: draft
chapter_id: CH26
chapter_number: 26
title: "Software Development and Version Control"
author: "Edmund Gunn, Jr."
part: VI
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: []
figures:
  - FIG-CH26-001
  - FIG-CH26-002
  - FIG-CH26-003
---

# Chapter 26 — Software Development and Version Control

**Status:** `draft` · **Chapter ID:** `CH26`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working draft complete · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does **not** claim Gate 3 PASS; fixtures and illustrative worksheets are teaching infrastructure, not human reader evidence).

Part VI opens the build-prove-contribute arc. Earlier chapters taught you to notice experiences, name cooperating layers, and keep evidence honest. This chapter turns that literacy into a small, reviewable change loop: edit, inspect, commit, show what differed—and recover without mythology.

---

## 1. The moment {#sec-moment}

You change one behavior.

Maybe you fix a typo in a README, rename a confusing label, tighten a checklist, or adjust a tiny function so a test passes. The file looks different on your screen. Then someone asks the adult question: *what exactly changed, and can I trust that story later?*

From the seat: either confidence or fog.

Underneath: **version control**—recording changes so history can be inspected and recovered [@git-scm-docs] (CLM-CH26-001). A **commit** is a snapshot with a message and identity metadata. A **diff** is the readable difference. A **branch** is a parallel line of work that must later integrate carefully. None of those words are slogans about “being a developer.” They are tools for making a change *reviewable*.

The governing question for this chapter:

> After I change one behavior, can I show what differed, leave a clear message, and recover from a mistake without rewriting history myths?

This is Part VI’s software-pathway opener (CH01→CH02→…→CH26→CH27). It is not a full Git encyclopedia, not an employment promise, and not a Device Quartet shipping claim.

---

## 2. What you notice {#sec-notice}

Before naming remotes or rebase strategies, notice the human contracts you already expect.

You expect to know whether your work is saved as history or still only local edits. You expect a teammate—or your future self—to see *what* changed without replaying your whole afternoon. You expect a mistake to be recoverable without panic folklore (“just force it”). You expect secrets (tokens, passwords, private keys) never to become permanent history. You expect a clear message to beat a vague “fixes.”

Those expectations *are* the development loop from the person’s point of view.

**Status and diff are observations about change; “I’m done” is a claim that needs evidence.**

Optional commodity notice (no paid IDE required): open any small text project you already may edit—or a fixture worksheet if you prefer offline. Make one harmless change. Before you “save forever,” write two columns: *what I think I changed* and *what status/diff actually lists*. If tools are unavailable, use a printed before/after pair and mark the row `fixture`. Fixture worksheets are teaching aids, not Gate 3 human validation.

---

## 3. Exploded ecosystem {#sec-ecosystem}

A single commit is not a lone object. It is a path through an ecosystem. **FIG-CH26-001** (planned conceptual sequence) is the first-minute map: edit → status → diff → commit → review. Treat it as **Representative educational architecture**, not a claim that every team uses identical tools or hosting vendors.

### Human and intent

You decide what “better” means for this change: clearer text, safer behavior, a passing check. Intent sets the review question.

### Working tree

Files as they exist on disk right now—including uncommitted edits. The working tree can disagree with history [@git-scm-docs].

### Staging / index (when used)

The optional “what I intend to include next” set. Confusion here produces commits that omit the file you thought you saved or include a file you meant to leave out.

### Committed history

Snapshots linked as history. **FIG-CH26-002** (planned comparison) separates working tree vs committed history so readers stop treating “I edited a file” as “it is in history.”

### Message and identity metadata

Who recorded the snapshot, when, and what they claimed it meant. Messages are part of the evidence surface.

### Branch / integration path

Parallel lines of work and the careful combine later. Integration is a social and technical event—not automatic correctness.

### Review surface

Humans inspect diffs before integration. Review is literacy, not theater.

### Build-test loop

Change → verify → evidence before claiming done. Chapter 27 deepens testing and observability; here the loop is the minimum honesty check.

### Secrets boundary

Credentials and tokens must not enter history. **FIG-CH26-003** (planned boundary) makes the refuse-line visible.

### Project evidence neighbors (adjacency only)

WAIKE’s `SOFTWARE_BUILDER` package is an **adjacent** builder competency neighbor—not a CH26 module ID and not an invented course label [@src-waike] (CLM-CH26-002). DS-XL Coder may appear later as a learn-to-build lens only; any measured local-build hardware claim remains **PHYSICAL_PENDING** [@src-hardware-quartet] (CLM-CH26-003).

---

## 4. Follow the signal {#sec-signal}

Here the “signal” is one reviewable change traveling from intent into inspectable history.

1. **Intent.** You choose one small behavior to change.
2. **Edit.** The working tree diverges from the last snapshot.
3. **Status.** You ask what the tool believes is modified, untracked, or staged [@git-scm-docs].
4. **Diff.** You read the actual line-level (or file-level) difference before freezing it [@git-scm-docs].
5. **Secrets scan (human).** You refuse tokens, passwords, and private keys—even in “temporary” files.
6. **Commit.** You record a snapshot with a clear message [@git-scm-docs].
7. **Verify.** You run the relevant check, test, or checklist for *this* change.
8. **Review.** You (or a peer) inspect the diff as if you did not write it.
9. **Integrate carefully.** Branch work combines without pretending history myths fix mistakes.
10. **Evidence keep.** You can point to a SHA, a message, and a scrubbed artifact—not a vibe.

### Alternate paths stay labeled

GUI clients, accessible front-ends, and offline fixture worksheets can complete the same literacy when a CLI is unavailable. The pedagogy is the loop, not a brand of hosting. Open questions (exact team policy, required review tools) stay undetermined until evidence exists.

### Version numbers when APIs are public

When a change crosses a public API boundary, **Semantic Versioning** offers MAJOR.MINOR.PATCH compatibility vocabulary: incompatible API changes, backward-compatible additions, and backward-compatible fixes [@semver-2.0.0]. That vocabulary is optional depth here—use it when you claim compatibility, not as decoration on every typo fix.

---

## 5. Component cards {#sec-components}

For each idea: plain language, analogy (labeled), technical function, constraints, common symptoms.

### Version control

- **Plain language.** Recording changes so history can be inspected and recovered.
- **Analogy (labeled).** Like keeping dated drafts of an essay instead of one overwritten file—so you can see what changed between versions.
- **Technical function.** Stores snapshots and relationships so diffs and recovery are possible [@git-scm-docs].
- **Constraints.** Tool literacy required; policies differ by team; history that includes secrets is hard to truly un-share.
- **Symptoms.** “I thought I saved it,” “I can’t show what changed,” “we lost the good version.”

### Commit

- **Plain language.** A snapshot of change with message and identity metadata.
- **Analogy (labeled).** Like sealing a labeled envelope of today’s draft—not the whole library rebuild.
- **Technical function.** Creates a recoverable history node with a message [@git-scm-docs].
- **Constraints.** A commit is not automatic proof of correctness; huge unrelated dumps hurt review.
- **Symptoms.** Empty messages, kitchen-sink commits, “fixed stuff” with no readable scope.

### Diff

- **Plain language.** The readable difference between states.
- **Analogy (labeled).** Like a red-pen markup showing additions and deletions.
- **Technical function.** Surfaces what will enter (or already entered) history [@git-scm-docs].
- **Constraints.** Binary files may not show useful text diffs; generated noise can hide intent.
- **Symptoms.** Surprising files in the change set; “I didn’t mean to include that.”

### Branch / integration

- **Plain language.** Parallel lines of work later combined carefully.
- **Analogy (labeled).** Like two co-authors editing copies, then merging with a checklist—not silently overwriting each other.
- **Technical function.** Names lines of development and integration points [@git-scm-docs].
- **Constraints.** Integration conflicts need human judgment; rewriting shared history has collaboration costs.
- **Symptoms.** Lost work after a careless overwrite; fear of “touching main.”

### Code review

- **Plain language.** Human inspection of diffs before integration.
- **Analogy (labeled).** Like a second reader checking a proof before publication.
- **Technical function.** Catches intent mismatches, missing tests, and secrets before they spread.
- **Constraints.** Review without time or norms becomes rubber-stamping.
- **Symptoms.** “LGTM” with no diff read; surprises after merge.

### Secrets hygiene

- **Plain language.** Credentials and tokens must not enter history.
- **Analogy (labeled).** Like not laminating your house key into the scrapbook—you cannot truly take it back from every copy.
- **Technical function.** Keeps sensitive material out of commits, logs, and portfolio screenshots.
- **Constraints.** Once pushed widely, assume exposure; rotation and revocation become necessary.
- **Symptoms.** Keys in README samples; `.env` committed “just once.”

### Build-test loop

- **Plain language.** Change → verify → evidence before claiming done.
- **Analogy (labeled).** Like tasting the soup after you salt it—before serving guests.
- **Technical function.** Ties commits to observable checks appropriate to the change size.
- **Constraints.** No test suite does not excuse skipping a checklist; fixtures ≠ production proof.
- **Symptoms.** “It worked on my machine” with no artifact; green CI misunderstood as full correctness.

---

## 6. Stability contract {#sec-stability}

A reviewable change experience exists only while several conditions remain within acceptable bounds.

| Condition | Plain meaning | Failure symptom |
|---|---|---|
| Working-tree understandability | Status/diff are readable for this change | Surprise files; unknown dirty state |
| History integrity practices | Collaboration-appropriate honesty about shared history | Lost peer work; panic rewrites |
| Secrets never committed | Tokens/passwords/keys stay out | Credential exposure in history |
| Build/test loop runnable | Commodity hardware or fixtures can verify | “Done” with no check path |
| Message clarity | Future readers can see intent | Undebuggable archaeology |
| Accessible tool path | CLI *or* GUI/fixture route exists | Equity exclusion by tool assumption |
| Observation vs inference | What the tool showed vs what you guess | Confident wrong blame |

A repository can be “technically present” while the human experience has already failed: nobody can tell what changed, secrets leaked, or verification never ran.

---

## 7. Try it {#sec-try}

**Inherited adjacency.** Builder pathway habits from Concept Edition packages and WAIKE `SOFTWARE_BUILDER` remain **adjacent**—link, do not invent a CH26 WAIKE lab ID [@src-waike] (CLM-CH26-002).

**Proposed publication worksheet (not shipped this wave).** A publication-owned git fixture lab remains **proposed** in the CH26 packet (safe commit/review worksheet with offline fixture route). Until it ships under `labs/`, do not treat the proposal as an implemented lab ID and do not mint it as a WAIKE course code.

**Living example without marketing.** This publication repository itself is a real Git history you can read as a learner: status, diff, commit messages, and SHAs are ordinary evidence surfaces. Reading history is not permission to invent product claims.

### Explorer baseline (about 40–50 minutes)

1. Predict, in ordinary language, what “commit,” “branch,” and “diff” mean before touching tools.
2. Make one tiny safe edit (or use a fixture before/after pair).
3. Run or simulate **status**, then **diff**—write what you observe [@git-scm-docs].
4. Draft a clear commit message *before* recording (even on paper for fixtures).
5. Fill observation vs inference: what the tool showed vs what you assume about “done.”
6. Teach-back: explain the loop to a family member without saying “rebase.”

### Operator extension

Read a status/diff and say what will change **before** running a mutating command. Practice stopping when a surprise file appears.

### Builder extension

Make a small change with a test note or checklist evidence. Prefer PR-sized scope: one intent, one message, one verification note.

### Engineer extension

Propose a reviewable change with rationale: why this diff, what could break, what evidence would convince a reviewer.

### Researcher extension

Document reproducibility of the change environment at a SHA (tool versions you actually used; unknowns labeled). Do not invent Git behavior beyond official docs [@git-scm-docs].

### Safety / privacy / accessibility

- No exploit steps, credential harvesting, or capture of others’ private data.
- Redact identifiers before portfolio share.
- Provide fixture / no-specialized-hardware completion routes.
- Prefer accessible CLI *or* GUI paths; do not assume a paid IDE [@wcag22-20241212].

---

## 8. Build it {#sec-build}

Extend the Try-it loop by one honest notch—not by boiling the ocean.

1. **Pick one behavior** with a human-visible outcome (label clarity, checklist item, tiny logic fix).
2. **Write the review question** you want a stranger to answer from your diff alone.
3. **Keep the change small** enough that a peer can finish the review in one sitting.
4. **Attach evidence:** scrubbed status/diff excerpt, message text, and pass/fail note for your check.
5. **Optional compatibility note:** if you touch a public API, state whether SemVer MAJOR/MINOR/PATCH thinking applies—or explicitly say “not a public API change” [@semver-2.0.0].
6. **Refuse scope creep:** new features, refactors, and secret cleanup are separate commits when possible.

**Success looks like:** another learner can restate your intent from the message + diff without asking you to narrate your afternoon.

**Failure modes to name:** kitchen-sink commits; “WIP” forever; screenshots that leak tokens; claiming employment readiness from one worksheet.

---

## 9. Secure and include it {#sec-secure}

### Secrets

Never commit credentials, API tokens, private keys, or live customer data. Treat “I’ll remove it in the next commit” as insufficient once history is shared. Portfolio packets get redaction passes.

### Inclusive tooling

Do not assume a paid IDE, a particular OS, or unbroken high-speed networking. Offline fixtures and GUI clients are first-class equity routes. Color must never be the sole cue in status diagrams [@wcag22-20241212].

### Collaboration ethics

Rewriting shared history without agreement can erase peers’ work. Prefer honest recovery practices appropriate to your collaboration setting. “Force it” is not a teaching goal here.

### Device and hardware honesty

DS-XL Coder and other Device Quartet form factors remain **PHYSICAL_PENDING** for measured local-build claims—learning lenses only, not shipping-product marketing [@src-hardware-quartet] (CLM-CH26-003).

### Evidence ethics

Fixtures and illustrative worksheets are not human Gate 3 validation. Do not present proposed labs as shipped. Do not invent WAIKE IDs.

---

## 10. Career lens {#sec-career}

Version control literacy shows up across software roles. **Completing this chapter’s artifacts does not guarantee employment, promotion, or a job offer.** Portfolio evidence demonstrates that you can produce reviewable change; hiring decisions belong to organizations and remain outside this book’s promises.

| Role family | Portfolio evidence (miniature) | Review questions |
|---|---|---|
| Software engineer | Small PR-sized change + test/checklist note | Is the diff reviewable in one sitting? |
| Release engineer | SHA-pinned change evidence | Can someone reproduce *which* snapshot? |
| Tech lead / reviewer | Review checklist artifact | Did review catch secrets and scope? |
| Educator / mentor | Misconception log + teach-back notes | Can learners separate status from “done”? |

Prefer a scrubbed diff + clear message over a slogan résumé line about “passionate coding.”

---

## 11. Check understanding {#sec-check}

**Concept.** In one sentence each, explain *commit*, *branch*, and *diff* so none swallows the other two.

**Concept.** Why is the working tree not the same thing as committed history?

**System tracing.** Trace one small change from intent → status → diff → commit → review in numbered steps. Mark observed vs inferred.

**Misconception check.** Why is “I’ll delete the secret in the next commit” not good enough once history is shared?

**Misconception check.** Why does a clear commit message matter to someone who was not in the room?

**Evidence ethics.** What is the difference between a proposed publication git worksheet, an adjacent WAIKE `SOFTWARE_BUILDER` package, and Gate 3 human reader validation?

**Career boundary.** Why is portfolio evidence not an employment promise?

**Teach-it-back.** Explain to a newcomer—without saying “rebase” or “detached HEAD”—how to show what changed after editing one file.

**Researcher prompt.** What metadata would you record to make a change environment reproducible at a SHA, and what remains out of scope without primary sources [@git-scm-docs]?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). Official Git documentation is the preferred primary reference for core VCS concepts (CLM-CH26-001) [@git-scm-docs]. Semantic Versioning is cited only where compatibility vocabulary is claimed [@semver-2.0.0]. Project-specific adjacency uses repository evidence keys such as @src-waike and @src-hardware-quartet with **PHYSICAL_PENDING** where required (CLM-CH26-002, CLM-CH26-003).

Inline citations used in this chapter include @git-scm-docs, @semver-2.0.0, @src-waike, @src-hardware-quartet, and @wcag22-20241212.

Primary packet (link, prefer over duplication): `publication/full31/chapters/ch26/`. Gate 3 reader evidence remains pending; this working draft is not publication-ready and does not modify `publication/gates/gate-3/`.

---

## 12. Glossary links {#sec-glossary}

Candidate terms introduced or reinforced here (see also `GLOSSARY_CANDIDATES.yaml`; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Version control | Recording changes so history can be inspected and recovered |
| Commit | Snapshot of change with message and identity metadata |
| Diff | Readable difference between states |
| Branch / integration | Parallel lines of work later combined carefully |
| Code review | Human inspection of diffs before integration |
| Secrets hygiene | Credentials/tokens must not enter history |
| Build-test loop | Change → verify → evidence before claiming done |
| Working tree | Files on disk now, including uncommitted edits |
| SHA | Identifier for a specific snapshot in history |
| Semantic versioning | MAJOR.MINOR.PATCH compatibility vocabulary for public APIs |
| Stability Contract | Concurrent conditions that keep a reviewable-change experience alive |
| Observation vs inference | What the tool showed vs what may explain it |

Related earlier chapters: experience-first method (CH02), applications/APIs and SemVer adjacency (CH14), containers/cloud placement (CH15). Related later chapters: testing and evidence (CH27), product design (CH29), career maps (CH30), capstone (CH31).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All three figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured learner evidence. No fabricated telemetry. Color never sole cue.

### FIG-CH26-001 — Edit → status → diff → commit → review

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Sequence.
- **Reader should notice.** The reviewable-change loop as ordered literacy, not vendor marketing.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name each stage in order; deny that every team hosts identically.

### FIG-CH26-002 — Working tree vs committed history

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Comparison.
- **Reader should notice.** Edited files are not automatically history.
- **Truth class.** Conceptual.
- **Alt text requirement.** Contrast “on disk now” vs “recorded snapshot”; shape + label encoding.

### FIG-CH26-003 — Secrets must not enter the repository

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Boundary.
- **Reader should notice.** The refuse-line for credentials/tokens/keys.
- **Truth class.** Conceptual.
- **Alt text requirement.** State the boundary explicitly; color never sole cue.

---

## Claim footnotes used in this chapter (project-specific)

- **CLM-CH26-001.** Git official documentation is the preferred primary reference for core VCS concepts [@git-scm-docs].
- **CLM-CH26-002.** WAIKE `SOFTWARE_BUILDER` is adjacent builder competency—not a CH26 module ID [@src-waike].
- **CLM-CH26-003.** DS-XL Coder learn-to-build form factor remains **PHYSICAL_PENDING** for measured local-build claims [@src-hardware-quartet].
