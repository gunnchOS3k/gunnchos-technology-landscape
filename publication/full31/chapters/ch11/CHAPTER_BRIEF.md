# CH11 Chapter Brief — Firmware, Boot, and Trust

**Chapter ID:** `CH11` (`ch11`)  
**Part:** III — Make hardware useful  
**Package status:** `preproduction` (concept packet; **no** canonical manuscript prose)  
**Accepted-main base:** `0e694176652d4729c7f2b71df08b871a863afb8c`  
**Gate note:** `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`. This package does not claim Gate 3 PASS.  
**Do not alter:** `publication/gates/gate-3/` or `CH02-REVIEW-R1`.

---

## Canonical title

Firmware, Boot, and Trust

## Primary reader promise

After this chapter, a reader can explain how a device becomes a trustworthy-enough computer—from power-on through firmware and boot into an OS—and can separate secure-boot intent from marketing claims without inventing measured attestation results.

## Experience-first opening moment (section intent)

**Canonical anchor:** You press the power button (or wake a phone). Lights/logo appear, then a lock screen or desktop—or a recovery screen, endless logo, or unverified software warning. From the seat it feels like booting. Underneath, firmware initializes hardware, verifies (or fails to verify) a chain of trust, and hands control to a bootloader/OS before any app you recognize exists.

## Part emphasis

Firmware and boot as the first software abstractions that make raw silicon useful—and as early trust boundaries.

## Teaching model

> moment → notice → ecosystem → signal → components → Stability Contract → Try/Build → secure/include → career → check → glossary

Central arc: **Human experience → system → component → code → network → society**

## Measurable outcomes (Explorer → Researcher)

| Pathway | After this chapter the reader can… |
|---|---|
| Explorer | Name firmware vs OS vs app; describe boot as a handoff; teach-back why lock screen is not secure boot. |
| Operator | Recognize update/recovery banners; capture observation-only notes of boot failure symptoms. |
| Builder | Draw a labeled boot-chain diagram for one owned device class (phone/laptop) without claiming measured timings. |
| Engineer | Separate secure-boot policy from attestation evidence; list what evidence would be needed for a trust claim. |
| Researcher | Propose a hypothesis about update failure modes with uncertainty bounds; PHYSICAL_PENDING for Quartet. |

## Stability Contract (chapter lens)

Definition: a user experience exists only while multiple hidden technical conditions remain within acceptable bounds.

Chapter-focused concurrent conditions (qualitative; no invented numeric budgets):

- Firmware completes enough init for storage/display/input paths needed by the experience
- Boot chain reaches an intended OS or honest recovery UI (not silent brick from learner's view)
- Trust policy matches learner expectation (or failure is visible, not silent)
- Update state does not leave device mid-brick without recovery affordance
- Accessibility: boot/recovery messages have readable/alt paths where platform allows

## Secure / include / equity (integrated)

No exploit, unlock, or bypass guidance. Emphasize update authenticity and least privilege. Equity: recovery literacy without assuming spare devices. A11y: text alternatives for logo-only failure states where possible.

## Career lens (intent)

Roles/layers to surface (publication `careers/role_registry.yaml` where IDs exist; otherwise descriptive): ROLE-FIRMWARE, ROLE-EMBEDDED, ROLE-KERNEL, ROLE-DRIVER, Security engineer (forward CH23).  
No employment guarantees.

## CE / lab inheritance (prefer link over duplication)

### CE preproduction
- `publication/preproduction/ce-05/` — Trust/identity/privacy themes (adjacent; CE-5 owns AI×trust synthesis)
- `publication/preproduction/ce-03/` — Inside-device context for what firmware hands to the OS
- `publication/preproduction/ce-01/` — System lens: visible surface vs hidden cooperating parts

### Labs (real IDs only)
- **LAB-TRUST-001**: CE-5 / labs worktree agent-d — adjacency only for trust/consent literacy; Ch11 does not claim LAB-TRUST-001 as its chapter lab. Forward link to CH23 for chip-to-cloud security depth.
- **LAB-CMS-001**: CE-3 — optional Operator path for post-boot local health after a failed/slow boot narrative (do not duplicate CMS as Ch11 core).

## Explicit non-goals

- Final canonical prose for `CH11`.
- Fabricated citations, measurements, or Gate 3 reader evidence.
- Invented WAIKE course/lab IDs.
- Collapsing Wi-Fi / cellular / Internet / cloud into synonyms (especially Part IV).
- Device Quartet as shipping products; physical claims stay `PHYSICAL_PENDING`.

## Twelve-section anatomy (intent only — no prose)

1. The moment  
2. What you notice  
3. Exploded ecosystem  
4. Follow the signal  
5. Component cards  
6. Stability contract  
7. Try it  
8. Build it  
9. Secure and include it  
10. Career lens  
11. Check understanding  
12. Glossary links  

## Editorial status language

Allowed now: `preproduction` / `scaffold`.  
Not allowed: Gate 3 PASS, `PUBLICATION_READY` prose claims.
