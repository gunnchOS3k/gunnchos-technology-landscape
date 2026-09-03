# LAB-CE06-001 — Explain, Measure, Improve, and Teach

**Chapter:** CE-6 (publication-owned capstone)  
**EMIT spine:** Explain → Measure → Improve → Teach  
**Status:** `FIXTURE_VALIDATED` (illustrative fixtures + digital stall demo)  
**Gate posture:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
**Hardware rule:** Commodity devices only. No Device Quartet / specialized lab gear.

## Observable question

> Using the book’s full model, what evidence can I gather—on devices and tools I already have—to explain a real experience, measure what is actually observable, propose one improvement, and teach the ecosystem to someone else?

## Capstone prompt

Choose a real technology experience you can access ethically. **Explain** its ecosystem with the book’s model. **Measure** what you can on commodity tools (or fixtures). **Improve** one bounded aspect and state how you would know it worked. **Teach** the Stability Contract for that experience to another person.

## Safety / privacy

- No passwords, tokens, private messages, health data, or classmate PII.
- Prefer local demos or supplied fixtures.
- No unauthorized scanning, rooting, jailbreaking, or attacking systems.
- Metered-data warning: use Route F (fixture) or browser throttle.

## Time estimate

45–90 minutes for Route A / Route F baseline.

## Prediction (required)

Before measuring, predict which **failure domain** will dominate:

input · compute/schedule · memory/storage · network path · service/backend · render/display · power/thermal · trust/permissions · equity/access

## Route A — Notebook + status UI (baseline)

1. Choose the default anchor (**connected but unusable** send/submit/sync) or an allowed substitute.
2. Reproduce once on a phone, tablet, or computer you already own.
3. Record OS connectivity status **separately** from whether the action finished for a human.
4. Optional: open browser DevTools Network/Performance for a web experience.
5. Fill the blank portfolio under `portfolio/` (all EMIT + capstone fields).

## Route B — Local stall demo (optional commodity)

Open `browser/index.html` in a desktop browser. The page intentionally stalls a “send” while local UI still updates. Compare local feedback vs stalled remote path. Label every timing **observed** (on-page) vs **inferred**.

```bash
# from repo root (or open the file directly)
open labs/LAB-CE06-001/browser/index.html
```

## Route F — Fixture fallback (mandatory offline path)

When live reproduction is unsafe, offline, inaccessible, or metered:

1. Read `fixtures/sample_observation.md` and `fixtures/sample_result_table.csv`.
2. Optionally study `fixtures/illustrative_example/` (**ILLUSTRATIVE ONLY — not human evidence**).
3. Still complete: observation vs inference labels, diagnosis shortlist, Improve plan, teach-back.
4. Mark fixture-derived rows as `fixture` in your result table.

## Pathway depth

| Level | Expectation |
|---|---|
| Explorer | Experience + ≥4 contract conditions (observed vs guessed) + ecosystem path + teach-back |
| Operator | Explorer + ≥3 inspection artifacts + one comparison + failure-domain shortlist |
| Builder | Operator + reusable checklist/helper + tradeoff + Improve plan |
| Engineer | Diagnosis tree + two claims on evidence hierarchy + instrumentation limits |
| Researcher | Falsifiable hypothesis + ≥3 confounders; no invented statistics |
| Educator | Facilitation plan + misconception prompts + score with `rubric.yaml` |

## Capstone fields (required portfolio set)

human experience · system boundary · components · software/code role · network role · Stability Contract · observations · inferences · measurements · evidence limitations · security/privacy/accessibility · equity/societal impact · proposed improvement · teach-back · portfolio summary

Blank templates live in `portfolio/`. Validator: `validate_portfolio.py`. Export: `export_portfolio.py`.

## Observation vs inference

- **Observation:** timestamps, status strings, HTTP codes, visible stalls, AT announcements.
- **Inference:** “DNS is broken,” “server overloaded,” without supporting signals.
- **Causal claim:** needs boundary evidence and remaining alternatives.

## Limits

- Software timestamps are not physical touch-to-photon or RF measurements.
- One run ≠ benchmark; label illustrative vs measured.
- Fixture / illustrative packets are teaching data, not product SLOs or Gate evidence.

## Portfolio output

Use `labs/LAB-CE06-001/portfolio/` as the blank template. See also `rubric.yaml`.
