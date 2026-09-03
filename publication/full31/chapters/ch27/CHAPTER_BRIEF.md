# CH27 — Testing, Observability, and Evidence

**Package status:** `preproduction`  
**Manuscript status:** scaffold (no canonical chapter prose in this wave)  
**Full-book chapter:** CH27 (ch27)  
**Part:** VI — Build, prove, and contribute  
**Agent:** J (`agent-j/full31-part-v-vi`)  
**Accepted-main base:** `0e694176652d4729c7f2b71df08b871a863afb8c` (PR #3 merge)  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`. Do not claim PASS. Do not alter `CH02-REVIEW-R1`. Do not fabricate reader evidence.

---

## Reader promise

Produce evidence that distinguishes tests, observations, and inferences—so 'it works' becomes inspectable.

## Anchor human moment

A feature 'passes' locally while production users see stalls; status dashboards look green until someone inspects the right signal.

## Teaching model

`moment → notice → ecosystem → signal → components → Stability Contract → Try/Build → secure/include → career → check → glossary`

Central chain: **Human experience → system → component → code → network → society**

## Measurable outcomes (Explorer → Researcher)

| Pathway | Outcome |
|---|---|
| Explorer | Separate test result, log/trace observation, and causal story. |
| Operator | Read a simple metric/log and label what is observed vs inferred. |
| Builder | Add one test or assertion and one observability note to a change. |
| Engineer | Design a minimal signal set for a failure domain. |
| Researcher | State uncertainty and evidence limitations explicitly. |

## Stability Contract (chapter conditions)

- Signals available at the needed depth
- Test oracles match the human experience claims
- Observation/inference boundaries enforced in artifacts
- PII redaction in traces/logs for portfolio sharing

## Security / equity / accessibility (integrated)

Redact secrets/PII from observability artifacts. Accessible tooling alternatives. Equity: fixture traces for readers without production access.

## Career lens

| Role family | Portfolio evidence |
|---|---|
| SRE / observability engineer | signal map + redacted trace note |
| QA / test engineer | oracle vs experience mismatch writeup |
| Security-minded developer | log redaction checklist |

Employment is **not** guaranteed by completing artifacts.

## CE / lab inheritance (link — do not duplicate depth)

### Concept Edition
- CE-6 evidence hierarchy / observation vs inference
- LAB-CE06-001 evidence fields

### Labs
- LAB-CE06-001
- CLOUD_DEVOPS SLO/incident adjacency
- DATA_DASHBOARDS debug adjacency

## Device Quartet

not required

## Twelve-section anatomy (section intent only)

1. The moment — anchor above  
2. What you notice — human symptoms  
3. Exploded ecosystem — layers for this chapter  
4. Follow the signal — numbered path  
5. Component cards — plain language + constraints + failure symptoms  
6. Stability contract — conditions listed above  
7. Try it — lab opportunities  
8. Build it — small extension  
9. Secure and include it — integrated, not appendix  
10. Career lens — table above  
11. Check understanding — misconceptions + teach-back  
12. Glossary links — see `GLOSSARY_CANDIDATES.yaml`

## Explicit non-goals this wave

- Final canonical prose  
- Gate 3 PASS / fabricated human reviews  
- Invented WAIKE course/lab IDs  
- Fake citations or marketing Device Quartet claims  
- Representing illustrative EMIT / fixture examples as human evidence

## Next automatable action

Verify OpenTelemetry (or chosen) primary docs; align claim IDs with CE-6 evidence hierarchy figures
