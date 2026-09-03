# LAB-TRUST-001 — Compare local vs remote AI paths and write a consent/trust card

**Chapter:** CE-5 — AI, Security, Privacy and Trust  
**Publication lab ID:** `LAB-TRUST-001` (not a WAIKE module ID)  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Statuses:** `IMPLEMENTED_DIGITAL` | `FIXTURE_VALIDATED` | `PHYSICAL_PENDING` | `EXTERNAL_DEPENDENCY`

## Observable question

> When the same practical question is answered by a local path vs a remote path, what can I observe about privacy, identity, and trust—without treating the model as a person who knows?

## What this lab teaches

1. **Data → model → inference** — input text is transformed by stored parameters into an output; the output is not a person “knowing.”
2. **Local vs remote AI** — whether inference is claimed to run on-device or on someone else’s computers.
3. **Authn vs authz** — proving an identity claim vs deciding what that identity may do.
4. **Data lifecycle** — collect → use → retain → share → delete/redact.
5. **Privacy boundary** — what (claimed) leaves the device for a given route.
6. **Security design principle** — least privilege + psychological acceptability (UX-linked; no exploits).
7. **Trust / uncertainty** — felt trust vs technical controls; fluent answers can be wrong.

## Safety (required)

- Use **safe fixtures and non-sensitive prompts only**.
- Never paste real secrets, private messages, precise location, health records, or confidential work data.
- Do not attempt vulnerability exploitation, unauthorized scanning, or credential harvesting.
- Prefer the supplied transcripts when a live local model or cloud assistant is unavailable.

## Time estimate

About 50 minutes for the Explorer baseline (including fixtures).

## Prediction (do this first)

Write which route you expect to:

1. require network (Y/N),
2. send prompt text off-device (claimed / unknown),
3. break first among bounds **SC-CE5-L** (path locality), **SC-CE5-P** (privacy lifecycle), **SC-CE5-U** (uncertainty honesty).

## Shared practical question (safe)

Use this exact prompt for both routes (or the fixtures that already use it):

> How can I tell whether a public library website is slow because of my phone or because of the site, without logging into any personal accounts?

## Route L — Local / offline-capable (`IMPLEMENTED_DIGITAL`)

```bash
python3 labs/LAB-TRUST-001/local_app/trust_sim.py
```

Or open `browser/index.html` and use **Route L (local sim)**.

If no Python/browser is available, read `fixtures/route_l_transcript.md` and label evidence `FIXTURE` / `illustrative`.

## Route C — Cloud / remote (`EXTERNAL_DEPENDENCY` + fixture fallback)

- **Optional live:** ask the same practical question in a cloud/browser assistant you already use. Do not paste private context. Capture observations only (not full account screenshots with identifiers).
- **Equity path (required when live is unavailable):** use `fixtures/route_c_transcript.md` labeled `FIXTURE` / `illustrative`.

## Route Paper — No-device fallback (`FIXTURE_VALIDATED`)

Print or read both fixture transcripts and complete the comparison table + consent card on paper or in Markdown. Keyboard-only digital worksheet is also fine.

## Evidence (completion ≠ command ran)

| Artifact | Required contents |
|---|---|
| Comparison table | Observations: time-to-first-token or wall time if measured; network required? (Y/N); data leaving device? (claimed/unknown); errors/hedges noticed |
| Consent/trust card | Audience, purpose, data classes, retention, opt-out, AI disclosure |
| Dual-ledger note | One human-trust feeling + one technical-trust control |
| Uncertainty note | One fluent-but-wrong or unverifiable claim (or “none observed” + what was checked) |

Mark Stability Contract bounds as in-bounds / out-of-bounds / unknown (see CE-5 `STABILITY_CONTRACT.md`).

## Pathway extensions

| Pathway | Task |
|---|---|
| Explorer | Fill observation columns; one-sentence teach-back |
| Operator | Classify a failure symptom: authn / authz / network / model quality |
| Builder | Add one redaction rule for `fixtures/sample_log_line.txt` |
| Engineer | Sketch trust boundaries crossed by Route C |
| Researcher | Hypothesis + limitation (n=1, fixture bias) |
| Educator | No-device storyboard + misconception drill (see `extensions/educator.md`) |

## Interpretation

### Observation

What text, timings, and network/locality claims did you directly see?

### Explanation

What might explain differences between Route L and Route C?

### Causal caution

What extra evidence would you need before blaming the model, the network, authn, or authz?

## Limits

- Fixtures are teaching data, not gunnchOS product benchmarks.
- No Device Quartet physical AI measurements (`PHYSICAL_PENDING`).
- “Encrypted in transit” does not equal “private forever.”
- This lab does not map to a WAIKE ID named `LAB-TRUST-001`.

## Portfolio

Use `portfolio/` as the template. Copy fixtures into your own filled artifacts; do not invent latency numbers as product measurements.

## A11y / privacy / safety

See `A11Y_PRIVACY_SAFETY.md`.
