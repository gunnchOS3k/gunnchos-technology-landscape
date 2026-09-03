# CE-4 Stability Contract (preproduction)

**Anchor experience:** A send/sync action remains *human-usable* across ordinary path and access conditions.  
**Status:** Qualitative only — **no invented numeric budgets**.  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

---

## Contract statement

A connected experience continues only while multiple hidden conditions remain within acceptable bounds at once: local device readiness, access-network attachment, name resolution when names are used, reachable routing toward the service, transport/application retry behavior that finishes in time for the human task, and a healthy enough edge/cloud placement.  

A system can remain technically “connected” (radio icon, association, or bearer present) while the human experience has already failed.

---

## Hidden technical conditions (qualitative)

| Condition | Why it matters to the anchor |
|---|---|
| Device local stack responsive | App/OS must be able to enqueue and process network work |
| Access attachment meaningful | Wi-Fi association or cellular attachment must exist *for the needed path* |
| Auth/captive gates cleared | Portal or credentials may block Internet scope despite LAN/Wi-Fi up |
| Name resolution (if used) | Wrong/stale/failed DNS yields “connected but useless” |
| Next-hop / routing reachability | Gateway or upstream path must forward toward the service |
| Transport/application progress | Retries/timeouts must not strand the UI in eternal “sending” |
| Remote service placement healthy | Edge/cloud dependency must accept and complete the sync |
| Continuity across changes | Path/access switches must not silently drop user-visible state |

---

## Failure domains

1. **On-device** — app bug, OS network stack stuck, storage full for draft, CPU/thermal overload misread as network.  
2. **Access network** — Wi-Fi congestion/interference; cellular coverage/policy; wrong VLAN/guest isolation.  
3. **Naming & middleboxes** — DNS, captive portal, NAT binding issues.  
4. **Path / Internet** — routing failure, congestion, filtering.  
5. **Placement / service** — edge/cloud outage, overload, region mismatch.  
6. **Human/task** — expectation that “sent” means peer received when only local queue succeeded.

---

## Dependencies

- Prior CE mental models: CE-1 ecosystem lens; CE-2 observation vs inference; CE-3 local compute/storage so “slow” is not always network.  
- External: operator/campus networks, DNS, remote services—often unowned by the learner.

---

## Locally observable symptoms

- Spinner / “waiting for network” / delayed checkmarks  
- Works on cellular but not café Wi-Fi (or reverse)  
- Chat works while large upload fails (throughput vs latency/reliability contrast)  
- Immediate failure vs long stall  
- Recovery after moving closer to AP or toggling radios

---

## Measurements that would support diagnosis (when available)

- Browser Resource Timing / Network waterfall phases  
- OS reports of Wi-Fi vs cellular active interface  
- Fixture field parse proving header/TTL/LPM reasoning (Route B)  
- Repeated runs under controlled condition changes (Researcher path)

---

## Measurements we cannot yet obtain (do not invent)

- Authoritative RF drive-test metrics for reader devices in CE-4  
- Operator core traces  
- Exact edge PoP geolocation proof for arbitrary consumer apps  
- Universal millisecond SLOs for the anchor experience  
- Certified 6G performance claims

---

## Human consequence

Learners miss deadlines, lose trust in “the Internet,” or blame themselves/devices when the failure domain is path, naming, or remote placement. Equity impact: learners on contested shared Wi-Fi or metered cellular face different stability envelopes than peers on stable home broadband—without any change in their effort.
