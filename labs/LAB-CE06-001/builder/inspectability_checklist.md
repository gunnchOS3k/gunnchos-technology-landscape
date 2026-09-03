# Builder helper — inspectability checklist

Reusable checklist that makes **one** Stability Contract condition more inspectable on commodity devices.

## Target condition (pick one)
Example: SC-05 network path usable *if* remote work is required.

## Checklist
1. Record connectivity **text** (not color alone) before the action.
2. Record whether the human action completed (yes/no/unknown).
3. If browser DevTools available: note request start and whether a response status appeared (no payloads with secrets).
4. Run one comparison (Wi‑Fi vs cellular, or online vs offline/fixture).
5. Label every row observed / inferred / fixture.

## Tradeoff introduced by this helper
More inspection can expand privacy surface (screenshots/logs). Default to least data and redaction.
