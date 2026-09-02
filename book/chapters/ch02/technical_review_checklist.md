# Technical Review Checklist — Chapter 2 (CH02)

**Chapter:** Follow One Tap Through the Entire Stack  
**Manuscript:** `book/chapters/ch02/chapter.md`  
**Reviewer role:** technical + editorial gate for Concept Edition prototype  
**Legend:** `[x]` satisfied by current draft manuscript · `[ ]` pending human reader testing / author editorial acceptance

---

## 1. Narrative

- [x] Opens from a recognizable human moment (tap → immediate change → later content) without leading definitions
- [x] Governing question stated clearly
- [x] Warm, direct, curious voice; middle-school-accessible with progressive depth
- [x] Teaching model visible: Human experience → system → component → code → network → society
- [x] Distinguishes immediate local feedback vs later remote content
- [x] Complete prose manuscript (not an outline), with all 12 required numbered sections
- [ ] Human reader testing: Explorer can retell the path in ordinary language
- [ ] Author editorial acceptance of tone, pacing, and length

## 2. Systems accuracy

- [x] Full-stack layers covered: human, input hardware, compute, system software, application, networking (optional), output, human feedback
- [x] Explicit alternate paths: local-only, local service, LAN, internet/cloud, edge, cache hit, cache miss
- [x] Never implies every tap goes to the cloud
- [x] Numbered signal sequence with overlap / non-simplistic timeline caveat
- [x] Guardrails observed: no claim that every touch is an app-visible interrupt; timestamps ≠ full touch-to-photon; network latency ≠ total interaction latency
- [x] Component cards present for touch digitizer, device driver, kernel, scheduler, event loop, RAM, GPU, packet
- [x] Stability Contract defined with concurrent hidden conditions
- [ ] Independent technical reviewer sign-off on abstractions and wording
- [ ] Platform-diversity spot-check (iOS/Android/desktop/browser naming differences)

## 3. Pathways (Explorer → Researcher + Educator)

- [x] Explorer tasks (local state change + ordinary-language explanation)
- [x] Operator tasks (devtools local vs network comparison)
- [x] Builder tasks (timing instrumentation)
- [x] Engineer tasks (measured vs inferred latency budget segments)
- [x] Researcher tasks (repeated experiment design, variability, limitations)
- [x] Educator facilitation hooks (teach-back, lab adaptation)
- [ ] Classroom pilot with at least one Educator facilitator
- [ ] Pathway differentiation review (cognitive load per audience)

## 4. Visuals

- [x] Figure references FIG-CH02-001 through FIG-CH02-007 present in prose
- [x] Conceptual / Representative educational architecture labels required in captions/metadata
- [x] Accessibility metadata stubs: caption, alt text, text equivalent / reading order, status, source
- [x] Latency figure requires illustrative / measured / inferred labeling (no fake benchmarks)
- [ ] Final SVG (or approved) art assets produced and versioned
- [ ] Color-not-alone and pattern reinforcement checked on finished art
- [ ] Alt text / long-description quality pass with a screen-reader user or specialist

## 5. Glossary

- [x] Section 12 lists terms introduced for registry linking
- [x] Terms introduced progressively in body rather than a front-loaded dump
- [ ] Glossary registry entries exist for every listed term (IDs, plain definitions, related links)
- [ ] Automated glossary-link validation in build pipeline passes
- [ ] Plain-language glossary review by non-specialist reader

## 6. Lab (LAB-TAP-001)

- [x] Observable question stated
- [x] Commodity / no-specialized-hardware baseline (browser Route A)
- [x] Optional local GUI and Android-compatible extension routes
- [x] Prediction, evidence minimum, interpretation (observed vs inferred), limits
- [x] Portfolio output list (README, diagram, table, evidence, reflection, teach-back paragraph)
- [x] Safety/privacy: no secrets in logs; no root requirement
- [x] Publication-owned lab ID; WAIKE mapping without inventing a tap-lab module ID
- [ ] Baseline Route A reproduced cold by a second person
- [ ] Example portfolio artifact bundle committed for instructor reference
- [ ] Time-estimate validated with real learners

## 7. Evidence integrity

- [x] No fabricated gunnchOS hardware capabilities, benchmarks, or deployments
- [x] Device OS mentions qualified: alpha / digital / SOFTWARE_SIMULATED (CLM-0002)
- [x] Device Quartet qualified: research form factors / PHYSICAL_PENDING; educational architecture labeling (CLM-0003)
- [x] WAIKE: no literal tap lab; LAB-TAP-001 publication-owned; curriculum ops claim cited (CLM-0001)
- [x] Project claims use CLM-#### style citations where used
- [x] General knowledge vs project-specific knowledge distinguished in claim footnotes
- [ ] Claim registry YAML entries CLM-0001–CLM-0003 formally filed with SHAs/paths
- [ ] Author accepts claim wording against `evidence/ACCEPTED_MAIN_SOURCE_AUDIT.md`
- [ ] Unresolved-claims cross-check before Concept Edition freeze

## 8. Careers

- [x] Career table spans interaction → accessibility across the stack
- [x] Professional artifacts named per role
- [x] Lab resemblance column ties learner work to professional evidence
- [x] No employment promises or outcome guarantees
- [ ] Career advisor / practitioner spot-check of role titles and artifacts

## 9. Responsibility (security, privacy, accessibility, equity)

- [x] Security: permissions, authentication, trusted UI, secure transport, validation (scoped, not full cyber chapter)
- [x] Privacy: input telemetry sensitivity; lab log scrubbing
- [x] Accessibility: keyboard / switch / voice / AT; intent→event constant; equivalent-path experiment prompt
- [x] Equity: weak connectivity, latency, data caps, low-cost/older hardware
- [x] Check-understanding includes teach-back without jargon then term introduction
- [ ] Accessibility specialist review of chapter + finished figures
- [ ] Equity review with low-bandwidth / phone-first teaching context
- [ ] Author acceptance of security/privacy scope boundaries

---

## Gate summary

| Area | Draft manuscript | Human / editorial pending |
|---|---|---|
| Narrative | Substantially complete | Reader testing + author accept |
| Systems | Substantially complete | Independent tech sign-off |
| Pathways | Specified in prose | Classroom pilot |
| Visuals | Referenced + metadata stubs | Art production + a11y pass |
| Glossary | Link list present | Registry + validator |
| Lab | Spec complete in chapter | Cold reproduction + sample portfolio |
| Evidence | Qualified project claims | Registry filing + freeze audit |
| Careers | Table complete | Practitioner spot-check |
| Responsibility | Covered in §9 + §11 | Specialist + equity reviews |

**Prototype status:** Chapter 2 draft is manuscript-complete for technical content gates marked `[x]`. Concept Edition release still requires pending items (human reader testing, finished figures, glossary validation, lab reproduction, claim registry filing, and author editorial acceptance).
