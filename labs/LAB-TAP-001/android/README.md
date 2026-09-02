# Route C — Android-compatible extension

This route is optional and must not block baseline completion.

## Goal

Capture application log evidence around:

- input/click handler entry,
- network request start/end (if any),
- UI update.

## Constraints

- No root access required.
- No proprietary gunnchOS device required.
- Scrub secrets before saving logs into portfolio evidence.

## Suggested method

1. Use Android Studio Logcat or `adb logcat` with an app you can modify.
2. Log timestamps at handler start/end and around requests.
3. Export a short scrubbed excerpt to `portfolio/evidence/`.
