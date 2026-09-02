# Evidence and Accepted-Main Audit Specification

# Purpose

This file defines the publication's truth system.

The book will use the gunnchOS3k repository ecosystem as a source of authentic examples.

That makes repository evidence a publication-integrity concern.

The publication must not convert plans into facts.

---

# 1. Core rule

Before any repository-derived fact enters canonical manuscript prose:

1. inspect current accepted `main`,
2. identify exact evidence,
3. record commit SHA,
4. classify the claim,
5. record limitations,
6. register the claim,
7. cite/link the evidence.

If evidence is insufficient:

`EVIDENCE_PENDING`

is the correct result.

---

# 2. Evidence states

Allowed project-state vocabulary:

## Implemented

Code, configuration, hardware definition, or other artifact exists in accepted source-of-truth.

Does not automatically mean tested.

## Repository-tested

Relevant tests exist and pass in the audited repository state.

Does not automatically mean independent reproduction.

## Validated prototype

Prototype has evidence beyond mere implementation.

The validation method must be documented.

## Measured

Claim is supported by recorded measurement.

Requires methodology.

## Simulated

Claim is supported by simulation.

Never write as real-world deployment.

## Requirement

The system is designed or required to do something.

Not evidence that it already does.

## Hypothesis

Research proposition requiring testing.

## Future concept

Forward-looking design idea.

Must not be presented as current functionality.

---

# 3. Accepted-main source registry

Create:

`evidence/source_registry.yaml`

Recommended schema:

```yaml
audit:
  generated_at: ""
  auditor: ""
  policy_version: 1

sources:
  - source_id: SRC-WAIKE
    repository: gunnchOS3k/waike-research-ops
    branch: main
    head_sha: ""
    audited_at: ""
    roles:
      - curriculum
      - labs
      - assessment
      - accessibility
    status: audited
    relevant_paths: []
    notes: []
```

---

# 4. Required audit targets

At minimum:

## WAIKE

`gunnchOS3k/waike-research-ops`

Audit for:

- curriculum structure,
- lab design,
- assessment,
- portfolio evidence,
- accessibility,
- low-cost/no-device paths,
- claims-to-evidence practices,
- course mapping.

## gunnchOS Device OS

`gunnchOS3k/gunnchos-device-os`

Audit for:

- current architecture,
- operating-system services,
- device support claims,
- input pipeline examples,
- telemetry/measurement claims,
- build/test status.

## Hardware / industrial design

Locate the current canonical hardware repository.

Audit for:

- Device Quartet definitions,
- physical architecture,
- hardware status,
- design requirements,
- actual validated components,
- diagrams.

## Measurement/research projects

Only pull them into manuscript claims when relevant.

Possible categories:

- Edge IO measurement,
- beam selection,
- spectrum/AI-RAN,
- NTN resilience,
- 7GC digital twin.

Do not add advanced project claims merely to advertise the portfolio.

They must serve the book.

---

# 5. Claim registry

Create:

`evidence/claim_registry.yaml`

Recommended schema:

```yaml
claims:
  - claim_id: CLM-0001
    chapter: CH02
    text: ""
    scope: project-specific
    classification: repository-implemented

    source:
      type: github
      repository: ""
      branch: main
      commit: ""
      path: ""
      lines: ""

    verification:
      method: ""
      command: ""
      result: ""

    limitations: []

    wording:
      approved: ""
      prohibited: []

    status: verified
```

---

# 6. General knowledge vs project-specific knowledge

The claim registry does not need to turn every basic computer-science statement into a GitHub audit record.

Distinguish:

## General technical claim

Example:

> RAM is used as working memory by running systems.

Evidence route:

- authoritative text,
- standard,
- technical documentation.

## Project-specific claim

Example:

> The current gunnchOS device OS records X measurement.

Evidence route:

- accepted-main repository evidence,
- exact version,
- exact source.

## Performance claim

Example:

> The system completes the interaction in 12 ms.

Evidence route:

- measurement bundle,
- hardware/software details,
- repetitions,
- methodology,
- uncertainty.

---

# 7. Measurement bundle

Every measured publication claim should be reproducible enough to audit.

Recommended structure:

```text
measurements/
  EXP-0001/
    README.md
    environment.yaml
    method.md
    raw/
    processed/
    plots/
    result.json
    limitations.md
```

`environment.yaml` should identify as relevant:

- device,
- hardware revision,
- OS,
- kernel,
- application version,
- network,
- tool versions,
- date.

---

# 8. Status-language linter

Implement a linter that flags suspicious combinations.

Examples:

If classification is `planned`, flag prose containing:

- "currently supports"
- "implements"
- "achieves"
- "provides"

unless the sentence clearly refers to a requirement or future target.

If classification is `simulated`, flag:

- "deployed"
- "in production"
- "measured in the field"

If classification is `repository-tested`, flag:

- "independently validated"
- "field proven"

unless separate evidence exists.

---

# 9. Evidence strength

Recommended scale:

## E0 — unsupported

No adequate source.

Not allowed as factual project-specific prose.

## E1 — design/source exists

Requirement, architecture, or implementation source exists.

## E2 — repository-tested

Automated or documented tests support the claim.

## E3 — reproducibly measured

Method + raw result + environment.

## E4 — independently reproduced/reviewed

A separate party validates.

Do not treat this scale as universal scientific proof.

It is an internal publication-control system.

---

# 10. Diagram evidence

Every implementation diagram must identify:

- system/repo,
- revision,
- commit/tag,
- date,
- whether all components are implemented,
- whether any elements are conceptual.

A figure may combine implemented and conceptual elements only if the distinction is visually and textually explicit.

---

# 11. Screenshot/log sanitation

Before publication:

- remove secrets,
- remove API keys,
- remove tokens,
- remove private emails,
- remove personal identifiers,
- remove device serials where unnecessary,
- remove location data,
- remove unrelated private conversations.

Store scrubbed examples separately from raw private evidence.

---

# 12. Citation policy

Prefer:

1. official standards,
2. primary specifications,
3. textbooks,
4. peer-reviewed research,
5. official engineering documentation,
6. reputable technical organizations.

Avoid building chapter authority mainly from:

- generic SEO blogs,
- unsourced tutorials,
- vendor marketing,
- generated summaries.

Never invent:

- DOI,
- page number,
- standard number,
- author,
- title,
- URL.

---

# 13. Publication audit report

Create:

`evidence/ACCEPTED_MAIN_SOURCE_AUDIT.md`

Recommended sections:

## Audit scope

## Repositories audited

## Accepted-main SHAs

## Publication-useful artifacts

## Current capabilities

## Current limitations

## Candidate figures

## Candidate labs

## Candidate code excerpts

## Licensing considerations

## Claims safe to use

## Claims requiring qualification

## Claims not currently supported

## Upstream gaps

---

# 14. No source rewriting

The publication audit must not modify upstream repositories to make a book statement true.

If the book needs a capability that is not implemented:

1. register an upstream gap,
2. cite the requirement if useful,
3. mark the manuscript statement as planned/future,
4. do not silently "fix" the product during the publication task.

---

# 15. Definition of evidence integrity pass

Evidence integrity passes when:

- all project-specific claims are registered,
- each has adequate source/status,
- unsupported claims are blocked,
- measured claims have methods,
- conceptual figures are labeled,
- stale PR/branch claims are not silently promoted,
- status vocabulary is consistent,
- publication prose matches claim classification.
