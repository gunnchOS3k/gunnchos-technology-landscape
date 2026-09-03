#!/usr/bin/env python3
"""Validate full31 chapter production registry completeness."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REGISTRY = ROOT / "publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml"
REPORT = ROOT / "publication/full31/FULL31_PROGRESS_REPORT.md"
PACKET_FILES = [
    "CHAPTER_BRIEF.md",
    "CONCEPT_GRAPH.yaml",
    "CLAIM_PLAN.yaml",
    "SOURCE_NEEDS.md",
    "FIGURE_PLAN.yaml",
    "LAB_OPPORTUNITIES.md",
    "GLOSSARY_CANDIDATES.yaml",
    "WAIKE_CROSSWALK.md",
    "DEPENDENCY_MAP.yaml",
]
REQUIRED_FIELDS = [
    "chapter_number",
    "chapter_id",
    "title",
    "part",
    "current_state",
    "canonical_prose_state",
    "concept_preproduction_state",
    "source_state",
    "claim_state",
    "figure_state",
    "lab_state",
    "glossary_state",
    "waike_state",
    "next_automatable_action",
    "packet_path",
]


def main() -> int:
    errors: list[str] = []
    if not REGISTRY.exists():
        print("validate_full31: FAIL")
        print(" - missing CHAPTER_PRODUCTION_REGISTRY.yaml")
        return 1
    if not REPORT.exists():
        errors.append("missing FULL31_PROGRESS_REPORT.md")

    doc = load_yaml(REGISTRY)
    if str(doc.get("schema_version")) != "1.0.0":
        errors.append(f"schema_version must be 1.0.0, got {doc.get('schema_version')!r}")
    gate = str(doc.get("gate_posture") or "")
    if gate != "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING":
        errors.append(f"gate_posture must remain READER_EVIDENCE_PENDING, got {gate!r}")
    if "PASS" in gate and "IN_PROGRESS" not in gate:
        errors.append("Gate 3 PASS is forbidden")

    chapters = doc.get("chapters") or []
    if len(chapters) != 31:
        errors.append(f"expected 31 chapters, found {len(chapters)}")

    nums = [int(c.get("chapter_number")) for c in chapters]
    ids = [c.get("chapter_id") for c in chapters]
    titles = [c.get("title") for c in chapters]
    if sorted(nums) != list(range(1, 32)):
        errors.append(f"chapter_number set must be 1..31, got {sorted(nums)}")
    if len(set(ids)) != len(ids):
        errors.append("duplicate chapter_id values")
    if len(set(titles)) != len(titles):
        errors.append("duplicate chapter titles")

    for ch in chapters:
        cid = ch.get("chapter_id")
        for field in REQUIRED_FIELDS:
            if field not in ch or ch.get(field) in (None, ""):
                errors.append(f"{cid}: missing {field}")
        action = str(ch.get("next_automatable_action") or "").strip()
        if not action:
            errors.append(f"{cid}: next_automatable_action empty")
        packet = ROOT / str(ch.get("packet_path") or "")
        if not packet.is_dir():
            errors.append(f"{cid}: packet_path missing directory {ch.get('packet_path')}")
            continue
        for rel in PACKET_FILES:
            if not (packet / rel).exists():
                errors.append(f"{cid}: missing packet file {rel}")

    report = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    if "GATE_3_IN_PROGRESS" not in report:
        errors.append("progress report must retain GATE_3_IN_PROGRESS")
    if "Gate 3 PASS" in report and "Never claim Gate 3 PASS" not in report:
        errors.append("progress report must not claim Gate 3 PASS")

    if errors:
        print("validate_full31: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_full31: PASS")
    print(f" - chapters={len(chapters)}")
    print(f" - gate={gate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
