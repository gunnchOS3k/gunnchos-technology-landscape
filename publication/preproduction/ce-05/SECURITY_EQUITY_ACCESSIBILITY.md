# CE-5 — Secure, Equitable, and Accessible (section 9 prep)

**Chapter:** CE-5 — AI, Security, Privacy and Trust  
**Status:** preproduction guidance for eventual “Secure and include it” section  
**Constraint:** Security must stay attached to user experience—not a detached scare-list.

---

## Security (UX-linked)

| User-visible moment | Systems topic | Teaching move | Out of scope |
|---|---|---|---|
| Permission dialog | Least privilege, psychological acceptability | Ask what capability is requested and why | Exploit development |
| “Verify it’s you” | Authentication assurance | Separate identity claim from proof | Credential stuffing how-tos |
| Feature blocked | Authorization | Role/attribute mismatch story | Privilege-escalation recipes |
| Strange login email | Session/account recovery UX | Phishing as experience failure | Live social-engineering drills against third parties |
| Assistant follows a hidden instruction in a pasted doc | Prompt/document attack surface | Show boundary: untrusted text enters model context | Jailbreak catalogs as entertainment |
| App update badge | Supply chain / model update trust | Who signed what you run | Binary reverse engineering |

Reference principles: Saltzer & Schroeder (least privilege, fail-safe defaults, psychological acceptability)—see `references.local.bib`.

---

## Privacy

Teach lifecycle stages with decision owners:

1. **Collect** — what enters the prompt/telemetry  
2. **Use** — inference, ranking, support  
3. **Retain** — history, backups, fine-tune queues  
4. **Share** — vendors, reviewers, public demos  
5. **Delete/redact** — user request vs residual copies  

Consent card minimum fields (aligned with WAIKE `lab_consent_disclosure` adjacency): audience, purpose, data classes, retention, opt-out, AI disclosure.

Solove-style privacy vocabulary may label harms carefully; do not invent page cites.

---

## Equity

- **Private compute gap:** local models and GPUs are unevenly available → fixtures and recorded benchmarks required for fair completion.  
- **Language & dialect:** generative systems may under-serve some speakers; treat as quality/equity issue, not user failure.  
- **Verification exclusion:** SMS/CAPTCHA/video selfie may exclude people—pair with accessible alternatives discussion.  
- **Labor & data:** acknowledge that datasets and moderation involve human work; avoid “magic model” myths.  
- **Cost:** cloud API fees must not gate the Explorer path.

---

## Accessibility

Follow `publication/ACCESSIBILITY_REQUIREMENTS.md`:

- Figures: alt text + text equivalent + reading order; color never sole encoding  
- Auth flows: keyboard operable; screen-reader names for verify steps  
- Labs: no-device and low-bandwidth routes  
- Generative UI: do not rely on color-only confidence meters; provide text hedges  
- Avoid seizure-risk flashing in “AI thinking” animations  

Automated checkers do **not** certify WCAG conformance.

---

## Ethics & responsible use

- Disclose AI assistance where learners/professionals present work (`lab_ai_disclosure_modes` adjacency).  
- Prefer observation-before-inference ethics ladder (`lab_ethics_ladder` adjacency).  
- Do not anthropomorphize models as moral agents; humans remain accountable for deployment and reliance.  
- Frame trustworthy **systems practices** via NIST AI RMF vocabulary without declaring AI itself good/bad.

---

## Educator safety notes

- Ban real credential harvesting and unauthorized scanning.  
- Use synthetic/toy parsers only if ever demonstrating detection concepts (`lab_safe_vuln_detect` is WAIKE-adjacent—do not import exploit kits).  
- Trauma-aware: account takeover and surveillance examples should stay proportionate and optional.
