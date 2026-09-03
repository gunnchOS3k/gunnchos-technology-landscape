---
status: draft
chapter_id: CH13
chapter_number: 13
title: "Files, Databases, and Data Lifecycles"
author: "Edmund Gunn, Jr."
part: III
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-CMS-001, LAB-TRUST-001]
figures:
  - FIG-CH13-001
  - FIG-CH13-002
  - FIG-CH13-003
  - FIG-CH13-004
---

# Chapter 13 — Files, Databases, and Data Lifecycles

**Status:** `draft` · **Chapter ID:** `CH13`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working full-manuscript draft · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (this chapter does not claim Gate 3 completion).

---

## 1. The moment

You hit Save. Or you close a tab. Or you walk away assuming the document will be there tomorrow the way you left it.

Later the file is missing, an older version returns, a “recovered document” dialog appears, or two copies of the same cloud note disagree. From the seat it feels like storage is broken—or like the computer betrayed a promise you thought was simple.

Underneath that feeling, several persistence stories collide: working memory that forgets when power leaves, filesystems that organize durable bytes, application buffers that may still be holding the truth you thought you saved, optional cloud replicas that sync on their own schedule, and policies about how long data is kept or removed.

This chapter’s governing question:

> When I save, reopen, share, or delete, what durable-state contracts and lifecycle stages must hold—and why is “saved” not the same as “truth forever”?

Part III is about making hardware useful. Chapters nearby treat boot, trust, and the operating system’s handoff. Here the useful abstraction is **durable state**: named files, structured stores, and the human lifecycle from create to use to retain to share to delete or redact—without turning the chapter into forensics, undelete cookbooks, or invented product benchmarks.

Device Quartet storage endurance and performance numbers remain **PHYSICAL_PENDING** (CLM-CH13-006). Commodity observation is enough for the labs this chapter inherits.

---

## 2. What you notice

Before names like *filesystem* or *durability*, notice the human contracts you already expect.

You expect Save to mean the work will reopen. You expect Quit not to erase what you believed was durable. You expect “in the cloud” to mean another place holds a usable copy—not that every device instantly shares one perfect version. You expect Delete to reduce how available something is, at least for ordinary use. You also expect failure to be visible: a permission error, a conflict banner, a recovered-draft dialog—not silent wrong content that looks complete.

Those expectations *are* the product from the person’s point of view.

**A persistence experience is produced by layered contracts: working memory is not durable storage; UI Save is not always proof bits reached stable media; replicas can disagree without the local filesystem being “broken.”**

Notice the split timelines. What is on screen can still live only in RAM. What the app calls saved may still sit in a buffer. What one device shows may lag another replica. Optional comparison on a device you already own: type a short throwaway note in a local editor, save, quit, reopen—then compare that to an unsaved buffer you deliberately leave open. You are not collecting a product benchmark. You are noticing that “still visible” and “durable across quit” are different experiences (CLM-CH13-001) [@tanenbaum-bos].

A second optional notice: if you already use a cloud document, open the same note on two sessions you control and watch for conflict or version cues—**without** treating a conflict banner as proof that your disk failed. Label what you observe versus what you infer.

---

## 3. Exploded ecosystem

Persistence is not one object. It is a path through an ecosystem. **FIG-CH13-002** (conceptual) is the first-minute durability stack: app buffer → filesystem → device media → optional cloud replica. Treat it as **Representative educational architecture**, not a claim that every phone or laptop wires exactly like the diagram.

Walk the layers in ordinary language.

### Human

You form intent: keep this draft, finish tomorrow, share with a teammate, remove something that should not linger. Hands hit Save. Eyes check filenames and conflict banners. Later you judge whether the reopen matched the promise.

### Application buffer / working set

Editors and apps keep a live working copy in memory. That copy can feel complete while still depending on process lifetime. **RAM is not a substitute for durable storage** under ordinary power-off and quit conditions (CLM-CH13-001) [@tanenbaum-bos].

### File and filesystem

A **file** is the ordinary named durable byte-sequence abstraction on personal devices. A **filesystem** organizes files and directories with metadata and durability rules the OS exposes to apps [@tanenbaum-bos]. From the seat, “Documents” is a place. Underneath, it is a contract about names, permissions, and when writes become durable enough to survive crashes—within the OS’s stated assumptions.

### Caches and write-back

Operating systems and devices use caches and buffers for speed. **Write-back** behavior can delay when data reaches stable media. The Save button is a human signal; it is not always instantaneous proof that bits are on non-volatile media (CLM-CH13-002) [@tanenbaum-bos; @saltzer-kaashoek]. Systems design treats naming, buffering, and failure as first-class concerns rather than UI decorations [@saltzer-kaashoek].

### Device media

Flash, disk, and related controllers hold durable bytes—until wear, full volumes, permission failures, or hardware faults intervene. Quartet-specific endurance curves stay **PHYSICAL_PENDING** (CLM-CH13-006). Classroom work uses commodity devices and fixtures, not invented EVT telemetry.

### Structured stores (qualitative)

Many apps also keep state in **databases** or other structured stores: tables, indexes, and concurrency rules sitting above raw files. This draft treats that as a **responsibility split**—structure and concurrent access versus a single file blob—without citing a pinned database-systems textbook edition. Formal recovery and consistency slogans stay out of the cited-claim set until SOURCE_NEEDED closes (CLM-CH13-003 omitted as a sourced claim). **FIG-CH13-004** (conceptual) sketches file versus database responsibilities as a teaching plate, not as product endorsement.

### Sync and replicas (qualitative)

Optional cloud sync adds copies that update over time. From the seat, a conflict can feel like “storage broke.” A more careful reading: multiple durable states can exist at once, and disagreement is a distributed-state symptom to observe—not automatic proof that the local filesystem failed. Specific sync theorems and vendor conflict algorithms remain SOURCE_NEEDED (CLM-CH13-004 omitted as a sourced claim); this chapter keeps the honesty rule: label conflict UI as observation.

### Lifecycle policy

Beyond mechanism sits **lifecycle**: create/collect → use → retain → share → delete/redact. **FIG-CH13-001** (conceptual) is the lifecycle arc. Policy language (“we delete after…”) and mechanism (what the UI removes) can diverge; later sections stay qualitative and refuse recoverability cookbooks.

### System software

The OS mediates process lifetime, file APIs, permissions, and often sync agents. Apps still own when they call durable write paths. Mis-attribution is easy: blaming “the cloud” for a local unsaved buffer, or blaming “the disk” for a replica conflict.

---

## 4. Follow the signal

Here the “signal” is durable state moving through time—not a tap packet. **FIG-CH13-003** (illustrative) contrasts a Save click with a later durability point such as flush/fsync conceptually. Read it as a logical story, not as a claim that every app executes identical steps.

1. **Intent.** You decide content should survive quit, crash, or tomorrow’s reopen.
2. **Edit in working memory.** Keystrokes update an in-memory buffer; the screen looks complete.
3. **Save action.** UI Save (or autosave) requests persistence.
4. **App write path.** The application issues write APIs toward a file or structured store.
5. **OS buffering.** Caches and write-back may hold data for performance before stable media acknowledges it (CLM-CH13-002) [@tanenbaum-bos; @saltzer-kaashoek].
6. **Durable media.** Bytes reach device storage—or fail (full volume, permission denied, I/O error).
7. **Optional replica.** A sync agent may upload, download, or merge copies on another device or service.
8. **Human reopen / share / delete.** Later experience tests whether the contract matched expectations.
9. **Feedback.** Success toast, conflict banner, recovered-draft dialog, or silent surprise closes the loop—or fails to.

### Alternate paths (honesty rule)

| Path | Everyday example | What changes |
|---|---|---|
| **Local file, explicit Save** | Notes app → Save → quit → reopen | Durability depends on write completion, not screen content |
| **Autosave buffer** | Recovered document after crash | Partial durability; timing uncertain from outside |
| **Unsaved tab** | Close without Save | Working memory ends with the process |
| **Cloud conflict cue** | Two devices edited offline | Replica disagreement symptom—not proven local FS failure |
| **Delete in UI** | Trash / remove | Ordinary availability may change; global unrecoverability is a separate, often unverified claim |

Do not invent flush latency budgets. Do not treat one successful reopen as proof that every future autosave is durable.

---

## 5. Component cards

Component cards answer: What is it? What does it do for the person? What fails when it misbehaves?

### File

**Plain definition.** A named durable sequence of bytes managed through a filesystem [@tanenbaum-bos].

**Experience benefit.** Work can outlive the process that created it.

**Failure symptom.** Missing file, permission denied, truncated content, or reopen that does not match what was on screen.

### Filesystem

**Plain definition.** Software organizing files, directories, and metadata on storage with durability and permission rules [@tanenbaum-bos].

**Experience benefit.** Names, folders, and ordinary Save/Open paths stay navigable.

**Failure symptom.** Corrupt directory views, unexpected “file in use,” or space/permission failures surfaced as app errors.

### Cache vs durable store

**Plain definition.** Fast temporary copies can present a complete picture before data is durable on stable media (CLM-CH13-002) [@tanenbaum-bos; @saltzer-kaashoek].

**Experience benefit.** Snappy editing and Saves that feel instant.

**Failure symptom.** Power loss or crash after a green checkmark still loses work; “saved” and “on media” diverge.

### Durability

**Plain definition.** A promise that committed data survives expected crashes or power loss—within stated assumptions [@tanenbaum-bos; @saltzer-kaashoek].

**Experience benefit.** Reopen tomorrow matches the last honest commit.

**Failure symptom.** Lost edits, recovered partial drafts, or silent rollback to an older version.

### Database (intro, qualitative)

**Plain definition.** A structured durable store with query and concurrency responsibilities beyond a single opaque file blob.

**Experience benefit.** Apps can keep related records consistent enough for everyday use without the person managing dozens of raw files.

**Failure symptom.** App-level “database error,” stuck sync of structured state, or migrations that block open—without this chapter claiming a sourced ACID textbook definition (CLM-CH13-003 omitted).

**FIG-CH13-004** keeps the teaching split: files as named byte sequences; databases as structured stores with their own failure modes.

### Consistency model (intro, qualitative)

**Plain definition.** Rules for when readers see writers’ updates—especially across replicas or sync.

**Experience benefit.** Shared documents feel coherent enough for the task.

**Failure symptom.** Conflict banners, divergent copies, or “old version returned.” Formal distributed consistency citations stay SOURCE_NEEDED (CLM-CH13-004 omitted).

### Data lifecycle

**Plain definition.** Stages of data over time: create/collect → use → retain → share → delete/redact.

**Experience benefit.** People can map where a note goes and who can see it.

**Failure symptom.** Retention longer than expected, sharing broader than expected, or delete that does not match disclosed expectations—discussed qualitatively only.

### Deletion / redaction (qualitative)

**Plain definition.** Removing or limiting ordinary availability of data; policy language and mechanism can differ.

**Experience benefit.** A person can reduce how present something is in everyday apps.

**Failure symptom.** Trash restores, synced copies elsewhere, or backups that retain content. This chapter states **uncertainty**—not a recoverability procedure (CLM-CH13-005 omitted as a sourced claim; no undelete cookbook).

---

## 6. Stability contract

The **Stability Contract** returns with persistence as a first-class condition:

> A user experience exists only while multiple hidden technical conditions remain within acceptable bounds—including durable writes, coherent enough reads, visible or safely handled sync disagreement, and retention/deletion behavior that matches disclosed expectations.

For this chapter, a sustainably honest save/reopen/share experience may require all of the following to stay “good enough” at once:

- writes needed for the experience reach a durable store within a delay the person can accept (qualitative—no invented millisecond budgets),
- reads return coherent enough state for the task,
- app buffers and OS caches are not mistaken for completed durability,
- sync or replica conflicts are visible or resolved safely enough that the person is not silently misled,
- deletion and retention policies match what was disclosed—at least for ordinary use,
- status cues (saved, conflict, offline, permission denied) remain perceivable as text, not color-only icons,
- no lab asks for forensics, undelete exploits, or paid-cloud requirements.

Three separations matter:

1. **On screen ≠ durable.** RAM and dirty buffers can look complete [@tanenbaum-bos].
2. **Save UI ≠ instantaneous stable media.** Write-back can delay durability (CLM-CH13-002) [@tanenbaum-bos; @saltzer-kaashoek].
3. **Conflict UI ≠ proof the filesystem is broken.** Treat replica disagreement as an observation pending evidence (CLM-CH13-004 qualitative only).

Device Quartet storage Stability Contract numbers remain **PHYSICAL_PENDING** (CLM-CH13-006).

---

## 7. Try it

### LAB-CMS-001 — Experience B adjacency (save / quit / reopen)

**Observable question.** After a controlled Save (or deliberate non-Save), quit, and reopen on a device I already own—or via offline fixtures—what content returned, and what cues appeared—without claiming root cause beyond observation?

**Inheritance note.** **LAB-CMS-001** (*Make Local Slowness Visible*) already ships Experience B as an optional persistence check beside Experience A’s local-lag path. This chapter **inherits** that adjacency; it does not rename the lab. Prefer the published routes and fixtures under `labs/LAB-CMS-001/`.

**WAIKE alignment note.** WAIKE accepted `main` (SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`) includes adjacent digital_rc labs such as `GENERAL_IT / lab_storage` and `GENERAL_IT / lab_backup`. Those are **neighbors**, not renamed publication IDs. Proposed **LAB-DATA-LIFE-001** remains publication-owned ideation only until implemented.

**Prerequisites.** A commodity computer or phone you may use for learning; or LAB-CMS-001 offline fixtures when shared-lab policy or equity requires them.

**Safety and privacy (mandatory).**

- Do **not** capture personal document contents, passwords, tokens, or private photos.
- Redact filenames, account names, and thumbnails before any portfolio leave-device.
- Do not require a paid cloud account; fixture transcripts satisfy completion.
- No undelete tools, disk imaging, forensic recovery steps, or attempts to bypass trash/retention.
- Mild local edits only; stop on thermal warnings.

**Time estimate.** About 20–40 minutes for Experience B alone; longer if combined with Experience A from LAB-CMS-001.

#### Prediction

Write one sentence: after Save → quit → reopen, do you expect full content, partial recovery UI, or loss—and why?

#### Route A — Commodity local editor (baseline)

1. Create a short throwaway file with a unique phrase you will recognize.
2. Save explicitly. Note any UI cue (“Saved”, checkmark, path).
3. Quit the app fully (not only hide a window).
4. Reopen the file. Record whether the phrase returned.
5. Optional second trial: type a second phrase, **do not** Save, quit, reopen. Compare.
6. Label each row **observed** vs **inferred**.

#### Route B — Optional cloud conflict screenshot (equity-safe)

Only if you already have access without new paid accounts: open the same cloud note in two sessions you control and look for conflict or version cues. Capture at most one scrubbed screenshot. If you lack access, skip—fixtures and Route A remain enough.

#### Route C — Offline fixture (required fallback)

Use LAB-CMS-001 fixtures / Experience B instructions when a personal device is unavailable. Treat fixture numbers and transcripts as **illustrative**, not measurements of your hardware.

#### Lifecycle adjacency — LAB-TRUST-001

For retain/share/delete language, **LAB-TRUST-001** already includes a consent/trust card and data-lifecycle vocabulary. Do not reassign that lab. Optionally complete one lifecycle row (retain / share / delete-redact) on a throwaway example after Experience B—still with redaction rules.

#### Evidence (minimum)

- observation table (Save vs non-Save, or fixture IDs),
- one scrubbed screenshot or written status list,
- one paragraph separating observation from inference,
- explicit statement: no forensic recovery attempted.

#### Limits (say them out loud)

- One reopen does not prove all future autosaves.
- Conflict UI is not a filesystem root-cause report.
- “Deleted” in a UI is not a sourced claim of global unrecoverability.
- Quartet storage benches stay PHYSICAL_PENDING.

#### Portfolio output

Follow LAB-CMS-001 portfolio norms: README (question, method, limits), observation table, teach-back (RAM vs durable file), and redaction confirmation.

---

## 8. Build it

Use the persistence story at the depth that matches your pathway.

### Explorer

Draw a personal **data lifecycle** postcard: create → use → retain → share → delete/redact for one throwaway note. Use ordinary words. Mark which stages you observed in Try it.

### Operator

From LAB-CMS-001 Experience B notes, build a symptom checklist: missing content, recovered-draft dialog, conflict banner, permission denied. Pair each with “needs more evidence”—never with fake certainty.

### Builder

Design a one-page **durability checklist** for a tiny app: when is content only in memory; when do you request a durable write; what UI cue will you show if write fails; what will you refuse to claim about fsync timing without measurement? Keep flush language conceptual [@tanenbaum-bos; @saltzer-kaashoek].

### Engineer

Compare **file vs database responsibilities** for one use case (for example, a homework tracker): what belongs in a named file, what needs structured records and concurrent updates. Keep the comparison qualitative; do not invent ACID slogans as if a pinned textbook were already cited (CLM-CH13-003 still SOURCE_NEEDED). Sketch against **FIG-CH13-004**’s teaching split.

### Researcher

State uncertainty about deletion across replicas in one careful paragraph: what a UI delete can mean, what would still be unknown without primary policy and storage documents, and why this book refuses recoverability steps. Keep Quartet endurance claims PHYSICAL_PENDING (CLM-CH13-006).

Educators can run Route C fixtures when devices cannot quit/reopen freely, and can treat redaction as a first learning outcome—not an afterthought.

---

## 9. Secure and include it

### Security

Files and databases are access-control surfaces. Ordinary posture: least privilege for shared folders, care with sync of sensitive notes, and refusal to disable security tools “to make Save faster.” This chapter does not teach unauthorized access, bypass, or recovery exploits.

### Privacy

Lifecycle honesty matters: collect, use, retain, share, and delete/redact are human stakes, not only storage jargon. Discuss deletion as **policy plus mechanism**—qualitatively. Because replica and garbage-collection recoverability claims remain SOURCE_NEEDED (CLM-CH13-005), do not assert global erasure from a trash click. Portfolio artifacts must scrub identifiers; do not sync lab evidence to cloud accounts as a requirement.

### Accessibility

Sync, save, and error status must be perceivable as text (or equivalent), not color-only dots. Conflict and offline banners should remain reachable with keyboard and screen-reader paths where the platform supports them. Filenames and paths in teaching materials need text equivalents, not screenshot-only instructions.

### Equity

Do not require paid cloud seats. Offline fixtures and local editors are first-class. Learners on shared or low-storage devices must be able to complete Experience B without buying upgrades. Backup and sync literacy includes naming cost barriers without pretending every classroom can stock every service.

### Safety and ethics

No forensics labs. No undelete cookbooks. No fabricated durability latency tables. No shipping-SKU claims about Quartet storage. Overclaiming “deleted forever” or “always synced” is still a form of false evidence.

---

## 10. Career lens

Persistence work crosses many ownership domains. No table promises employment; roles vary by organization. Artifacts from LAB-CMS-001 Experience B resemble early professional habit: prediction, observation/inference split, and explicit uncertainty.

| Layer | Example role | Professional artifact | Lab resemblance |
|---|---|---|---|
| Application durability | Backend / ROLE-BACKEND | Save/flush design notes; failure UX | Builder durability checklist |
| Filesystems / OS | Systems / OS engineer | FS and caching behavior notes | Save vs buffer separation; [@tanenbaum-bos] |
| Data platform | Data engineer | Pipeline retain/delete policy map | Explorer lifecycle postcard |
| Database operations | DBA-adjacent practitioner | Backup/restore runbooks (authorized) | Engineer file-vs-DB split (qualitative) |
| Sync / cloud | Cloud or mobile engineer | Conflict-resolution UX + limits | Operator conflict-symptom checklist |
| Privacy | Privacy engineer (see CH24) | Retention and deletion disclosures | Qualitative delete uncertainty note |
| Support / IT | Field or support engineer | Triage: unsaved buffer → disk → sync | Experience B observation table |
| Accessibility | Accessibility specialist | Status-cue perceivability review | Text status for save/sync/errors |

Portfolio hint: a scrubbed reopen table plus a lifecycle postcard is more honest than vibes-based “the cloud ate my homework.”

---

## 11. Check understanding

Answer with reasoning. Prefer short paragraphs over one-word guesses.

1. Why can content on screen disappear after quit even though you “saw it finished”?
2. Why is a Save checkmark incomplete evidence that bits are on stable media?
3. What is the difference between a **file** and a **filesystem** in one careful sentence each?
4. Why might a cloud conflict banner appear even when the local disk is healthy? What must you *not* claim without more evidence?
5. Name the lifecycle stages create → use → retain → share → delete/redact and give one human stake for delete/redact that stays qualitative.
6. Why does this chapter refuse undelete or forensic recovery steps in labs?
7. Why are Device Quartet storage endurance claims labeled PHYSICAL_PENDING?
8. **Teach-back.** Explain to a family member—without saying *write-back*, *inode*, or *replica*—why Save and “still on screen” are different promises. Then introduce those three terms one at a time, tied to something already understood.

Educator note: success is causal sequence (buffer → write → durable media → optional sync → human reopen) plus at least one privacy/uncertainty boundary, not a product catalog.

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). Project-specific Device Quartet storage evidence remains **PHYSICAL_PENDING** (CLM-CH13-006) and is tracked in the chapter claim plan, separately from external literature.

Inline citations used in this chapter include @tanenbaum-bos and @saltzer-kaashoek.

**Omitted as cited technical claims (SOURCE_NEEDED remaining in the chapter claim plan):**

- **CLM-CH13-003** — databases add structure/concurrency/recovery relative to raw files (needs a pinned database-systems textbook edition; no invented ISBN in this draft).
- **CLM-CH13-004** — cloud sync conflicts as distributed-state problems (needs distributed-systems chapter and/or official sync docs).
- **CLM-CH13-005** — deletion as policy plus garbage collection plus replicas (needs privacy/retention and storage GC primary docs; no recovery exploit steps).

Prose above treats those topics **qualitatively** or omits them as sourced claims.

---

## 12. Glossary links

Terms introduced or relied on as formal vocabulary in this chapter should resolve in the living glossary registry as candidates mature. This section lists them for linking—not as a dump of free-standing encyclopedia entries.

| Term | Role in this chapter |
|---|---|
| File | Named durable byte sequence via a filesystem |
| Filesystem | Organization of files/directories with metadata and durability rules |
| Database | Structured durable store beyond a single file blob (intro) |
| Durability | Committed data survives expected failures within assumptions |
| Cache vs durable store | Fast copies can precede stable-media durability |
| Consistency model (intro) | When readers see writers’ updates across replicas/sync |
| Data lifecycle | Create/use/retain/share/delete-redact over time |
| Deletion / redaction | Limiting availability; policy and mechanism can differ |
| Stability Contract | Experience depends on hidden conditions staying acceptable |
| Write-back / buffer | Delayed durability behind a fast Save feel |

Deeper entries and “not the same as” warnings live in the glossary network. Prefer following a link when stuck over inventing a private definition.

Related earlier chapters: memory and storage adjacency (CH07), OS abstractions (CH12). Related later chapters: networked services (CH14–CH15), privacy depth (CH24).

---

## Figure references (planned embeds; **draft-blocked** until SVG + a11y land)

All four figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured evidence. No fabricated telemetry. Device Quartet storage curves remain PHYSICAL_PENDING.

### FIG-CH13-001 — Data lifecycle (create → use → retain → share → delete/redact)

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Lifecycle diagram.
- **Reader should notice.** Ordered stages with human stakes at delete/redact; policy vs mechanism note.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name all five stages in order; state conceptual truth class; no recoverability instructions.

### FIG-CH13-002 — App buffer → filesystem → device media → optional cloud replica

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Comparative layers.
- **Reader should notice.** Left-to-right durability stack; RAM/buffer distinct from durable media.
- **Truth class.** Conceptual / Representative educational architecture.
- **Alt text requirement.** List layers in reading order; deny Quartet EVT implication.

### FIG-CH13-003 — Save click vs durability point

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** Sequence diagram.
- **Reader should notice.** Save UI precedes possible flush/fsync durability; failure branch for incomplete write.
- **Truth class.** Illustrative.
- **Alt text requirement.** Enumerate steps; label illustrative; no invented latency numbers.

### FIG-CH13-004 — File vs database responsibilities

- **Production status.** `draft-blocked` (no SVG embed in this draft).
- **Type.** System map / comparative.
- **Reader should notice.** Named bytes vs structured store responsibilities; both can fail.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name both columns; state that formal DB textbook pinning is still SOURCE_NEEDED for stronger claims.

---

## Claim footnotes used in this chapter

| Claim ID | Approved gist | Classification |
|---|---|---|
| CLM-CH13-001 | Files are ordinary persistence on personal devices; RAM is not a durable substitute | general_technical · SOURCE_IDENTIFIED via @tanenbaum-bos |
| CLM-CH13-002 | Write-back caches/buffers can delay durability; Save UI ≠ proof on stable media | general_technical · SOURCE_IDENTIFIED via @tanenbaum-bos, @saltzer-kaashoek |
| CLM-CH13-003 | Databases add structure/concurrency/recovery vs raw files | SOURCE_NEEDED — **omitted as cited claim**; qualitative responsibility split only |
| CLM-CH13-004 | Cloud sync conflicts are distributed-state symptoms, not proof FS broke | SOURCE_NEEDED — **reframed qualitatively**; observation vs inference only |
| CLM-CH13-005 | Deletion is often policy + GC + replicas; UI delete ≠ global unrecoverable | SOURCE_NEEDED — **qualitative uncertainty only**; no recovery steps |
| CLM-CH13-006 | Quartet storage endurance/performance | PHYSICAL_PENDING |

General teaching statements that working memory is volatile relative to durable files are tied to CLM-CH13-001 and the cited OS/systems texts. Any future numeric durability or endurance figures must carry **illustrative**, **measured**, or **inferred** labels—and Quartet measured figures stay blocked until PHYSICAL_PENDING clears.
