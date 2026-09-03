# CE-1 Stability Contract (preview)

**Chapter:** CE-1 / CH01  
**Anchor experience:** Chrome visible before content usable  
**Status:** qualitative preproduction contract — **no invented numeric budgets**  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Contract statement (pedagogical)

A person experiences a **usable open** only while multiple hidden conditions remain within acceptable bounds.

The interface can look alive (chrome, skeleton, spinner) **after** the human-usable result has already failed—or **before** the result is ready.

## Hidden technical conditions (qualitative)

For the anchor experience, conditions typically include:

1. **Input path available** — unlock/open action can be issued (touch, keyboard, switch, voice).  
2. **Application / runtime schedulable** — the local program can run soon enough to show chrome and continue work.  
3. **State restore / session validity** — remembered session or local state is usable, or a failure is communicated.  
4. **Storage readable** for needed local data (when the path is local).  
5. **Optional network/service path** healthy end-to-end **when** the experience needs remote content (association ≠ DNS ≠ route ≠ auth ≠ API).  
6. **Output path** can present updates (display/audio) the person can perceive.  
7. **Power/thermal headroom** sufficient that the device does not silently defer needed work beyond human patience (qualitative; no fabricated temperature thresholds).

## Failure domains

| Domain | Example human symptom | Still looks “fine”? |
|---|---|---|
| UI / presentation | Spinner forever; empty skeleton | Often yes |
| Local app / runtime | Crash after chrome; frozen chrome | Mixed |
| OS / resources | Extreme lag opening anything | Sometimes |
| Storage | Missing offline file; corrupt cache | Chrome may still show |
| Network / service | Tiles never fill while bars look healthy | Often yes |
| Identity / session | Endless login redirect | Chrome may show |
| Human perception / a11y | Ready state not announced | Visual chrome may exist |

## Dependencies

- Local dependencies are **not optional** for on-device opens.  
- Network/service dependencies are **optional branches**—teach the word *optional* explicitly.  
- A green connectivity icon is a **dependency signal for the link**, not a certificate for the whole experience.

## Locally observable symptoms

- Chrome/skeleton appears before content.  
- Stale content appears while refresh fails.  
- Offline mode: local item works; remote item fails.  
- “Connected” icon with unusable target service (Experience C).

## Measurements that would support diagnosis (future / light)

- Learner wall-clock chrome-visible vs content-usable (LAB-SYS-001).  
- Online vs offline comparison of the same open.  
- Optional browser network waterfalls on non-sensitive pages.  
- Optional OS battery/network status panes as **context**, not root-cause proof.

## Measurements we cannot yet obtain (honest limits)

- Touch-to-photon laboratory timings on Device Quartet hardware (PHYSICAL_PENDING).  
- Validated EVT power/thermal envelopes for research form factors.  
- Publication-grade benchmark distributions claiming universal app-launch laws.  
- Packet-level proof of a remote outage without appropriate tooling and consent.

## Human consequence

When the contract breaks, people lose time, trust, and sometimes access to school/work/care tasks. Mis-naming the failure domain (“the phone is broken” vs “the service is unreachable”) leads to wrong fixes and unfair blame—especially in shared or low-bandwidth environments.

## Link forward

CE-6 deepens this preview into the formal Stability Contract + capstone. CE-1 only needs readers to **notice concurrent conditions** and refuse false certainty.
