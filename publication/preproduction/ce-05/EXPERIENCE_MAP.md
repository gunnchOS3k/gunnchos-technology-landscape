# CE-5 Experience Map

**Chapter:** CE-5 — AI, Security, Privacy and Trust  
**Teaching spine:** Human experience → system → component → code → network → society  
**Status:** preproduction map (not manuscript prose)

---

## Anchor moment

You ask an assistant a practical question while signed into an ordinary account. The reply arrives quickly and sounds polished. A permission, privacy, or “verify it’s you” prompt may appear before or after. You feel either helped, uneasy, or unsure whether to trust the next step.

---

## Layer map

| Layer | What the human notices | Hidden technical objects (teaching names) | Failure / friction that is still “the same experience” |
|---|---|---|---|
| Human experience | Helpful answer, delay, refusal, lockout, creepy recall | Expectation, workload, trust, stigma of being wrong | Fluency without usefulness; usable UI that excludes assistive tech |
| System | App/assistant session continues | Application + model runtime + identity session + policy engine | Session expires; model offline; policy blocks feature |
| Component | Microphone/keyboard, screen, “AI” chip/cloud badge | Sensors/UI toolkit; inference engine; IdP; keystore; log store | Broken mic permission; missing model weights; clock skew on tokens |
| Code | Settings toggles, “improve the product” checkbox | Prompt assembly; authz checks; redaction filters; telemetry flags | Logging more than disclosed; authz bug that feels like “random deny” |
| Network | Spinner, “connecting…”, captive portal | TLS session; API gateway; CDN; regional model endpoint | TLS intercept UX; high latency; DNS failure misread as “AI is dumb” |
| Society | Who is helped, who is surveilled, who is locked out | Policy, vendors, regulators, equity of access to private compute | Biased refusals; unpaid data labor; inaccessible verification flows |

---

## Experience → pathway routes

### Explorer
1. Write three observations (what appeared on screen / what you heard).  
2. Circle words that claim certainty.  
3. Ask: “What would change my mind about trusting this?”

### Operator
1. Locate permission, account, and privacy surfaces.  
2. Note whether a failure looks like identity, authorization, network, or model quality.  
3. Capture screenshots/redacted logs as **observations**, not conclusions.

### Builder
1. Draft a consent card: audience, purpose, data classes, retention, opt-out.  
2. Add one redaction rule for a sample prompt/log line.  
3. Document tradeoffs (utility vs exposure).

### Engineer
1. Sketch local vs cloud inference boundaries (data residency, keys, latency).  
2. List trust boundaries crossed by one prompt.  
3. Propose one control that preserves UX (least privilege, clearer disclosure).

### Researcher
1. State a hypothesis about error modes (hallucination, overrefusal, leakage).  
2. Define variables you can actually observe without specialized hardware.  
3. Record uncertainty and limitations explicitly.

### Educator
1. Facilitation prompt: “Show me where trust is a feeling vs a control.”  
2. Misconception drill from `LEARNING_OBJECTIVES.yaml`.  
3. No-device adaptation: paper consent card + storyboard of local vs cloud.

---

## Signal path (Follow the signal — outline)

1. **Input** — user text/voice/image enters the app.  
2. **Context assembly** — UI state, account claims, retrieved docs (if any).  
3. **Policy gate** — authn session valid? authz allows feature? consent covers purpose?  
4. **Inference** — local runtime or remote API applies model parameters to inputs.  
5. **Output** — tokens/text/actions returned; may include hedges or tool calls.  
6. **Side effects** — logs, analytics, fine-tuning queues, abuse review (disclosed or not).  
7. **Feedback to human** — UI rendering, accessibility tree, time-to-usable-answer.

Numbered journey teaching labels: **data**, **control**, **state**, **feedback** (power only where device/thermal budgets matter).

---

## Failure domains (UX-linked, not scare-list)

| Domain | Human-visible symptom | Systems hint |
|---|---|---|
| Model quality | Wrong-but-fluent answer | Evaluation/threshold / retrieval miss |
| Uncertainty UX | No hedge when needed / too many refusals | Decoding policy, safety filters |
| Identity | Forced re-login, MFA loop | Session/token lifetime, IdP outage |
| Authorization | Feature visible but blocked | Role/attribute mismatch |
| Privacy disclosure | Surprise reuse of past prompts | Retention + purpose creep |
| Network/security UX | Padlock present but account takeover fear | Endpoint malware, phishing, session theft — teach boundaries |
| Accessibility | CAPTCHA or voice-only verify excludes | Inclusive auth alternatives |

---

## Capstone teach-back (prep)

“Explain to a family member: why a smooth AI answer can still be unsafe to act on, and what one control (technical or social) would make the experience more trustworthy for more people.”
