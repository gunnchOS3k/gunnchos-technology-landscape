# CE-1 Security, Equity, and Accessibility Plan

**Chapter:** CE-1 / CH01  
**Rule:** These concerns enter the technical story early—not as a final-page disclaimer.  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Where they enter the 12-section anatomy

| Concern | Natural entry |
|---|---|
| Accessibility | Sections 1–2 (who can perform “open”); Section 9; LAB pathways |
| Security / privacy | Section 7–9 (what evidence is safe to capture); failure domains including session/auth |
| Digital equity | Sections 3, 6, 9 (device/network assumptions); Device Quartet foreshadow without requiring purchase |
| Safety / ethics | Lab boundaries; observation vs inference; no surveillance framing |

## Security boundaries

- CE-1 teaches system structure, **not** offensive techniques.  
- Lab traces stay on the learner’s own device/accounts or public fixtures.  
- No capturing credentials, session tokens, private message bodies, or others’ traffic.  
- “Identity/session” is a first-class failure domain: expired login can look like a “broken app.”

## Privacy concerns

- Screenshots and logs are evidence **and** risk.  
- Prefer redaction templates in portfolio output.  
- Classroom mode should default to fixture/demo content.  
- Do not require learners to expose personal cloud drive contents.

## Accessibility concerns

- “Open” must include keyboard, switch, voice, and assistive pointer paths.  
- Readiness states (busy vs ready) should be communicable beyond color alone (WCAG-oriented guidance; cite `wcag22` in prose wave).  
- Figures need alt text, long descriptions, and reading order (see FIGURE_PLAN).  
- Labs must allow non-visual evidence (audio notes, structured text tables).

## Digital-equity implications

- Do not assume high-end phones, unlimited data, or Device Quartet hardware.  
- Offline/fixture fallback is mandatory for LAB-SYS-001.  
- “Bars look fine but service fails” is also an equity story: shared networks, captive portals, throttled plans.  
- Avoid framing low-cost devices as “lesser technology”; treat them as first-class learning instruments.

## Potential exclusion from hardware/software/network assumptions

| Assumption | Exclusion risk | Mitigation in CE-1 |
|---|---|---|
| Must own a smartphone | Learners with shared/family-only access | Laptop/library device + fixture cards |
| Must have home broadband | Rural / metered / outage contexts | Airplane-mode contrast + offline media experience |
| Must install specialty apps | Permission/age restrictions | Browser public page route |
| Must see fine UI detail | Low vision / small screens | Large-print sheets; teach-back audio |

## Safety boundaries

- No disabling security controls required for the learner’s safety context.  
- No thermal abuse testing.  
- No social-engineering scenarios against real people.

## Ethical framing

- Systems thinking includes **who is blamed** when experience fails.  
- Observation vs inference is an ethical practice, not only a scientific one.  
- Device Quartet is a **learning laboratory foreshadow**, never a purchase pressure narrative.

## Planned prose hooks (intent only)

1. Opening moment acknowledges diverse input methods.  
2. Ecosystem map includes “who is left out if we assume always-online.”  
3. Stability preview ties failed experience to human consequence.  
4. Career lens includes accessibility and support roles, not only elite engineering titles.
