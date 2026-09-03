---
status: draft
chapter_id: CH11
chapter_number: 11
title: "Firmware, Boot, and Trust"
author: "Edmund Gunn, Jr."
part: III
concept_edition: false
manuscript_status: WORKING_DRAFT_COMPLETE
human_validation_status: PENDING_FULL_MANUSCRIPT_REVIEW
publication_status: NOT_PUBLICATION_READY
labs: [LAB-BOOT-OBS-001]
figures:
  - FIG-CH11-001
  - FIG-CH11-002
  - FIG-CH11-003
  - FIG-CH11-004
---

# Chapter 11 — Firmware, Boot, and Trust

**Status:** `draft` · **Chapter ID:** `CH11`  
**Author:** Edmund Gunn, Jr.  
**Manuscript:** working draft complete · human validation pending · not publication-ready  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (no Gate 3 PASS claimed)

---

## 1. The moment {#sec-moment}

You press the power button—or wake a phone that was only sleeping. A logo appears. Lights blink. A spinner turns. Then, if you are lucky, a lock screen or desktop. If you are unlucky: an endless logo, a recovery menu you did not ask for, or a warning that software could not be verified.

From the seat it feels like one event: *booting*.

Underneath that feeling, early software called **firmware** initializes hardware that Part II treated as ports, buses, boards, power, and compute. A **boot sequence** hands capability and—when the platform is designed for it—trust checks from stage to stage until an operating system can present something a person recognizes. None of that is the app you will open later. The lock screen is not the same thing as “secure boot.” A marketing checkbox is not a measured attestation result.

This chapter opens Part III: making hardware useful by naming the first software abstractions that sit between raw silicon and a usable computer—and by separating **trust intent**, **user authentication**, and **authorization** before deeper security chapters arrive.

The governing question:

> When I press power, what ordered handoffs must succeed—and what would honest failure look like—before I can trust this device enough to type a password?

---

## 2. What you notice {#sec-notice}

Before words like *root of trust* or *measured boot* enter, notice the human contract you already expect.

You expect the device to become interactive in a bounded time—or to fail in a way a person can understand. You expect logos and spinners to mean “still working,” not “silently dead.” You expect update banners and recovery screens to be readable, not logo-only mysteries. You expect that entering a PIN or password proves *you* to the device—not that every piece of software that ran before the lock screen was authentic. You also expect that a feature named “secure boot” on a settings page or a sticker is a claim about **policy intent**, not automatic proof that *your* unit measured and attested a known-good chain.

Those expectations are the product, from the person’s point of view.

**A successful boot is a human perception produced by ordered handoffs: firmware init, bootloader load, OS start, and only then the familiar UI—plus trust checks that may pass, fail visibly, or (on weaker designs) be absent.**

Notice the split timelines. Hardware can power on while storage is still probing. A logo can freeze while a verification step waits. A lock screen can appear after a chain that never verified anything cryptographic at all. Cold boot, warm wake from sleep, and “restart after update” can feel similar while using different paths underneath.

Optional comparison on a device you already own: cold boot once (power fully off, then on), then wake from sleep if the device supports it. Record only what you can see—lights, logos, banners, lock screen, wall-clock time bands if you watch a clock. Do not flash firmware. Do not enter recovery menus you do not already know how to exit safely. Label every causal guess as inference.

---

## 3. Exploded ecosystem {#sec-ecosystem}

Boot is not a single object. It is a path through an ecosystem. **FIG-CH11-001** (conceptual) is the first-minute map: power/reset → firmware → bootloader → kernel → userspace → lock screen or recovery. Treat it as **Representative educational architecture**, not a claim that every phone or laptop implements identical stages with identical names.

Walk the layers in ordinary language, then keep the same layers when vocabulary deepens.

### Human

You form intent: start working, check a message, recover a broken update. Hands press power. Eyes watch logos. Later, fingers meet a lock screen or a recovery choice. Accessibility matters already: if failure is logo-only, some readers are excluded before any app exists.

### Firmware

**Firmware** is software that runs early to initialize and configure hardware so later software can treat devices as usable abstractions [@tanenbaum-bos; @saltzer-kaashoek]. It may live in flash, ROM, or vendor-partitioned storage. It is not “the whole computer,” and it is not the app. It is the first cooperating software story after electricity and clocks become usable.

### Root of trust

A **root of trust** is a hardware and/or firmware foundation that later verification steps depend on. If that foundation is weak or bypassed by design, later “secure” labels inherit the weakness. Teaching the idea does not require inventing a measured root for the reader’s sealed device.

### Bootloader

A **bootloader** loads and starts an operating-system image (or another stage). It is a handoff program—not the OS, and not proof that the image is authentic unless a separate policy checks signatures or measurements [@tanenbaum-bos].

### Operating system kernel and userspace

The kernel takes control of privileged hardware mediation; userspace eventually presents the lock screen, desktop, or launcher. Chapter 12 deepens processes and scheduling. Here, keep the honesty rule: the familiar UI is late in the chain.

### Trust policy vs user proof

**Secure boot** (policy intent) tries to constrain which software may run during boot [@uefi-secure-boot-2.10]. **Authentication** at the lock screen asks who the user is. **Authorization** decides what that authenticated identity may do afterward. Collapsing those three into one word—“security”—is how marketing language and literacy diverge. CE-5 adjacency (AI, identity, privacy, and trust) owns richer consent and AI×trust synthesis; this chapter only needs the boot-time distinction clear.

### Updates and recovery (preview)

Platforms often provide alternate paths when primary images fail verification or when an update leaves the device needing an honest recovery UI. Naming the path is literacy. Inventing vendor-specific brick rates or Quartet EVT recovery timings is not. Device Quartet boot and firmware behavior remains **PHYSICAL_PENDING** research form-factor context only (CLM-CH11-005).

**FIG-CH11-002** (conceptual) later sketches root-of-trust → verified stages as policy intent—not a product badge for any reader’s unit.

---

## 4. Follow the signal {#sec-signal}

**FIG-CH11-001** (conceptual sequence) shows a numbered path. Read it as a logical story, not as a universal SoC bring-up with invented millisecond budgets.

1. **Power / reset.** Energy and clocks become available enough for early code to run (Chapter 5 and Chapter 9 adjacency). Incomplete power is an observation domain, not a root-cause claim from outside.
2. **Firmware init.** Early software probes memory controllers, storage, display, and input paths enough for later stages—or fails before anything readable appears [@tanenbaum-bos].
3. **Root-of-trust decision point (when present).** A foundation component may hold keys, measurements, or immutable code that later checks depend on [@saltzer-kaashoek]. Absence of this step on some devices is itself a fact pattern—not a moral judgment about the owner.
4. **Bootloader handoff.** Control transfers to a program that can find and load an OS image [@tanenbaum-bos].
5. **Secure-boot policy check (when enabled).** Signature or authentication-info checks may allow, deny, or divert the next image according to platform policy [@uefi-secure-boot-2.10]. A settings toggle labeled “secure boot” does not, by itself, prove your unit’s configuration matched a lab measurement.
6. **Optional measurement recording.** Some platforms record digests of boot components into registers or logs for later **attestation**—evidence about what ran, distinct from locking a policy and distinct from a PIN entry [@tcg-pc-client-pfp-1.06].
7. **Kernel start → userspace.** Privileged software takes over resource mediation; services start; the lock screen or desktop becomes possible.
8. **Human feedback.** Logo ends; lock screen, desktop, recovery UI, or an unverified-software warning closes the loop—or fails to.

### Alternate paths (the honesty rule)

Not every boot is a cold power-on. Sleep/wake may skip much of the chain. Recovery environments may load different images on purpose. Some embedded devices never show a lock screen. Teaching those forks prevents the encyclopedia trap: listing every vendor bootloader name instead of tracing one honest path.

### Failure branch without drama

When something fails, prefer failure *domains* over confident blame:

- Power / incomplete init (still a hypothesis until evidenced)
- Storage or image not found
- Verification / policy deny
- Update mid-state requiring recovery affordance (qualitative Stability Contract concern; see Section 6)
- User-visible UI crash after a successful-enough boot

Outside observation rarely distinguishes those cleanly. That limitation is literacy.

---

## 5. Component cards {#sec-components}

For each object: plain language, analogy, technical function, constraints, common symptoms. Analogies are labeled as analogies.

### Firmware

- **Plain language.** Early software that initializes hardware and often participates in boot trust.
- **Analogy (labeled).** Like stage crew before the curtain—necessary, mostly invisible, not the play.
- **Technical function.** Configures devices and prepares abstractions later software can use [@tanenbaum-bos; @saltzer-kaashoek].
- **Constraints.** Flash size, update risk, vendor lock regions, platform diversity (do not universalize one SoC sequence).
- **Symptoms.** No display, endless logo, partial bring-up (fans/lights without UI).

### Boot sequence

- **Plain language.** Ordered handoff from power/reset through firmware and bootloader into an OS.
- **Analogy (labeled).** Like a relay race—dropping the baton at any handoff ends the experience.
- **Technical function.** Sequences capability and optional trust checks before userspace [@tanenbaum-bos].
- **Constraints.** Timing expectations are product-specific; this book does not invent them.
- **Symptoms.** Hang at a recognizable stage; reboot loops; recovery entry.

### Bootloader

- **Plain language.** Program that loads and starts an OS image.
- **Analogy (labeled).** Like a ferry that only carries what it is given—or what policy allows.
- **Technical function.** Locates, loads, and transfers control to the next image [@tanenbaum-bos].
- **Constraints.** Storage layout, signing policy, rollback rules (vendor-specific).
- **Symptoms.** “No bootable device,” wrong-slot boot, recovery menu.

### Root of trust

- **Plain language.** Foundation whose integrity later verification depends on.
- **Analogy (labeled).** Like the first trustworthiness of a measuring stick—everything measured inherits its limits.
- **Technical function.** Anchors keys, immutable code, or measurement facilities for later stages [@saltzer-kaashoek; @tcg-pc-client-pfp-1.06].
- **Constraints.** Physical access models, supply-chain assumptions, design threats out of Explorer scope.
- **Symptoms.** Usually invisible; learner sees downstream verify failures, not the root itself.

### Secure boot (intent)

- **Plain language.** Boot-time policy intending to run only authorized software images.
- **Analogy (labeled).** Like a door policy for which costumes may enter the stage—not a name badge for the audience.
- **Technical function.** Constrains executable images via platform authentication/signing mechanisms [@uefi-secure-boot-2.10].
- **Constraints.** Key management, policy misconfiguration, update compatibility; **feature name ≠ measured guarantee for your device**.
- **Symptoms.** Unverified software warnings; refusal to boot unsigned images; surprising “secure boot off” after a repair.

### Measured boot and attestation (concepts)

- **Plain language.** Recording what ran (measurement) and producing evidence about that state (attestation).
- **Analogy (labeled).** Like a sealed flight recorder versus a locked cockpit door—related aviation ideas, different jobs.
- **Technical function.** Measurement logs / platform configuration registers support attestation uses distinct from UI authentication [@tcg-pc-client-pfp-1.06].
- **Constraints.** Evidence must be requested and interpreted; slogans are not attestations. No fabricated quotes or PCR values in this chapter.
- **Symptoms.** Remote “device not trusted” at work (when an enterprise system actually checks evidence); local PIN success despite never attesting anything.

### Recovery / fail-safe path

- **Plain language.** Alternate boot environment when primary images fail verification or update.
- **Analogy (labeled).** Like a clearly marked emergency exit—useful only if a person can find and read it.
- **Technical function.** Loads a known recovery image or menu so the device can become honest again instead of silently unusable.
- **Constraints.** Requires readable messaging and reachable controls; equity: not every learner has a spare device.
- **Symptoms.** Recovery menus, “update failed” banners, limited function until repair completes.

---

## 6. Stability contract {#sec-stability}

A boot experience continues only while multiple hidden conditions stay within acceptable bounds.

Definition used throughout this book: a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

For the ordinary “I pressed power and got a trustworthy-enough computer” feeling, conditions like these must hold together (qualitative; no invented numeric budgets):

1. **Firmware completes enough init** for storage, display, and input paths the experience needs.
2. **Boot chain reaches** an intended OS **or** an honest recovery UI—not a silent brick from the learner’s view.
3. **Trust policy matches learner expectation**, or failure is visible rather than silent.
4. **Update state** does not leave the device mid-change without a recovery affordance the person can understand (teaching concern; interrupted-update failure modes as a formal claim remain **SOURCE_NEEDED** and are **omitted** here as CLM-CH11-006—see blockers).
5. **Accessibility:** boot and recovery messages have readable or alternate paths where the platform allows—not logo-only dead ends when text is possible.

A system can remain *electrically on* while the human experience has already failed: endless logo, inaccessible verify step, lock screen that appears after an unverified chain the person never consented to trust. Conversely, a lock screen can look “secure” while secure-boot policy was never enabled. Stability is concurrent conditions—not a single spinner.

**Honesty bound for this edition:** Device Quartet boot/firmware measurements are not claimed as completed physical evidence (CLM-CH11-005). Commodity observation in **LAB-BOOT-OBS-001** produces *your* evidence for *your* device—not a universal secure-boot score and not an attestation quote.

CE-5’s stability sketch (answer usability, identity continuity, authorization clarity, accessible trust) is **adjacent** for later identity and AI chapters. This chapter’s contract stays on power-on → trustworthy-enough computer.

---

## 7. Try it {#sec-try}

### LAB-BOOT-OBS-001 — Observe Boot and Wake (publication-owned, proposed)

**Goal.** Observe cold boot vs wake (and any already-visible update/recovery banners) on a commodity device you own—or complete the offline fixture route—without flashing, unlocking, or bypassing anything.

**WAIKE alignment note.** WAIKE accepted `main` includes adjacent embedded bring-up and QEMU neighbors (`EMBEDDED_PROTOTYPING` / `HARDWARE_ENGINEERING` digital_rc adjacency at SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`). Those are competency adjacencies. They are **not** renamed as publication lab IDs. **LAB-BOOT-OBS-001** is publication-owned. **LAB-TRUST-001** (CE-5) is trust/consent adjacency only—do not treat it as this chapter’s lab. Forward chip-to-cloud depth to Chapter 23.

**Safety (hard stops).**

- Do not open sealed devices.
- Do not flash, unlock, jailbreak, or bypass secure boot / recovery protections.
- Do not enter recovery modes you do not already know how to exit safely.
- No Device Quartet fabrication or EVT timing claims.
- Redact account identifiers, photos of others’ screens, and secrets from artifacts.

**Routes.**

- **Commodity route.** One phone or laptop you already own and may power cycle safely.
- **Offline fixture route.** Use a provided boot-symptom card and worksheet without hardware (equity default).

**Explorer baseline (about 40–50 minutes).**

1. Predict stages before power: firmware → bootloader → OS → lock screen (or “unknown”).
2. Cold boot once—or study the fixture card.
3. If safe and already familiar, wake from sleep once and compare observations.
4. Record observations only: lights, logos, banners, lock screen, coarse wall-clock bands.
5. Draw a labeled boot-chain diagram for one device class (phone or laptop).
6. Fill an observation-vs-inference table. Every causal guess needs a note about extra evidence required.
7. Teach-back in one sentence: why the lock screen is not secure boot.

**Operator extension.** Note any update-pending or recovery banner text already visible. Classify symptoms into domains (power/init, policy/verify, update/recovery, post-boot UI)—without claiming root cause.

**Builder extension.** Clean one-page diagram another student could follow without opening any device. Annotate visible vs sealed stages.

**Engineer extension.** Separate *secure-boot policy intent* from *attestation evidence*. List what evidence would be required before claiming “this device attested a known-good boot” [@uefi-secure-boot-2.10; @tcg-pc-client-pfp-1.06]. Still no flashing.

**Researcher extension.** State a hypothesis about one boot failure mode (for example, update-related recovery entry), name ethical variables, and list limitations. Explicitly forbid inventing Quartet timings or citing CLM-CH11-006 until sources exist.

**Evidence to keep.** Boot-chain diagram; observation-vs-inference table; scrubbed notes; teach-back paragraph. Prefer synthetic descriptions over photos of classmates’ devices.

Optional Operator post-boot health path: **LAB-CMS-001** (CE-3 adjacency) after a slow or failed boot narrative—do not duplicate CMS as Ch11 core.

---

## 8. Build it {#sec-build}

Extend LAB-BOOT-OBS-001 without turning Part III into a firmware flashing course.

### Explorer

Build a pocket card: firmware vs bootloader vs OS vs app, with one plain sentence each, plus “lock screen ≠ secure boot.”

### Operator

Build a boot-symptom checklist that starts with observed logos/banners and ends with “needs more evidence”—never with fake certainty about root cause.

### Builder

Build a labeled diagram (paper or digital) of power → firmware → bootloader → kernel → lock screen for one owned device class. Annotate where secure-boot policy *might* sit without claiming your unit’s configuration. Optional: second small diagram for sleep/wake as a shortened path.

### Engineer

Build a one-page evidence plan: what would convert “marketing secure boot” into a justified trust claim for *one* device (policy state, measurement logs, attestation quote, update authenticity). Mark each row “observable in lab,” “needs enterprise tooling,” or “out of scope.” Cite standards vocabulary rather than inventing PCR values [@uefi-secure-boot-2.10; @tcg-pc-client-pfp-1.06].

### Researcher

Build an evidence plan for a claim you are *not* allowed to assert yet—for example, interrupted firmware updates as a Stability Contract failure mode—keeping CLM-CH11-006 **SOURCE_NEEDED** / omitted, and Quartet boot claims **PHYSICAL_PENDING** (CLM-CH11-005).

Educators can facilitate Section 11 teach-backs and keep classrooms on the offline fixture route when admin rights or spare devices are unavailable.

---

## 9. Secure and include it {#sec-secure-include}

### Security — authentication vs authorization vs boot authenticity

Keep three ideas separate; CE-5 adjacency reinforces them for identity and AI contexts, and Chapter 23 deepens chip-to-cloud security.

| Idea | Plain question | Boot-chapter example |
|---|---|---|
| **Authentication** | Who is acting? | Unlocking with PIN, password, or biometrics |
| **Authorization** | What may they do once identified? | After unlock, may this account change firmware settings? |
| **Software authenticity / secure boot** | May this image run? | Policy constraining bootloader/OS images [@uefi-secure-boot-2.10] |
| **Attestation** | What evidence shows what ran? | Measurement/attestation mechanisms distinct from UI login [@tcg-pc-client-pfp-1.06] |

A person can authenticate successfully on a device that never enforced secure boot. A platform can refuse an unsigned image (authenticity policy) while still leaving authorization decisions to later OS policy. Classic protection and naming discipline still apply: names and boundaries matter [@saltzer-kaashoek; @tanenbaum-bos].

No exploit, unlock, or bypass guidance belongs here. Prefer update authenticity literacy and least privilege over cleverness.

### Privacy

Boot logs, serials, and recovery screenshots can become identifiers. LAB-BOOT-OBS-001 artifacts must not capture account tokens or photos of other people’s devices without consent. Scrub before portfolio save. **LAB-TRUST-001** consent-card craft remains available as adjacent practice—not a requirement to complete this chapter.

### Accessibility

Boot and recovery are accessibility surfaces. Logo-only failure states exclude readers who need text. Color-only “error red” is insufficient. Keyboard or assistive paths to recovery choices matter when platforms provide them. Document steps in words, not only screenshots.

### Equity

Not every learner has a spare device, admin rights, or a laptop that shows firmware menus. Observation-only commodity routes and offline fixtures are the equity default. Recovery literacy must not assume a second phone in the backpack.

### Safety

No flashing. No forced recovery experiments. No intentional bricking. Power and battery hard stops from Chapter 9 still apply.

### Ethics

Do not claim measured attestation results you did not obtain. Do not treat a feature name as proof. Do not invent Quartet EVT boot timings. Overclaiming trust is still false evidence.

---

## 10. Career lens {#sec-career}

One power press crosses many ownership domains. No table promises employment; roles vary by organization. LAB-BOOT-OBS-001 artifacts resemble early professional evidence in miniature: labeled diagrams, observation discipline, and explicit uncertainty.

| Role lens | Typical artifacts | Review questions |
|---|---|---|
| Firmware / embedded bring-up | Bring-up notes, flash maps (when authorized) | What initialized first—clocks, memory, or storage? |
| Bootloader / platform software | Signed image pipelines, rollback policy | What fails closed vs fails open? |
| Kernel / driver | Initcall order, device readiness | Which devices must exist before userspace? |
| Security engineer | Secure-boot policy, attestation design | Intent vs evidence distinguished? |
| SRE / fleet ops | Update rings, recovery runbooks | Is failure readable at human scale? |
| Accessibility / support | Recovery copy, alternate paths | Can someone exit recovery without vision-only cues? |

Portfolio hint: a scrubbed boot-chain diagram plus “lock screen ≠ secure boot ≠ attestation” teach-back is more honest than a vibes-based “my phone is secure” claim.

---

## 11. Check understanding {#sec-check}

**Concept.** In one sentence each, define *firmware*, *bootloader*, and *secure boot (intent)* so that none of them swallows the other two.

**System tracing.** Trace a familiar cold boot from power press to lock screen in numbered steps. Mark which steps you observed and which you inferred.

**Misconception check.** Why is “I typed my PIN, so secure boot worked” incomplete? Which ideas did that sentence collapse?

**Misconception check.** Why must authentication and authorization stay distinct after the lock screen appears?

**Teach-it-back.** Explain to a newcomer—using only LAB-BOOT-OBS-001 vocabulary—why a logo can spin forever without proving whether verification failed.

**Researcher prompt.** What evidence would convert a PHYSICAL_PENDING Quartet boot/firmware claim into a documented physical claim? What remains out of scope for a commodity classroom lab? What would be required before promoting interrupted-update failure modes out of SOURCE_NEEDED (CLM-CH11-006 omitted)?

---

## References

Selected authoritative sources for this chapter’s general technical explanations are listed in the bibliography (`book/references/references.bib`). Project-specific Device Quartet boot/firmware status remains **PHYSICAL_PENDING** (CLM-CH11-005). Interrupted firmware-update failure modes remain **SOURCE_NEEDED** (CLM-CH11-006) and are omitted as cited claims in this draft.

Inline citations used in this chapter include @tanenbaum-bos, @saltzer-kaashoek, @uefi-secure-boot-2.10, and @tcg-pc-client-pfp-1.06.

CE-5 preproduction (`publication/preproduction/ce-05/`) is trust/identity/privacy adjacency; it does not replace this chapter’s boot literacy. Full-book human validation remains deferred until the full manuscript draft exists (`publication/full31/VALIDATION_SEQUENCE_DECISION.md`). This chapter does **not** claim Gate 3 PASS.

---

## 12. Glossary links {#sec-glossary}

Candidate terms introduced or reinforced here (see also chapter glossary candidates; do not treat this list as an auto-merge into the live glossary):

| Term | Plain link |
|---|---|
| Firmware | Early software that initializes hardware and may participate in boot trust |
| Boot sequence | Ordered handoff from power/reset to firmware to bootloader to OS |
| Bootloader | Program that loads an OS image and transfers control |
| Root of trust | Foundation whose integrity later verification depends on |
| Secure boot | Boot-time policy intending to run only authorized images |
| Measured boot | Recording measurements of boot components for later evidence |
| Attestation | Producing evidence about a device’s software state |
| Recovery mode | Alternate boot path when primary images fail |
| Authentication | Establishing who is acting (e.g., lock-screen proof) |
| Authorization | Deciding what an authenticated identity may do |
| Stability contract | Concurrent conditions that keep the boot experience alive |

Related earlier chapters: system lens (CH01), signals/power adjacency (CH05, CH09), ports/boards handoff (CH10). Related later chapters: operating systems (CH12), cybersecurity chip-to-cloud (CH23), privacy/identity/ethics (CH24). LAB-TRUST-001 adjacency: CE-5 / CH23 forward link only.

---

## Figure references (planned embeds; accessibility metadata)

All four figures are **conceptual / illustrative teaching aids** unless a future revision replaces them with measured evidence. No fabricated telemetry or attestation quotes.

### FIG-CH11-001 — Power → firmware → bootloader → kernel → lock screen

- **Type.** Sequence diagram.
- **Reader should notice.** Ordered handoff plus optional recovery branch; lock screen is late.
- **Truth class.** Conceptual.
- **Alt text requirement.** List stages in order; name recovery branch; state conceptual truth class; deny universal timings.

### FIG-CH11-002 — Root of trust → verified stages

- **Type.** System map.
- **Reader should notice.** Policy intent layers—not a product badge for the reader’s device.
- **Truth class.** Conceptual.
- **Alt text requirement.** Name root and stages; state that presence of a marketing name is not measured proof.

### FIG-CH11-003 — Lock screen vs secure boot

- **Type.** Comparative layers.
- **Reader should notice.** User authentication vs software authenticity policy; authorization as a third idea.
- **Truth class.** Illustrative.
- **Alt text requirement.** Name both columns (and authz callout); forbid color-only encoding.

### FIG-CH11-004 — Update failure → recovery → outcomes

- **Type.** Failure map.
- **Reader should notice.** Readable recovery vs unusable outcomes as Stability Contract teaching—not vendor brick statistics.
- **Truth class.** Conceptual.
- **Alt text requirement.** List branches; mark CLM-CH11-006 omitted / SOURCE_NEEDED for formal interrupted-update claims; mark Quartet PHYSICAL_PENDING.

---

## Claim footnotes used in this chapter

- **CLM-CH11-001.** Firmware initializes hardware for later abstractions—textbook framing [@tanenbaum-bos; @saltzer-kaashoek].
- **CLM-CH11-002.** Boot as ordered handoff—not a single mysterious OS appearance [@tanenbaum-bos].
- **CLM-CH11-003.** Secure boot as policy intent; feature name ≠ measured guarantee for a reader’s device [@uefi-secure-boot-2.10].
- **CLM-CH11-004.** Attestation / measured boot distinct from UI lock screens [@tcg-pc-client-pfp-1.06].
- **CLM-CH11-005.** Device Quartet boot/firmware behavior **PHYSICAL_PENDING**; research form factors only.
- **CLM-CH11-006.** **OMITTED as cited claim** (`SOURCE_NEEDED`—pin vendor/OS capsule or A/B update recovery docs before promoting). Recovery paths appear only as qualitative Stability Contract teaching.
