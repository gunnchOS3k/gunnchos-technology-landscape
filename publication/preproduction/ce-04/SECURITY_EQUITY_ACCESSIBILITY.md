# CE-4 Security, Equity, and Accessibility Plan

**Module:** CE-4  
**Status:** `preproduction` — weave into technical story; not a final-page disclaimer  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

---

## Where these themes enter the chapter anatomy

| Section | Natural entry |
|---|---|
| The moment / What you notice | Captive portals, “connected but blocked,” metered warnings |
| Exploded ecosystem | Who can observe packets at each hop |
| Follow the signal | Encryption-in-transit concept (TLS) without packet-snooping labs |
| Component cards | DNS trust, gateway as policy point |
| Stability contract | Continuity vs attachment; equity of network assumptions |
| Try it / Build it | Privacy rules for captures; fixture fallback |
| Secure and include it | Primary home for threats, privacy, a11y, equity |
| Career lens | Security + support + wireless roles |
| Check understanding | Misconception: public Wi-Fi is “the same Internet” |

---

## Security boundaries

- **Threats in-scope (concept):** eavesdropping on open Wi-Fi, captive-portal phishing patterns, credential reuse on public networks, malicious free VPNs (warn, don’t tutorial abuse), confusing Wi-Fi evil-twin at awareness level.  
- **Controls in-scope (concept):** prefer HTTPS/TLS sessions (RFC 8446 adjacency), avoid sending secrets on untrusted networks, use official apps/sites, understand that “Wi-Fi on” is not a security state.  
- **Out of scope:** exploit development, cracking WPA, unauthorized scanning, interception labs, bypassing access controls.  
- **Lab rule:** no capture of secrets; no attacking networks.

---

## Privacy concerns

- Network screenshots may reveal hostnames, account emails, locations, or message previews—redact.  
- Timing tables should store action labels, not payload content.  
- Cellular vs Wi-Fi choice can leak location patterns; discuss without collecting learner location trails.  
- Cloud/edge placement implies third-party processing—tie forward to CE-5 without dumping full privacy law.

---

## Accessibility concerns

- Network status UIs often rely on color icons (bars/waves)—require text status in lab writeups.  
- Captive portals frequently break screen readers or keyboard flows—document as real exclusion risk.  
- Fixture Route B required so learners without personal hotspots can complete evidence.  
- Provide text-first path diagrams; avoid motion-only explanations of packet flow.  
- Timeouts and auto-refresh can disorient—encourage pausing captures.

---

## Digital-equity implications

- Assuming always-on unlimited home broadband excludes many readers.  
- Café/library Wi-Fi and metered cellular are first-class conditions in Experience C—not edge cases.  
- “Just use cellular” can impose cost; treat as constrained option.  
- Edge/cloud features that need continuous sync may fail offline—teach local drafts as equity-relevant design.  
- Do not require Device Quartet hardware; commodity devices only.

---

## Potential exclusion from hardware/software/network assumptions

| Assumption | Exclusion risk | Mitigation in CE-4 |
|---|---|---|
| Personal smartphone hotspot | Cost/policy | Fixture route |
| Admin rights / packet capture tools | School-locked devices | Browser UI + fixtures |
| Uncensored Internet path | Filtered networks | Local demo pages + fixtures |
| High throughput for video examples | Low-bandwidth learners | Prefer small sync actions |

---

## Safety boundaries

- No climbing for “better signal” stunts; no illegal antenna operation.  
- No social-engineering classmates’ credentials for “labs.”  
- Physical safety: awareness of distraction while walking-and-testing radios.

---

## Ethical framing

Connectivity failures are often **system and policy** issues, not learner moral failures. Teaching must avoid shaming people on constrained networks. Distinguishing access technologies prevents false blame (“your Wi-Fi is stupid”) when the failure is DNS, cloud placement, or captive policy.
