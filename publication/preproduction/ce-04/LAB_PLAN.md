# CE-4 Lab Plan — LAB-PKT-001

**Provisional lab ID:** `LAB-PKT-001`  
**Title:** Trace One Connected Action Across Path and Access  
**Chapter:** CE-4  
**Anchor experience:** Sync/send stalls or recovers when path or access changes  
**Status:** `preproduction` (publication-owned; not a WAIKE module ID)  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

---

## Question

When a connected action feels stuck, what parts of the path can I **observe** on a device I already own—and what must I treat as **inference**—including whether the issue looks like **latency**, **reliability**, or **throughput**, and whether **Wi-Fi**, **cellular**, or a **fixture** path was in play?

---

## Pathway depth

| Pathway | Learner action |
|---|---|
| Explorer | Observe UI cues; label local vs LAN vs Internet hypothesis; name access network if known |
| Operator | Inspect browser/OS network indicators; compare two conditions; fill observation table |
| Builder | Create labeled path diagram; optionally edit fixture timing JSON/Markdown template |
| Engineer | Diagnose ordered hypotheses (access → DNS → reachability → transport/retries → remote placement) |
| Researcher | Controlled comparison (N≥3 runs) with confounders listed; no published benchmark claim |
| Educator | Facilitate misconception check; run fixture route when live networks are unsafe/unavailable |

---

## Required devices / software

**Preferred (Route A — live commodity):**
- Phone or laptop the learner already owns
- Modern browser with developer tools **or** OS network settings screens
- Optional: ability to toggle Wi-Fi vs cellular safely

**Not required:**
- Spectrum analyzers, SDR, operator base stations, enterprise controllers
- Paid cloud accounts
- Root/jailbreak

**Software for fixture route:** Python 3 optional; Markdown/CSV editor sufficient

---

## Lowest-friction route (Route A)

1. Predict: will failure feel like wait (latency), retry/error (reliability), or long transfer (throughput)?  
2. Perform one familiar sync/send/open-online-doc action on current access network.  
3. Record wall-clock or browser Network/Resource Timing phases if available (DNS / connect / waiting / download—as exposed).  
4. Change **one** condition (airplane mode briefly, Wi-Fi off→cellular, or move location) and repeat.  
5. Label observation vs inference; do not claim RF root cause from bars alone.

---

## Offline / fixture fallback (Route B) — mandatory accessible path

When live networks are unavailable, unsafe (public Wi-Fi credential risk), or inaccessible:

1. Use **supplied fixtures** (to be authored with the lab implementation wave):  
   - `fixtures/sample_path_trace.json` — crafted Ethernet/IPv4-oriented field parse story compatible with WAIKE `lab_datapath` *competency adjacency* (not a copied validator submission requirement)  
   - `fixtures/sample_timing_table.csv` — DNS vs connect vs wait vs transfer illustrative rows labeled `ILLUSTRATIVE_FIXTURE`  
   - `fixtures/sample_observation.md` — filled example with observation/inference tags  
2. Learner answers parse/identification questions and redraws the path.  
3. Explicit honesty banner: fixture rows are **not** the learner’s device measurements.

This satisfies “accessible packet-path or connectivity lab with fixture fallback.”

---

## Expected evidence artifact

Portfolio folder proposal: `labs/LAB-PKT-001/portfolio/` (implementation later)

| Artifact | Required |
|---|---|
| Observation / timing table | Yes |
| Path diagram (local/LAN/Internet + access + placement hypothesis) | Yes |
| Screenshot **or** fixture note proving which route was used | Yes |
| Reflection separating observation vs inference | Yes |
| Teach-back paragraph (Wi-Fi ≠ Internet ≠ cellular ≠ cloud) | Yes |

---

## Observation vs inference boundary

**Observation examples:** UI said “waiting for network”; browser showed DNS time; Wi-Fi icon on; cellular icon on; fixture TTL field equals N.  
**Inference examples:** “The tower is congested”; “the cloud region failed”; “DNS is broken” without name-resolution evidence.  
**Causal claims** require extra evidence named in the diagnosis plan.

---

## Privacy / safety boundary

- Do **not** capture passwords, session tokens, message bodies, banking amounts, or classmate personal data.  
- Prefer demo pages, public documentation URLs, or fixtures.  
- No unauthorized scanning of others’ networks; no packet capture on networks you do not administer unless local loopback/demo and policy allows.  
- No radio transmission experiments; no bypass of captive-portal terms.  
- Public Wi-Fi: prefer fixture route for classrooms.

---

## Accessibility considerations

- Keyboard-only and screen-reader-friendly instructions; avoid color-only status.  
- Fixture route for learners without personal hotspots or unstable home broadband.  
- Text equivalents for all figures produced in the lab.  
- Allow voice notes as reflection alternative where writing is a barrier (educator adaptation).  
- Timebox: target ≤45–60 minutes baseline.

---

## Reproducibility strategy

- Record device type (general), route (A/B), access mode, timestamp source, browser/OS name if used.  
- N=1 is learning; Researcher path states N and variance qualitatively.  
- Fixture SHA/path recorded when Route B used.  
- Ban bare `PASS` as evidence (align with WAIKE validator honesty culture without claiming WAIKE ownership of this lab).

---

## Portfolio artifact produced

A reusable **path + placement one-pager** showing:
- scopes (local/LAN/Internet),
- access network,
- edge/cloud hypothesis,
- metric family (latency/reliability/throughput),
- evidence pointers.

---

## WAIKE adjacency (not identity)

See `WAIKE_CROSSWALK.md`. Closest accepted-main neighbors include `COMPUTER_NETWORKING` / `lab_datapath`, `GENERAL_IT` / `lab_dns_hosts`, `CLOUD_DEVOPS` placement/cost labs, and limited `WIRELESS_6G` radio-intuition labs—**adjacent**, not renamed into LAB-PKT-001.
