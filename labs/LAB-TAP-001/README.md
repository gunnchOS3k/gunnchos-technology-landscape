# LAB-TAP-001 — Trace and Measure One Tap

## Observable question

> How much of a tap-to-response path can I directly observe on a device I already own?

## Safety

- Do not capture passwords, tokens, private chats, or personal identifiers.
- Use the supplied local demos when possible.
- No proprietary gunnchOS hardware is required.

## Time estimate

About 45 minutes for the baseline route.

## Prediction

Before running, write which portion you expect to take longest:

1. input recognition / event delivery,
2. local handler work,
3. network/service (if used),
4. rendering / visible update.

## Route A — Browser (baseline)

1. Open `labs/LAB-TAP-001/browser/index.html` in a desktop browser.
2. Open developer tools (Network + Performance or console timestamps).
3. Click **Local only** and note immediate feedback timing.
4. Click **Fetch remote sample** and compare.
5. Record timestamps from the on-page table and/or DevTools.

## Route B — Local application (baseline)

```bash
python3 labs/LAB-TAP-001/local_app/tap_timer.py
```

Click the buttons and copy the printed timestamp table.

## Route C — Android-compatible extension (optional)

Where an Android device/emulator is available, install or run any simple app you can instrument with log timestamps around click handlers and network calls. Do not require root. Capture log excerpts only after scrubbing secrets.

## Evidence

Minimum:

- screenshot or log,
- timestamp table,
- short explanation separating observation vs inference.

## Interpretation

### Observation

What timestamps and UI changes did you directly see?

### Explanation

What might explain the differences between local-only and network-dependent actions?

### Causal caution

What additional evidence would you need before blaming the network, the app, or the device?

## Limits

- Software timestamps are not physical touch-to-photon measurements.
- Logging itself adds overhead.
- One run is not a benchmark.

## Builder extension

Add more instrumentation markers (for example, paint/visible callback approximations).

## Researcher extension

Repeat N times, report a summary statistic and variability, and document environment controls.

## Teach-back

Explain your result to a nontechnical person without using the words kernel, interrupt, API, or packet. Then introduce those terms one at a time.

## Portfolio output

Use `labs/LAB-TAP-001/portfolio/` as the template.
