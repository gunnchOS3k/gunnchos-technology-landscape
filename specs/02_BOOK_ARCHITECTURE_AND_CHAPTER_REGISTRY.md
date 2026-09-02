# Book Architecture and Chapter Registry

# Canonical full-book architecture

The full publication contains **31 chapters in six parts**.

Do not silently rename, merge, remove, or reorder these chapters without an explicit editorial decision.

---

# Part I — Read the experience

## 1. Technology Is a System, Not a Screen

Purpose:

Establish the whole-book mental model.

Central idea:

The screen is only the visible surface of a much larger system.

## 2. Follow One Tap Through the Entire Stack

Purpose:

Demonstrate the book's experience-first method.

This is the canonical prototype chapter.

## 3. Performance: Why Technology Feels Fast, Slow, Smooth, or Unstable

Purpose:

Connect human perception to measurable system behavior.

## 4. The Device Quartet as a Learning Laboratory

Purpose:

Introduce the four recurring form factors and explain how they expose different parts of the technology ecosystem.

---

# Part II — Open the device

## 5. Electricity, Signals, Clocks, and Logic

## 6. CPU, Instructions, and Parallel Work

## 7. Memory, Cache, and Storage

## 8. Graphics, Displays, Audio, Cameras, and Sensors

## 9. Power, Batteries, Thermals, and Mechanical Design

## 10. Ports, Buses, Boards, Packaging, and Manufacturing

---

# Part III — Make hardware useful

## 11. Firmware, Boot, and Trust

## 12. Operating Systems, Processes, Threads, and Scheduling

## 13. Files, Databases, and Data Lifecycles

## 14. Applications, APIs, Runtimes, and User Interfaces

## 15. Containers, Virtualization, Cloud, and Edge Computing

---

# Part IV — Connect everything

## 16. Packets, Protocols, Routing, and the Internet

## 17. Wi-Fi, Cellular, 5G, and the Road to 6G

## 18. Spectrum, Antennas, Beams, MIMO, and Radio Conditions

## 19. NTN and Service Continuity Across Ground, Air, and Space

## 20. Latency, Reliability, QoE, and the Stability Contract

---

# Part V — Intelligence, security, and responsibility

## 21. Data, Machine Learning, and Generative AI

## 22. Edge AI, Sensors, and Embodied Interaction

## 23. Cybersecurity from Chip to Cloud

## 24. Privacy, Identity, Safety, Accessibility, and Ethics

## 25. Digital Equity: Who Benefits, Who Is Excluded, and What We Can Measure

---

# Part VI — Build, prove, and contribute

## 26. Software Development and Version Control

## 27. Testing, Observability, and Evidence

## 28. Digital Twins, Simulation, and Reproducible Research

## 29. Designing a Complete Technology Product

## 30. Career Maps and Portfolio Proof

## 31. Capstone: Explain, Measure, Improve, and Teach the Ecosystem

---

# Concept Edition

The first reader-facing release should contain six integrated chapters/modules.

## CE-1 — Technology Is a System, Not a Screen

Establishes the mental model for the entire publication.

## CE-2 — Follow One Tap Through the Entire Stack

Proves the experience-first teaching method.

## CE-3 — CPU, Memory, Storage, and the OS

Provides the essential inside-the-device foundation.

This may synthesize selected content from full-book Chapters 6, 7, and 12 while preserving the full-book architecture.

## CE-4 — Packets, Wi-Fi/Cellular, Edge and Cloud

Shows that the experience extends beyond the device enclosure.

This may synthesize selected content from Chapters 15–18.

## CE-5 — AI, Security, Privacy and Trust

Addresses consequential modern technology topics together while preserving links to full-book Chapters 21, 23, and 24.

## CE-6 — The Stability Contract + Capstone

Unifies:

- measurement,
- QoE,
- debugging,
- evidence,
- system thinking,
- teach-back.

The Concept Edition is a deliberate first edition, not a random six-chapter sample.

---

# Recurring chapter anatomy

Every complete chapter should contain the following twelve sections unless there is a documented editorial reason to deviate.

## 1. The moment

A story or use case anyone can recognize.

## 2. What you notice

The visible experience and user benefit.

## 3. Exploded ecosystem

A labeled view from physical parts through software and connectivity.

## 4. Follow the signal

A numbered journey of:

- data,
- power,
- control,
- state,
- feedback.

## 5. Component cards

For each important object:

- plain-language definition,
- analogy,
- true technical function,
- constraints,
- common failure symptoms.

## 6. Stability contract

What must remain within acceptable bounds for the experience to continue.

## 7. Try it

A safe WAIKE lab with evidence collection.

## 8. Build it

A code, configuration, hardware, or design extension.

## 9. Secure and include it

Discuss as relevant:

- threats,
- privacy,
- identity,
- accessibility,
- ethics,
- equity,
- safety.

## 10. Career lens

Identify:

- roles,
- tools,
- artifacts,
- review criteria,
- portfolio evidence.

## 11. Check understanding

Include:

- concept questions,
- system tracing,
- misconception checks,
- teach-it-back challenge.

## 12. Glossary links

Include:

- terms introduced,
- prerequisites,
- related concepts,
- linked chapters,
- linked labs.

---

# Required chapter metadata

Each chapter directory should have structured metadata.

Recommended schema:

```yaml
chapter_id: CH02
chapter_number: 2
title: Follow One Tap Through the Entire Stack
part: I
status: draft
concept_edition: true

human_question:
  - What actually happens when I tap a button?

experience:
  - responsive touch interaction

reader_paths:
  - explorer
  - operator
  - builder
  - engineer
  - researcher
  - educator

systems:
  - input
  - operating-system
  - application
  - networking
  - rendering

devices:
  - student-14-5
  - handheld-hybrid
  - ds-xl-coder
  - edge-io-wearables

labs:
  - LAB-TAP-001

figures:
  - FIG-CH02-001
  - FIG-CH02-002

concepts:
  introduced: []
  required: []
  related: []

waike:
  mapped: true
  courses: []

claims:
  registry: evidence/claim_registry.yaml
```

---

# Chapter completion definition

A chapter is not complete merely because prose exists.

A chapter is complete only when all required categories are satisfied.

## Narrative

- opening human experience exists,
- explanations remain coherent,
- reader can follow the system path.

## Systems

- physical layer represented,
- software layer represented,
- data/control path represented,
- relevant network behavior represented,
- human outcome represented.

## Reader pathways

At minimum:

- Explorer route,
- Operator route,
- Builder route,
- Engineer route,
- Researcher extension,
- Educator note.

## Visuals

- required diagrams exist,
- source files exist,
- alt text exists,
- reading order exists,
- conceptual vs implemented status is explicit.

## Glossary

- introduced terms registered,
- cross-references valid,
- no circular definition dependency.

## Lab

- runnable baseline route,
- no-specialized-hardware alternative,
- evidence artifact,
- portfolio output,
- safety guidance.

## Evidence

- citations present,
- repository-specific claims registered,
- status language valid,
- unsupported claims blocked or marked pending.

## Careers

- responsible roles identified,
- tools/artifacts identified,
- portfolio relationship explained.

## Responsibility

Where relevant:

- security,
- privacy,
- accessibility,
- ethics,
- digital equity,
- safety.

---

# Chapter status vocabulary

Allowed chapter statuses:

- `outline`
- `scaffold`
- `draft`
- `technical-review`
- `editorial-review`
- `reader-test`
- `release-candidate`
- `published`

Do not mark a chapter `release-candidate` while major diagrams, labs, or evidence remain placeholders.

---

# Dependency architecture

The book should maintain a prerequisite graph.

Examples:

```text
Technology Is a System, Not a Screen
    ↓
Follow One Tap Through the Entire Stack
    ↓
Performance
    ↓
CPU / Memory / OS
    ↓
Applications / Networking
    ↓
Wireless / Cloud / AI / Security
    ↓
Evidence / Digital Twins / Product Design
    ↓
Capstone
```

The graph must not require strict linear reading.

Instead, it should allow pathway navigation.

Examples:

### Wireless pathway

1 → 2 → 3 → 16 → 17 → 18 → 19 → 20 → 28

### Software pathway

1 → 2 → 6 → 7 → 12 → 14 → 15 → 26 → 27

### AI pathway

1 → 2 → 7 → 14 → 15 → 21 → 22 → 23 → 27

### Device engineering pathway

1 → 2 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 29

### Cybersecurity pathway

1 → 2 → 11 → 12 → 14 → 16 → 23 → 24 → 27

### Research pathway

1 → 2 → 3 → domain chapters → 27 → 28 → 31

---

# Chapter authoring rule

Do not write 31 superficial AI-generated chapters merely to achieve file count.

The full-book architecture may be scaffolded, but manuscript depth should progress in this order:

1. Chapter 2 canonical prototype
2. six-chapter Concept Edition
3. validation with readers/educators
4. remaining full manuscript
