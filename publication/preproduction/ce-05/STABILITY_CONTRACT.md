# CE-5 Stability Contract (prep)

**Chapter:** CE-5 — AI, Security, Privacy and Trust  
**Principle:** A user experience exists only while multiple hidden technical conditions remain within acceptable bounds.  
**Status:** preproduction contract sketch (not measured SLOs)

---

## Experience under contract

The learner can **ask**, **receive a usable answer or clear refusal**, and **continue the account session** without surprise reuse of sensitive context—or they can understand *which bound broke*.

A system may remain “technically online” while the human experience has already failed (fluent nonsense, inaccessible verify step, silent logging beyond consent).

---

## Bounds (teaching categories)

| Bound ID | Name | Within bounds means | Out of bounds (human-visible) | Typical owning roles |
|---|---|---|---|---|
| SC-CE5-Q | Answer usability | Output is actionable or clearly refused/hedged | Fluent wrong answer treated as fact | ML eng, product, educator facilitation |
| SC-CE5-U | Uncertainty honesty | Uncertainty communicated when stakes require it | Confident fabrication; unexplained refusal storms | ML eng, UX writer |
| SC-CE5-L | Path locality | User can tell local vs cloud path at a usable level | Unexpected off-device send | Privacy eng, app eng |
| SC-CE5-I | Identity continuity | Session authn matches risk of action | Mystery re-auth loops; session fixation UX | Identity eng, SRE |
| SC-CE5-Z | Authorization clarity | Allow/deny matches role expectations | Feature visible but silently blocked | App/security eng |
| SC-CE5-C | Crypto boundary | Transit/at-rest protections match disclosure | Padlock present but endpoint fully exposed without saying so | Security eng |
| SC-CE5-P | Privacy lifecycle | Retention/share/delete match consent card | Prompt history resurfaces after delete request | Privacy eng, DPO analogue |
| SC-CE5-A | Accessible trust | Auth and disclosure paths work with AT / keyboard / low bandwidth | CAPTCHA-only or vision-only verify | A11y eng, identity eng |
| SC-CE5-E | Equity of private compute | Learners without GPUs/cloud credits still complete lab via fixtures | Lab requires paid API with no fallback | Educator, TPM |

---

## Observation vs inference rule

Labs and eventual prose must separate:

- **Observation** — timestamp, on-screen text, network required Y/N, fixture vs live  
- **Interpretation** — “probably cloud latency” / “probably authz”  
- **Causal claim** — needs extra evidence (logs, traces, config)

---

## Connected vs usable (CE-5 instances)

| Technically true | Experience failed |
|---|---|
| API returns HTTP 200 | Answer is harmful/wrong and looks authoritative |
| TLS session established | Phished site; user authenticated to attacker |
| Model loaded | Output not exposed to screen reader |
| User authenticated | User not authorized; UI offers the button anyway |
| Data encrypted at rest | Plaintext prompt mirrored to human support without disclosure |

---

## Non-claims

- No numeric latency/privacy SLOs claimed for Device Quartet or gunnchOS product AI.  
- No assertion that meeting this teaching contract equals legal compliance.  
- AI is not labeled inherently inside or outside the trust bound—only **systems and practices** are.

---

## Lab linkage

`LAB-TRUST-001` evidence artifacts should mark which bounds were observed in-bounds / out-of-bounds / unknown.
