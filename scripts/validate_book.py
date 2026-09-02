#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REQUIRED_SECTIONS = [
    "The moment",
    "What you notice",
    "Exploded ecosystem",
    "Follow the signal",
    "Component cards",
    "Stability contract",
    "Try it",
    "Build it",
    "Secure and include it",
    "Career lens",
    "Check understanding",
    "Glossary links",
]


def main() -> int:
    errors: list[str] = []
    reg = load_yaml(ROOT / "book/chapter_registry.yaml")
    chapters = reg.get("chapters") or []
    if len(chapters) != 31:
        errors.append(f"expected 31 chapters, found {len(chapters)}")
    ids = [c.get("chapter_id") for c in chapters]
    if len(ids) != len(set(ids)):
        errors.append("duplicate chapter_id values")
    for c in chapters:
        cid = c["chapter_id"].lower()
        meta = ROOT / f"book/chapters/{cid}/metadata.yaml"
        body = ROOT / f"book/chapters/{cid}/chapter.md"
        if not meta.exists():
            errors.append(f"missing metadata for {cid}")
        if not body.exists():
            errors.append(f"missing chapter.md for {cid}")
    # CH02 completeness
    ch2 = (ROOT / "book/chapters/ch02/chapter.md").read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section.lower() not in ch2.lower():
            errors.append(f"CH02 missing section: {section}")
    paths = ["explorer", "operator", "builder", "engineer", "researcher", "educator"]
    meta2 = load_yaml(ROOT / "book/chapters/ch02/metadata.yaml")
    for p in paths:
        if p not in (meta2.get("reader_paths") or []):
            errors.append(f"CH02 metadata missing pathway {p}")
    ce = load_yaml(ROOT / "concept-edition/registry.yaml")
    if len(ce.get("modules") or []) != 6:
        errors.append("Concept Edition must list 6 modules")
    if errors:
        print("validate_book: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_book: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
