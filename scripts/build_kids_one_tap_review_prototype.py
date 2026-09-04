#!/usr/bin/env python3
"""Build review-quality ONE TAP developmental prototypes (Track 3 / PR #7).

Separates editor/integrator meta into AUTHOR_NOTES.yaml; expands ELEM1/ELEM2 into
illustrated learning units; keeps Baby/Toddler developmentally sparse.
Claims ceiling: KIDS_REVIEW_PROTOTYPE_COMPLETE (not global-foundation-complete).
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "kids" / "pilots" / "ONE_TAP"
PROTOTYPE_BANNER = (
    "KIDS DEVELOPMENTAL PROTOTYPE\n"
    "NOT CHILD-VALIDATED\n"
    "NOT PUBLICATION-READY"
)
ADULT_MAIN = "82284cd8f41d750ff508cd6ea5bad0a9534d8162"
INTEGRATION_BASE = "ce9cc419841fa0588e30d8d917b048c72f8cc2c0"
WAIKE_SHA = "e97e74fc9bfb44b1cdc26b272dc4848264f15fe0"
CAST = {
    "option": "A_Signal_Crew_provisional",
    "explorer": "Mira",
    "builder": "Bolt",
    "instructions": "Step",
    "signals": "Ping",
    "safety": "Shield",
    "note": "Provisional Character Bible Option A — not owner-locked IP.",
}

BANDS = [
    ("KIDS-BABY", "BABY", "0–18 months"),
    ("KIDS-TODDLER", "TODDLER", "18–36 months"),
    ("KIDS-PRESCHOOL", "PRESCHOOL", "3–4 years"),
    ("KIDS-PREK", "PREK", "4–6 years"),
    ("KIDS-ELEM1", "ELEM1", "Kindergarten–Grade 2"),
    ("KIDS-ELEM2", "ELEM2", "Grades 3–5/6"),
]

EARLY_ATLAS = [
    "MAP-ELOF-PLAY-KE",
    "MAP-EYFS-PLAY-KE",
    "MAP-EYLF-PLAY-KE",
    "MAP-TEWHARIKI-PLAY-KE",
    "MAP-NEL-PLAY-KE",
    "MAP-ON-KG-PLAY-KE",
    "MAP-OECD-AGENCY-KE",
    "MAP-NCF-PLAY-KE",
]
EARLY_TARGETS = ["KE-TARGET-PLAY-INQUIRY"]
ELEM_ATLAS = [
    "MAP-CSTA2026-ALGO-KE",
    "MAP-AC-DT-KE",
    "MAP-CSTA2026-SYS-KE",
    "MAP-NGSS-SCI-KE",
    "MAP-CSTA2026-DATA-KE",
]
ELEM_TARGETS = [
    "KE-TARGET-ALGO-FOUNDATIONS",
    "KE-TARGET-SYSTEMS-STABILITY",
    "KE-TARGET-SCIENCE-PRACTICES",
    "KE-TARGET-DATA-PATTERNS",
]

# Design rules → child-media evidence IDs (CHILD_MEDIA_EVIDENCE_REGISTER.yaml)
DESIGN_RULE_EVIDENCE = {
    "one_focal_action": ["CME-001", "CME-005", "CME-007"],
    "low_clutter": ["CME-005", "CME-006"],
    "color_not_sole_encoding": ["CME-003", "CME-004"],
    "high_contrast_infant": ["CME-001", "CME-003"],
    "print_first_infant_toddler": ["CME-002", "CME-019", "CME-020"],
    "serve_and_return": ["CME-008", "CME-009", "CME-010"],
    "contingent_cause_effect": ["CME-011", "CME-013"],
    "stable_cast_continuity": ["CME-016", "CME-017", "CME-018"],
    "participatory_prompts": ["CME-018", "CME-021"],
    "easy_stop_agency": ["CME-022", "CME-023", "CME-024"],
    "no_dark_patterns": ["CME-025", "CME-026", "CME-027"],
    "observation_over_diagnosis": ["CME-028", "CME-029"],
    "style_neutral_prototype": ["CME-006", "CME-016"],
}

META_REMOVED = [
    "Use pilot figure",
    "No false GHz claims",
    "Link to adult CH02 honestly",
    "Honesty label required",
    "Adult CH02 developmental rewrite (from child-facing concept line)",
    "Standards appendix NOT_YET_MAPPED / dangling STD-WIRE body text",
    "Git SHA provenance in child/caregiver manuscript body",
    "sentence simplification disclaimer in child-facing header",
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def atlas_for(short: str) -> tuple[list[str], list[str]]:
    if short in {"BABY", "TODDLER", "PRESCHOOL", "PREK"}:
        return EARLY_ATLAS, EARLY_TARGETS
    return ELEM_ATLAS, ELEM_TARGETS


def spreads_for(short: str) -> list[dict]:
    """Return spreads. Keys: id, cadence, title, words, action, talk, author_meta, facilitator."""
    if short == "BABY":
        # Keep sparse — do not densify academically (C3 restraint).
        rows = [
            ("S01", "LOOK", "Look", "Look.", "Look together at one lit control.", "Follow gaze. Soft voice."),
            ("S02", "POINT", "Hand", "Hand.", "Notice hand near the surface.", "Point to hand, then control."),
            ("S03", "NAME", "Touch", "Touch.", "Finger meets surface.", "Name the touch when contact happens."),
            ("S04", "WAIT", "Wait", "Wait…", "A short wait before change.", "Pause. Do not rush."),
            ("S05", "RESPOND", "Change", "Change!", "Light or sound changes.", "Celebrate the change calmly."),
            ("S06", "REPEAT", "Again", "Again?", "Optional second touch.", "Offer repeat; accept no."),
            ("S07", "NAME", "Same place", "Same.", "Repeat at same control.", "Same spot → same kind of change."),
            ("S08", "LOOK", "New place", "New.", "Move attention to another control.", "Different control, different change."),
            ("S09", "POINT", "Point with me", "Point.", "Point to what changed.", "Invite pointing; no demand for speech."),
            ("S10", "RESPOND", "All done", "All done.", "Session ends positively.", "Easy stop. Close the book."),
        ]
        return [
            {
                "id": a,
                "cadence": b,
                "title": c,
                "words": d,
                "action": e,
                "talk": f,
                "author_meta": "print_first; one_focal; high_contrast",
                "facilitator": f,
            }
            for a, b, c, d, e, f in rows
        ]

    if short == "TODDLER":
        rows = [
            ("S01", "LOOK", "We look", "We look.", "Find the button together.", "One focal object."),
            ("S02", "NAME", "Input", "Touch is input.", "Name input with a gesture.", "Short phrase; gesture touch."),
            ("S03", "NAME", "Output", "Change is output.", "Point to the change.", "Point to the change."),
            ("S04", "WAIT", "First", "First: touch.", "Sequence start.", "Hold up one finger."),
            ("S05", "RESPOND", "Next", "Next: change.", "Sequence continue.", "Hold up two fingers."),
            ("S06", "POINT", "Find", "Find the button.", "Child points or finds.", "Child leads the find."),
            ("S07", "TRY", "Match", "Match touch to change.", "One supervised tap.", "One physical try."),
            ("S08", "REPEAT", "Again same", "Again — same.", "Repeat once.", "Repetition with joy."),
            ("S09", "SAFE + FAIR", "Ask adult", "New button? Ask.", "Practice ask-before-new.", "Calm safety rule."),
            ("S10", "TEACH", "Show me", "Show me touch → change.", "Child shows caregiver.", "Invite teach-back gesture."),
        ]
        return [
            {
                "id": a,
                "cadence": b,
                "title": c,
                "words": d,
                "action": e,
                "talk": f,
                "author_meta": "keep language short; no ranking",
                "facilitator": f,
            }
            for a, b, c, d, e, f in rows
        ]

    if short == "PRESCHOOL":
        return [
            {
                "id": "S01",
                "cadence": "STORY",
                "title": "The sticky song",
                "words": "Mira wants the song button to work. Bolt taps the box. Can they make music?",
                "action": "Meet Mira and Bolt; set the tiny problem.",
                "talk": "Tell the tiny story once. Pause for looking.",
                "author_meta": "Cast Option A provisional: Mira + Bolt",
                "facilitator": "Story hook only; do not lecture about stacks.",
            },
            {
                "id": "S02",
                "cadence": "NOTICE",
                "title": "What we notice",
                "words": "Mira presses. A light blinks. Music starts. What did you see first?",
                "action": "List noticed events in order with gestures.",
                "talk": "Notice before naming tech words.",
                "author_meta": None,
                "facilitator": "Accept pointing/vocalizing as answers.",
            },
            {
                "id": "S03",
                "cadence": "NAME",
                "title": "Parts",
                "words": "Button. Light. Speaker. Those are parts we can name.",
                "action": "Count three parts on fingers.",
                "talk": "Count parts on fingers.",
                "author_meta": None,
                "facilitator": "Concrete nouns only.",
            },
            {
                "id": "S04",
                "cadence": "CONNECT",
                "title": "Inside helps",
                "words": "Something inside the box helps the parts talk. The screen is not the whole story.",
                "action": "Connect outside parts to an “inside helpers” idea.",
                "talk": "Gesture from outside to inside.",
                "author_meta": "Do not invent magical frequencies.",
                "facilitator": "Keep mystery honest: we do not open sealed devices.",
            },
            {
                "id": "S05",
                "cadence": "PREDICT",
                "title": "Predict",
                "words": "If we press, what happens first? Next? Last?",
                "action": "Predict order before trying.",
                "talk": "Accept any sincere guess.",
                "author_meta": None,
                "facilitator": "Prediction before correction.",
            },
            {
                "id": "S06",
                "cadence": "TRY",
                "title": "Try the order",
                "words": "First press. Next blink. Last sound. Act it with Mira.",
                "action": "Act the sequence with body gestures.",
                "talk": "Act the sequence together.",
                "author_meta": None,
                "facilitator": "Movement helps memory.",
            },
            {
                "id": "S07",
                "cadence": "EXPLAIN",
                "title": "Sensor idea",
                "words": "The button notices a press. Bolt says it is like a tiny sensor.",
                "action": "Explain sensing in plain words.",
                "talk": "Keep language concrete.",
                "author_meta": None,
                "facilitator": "Sensor = notices a press.",
            },
            {
                "id": "S08",
                "cadence": "MAKE",
                "title": "Sort the cards",
                "words": "Sort three cards: press / blink / sound. Can you put them in order?",
                "action": "Sorting and sequencing with cards or drawings.",
                "talk": "Use three cards or drawings.",
                "author_meta": None,
                "facilitator": "Hands-on sequence evidence.",
            },
            {
                "id": "S09",
                "cadence": "SAFE + FAIR",
                "title": "Stop anytime",
                "words": "If it is too loud, Shield says we stop. Stopping is fair.",
                "action": "Model agency to stop.",
                "talk": "Model stop without shame.",
                "author_meta": "easy_stop_agency",
                "facilitator": "Stopping is success, not failure.",
            },
            {
                "id": "S10",
                "cadence": "TEACH",
                "title": "Teach a friend",
                "words": "Tell the story: press → blink → sound. Teach someone you trust.",
                "action": "Optional teach-back.",
                "talk": "Optional peer or caregiver share.",
                "author_meta": "participatory_prompts",
                "facilitator": "No forced performance.",
            },
        ]

    if short == "PREK":
        return [
            {
                "id": "S01",
                "cadence": "STORY",
                "title": "Message or local?",
                "words": (
                    "Jordan taps Refresh with Mira. Sometimes the phone already has the page. "
                    "Sometimes Ping says it must ask far away."
                ),
                "action": "Story hook: local copy vs far ask.",
                "talk": "Plant the optional network idea gently.",
                "author_meta": "Cast: Mira + Ping; Jordan is child peer",
                "facilitator": "Do not require network vocabulary yet.",
            },
            {
                "id": "S02",
                "cadence": "NOTICE",
                "title": "Two timelines",
                "words": (
                    "A quick highlight can happen before new words arrive. "
                    "Fast light now. New words maybe later."
                ),
                "action": "Notice immediate vs later feedback.",
                "talk": "Point to “now” and “later.”",
                "author_meta": None,
                "facilitator": "Two timings, one tap.",
            },
            {
                "id": "S03",
                "cadence": "NAME",
                "title": "System and component",
                "words": "The phone is a system. The button is a component — one part of the system.",
                "action": "Name system and component once, concretely.",
                "talk": "Use both words once with pointing.",
                "author_meta": None,
                "facilitator": "Concrete use only.",
            },
            {
                "id": "S04",
                "cadence": "CONNECT",
                "title": "Simple algorithm",
                "words": "Step shows three ordered steps: 1 sense press  2 choose action  3 show result.",
                "action": "Draw or line up three steps.",
                "talk": "Algorithm means ordered steps.",
                "author_meta": "Step = instructions character",
                "facilitator": "Order matters more than fancy words.",
            },
            {
                "id": "S05",
                "cadence": "PREDICT",
                "title": "Local prediction",
                "words": "If the page is already here, maybe no far message. What do you predict?",
                "action": "Predict local path.",
                "talk": "Prediction, not certainty.",
                "author_meta": None,
                "facilitator": "Mark guesses as guesses.",
            },
            {
                "id": "S06",
                "cadence": "TRY",
                "title": "Message path",
                "words": "If it needs new info, a message can travel out and back. Draw Ping’s path.",
                "action": "Draw a simple out-and-back path.",
                "talk": "Path drawing on paper.",
                "author_meta": None,
                "facilitator": "Paper path is enough.",
            },
            {
                "id": "S07",
                "cadence": "SAFE + FAIR",
                "title": "Private choice",
                "words": "Do we share the screen with a stranger? Shield says no — ask a trusted adult.",
                "action": "Choose the safer option.",
                "talk": "Safe and private choice.",
                "author_meta": "no_dark_patterns; caregiver mediation",
                "facilitator": "Calm, not scary.",
            },
            {
                "id": "S08",
                "cadence": "MAKE",
                "title": "Build-a-sequence",
                "words": "Build cards: Input → Steps → Output. Add optional Message if needed.",
                "action": "Hands-on sequence build.",
                "talk": "Hands-on sequence.",
                "author_meta": None,
                "facilitator": "Optional message card.",
            },
            {
                "id": "S09",
                "cadence": "EXPLAIN",
                "title": "Explain the path",
                "words": "Explain which path you built and why. Mira listens. Mistakes are OK.",
                "action": "Explain without perfection pressure.",
                "talk": "Listen without correcting every word.",
                "author_meta": None,
                "facilitator": "Process over polish.",
            },
            {
                "id": "S10",
                "cadence": "TEACH",
                "title": "Teach caregiver",
                "words": "Teach your caregiver the three steps. You are the teacher now.",
                "action": "Teach-back to caregiver.",
                "talk": "Adult becomes the learner.",
                "author_meta": "participatory_prompts",
                "facilitator": "Celebrate the teach-back.",
            },
        ]

    if short == "ELEM1":
        # Review-quality illustrated learning unit (C7) — ~80–120 words/spread target.
        return [
            {
                "id": "S01",
                "cadence": "OBSERVE",
                "title": "Two taps, two stories",
                "words": (
                    "Mira and Bolt sit with a tablet. First, Mira taps a lamp icon that only changes this device — "
                    "the screen brightens right away. Next, Mira taps Refresh on a class page that sometimes needs "
                    "the network. Watch both taps carefully. Write or draw: What changed fast? What waited? "
                    "Keep your notes for the portfolio page later."
                ),
                "action": "Observe one local tap and one network-ish tap; record what was seen.",
                "talk": "Supervise. No accounts. Separate “I saw” from “I think.”",
                "author_meta": "Supervise; no accounts. Prefer school-safe demo devices.",
                "facilitator": "Two observations before any vocabulary lecture.",
            },
            {
                "id": "S02",
                "cadence": "NAME",
                "title": "Hardware and software",
                "words": (
                    "Bolt points under the glass: hardware senses the touch — the touchscreen and chips you can touch "
                    "if a grown-up opened the case. Step holds a checklist: software is the instructions that decide "
                    "what happens next. Hardware notices. Software chooses. Say both words and point to an example."
                ),
                "action": "Name hardware vs software with one example each.",
                "talk": "Keep definitions short and pointed at the device.",
                "author_meta": "No GHz / IQ marketing claims.",
                "facilitator": "HW senses; SW instructs.",
            },
            {
                "id": "S03",
                "cadence": "NAME",
                "title": "Input → process → output",
                "words": (
                    "Fill three boxes with Mira. Input: the touch report (“someone pressed here”). "
                    "Process: the app decides what to do. Output: pixels, sound, or motion you can notice. "
                    "Draw arrows Input → Process → Output for the lamp tap."
                ),
                "action": "Complete an IPO diagram for one local tap.",
                "talk": "IPO diagram on paper or whiteboard.",
                "author_meta": None,
                "facilitator": "One concrete tap only.",
            },
            {
                "id": "S04",
                "cadence": "PREDICT",
                "title": "A four-step algorithm",
                "words": (
                    "Step asks for a four-step algorithm for the local lamp tap. Example shape: "
                    "1) sense press 2) check which control 3) change brightness 4) show new light. "
                    "Write your own clear order. Algorithms are recipes — order matters."
                ),
                "action": "Write a 4-step algorithm for a local tap.",
                "talk": "Any clear order is OK; fix together if stuck.",
                "author_meta": None,
                "facilitator": "Clarity > jargon.",
            },
            {
                "id": "S05",
                "cadence": "TEST",
                "title": "Local vs network",
                "words": (
                    "Test time. Which tap stayed local — finished on this device? Which tap waited as if a message "
                    "went out and came back? Ping draws two paths: a short loop on the tablet, and a longer path "
                    "that leaves the room. Classify your two taps. Mark guesses with a question mark."
                ),
                "action": "Classify taps as local vs network; mark uncertain inferences.",
                "talk": "Observation vs guess — label both.",
                "author_meta": None,
                "facilitator": "Core systems habit.",
            },
            {
                "id": "S06",
                "cadence": "EXPLAIN",
                "title": "Why feedback felt instant",
                "words": (
                    "Sometimes a button highlights instantly even when new words are still traveling. "
                    "Explain two timelines: Timeline A — local highlight. Timeline B — remote content. "
                    "Instant does not always mean “finished everywhere.”"
                ),
                "action": "Explain two timelines for one networked-feeling tap.",
                "talk": "Two timelines on one page.",
                "author_meta": None,
                "facilitator": "Felt speed ≠ full completion.",
            },
            {
                "id": "S07",
                "cadence": "SECURE",
                "title": "Safe practice",
                "words": (
                    "Shield’s checklist: Do not install unknown apps. Ask before sharing your name, photo, or school. "
                    "Locks and passwords are tools, not toys to share. Safety without scare stories — we practice calm choices."
                ),
                "action": "Complete a short safety checklist aloud or on paper.",
                "talk": "Safety without fear.",
                "author_meta": "No exploit content; no stranger-danger sensationalism.",
                "facilitator": "Consent + ask-a-trusted-adult.",
            },
            {
                "id": "S08",
                "cadence": "BUILD",
                "title": "Observation worksheet",
                "words": (
                    "Build a portfolio page with three columns: What I saw · What I infer · What I still don’t know. "
                    "Use your lamp tap and refresh tap. Inferences stay uncertain until tested. Unknowns are honest science."
                ),
                "action": "Complete observation worksheet for portfolio.",
                "talk": "Portfolio piece — process, not ranking.",
                "author_meta": "observation_over_diagnosis",
                "facilitator": "Celebrate unknowns.",
            },
            {
                "id": "S09",
                "cadence": "REFLECT",
                "title": "Misconception check",
                "words": (
                    "True or rethink: “Every tap goes to the internet.” Discuss kindly with Mira. "
                    "Many taps finish locally. Some need a network. Evidence from your tests beats the slogan."
                ),
                "action": "Revisit the misconception with evidence.",
                "talk": "Discuss kindly; no shame.",
                "author_meta": None,
                "facilitator": "Evidence > slogans.",
            },
            {
                "id": "S10",
                "cadence": "TEACH",
                "title": "Teach-back IPO",
                "words": (
                    "Teach a partner or caregiver the IPO path for one tap. Use Mira’s cast roles if it helps: "
                    "Bolt for parts you can touch, Step for instructions, Ping for optional messages, Shield for pause-and-check. "
                    "Stop anytime. This prototype is for learning practice — not a test score."
                ),
                "action": "Teach-back IPO path.",
                "talk": "Optional peer; easy stop.",
                "author_meta": "stable_cast_continuity; participatory_prompts",
                "facilitator": "Teach-back is evidence of process.",
            },
        ]

    # ELEM2 — junior-reader review prototype (C8)
    return [
        {
            "id": "S01",
            "cadence": "OBSERVE",
            "title": "Cross-layer path",
            "words": (
                "Follow one tap with Mira across layers you can name on paper: human intent → input hardware → "
                "operating-system event → application handler → optional network → output (pixels or sound) → "
                "your perception. Annotate the shared map. Circle steps you truly observed. Put a question mark on "
                "steps you only infer. A map is a model — useful, incomplete, and revisable. If two classmates mark "
                "different question marks, that is good science, not a fight. Compare notes before you “fix” anything. "
                "Leave one blank margin note titled Still invisible to us."
            ),
            "action": "Annotate cross-layer map; mark observe vs infer.",
            "talk": "Keep discussion concrete; shared figure is a tool, not a quiz key.",
            "author_meta": "EDITOR: use pilot figure as shared artifact; not child-facing instruction text.",
            "facilitator": "Model ≠ full machine. Mark uncertainty.",
        },
        {
            "id": "S02",
            "cadence": "NAME",
            "title": "CPU, memory, storage",
            "words": (
                "Bolt deals three role cards. CPU: runs instructions right now. Memory (working space): holds state "
                "the program is using this moment. Storage (keep-box): keeps durable data for later. "
                "Sort classroom examples: the instructions being followed, today’s draft text still open, yesterday’s "
                "saved file. Say the roles aloud. We describe jobs machines do — we do not invent magic megahertz, "
                "“brain speed,” or frequency-to-intelligence product claims. If a label sounds like an ad, rewrite it."
            ),
            "action": "Sort role cards for CPU / memory / storage.",
            "talk": "Roles, not marketing numbers.",
            "author_meta": "EDITOR: no false GHz / IQ claims (author constraint).",
            "facilitator": "Plain roles beat specs theater.",
        },
        {
            "id": "S03",
            "cadence": "NAME",
            "title": "OS and app events",
            "words": (
                "A tap becomes an event. The operating system notices input-hardware activity and delivers an event "
                "toward the app that should respond. Inside the app, an event loop can dispatch a handler that updates "
                "state and asks for a new frame of output. Draw one chain on a single page: "
                "tap → OS event → app handler → updated state → screen or sound. "
                "This is a junior model of stack ideas — earned with classroom words. Do not copy adult chapter prose; "
                "if a word is new, define it once with a pointing example."
            ),
            "action": "Draw event-handling sequence.",
            "talk": "Keep the chain on one page; avoid jargon dumps.",
            "author_meta": "EDITOR: honest adjacency to adult CH02; no paste.",
            "facilitator": "Event → handler → state → output.",
        },
        {
            "id": "S04",
            "cadence": "PREDICT",
            "title": "Packets or not?",
            "words": (
                "Ping asks: does your action need packets — little addressed message pieces that can travel on a network? "
                "Predict first, in writing. Then imagine airplane mode or radio off: what would you observe if the action "
                "were local only? What would fail, hang, or stay blank if it needed the network? "
                "Fill three boxes: prediction → planned observation → result. Local vs network is a question for evidence, "
                "not a slogan you memorize. If you cannot test safely today, keep the prediction and write why the test waited."
            ),
            "action": "Predict packet need; plan an observation if radio is off.",
            "talk": "Prediction before trial.",
            "author_meta": None,
            "facilitator": "Hypothesis discipline.",
        },
        {
            "id": "S05",
            "cadence": "MEASURE",
            "title": "Latency: feel vs measure",
            "words": (
                "Latency means waiting time somewhere on a path. Felt delay is what your body notices; measured delay is "
                "what a timer roughly shows. Use a classroom stopwatch on a remote refresh. Record three marks if you can: "
                "start, first visible change, and content “done enough.” Separate felt delay from guessed cause — "
                "slow Wi‑Fi, a busy CPU, and a far server can feel similar until you gather evidence. "
                "Rough numbers beat confident myths. Write units (seconds) beside every mark."
            ),
            "action": "Rough stopwatch measure of a remote refresh.",
            "talk": "Classroom timer OK; rough is honest.",
            "author_meta": None,
            "facilitator": "Feel ≠ cause.",
        },
        {
            "id": "S06",
            "cadence": "EXPLAIN",
            "title": "Observation vs inference",
            "words": (
                "Two columns only: Observation | Inference. Example observation: “Highlight appeared in under a second.” "
                "Example inference: “Therefore no packets were sent.” Mark every inference with a ? until tested. "
                "Systems literacy starts when we stop pretending every story we tell ourselves is a measurement. "
                "Trade papers with a partner and circle any inference dressed up as a fact. "
                "Add a third tiny box if needed: Still don’t know — and keep it empty of fake certainty."
            ),
            "action": "Two-column notes with uncertainty marks.",
            "talk": "Core systems skill — model it first.",
            "author_meta": None,
            "facilitator": "Uncertainty is a feature.",
        },
        {
            "id": "S07",
            "cadence": "SECURE",
            "title": "Security vs privacy",
            "words": (
                "Shield separates two ideas that often get mashed together. Security: controls that protect systems and "
                "accounts — lock screen, updates, permission prompts. Privacy: choices about who can see or keep your "
                "information. List one security control and one privacy choice that change a tap path. "
                "We may talk about HTTPS as “the path tries to keep the message harder for strangers to read on the way.” "
                "No exploit steps. No hacking practice. Calm tools beat scary stories."
            ),
            "action": "List one security control + one privacy choice.",
            "talk": "No exploit content.",
            "author_meta": "EDITOR: no exploit / offensive content.",
            "facilitator": "Security ≠ privacy; both matter.",
        },
        {
            "id": "S08",
            "cadence": "BUILD",
            "title": "Build, test, teach",
            "words": (
                "Build a paper protocol for tracing one tap: numbered steps, a failure branch "
                "(“if no change, check power / ask a trusted adult”), and a teach-back script written for a younger band "
                "(Pre‑K or K–2 language — short sentences, no stack jargon). Test the protocol once with a partner. "
                "Repair one unclear step and date the repair. Portfolio artifact = protocol + teach script + one repair note. "
                "Repair is success."
            ),
            "action": "Paper protocol + younger-band teach script + one repair.",
            "talk": "Portfolio artifact; process evidence.",
            "author_meta": None,
            "facilitator": "Repair is celebrated.",
        },
        {
            "id": "S09",
            "cadence": "REFLECT",
            "title": "Spiral: baby to map",
            "words": (
                "What stays the same from baby LOOK → CHANGE to this cross-layer map? Contingent action and response — "
                "something happens, then something answers. What vocabulary was earned later: input, output, event, packet, "
                "latency, privacy, security? Spiral learning means the same idea grows tools as learners grow. "
                "It does not mean babies should hear junior-reference prose. Honor the sparse earlier bands. "
                "Write one sentence you would teach a toddler and one you would only teach this band."
            ),
            "action": "Spiral reflection note.",
            "talk": "Honor earlier bands’ restraint.",
            "author_meta": "Spiral reflection — not adult dump.",
            "facilitator": "Continuity without densifying babies.",
        },
        {
            "id": "S10",
            "cadence": "TEACH",
            "title": "EMIT mini-capstone",
            "words": (
                "EMIT loop: Explain one tap path · Measure one wait · Improve one step of your protocol · Teach someone else. "
                "Say the honesty lines with Shield, calmly: this is a kids developmental prototype; it is not child-validated; "
                "it is not publication-ready. Learning bravely includes labeling what we have not tested with children. "
                "Your portfolio shows process evidence — not a fake certificate. When you teach, invite questions you cannot "
                "answer yet, and write them down for next time."
            ),
            "action": "Complete EMIT loop with honesty labels spoken.",
            "talk": "Honesty labels are part of the learning, spoken calmly.",
            "author_meta": "EDITOR: honesty label required in facilitator practice — keep prototype banner on artifacts.",
            "facilitator": "EMIT + honesty; no fabricated validation.",
        },
    ]


def write_format_truth_vocab() -> None:
    lines = [
        "# ONE TAP format truth vocabulary (by age band)",
        "# Status: KIDS_REVIEW_PROTOTYPE — NOT CHILD-VALIDATED · NOT PUBLICATION-READY",
        "",
        "meta:",
        "  document_id: ONE_TAP_FORMAT_TRUTH_VOCABULARY",
        '  version: "0.2.0-review-prototype"',
        "  companion_format_matrix: kids/publication/KIDS_FORMAT_MATRIX.yaml",
        "  companion_visual_system: kids/design/KIDS_VISUAL_SYSTEM.md",
        "",
        "global_allowed_truth_classes:",
        "  - CONCEPTUAL_EDUCATIONAL_PROTOTYPE",
        "  - CAREGIVER_FACILITATOR_GUIDANCE",
        "  - EDITORIAL_STANDARDS_CROSSWALK  # adult/integrator facing only",
        "",
        "global_forbidden_claims:",
        "  - CHILD_VALIDATED",
        "  - PUBLICATION_READY",
        "  - OFFICIALLY_STANDARDS_ALIGNED",
        "  - GHz_OR_FREQUENCY_TO_INTELLIGENCE_CLAIMS",
        "  - FABRICATED_READER_EVIDENCE",
        "",
        "bands:",
    ]
    band_vocab = {
        "BABY": {
            "print_truth": "board_book_intent_prototype_PDF_not_vendor_board",
            "digital_truth": "caregiver_preview_only_print_first",
            "child_text_truth": "micro_labels_0_to_8_words",
            "evidence_ids": ["CME-001", "CME-002", "CME-003", "CME-005"],
        },
        "TODDLER": {
            "print_truth": "board_or_picture_prototype_PDF",
            "digital_truth": "co_use_preview_autoplay_off",
            "child_text_truth": "short_phrases_input_output",
            "evidence_ids": ["CME-002", "CME-005", "CME-008", "CME-011"],
        },
        "PRESCHOOL": {
            "print_truth": "picture_activity_prototype",
            "digital_truth": "fixed_layout_preferred_when_spatial",
            "child_text_truth": "story_plus_sequence_15_to_40_words",
            "evidence_ids": ["CME-006", "CME-016", "CME-018"],
        },
        "PREK": {
            "print_truth": "picture_activity_plus_guides_prototype",
            "digital_truth": "PDF_plus_optional_fixed_epub_later",
            "child_text_truth": "system_component_algorithm_plain_language",
            "evidence_ids": ["CME-006", "CME-016", "CME-021", "CME-024"],
        },
        "ELEM1": {
            "print_truth": "illustrated_reader_activity_pack_prototype",
            "digital_truth": "reflowable_preferred_for_text_heavy",
            "child_text_truth": "ipo_local_vs_network_portfolio_40_to_120_words",
            "evidence_ids": ["CME-006", "CME-016", "CME-018", "CME-028"],
        },
        "ELEM2": {
            "print_truth": "junior_reference_labs_portfolio_prototype",
            "digital_truth": "HTML_PDF_educator_notes_ok",
            "child_text_truth": "cross_layer_measure_secure_chunked_prose",
            "evidence_ids": ["CME-006", "CME-016", "CME-028", "CME-029"],
        },
    }
    for band_id, short, ages in BANDS:
        v = band_vocab[short]
        lines += [
            f"  - age_band: {band_id}",
            f"    age_guide: {yaml_quote(ages)}",
            f"    print_truth_label: {v['print_truth']}",
            f"    digital_truth_label: {v['digital_truth']}",
            f"    child_text_truth_label: {v['child_text_truth']}",
            "    figure_truth_class: CONCEPTUAL_EDUCATIONAL_PROTOTYPE",
            "    media_evidence_ids:",
        ]
        for eid in v["evidence_ids"]:
            lines.append(f"      - {eid}")
        lines.append("")
    write(PILOT / "FORMAT_TRUTH_VOCABULARY.yaml", "\n".join(lines))


def svg_for_spread(band: str, spread: dict, idx: int) -> str:
    asset = f"FIG-ONE-TAP-{band}-{spread['id']}"
    title = spread["title"]
    words = spread["words"]
    # Character silhouettes for older bands (style-neutral)
    cast_note = ""
    if band in {"PRESCHOOL", "PREK", "ELEM1", "ELEM2"}:
        cast_note = (
            f'<text x="40" y="108" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#333">'
            f"Cast (provisional): {CAST['explorer']} · {CAST['builder']} · {CAST['instructions']} · "
            f"{CAST['signals']} · {CAST['safety']}</text>"
        )
    shapes = [
        '<circle cx="200" cy="200" r="68" fill="#f4f4f4" stroke="#111" stroke-width="4"/>',
        '<rect x="130" y="140" width="140" height="120" rx="8" fill="#f4f4f4" stroke="#111" stroke-width="4"/>',
        '<polygon points="200,130 270,250 130,250" fill="#f4f4f4" stroke="#111" stroke-width="4"/>',
    ]
    shape = shapes[idx % 3]
    # Layer ticks for ELEM2 cross-layer feel
    layers = ""
    if band == "ELEM2" and spread["id"] == "S01":
        layers = """
  <g font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#111">
    <text x="520" y="150">1 human</text>
    <text x="520" y="170">2 input HW</text>
    <text x="520" y="190">3 OS event</text>
    <text x="520" y="210">4 app</text>
    <text x="520" y="230">5 network?</text>
    <text x="520" y="250">6 output</text>
    <text x="520" y="270">7 perception</text>
  </g>"""
    body = words if len(words) < 160 else (words[:157] + "…")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500" role="img" aria-labelledby="{asset}-title {asset}-desc" data-asset-id="{asset}">
  <title id="{asset}-title">{asset}: {title}</title>
  <desc id="{asset}-desc">Style-neutral ONE TAP prototype for {band}. Action: {spread['action']}. Child text excerpt: {body}</desc>
  <rect width="800" height="500" fill="#fffef8"/>
  <rect x="16" y="16" width="768" height="468" fill="none" stroke="#222" stroke-width="3"/>
  <text x="40" y="52" font-family="Georgia, serif" font-size="20" fill="#111">{asset}</text>
  <text x="40" y="74" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#333">truth_class: CONCEPTUAL_EDUCATIONAL_PROTOTYPE · age_band: {band}</text>
  <text x="40" y="98" font-family="Georgia, serif" font-size="28" font-weight="bold" fill="#111">{title}</text>
  {cast_note}
  <g transform="translate(380,50)">
    {shape}
    <circle cx="200" cy="200" r="9" fill="#111"/>
    <line x1="200" y1="210" x2="200" y2="270" stroke="#111" stroke-width="4"/>
    <path d="M200 270 L182 290 L218 290 Z" fill="#111"/>
  </g>
  {layers}
  <foreignObject x="40" y="320" width="720" height="120">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Georgia, serif; font-size: 16px; color:#111; line-height:1.35;">{body}</div>
  </foreignObject>
  <text x="40" y="460" font-family="Helvetica, Arial, sans-serif" font-size="11" fill="#444">KIDS DEVELOPMENTAL PROTOTYPE · NOT CHILD-VALIDATED · NOT PUBLICATION-READY</text>
</svg>
'''


def write_asset_meta(band: str, spread: dict, svg_path: Path) -> None:
    asset = f"FIG-ONE-TAP-{band}-{spread['id']}"
    alt = f"Style-neutral illustration for '{spread['title']}': {spread['action']}"
    purpose = f"ONE TAP review prototype spread {spread['id']} ({spread['cadence']})"
    write(
        svg_path.with_suffix(".meta.yaml"),
        "\n".join(
            [
                f"asset_id: {asset}",
                "truth_class: CONCEPTUAL_EDUCATIONAL_PROTOTYPE",
                f"age_band: KIDS-{band}",
                f"alt: {yaml_quote(alt)}",
                f"description: {yaml_quote(spread['action'])}",
                f"purpose: {yaml_quote(purpose)}",
                "text_safe_zones:",
                "  title_band: [40, 40, 720, 90]",
                "  body_band: [40, 320, 720, 120]",
                "print_dimensions_px: {width: 800, height: 500}",
                "digital_dimensions_px: {width: 800, height: 500}",
                f"path: {yaml_quote(str(svg_path.relative_to(ROOT)))}",
                "owner_aesthetic_approval: PENDING",
                "copyrighted_character_imitation: false",
                f"character_cast_option: {CAST['option']}",
                "media_evidence_ids: [CME-001, CME-003, CME-006, CME-016]",
                "a11y:",
                "  has_title_desc: true",
                "  color_not_sole_encoding: true",
                "  reading_order: title_then_focal_then_body",
            ]
        ),
    )


def write_traceability(band_id: str, short: str, spreads: list[dict]) -> None:
    atlas, targets = atlas_for(short)
    lines = [
        "# ONE TAP review-prototype traceability",
        "# NOT CHILD-VALIDATED · NOT PUBLICATION-READY · editorial ADJACENT crosswalk only",
        "",
        "meta:",
        "  pilot: ONE_TAP",
        f"  age_band: {band_id}",
        "  adult_source_chapter: CH02",
        "  rewrite_method: developmental_precursor_rewrite",
        "  child_validation: NONE",
        "  claim_ceiling: KIDS_REVIEW_PROTOTYPE_COMPLETE",
        "  standards_relationship: CROSSWALKED_AGAINST",
        "  character_cast_option: " + CAST["option"],
        "spreads:",
    ]
    for sp in spreads:
        lines += [
            f"  - page_or_spread_id: ONE-TAP-{short}-{sp['id']}",
            "    concept_ids:",
            "      - KCON-CH02-ONE-TAP",
            f"    learning_goal: {yaml_quote(sp['action'])}",
            f"    developmental_domain: {yaml_quote(sp['cadence'])}",
            "    standards:",
            "      - status: ADJACENT",
            "        atlas_mapping_ids:",
        ]
        for m in atlas:
            lines.append(f"          - {m}")
        lines.append("        atlas_kids_targets:")
        for t in targets:
            lines.append(f"          - {t}")
        lines += [
            "        wire_registry_key: "
            + f"STD-WIRE-ONE-TAP-{short}-{sp['id']}",
            "        note: "
            + yaml_quote(
                f"Editorial ADJACENT crosswalk to atlas maps for {band_id}; "
                "not official alignment; NO_CHILD_VALIDATION_EVIDENCE. "
                "wire_registry_key indexes WIRE_HOOK_REGISTRY only — not a dangling map substitute."
            ),
            "    evidence_rules:",
            "      - no_fabricated_child_validation",
            "      - observation_over_diagnosis",
            "    visual_rules:",
            "      - one_focal_action",
            "      - low_clutter",
            "      - color_not_sole_encoding",
            "      - style_neutral_prototype",
            "    visual_rule_evidence:",
            "      one_focal_action: [CME-001, CME-005, CME-007]",
            "      low_clutter: [CME-005, CME-006]",
            "      color_not_sole_encoding: [CME-003, CME-004]",
            "      style_neutral_prototype: [CME-006, CME-016]",
            "    audio_rules:",
            "      - caregiver_read_aloud_optional",
            "      - no_mandatory_audio",
            "      - no_artificial_squeak_claims",
            "    safety_rules:",
            "      - easy_stop",
            "      - caregiver_mediation",
            "      - no_child_data_collection",
            "      - no_dark_patterns",
            "    safety_rule_evidence:",
            "      easy_stop: [CME-022, CME-023, CME-024]",
            "      no_dark_patterns: [CME-025, CME-026, CME-027]",
            f"    figure_id: FIG-ONE-TAP-{short}-{sp['id']}",
            f"    word_count_estimate: {len(sp['words'].split())}",
        ]
    # Honest gap row example for non-English frameworks needing translation (not dangling)
    lines += [
        "gaps:",
        "  - status: TRANSLATION_REQUIRED",
        "    note: "
        + yaml_quote(
            "Some atlas-adjacent jurisdictions remain TRANSLATION_REQUIRED at atlas level; "
            "ONE TAP does not invent EXACT maps for those rows."
        ),
        "  - status: VERSION_UNCLEAR",
        "    note: "
        + yaml_quote(
            "Where atlas sources mark SOURCE_VERSION_UNCLEAR, pilot keeps ADJACENT only."
        ),
        "  - status: NO_MAP",
        "    note: "
        + yaml_quote(
            "No EXACT official kids ONE TAP competency exists; do not fabricate EXACT status."
        ),
    ]
    write(PILOT / f"KIDS-{short}" / "TRACEABILITY.yaml", "\n".join(lines))


def write_author_notes(band_id: str, short: str, ages: str, spreads: list[dict]) -> None:
    lines = [
        f"# AUTHOR / INTEGRATOR NOTES — {band_id} (not child-facing)",
        "",
        "meta:",
        f"  age_band: {band_id}",
        f"  age_guide: {yaml_quote(ages)}",
        "  claim_ceiling: KIDS_REVIEW_PROTOTYPE_COMPLETE",
        "  child_validation: NONE",
        "  publication_ready: false",
        f"  adult_main_sha: {ADULT_MAIN}",
        f"  adult_source: CH02 developmental rewrite (not sentence simplification)",
        f"  character_cast: {CAST['option']}",
        "  spiral_ref: kids/concepts/ADULT31_TO_KIDS_SPIRAL.yaml",
        "",
        "editor_constraints_moved_out_of_body:",
    ]
    for m in META_REMOVED:
        lines.append(f"  - {yaml_quote(m)}")
    lines += [
        "",
        "design_rule_evidence_index:",
    ]
    for rule, ids in DESIGN_RULE_EVIDENCE.items():
        lines.append(f"  {rule}: [{', '.join(ids)}]")
    lines += ["", "spreads:"]
    for sp in spreads:
        lines += [
            f"  - id: {sp['id']}",
            f"    facilitator_note: {yaml_quote(sp['facilitator'])}",
            f"    author_meta: {yaml_quote(sp.get('author_meta') or 'none')}",
            f"    talk_together_child_safe: {yaml_quote(sp['talk'])}",
        ]
    lines += [
        "",
        "standards:",
        "  see: TRACEABILITY.yaml",
        "  relationship: CROSSWALKED_AGAINST",
        "  fidelity_ceiling: ADJACENT",
        "",
        "non_claims:",
        "  - NOT CHILD-VALIDATED",
        "  - NOT PUBLICATION-READY",
        "  - NOT GLOBALLY_ALIGNED / not KIDS_GLOBAL_FOUNDATION_AND_REVIEW_PROTOTYPE_COMPLETE",
    ]
    write(PILOT / f"KIDS-{short}" / "AUTHOR_NOTES.yaml", "\n".join(lines))


def write_manuscript(band_id: str, short: str, ages: str, spreads: list[dict]) -> dict:
    words_total = sum(len(s["words"].split()) for s in spreads)
    opener = {
        "BABY": "Follow gaze. Soft voice. Print-first. Stop anytime.",
        "TODDLER": "One focal object. Short phrases. Stop anytime.",
        "PRESCHOOL": "Story first. Notice before naming. Stop anytime.",
        "PREK": "Prediction before certainty. Stop anytime.",
        "ELEM1": "Observe before explaining. Portfolio over ranking. Stop anytime.",
        "ELEM2": "Separate observation from inference. Measure roughly. Stop anytime.",
    }[short]
    body = [
        f"# ONE TAP — {band_id} ({ages})",
        "",
        "```",
        *PROTOTYPE_BANNER.splitlines(),
        "```",
        "",
        "**Pilot concept:** Input → Response across devices and (sometimes) networks.",
        "**Concept ID:** `KCON-CH02-ONE-TAP`",
        "**Child validation:** none",
        "",
        "## Caregiver / educator note",
        "",
        opener,
        "",
    ]
    if short not in {"BABY", "TODDLER"}:
        body += [
            "## Cast (provisional — Character Bible Option A)",
            "",
            f"- Explorer: **{CAST['explorer']}** · Builder: **{CAST['builder']}** · "
            f"Instructions: **{CAST['instructions']}** · Signals: **{CAST['signals']}** · "
            f"Safety: **{CAST['safety']}**",
            f"- _{CAST['note']}_",
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
            f"**Try it:** {sp['action']}",
            "",
            f"**Talk together:** {sp['talk']}",
            "",
        ]
    body += [
        "## Facilitator pointer",
        "",
        "Editor, standards, and provenance notes live in `AUTHOR_NOTES.yaml` and `TRACEABILITY.yaml` — "
        "not in child-facing spreads.",
        "",
    ]
    write(PILOT / f"KIDS-{short}" / "MANUSCRIPT.md", "\n".join(body))
    return {"spreads": len(spreads), "words": words_total, "figures": len(spreads)}


def build_html(band_id: str, short: str, ages: str, spreads: list[dict]) -> None:
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        f"<title>ONE TAP {band_id} caregiver preview</title>",
        "<style>",
        "body{font-family:Georgia,serif;max-width:820px;margin:2rem auto;padding:0 1rem;background:#fffef8;color:#111;line-height:1.45;}",
        ".banner{border:3px solid #111;padding:1rem;margin-bottom:1.5rem;background:#f3f3f3;font-family:Helvetica,Arial,sans-serif;}",
        ".stop{position:sticky;top:0;z-index:2;background:#111;color:#fff;padding:.75rem 1rem;font-family:Helvetica,Arial,sans-serif;}",
        "img{max-width:100%;height:auto;border:1px solid #222;}",
        "figure{margin:2rem 0;} figcaption{font-size:.95rem;color:#333;}",
        "a:focus{outline:3px solid #005fcc;outline-offset:2px;}",
        "</style></head><body>",
        "<div class='stop'><a href='#end' style='color:#fff'>Easy exit / stop</a> · Autoplay: OFF · No data collection</div>",
        "<div class='banner' role='note'><pre style='margin:0;white-space:pre-wrap'>",
        PROTOTYPE_BANNER,
        "</pre></div>",
        f"<h1>ONE TAP — {band_id}</h1>",
        f"<p>Age guide: {ages}. Caregiver/educator preview. Not for unsupervised infant digital use as a product.</p>",
    ]
    for sp in spreads:
        # HTML lives in builds/; figures are sibling under band root
        src = f"../figures/FIG-ONE-TAP-{short}-{sp['id']}.svg"
        parts += [
            f"<figure id='{sp['id']}'>",
            f"<img src='{src}' alt=\"{sp['title']}: {sp['action']}\"/>",
            f"<figcaption><strong>{sp['id']} · {sp['title']}</strong><br/>{sp['words']}"
            f"<br/><em>Talk together:</em> {sp['talk']}</figcaption>",
            "</figure>",
        ]
    parts += [
        "<section id='end'><h2>End / stop</h2>"
        "<p>Close this preview anytime. No accounts. No tracking. "
        "Author notes are not shown in this child-safe preview.</p></section>",
        "</body></html>",
    ]
    write(PILOT / f"KIDS-{short}" / "builds" / "caregiver-preview.html", "\n".join(parts))


def build_pdf(band_id: str, short: str, ages: str, spreads: list[dict]) -> None:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

    out = PILOT / f"KIDS-{short}" / "builds" / f"ONE_TAP_{short}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out), pagesize=letter)
    w, h = letter

    def banner(cv):
        cv.setFont("Helvetica-Bold", 12)
        y = h - 0.7 * inch
        for line in PROTOTYPE_BANNER.splitlines():
            cv.drawString(0.75 * inch, y, line)
            y -= 14
        return y - 10

    y = banner(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.75 * inch, y, f"ONE TAP / INPUT→RESPONSE — {band_id}")
    y -= 22
    c.setFont("Helvetica", 11)
    c.drawString(0.75 * inch, y, f"Age guide: {ages}")
    y -= 16
    c.drawString(0.75 * inch, y, "Review prototype · style-neutral figures · not child-validated")
    c.showPage()

    for sp in spreads:
        y = banner(c)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(0.75 * inch, y, f"{sp['id']} — {sp['title']} ({sp['cadence']})")
        y -= 24
        c.setStrokeColorRGB(0.1, 0.1, 0.1)
        c.setLineWidth(2)
        c.circle(3.5 * inch, y - 0.9 * inch, 0.75 * inch)
        c.circle(3.5 * inch, y - 0.85 * inch, 0.1 * inch, fill=1)
        y -= 2.1 * inch
        c.setFont("Times-Roman", 11)
        for line in textwrap.wrap(sp["words"], 88):
            c.drawString(0.75 * inch, y, line)
            y -= 14
            if y < 1.4 * inch:
                c.showPage()
                y = banner(c)
        y -= 6
        c.setFont("Helvetica", 10)
        for line in textwrap.wrap(f"Try it: {sp['action']}", 95):
            c.drawString(0.75 * inch, y, line)
            y -= 12
        for line in textwrap.wrap(f"Talk together: {sp['talk']}", 95):
            c.drawString(0.75 * inch, y, line)
            y -= 12
        c.setFont("Helvetica", 8)
        c.drawString(
            0.75 * inch,
            0.55 * inch,
            f"FIG-ONE-TAP-{short}-{sp['id']} · CONCEPTUAL_EDUCATIONAL_PROTOTYPE",
        )
        c.showPage()

    y = banner(c)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.75 * inch, y, "Facilitator pointer")
    y -= 18
    c.setFont("Helvetica", 10)
    for line in [
        "Standards + provenance: AUTHOR_NOTES.yaml / TRACEABILITY.yaml",
        f"Adult main (provenance only): {ADULT_MAIN}",
        "No child validation evidence exists for this prototype.",
        "Claim ceiling: KIDS_REVIEW_PROTOTYPE_COMPLETE",
    ]:
        c.drawString(0.75 * inch, y, line)
        y -= 14
    c.save()


def write_reports(stats: dict) -> None:
    lines = [
        "# ONE TAP pilot report",
        "",
        "```",
        *PROTOTYPE_BANNER.splitlines(),
        "```",
        "",
        "## Claim ceiling",
        "",
        "**`KIDS_REVIEW_PROTOTYPE_COMPLETE`** for Track 3 (review-quality developmental prototypes).",
        "",
        "Not claimed: `KIDS_GLOBAL_FOUNDATION_AND_REVIEW_PROTOTYPE_COMPLETE` "
        "(standards research / global foundation remains a sister-track concern).",
        "",
        "## Provenance",
        "",
        f"- Adult main: `{ADULT_MAIN}`",
        f"- Integration base: `{INTEGRATION_BASE}`",
        f"- WAIKE main reconfirmed: `{WAIKE_SHA}`",
        "- Adult source chapter: CH02 (developmental rewrite)",
        f"- Character cast: provisional `{CAST['option']}`",
        "",
        "## Coverage",
        "",
        "| Band | Spreads | Words (child-facing) | Figures | HTML | PDF | AUTHOR_NOTES |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for band_id, short, _ in BANDS:
        s = stats[short]
        lines.append(
            f"| {band_id} | {s['spreads']} | {s['words']} | {s['figures']} | yes | yes | yes |"
        )
    lines += [
        "",
        "## Standards mappings",
        "",
        "Each spread `TRACEABILITY.yaml` entry uses **ADJACENT** fidelity with real atlas "
        "`atlas_mapping_ids` (early-years play/inquiry maps for Baby→Pre-K; CSTA/AC/NGSS-adjacent "
        "maps for Elem). `wire_registry_key` indexes `WIRE_HOOK_REGISTRY.yaml` only — it is **not** "
        "a substitute for atlas IDs.",
        "",
        "Honest gap statuses recorded at band level: `TRANSLATION_REQUIRED`, `VERSION_UNCLEAR`, `NO_MAP` "
        "(no fabricated EXACT official ONE TAP competency).",
        "",
        "**Stale contradiction fixed:** earlier report text claiming all spreads were `NOT_YET_MAPPED` "
        "with dangling `STD-WIRE-*` only is superseded.",
        "",
        "## Meta-text removals (out of child/caregiver body)",
        "",
    ]
    for m in META_REMOVED:
        lines.append(f"- {m}")
    lines += [
        "",
        "## Validation",
        "",
        "- Real SVG prototypes (no image placeholders)",
        "- Asset metadata + a11y title/desc",
        "- Traceability YAML per band with atlas mapping IDs",
        "- Prototype banners on manuscripts/HTML/PDF",
        "- Format truth vocabulary: `FORMAT_TRUTH_VOCABULARY.yaml`",
        "- `make kids-pilot-check` / `make kids-review-prototype-check`",
        "",
        "## Explicit non-claims",
        "",
        "- NOT CHILD-VALIDATED",
        "- NOT PUBLICATION-READY",
        "- NOT GLOBALLY_ALIGNED",
        "- No EPUB in this wave (justified deferral per format matrix)",
        "- No fabricated child testing / reader evidence",
        "",
    ]
    write(PILOT / "PILOT_REPORT.md", "\n".join(lines))

    write(
        PILOT / "README.md",
        f"""# ONE TAP / INPUT → RESPONSE pilot

```
{PROTOTYPE_BANNER}
```

Cross-age developmental rewrite of adult **CH02** (“Follow One Tap Through the Entire Stack”).

**Claim ceiling:** `KIDS_REVIEW_PROTOTYPE_COMPLETE`

| Band | Path |
| --- | --- |
| Baby | `KIDS-BABY/` |
| Toddler | `KIDS-TODDLER/` |
| Preschool | `KIDS-PRESCHOOL/` |
| Pre-K | `KIDS-PREK/` |
| Elem1 (K–2) | `KIDS-ELEM1/` |
| Elem2 (3–5/6) | `KIDS-ELEM2/` |

Each band includes: `MANUSCRIPT.md`, `AUTHOR_NOTES.yaml`, `TRACEABILITY.yaml`, `figures/*.svg` + `.meta.yaml`, `builds/caregiver-preview.html`, `builds/ONE_TAP_*.pdf`.

Shared: `FORMAT_TRUTH_VOCABULARY.yaml`, `PILOT_REPORT.md`.

**EPUB/fixed-layout:** deferred — PDF + HTML caregiver preview are the justified prototypes for this wave.
""",
    )


def build_all() -> dict:
    write_format_truth_vocab()
    stats = {}
    for band_id, short, ages in BANDS:
        spreads = spreads_for(short)
        fig_dir = PILOT / f"KIDS-{short}" / "figures"
        for i, sp in enumerate(spreads):
            svg_path = fig_dir / f"FIG-ONE-TAP-{short}-{sp['id']}.svg"
            write(svg_path, svg_for_spread(short, sp, i))
            write_asset_meta(short, sp, svg_path)
        write_traceability(band_id, short, spreads)
        write_author_notes(band_id, short, ages, spreads)
        stats[short] = write_manuscript(band_id, short, ages, spreads)
        build_html(band_id, short, ages, spreads)
        build_pdf(band_id, short, ages, spreads)
        write(
            PILOT / f"KIDS-{short}" / "README.md",
            f"# {band_id} ONE TAP review prototype\n\n```\n{PROTOTYPE_BANNER}\n```\n\n"
            f"- Spreads: {stats[short]['spreads']}\n"
            f"- Child-facing words: {stats[short]['words']}\n"
            f"- Figures: {stats[short]['figures']}\n"
            f"- AUTHOR_NOTES: `AUTHOR_NOTES.yaml`\n"
            f"- HTML: `builds/caregiver-preview.html`\n"
            f"- PDF: `builds/ONE_TAP_{short}.pdf`\n",
        )
    write_reports(stats)
    summary = {
        "claim_ceiling": "KIDS_REVIEW_PROTOTYPE_COMPLETE",
        "bands": stats,
        "meta_removed": META_REMOVED,
        "adult_main": ADULT_MAIN,
        "waike_sha": WAIKE_SHA,
    }
    write(PILOT / "build_summary.json", json.dumps(summary, indent=2))
    return summary


def main() -> None:
    summary = build_all()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
