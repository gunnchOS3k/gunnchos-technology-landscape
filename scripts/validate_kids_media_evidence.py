#!/usr/bin/env python3
"""Validate Kids Edition child-media evidence/source registers and design artifacts.

Meaningful checks (not a hollow make target):
- required files exist
- YAML parses
- mandatory evidence topics covered
- evidence source IDs resolve to source register
- adopted rules and rejected claims present
- age-band docs exist for all six bands
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

MANDATORY_TOPICS = {
    "infant_visual_attention",
    "color_contrast",
    "visual_clutter",
    "shape_complexity",
    "child_directed_speech",
    "pitch_contour",
    "speaking_rate",
    "repetition",
    "pause_response_cadence",
    "repeated_exposure",
    "songs_rhyme",
    "memory_word_learning",
    "stable_characters",
    "parasocial_character_learning",
    "participatory_prompts",
    "caregiver_co_use",
    "serve_and_return",
    "pacing",
    "fast_fantastical_media",
    "attention_vs_learning",
    "child_centered_digital_design",
    "autoplay_infinite_engagement",
    "privacy_and_agency",
}

AGE_BANDS = [
    "KIDS-BABY",
    "KIDS-TODDLER",
    "KIDS-PRESCHOOL",
    "KIDS-PREK",
    "KIDS-ELEM1",
    "KIDS-ELEM2",
]

REQUIRED_FILES = [
    "kids/00_KIDS_PUBLICATION_FAMILY_CHARTER.md",
    "kids/research/CHILD_MEDIA_EVIDENCE_REGISTER.yaml",
    "kids/research/CHILD_MEDIA_SOURCE_REGISTER.yaml",
    "kids/research/CHILD_MEDIA_RESEARCH_REPORT.md",
    "kids/design/CHILD_CENTERED_MEDIA_POLICY.md",
    "kids/design/KIDS_VISUAL_SYSTEM.md",
    "kids/design/KIDS_AUDIO_PROSODY_GUIDE.md",
    "kids/design/KIDS_ACCESSIBILITY_REQUIREMENTS.md",
    "kids/characters/CHARACTER_BIBLE.md",
    "kids/caregivers/CAREGIVER_GUIDE_SYSTEM.md",
    "kids/publication/KIDS_FORMAT_MATRIX.yaml",
    "kids/multilingual/MULTILINGUAL_ARCHITECTURE.md",
]

EVIDENCE_REQUIRED_KEYS = {
    "evidence_id",
    "topic",
    "age_range",
    "source_type",
    "source",
    "year",
    "sample_or_scope",
    "finding",
    "implementation_implication",
    "limitations",
    "confidence",
}


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    for band in AGE_BANDS:
        p = ROOT / "kids" / "age-bands" / f"{band}.md"
        if not p.is_file():
            errors.append(f"missing age-band doc: {p.relative_to(ROOT)}")

    if errors:
        # still try YAML if present
        pass

    evidence_path = ROOT / "kids/research/CHILD_MEDIA_EVIDENCE_REGISTER.yaml"
    source_path = ROOT / "kids/research/CHILD_MEDIA_SOURCE_REGISTER.yaml"
    matrix_path = ROOT / "kids/publication/KIDS_FORMAT_MATRIX.yaml"

    sources = {}
    if source_path.is_file():
        src_data = load_yaml(source_path) or {}
        for s in src_data.get("sources") or []:
            sid = s.get("source_id")
            if not sid:
                errors.append("source entry missing source_id")
            elif sid in sources:
                errors.append(f"duplicate source_id: {sid}")
            else:
                sources[sid] = s
                for key in ("authority", "title", "url", "retrieved_on", "allowed_use"):
                    if not s.get(key):
                        errors.append(f"{sid}: missing {key}")

    topics_found: set[str] = set()
    evidence_ids: set[str] = set()
    if evidence_path.is_file():
        ev_data = load_yaml(evidence_path) or {}
        entries = ev_data.get("evidence") or []
        if len(entries) < len(MANDATORY_TOPICS):
            errors.append(
                f"evidence entries ({len(entries)}) fewer than mandatory topics ({len(MANDATORY_TOPICS)})"
            )
        for e in entries:
            eid = e.get("evidence_id")
            if not eid:
                errors.append("evidence entry missing evidence_id")
                continue
            if eid in evidence_ids:
                errors.append(f"duplicate evidence_id: {eid}")
            evidence_ids.add(eid)
            missing = EVIDENCE_REQUIRED_KEYS - set(e)
            if missing:
                errors.append(f"{eid}: missing keys {sorted(missing)}")
            topic = e.get("topic")
            if topic:
                topics_found.add(topic)
            src = e.get("source")
            if src and src not in sources and not str(src).startswith("SRC-"):
                errors.append(f"{eid}: source {src} not in source register")
            elif src and src not in sources:
                errors.append(f"{eid}: source_id {src} not found in source register")
            conf = e.get("confidence")
            if conf not in {"high", "medium", "low", "provisional"}:
                errors.append(f"{eid}: invalid confidence {conf!r}")

        missing_topics = sorted(MANDATORY_TOPICS - topics_found)
        if missing_topics:
            errors.append(f"mandatory topics missing coverage: {missing_topics}")

        rules = ev_data.get("adopted_production_rules") or []
        if len(rules) < 5:
            errors.append("expected at least 5 adopted_production_rules")
        rejected = ev_data.get("rejected_unsupported_claims") or []
        if len(rejected) < 4:
            errors.append("expected at least 4 rejected_unsupported_claims")
        # Spot-check prohibited claim themes mentioned
        blob = " ".join((r.get("claim") or "") for r in rejected).lower()
        for needle in ("432", "color activates", "high pitch"):
            if needle not in blob:
                errors.append(f"rejected claims should mention theme: {needle}")

    if matrix_path.is_file():
        matrix = load_yaml(matrix_path) or {}
        bands = {b.get("age_band") for b in (matrix.get("bands") or [])}
        for band in AGE_BANDS:
            if band not in bands:
                errors.append(f"format matrix missing age_band: {band}")
        # Board book vendor honesty
        text = matrix_path.read_text(encoding="utf-8")
        if "EXTERNAL_PRINT_VENDOR_REQUIRED" not in text:
            errors.append("format matrix must mark EXTERNAL_PRINT_VENDOR_REQUIRED for board books")

    # Character bible must offer multiple options without final lock language as done
    bible = ROOT / "kids/characters/CHARACTER_BIBLE.md"
    if bible.is_file():
        bt = bible.read_text(encoding="utf-8")
        if "Option A" not in bt or "Option B" not in bt:
            errors.append("CHARACTER_BIBLE.md must include at least Option A and Option B")
        if "no final" not in bt.lower() and "no IP lock" not in bt.lower() and "without owner" not in bt.lower():
            errors.append("CHARACTER_BIBLE.md must state no final IP lock without owner")

    # Multilingual honesty
    multi = ROOT / "kids/multilingual/MULTILINGUAL_ARCHITECTURE.md"
    if multi.is_file():
        mt = multi.read_text(encoding="utf-8")
        if "MT_DRAFT_UNVALIDATED" not in mt and "machine-translate" not in mt.lower():
            errors.append("multilingual architecture must forbid fake validated MT")

    if errors:
        print("kids-media-evidence-check: FAIL")
        for err in errors:
            print(" -", err)
        return 1

    print("kids-media-evidence-check: PASS")
    print(f" - sources: {len(sources)}")
    print(f" - evidence entries: {len(evidence_ids)}")
    print(f" - mandatory topics covered: {len(topics_found & MANDATORY_TOPICS)}/{len(MANDATORY_TOPICS)}")
    print(f" - age bands: {len(AGE_BANDS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
