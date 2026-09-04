# Misconception matrix (full31)

**Registry:** `book/terminology.yaml`  
**Living glossary:** `glossary/glossary.yaml`  
**Purpose:** Editorial QA + educator aid. Prevents conceptual conflation without forcing identical prose in every chapter.

Status: machine-assisted canonical mapping for quality convergence. Not human-validated Gate 3 evidence.

| Misconception | Canonical distinction | Introduces | Reinforces | Terminology ids |
|---|---|---|---|---|
| Internet ≠ Wi-Fi | Wi-Fi is local radio access; the Internet is the global internetwork | CH16, CH17 | CH02, CH18 | `internet`, `wifi` |
| cloud ≠ Internet | Cloud is a remote compute/storage delivery model that often *uses* the Internet | CH02, CH15 | CH16, CH23 | `cloud`, `internet` |
| LAN ≠ Internet | A LAN can be healthy while upstream Internet paths fail | CH16 | CH02, CH17 | `lan`, `internet` |
| authentication ≠ authorization | Authn verifies identity; authz decides allowed actions | CH23 | CH11, CH24 | `authentication`, `authorization` |
| identity ≠ authentication | An identity record is not proof of a successful login | CH23 | CH24 | `identity`, `authentication` |
| privacy ≠ security | Security can hold while privacy-harming collection continues | CH23, CH24 | CH22, CH25 | `privacy`, `security` |
| latency ≠ throughput | Delay is not the same as rate of completed work | CH02, CH03 | CH16, CH20 | `latency`, `throughput` |
| latency ≠ jitter | Average delay is not the same as delay variability | CH02 | CH03, CH20 | `latency`, `jitter` |
| reliability ≠ latency | Fast-but-flaky is not “reliable” | CH03 | CH20, CH27 | `reliability`, `latency` |
| QoE ≠ network KPI alone | Lived experience is not identical to meter readings | CH03 | CH20, CH25 | `qoe`, `latency`, `reliability` |
| simulation ≠ measurement | Modeled imitation is not field observation | CH28 | CH27, CH05 | `simulation`, `measurement` |
| digital twin ≠ any model | A twin is bound to a real counterpart with validity discipline | CH28 | — | `digital-twin`, `model` |
| storage ≠ memory | Persistent storage is not volatile working RAM | CH02, CH07 | CH13 | `storage`, `memory` |
| cache ≠ storage | Cache is a speed layer; it is not durable filing | CH02, CH07 | CH14 | `cache`, `storage` |
| process ≠ thread | Process isolates resources; thread is an execution sequence inside | CH02 | CH12 | `process`, `thread` |
| CPU core ≠ thread | Core is hardware; thread is a schedulable software context | CH06 | CH12 | `core`, `thread` |
| firmware ≠ operating system | Firmware is close-to-hardware boot/control software, not the full OS | CH11 | CH12, CH23 | `firmware`, `operating-system` |
| API ≠ user interface | APIs are software contracts; UIs are human-facing surfaces | CH02, CH14 | CH16 | `api` |
| runtime ≠ API | Execution environment is not the call contract | CH14 | CH15 | `runtime`, `api` |
| edge ≠ cloud | Placement closer to devices is not identical to provider cloud | CH02, CH15 | CH22 | `edge`, `cloud` |
| spectrum ≠ channel | Spectrum is the frequency resource; a channel is a usable slice/condition | CH18 | CH17 | `spectrum`, `channel` |
| antenna ≠ beamforming | Hardware radiators ≠ spatial steering algorithms | CH18 | — | `antenna`, `beamforming` |
| MIMO ≠ guaranteed N× speed | Multi-antenna spatial streams depend on real channels | CH18 | — | `mimo` |
| NTN ≠ ordinary cellular behavior | Non-terrestrial access changes delay/continuity assumptions | CH19 | CH17, CH18 | `ntn`, `cellular` |
| service continuity ≠ “has bars” | Attachment is not unbroken application sessions | CH19 | CH20 | `service-continuity`, `reliability` |
| training ≠ inference | Fitting parameters ≠ applying a trained model | CH21 | CH22 | `training`, `inference` |
| generative AI ≠ all ML | Generative systems are a class within broader ML/AI | CH21 | CH24 | `generative-ai`, `model` |
| accessibility ≠ convenience | Access for diverse abilities is not a nicety for already-served users | CH24 | CH25 | `accessibility` |
| digital equity ≠ feature availability | Shipping a feature does not prove equitable benefit | CH25 | CH24 | `digital-equity`, `accessibility` |
| portfolio evidence ≠ job guarantee | Artifacts show capability; they do not hire anyone | CH30 | CH31 | `portfolio-proof` |
| system ≠ component | The whole cooperating stack is not any single part | CH01 | CH02, CH29 | `system`, `component` |
| model ≠ understanding | Outputs are not proof of human-like knowing or wanting | CH21 | CH24 | `model`, `inference` |

## How to use

1. Before rewriting a chapter definition, check `book/terminology.yaml` for the canonical distinction.
2. Prefer local wording that preserves meaning; do not paste identical sentences book-wide.
3. When Agents A–C file `TERMINOLOGY` issues, cite the matrix row and term ids.
4. Educator follow-on: turn rows into discussion prompts (“why might Wi-Fi work while the Internet fails?”).

## Collision / coverage notes

- High-risk canonical term count: see `book/terminology.yaml` (`terms` length).
- Alias collisions (same alias → different term ids): reported by `make full31-terminology-check`.
- Glossary promotion gaps (`glossary_id: null`) are intentional for this wave; do not invent Gate 3 readiness from terminology alone.
