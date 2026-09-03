#!/usr/bin/env python3
"""Visual text-integrity checks for implemented CE preproduction SVGs.

Fails on:
  - missing <title>/<desc>
  - mid-word heading cuts vs metadata title
  - mid-sentence caption slicing
  - text clearly outside viewBox (basic geometry)
  - missing evidence note markers for implemented figures
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REG_PATH = ROOT / "figures/preproduction/ce_figure_registry.yaml"
NS = {"svg": "http://www.w3.org/2000/svg"}


def local(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def text_content(el: ET.Element) -> str:
    return "".join(el.itertext()).strip()


def parse_viewbox(root: ET.Element) -> tuple[float, float, float, float]:
    vb = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if vb:
        parts = [float(x) for x in vb.replace(",", " ").split()]
        if len(parts) == 4:
            return parts[0], parts[1], parts[2], parts[3]
    w = float(root.attrib.get("width", "1000"))
    h = float(root.attrib.get("height", "600"))
    return 0.0, 0.0, w, h


def estimate_text_width(s: str, size: float) -> float:
    # Helvetica-ish average width factor
    return max(0.0, len(s) * size * 0.55)


def midword_cut(visible: str, full: str) -> bool:
    """True if visible is a proper prefix of full that ends mid-word."""
    v = visible.strip()
    f = full.strip()
    if not v or not f:
        return False
    # strip figure id prefixes from visible
    v2 = re.sub(r"^FIG-[A-Z0-9-]+\s*[—:\-]\s*", "", v).strip()
    f2 = re.sub(r"^FIG-[A-Z0-9-]+\s*[—:\-]\s*", "", f).strip()
    if not v2:
        return False
    if f2.startswith(v2) and len(v2) < len(f2):
        nxt = f2[len(v2) : len(v2) + 1]
        if nxt and nxt.isalnum() and v2[-1].isalnum():
            return True
    # also catch ellipsis truncation markers mid-token
    if v2.endswith("…") or v2.endswith("..."):
        core = v2.rstrip("….").rstrip()
        if core and f2.startswith(core) and len(core) < len(f2) - 1:
            nxt = f2[len(core) : len(core) + 1]
            if nxt.isalnum() and core[-1].isalnum():
                return True
    return False


def caption_mid_sentence(caption: str) -> bool:
    c = caption.strip()
    if not c.lower().startswith("caption"):
        return False
    if len(c) < 24:
        return False
    # Accept complete terminal punctuation.
    if c.endswith((".", "!", "?", "…")):
        return False
    return True


def main() -> int:
    errors: list[str] = []
    if not REG_PATH.exists():
        print("validate_visual_text_integrity: FAIL")
        print(f" - missing {REG_PATH}")
        return 1
    reg = load_yaml(REG_PATH) or {}
    figures = [f for f in (reg.get("figures") or []) if f.get("production_status") == "implemented"]

    for fig in figures:
        fid = fig.get("figure_id") or "<no-id>"
        rel = fig.get("path")
        if not rel:
            errors.append(f"{fid}: implemented without path")
            continue
        path = ROOT / rel
        if not path.exists():
            errors.append(f"{fid}: missing SVG {rel}")
            continue
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as exc:
            errors.append(f"{fid}: malformed SVG: {exc}")
            continue

        title_el = root.find("svg:title", NS)
        desc_el = root.find("svg:desc", NS)
        if title_el is None:
            title_el = root.find("title")
        if desc_el is None:
            desc_el = root.find("desc")
        title = text_content(title_el) if title_el is not None else ""
        desc = text_content(desc_el) if desc_el is not None else ""
        if not title:
            errors.append(f"{fid}: missing <title>")
        if not desc:
            errors.append(f"{fid}: missing <desc>")

        vb_x, vb_y, vb_w, vb_h = parse_viewbox(root)
        texts = [el for el in root.iter() if local(el.tag) == "text"]
        if not texts:
            errors.append(f"{fid}: no visible <text> nodes")
            continue

        heading = text_content(texts[0])
        if title and midword_cut(heading, title):
            errors.append(f"{fid}: mid-word heading cut in visible title: {heading!r}")

        for el in texts:
            t = text_content(el)
            if t.lower().startswith("caption") and caption_mid_sentence(t):
                errors.append(f"{fid}: mid-sentence caption slicing: {t[-80:]!r}")
            # outside viewBox (basic)
            try:
                x = float(el.attrib.get("x", "0"))
                y = float(el.attrib.get("y", "0"))
            except ValueError:
                continue
            size = float(el.attrib.get("font-size", "12"))
            anchor = el.attrib.get("text-anchor", "start")
            width = estimate_text_width(t, size)
            if anchor == "middle":
                left, right = x - width / 2, x + width / 2
            elif anchor == "end":
                left, right = x - width, x
            else:
                left, right = x, x + width
            if y < vb_y - 2 or y > vb_y + vb_h + 2:
                errors.append(f"{fid}: text y outside viewBox ({y})")
            # Only enforce x-extent for banner/caption lines near edges; body labels may be tight.
            if y <= 100 or t.lower().startswith("caption") or t.lower().startswith("evidence"):
                if left < vb_x - 8 or right > vb_x + vb_w + 8:
                    errors.append(f"{fid}: text x-extent outside viewBox ({t[:40]!r})")

        blob = ET.tostring(root, encoding="unicode")
        if "Evidence:" not in blob and "evidence" not in blob.lower():
            # evidence note may live only in desc; require desc mention or visible Evidence
            if "evidence" not in desc.lower() and "PHYSICAL_PENDING" not in blob:
                errors.append(f"{fid}: missing legible evidence note")
        if "color is not the sole encoding" not in blob.lower() and "not the sole encoding" not in blob.lower():
            # color-only risk marker expected in CE visual system
            if "stroke-dasharray" not in blob and "marker-end" not in blob:
                errors.append(f"{fid}: no non-color encoding marker found")

        # stable ID unchanged
        if fid not in blob:
            errors.append(f"{fid}: stable figure id missing from SVG markup")

    # FIG-CE3-009 must remain blocked
    blocked = [f for f in (reg.get("figures") or []) if f.get("figure_id") == "FIG-CE3-009"]
    if not blocked:
        errors.append("FIG-CE3-009 missing from registry")
    else:
        b = blocked[0]
        if b.get("production_status") != "blocked" or b.get("block_reason") != "BLOCKED_EVIDENCE_REQUIRED":
            errors.append("FIG-CE3-009 must remain BLOCKED_EVIDENCE_REQUIRED")
        if b.get("path"):
            errors.append("FIG-CE3-009 blocked measured figure must not ship SVG path")

    if errors:
        print("validate_visual_text_integrity: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_visual_text_integrity: PASS")
    print(f" - implemented_checked={len(figures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
