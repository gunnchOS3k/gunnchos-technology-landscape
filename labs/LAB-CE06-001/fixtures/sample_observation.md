# Sample observation (fixture)

**Route:** F — supplied fixture (no live network required)  
**Label:** `fixture` — illustrative teaching data, **not** a device or product benchmark  
**Anchor:** Connected-but-unusable send/submit/sync

## Environment (class only)

- Device class: laptop
- OS name: illustrative desktop OS
- Browser: illustrative modern browser
- Network class: fixture (simulated Wi‑Fi “connected”)

## Observation

1. Connectivity status text showed **Connected** before the send attempt.
2. Learner pressed **Send** on a benign local demo form.
3. Local button state changed to “Sending…” within the same second (UI feedback observed).
4. No completion toast appeared within a 15-second wall-clock window.
5. After ~15s, a retry prompt appeared: “Still working — try again?”
6. Airplane-mode comparison was **not** run in this fixture packet (explicit gap).

## Inference (not proven by this fixture)

The stall is **consistent with** a delayed or unavailable remote path while local UI remained responsive. This does **not** prove DNS failure, server overload, or thermal throttle.

## Under-determined domain

Service/backend vs network path vs client retry policy remain under-determined without request timing, status codes, or service health signals.

## Limits

- Fixture timings are authored for teaching, not measured from a production product.
- Do not cite this packet as human reader evidence or Gate proof.
