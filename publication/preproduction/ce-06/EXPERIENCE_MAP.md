# CE-6 Experience Map

**Chapter:** CE-6 — The Stability Contract + Capstone  
**Teaching model:** Human experience → system → component → code → network → society  
**Rule:** synthesize CE-1…CE-5; do not restart as a second one-tap chapter.

---

## Canonical anchor experience (selected)

### A. “Connected but unusable” send / submit / sync

**Why canonical:** Universally recognizable, needs no specialized hardware, forces concurrent-condition thinking, and naturally reaches equity (who still gets a usable experience). It synthesizes CE-2’s local-vs-network distinction, CE-4 connectivity, CE-3 resource pressure, and CE-5 trust/privacy of traces — without replaying the full tap path lecture.

```text
Human moment
  Person tries to send, submit, refresh, or sync a familiar action.
  Status shows online / connected; progress stalls, flickers, or never finishes.

Observable behavior
  Spinner persists; partial UI update; retry prompts; offline banner absent;
  or success toast without confirmed remote effect.

Hidden systems
  Radio/link association; DNS/TLS/path; transport retries; app event loop;
  storage flush; service availability; auth/session; render/compositor;
  power/thermal throttling; assistive-tech path timing.

Likely failure modes
  Link up but high loss/latency; DNS/TLS stall; main-thread blocked;
  storage IO wait; service 5xx/timeout; token expiry; render jank;
  aggressive battery saver; a11y path missing equivalent feedback.

Measurement or inspection opportunity
  Commodity: OS link status, browser DevTools timings, app retry logs,
  Performance API marks, airplane-mode A/B, supplied fixture traces.
  Label every number observed / inferred / illustrative.

Career/system connection
  SRE / network / frontend / backend / accessibility / TPM ownership map.
```

---

## Alternate experience 1

### B. Video / call / stream quality collapse under mobility or contention

```text
Human moment
  A call, class stream, or video suddenly becomes choppy or freezes while
  the app still shows “connected.”

Observable behavior
  Frozen frames, audio glitches, resolution drops, reconnect banners.

Hidden systems
  Radio conditions; jitter buffer; codec adaptation; CDN/edge placement;
  CPU decode budget; thermal throttling; uplink contention.

Likely failure modes
  Throughput ok but latency/jitter bad; adaptation too slow; decode overload;
  background upload stealing budget; weak uplink with strong downlink.

Measurement or inspection opportunity
  App stats panels where available; repeat under Wi‑Fi vs cellular;
  note what cannot be measured without vendor tools (do not invent RF budgets).

Career/system connection
  Wireless, media, edge, performance engineering; digital-equity classroom access.
```

**Role in CE-6:** optional Engineer/Researcher extension; not required for Explorer baseline.

---

## Alternate experience 2

### C. Assistive or low-cost path divergence (“works for me”)

```text
Human moment
  Task completes for one person/device profile and fails or is painfully slow
  for keyboard-only, screen-reader, low-end device, metered link, or offline-first user.

Observable behavior
  Focus traps; missing labels; timeouts; huge downloads; features gated on
  always-on cloud AI; no offline fallback.

Hidden systems
  Accessibility tree / AT APIs; permissions; CDN asset weight; client-side
  compute assumptions; identity/CAPTCHA friction; telemetry consent defaults.

Likely failure modes
  Experience contract silently assumes mouse, vision, strong CPU, unlimited data;
  “secure” flows that exclude; AI features that require cloud round-trips.

Measurement or inspection opportunity
  Keyboard-only run; reduce bandwidth (browser throttle); use fixture “low-end”
  timeline; WCAG-oriented checklist (intent, not certification claim).

Career/system connection
  Accessibility engineering, product ethics, SRE error budgets that include
  inclusion, educator facilitation of equitable labs.
```

**Role in CE-6:** required lens inside Secure & Include + capstone Improve/Teach; can be the primary experience for Educator/A11y-focused readers.

---

## Selection rationale summary

| Experience | Universality | Hardware demand | Synthesis power | Capstone fit |
|---|---|---|---|---|
| **A Connected but unusable (anchor)** | High | Commodity only | High across CE-1…5 | Best default |
| B Stream/call collapse | Medium–high | Commodity; RF tools optional | Strong CE-4/perf | Extension |
| C Works-for-me divergence | High | Commodity + AT if owned | Equity/a11y core | Required lens |

---

## Capstone binding

Whatever experience the reader chooses, the portfolio must cover:

1. **Explain** the ecosystem path  
2. **Measure** what is actually observable  
3. **Improve** one bounded change with evidence criteria  
4. **Teach** via teach-back to a peer / learner
