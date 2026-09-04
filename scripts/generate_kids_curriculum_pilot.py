#!/usr/bin/env python3
"""Generate Kids curriculum scope/sequence, ONE TAP pilot artifacts, builds, and checks."""
from __future__ import annotations

import hashlib
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIDS = ROOT / "kids"
PILOT = KIDS / "pilots" / "ONE_TAP"
BANDS = [
    ("KIDS-BABY", "BABY", "0–18 months"),
    ("KIDS-TODDLER", "TODDLER", "18–36 months"),
    ("KIDS-PRESCHOOL", "PRESCHOOL", "3–4 years"),
    ("KIDS-PREK", "PREK", "4–6 years"),
    ("KIDS-ELEM1", "ELEM1", "Kindergarten–Grade 2"),
    ("KIDS-ELEM2", "ELEM2", "Grades 3–5/6"),
]
STRANDS = [
    ("STRAND-ME-TECH", "Me & Technology"),
    ("STRAND-INSIDE", "Inside the Machine"),
    ("STRAND-INSTRUCTIONS", "Instructions & Code"),
    ("STRAND-MESSAGES", "Messages & Connections"),
    ("STRAND-DATA", "Data & Intelligence"),
    ("STRAND-SAFE", "Safe, Private & Fair"),
    ("STRAND-BUILD", "Build, Test & Share"),
]
PROTOTYPE_BANNER = (
    "KIDS DEVELOPMENTAL PROTOTYPE\n"
    "NOT CHILD-VALIDATED\n"
    "NOT PUBLICATION-READY"
)
WAIKE_SHA = "e97e74fc9bfb44b1cdc26b272dc4848264f15fe0"
ADULT_MAIN = "82284cd8f41d750ff508cd6ea5bad0a9534d8162"
INTEGRATION_BASE = "ce9cc419841fa0588e30d8d917b048c72f8cc2c0"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def yaml_quote(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


# --- Cadence / assessment / caregiver docs ---------------------------------


def write_support_docs() -> None:
    write(
        KIDS / "cadence" / "STORY_LEARNING_CADENCE.md",
        f"""# Story / learning cadence (Kids Edition)

**Status:** developmental prototype scaffolding  
**Labels:**
```
{PROTOTYPE_BANNER}
```

## Canonical unit cadence (shared spine)

```text
STORY → NOTICE → NAME → CONNECT → PREDICT → TRY → EXPLAIN → MAKE → SAFE + FAIR → TEACH
```

This spine adapts by age. It is a teaching rhythm, not a quiz script.

## Baby / Toddler adaptation

```text
LOOK → POINT → NAME → WAIT → RESPOND → REPEAT
```

- Follow the child's attention (serve-and-return).
- No expectation of verbal answers for babies.
- Caregiver narrates; child may look, reach, vocalize, or move away.
- Always offer an easy stop.

## Preschool / Pre-K adaptation

Keep the shared spine, shorten language, emphasize:

- first / next / last
- parts of a device
- prediction before trying
- safe / private choice moments

## Elementary adaptation

```text
OBSERVE → PREDICT → TEST → MEASURE → EXPLAIN → BUILD → SECURE → REFLECT → TEACH
```

- Separate observation from inference.
- Low-stakes checks only.
- Portfolio evidence for process, not ranking.

## ONE TAP pilot mapping

| Age band | Cadence used |
| --- | --- |
| KIDS-BABY | LOOK / POINT / NAME / WAIT / RESPOND / REPEAT |
| KIDS-TODDLER | LOOK / POINT / NAME / WAIT / RESPOND / REPEAT (+ first/next) |
| KIDS-PRESCHOOL | Shortened STORY…TEACH |
| KIDS-PREK | Full spine, simple algorithm + message path |
| KIDS-ELEM1 | Elementary OBSERVE…TEACH |
| KIDS-ELEM2 | Elementary + cross-layer measure/secure |

## Non-claims

- Cadence is not a developmental screen.
- Cadence is not child-validated in this wave.
""",
    )

    write(
        KIDS / "assessment" / "KIDS_ASSESSMENT_PHILOSOPHY.md",
        f"""# Kids assessment philosophy

**Status:** developmental prototype policy  
**Labels:**
```
{PROTOTYPE_BANNER}
```

## Principles

1. **No developmental diagnosis** from book activities.
2. **No ranking** young children against each other.
3. **Observation and play** for infant–Pre-K.
4. **Low-stakes portfolio evidence** for elementary.
5. Caregiver/educator notes describe *what was tried*, not ability labels.

## Infant – Pre-K

Preferred evidence forms:

- looking / pointing / matching
- sorting / sequencing with objects
- drawing / building
- teach-back gestures or short phrases
- caregiver notes of interest and affect
- play observation

Forbidden in this age range:

- high-stakes quizzes
- timed competitive drills
- percentile/ranking language
- screening disguised as “check understanding”

## Elementary (K–2 and Grades 3–5/6)

Allowed:

- short observation worksheets
- predict / test / explain prompts
- build-a-sequence or trace-a-path artifacts
- portfolio folders with dated tries
- peer teach-back (optional, opt-in)

Still forbidden:

- diagnostic labeling
- public leaderboards for young learners
- fabricated “child validated” claims

## Relation to adult book / WAIKE

Adult CH30/CH31 and WAIKE portfolio culture are **adjacent** inspirations for elementary portfolio honesty.  
Kids Edition does **not** invent WAIKE module IDs for early-learning assessments.
""",
    )

    write(
        KIDS / "caregivers" / "CAREGIVER_GUIDE_SYSTEM.md",
        f"""# Caregiver co-learning system

**Status:** developmental prototype  
**Labels:**
```
{PROTOTYPE_BANNER}
```

## For ages 0–5 (Baby → Pre-K)

Explicit caregiver moves:

1. Follow the child's attention.
2. Name what they notice (“You touched. It changed.”).
3. Wait for a response (look, sound, reach, or pause).
4. Point / gesture together.
5. Repeat with small variation.
6. Connect to household objects (lamp switch, remote, toy button)—safely.
7. Avoid forcing performance.
8. Use the family's home language.
9. Adapt for disability / sensory needs (alternate routes, shorter sessions).
10. Stop early if the child disengages.

## What this is not

- Not a developmental screening tool.
- Not a requirement that a child produce speech.
- Not permission to collect child data.

## For elementary

Caregiver/educator role shifts toward:

- co-observing local vs networked actions
- helping separate “I saw” from “I guess”
- protecting privacy/safety choices
- celebrating process evidence in a portfolio

## Media ethics (co-use)

- Prefer print / caregiver-led for infants and toddlers.
- Autoplay off; no infinite scroll patterns in any digital preview.
- Easy exit always visible in HTML previews.
""",
    )


# --- Scope and sequence -----------------------------------------------------


UNIT_SEEDS = {
    "STRAND-ME-TECH": {
        "BABY": ("Tap-Look Wait", "Notice change after contact", "KCON-CH02-ONE-TAP"),
        "TODDLER": ("Touch Then Change", "Input then response", "KCON-CH02-ONE-TAP"),
        "PRESCHOOL": ("Screen Is One Part", "Outside vs inside", "KCON-CH01-SYSTEM-NOT-SCREEN"),
        "PREK": ("Systems Have Parts", "Parts work together", "KCON-CH01-SYSTEM-NOT-SCREEN"),
        "ELEM1": ("Systems Not Screens", "People+parts+rules", "KCON-CH01-SYSTEM-NOT-SCREEN"),
        "ELEM2": ("Experience Maps Systems", "Visible to hidden path", "KCON-CH01-SYSTEM-NOT-SCREEN"),
    },
    "STRAND-INSIDE": {
        "BABY": ("Awake Device", "Dark to awake with adult", "KCON-CH11-BOOT-TRUST"),
        "TODDLER": ("Busy Then Ready", "Machine doing a job", "KCON-CH06-CPU-WORK"),
        "PRESCHOOL": ("Parts We Can Name", "Button, light, speaker", "KCON-CH04-DEVICE-FORMS"),
        "PREK": ("Working Space vs Keep-Box", "Now vs later memory", "KCON-CH07-MEMORY-STORAGE"),
        "ELEM1": ("Inside the Box", "CPU, memory, storage roles", "KCON-CH06-CPU-WORK"),
        "ELEM2": ("Hardware Constraints", "Power, heat, interconnect", "KCON-CH09-POWER-HEAT"),
    },
    "STRAND-INSTRUCTIONS": {
        "BABY": ("Same Action Again", "Repeat a known cause", "KCON-CH02-ONE-TAP"),
        "TODDLER": ("First Next", "Order of two steps", "KCON-CH02-ONE-TAP"),
        "PRESCHOOL": ("Steps for a Helper", "First/next/last", "KCON-CH14-APPS-UI"),
        "PREK": ("Simple Algorithm", "Ordered instructions", "KCON-CH14-APPS-UI"),
        "ELEM1": ("Hardware and Software", "Senses vs instructions", "KCON-CH12-OS-SCHEDULE"),
        "ELEM2": ("Events and Handlers", "Event loop idea", "KCON-CH14-APPS-UI"),
    },
    "STRAND-MESSAGES": {
        "BABY": ("Here to There", "Gesture across space", "KCON-CH16-PACKETS-INTERNET"),
        "TODDLER": ("Messages Move", "Send a sound/look afar", "KCON-CH16-PACKETS-INTERNET"),
        "PRESCHOOL": ("Devices Send Messages", "Local story of sending", "KCON-CH16-PACKETS-INTERNET"),
        "PREK": ("Paths and Rules", "Message follows a path", "KCON-CH16-PACKETS-INTERNET"),
        "ELEM1": ("Networks Connect", "Local vs network action", "KCON-CH16-PACKETS-INTERNET"),
        "ELEM2": ("Packets and Routes", "Represent/transmit/interpret", "KCON-CH16-PACKETS-INTERNET"),
    },
    "STRAND-DATA": {
        "BABY": ("Familiar Pattern", "Known face/sound comfort", "KCON-CH21-DATA-AI"),
        "TODDLER": ("Guess Can Be Wrong", "Pattern guess play", "KCON-CH21-DATA-AI"),
        "PRESCHOOL": ("Keep-Boxes Have Names", "Named keepsakes/files", "KCON-CH13-FILES-DATA-LIFE"),
        "PREK": ("Saved for Later", "Create/save/find", "KCON-CH13-FILES-DATA-LIFE"),
        "ELEM1": ("Data Helps Predictions", "Examples then guess", "KCON-CH21-DATA-AI"),
        "ELEM2": ("Models Need Checks", "AI can err; humans check", "KCON-CH21-DATA-AI"),
    },
    "STRAND-SAFE": {
        "BABY": ("Grown-Up Only", "Some controls are adult", "KCON-CH23-CYBERSECURITY"),
        "TODDLER": ("Ask Before New", "Stop and ask", "KCON-CH23-CYBERSECURITY"),
        "PRESCHOOL": ("Private Means Not Everyone", "Share with caregiver", "KCON-CH24-PRIVACY-ETHICS"),
        "PREK": ("Safe or Private Choice", "Choose the safer path", "KCON-CH24-PRIVACY-ETHICS"),
        "ELEM1": ("Locks and Fair Access", "Security + inclusion", "KCON-CH24-PRIVACY-ETHICS"),
        "ELEM2": ("Privacy Security Equity", "Chip-to-cloud duties", "KCON-CH25-DIGITAL-EQUITY"),
    },
    "STRAND-BUILD": {
        "BABY": ("Show What Happened", "Gesture teach-back", "KCON-CH31-CAPSTONE-TEACH"),
        "TODDLER": ("Make and Try Again", "Build a tiny try", "KCON-CH26-SOFTWARE-VCS"),
        "PRESCHOOL": ("Test Means Try and See", "Check the change", "KCON-CH27-TEST-EVIDENCE"),
        "PREK": ("Build a Sequence", "Plan → try → fix", "KCON-CH26-SOFTWARE-VCS"),
        "ELEM1": ("Evidence Folder", "Keep process proof", "KCON-CH30-CAREER-PORTFOLIO"),
        "ELEM2": ("Explain Measure Improve Teach", "EMIT mini-capstone", "KCON-CH31-CAPSTONE-TEACH"),
    },
}


def write_scope_sequence() -> int:
    lines = [
        "# Kids scope and sequence — strands × age bands",
        "# Status: SCOPE_SEQUENCE draft for integrator; standards mostly NOT_YET_MAPPED",
        "# NOT CHILD-VALIDATED · NOT PUBLICATION-READY · NOT GLOBALLY_ALIGNED",
        "",
        "meta:",
        "  document_id: KIDS_SCOPE_AND_SEQUENCE",
        '  version: "0.1.0-prototype"',
        f'  adult_main_sha: "{ADULT_MAIN}"',
        f'  integration_base_sha: "{INTEGRATION_BASE}"',
        "  spiral_ref: kids/concepts/ADULT31_TO_KIDS_SPIRAL.yaml",
        "  standards_atlas_status: NOT_YET_LANDED_USE_WIRE_IDS",
        "  child_validation: NONE",
        "  publication_ready: false",
        "  alignment_claim: CROSSWALKED_AGAINST",
        "",
        "units:",
    ]
    count = 0
    for strand_id, strand_name in STRANDS:
        for band_id, short, ages in BANDS:
            title, goal, concept = UNIT_SEEDS[strand_id][short]
            count += 1
            uid = f"UNIT-{short}-{strand_id.split('-',1)[1]}-01"
            # humanize strand fragment
            uid = f"UNIT-{short}-{strand_id.replace('STRAND-','')}-01"
            lines += [
                f"  - unit_id: {uid}",
                f"    age_band: {band_id}",
                f"    age_guide: {yaml_quote(ages)}",
                f"    title: {yaml_quote(title)}",
                f"    kids_strand: {strand_id}",
                f"    strand_name: {yaml_quote(strand_name)}",
                f"    technology_concepts: [{concept}]",
                f"    developmental_precursors: {yaml_quote(goal)}",
                f"    learning_goal: {yaml_quote(goal)}",
                "    global_standard_mappings:",
                "      - mapping_id: "
                + f"MAP-{uid}",
                "        status: NOT_YET_MAPPED",
                f"        wire_id: STD-WIRE-{uid}",
                "        note: "
                + yaml_quote(
                    "Sister standards atlas not landed; integrator wires official IDs later."
                ),
                f"    story_hook: {yaml_quote('A familiar household moment opens the unit.')}",
                "    vocabulary: []  # age-appropriate terms filled in band manuscripts",
                "    visuals:",
                f"      - style_neutral_prototype_for: {concept}",
                "    caregiver_or_teacher_role: "
                + yaml_quote(
                    "Follow attention; name; wait; never force performance."
                    if short in {"BABY", "TODDLER", "PRESCHOOL", "PREK"}
                    else "Coach observe/predict/test; protect privacy; portfolio not ranking."
                ),
                "    try_it: "
                + yaml_quote("Short, safe, stoppable activity matched to band."),
                "    make_it: "
                + yaml_quote("Build, draw, or sequence a tiny artifact."),
                "    safety_and_fairness: "
                + yaml_quote("Adult mediation; no child data collection; inclusive routes."),
                "    misconceptions: "
                + yaml_quote("See spiral entry for concept-level misconceptions."),
                "    assessment_or_observation: "
                + yaml_quote(
                    "Observation/play notes only."
                    if short in {"BABY", "TODDLER", "PRESCHOOL", "PREK"}
                    else "Low-stakes portfolio artifact; no ranking."
                ),
                "    extension: "
                + yaml_quote("Optional household connection if child remains interested."),
                "    adult_book_connections:",
                f"      - {concept.replace('KCON-','').split('-')[0] if False else concept}",
                "",
            ]
            # fix adult_book_connections to chapter
            # rewrite last connection properly after loop — patch via replace below
    text = "\n".join(lines)
    # Fix adult_book_connections lines to use concept ids already present
    text = text.replace(
        "    adult_book_connections:\n      - False",
        "    adult_book_connections:\n      - SEE_technology_concepts",
    )
    # cleaner fix: regenerate adult connections
    out_lines = []
    pending_concept = None
    for line in text.splitlines():
        if line.strip().startswith("technology_concepts:"):
            pending_concept = line.split("[", 1)[1].rstrip("]")
        if line.strip().startswith("- SEE_technology_concepts") or (
            line.strip().startswith("- KCON-") and "adult_book" in "\n".join(out_lines[-3:])
        ):
            out_lines.append(f"      - {pending_concept}")
            continue
        if line.strip() == "- SEE_technology_concepts":
            out_lines.append(f"      - {pending_concept}")
            continue
        out_lines.append(line)
    # Actually the generator put concept in technology_concepts already; fix the broken adult_book_connections
    fixed = []
    concept = None
    for line in "\n".join(lines).splitlines():
        if "technology_concepts:" in line:
            concept = line.split("[")[1].split("]")[0]
        if line.strip().startswith("- ") and "adult_book_connections" in "\n".join(fixed[-2:]):
            fixed.append(f"      - {concept}")
            continue
        if line.strip().startswith("- KCON-") and fixed and "adult_book_connections:" in fixed[-1]:
            fixed.append(f"      - {concept}")
            continue
        fixed.append(line)
    # Simpler: rewrite file cleanly
    lines = [
        "# Kids scope and sequence — strands × age bands",
        "# Status: SCOPE_SEQUENCE draft for integrator; standards mostly NOT_YET_MAPPED",
        "# NOT CHILD-VALIDATED · NOT PUBLICATION-READY · NOT GLOBALLY_ALIGNED",
        "",
        "meta:",
        "  document_id: KIDS_SCOPE_AND_SEQUENCE",
        '  version: "0.1.0-prototype"',
        f'  adult_main_sha: "{ADULT_MAIN}"',
        f'  integration_base_sha: "{INTEGRATION_BASE}"',
        "  spiral_ref: kids/concepts/ADULT31_TO_KIDS_SPIRAL.yaml",
        "  standards_atlas_status: NOT_YET_LANDED_USE_WIRE_IDS",
        "  child_validation: NONE",
        "  publication_ready: false",
        "  alignment_claim: CROSSWALKED_AGAINST",
        "  unit_count_target_note: "
        + yaml_quote("One coherent unit per strand per age band (42). Not optimized for count."),
        "",
        "units:",
    ]
    count = 0
    for strand_id, strand_name in STRANDS:
        for band_id, short, ages in BANDS:
            title, goal, concept = UNIT_SEEDS[strand_id][short]
            count += 1
            uid = f"UNIT-{short}-{strand_id.replace('STRAND-','')}-01"
            lines += [
                f"  - unit_id: {uid}",
                f"    age_band: {band_id}",
                f"    age_guide: {yaml_quote(ages)}",
                f"    title: {yaml_quote(title)}",
                f"    kids_strand: {strand_id}",
                f"    strand_name: {yaml_quote(strand_name)}",
                f"    technology_concepts:",
                f"      - {concept}",
                f"    developmental_precursors: {yaml_quote(goal)}",
                f"    learning_goal: {yaml_quote(goal)}",
                "    global_standard_mappings:",
                f"      - mapping_id: MAP-{uid}",
                "        status: NOT_YET_MAPPED",
                f"        wire_id: STD-WIRE-{uid}",
                "        note: "
                + yaml_quote(
                    "Sister standards atlas not landed; integrator maps official records later."
                ),
                "    story_hook: "
                + yaml_quote("Open from a familiar household cause→effect moment."),
                "    vocabulary: []",
                "    visuals:",
                "      - production_style: style_neutral_prototype",
                f"        concept_id: {concept}",
                "    caregiver_or_teacher_role: "
                + yaml_quote(
                    "Follow attention; name; wait; never force performance."
                    if short in {"BABY", "TODDLER", "PRESCHOOL", "PREK"}
                    else "Coach observe/predict/test; privacy first; portfolio not ranking."
                ),
                "    try_it: "
                + yaml_quote("Short, safe, stoppable try matched to the band."),
                "    make_it: "
                + yaml_quote("Draw, build, or sequence a tiny artifact."),
                "    safety_and_fairness: "
                + yaml_quote("Adult mediation; no child data collection; inclusive routes."),
                "    misconceptions:",
                "      - see_spiral_entry",
                "    assessment_or_observation: "
                + yaml_quote(
                    "Observation/play notes only."
                    if short in {"BABY", "TODDLER", "PRESCHOOL", "PREK"}
                    else "Low-stakes portfolio artifact; no ranking/diagnosis."
                ),
                "    extension: "
                + yaml_quote("Optional household connection if interest continues."),
                "    adult_book_connections:",
                f"      - {concept}",
                "",
            ]
    write(KIDS / "curriculum" / "KIDS_SCOPE_AND_SEQUENCE.yaml", "\n".join(lines))
    return count


# --- ONE TAP pilot content --------------------------------------------------


def pilot_spreads(short: str) -> list[dict]:
    """Developmentally rewritten ONE TAP spreads (not sentence-simplified adult CH02)."""
    if short == "BABY":
        return [
            {"id": "S01", "cadence": "LOOK", "title": "Look", "words": "Look.", "caregiver": "Follow gaze. Soft voice.", "action": "Look together at a single lit control."},
            {"id": "S02", "cadence": "POINT", "title": "Hand", "words": "Hand.", "caregiver": "Point to hand, then control.", "action": "Notice hand near the surface."},
            {"id": "S03", "cadence": "NAME", "title": "Touch", "words": "Touch.", "caregiver": "Name the touch when contact happens.", "action": "Finger meets surface."},
            {"id": "S04", "cadence": "WAIT", "title": "Wait", "words": "Wait…", "caregiver": "Pause. Do not rush.", "action": "A short wait before change."},
            {"id": "S05", "cadence": "RESPOND", "title": "Change", "words": "Change!", "caregiver": "Celebrate the change calmly.", "action": "Light or sound changes."},
            {"id": "S06", "cadence": "REPEAT", "title": "Again", "words": "Again?", "caregiver": "Offer repeat; accept no.", "action": "Optional second touch."},
            {"id": "S07", "cadence": "NAME", "title": "Same place", "words": "Same.", "caregiver": "Same spot → same kind of change.", "action": "Repeat at same control."},
            {"id": "S08", "cadence": "LOOK", "title": "New place", "words": "New.", "caregiver": "Different control, different change.", "action": "Move attention to another control."},
            {"id": "S09", "cadence": "POINT", "title": "Point with me", "words": "Point.", "caregiver": "Invite pointing; no demand for speech.", "action": "Point to what changed."},
            {"id": "S10", "cadence": "RESPOND", "title": "All done", "words": "All done.", "caregiver": "Easy stop. Close the book/device.", "action": "Session ends positively."},
        ]
    if short == "TODDLER":
        return [
            {"id": "S01", "cadence": "LOOK", "title": "We look", "words": "We look.", "caregiver": "One focal object.", "action": "Find the button together."},
            {"id": "S02", "cadence": "NAME", "title": "Input", "words": "Touch is input.", "caregiver": "Short phrase; gesture touch.", "action": "Name input."},
            {"id": "S03", "cadence": "NAME", "title": "Output", "words": "Change is output.", "caregiver": "Point to the change.", "action": "Name output."},
            {"id": "S04", "cadence": "WAIT", "title": "First", "words": "First: touch.", "caregiver": "Hold up one finger.", "action": "Sequence start."},
            {"id": "S05", "cadence": "RESPOND", "title": "Next", "words": "Next: change.", "caregiver": "Hold up two fingers.", "action": "Sequence continue."},
            {"id": "S06", "cadence": "POINT", "title": "Find", "words": "Find the button.", "caregiver": "Child points/finds.", "action": "Match control."},
            {"id": "S07", "cadence": "TRY", "title": "Match", "words": "Match touch to change.", "caregiver": "One physical try.", "action": "Do one supervised tap."},
            {"id": "S08", "cadence": "REPEAT", "title": "Again same", "words": "Again — same.", "caregiver": "Repetition with joy.", "action": "Repeat once."},
            {"id": "S09", "cadence": "SAFE + FAIR", "title": "Ask adult", "words": "New button? Ask.", "caregiver": "Safety rule, calm tone.", "action": "Practice ask-before-new."},
            {"id": "S10", "cadence": "TEACH", "title": "Show me", "words": "Show me touch → change.", "caregiver": "Invite teach-back gesture.", "action": "Child shows caregiver."},
        ]
    if short == "PRESCHOOL":
        return [
            {"id": "S01", "cadence": "STORY", "title": "The sticky song", "words": "Maya wants the song button to work.", "caregiver": "Tell the tiny story.", "action": "Meet the problem."},
            {"id": "S02", "cadence": "NOTICE", "title": "What we notice", "words": "She presses. A light blinks. Music starts.", "caregiver": "Notice before naming tech words.", "action": "List noticed events."},
            {"id": "S03", "cadence": "NAME", "title": "Parts", "words": "Button. Light. Speaker. Those are parts.", "caregiver": "Count parts on fingers.", "action": "Name parts."},
            {"id": "S04", "cadence": "CONNECT", "title": "Inside helps", "words": "Something inside the box helps the parts talk.", "caregiver": "Screen is not the whole story.", "action": "Connect outside→inside."},
            {"id": "S05", "cadence": "PREDICT", "title": "Predict", "words": "If we press, what happens first? Next? Last?", "caregiver": "Accept any sincere guess.", "action": "Predict order."},
            {"id": "S06", "cadence": "TRY", "title": "Try the order", "words": "First press. Next blink. Last sound.", "caregiver": "Act the sequence with gestures.", "action": "Sequence practice."},
            {"id": "S07", "cadence": "EXPLAIN", "title": "Sensor idea", "words": "The button notices a press. Like a tiny sensor.", "caregiver": "Keep language concrete.", "action": "Explain sensing."},
            {"id": "S08", "cadence": "MAKE", "title": "Sort the cards", "words": "Sort: press / blink / sound.", "caregiver": "Use three cards or drawings.", "action": "Sorting/sequencing."},
            {"id": "S09", "cadence": "SAFE + FAIR", "title": "Stop anytime", "words": "If it is too loud, we stop. That is fair.", "caregiver": "Model stop.", "action": "Agency to stop."},
            {"id": "S10", "cadence": "TEACH", "title": "Teach a friend", "words": "Tell the story: press → blink → sound.", "caregiver": "Optional peer share.", "action": "Teach-back."},
        ]
    if short == "PREK":
        return [
            {"id": "S01", "cadence": "STORY", "title": "Message or local?", "words": "Jordan taps Refresh. Sometimes the phone already has the page. Sometimes it asks far away.", "caregiver": "Plant optional network idea.", "action": "Story hook."},
            {"id": "S02", "cadence": "NOTICE", "title": "Two timelines", "words": "A quick highlight can happen before new words arrive.", "caregiver": "Immediate vs later.", "action": "Notice two timings."},
            {"id": "S03", "cadence": "NAME", "title": "System and component", "words": "The phone is a system. The button is a component.", "caregiver": "Use both words once, concretely.", "action": "Name system/component."},
            {"id": "S04", "cadence": "CONNECT", "title": "Simple algorithm", "words": "1 sense press 2 choose action 3 show result.", "caregiver": "Algorithm = ordered steps.", "action": "Write/draw 3 steps."},
            {"id": "S05", "cadence": "PREDICT", "title": "Local prediction", "words": "If the page is already here, maybe no far message.", "caregiver": "Prediction, not certainty.", "action": "Predict local path."},
            {"id": "S06", "cadence": "TRY", "title": "Message path", "words": "If it needs new info, a message can travel out and back.", "caregiver": "Path drawing.", "action": "Draw message path."},
            {"id": "S07", "cadence": "SAFE + FAIR", "title": "Private choice", "words": "Do we share the screen with a stranger? No — ask a trusted adult.", "caregiver": "Safe/private choice.", "action": "Choose safe option."},
            {"id": "S08", "cadence": "MAKE", "title": "Build-a-sequence", "words": "Build cards: Input → Steps → Output (optional Message).", "caregiver": "Hands-on sequence.", "action": "Build sequence."},
            {"id": "S09", "cadence": "EXPLAIN", "title": "Explain the path", "words": "Explain which path you built and why.", "caregiver": "Listen without correcting every word.", "action": "Explain."},
            {"id": "S10", "cadence": "TEACH", "title": "Teach caregiver", "words": "Teach your caregiver the three steps.", "caregiver": "Be the learner.", "action": "Teach-back."},
        ]
    if short == "ELEM1":
        return [
            {"id": "S01", "cadence": "OBSERVE", "title": "Observe a tap", "words": "Tap a control that only changes this device. Then tap one that needs the network. Write what you saw.", "caregiver": "Supervise; no accounts.", "action": "Two observations."},
            {"id": "S02", "cadence": "NAME", "title": "Hardware / software", "words": "Hardware senses the touch. Software follows instructions about what to do next.", "caregiver": "Keep definitions short.", "action": "Name HW/SW."},
            {"id": "S03", "cadence": "NAME", "title": "Input → process → output", "words": "Input: touch report. Process: app decides. Output: pixels, sound, or motion.", "caregiver": "IPO diagram.", "action": "Fill IPO."},
            {"id": "S04", "cadence": "PREDICT", "title": "Algorithm steps", "words": "Write a 4-step algorithm for your local tap.", "caregiver": "Any clear order OK.", "action": "Write algorithm."},
            {"id": "S05", "cadence": "TEST", "title": "Local vs network", "words": "Test: which tap stayed local? Which waited on a network?", "caregiver": "Observation vs guess.", "action": "Classify taps."},
            {"id": "S06", "cadence": "EXPLAIN", "title": "Why feedback felt instant", "words": "Instant highlight can finish before remote content arrives.", "caregiver": "Two timelines.", "action": "Explain timelines."},
            {"id": "S07", "cadence": "SECURE", "title": "Safe practice", "words": "Do not install unknown apps. Ask before sharing personal info.", "caregiver": "Safety without fear.", "action": "Safety checklist."},
            {"id": "S08", "cadence": "BUILD", "title": "Worksheet", "words": "Complete the observation worksheet: what I saw / what I infer / what I still don't know.", "caregiver": "Portfolio piece.", "action": "Worksheet."},
            {"id": "S09", "cadence": "REFLECT", "title": "Misconception check", "words": "True or rethink: “Every tap goes to the internet.”", "caregiver": "Discuss kindly.", "action": "Misconception."},
            {"id": "S10", "cadence": "TEACH", "title": "Teach-back", "words": "Teach a partner the IPO path for one tap.", "caregiver": "Optional peer.", "action": "Teach-back."},
        ]
    # ELEM2
    return [
        {"id": "S01", "cadence": "OBSERVE", "title": "Cross-layer map", "words": "Map one tap across human → input hardware → OS → application → optional network → output → perception.", "caregiver": "Use pilot figure.", "action": "Annotate map."},
        {"id": "S02", "cadence": "NAME", "title": "CPU, memory, storage", "words": "Name roles: CPU runs instructions; memory holds working state; storage keeps durable data.", "caregiver": "No false GHz claims.", "action": "Role cards."},
        {"id": "S03", "cadence": "NAME", "title": "Event handling", "words": "A tap becomes an event. The app’s event loop dispatches a handler that updates state.", "caregiver": "Link to adult CH02 honestly.", "action": "Event diagram."},
        {"id": "S04", "cadence": "PREDICT", "title": "Packet possibility", "words": "Predict whether your action needs packets. What would you observe if the radio is off?", "caregiver": "Prediction first.", "action": "Predict network need."},
        {"id": "S05", "cadence": "MEASURE", "title": "Latency feel vs measure", "words": "Measure a rough wait with a stopwatch for a remote refresh. Separate felt delay from guessed cause.", "caregiver": "Classroom timer OK.", "action": "Rough measure."},
        {"id": "S06", "cadence": "EXPLAIN", "title": "Observation vs inference", "words": "Write two columns: Observation | Inference. Mark inferences as uncertain.", "caregiver": "Core systems skill.", "action": "Two-column notes."},
        {"id": "S07", "cadence": "SECURE", "title": "Security & privacy", "words": "List one security control and one privacy choice that affect a tap path (lock screen, permissions, HTTPS idea).", "caregiver": "No exploit content.", "action": "Secure+private."},
        {"id": "S08", "cadence": "BUILD", "title": "Build / test / teach", "words": "Build a paper protocol: steps, failure branch, and a teach-back script for a younger band.", "caregiver": "Portfolio artifact.", "action": "Protocol + teach script."},
        {"id": "S09", "cadence": "REFLECT", "title": "Adult CH02 bridge", "words": "What stays the same from baby LOOK→CHANGE to this cross-layer map? What vocabulary was earned later?", "caregiver": "Spiral reflection.", "action": "Spiral note."},
        {"id": "S10", "cadence": "TEACH", "title": "EMIT mini-capstone", "words": "Explain, measure, improve one step, teach someone else—without claiming child-validated science.", "caregiver": "Honesty label required.", "action": "EMIT loop."},
    ]


def svg_for_spread(band: str, spread: dict, idx: int) -> str:
    asset = f"FIG-ONE-TAP-{band}-{spread['id']}"
    title = spread["title"]
    words = spread["words"]
    # simple style-neutral prototype: large focal shape + labels; color not sole encoding
    shapes = [
        # alternating simple compositions
        f'<circle cx="200" cy="210" r="70" fill="#f4f4f4" stroke="#111" stroke-width="4"/>',
        f'<rect x="130" y="150" width="140" height="120" rx="8" fill="#f4f4f4" stroke="#111" stroke-width="4"/>',
        f'<polygon points="200,140 270,260 130,260" fill="#f4f4f4" stroke="#111" stroke-width="4"/>',
    ]
    shape = shapes[idx % 3]
    # add action glyph (finger/dot/arrow) with patterns not only color
    glyph = f'''
  <circle cx="200" cy="210" r="10" fill="#111"/>
  <line x1="200" y1="220" x2="200" y2="280" stroke="#111" stroke-width="4"/>
  <path d="M200 280 L180 300 L220 300 Z" fill="#111"/>
'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500" role="img" aria-labelledby="{asset}-title {asset}-desc" data-asset-id="{asset}">
  <title id="{asset}-title">{asset}: {title}</title>
  <desc id="{asset}-desc">Style-neutral ONE TAP prototype spread for {band}. Focal action: {spread['action']}. Text: {words}</desc>
  <rect width="800" height="500" fill="#fffef8"/>
  <rect x="16" y="16" width="768" height="468" fill="none" stroke="#222" stroke-width="3"/>
  <text x="40" y="56" font-family="Georgia, serif" font-size="22" fill="#111">{asset}</text>
  <text x="40" y="86" font-family="Helvetica, Arial, sans-serif" font-size="14" fill="#333">truth_class: CONCEPTUAL_EDUCATIONAL_PROTOTYPE · age_band: {band}</text>
  <text x="40" y="120" font-family="Georgia, serif" font-size="36" font-weight="bold" fill="#111">{title}</text>
  <g transform="translate(400,40)">
    {shape}
    {glyph}
  </g>
  <foreignObject x="40" y="340" width="720" height="100">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Georgia, serif; font-size: 22px; color:#111; line-height:1.35;">{words}</div>
  </foreignObject>
  <text x="40" y="460" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#444">KIDS DEVELOPMENTAL PROTOTYPE · NOT CHILD-VALIDATED · NOT PUBLICATION-READY</text>
  <!-- text-safe zone: left 40..760, top title band; illustration primarily x=400..700 -->
</svg>
'''


def write_asset_meta(band: str, spread: dict, svg_path: Path) -> dict:
    asset = f"FIG-ONE-TAP-{band}-{spread['id']}"
    meta = {
        "asset_id": asset,
        "truth_class": "CONCEPTUAL_EDUCATIONAL_PROTOTYPE",
        "age_band": f"KIDS-{band}",
        "alt": f"Style-neutral illustration for '{spread['title']}': {spread['action']}",
        "description": spread["action"],
        "purpose": f"ONE TAP pilot spread {spread['id']} ({spread['cadence']})",
        "text_safe_zones": {"title_band": [40, 40, 720, 90], "body_band": [40, 340, 720, 100]},
        "print_dimensions_px": {"width": 800, "height": 500, "note": "prototype CSS px @ ~150dpi intent"},
        "digital_dimensions_px": {"width": 800, "height": 500},
        "path": str(svg_path.relative_to(ROOT)),
        "owner_aesthetic_approval": "PENDING",
        "copyrighted_character_imitation": False,
    }
    write(svg_path.with_suffix(".meta.yaml"), "\n".join([
        f"asset_id: {meta['asset_id']}",
        f"truth_class: {meta['truth_class']}",
        f"age_band: {meta['age_band']}",
        f"alt: {yaml_quote(meta['alt'])}",
        f"description: {yaml_quote(meta['description'])}",
        f"purpose: {yaml_quote(meta['purpose'])}",
        "text_safe_zones:",
        "  title_band: [40, 40, 720, 90]",
        "  body_band: [40, 340, 720, 100]",
        "print_dimensions_px: {width: 800, height: 500}",
        "digital_dimensions_px: {width: 800, height: 500}",
        f"path: {yaml_quote(meta['path'])}",
        "owner_aesthetic_approval: PENDING",
        "copyrighted_character_imitation: false",
    ]))
    return meta


def write_page_trace(band_id: str, short: str, spreads: list[dict]) -> None:
    lines = [
        f"# Page/spread traceability — ONE TAP / {band_id}",
        "meta:",
        "  pilot: ONE_TAP",
        f"  age_band: {band_id}",
        "  adult_source_chapter: CH02",
        "  rewrite_method: developmental_precursor_rewrite",
        "  child_validation: NONE",
        "spreads:",
    ]
    for sp in spreads:
        lines += [
            f"  - page_or_spread_id: ONE-TAP-{short}-{sp['id']}",
            "    concept_ids: [KCON-CH02-ONE-TAP]",
            f"    learning_goal: {yaml_quote(sp['action'])}",
            f"    developmental_domain: {yaml_quote(sp['cadence'])}",
            "    standards:",
            "      - status: NOT_YET_MAPPED",
            f"        wire_id: STD-WIRE-ONE-TAP-{short}-{sp['id']}",
            "    evidence_rules: [no_fabricated_child_validation, observation_over_diagnosis]",
            "    visual_rules: [one_focal_action, low_clutter, color_not_sole_encoding, style_neutral_prototype]",
            "    audio_rules: [caregiver_read_aloud_optional, no_mandatory_audio, no_artificial_squeak_claims]",
            "    safety_rules: [easy_stop, caregiver_mediation, no_child_data_collection, no_dark_patterns]",
            f"    figure_id: FIG-ONE-TAP-{short}-{sp['id']}",
            f"    word_count_estimate: {len(sp['words'].split())}",
        ]
    write(PILOT / f"KIDS-{short}" / "TRACEABILITY.yaml", "\n".join(lines))


def write_band_manuscript(band_id: str, short: str, ages: str, spreads: list[dict]) -> dict:
    words_total = sum(len(s["words"].split()) for s in spreads)
    body = [
        f"# ONE TAP — {band_id} ({ages})",
        "",
        "```",
        *PROTOTYPE_BANNER.splitlines(),
        "```",
        "",
        "**Pilot concept:** Input → Response (adult CH02 developmental rewrite, not sentence simplification).",
        "**Concept ID:** `KCON-CH02-ONE-TAP`",
        "**Child validation:** none",
        "",
        "## Caregiver / educator note",
        "",
        spreads[0]["caregiver"] if short in {"BABY", "TODDLER"} else "Use observation, not ranking. Stop anytime.",
        "",
    ]
    for sp in spreads:
        body += [
            f"## Spread {sp['id']} — {sp['title']} ({sp['cadence']})",
            "",
            f"![FIG-ONE-TAP-{short}-{sp['id']}](figures/FIG-ONE-TAP-{short}-{sp['id']}.svg)",
            "",
            f"**Child-facing text:** {sp['words']}",
            "",
            f"**Action:** {sp['action']}",
            "",
            f"**Caregiver prompt:** {sp['caregiver']}",
            "",
        ]
    body += [
        "## Standards appendix (adult-facing)",
        "",
        "All mappings `NOT_YET_MAPPED` pending sister standards atlas land. Wire IDs in `TRACEABILITY.yaml`.",
        "",
        "## Source / evidence appendix (adult-facing)",
        "",
        f"- Adult CH02 on main `{ADULT_MAIN}`",
        f"- Spiral: `kids/concepts/ADULT31_TO_KIDS_SPIRAL.yaml`",
        "- No child testing was conducted for this prototype.",
        "",
    ]
    write(PILOT / f"KIDS-{short}" / "MANUSCRIPT.md", "\n".join(body))
    return {"spreads": len(spreads), "words": words_total, "figures": len(spreads)}


def build_html(band_id: str, short: str, ages: str, spreads: list[dict]) -> Path:
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        f"<title>ONE TAP {band_id} caregiver preview</title>",
        "<style>",
        "body{font-family:Georgia,serif;max-width:820px;margin:2rem auto;padding:0 1rem;background:#fffef8;color:#111;}",
        ".banner{border:3px solid #111;padding:1rem;margin-bottom:1.5rem;background:#f3f3f3;font-family:Helvetica,Arial,sans-serif;}",
        ".stop{position:sticky;top:0;background:#111;color:#fff;padding:.75rem 1rem;font-family:Helvetica,Arial,sans-serif;}",
        "img,svg{max-width:100%;height:auto;border:1px solid #222;}",
        "figure{margin:2rem 0;} figcaption{font-size:.95rem;color:#333;}",
        "</style></head><body>",
        "<div class='stop'><a href='#end' style='color:#fff'>Easy exit / stop</a> · Autoplay: OFF · No data collection</div>",
        "<div class='banner'><pre style='margin:0;white-space:pre-wrap'>",
        PROTOTYPE_BANNER,
        "</pre></div>",
        f"<h1>ONE TAP — {band_id}</h1>",
        f"<p>Age guide: {ages}. Caregiver/educator preview. Not for unsupervised infant digital use as a product.</p>",
    ]
    for sp in spreads:
        src = f"figures/FIG-ONE-TAP-{short}-{sp['id']}.svg"
        parts += [
            f"<figure id='{sp['id']}'>",
            f"<img src='{src}' alt=\"FIG-ONE-TAP-{short}-{sp['id']}: {sp['action']}\"/>",
            f"<figcaption><strong>{sp['id']} · {sp['title']}</strong> — {sp['words']}<br/>Caregiver: {sp['caregiver']}</figcaption>",
            "</figure>",
        ]
    parts += [
        "<section id='end'><h2>End / stop</h2><p>Close this preview anytime. No accounts. No tracking.</p></section>",
        "</body></html>",
    ]
    out = PILOT / f"KIDS-{short}" / "builds" / "caregiver-preview.html"
    write(out, "\n".join(parts))
    return out


def build_pdf(band_id: str, short: str, ages: str, spreads: list[dict]) -> Path:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

    out = PILOT / f"KIDS-{short}" / "builds" / f"ONE_TAP_{short}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out), pagesize=letter)
    w, h = letter

    def banner(c):
        c.setFont("Helvetica-Bold", 12)
        y = h - 0.7 * inch
        for line in PROTOTYPE_BANNER.splitlines():
            c.drawString(0.75 * inch, y, line)
            y -= 14
        return y - 10

    # cover
    y = banner(c)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.75 * inch, y, f"ONE TAP / INPUT→RESPONSE — {band_id}")
    y -= 24
    c.setFont("Helvetica", 12)
    c.drawString(0.75 * inch, y, f"Age guide: {ages}")
    y -= 18
    c.drawString(0.75 * inch, y, "Developmental rewrite of adult CH02 · style-neutral prototypes")
    c.showPage()

    for sp in spreads:
        y = banner(c)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(0.75 * inch, y, f"{sp['id']} — {sp['title']} ({sp['cadence']})")
        y -= 28
        # simple drawn focal mark (not placeholder text)
        c.setStrokeColorRGB(0.1, 0.1, 0.1)
        c.setLineWidth(2)
        c.circle(3.5 * inch, y - 1.1 * inch, 0.9 * inch)
        c.circle(3.5 * inch, y - 1.0 * inch, 0.12 * inch, fill=1)
        y -= 2.5 * inch
        c.setFont("Times-Roman", 14)
        for line in textwrap.wrap(sp["words"], 85):
            c.drawString(0.75 * inch, y, line)
            y -= 18
        y -= 8
        c.setFont("Helvetica", 11)
        for line in textwrap.wrap(f"Action: {sp['action']}", 90):
            c.drawString(0.75 * inch, y, line)
            y -= 14
        for line in textwrap.wrap(f"Caregiver: {sp['caregiver']}", 90):
            c.drawString(0.75 * inch, y, line)
            y -= 14
        c.setFont("Helvetica", 9)
        c.drawString(0.75 * inch, 0.6 * inch, f"FIG-ONE-TAP-{short}-{sp['id']} · CONCEPTUAL_EDUCATIONAL_PROTOTYPE")
        c.showPage()

    # appendix
    y = banner(c)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.75 * inch, y, "Adult-facing appendices")
    y -= 22
    c.setFont("Helvetica", 11)
    for line in [
        "Standards: NOT_YET_MAPPED (wire IDs in TRACEABILITY.yaml)",
        f"Adult main: {ADULT_MAIN}",
        "No child validation evidence exists for this prototype.",
        "EPUB/fixed-layout: not generated — HTML+PDF sufficient for this pilot band.",
    ]:
        c.drawString(0.75 * inch, y, line)
        y -= 16
    c.save()
    return out


def write_waike_crosswalk() -> None:
    # Honest adjacency only — known digital_rc courses from adult CH02 metadata
    lines = [
        "# Kids Edition ↔ WAIKE crosswalk",
        "# Invent nothing. Statuses: exact | adjacent | proposed | no-map",
        "",
        "meta:",
        "  document_id: KIDS_WAIKE_CROSSWALK",
        "  waike_repo: gunnchOS3k/waike-research-ops",
        "  waike_ref: main",
        f'  waike_sha_reconfirmed: "{WAIKE_SHA}"',
        "  reconfirmed_on: \"2026-09-04\"",
        "  reconfirm_method: github_api_commits_main",
        f'  adult_main_sha: "{ADULT_MAIN}"',
        "  kids_as_waike_precursor_layer: DESIGN_STATE_NOT_IMPLEMENTED_UPSTREAM",
        "  child_validation: NONE",
        "",
        "mappings:",
        "  - kids_object: KCON-CH02-ONE-TAP",
        "    waike_id: SOFTWARE_BUILDER",
        "    id_system: digital_rc",
        "    status: adjacent",
        "    notes: "
        + yaml_quote("Adult CH02 already maps competency adjacency; kids pilot is precursor, not a WAIKE module."),
        "  - kids_object: KCON-CH02-ONE-TAP",
        "    waike_id: GAME_DEV_INTERACTIVE",
        "    id_system: digital_rc",
        "    status: adjacent",
        "    notes: "
        + yaml_quote("Interactive event/input adjacency only."),
        "  - kids_object: KCON-CH02-ONE-TAP",
        "    waike_id: COMPUTER_NETWORKING",
        "    id_system: digital_rc",
        "    status: adjacent",
        "    notes: "
        + yaml_quote("Optional network branch of ONE TAP; not exact kids module."),
        "  - kids_object: KCON-CH02-ONE-TAP",
        "    waike_id: EMBEDDED_PROTOTYPING",
        "    id_system: digital_rc",
        "    status: adjacent",
        "    notes: "
        + yaml_quote("Input/sensing adjacency for older bands only."),
        "  - kids_object: ONE_TAP_PILOT_AS_WAIKE_MODULE",
        "    waike_id: null",
        "    id_system: null",
        "    status: no-map",
        "    notes: "
        + yaml_quote("Do not invent ONE_TAP / KIDS-* WAIKE course IDs."),
        "  - kids_object: EARLY_LEARNING_PRECURSOR_LAYER",
        "    waike_id: null",
        "    id_system: null",
        "    status: proposed",
        "    notes: "
        + yaml_quote("Future upstream design discussion only; not present on audited SHA."),
        "  - kids_object: KCON-CH21-DATA-AI",
        "    waike_id: AI_ML_EDGE",
        "    id_system: digital_rc",
        "    status: adjacent",
        "    notes: "
        + yaml_quote("Adult materials reference AI_ML_EDGE labs; kids content is precursor only."),
        "  - kids_object: KCON-CH23-CYBERSECURITY",
        "    waike_id: CYBERSECURITY",
        "    id_system: digital_rc",
        "    status: adjacent",
        "    notes: "
        + yaml_quote("Adjacent package name used in adult audits; no kids cyber module ID invented."),
        "  - kids_object: KCON-CH30-CAREER-PORTFOLIO",
        "    waike_id: portfolio_evidence",
        "    id_system: docs_culture",
        "    status: adjacent",
        "    notes: "
        + yaml_quote("Portfolio culture adjacency; not an exact early-learning assessment module."),
        "",
        "non_claims:",
        "  - No exact WAIKE course titled Kids ONE TAP on audited main.",
        "  - No invented lab IDs.",
        "  - Kids Edition is not a certified WAIKE track.",
    ]
    write(KIDS / "waike" / "KIDS_WAIKE_CROSSWALK.yaml", "\n".join(lines))


def write_pilot_readme() -> None:
    write(
        PILOT / "README.md",
        f"""# ONE TAP / INPUT → RESPONSE pilot

```
{PROTOTYPE_BANNER}
```

Cross-age developmental rewrite of adult **CH02** (“Follow One Tap Through the Entire Stack”).

| Band | Path |
| --- | --- |
| Baby | `KIDS-BABY/` |
| Toddler | `KIDS-TODDLER/` |
| Preschool | `KIDS-PRESCHOOL/` |
| Pre-K | `KIDS-PREK/` |
| Elem1 | `KIDS-ELEM1/` |
| Elem2 | `KIDS-ELEM2/` |

Each band includes: `MANUSCRIPT.md`, `TRACEABILITY.yaml`, `figures/*.svg` + `.meta.yaml`, `builds/caregiver-preview.html`, `builds/ONE_TAP_*.pdf`.

**EPUB/fixed-layout:** not produced in this wave — print-like PDF + HTML caregiver preview are the justified prototypes; fixed-layout EPUB deferred until format matrix + media design constraints land.
""",
    )


def write_reports(unit_count: int, stats: dict) -> None:
    pilot_lines = [
        "# ONE TAP pilot report",
        "",
        f"```",
        *PROTOTYPE_BANNER.splitlines(),
        "```",
        "",
        "## Provenance",
        "",
        f"- Adult main: `{ADULT_MAIN}`",
        f"- Integration base: `{INTEGRATION_BASE}`",
        f"- WAIKE main reconfirmed: `{WAIKE_SHA}`",
        "- Adult source chapter: CH02 (developmental rewrite)",
        "",
        "## Coverage",
        "",
        "| Band | Spreads | Words (child-facing) | Figures | HTML | PDF |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for band_id, short, _ in BANDS:
        s = stats[short]
        pilot_lines.append(
            f"| {band_id} | {s['spreads']} | {s['words']} | {s['figures']} | yes | yes |"
        )
    pilot_lines += [
        "",
        "## Standards mappings",
        "",
        "All pilot spread standards entries: **NOT_YET_MAPPED** with `STD-WIRE-ONE-TAP-*` IDs.",
        "Sister standards atlas had not landed on integration at authoring time.",
        "",
        "## Validation",
        "",
        "- Real SVG prototypes (no “image here” placeholders)",
        "- Asset metadata present",
        "- Traceability YAML per band",
        "- Prototype banners on manuscripts/HTML/PDF",
        "- `make kids-pilot-check` / `make kids-concept-spiral-check`",
        "",
        "## Explicit non-claims",
        "",
        "- NOT CHILD-VALIDATED",
        "- NOT PUBLICATION-READY",
        "- NOT GLOBALLY_ALIGNED",
        "- No EPUB in this wave (justified deferral)",
        "",
    ]
    write(PILOT / "PILOT_REPORT.md", "\n".join(pilot_lines))

    write(
        KIDS / "KIDS_PRODUCTION_STATUS.md",
        f"""# Kids production status (curriculum / spiral / ONE TAP)

```
{PROTOTYPE_BANNER}
```

## Allowed state ceiling this wave

`KIDS_DEVELOPMENTAL_PROTOTYPE_READY_FOR_HUMAN_REVIEW` (candidate for integrator review)

**Not** `PUBLICATION_READY` · **Not** `GLOBALLY_ALIGNED` · **Not** child-validated

## Track progress (K10 / B3–B4, B17–B18, B23–B30)

| Deliverable | Path | State |
| --- | --- | --- |
| Concept spiral 31→7 | `kids/concepts/ADULT31_TO_KIDS_SPIRAL.yaml` | DRAFT_INTERNAL |
| Scope & sequence ({unit_count} units) | `kids/curriculum/KIDS_SCOPE_AND_SEQUENCE.yaml` | DRAFT_INTERNAL |
| Story/learning cadence | `kids/cadence/STORY_LEARNING_CADENCE.md` | DRAFT_INTERNAL |
| Caregiver co-learning | `kids/caregivers/CAREGIVER_GUIDE_SYSTEM.md` | DRAFT_INTERNAL |
| Assessment philosophy | `kids/assessment/KIDS_ASSESSMENT_PHILOSOPHY.md` | DRAFT_INTERNAL |
| ONE TAP pilot (6 bands) | `kids/pilots/ONE_TAP/` | DEVELOPMENTAL_PROTOTYPE |
| WAIKE crosswalk | `kids/waike/KIDS_WAIKE_CROSSWALK.yaml` | DRAFT_INTERNAL |
| Pilot report | `kids/pilots/ONE_TAP/PILOT_REPORT.md` | DRAFT_INTERNAL |

## SHAs

| Ref | SHA |
| --- | --- |
| Accepted adult main | `{ADULT_MAIN}` |
| Integration base | `{INTEGRATION_BASE}` |
| WAIKE main (reconfirmed) | `{WAIKE_SHA}` |

## Gaps for integrator

1. Wire `STD-WIRE-*` / `NOT_YET_MAPPED` entries when standards atlas lands.
2. Merge media/design visual system rules into figure metadata when K8/K9 land.
3. Decide EPUB/fixed-layout per `KIDS_FORMAT_MATRIX` (not authored on this branch).
4. Do not mark child validation complete.
5. Preserve adult Gate 3 / FULL31 candidate provenance untouched.

## Sister-agent dependency note

At authoring time, standards atlas and media-design kids artifacts were **not** available on the integration tip used as base (`{INTEGRATION_BASE}`). Placeholders are honest.
""",
    )


def main() -> None:
    write_support_docs()
    unit_count = write_scope_sequence()
    write_waike_crosswalk()
    write_pilot_readme()

    stats = {}
    for band_id, short, ages in BANDS:
        spreads = pilot_spreads(short)
        fig_dir = PILOT / f"KIDS-{short}" / "figures"
        for i, sp in enumerate(spreads):
            svg_path = fig_dir / f"FIG-ONE-TAP-{short}-{sp['id']}.svg"
            write(svg_path, svg_for_spread(short, sp, i))
            write_asset_meta(short, sp, svg_path)
        write_page_trace(band_id, short, spreads)
        stats[short] = write_band_manuscript(band_id, short, ages, spreads)
        build_html(band_id, short, ages, spreads)
        build_pdf(band_id, short, ages, spreads)
        # band README
        write(
            PILOT / f"KIDS-{short}" / "README.md",
            f"# {band_id} ONE TAP pilot\n\n```\n{PROTOTYPE_BANNER}\n```\n\n"
            f"- Spreads: {stats[short]['spreads']}\n"
            f"- Child-facing words: {stats[short]['words']}\n"
            f"- Figures: {stats[short]['figures']}\n"
            f"- HTML: `builds/caregiver-preview.html`\n"
            f"- PDF: `builds/ONE_TAP_{short}.pdf`\n",
        )

    write_reports(unit_count, stats)
    summary = {
        "unit_count": unit_count,
        "bands": stats,
        "waike_sha": WAIKE_SHA,
    }
    write(PILOT / "build_summary.json", json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
