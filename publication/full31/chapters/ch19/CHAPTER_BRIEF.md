# CH19 Chapter Brief — NTN and Service Continuity Across Ground, Air, and Space

**Chapter ID:** `CH19` (`ch19`)  
**Part:** IV — Connect everything  
**Package status:** `preproduction` (concept packet; **no** canonical manuscript prose)  
**Accepted-main base:** `0e694176652d4729c7f2b71df08b871a863afb8c`  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`. This package does not claim Gate 3 PASS.  
**Do not alter:** `publication/gates/gate-3/` or `CH02-REVIEW-R1`.

---

## Canonical title

NTN and Service Continuity Across Ground, Air, and Space

## Primary reader promise

After this chapter, a reader can explain non-terrestrial networks (NTN) as an additional path class and treat service continuity as experience continuity across ground/air/space—not as an always-on icon.

## Experience-first opening moment (section intent)

**Canonical anchor:** A flight mode, rural gap, or outage story: service works on terrestrial cellular, fails, then a satellite-messaging or NTN feature offers limited continuity—or marketing implies seamless space Internet. From the seat: confusion. Underneath: different delays, coverage, and continuity mechanisms.

## Part emphasis

Continuity across domains; humility on deployed capabilities; no fabricated satellite demos.

## Teaching model

> moment → notice → ecosystem → signal → components → Stability Contract → Try/Build → secure/include → career → check → glossary

Central arc: **Human experience → system → component → code → network → society**

## Measurable outcomes (Explorer → Researcher)

| Pathway | After this chapter the reader can… |
|---|---|
| Explorer | Teach-back NTN is not automatic full Internet. |
| Operator | Classify a feature's capability from official docs. |
| Builder | Continuity checklist across path classes. |
| Engineer | Compare delay regimes qualitatively with sources. |
| Researcher | Mark project NTN evidence needs explicitly. |

## Stability Contract (chapter lens)

Definition: a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

Chapter-focused concurrent conditions (qualitative; no invented numeric budgets):

- At least one usable path class available for the required capability
- Delay/reliability of active path within task tolerance
- Handover across domains does not silently drop human-visible state
- Capability class matches user expectation (messaging vs broadband)

## Secure / include / equity (integrated)

No unauthorized satellite ground-station activity. Equity: rural/flight stories without requiring travel. A11y: text continuity checklists.

## Career lens (intent)

Roles/layers to surface (publication `careers/role_registry.yaml` where IDs exist; otherwise descriptive): Satellite systems, Mobile core engineer, Resilience/SRE, Policy/spectrum roles.  
No employment guarantees.

## CE / lab inheritance (prefer link over duplication)

### CE preproduction
- `publication/preproduction/ce-04/` — Service continuity named; full NTN deferred to CH19
- `publication/preproduction/ce-06/` — Connected ≠ usable under path changes

### Labs (real IDs only)
- **LAB-PKT-001**: Continuity framing adjacency only.
- **LAB-CE06-001**: Cross-layer continuity diagnosis adjacency.

## Explicit non-goals

- Final canonical prose for `CH19`.
- Fabricated citations, measurements, or Gate 3 reader evidence.
- Invented WAIKE course/lab IDs.
- Collapsing Wi-Fi / cellular / Internet / cloud into synonyms (especially Part IV).
- Device Quartet as shipping products; physical claims stay `PHYSICAL_PENDING`.

## Twelve-section anatomy (intent only — no prose)

1. The moment  
2. What you notice  
3. Exploded ecosystem  
4. Follow the signal  
5. Component cards  
6. Stability contract  
7. Try it  
8. Build it  
9. Secure and include it  
10. Career lens  
11. Check understanding  
12. Glossary links  

## Editorial status language

Allowed now: `preproduction` / `scaffold`.  
Not allowed: Gate 3 PASS, `PUBLICATION_READY` prose claims.

## Next automatable action / integrator handoff

Keep packet truthful; promote selected candidates only after Gate 3 evidence exists.
