# CE-3 Security, Equity, and Accessibility Plan

**Module:** CE-3  
**Status:** `preproduction`  
**Rule:** These topics enter the technical story naturally—not as a final-page disclaimer.

---

## Where they enter the twelve-section anatomy

| Section | SEA entry |
|---|---|
| The moment | Local lag can push users toward unsafe “optimizer” downloads—name the risk early. |
| Follow the signal | Process isolation and privilege boundaries appear when explaining OS abstractions. |
| Component cards | Storage card includes confidentiality of files at rest (concept-level). |
| Stability contract | Accessibility of “responsive enough” is part of usable experience. |
| Try it / Build it | Privacy-preserving screenshots; no personal content in portfolio. |
| Secure and include it | Dedicated synthesis of the points below. |
| Career lens | Roles that own isolation, secure storage, inclusive performance. |

---

## Security boundaries

- **Process isolation intent:** OS abstractions exist partly so one app should not freely read another’s memory; teach the *purpose* without claiming every consumer OS is perfectly enforced.
- **Privilege:** Monitors and labs must not require disabling security tools, rooting/jailbreaking, or installing untrusted kernel modules.
- **Supply-chain hygiene:** Warn that “PC cleaner” tools marketed for RAM/CPU symptoms are a common social-engineering path.
- **Integrity of saves:** Durability failures can be safety issues for important documents; do not overclaim cryptographic storage.

## Privacy concerns

- Monitor screenshots can leak filenames, account names, thumbnails.
- Portfolio artifacts should redact personal paths and document text.
- Do not require cloud sync of lab evidence.
- Device-os telemetry remains opt-in / research-prototype in upstream docs—do not imply CE-3 lab needs it.

## Accessibility concerns

- Lag itself is an accessibility failure mode (motor, cognitive, vestibular load from stutter).
- Lab UI alternatives: keyboard access, text equivalents for graphs, fixture routes.
- Avoid color-only encoding in figures and monitor callouts.
- Provide plain-language pathway materials; engineer depth is optional, not gated behind unexplained jargon.

## Digital-equity implications

- Not every learner has a multi-core laptop with lots of RAM; teaching must not shame low-end devices.
- Fixture/offline routes exist so learners without admin rights or high-end hardware can still complete Explorer/Operator goals.
- “Just buy more RAM” is not the default moral of the chapter; diagnosis and workload control come first.
- Device Quartet form factors are **learning benchmarks**, not purchase requirements.

## Potential exclusion from assumptions

| Assumption | Exclusion risk | Mitigation |
|---|---|---|
| Desktop Task Manager available | Chromebooks/phones/shared school images | Fixture screenshots + phone/tablet settings pages where present |
| Can install `htop` | Locked-down machines | Use built-in monitors only |
| Sustained stress tests OK | Shared/lab devices, thermal safety | Mild loads; stop on warnings |
| English-only monitor UI | Multilingual classrooms | Label concepts, not only UI strings |

## Safety boundaries

- No intentional overheating.
- No removal of battery/thermal protections.
- No electrical hardware probing in CE-3 Concept Edition lab.
- Stop rules must appear in LAB-CMS-001 student sheet.

## Ethical framing

- Performance advice should not push surveillance of other users’ processes beyond what a learner already administers on their own device.
- Classroom facilitators should not collect screenshots that identify minors’ personal files.
- Be honest about uncertainty: a high CPU number is not moral failure by the user.

## Non-goals

- Full cybersecurity chapter (CE-5 / CH23).
- Full privacy/identity deep dive (CE-5 / CH24).
- WCAG certification claims for gunnchOS/WAIKE (unsupported per evidence audit).
