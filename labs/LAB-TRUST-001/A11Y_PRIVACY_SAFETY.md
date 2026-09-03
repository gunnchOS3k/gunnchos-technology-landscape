# Accessibility, privacy, and safety — LAB-TRUST-001

**Lab:** LAB-TRUST-001  
**Chapter:** CE-5  
**Statuses:** IMPLEMENTED_DIGITAL | FIXTURE_VALIDATED | PHYSICAL_PENDING | EXTERNAL_DEPENDENCY

## Accessibility

| Need | Lab provision |
|---|---|
| No GPU / no local model | `fixtures/route_l_transcript.md` labeled illustrative |
| No network | Paper or Markdown comparison using Route C fixture |
| Low vision | Semantic HTML table + Markdown; status text, not color alone |
| Motor / switch | Keyboard-operable worksheet; no drag-only UI |
| Cognitive load | Explorer table capped at three observation rows |
| Screen readers | `aria-live` status regions; labeled form fields on consent card |
| Seizure risk | No flashing “thinking” animations |

Automated checkers do **not** certify WCAG conformance.

## Privacy

Safe fixtures only. Forbidden in learner captures and in shipped fixtures:

- real secrets, passwords, tokens, API keys
- private messages or email bodies
- precise personal location
- health records, government IDs, financial account numbers
- confidential employer documents

Data lifecycle stages to name on the consent card: **collect → use → retain → share → delete/redact**.

## Safety & ethics envelope

- Security content = concepts + UX symptoms only.
- No exploit steps, jailbreak catalogs, or unauthorized scanning.
- Align with responsible-use language: consent, AI disclosure, observation-before-inference.
- Do not anthropomorphize the simulator as a moral agent.

## Equity

- Live cloud APIs must not gate Explorer completion (`SC-CE5-E`).
- Fixtures keep the lab completable without paid credits or specialized hardware.
- Device Quartet on-device AI remains `PHYSICAL_PENDING` foreshadowing only.

## Gate posture

`GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`  
This package does not claim Gate 3 PASS and does not modify CH02-REVIEW-R1.
