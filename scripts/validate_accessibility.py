#!/usr/bin/env python3
"""Validate accessibility text against visible SVG structure."""
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
    prev = levels[0]
    for lv in levels[1:]:
        if lv > prev + 1:
            return False
        prev = lv
    return True


def svg_has_arrows(svg: str) -> bool:
    return ("marker-end=" in svg) and ("<line" in svg or "<path" in svg)


def svg_has_dashed(svg: str) -> bool:
    return "stroke-dasharray" in svg


def svg_has_stacked_bar(svg: str) -> bool:
    rects = re.findall(r"<rect\b", svg)
    return len(rects) >= 5 and ("stacked" in svg.lower() or "segment" in svg.lower())


def main() -> int:
    errors: list[str] = []
    for acc_path in sorted((ROOT / "figures/accessibility").glob("fig-ch02-*.yaml")):
        data = load_yaml(acc_path)
        for field in ("alt_text", "text_equivalent", "caption", "reading_order", "status"):
            if not data.get(field):
                errors.append(f"{acc_path.name}: missing {field}")
        src = ROOT / data.get("source", "")
        if not src.exists():
            errors.append(f"{acc_path.name}: missing source SVG {data.get('source')}")
            continue
        svg = src.read_text(encoding="utf-8")
        if not re.search(r"<title>.*?</title>", svg, flags=re.S):
            errors.append(f"{src.name}: missing <title>")
        desc = re.search(r"<desc>(.*?)</desc>", svg, flags=re.S)
        if not desc:
            errors.append(f"{src.name}: missing <desc>")
            continue
        combined = (
            desc.group(1).lower()
            + " "
            + str(data.get("text_equivalent", "")).lower()
            + " "
            + str(data.get("alt_text", "")).lower()
        )
        if re.search(r"\barrows?\b|message arrows|directional connectors", combined):
            if not svg_has_arrows(svg):
                errors.append(
                    f"{src.name}: accessibility claims arrows but SVG lacks arrow geometry"
                )
        if re.search(r"dashed|optional branch|optional network", combined):
            if not svg_has_dashed(svg):
                errors.append(
                    f"{src.name}: accessibility claims dashed/optional branch but SVG has no stroke-dasharray"
                )
        if re.search(r"stacked bar|adjacent rect", combined):
            if not svg_has_stacked_bar(svg):
                errors.append(
                    f"{src.name}: accessibility claims stacked bar but SVG lacks bar segments"
                )
        if "exploded" in combined and "fig-ch02-003" in src.name:
            if svg.count("<rect") + svg.count("<path") < 8:
                errors.append(f"{src.name}: claimed exploded view lacks sufficient shapes")
        if re.search(r"sequence diagram|lifelines|actor columns", combined) and "fig-ch02-002" in src.name:
            if svg.count("<line") < 8:
                errors.append(f"{src.name}: claimed sequence diagram lacks enough lines")

    ch2 = (ROOT / "book/chapters/ch02/chapter.md").read_text(encoding="utf-8")
    if not heading_hierarchy_ok(ch2):
        errors.append("CH02 heading hierarchy invalid")
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
