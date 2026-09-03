# CE-1 Experience Map

**Chapter:** Technology Is a System, Not a Screen (CE-1 / CH01)  
**Status:** preproduction  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

Avoids duplicating Chapter 2’s one-tap end-to-end sequence. Experiences teach the **system lens** (visible surface vs hidden cooperating parts).

---

## Canonical anchor (selected)

### Experience A — Chrome ready before content usable

**Human moment**  
You unlock a familiar phone, tablet, or laptop and open something you use often. The app **chrome** appears quickly (title, nav, skeleton, splash). The **usable content** arrives later—or fails while the chrome still looks fine.

```text
Human moment
↓
Observable behavior: chrome/skeleton visible; list/tiles/content empty, stale, or spinning
↓
Hidden systems: process start, app state restore, storage reads, caches, optional sync/API, renderer, optional radio/path to service
↓
Likely failure modes: slow storage; blocked main thread; expired session; DNS/service outage; airplane mode; offline cache miss; thermal/power throttle that still “shows” UI
↓
Measurement / inspection opportunity: wall-clock chrome-visible vs content-usable; offline vs online comparison; status icons vs actual usability (observation vs inference)
↓
Career / system connection: UX (perceived readiness), app/frontend (loading states), backend/SRE (service health), network ops, accessibility (announce busy/ready), support triage
```

**Why this is the canonical anchor**

- Broadly universal across ages and devices.
- Makes **visible interface ≠ whole system** unavoidable.
- Naturally introduces **inputs → processing → state → outputs** and **optional network**.
- Leaves the detailed gesture→stack path for CE-2 without overlap.

---

## Alternate experience B — Offline media vs streaming media

**Human moment**  
You play a song or video that is already on the device, then play one that must stream.

```text
Human moment
↓
Observable behavior: local item starts promptly; stream may buffer, drop quality, or stall while playback UI still looks “playing”
↓
Hidden systems: local storage/decode path vs buffer + network + CDN/edge + codec pipeline
↓
Likely failure modes: weak signal; buffer underrun; DRM/license check; decode overload; storage corruption of local file
↓
Measurement / inspection opportunity: note start delay and stall counts; compare airplane-mode local success vs stream failure
↓
Career / system connection: media engineer, wireless/network, edge/CDN, device power/thermal
```

**Teaching use:** Reinforces **local-only vs network-dependent** branches without a tap-sequence narrative.

---

## Alternate experience C — “Bars look fine” but the needed service fails

**Human moment**  
The device shows connectivity (Wi-Fi/cellular indicator), yet a specific portal, map tiles, or message sync will not complete.

```text
Human moment
↓
Observable behavior: connectivity icon healthy; target experience unusable or partially usable
↓
Hidden systems: radio association ≠ DNS ≠ route ≠ TLS ≠ auth session ≠ application API health
↓
Likely failure modes: captive portal; DNS failure; service outage; auth expiry; app bug; content blocked; VPN misconfig
↓
Measurement / inspection opportunity: compare icon state (observation) with a second local action that does not need the network; document what extra evidence would blame the service
↓
Career / system connection: network engineer, SRE, security/identity, helpdesk triage, digital-equity analysis
```

**Teaching use:** Separates **link-layer “connected”** from **experience success**—prepares Stability Contract language for CE-6 without inventing budgets.

---

## Experience selection summary

| ID | Experience | Role in CE-1 |
|---|---|---|
| A | Chrome before content | **Canonical anchor** |
| B | Offline vs streaming media | Contrast local vs remote paths |
| C | Healthy bars, failed service | Failure-domain honesty |

## Device Quartet note (non-marketing)

When form factors appear later, treat Student 14.5", Handheld Hybrid, DS-XL Coder, and Edge IO Wearables as **research / learning benchmarks** (PHYSICAL_PENDING). CE-1’s labs run on **commodity devices learners already own**; Quartet is foreshadowed as a future shared laboratory spine, not a product pitch.
