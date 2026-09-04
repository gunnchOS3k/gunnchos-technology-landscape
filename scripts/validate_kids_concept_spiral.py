#!/usr/bin/env python3
"""Validate Kids 31→7 concept spiral completeness."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SPIRAL = ROOT / "kids" / "concepts" / "ADULT31_TO_KIDS_SPIRAL.yaml"
REQUIRED_STRANDS = {
    "STRAND-ME-TECH",
    "STRAND-INSIDE",
    "STRAND-INSTRUCTIONS",
    "STRAND-MESSAGES",
    "STRAND-DATA",
    "STRAND-SAFE",
    "STRAND-BUILD",
}
AGE_FIELDS = [
    "baby_representation",
    "toddler_representation",
    "preschool_representation",
    "prek_representation",
    "elem1_representation",
    "elem2_representation",
]


def main() -> int:
    errors: list[str] = []
    if not SPIRAL.is_file():
        print(f"FAIL: missing {SPIRAL}")
        return 1
    data = yaml.safe_load(SPIRAL.read_text(encoding="utf-8"))
    concepts = data.get("concepts") or []
    if len(concepts) != 31:
        errors.append(f"expected 31 concepts, found {len(concepts)}")

    chapters = set()
    strands_seen = set()
    for c in concepts:
        cid = c.get("concept_id")
        for field in AGE_FIELDS + ["kids_strand", "adult_chapters"]:
            if not c.get(field):
                errors.append(f"{cid}: missing {field}")
        strand = c.get("kids_strand")
        strands_seen.add(strand)
        if strand not in REQUIRED_STRANDS:
            errors.append(f"{cid}: unknown strand {strand}")
        for ch in c.get("adult_chapters") or []:
            chapters.add(ch)
        # precursor honesty: baby text should not dump adult jargon piles
        baby = (c.get("baby_representation") or "").lower()
        banned = ["packet routing", "event loop", "system-on-chip", "virtualization"]
        for b in banned:
            if b in baby:
                errors.append(f"{cid}: baby_representation contains advanced term '{b}'")

    expected_ch = {f"CH{i:02d}" for i in range(1, 32)}
    missing = sorted(expected_ch - chapters)
    extra = sorted(chapters - expected_ch)
    if missing:
        errors.append(f"missing adult chapters: {missing}")
    if extra:
        errors.append(f"unexpected adult chapters: {extra}")
    if strands_seen != REQUIRED_STRANDS:
        errors.append(f"strand coverage mismatch: {sorted(strands_seen)}")

    if data.get("meta", {}).get("publication_ready") is True:
        errors.append("publication_ready must not be true")
    if data.get("meta", {}).get("child_validation") not in (None, "NONE", False, "none"):
        # allow NONE string
        cv = data.get("meta", {}).get("child_validation")
        if str(cv).upper() not in {"NONE", "FALSE", "0"}:
            errors.append(f"child_validation overclaim: {cv}")

    if errors:
        print("kids-concept-spiral-check FAIL")
        for e in errors:
            print(f" - {e}")
        return 1
    print("kids-concept-spiral-check PASS")
    print(f" concepts=31 strands={len(strands_seen)} chapters=31")
    return 0


if __name__ == "__main__":
    sys.exit(main())
