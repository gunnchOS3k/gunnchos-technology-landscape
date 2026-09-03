# CE-5 Source Register (chapter-local)

**Chapter:** CE-5  
**Accepted-main (publication repo):** `166e9544bc6e2aee344bc962ace76d49ee3e04e4`  
**Audit date:** 2026-09-02  
**Policy:** verify metadata; no invented DOI/ISBN/pages/years  

Companion BibTeX: `references.local.bib`  
Do **not** edit shared `book/references/references.bib` in this wave.

---

## A. Repository sources (accepted main)

| Source ID | Repository | Branch | HEAD SHA (audited) | Role for CE-5 | Status |
|---|---|---|---|---|---|
| SRC-WAIKE | `gunnchOS3k/waike-research-ops` | `main` | `e97e74fc9bfb44b1cdc26b272dc4848264f15fe0` | AI_ML_EDGE, CYBERSECURITY, COMM_PD_ETHICS labs; dual ID systems | audited |
| SRC-DEVICE-OS | `gunnchOS3k/gunnchos-device-os` | `main` | `28562a8456207540c205a1c8a6434a491b0a4771` | Consent/telemetry claim boundaries; not shipping OS | audited |
| SRC-HARDWARE | `gunnchOS3k/gunnchos-hardware-industrial-design` | `main` | `9ee0ef2f688b2c18428bfabc316b23687a02988d` | Device Quartet research form factors only | audited |

### WAIKE note

Publication-repo `evidence/source_registry.yaml` still records older WAIKE SHA `8eb2827dc58ffa391842da1bfb1ee665c25a31a7` from the Chapter 2 audit. **CE-5 preproduction audited current `main` at `e97e74f...` (PR #56 merge).** Integrator should refresh shared registry; this package does not edit it.

### Safe WAIKE paths for CE-5 adjacency

- `curriculum/catalog.yaml` — includes `ai_ml_data`, `cybersecurity`, `communication_ethics_professional_dev`
- `curriculum/digital_rc/AI_ML_EDGE/` — esp. `labs/lab_score_model`, `labs/lab_quantize_budget`, `labs/lab_rag_redact`
- `curriculum/digital_rc/CYBERSECURITY/` — esp. `labs/lab_iam_rbac`, `labs/lab_hardening_baseline`, `labs/lab_incident_playbook`
- `curriculum/digital_rc/COMM_PD_ETHICS/` — esp. `labs/lab_consent_disclosure`, `labs/lab_ai_disclosure_modes`, `labs/lab_ethics_ladder`
- Supporting: `SOFTWARE_BUILDER` `lab_authz`, `CLOUD_DEVOPS` `lab_iam_secrets`

---

## B. Standards and peer-reviewed sources (verified metadata)

| Local key | Class | Citation essentials | Verification |
|---|---|---|---|
| `nist_ai_rmf_100_1` | standard | NIST AI 100-1, AI RMF 1.0, Jan 2023, DOI `10.6028/NIST.AI.100-1` | DOI resolved HTTP 200 → nvlpubs PDF (2026-09-02) |
| `nist_sp_800_63_4` | standard | NIST SP 800-63-4 Digital Identity Guidelines, July 2025, DOI `10.6028/NIST.SP.800-63-4` | DOI resolved HTTP 200 → nvlpubs PDF; supersedes SP 800-63-3 |
| `saltzer_schroeder_1975` | peer-reviewed | Saltzer & Schroeder, Proc. IEEE 63(9):1278–1308, 1975, DOI `10.1109/PROC.1975.9939` | DOI resolved; IEEE Xplore document 1451869 |

---

## C. Textbook / general references (conservative metadata)

| Local key | Class | Notes |
|---|---|---|
| `russell_norvig_aima` | textbook | Cite by title/authors/edition only in prose prep; ISBN omitted here pending shelf verification of the exact edition used by the project |
| `goodfellow_deep_learning` | textbook | Goodfellow, Bengio, Courville, *Deep Learning*, MIT Press, 2016 — used for “parameters/inference” vocabulary, not advanced derivations |
| `solove_taxonomy_2006` | peer-reviewed | Solove, “A Taxonomy of Privacy,” *University of Pennsylvania Law Review* 154 (2006) — privacy harm vocabulary; page cites deferred until PDF page-check in production |

**Rule:** if a page number, ISBN, or edition cannot be confirmed in-hand, omit it rather than invent it.

---

## D. Explicit non-sources / non-claims

- No invented WAIKE module ID for `LAB-TRUST-001` / CE-5.
- No measured on-device vs cloud AI latency for Device Quartet SKUs.
- No claim that HTTPS alone equals end-to-end privacy or integrity of endpoints.
- No anthropomorphic “model understanding” claims.
- OWASP/Top-N lists may be discussed later as living documents; not pinned with fake retrieval dates in this package.

---

## E. Source class counts (this register)

| Class | Count |
|---|---|
| repository-implemented / repository-documented | 3 |
| standard | 2 |
| peer-reviewed | 2 |
| textbook | 2 |
| **Total entries** | **9** |

## Project evidence closure (2026-09-03)

See `evidence/PROJECT_EVIDENCE_CLOSURE_B.md` for accepted-main SHA citations resolving prior `PROJECT_EVIDENCE_NEEDED` claims in this package.
