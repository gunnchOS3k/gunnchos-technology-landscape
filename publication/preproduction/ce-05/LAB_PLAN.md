# CE-5 Lab Plan — LAB-TRUST-001 (proposed)

**Chapter:** CE-5 — AI, Security, Privacy and Trust  
**Proposed lab ID (publication-side):** `LAB-TRUST-001`  
**Title:** Compare local vs remote AI paths and write a consent/trust card  
**Status:** `planned` (not implemented in this wave; not a WAIKE module ID)  
**Pedagogy:** observation → interpretation boundary; accessible fallbacks required

---

## Learning intent

Help learners see that an AI answer is an **inference output** produced under **identity/privacy constraints**, not a person who “knows.” Connect security to experience: what broke, what felt unsafe, what control would restore usable trust.

---

## Experience under test

1. Ask the **same** practical question in two settings when available:  
   - **Route L:** on-device / offline-capable or clearly local runtime (or a provided recorded local transcript if hardware is unavailable).  
   - **Route C:** cloud/browser assistant requiring network.  
2. Complete a **consent/trust card** for one route: audience, purpose, data classes, retention, opt-out, AI disclosure.

If only one live route exists, use the supplied **fixture transcript** for the other and label it `FIXTURE` / `illustrative`.

---

## Evidence artifacts (completion ≠ command ran)

| Artifact | Required contents |
|---|---|
| Comparison table | Observations only: time-to-first-token or wall time if measured by learner; network required? (Y/N); data leaving device? (claimed/unknown); errors/hedges noticed |
| Consent/trust card | Audience, purpose, classes, retention, opt-out, disclosure |
| Dual-ledger note | One human-trust feeling + one technical-trust control |
| Uncertainty note | One fluent-but-wrong or unverifiable claim spotted (or “none observed” with what was checked) |

**Prohibited:** invented latency numbers presented as gunnchOS product measurements; exploit steps; secret exfiltration exercises.

---

## Pathway variants

| Pathway | Task focus |
|---|---|
| Explorer | Fill observation columns; teach-back one sentence |
| Operator | Classify a failure symptom (authn / authz / network / model quality) |
| Builder | Add one redaction rule for a sample log line |
| Engineer | Sketch trust boundaries crossed by Route C |
| Researcher | State hypothesis + limitation (n=1, fixture bias) |
| Educator | Run no-device storyboard + misconception drill |

---

## Accessible / no-device fallbacks

- **No GPU / no local model:** use short provided transcripts labeled illustrative.  
- **No network:** paper comparison using printed Route C fixture.  
- **Low vision:** table in semantic HTML/Markdown; avoid color-only encoding.  
- **Motor / switch access:** keyboard-only worksheet; no drag-only UI.  
- **Cognitive load:** three-row table maximum for Explorer track.

---

## Safety & ethics envelope

- Use non-sensitive prompts (no real SSNs, health records, passwords).  
- Redact account identifiers in screenshots.  
- Security content stays at **concepts + UX symptoms**; no vulnerability exploitation.  
- Align responsible-use language with WAIKE `COMM_PD_ETHICS` adjacency (consent, AI disclosure).

---

## WAIKE mapping posture

`LAB-TRUST-001` is **proposed** for the book. Map WAIKE courses as **adjacent** only—see `WAIKE_CROSSWALK.md`.  
Do **not** invent a WAIKE lab ID named `LAB-TRUST-001`.

Closest audited adjacencies (WAIKE SHA `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0`):

| Theme | WAIKE course | Example lab IDs (exact in repo) | Map class |
|---|---|---|---|
| Inference + privacy redaction | `AI_ML_EDGE` | `lab_score_model`, `lab_quantize_budget`, `lab_rag_redact` | adjacent |
| Identity / RBAC | `CYBERSECURITY` | `lab_iam_rbac` | adjacent |
| Consent + AI disclosure | `COMM_PD_ETHICS` | `lab_consent_disclosure`, `lab_ai_disclosure_modes` | adjacent |
| Authz matrix (builder) | `SOFTWARE_BUILDER` | `lab_authz` | adjacent |
| Secrets / least privilege | `CLOUD_DEVOPS` | `lab_iam_secrets` | adjacent |

---

## Build-it extension (section 8 prep)

Optional builder stretch: minimal authz matrix (desk / reader / bot) **or** a redaction config for RAG-like snippets—mirroring WAIKE patterns without copying proprietary curricula text.

---

## Implementation blockers (honest)

- No publication-repo lab directory for `LAB-TRUST-001` yet.  
- Shared `labs/lab_registry.yaml` must not be edited in this agent wave.  
- Local model availability varies; fixtures mandatory for equity of completion.
