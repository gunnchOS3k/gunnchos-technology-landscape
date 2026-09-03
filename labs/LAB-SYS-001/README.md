# LAB-SYS-001 — Name the System Behind a Familiar “Open”

**Chapter:** CE-1 / CH01  
**Status:** `IMPLEMENTED_DIGITAL` (fixture available; not a human-learning PASS)  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Observable question

> When I open something I already use, what becomes visible first, what becomes usable later, and which hidden parts might still be working?

## Why this lab (vs LAB-TAP-001)

`LAB-TAP-001` traces and times a **tap-to-response** path. This lab is a **system-lens** exercise: readiness, layers, dependencies, and failure domains—**without** duplicating one-tap instrumentation.

## Safety and privacy

- Do not capture passwords, tokens, private chats, ID photos, or classmate PII.
- Prefer the supplied fixture or public demo pages in shared spaces.
- No packet capture of others’ traffic; do not disable required safety features.
- Scrub identifiers before saving portfolio evidence.

## Time estimate

About 45 minutes for the Explorer baseline.

## Prediction

Before opening anything, write whether you expect **chrome** (shell/nav/title) or **content** (usable body) to become ready first, and why.

## Routes

### Route A — Browser (baseline)

1. Open `labs/LAB-SYS-001/browser/index.html` in a desktop browser.
2. Watch once without changing settings.
3. Record wall-clock (or on-page) times for **chrome visible** and **content usable** (or failed).
4. List ≥3 visible cues and ≥3 guessed hidden parts (mark guesses as inference).

### Route B — Local observation sheet (baseline, no special hardware)

```bash
python3 labs/LAB-SYS-001/local/observation_sheet.py
```

Prints a large-print structured sheet you can fill while opening a familiar app, or while using the fixture.

### Route C — Offline fixture (required fallback)

1. Open `labs/LAB-SYS-001/fixtures/readiness_demo.html` (works offline once loaded from disk).
2. Use **Simulate offline** to contrast chrome-still-visible vs content failure.
3. Or use `fixtures/scenario_card.md` (labeled **fixture / illustrative**) for Explorer/Educator only.

## Depth ladder

### Explorer — observe / identify

Choose one familiar open (or the fixture). Record chrome-visible and content-usable times. List visible cues and guessed hidden parts.

### Operator — inspect / compare

Repeat once “online” and once offline/airplane (if safe) or use the fixture offline toggle. Fill the observation table; assign a **failure domain** guess only as inference.

### Builder — modify / create

Fill the ecosystem-map template; adapt the readiness checklist; document one privacy/detail tradeoff.

### Engineer — measure / diagnose

Separate observation / interpretation / causal claim. State what extra evidence would be needed before blaming network vs app vs storage. Optional DevTools only on non-sensitive pages; scrub secrets.

### Researcher — hypothesis / controlled comparison

Example: “For experience X, offline mode increases content-usable delay or causes failure while chrome still appears.” Define small N, environment notes, and limits—not a publication benchmark.

### Educator — facilitate / adapt

10–15 minute misconception probe (screen-as-system vs screen-as-surface). Offer fixture/scenario fallback when networks or personal apps are unavailable.

## Observation vs inference

| Allowed as observation | Inference until more evidence |
|---|---|
| Chrome appeared at time T1 | “Network is bad” |
| Content usable/failed at T2 | “Storage is dying” |
| Airplane mode was on/off | “DNS failed” |
| Icon/text showed connected | “Server is down” |

## Accessibility

- Keyboard / switch / voice “open” paths count.
- Audio notes may replace screenshots.
- Observation sheet is structured text (large-print friendly).
- Readiness is labeled in text; color is not required.

## Evidence and portfolio

Minimum packet under `labs/LAB-SYS-001/portfolio/`:

- readiness observation table,
- labeled ecosystem map,
- observation vs inference paragraph,
- scrubbed evidence note,
- optional teach-back.

## Limits

- Fixture delays are illustrative teaching signals, not measured device architecture.
- One run ≠ benchmark.
- Personal-app runs stay private; prefer fixture when sharing.

## Gate status

`GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` — this lab package does not claim Gate 3 PASS.
