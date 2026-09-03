# CE-1 Lab Plan — LAB-SYS-001

**Provisional lab ID:** `LAB-SYS-001`  
**Title:** Name the System Behind a Familiar “Open”  
**Chapter:** CE-1 / CH01  
**Status:** preproduction plan (not a runnable manuscript-complete lab yet)  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Observable question

> When I open something I already use, what becomes visible first, what becomes usable later, and which hidden parts might still be working?

## Why this lab (vs LAB-TAP-001)

Chapter 2’s `LAB-TAP-001` traces and times a **tap-to-response** path. CE-1 needs a **system-lens** lab: readiness, layers, dependencies, and failure domains—**without** duplicating the one-tap sequence.

## Required devices / software

| Route | Requirements |
|---|---|
| Lowest friction | Any phone, tablet, or laptop the learner already owns + paper/notes or a text editor |
| Optional operator | Browser with basic developer tools **or** OS battery/network status panes |
| Explicit non-requirement | No Device Quartet hardware; no proprietary gunnchOS EVT; no root/jailbreak |

## Pathway depth

### Explorer — observe / identify

1. Choose one familiar open action (messages, documents, maps, school portal).  
2. Watch once without touching developer tools.  
3. Write two timestamps with an ordinary clock: **chrome visible** and **content usable** (or “failed”).  
4. List ≥3 visible cues and ≥3 guessed hidden parts.

### Operator — inspect / compare

1. Repeat the open once **online** and once with **airplane mode / offline** (or Wi-Fi off), if safe for the chosen app.  
2. Record observation table: condition, chrome-visible, content-usable, notes.  
3. Assign a **failure domain** guess for any failure; mark it as inference.  
4. Optional: capture a connectivity icon state as a separate observation from usability.

### Builder — modify / create

1. Fill the ecosystem-map template (layers + optional remote branch).  
2. Modify the readiness checklist for the chosen experience.  
3. Document one tradeoff (example: more detailed notes vs avoiding personal content).

### Engineer — measure / diagnose

1. Produce a diagnosis plan separating observation / interpretation / causal claim.  
2. State what additional evidence would be required before blaming network vs app vs device storage.  
3. Optional: use browser Performance/Network panels **only** on a non-sensitive page; scrub secrets.

### Researcher — hypothesis / controlled comparison

1. Hypothesis example: “For app X, airplane mode increases content-usable time or causes failure while chrome still appears.”  
2. Define N small runs, environment notes, and limits (not a publication benchmark).  
3. Report variability qualitatively; do not invent instrument precision.

### Educator — facilitate / adapt

1. Run a 10–15 minute misconception probe: screen-as-system vs screen-as-surface.  
2. Offer the offline/fixture fallback below for classrooms without reliable networks.

## Lowest-friction route

Paper + everyday device. No install required.

## Offline / fixture fallback

If the learner cannot safely use a personal app:

1. Use a **public static webpage** or the future local fixture `labs/LAB-SYS-001/fixtures/readiness_demo.html` (to be added in implementation wave).  
2. Or use a **written scenario card** describing chrome-before-content and fill the observation sheet from the scenario (Explorer/Educator only).  
3. Scenario cards must be labeled **fixture / illustrative**, not measured device evidence.

## Expected evidence artifact

Minimum portfolio packet:

- observation table (chrome vs usable; online vs offline if attempted),  
- labeled ecosystem map,  
- observation vs inference paragraph,  
- scrubbed notes (no passwords, messages bodies, personal identifiers).

Proposed path (implementation later): `labs/LAB-SYS-001/portfolio/`.

## Observation vs inference boundary

| Allowed as observation | Inference until more evidence |
|---|---|
| Chrome appeared at time T1 | “Network is bad” |
| Content usable/failed at T2 | “Storage is dying” |
| Airplane mode was on/off | “DNS failed” |
| Icon showed connected | “Server is down” |

## Privacy / safety boundary

- Do not capture passwords, tokens, private chats, photos of ID documents, or classmate PII.  
- Prefer school/public demo pages when in shared spaces.  
- No packet capture of others’ traffic.  
- Stop if the exercise would require disabling safety features needed for the learner’s context.

## Accessibility considerations

- Accept keyboard/switch/voice paths as first-class “open” actions.  
- Allow audio description of on-screen changes instead of screenshots.  
- Provide large-print observation sheet.  
- Do not require color vision to complete the lab.  
- Align readiness messaging guidance with WCAG-oriented “busy/ready” communication (see SECURITY_EQUITY_ACCESSIBILITY.md).

## Reproducibility strategy

- Record device class (phone/laptop), OS family if known, online/offline condition, and approximate time of day.  
- One run ≠ benchmark.  
- Fixture route must be preferred when personal apps cannot be shared.

## Portfolio artifact produced

- `ecosystem_map` (diagram or structured text)  
- `readiness_observation_table`  
- `teach_back_paragraph` (optional Educator/Explorer)

## Implementation deferral

Runnable lab code/fixtures are **out of scope for this preproduction package**. This file is the evidence-first plan for the integrator and later implementation wave.
