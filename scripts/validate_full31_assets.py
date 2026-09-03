#!/usr/bin/env python3
"""Strict reader-facing Full31 asset/reference checks.

Fails when manuscript prose cites FIG-* or LAB-* that cannot resolve to a
live asset/package. Internal planned/blocked figures may exist in plans
only; FIG-CE3-009 must not appear as a live reader-facing figure ref.
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

FIG_RE = re.compile(r"\bFIG-[A-Z0-9-]+\b")
LAB_RE = re.compile(r"\bLAB-[A-Z0-9-]+\b")
PROPOSED_LAB_CONTEXT_RE = re.compile(
    r"(?i)(proposed|namespaced(?:-only)?|not\s+(?:a\s+)?(?:shipped|live|implemented)|"
    r"do\s+not\s+treat|not\s+mint|ideation\s+only|packet\s+opportunity|"
    r"until\s+(?:that\s+package|authored|published)|remains\s+a\s+packet|"
    r"inventing\s+a\s+duplicate|rather\s+than\s+inventing|"
    r"as\s+if\s+published|non-?claims?|explicit\s+non)",
)
META_RE = re.compile(
    r"(?i)\b(planned conceptual|planned comparative|future figure|figure to be added|"
    r"\[INSERT\]|\bTODO\b|\bTBD\b|vscode-file://|integrator merge|worktree|"
    r"Batch [123]\b|Wave 1\b)\b",
)


def _prose(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    return re.sub(r"```.*?```", "", text, flags=re.S)


def load_registry() -> dict[str, dict]:
    path = ROOT / "figures/figure_registry.yaml"
    doc = load_yaml(path) or {}
    out: dict[str, dict] = {}
    for item in doc.get("figures") or []:
        if not isinstance(item, dict):
            continue
        fid = str(item.get("figure_id") or item.get("id") or "").upper()
        if fid:
            out[fid] = item
    return out


def load_labs() -> set[str]:
    labs = ROOT / "labs"
    return {p.name for p in labs.iterdir() if p.is_dir() and p.name.startswith("LAB-")} if labs.is_dir() else set()


def find_a11y(fid: str, item: dict) -> Path | None:
    if item.get("accessibility"):
        p = ROOT / str(item["accessibility"])
        if p.exists():
            return p
    candidates = [
        ROOT / "figures/accessibility" / f"{fid.lower()}.yaml",
        ROOT / "figures/preproduction/accessibility" / f"{fid.lower()}.yaml",
    ]
    # CE aliases often keep CE a11y filenames
    m = re.match(r"FIG-CH(\d{2})-(\d{3})", fid)
    if m and int(m.group(1)) == 1:
        candidates.append(
            ROOT / "figures/preproduction/accessibility" / f"fig-ce1-{m.group(2)}.yaml"
        )
    if fid.startswith("FIG-CE"):
        slug = fid.lower().replace("fig-ce06-", "fig-ce06-").replace("fig-ce0", "fig-ce")
        # normalize FIG-CE06-001 -> fig-ce06-001, FIG-CE1-001 -> fig-ce1-001
        slug = fid.lower()
        candidates.append(ROOT / "figures/preproduction/accessibility" / f"{slug}.yaml")
        candidates.append(ROOT / "figures/accessibility" / f"{slug}.yaml")
    for c in candidates:
        if c.exists():
            return c
    return None


def validate_svg(path: Path, expected_id: str, errors: list[str], alias_ok: set[str] | None = None) -> None:
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        errors.append(f"{expected_id}: malformed SVG/XML at {path}: {exc}")
        return
    root = tree.getroot()
    title = root.find("{http://www.w3.org/2000/svg}title")
    if title is None:
        title = root.find("title")
    desc = root.find("{http://www.w3.org/2000/svg}desc")
    if desc is None:
        desc = root.find("desc")
    if title is None or not (title.text or "").strip():
        errors.append(f"{expected_id}: missing <title> in {path}")
    if desc is None or not (desc.text or "").strip():
        errors.append(f"{expected_id}: missing <desc> in {path}")
    data_id = root.attrib.get("data-figure-id")
    if data_id:
        allowed = {expected_id.upper()}
        if alias_ok:
            allowed |= {a.upper() for a in alias_ok}
        if data_id.upper() not in allowed:
            errors.append(
                f"{expected_id}: data-figure-id={data_id!r} disagrees with registry id "
                f"(allowed={sorted(allowed)})"
            )
    # Mid-word truncation: hyphenated cut mid-token, not deliberate em dash endings.
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag != "text" or not el.text:
            continue
        t = el.text.rstrip()
        if re.search(r"[A-Za-z]{3}-$", t):
            errors.append(f"{expected_id}: possible mid-word truncated text in {path}: {el.text!r}")


def alias_ids_for(fid: str, item: dict) -> set[str]:
    aliases: set[str] = set()
    note = str(item.get("note") or item.get("alias_of") or "")
    for m in re.finditer(r"FIG-[A-Z0-9-]+", note.upper()):
        aliases.add(m.group(0))
    if item.get("alias_of"):
        aliases.add(str(item["alias_of"]).upper())
    # CH01 figures are CE-1 aliases by convention
    m = re.match(r"FIG-CH01-(\d{3})", fid)
    if m:
        aliases.add(f"FIG-CE1-{m.group(1)}")
    return aliases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run checks (default)")
    args = parser.parse_args()
    del args

    errors: list[str] = []
    warnings: list[str] = []
    registry = load_registry()
    labs = load_labs()
    seen_paths: dict[str, str] = {}

    # duplicate IDs in registry
    # (dict already unique; also check path collisions)
    for fid, item in registry.items():
        path = item.get("path")
        if not path:
            # blocked internal entries may omit live path when status says blocked
            status = str(item.get("status") or item.get("truth_classification") or "").lower()
            if "block" in status:
                continue
            continue
        p = ROOT / str(path)
        key = str(path)
        if key in seen_paths and seen_paths[key] != fid:
            errors.append(f"duplicate asset path {path} for {seen_paths[key]} and {fid}")
        seen_paths[key] = fid

    for chapter in sorted((ROOT / "book/chapters").glob("ch*/chapter.md")):
        cid = chapter.parent.name.upper().replace("CH", "CH")
        prose = _prose(chapter.read_text(encoding="utf-8"))
        for m in META_RE.finditer(prose):
            errors.append(f"{chapter}: reader-facing production/meta-text: {m.group(0)!r}")
        if "FIG-CE3-009" in prose:
            errors.append(f"{chapter}: FIG-CE3-009 must not appear as a live reader-facing figure ref (BLOCKED_EVIDENCE_REQUIRED)")

        for fid in sorted(set(FIG_RE.findall(prose))):
            if fid.startswith("FIG-CE") and fid != "FIG-CE3-009":
                # CE figures must exist on disk/registry
                pass
            item = registry.get(fid)
            if item is None:
                # allow discovery via filesystem for CE aliases
                hits = list((ROOT / "figures").rglob(f"{fid.lower()}.svg"))
                if not hits:
                    # try fig-ch02-001-* pattern
                    m = re.match(r"FIG-CH(\d{2})-(\d{3})", fid)
                    if m:
                        hits = list((ROOT / "figures").rglob(f"fig-ch{m.group(1)}-{m.group(2)}*.svg"))
                if not hits:
                    errors.append(f"{chapter}: figure {fid} unregistered and no asset on disk")
                    continue
                # synthesize minimal item
                item = {"path": str(hits[0].relative_to(ROOT)), "status": "conceptual"}
            status = str(item.get("status") or item.get("truth_classification") or "").lower()
            if "block" in status or status == "blocked_evidence_required":
                errors.append(f"{chapter}: blocked figure {fid} cited as live reader asset")
                continue
            path = item.get("path")
            if not path:
                errors.append(f"{chapter}: figure {fid} registered without path for live embed")
                continue
            p = ROOT / str(path)
            if not p.exists():
                errors.append(f"{chapter}: figure {fid} asset missing: {path}")
                continue
            if p.suffix.lower() == ".svg":
                validate_svg(p, fid, errors, alias_ok=alias_ids_for(fid, item))
            a11y_path = find_a11y(fid, item)
            if a11y_path is None:
                errors.append(f"{chapter}: figure {fid} missing accessibility metadata")
            truth = str(item.get("truth_classification") or item.get("status") or "")
            if not truth:
                # CE filesystem fallback may lack registry row truth; default conceptual if asset exists
                if fid.startswith("FIG-CE") or fid.startswith("FIG-CH"):
                    truth = "conceptual"
                else:
                    errors.append(f"{chapter}: figure {fid} missing truth classification")
            if truth.lower() == "measured":
                if not item.get("evidence") and not item.get("evidence_note"):
                    errors.append(f"{chapter}: measured figure {fid} lacks evidence note")
            if truth.lower() in {"project_specific", "project-specific"}:
                note = str(item.get("evidence_note") or item.get("qualification") or item.get("note") or "")
                if "PHYSICAL_PENDING" not in note and "physical" not in note.lower():
                    if "pending" not in note.lower() and "teaching" not in note.lower():
                        warnings.append(
                            f"{chapter}: project-specific figure {fid} should qualify physical pending"
                        )

        for m in LAB_RE.finditer(prose):
            lab = m.group(0)
            if lab in labs:
                continue
            start = max(0, m.start() - 160)
            end = min(len(prose), m.end() + 160)
            if PROPOSED_LAB_CONTEXT_RE.search(prose[start:end]):
                continue
            errors.append(f"{chapter}: unknown lab {lab} (not under labs/ and not proposed-only)")

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(" ", w)
    if errors:
        print("ERRORS:")
        for e in errors:
            print(" ", e)
        print(f"FAIL: {len(errors)} asset/reference error(s)")
        return 1
    print("PASS: full31 reader-facing assets/references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
