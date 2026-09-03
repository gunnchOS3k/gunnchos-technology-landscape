# Route A — Browser feel timeline

## Goal

Make continuous-interaction feel visible with wall-clock timing and optional browser performance tools.

## Steps

1. Write your prediction (axis + local/network/unclear).
2. Open a mostly local page (long local HTML document, notes app web view, or synthetic demo). Prefer content without personal data.
3. **Condition 1 (idle/light):** perform a fixed action (for example, 10 deliberate scrolls or 10 local button updates). Record wall-clock with a simple timer.
4. Note feel words: fast / slow / smooth / unstable.
5. If available, capture Performance / Resource Timing entries the browser exposes. If a metric is unavailable, write `unavailable`—do not invent it.
6. **Condition 2 (mild load):** open a few extra tabs or a second local document. Repeat the same fixed action. Record wall-clock and feel words again.
7. Fill observation vs inference columns in `portfolio/observation_table.csv`.

## Stop rules

- Stop if the device warns about heat or becomes uncomfortably hot.
- Do not capture passwords, tokens, or private page content.
