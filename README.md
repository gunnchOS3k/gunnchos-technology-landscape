# The Technology Landscape

**Author:** Edmund Gunn, Jr.  
**Series:** A gunnchOS3k + WAIKE learning system  
**Subtitle:** How Computers, Networks, AI, and Devices Create the Experiences We Depend On

## What is this?

A synchronized publication system for an illustrated technology field guide, textbook, lab manual, systems-thinking guide, career map, and bridge into deeper engineering and research.

It is not a generic “learn computers” book. Readers begin with experiences they already understand and trace those experiences through the systems that make them possible.

## Who is it for?

Learners and educators across six pathways:

- **Explorer** — little or no technical background
- **Operator** — regular device/software user
- **Builder** — student, maker, career changer
- **Engineer** — undergraduate learner or practitioner
- **Researcher** — graduate learner or investigator
- **Educator** — teacher, mentor, tutor, parent, or community guide

## What will I understand?

How familiar experiences—taps, calls, builds, AI answers, wearable alerts, weak-signal connections—map through:

> **Human experience → system → component → code → network → society**

## What makes it different?

- Experience-first teaching with authentic technology (not toy substitutes)
- Device Quartet as recurring research/learning form factors
- WAIKE-aligned labs that produce portfolio evidence
- Stability Contract: connected is not the same as usable
- Evidence integrity: no fabricated capabilities or benchmarks

## How do I read it?

1. Start with the Concept Edition scaffolds under `concept-edition/`
2. Read the canonical prototype: [`book/chapters/ch02/chapter.md`](book/chapters/ch02/chapter.md)
3. Use the glossary as a concept network: `glossary/glossary.yaml`
4. Follow figure accessibility sidecars in `figures/accessibility/`

Full-book architecture: 31 chapters in six parts (`BOOK_ARCHITECTURE.md`). Wave 1 does **not** manufacture all 31 chapters.

## How do I run the labs?

```bash
make setup
make validate
make test
make preview
```

Baseline lab (no proprietary hardware):

- Open `labs/LAB-TAP-001/browser/index.html`
- Or run `python3 labs/LAB-TAP-001/local_app/tap_timer.py`

## Device Quartet

Research/learning form factors (not mascots; not claimed as finished commercial products on accepted main):

1. Student 14.5-inch — sustained desk compute
2. Handheld Hybrid — mobile/docked compute
3. DS-XL Coder — learn-to-build
4. Edge IO Wearables — embodied/sensing compute

## Status (truthful)

**Highest legitimately claimed publication posture for this branch:**  
`GATE_2_PASS — GATE_3_IN_PROGRESS`

- Gate 0–1 artifacts: present
- Gate 2 visual prototype: present with accessibility metadata
- Gate 3 chapter prototype: substantial draft + lab + figures; human editorial/reader acceptance still required
- Gates 4–7: not claimed

See `publication/gates/` and `evidence/ACCEPTED_MAIN_SOURCE_AUDIT.md`.

## License

Publication content defaults to **CC BY 4.0**. Upstream audited gunnchOS/WAIKE sources are MIT-licensed; do not copy NDA vendor collateral.
