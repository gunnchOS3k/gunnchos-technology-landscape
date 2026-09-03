# CH20 Chapter Brief — Latency, Reliability, QoE, and the Stability Contract

**Chapter ID:** `CH20` (`ch20`)  
**Part:** IV — Connect everything  
**Package status:** `preproduction` (concept packet; **no** canonical manuscript prose)  
**Accepted-main base:** `0e694176652d4729c7f2b71df08b871a863afb8c`  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`. This package does not claim Gate 3 PASS.  
**Do not alter:** `publication/gates/gate-3/` or `CH02-REVIEW-R1`.

---

## Canonical title

Latency, Reliability, QoE, and the Stability Contract

## Primary reader promise

After this chapter, a reader can apply the Stability Contract with latency, reliability, and QoE as distinct lenses—and can diagnose connected-but-unusable experiences without collapsing metrics.

## Experience-first opening moment (section intent)

**Canonical anchor:** Everything looks connected; send/submit/stream still fails or feels awful. Or ping is fine but the app is not. From the seat: contradiction. Underneath: concurrent hidden conditions; QoE ≠ QoS ≠ ping.

## Part emphasis

Part IV close + CE-6 full-book expansion; inherit LAB-CE06-001 / LAB-PKT-001.

## Teaching model

> moment → notice → ecosystem → signal → components → Stability Contract → Try/Build → secure/include → career → check → glossary

Central arc: **Human experience → system → component → code → network → society**

## Measurable outcomes (Explorer → Researcher)

| Pathway | After this chapter the reader can… |
|---|---|
| Explorer | Teach-back Stability Contract + connected≠usable. |
| Operator | Run LAB-CE06-001 diagnosis worksheet. |
| Builder | Propose one bounded improvement + evidence that would confirm it. |
| Engineer | Separate QoE/QoS/ping; climb evidence hierarchy ethically. |
| Researcher | Design study with uncertainty; no fake MOS. |

## Stability Contract (chapter lens)

Definition: a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

Chapter-focused concurrent conditions (qualitative; no invented numeric budgets):

- SC-01..SC-11 style concurrent conditions from CE-6 (input, schedule, memory, storage, path, service, render, power/thermal, trust, a11y, total delay)
- Metric family matched to symptoms
- Evidence labeled observed/inferred/illustrative

## Secure / include / equity (integrated)

Privacy of traces; equity of device/network assumptions; a11y as contract condition (SC-10).

## Career lens (intent)

Roles/layers to surface (publication `careers/role_registry.yaml` where IDs exist; otherwise descriptive): SRE, Performance engineer, ROLE-HCI, Educator facilitator, Network engineer.  
No employment guarantees.

## CE / lab inheritance (prefer link over duplication)

### CE preproduction
- `publication/preproduction/ce-06/` — Primary inheritance — Stability Contract + capstone method
- `publication/preproduction/ce-04/` — Latency ≠ reliability ≠ throughput
- `publication/preproduction/ce-01/` — Ecosystem lens

### Labs (real IDs only)
- **LAB-CE06-001**: Primary synthesis lab adjacency (CE-6 / agent-e).
- **LAB-PKT-001**: Metric family prediction adjacency.
- **LAB-TAP-001**: Observation vs inference craft.
- **LAB-CMS-001**: Local conditions inside the contract.

## Explicit non-goals

- Final canonical prose for `CH20`.
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
