#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402


def heading_hierarchy_ok(text: str) -> bool:
    levels = [len(m.group(1)) for m in re.finditer(r"^(#{1,6})\s", text, flags=re.M)]
    if not levels:
        return False
    # allow starting at 1; no jumps greater than +1 from previous min trajectory
    prev = levels[0]
    for lv in levels[1:]:
        if lv > prev + 1:
            return False
        prev = lv
    return True


def main() -> int:
    errors: list[str] = []
    # figures
    for acc in (ROOT / "figures/accessibility").glob("*.yaml"):
        data = load_yaml(acc)
        if not data.get("alt_text") or not data.get("text_equivalent"):
            errors.append(f"{acc.name}: missing alt/text equivalent")
        if not data.get("reading_order"):
            errors.append(f"{acc.name}: missing reading_order")
    ch2 = (ROOT / "book/chapters/ch02/chapter.md").read_text(encoding="utf-8")
    if not heading_hierarchy_ok(ch2):
        errors.append("CH02 heading hierarchy invalid")
    # descriptive links heuristic: discourage [click here]
    if re.search(r"\[click here\]", ch2, flags=re.I):
        errors.append("CH02 contains non-descriptive 'click here' link text")
    print("NOTE: automated accessibility checks cannot certify WCAG conformance.")
    if errors:
        print("validate_accessibility: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_accessibility: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
