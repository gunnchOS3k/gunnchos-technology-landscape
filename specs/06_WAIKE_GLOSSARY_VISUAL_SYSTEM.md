# WAIKE, Glossary, Visual, and Career System

# 1. WAIKE lab framework

Every lab is evidence-generating.

Completion is not:

> "I ran the command."

Completion is:

> "I can support a claim with an artifact."

---

# 2. Canonical lab schema

Recommended structured representation:

```yaml
lab_id: LAB-TAP-001
title: Trace and Measure One Tap
chapter: CH02

question: ""
experience: ""

reader_paths:
  baseline: explorer
  extensions:
    - operator
    - builder
    - engineer
    - researcher

prerequisites:
  concepts: []
  safety: []
  time_minutes: 45
  equipment: []
  software: []

accessible_routes:
  no_specialized_hardware: true
  supplied_trace: true
  simulation: false

prediction:
  required: true

procedure:
  checkpoints: []
  rollback: []

evidence:
  required_artifacts: []

interpretation:
  observation_required: true
  inference_required: true
  causation_warning: true

limits:
  confounders: []
  uncertainty: []

portfolio:
  outputs: []

teach_back:
  required: true
```

---

# 3. Anchor lab system

The full book should develop anchor labs including:

## Trace one tap

Experience:

A button responds.

Concepts:

- event pipeline,
- process,
- device input,
- rendering.

Accessible route:

- browser developer tools,
- supplied trace.

## Make slowness visible

Experience:

An app becomes sluggish.

Concepts:

- CPU,
- memory,
- storage,
- scheduling.

Accessible route:

- system monitor,
- scripted workload.

## Keep the session stable

Experience:

A video call survives load.

Concepts:

- QoE,
- latency,
- jitter,
- packet loss,
- contention.

Accessible route:

- network emulator,
- prepared trace.

## Find the thermal limit

Experience:

Performance changes over time.

Concepts:

- power,
- heat,
- thermal throttling,
- enclosure design.

Accessible route:

- public data,
- simulation.

## Follow a packet

Experience:

A request reaches a service.

Concepts:

- DNS,
- protocols,
- routing,
- encryption,
- edge/cloud.

Accessible route:

- privacy-safe packet capture.

## Compare local and remote AI

Experience:

An AI feature answers.

Concepts:

- inference,
- data movement,
- latency,
- privacy,
- energy.

Accessible route:

- small local model,
- recorded benchmark.

## Break and restore trust

Experience:

A system rejects tampering.

Concepts:

- boot chain,
- identity,
- permissions,
- updates.

Accessible route:

- container/VM scenario.

## Model a radio handoff

Experience:

A mobile interaction continues.

Concepts:

- signal,
- cells,
- beam selection,
- mobility,
- continuity.

Accessible route:

- Sionna/ns-3 trace,
- supplied simplified data.

## Measure inclusion

Experience:

Users experience unequal service.

Concepts:

- access,
- affordability,
- accessibility,
- reliability.

Accessible route:

- community scenario,
- transparent metric set.

---

# 4. Lab writing rules

Every lab must include:

## Question

One observable question.

## Prerequisites

Include:

- concepts,
- time,
- equipment,
- software,
- safety,
- no-hardware alternative.

## Prediction

The learner states what they expect.

## Procedure

Reproducible steps.

Include checkpoints.

Include rollback.

## Evidence

Examples:

- log,
- screenshot,
- measurement,
- packet trace,
- source diff,
- result table.

## Interpretation

Require two sections:

### Observation

What happened.

### Explanation

What may explain it.

## Limits

Require:

- uncertainty,
- confounders,
- device-specific behavior,
- unsupported conclusions.

## Extension

Builder and researcher variants.

## Teach-back

Explain the result to someone without a technical background.

## Portfolio output

Minimum:

- concise README,
- figure,
- result table,
- reflection.

---

# 5. Glossary architecture

The glossary is structured data.

Recommended schema:

```yaml
- id: cache
  term: Cache
  acronym: null

  plain_definition: >
    Small, fast memory that keeps likely-needed data close to a processor.

  technical_definition: >
    ...

  experience_benefit: >
    Reduces waiting and helps work continue smoothly.

  analogy:
    text: >
      A small workbench holding tools you are likely to need next.
    explicitly_labeled: true

  not_the_same_as:
    - permanent-storage

  failure_or_limit:
    - stalls
    - lower-performance
    - increased-energy

  measure_it:
    - compare workload behavior with different working-set sizes

  related:
    - cpu
    - locality
    - ram
    - memory-hierarchy
    - latency
    - power

  introduced_in:
    - CH07

  labs: []

  careers: []
```

---

# 6. Glossary editorial rules

Every entry should answer:

- What is it?
- What does it do?
- Why does a person care?
- What is it often confused with?
- What happens when its limits matter?
- How could I observe or measure it?
- What concepts connect to it?

Analogies must say they are analogies.

Do not let analogy replace technical meaning.

Avoid circular definitions.

Bad:

> "A process is something managed by the process manager."

Better:

> "A process is a running instance of a program, together with the resources and execution state the operating system manages for it."

Then provide deeper detail.

---

# 7. Concept graph

Maintain:

- `concept_registry.yaml`
- `prerequisites.yaml`
- `relationships.yaml`

Relationship examples:

- `part-of`
- `uses`
- `depends-on`
- `produces`
- `transmits`
- `controls`
- `stores`
- `protects`
- `measures`
- `often-confused-with`

This allows the web edition to become a navigable technology map.

---

# 8. Visual grammar

The reader should learn how to read the book's diagrams.

Use consistent visual types.

## Hero exploded view

Shows:

- physical layers separated in space.

Each label includes:

- part name,
- plain-language role,
- experience benefit,
- failure symptom.

## End-to-end experience map

Shows:

- human action,
- sensing,
- compute,
- network,
- service,
- feedback.

Required:

- numbered order,
- data/control/power distinctions,
- latency/stability annotation.

## Component cutaway

Shows:

- internal transformation.

Examples:

- CPU core,
- memory hierarchy,
- radio chain,
- battery path,
- sensor pipeline.

Required:

- input,
- transformation,
- output,
- constraints.

## Stability budget

Shows where:

- time,
- energy,
- heat,
- memory,
- reliability

are consumed.

If values are shown, classify as:

- target,
- observed,
- illustrative,
- simulated.

## Cross-layer sequence

Shows events across:

- application,
- OS,
- hardware,
- radio,
- edge/cloud.

Required:

- actors,
- messages/events,
- duration where defensible,
- retry,
- failure branch.

## Compare-and-choose plate

Shows architecture alternatives.

Required:

- benefit,
- cost,
- risk,
- inclusion impact,
- evidence.

## Career artifact

Shows something professionals actually produce.

Required:

- role,
- tool,
- artifact,
- review criterion,
- student portfolio analogue.

---

# 9. Visual rule

Every labeled object must answer:

1. What is it?
2. What does it do?
3. What changes for the person when it works well—or fails?

---

# 10. Accessibility for visuals

Every visual needs:

- figure ID,
- title,
- concise alt text,
- long description,
- numbered reading order where complex,
- caption,
- source,
- conceptual/implementation status.

Never rely on color alone.

If arrows use different meanings, distinguish using:

- labels,
- arrow styles,
- patterns,
- text.

---

# 11. Career system

Create a structured role registry.

Recommended schema:

```yaml
- role_id: ROLE-OS-ENGINEER
  title: Operating Systems Engineer

  owns:
    - scheduling
    - memory-management
    - kernel-subsystems

  layers:
    - operating-system

  tools:
    - debugger
    - profiler
    - tracing

  artifacts:
    - patch
    - performance-trace
    - design-review

  related_chapters:
    - CH02
    - CH12
    - CH27

  portfolio_analogues:
    - instrumented-event-lab
    - scheduling-analysis
```

---

# 12. Career lens rule

The book must not promise:

- guaranteed employment,
- automatic qualification,
- "master this lab and get any role."

Instead, explain:

- what the role owns,
- what evidence demonstrates relevant skills,
- which professional artifacts resemble the learner's work,
- what deeper skills would still be required.

---

# 13. WAIKE crosswalk

Create:

- `waike/alignment.yaml`
- `waike/course_crosswalk.md`
- `waike/portfolio_evidence.md`
- `waike/assessment_crosswalk.md`

For each book chapter, record:

| Field | Purpose |
|---|---|
| WAIKE track | Curriculum connection |
| Module | Specific learning unit |
| Competency | What learner should demonstrate |
| Book chapter | Publication source |
| Lab | Practice/evidence |
| Assessment | How competence is reviewed |
| Portfolio artifact | Evidence learner keeps |
| Prerequisite | Required prior knowledge |
| Follow-on | Next concept |

Do not invent WAIKE mappings.

Audit accepted `main` before filling exact course/module IDs.

---

# 14. Educator system

Each Concept Edition chapter should eventually include educator notes.

Minimum:

- common misconceptions,
- recommended pacing,
- discussion prompt,
- lab adaptation,
- no-device adaptation,
- assessment evidence,
- teach-back criteria,
- safety notes.

---

# 15. Reader-testing preparation

Create simple comprehension protocols for:

- family/nontechnical reader,
- middle/high-school learner,
- college student,
- engineer,
- educator.

Questions should test:

- comprehension,
- jargon burden,
- diagram usability,
- lab clarity,
- confidence explaining the idea.

Do not call field validation complete until real reader evidence exists.
