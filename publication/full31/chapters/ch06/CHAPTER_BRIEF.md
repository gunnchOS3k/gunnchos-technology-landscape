# CH06 Chapter Brief — CPU, Instructions, and Parallel Work

**Chapter ID:** `CH06`  
**Full31 packet:** `publication/full31/chapters/ch06/`  
**Part:** II  
**Agent:** `agent-h/full31-part-i-ii`  
**Accepted-main base:** `0e694176652d4729c7f2b71df08b871a863afb8c`  
**Package status:** preproduction packet (no new canonical prose authored here)  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

---

## Canonical title

CPU, Instructions, and Parallel Work

## Primary reader promise

After this chapter, a reader can explain that programs run as instructions on a CPU (and sometimes accelerators), that the OS schedules competing work, and that ‘more cores’ only helps some workloads.

## Anchor human moment

You open a local app while other work runs. The UI still draws, but the device stutters or fans spin. From the seat it feels like ‘the CPU is bad.’ Underneath, instruction streams and schedulers are competing.

## Emphasis

Part II: compute fundamentals — instructions and parallel work

## Inheritance / non-duplication

Link CE-3 for CPU/parallel concepts; full-book Ch6 stays instruction/CPU/parallel focused—not full OS encyclopedia.

Links:
- `publication/preproduction/ce-03/ — CE-3 synthesizes CH06+CH07+CH12; inherit CPU/instruction/parallel slices; do not duplicate full CE-3 OS/storage depth.`
- `concept-edition/registry.yaml CE-3 → [CH06, CH07, CH12]`

## Measurable outcomes (Explorer → Researcher)

| Pathway | After this chapter the reader can… |
|---|---|
| Explorer | Explain that apps become instruction streams executed by hardware, scheduled by an OS. |
| Operator | Use commodity monitors to observe CPU activity during a controlled action. |
| Builder | Map one experience to process/threads/CPU (and optional accelerator) without claiming root cause. |
| Engineer | Distinguish CPU-bound vs waiting; explain why more cores are not universal speedups. |
| Researcher | Propose a controlled load comparison; report uncertainty; no invented IPC/GHz product claims. |

## Teaching model

> Human experience → system → component → code → network → society

Twelve-section anatomy (intent only — **no canonical prose in this packet**):

1. The moment  
2. What you notice  
3. Exploded ecosystem  
4. Follow the signal  
5. Component cards  
6. Stability Contract  
7. Try it  
8. Build it  
9. Secure and include it  
10. Career lens  
11. Check understanding  
12. Glossary links  

## Stability Contract (conditions summary)

Enough CPU time scheduled for interactive work; competing work bounded; thermal/power not silently collapsing compute—qualitative.

## Security / equity / accessibility

Process isolation intent foreshadow; equity of monitor tooling across OS; a11y of activity visualizations.

## Career lens

OS/embedded, performance engineering, compiler-lite literacy, SRE local diagnosis.

## Device Quartet

Only where relevant. All physical / EVT / fabricated measurements stay **`PHYSICAL_PENDING`**. Commodity-device lab routes preferred. No shipping-SKU marketing language.

## Explicit non-goals

- Final canonical prose for this chapter (except CH02 inherits existing draft; do not rewrite here).
- Fabricating Gate 3 reader evidence.
- Altering `publication/gates/gate-3/` or `CH02-REVIEW-R1`.
- Inventing WAIKE course/lab IDs.
- Encyclopedia component dumps.

## Production state (packet)

| Field | Value |
|---|---|
| current_state | `PREPRODUCTION_COMPLETE` |
| canonical_prose_state | `SCAFFOLD` |
| concept_preproduction_state | `PREPRODUCTION_COMPLETE` |

## Next automatable action

Diff CE-3 packet for CPU-only claim subset; mark CH12 OS depth as later dependency; avoid duplicating LAB-CMS-001.
