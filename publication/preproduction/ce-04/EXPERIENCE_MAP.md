# CE-4 Experience Map

**Module:** CE-4 — Packets, Wi-Fi/Cellular, Edge and Cloud  
**Status:** `preproduction`  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING` (no Gate 3 PASS claim)

Teaching chain for every experience below:

```text
Human moment
↓
Observable behavior
↓
Hidden systems
↓
Likely failure modes
↓
Measurement or inspection opportunity
↓
Career/system connection
```

---

## Experience A — Canonical anchor: “Sent” then stall (path & placement)

### Human moment
You send a short message or save to a shared document. The UI shows progress (“sending,” “syncing,” checkmarks) then hangs, errors, or suddenly finishes after you change location or radios.

### Observable behavior
- Progress spinner / “waiting for network”
- Partial success (local draft saved, remote not updated)
- Recovery when moving closer to an AP, toggling Wi-Fi/cellular, or leaving a captive portal

### Hidden systems
- Local app + OS networking stack
- DNS / name resolution (when names are used)
- Packets with layered headers; gateway/NAT on many home/campus paths
- Wi-Fi association **or** cellular attachment (distinct access networks)
- Internet routing toward a service that may be **edge-near** or **cloud-far**
- Transport retries / timeouts shaping “feels stuck”

### Likely failure modes
- Access network usable for some destinations but not others
- DNS failure or stale cache
- Captive portal / authentication gate
- Remote service overload or regional outage while radio looks fine
- Path change mid-session (Wi-Fi→cellular) without graceful continuity

### Measurement or inspection opportunity
- Commodity: browser DevTools Network / Resource Timing; OS connectivity indicators; wall-clock phases
- Fixture fallback: crafted packet/datapath JSON or recorded timing table (LAB-PKT-001 Route B)
- **Do not** invent RF drive-test numbers

### Career/system connection
Network engineering, SRE/cloud, wireless engineering, IT support—each owns a different hop in the same story.

### Why this is the canonical anchor
It is nearly universal, works on commodity devices, forces the non-synonym distinctions (Wi-Fi/cellular/Internet/cloud), and supports Explorer→Educator depth with an offline fixture.

---

## Experience B — Video call “connected” but unusable (latency vs throughput)

### Human moment
A call shows connected participants, yet speech stutters, tiles freeze, or only one direction works.

### Observable behavior
- UI still shows “in call”
- Glitches under motion or congestion
- Screen share fails while chat still works (or reverse)

### Hidden systems
- Real-time media vs elastic web traffic competing on the same access link
- Jitter buffers; loss concealment; TURN/relay paths (concept level)
- Uplink vs downlink asymmetry on cellular or saturated Wi-Fi

### Likely failure modes
- Latency/jitter dominate even when average throughput looks “enough”
- Asymmetric path problems
- Device thermal/CPU limits misread as “network”

### Measurement or inspection opportunity
- Qualitative: note stall frequency under two conditions (still vs walking; Wi-Fi vs cellular)
- Optional Engineer: compare chat (reliable/elastic) vs media (latency-sensitive) behavior—no fake MOS scores

### Career/system connection
Performance engineering, wireless engineering, realtime media/SRE collaboration.

---

## Experience C — Same account, different feel at café Wi-Fi vs home (equity & continuity)

### Human moment
Homework portal or banking app feels fine at home, painful or blocked on public/café Wi-Fi—or works on cellular when Wi-Fi is captive.

### Observable behavior
- Login loops; certificate/captive interstitial; slow first paint then fast navigation (or reverse)
- Feature subset disabled offline

### Hidden systems
- Captive portals and middleboxes
- Split DNS / private vs public name views
- CDN/edge caches near some networks but not others
- Policy differences (firewall, TLS inspection in managed networks—discussed carefully)

### Likely failure modes
- Treating all Wi-Fi as equivalent
- Assuming cellular is always the “fix” path (cost, coverage, privacy differ)
- Excluding learners who lack stable home broadband

### Measurement or inspection opportunity
- Compare three conditions if safe: home Wi-Fi, public Wi-Fi, cellular—**never** capture passwords or personal account contents
- Fixture: supplied captive-portal storyboard + timing table for classrooms without public Wi-Fi

### Career/system connection
IT support, network security policy, digital equity / accessibility advocacy, cloud edge placement.

---

## Selection decision

| Experience | Role in CE-4 |
|---|---|
| **A — sync stall / recovery** | **Canonical anchor** (lab + stability contract + figures) |
| B — call connected but unusable | Contrast for latency/reliability vs throughput teaching |
| C — café vs home | Equity, captive portals, continuity across access networks |

Secondary experiences B and C appear in misconception checks and Secure/Include sections; they do not replace A as the lab anchor.
