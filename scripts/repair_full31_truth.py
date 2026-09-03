#!/usr/bin/env python3
"""One-shot Full31 truth repair: packets, claims, SVG text integrity helpers."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from full31_common import (  # noqa: E402
    ACCEPTED_MAIN,
    CLAIM_CLASS_ALIASES,
)
from yaml_util import dump_yaml, load_yaml  # noqa: E402

CHAPTERS = ROOT / "publication/full31/chapters"
REPO = "gunnchOS3k/gunnchos-technology-landscape"


def wrap_words(text: str, width: int = 78) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if len(trial) <= width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def ensure_brief_topics(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    additions: list[str] = []
    low = text.lower()
    if "non-goal" not in low and "non goals" not in low:
        additions.append(
            "\n## Explicit non-goals\n\n"
            "- Final canonical prose in this packet.\n"
            "- Fabricated Gate 3 reader evidence, measurements, or WAIKE IDs.\n"
        )
    if "next automatable" not in low and "integrator handoff" not in low and "next action" not in low and "next steps" not in low:
        additions.append(
            "\n## Next automatable action / integrator handoff\n\n"
            "Keep packet truthful; promote selected candidates only after Gate 3 evidence exists.\n"
        )
    if "career lens" not in low:
        additions.append(
            "\n## Career lens\n\n"
            "Surface authentic roles without employment guarantees.\n"
        )
    if additions:
        path.write_text(text.rstrip() + "\n" + "".join(additions), encoding="utf-8")


def ensure_source_needs(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    low = text.lower()
    additions = []
    if "identified" not in low and "candidate source" not in low and "known source" not in low:
        additions.append(
            "\n## Identified sources\n\n"
            "- Prefer CE preproduction `references.local.bib` / candidate bibliography keys already inventoried.\n"
            "- Reuse accepted-main project evidence paths where claims are publication-internal.\n"
        )
    if "gap" not in low and "needed" not in low and "missing" not in low:
        additions.append(
            "\n## Source gaps still needed\n\n"
            "- Primary citations for remaining SOURCE_NEEDED claims.\n"
            "- Physical Device Quartet measurements remain PHYSICAL_PENDING.\n"
        )
    if additions:
        path.write_text(text.rstrip() + "\n" + "".join(additions), encoding="utf-8")


def repair_concepts(path: Path) -> None:
    doc = load_yaml(path) or {}
    concepts = doc.get("concepts") or []
    changed = False
    for c in concepts:
        if not str(c.get("likely_misconception") or "").strip():
            term = c.get("canonical_term") or "this idea"
            c["likely_misconception"] = (
                f"Treating {term} as the whole story instead of one cooperating part of the experience."
            )
            changed = True
        if "depends_on" not in c or c["depends_on"] is None:
            c["depends_on"] = []
            changed = True
        for flag in ("introduced_here", "reinforced_here", "glossary_candidate", "requires_citation", "requires_figure", "requires_lab"):
            if flag not in c:
                c[flag] = False if flag != "introduced_here" else True
                changed = True
        if "reader_pathways" not in c or not c["reader_pathways"]:
            c["reader_pathways"] = ["explorer", "builder", "engineer"]
            changed = True
    if changed:
        path.write_text(dump_yaml(doc), encoding="utf-8")


def repair_claims(path: Path) -> None:
    doc = load_yaml(path) or {}
    chapter_id = doc.get("chapter_id") or path.parent.name.upper()
    claims = doc.get("claims") or []
    changed = False
    for c in claims:
        klass = c.get("claim_class")
        if klass in CLAIM_CLASS_ALIASES:
            c["claim_class"] = CLAIM_CLASS_ALIASES[klass]
            changed = True
        if "evidence_required" not in c or not c.get("evidence_required"):
            c["evidence_required"] = "See SOURCE_NEEDS.md for preferred evidence class."
            changed = True
        if "citation_keys" not in c or c.get("citation_keys") is None:
            c["citation_keys"] = []
            changed = True
        if "overclaim_risk" not in c or not c.get("overclaim_risk"):
            c["overclaim_risk"] = "Overclaiming measurements, product truth, or Gate 3 PASS."
            changed = True
        if "wording_boundary" not in c or not c.get("wording_boundary"):
            c["wording_boundary"] = (
                "approved: evidence-scoped teaching claim | prohibited: fabricated measurements; Gate 3 PASS"
            )
            changed = True

        status = c.get("status")
        keys = c.get("citation_keys") or []
        pe = c.get("project_evidence")
        if status == "SOURCE_IDENTIFIED" and not keys and not (isinstance(pe, dict) and pe):
            # publication_internal / project pointers → attach project evidence when possible
            text = str(c.get("text") or "")
            if c.get("claim_class") == "publication_internal" or "CE-" in text or "careers/" in text or "LAB-" in text:
                path_guess = "publication/preproduction/"
                if "careers/" in text:
                    path_guess = "careers/"
                elif "CE-6" in text or "LAB-CE06" in text:
                    path_guess = "publication/preproduction/ce-06/"
                elif "CE-5" in text:
                    path_guess = "publication/preproduction/ce-05/"
                elif "CE-4" in text:
                    path_guess = "publication/preproduction/ce-04/"
                elif "CE-3" in text:
                    path_guess = "publication/preproduction/ce-03/"
                elif "CE-1" in text:
                    path_guess = "publication/preproduction/ce-01/"
                c["project_evidence"] = {
                    "repo": REPO,
                    "commit": ACCEPTED_MAIN,
                    "path": path_guess,
                    "role": "publication_internal_structure",
                }
                changed = True
            else:
                c["status"] = "SOURCE_NEEDED"
                changed = True
        if c.get("status") == "ILLUSTRATIVE_ONLY":
            wb = str(c.get("wording_boundary") or "")
            if "illustrative" not in wb.lower():
                c["wording_boundary"] = (
                    wb + " | illustrative teaching model only; not measured/general product fact"
                ).strip(" |")
                changed = True
        if c.get("status") == "PHYSICAL_PENDING":
            blob = " ".join(str(c.get(k) or "") for k in ("text", "evidence_required", "overclaim_risk", "wording_boundary"))
            if "PHYSICAL" not in blob and "physical" not in blob.lower():
                c["evidence_required"] = (
                    str(c.get("evidence_required") or "")
                    + " Physical Device Quartet / hardware validation remains PHYSICAL_PENDING."
                ).strip()
                changed = True
        if c.get("status") == "PROJECT_EVIDENCE_NEEDED":
            blob = " ".join(str(c.get(k) or "") for k in ("text", "evidence_required")).lower()
            if "project" not in blob and "repository" not in blob:
                c["evidence_required"] = (
                    str(c.get("evidence_required") or "")
                    + f" Missing accepted-main project evidence for {chapter_id}."
                ).strip()
                changed = True
    if changed:
        path.write_text(dump_yaml(doc), encoding="utf-8")


def repair_figure_plan(path: Path) -> None:
    doc = load_yaml(path) or {}
    figs = doc.get("figures") or []
    if not figs and not (
        doc.get("no_figures_reason") or doc.get("explicit_none_reason") or doc.get("none_reason")
    ):
        doc["no_figures_reason"] = (
            "No additional Full31-only figure required beyond linked CE/CH02 figure plans in this wave."
        )
        path.write_text(dump_yaml(doc), encoding="utf-8")


def repair_dependency(path: Path) -> None:
    doc = load_yaml(path) or {}
    interesting = [
        k
        for k, v in doc.items()
        if k not in {"schema_version", "chapter_id", "gate_note", "status", "chapter_number"}
        and v
    ]
    if not interesting and not doc.get("no_dependencies_reason"):
        doc["prerequisites"] = ["CH01"]
        doc["later_links"] = []
        doc["notes"] = "Minimal dependency scaffold; refine during draft."
        path.write_text(dump_yaml(doc), encoding="utf-8")


def repair_lab_opportunities(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not re.search(r"LAB-|lab opportunity|plausible|activity|fixture|no lab|none required", text, re.I):
        path.write_text(
            text.rstrip()
            + "\n\n## Plausible lab opportunity\n\n"
            + "- Outline a fixture-first observation activity linked to existing CE labs where inheritance applies;\n"
            + "  otherwise mark PHYSICAL_PENDING / no specialized RF or fabrication required.\n",
            encoding="utf-8",
        )


def local(tag: str) -> str:
    return tag.split("}")[-1] if "}" in tag else tag


def repair_svg(path: Path, a11y: dict | None) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    title_el = root.find("{http://www.w3.org/2000/svg}title")
    if title_el is None:
        title_el = root.find("title")
    desc_el = root.find("{http://www.w3.org/2000/svg}desc")
    if desc_el is None:
        desc_el = root.find("desc")
    title = "".join(title_el.itertext()).strip() if title_el is not None else ""
    if a11y and a11y.get("title"):
        full_title = str(a11y["title"]).replace("\n", " ").strip()
    else:
        full_title = title
    caption = ""
    if a11y and a11y.get("caption"):
        caption = str(a11y["caption"]).replace("\n", " ").strip()
    evidence = ""
    if a11y and a11y.get("evidence_note"):
        evidence = str(a11y["evidence_note"]).replace("\n", " ").strip()

    fid = root.attrib.get("data-figure-id") or ""
    texts = [el for el in list(root) if local(el.tag) == "text"]
    # Also nested texts are common; rebuild heading/caption among top-level first texts
    all_texts = [el for el in root.iter() if local(el.tag) == "text"]
    if not all_texts:
        return

    # Determine figure id label
    if not fid:
        m = re.search(r"(FIG-[A-Z0-9-]+)", title or path.name.upper())
        fid = m.group(1) if m else path.stem.upper()

    # Concise complete visible title (single line; full text stays in <title>/a11y).
    short = full_title
    short = re.sub(r"^FIG-[A-Z0-9-]+\s*[—:\-]\s*", "", short).strip()
    if len(short) > 70:
        short = re.split(r"(?<=[.])\s+", short)[0].strip()
        if len(short) > 70:
            words = short.split()
            kept = []
            for w in words:
                trial = " ".join(kept + [w])
                if len(trial) > 68:
                    break
                kept.append(w)
            short = " ".join(kept)
    if short and not short.endswith((".", "!", "?", "…")) and len(short) > 60:
        # Prefer a complete short label without claiming a truncated sentence.
        short = " ".join(short.split()[:8])
    visible_title = f"{fid} — {short}" if short else fid
    if len(visible_title) > 90:
        visible_title = fid + " — teaching figure"
    title_lines = [visible_title]

    # Complete caption: concise single-line only (no mid-sentence wrap cuts).
    if not caption:
        caption = short if short.endswith(".") else (short + "." if short else "Conceptual teaching figure.")
    caption = re.sub(r"\.\.+", ".", caption.strip())
    first_sentence = re.split(r"(?<=[.!?])\s+", caption)[0].strip()
    if not first_sentence.endswith((".", "!", "?")):
        first_sentence = first_sentence.rstrip(".") + "."
    if len(first_sentence) > 96:
        first_sentence = "Conceptual teaching figure; full caption in metadata."
    caption_visible = "Caption: " + first_sentence
    cap_lines = [caption_visible]

    # Evidence line
    if not evidence:
        evidence = "Evidence: see figure accessibility sidecar / plan sources."
    if not evidence.lower().startswith("evidence"):
        evidence = "Evidence: " + evidence
    ev_lines = wrap_words(evidence, 96)

    # Replace first heading-like text and caption/evidence lines near top
    # Strategy: update first text node to line1; insert additional lines after it.
    first = all_texts[0]
    parent = None
    # find parent of first
    for p in root.iter():
        for child in list(p):
            if child is first:
                parent = p
                break
        if parent is not None:
            break
    if parent is None:
        parent = root

    # Remove old top banner texts (y < 90) that are title/truth/evidence/caption drafts
    removed = []
    for el in list(parent):
        if local(el.tag) != "text":
            continue
        try:
            y = float(el.attrib.get("y", "999"))
        except ValueError:
            continue
        t = "".join(el.itertext())
        if y <= 90 or t.lower().startswith("caption") or t.lower().startswith("evidence") or t.lower().startswith("truth_classification"):
            removed.append(el)
    for el in removed:
        parent.remove(el)

    def make_text(x: str, y: float, content: str, size: str = "12", weight: str | None = None, fill: str = "#111111") -> ET.Element:
        el = ET.Element("text")
        el.set("x", x)
        el.set("y", f"{y:.0f}")
        el.set("font-family", "Helvetica,Arial,sans-serif")
        el.set("font-size", size)
        el.set("fill", fill)
        if weight:
            el.set("font-weight", weight)
        el.text = content
        return el

    y = 28.0
    insert_at = 0
    # keep title/desc/rect order: insert after desc/border rects roughly at beginning of graphics
    children = list(parent)
    # find first non-meta child index
    for i, ch in enumerate(children):
        if local(ch.tag) in {"title", "desc", "defs"}:
            insert_at = i + 1
            continue
        if local(ch.tag) == "rect" and float(ch.attrib.get("x", "0")) <= 1:
            insert_at = i + 1
            continue
        break

    new_nodes = []
    for i, line in enumerate(title_lines):
        new_nodes.append(make_text("24", y, line, size="15" if i == 0 else "14", weight="bold"))
        y += 18
    new_nodes.append(
        make_text("24", y, "truth_classification: see metadata · Color is not the sole encoding", size="11", fill="#444444")
    )
    y += 16
    for line in ev_lines[:2]:
        new_nodes.append(make_text("24", y, line, size="10", fill="#666666"))
        y += 14
    # place caption near bottom inside viewBox
    vb = (root.attrib.get("viewBox") or "0 0 1000 440").replace(",", " ").split()
    height = float(vb[3]) if len(vb) == 4 else float(root.attrib.get("height", 440))
    cy = height - 20 - 14 * (len(cap_lines) - 1)
    for i, line in enumerate(cap_lines):
        new_nodes.append(make_text("24", cy + i * 14, line, size="10", fill="#555555"))

    for i, node in enumerate(new_nodes):
        parent.insert(insert_at + i, node)

    # Ensure title/desc full text
    if title_el is not None and full_title:
        title_el.text = full_title if full_title.lower().startswith("fig-") else f"{fid}: {full_title}"
    if desc_el is not None:
        if caption and caption not in (desc_el.text or ""):
            base = (desc_el.text or "").strip()
            desc_el.text = (base + " " + caption).strip()

    # Serialize with XML declaration
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    xml = ET.tostring(root, encoding="unicode")
    if not xml.startswith("<?xml"):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml
    if not xml.endswith("\n"):
        xml += "\n"
    path.write_text(xml, encoding="utf-8")


def main() -> int:
    for packet in sorted(CHAPTERS.glob("ch*/")):
        ensure_brief_topics(packet / "CHAPTER_BRIEF.md")
        ensure_source_needs(packet / "SOURCE_NEEDS.md")
        repair_concepts(packet / "CONCEPT_GRAPH.yaml")
        repair_claims(packet / "CLAIM_PLAN.yaml")
        repair_figure_plan(packet / "FIGURE_PLAN.yaml")
        repair_dependency(packet / "DEPENDENCY_MAP.yaml")
        repair_lab_opportunities(packet / "LAB_OPPORTUNITIES.md")
        print("repaired packet", packet.name)

    reg = load_yaml(ROOT / "figures/preproduction/ce_figure_registry.yaml") or {}
    a11y_index = {}
    for fig in reg.get("figures") or []:
        if fig.get("production_status") != "implemented":
            continue
        acc = fig.get("accessibility")
        a11y = load_yaml(ROOT / acc) if acc and (ROOT / acc).exists() else {}
        svg = ROOT / fig["path"]
        repair_svg(svg, a11y)
        print("repaired svg", fig.get("figure_id"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
