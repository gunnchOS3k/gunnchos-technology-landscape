#!/usr/bin/env python3
"""LAB-SYS-001 local route: large-print structured observation sheet.

Not a tap timer (see LAB-TAP-001). Prints a readiness sheet for paper or
terminal use while observing chrome-visible vs content-usable.
"""
from __future__ import annotations

SHEET = """
LAB-SYS-001 — Local observation sheet (large-print / structured text)
======================================================================
Gate note: GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING
This sheet is for systems readiness observation, NOT tap-to-response timing.

PREDICTION (before open)
  Will chrome or content become ready first? ____________________________

ENVIRONMENT
  Device class (phone / tablet / laptop / other): _______________________
  OS family (if known): _________________________________________________
  Experience chosen (or FIXTURE): _______________________________________
  Condition (online / offline / airplane / fixture): ____________________
  Assistive path used (keyboard / switch / voice / pointer): ____________

OBSERVATION TABLE (wall clock OK)
  Condition | Chrome visible (time) | Content usable/failed (time) | Notes
  ----------|-----------------------|------------------------------|------
  1         |                       |                              |
  2         |                       |                              |

VISIBLE CUES (≥3)
  1. ____________________________________________________________________
  2. ____________________________________________________________________
  3. ____________________________________________________________________

GUESSED HIDDEN PARTS (≥3) — label INFERENCE
  1. ____________________________________________________________________
  2. ____________________________________________________________________
  3. ____________________________________________________________________

FAILURE DOMAIN GUESS (inference only)
  network / app / device storage / session-auth / unknown: ______________
  What extra evidence would you need? ___________________________________

PRIVACY CHECK
  [ ] No passwords, tokens, private chats, or classmate PII captured
  [ ] Notes scrubbed before portfolio save

TEACH-BACK (optional)
  Explain chrome-before-content without jargon: _________________________
"""


def main() -> None:
    print(SHEET)


if __name__ == "__main__":
    main()
