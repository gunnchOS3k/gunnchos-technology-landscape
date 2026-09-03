#!/usr/bin/env python3
"""Generate deterministic Full31 manuscript inventory from chapter files."""
from __future__ import annotations

import argparse
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

FIG_RE = re.compile(r"\bFIG-[A-Z0-9-]+\b")
LAB_RE = re.compile(r"\bLAB-[A-Z0-9-]+\b")
CITATION_RE = re.compile(r"@([A-Za-z][A-Za-z0-9_:-]*(?:\.[A-Za-z0-9_:-]+)*)")
WORD_RE = re.compile(r"\b[\w']+\b")
PROPOSED_LAB_CONTEXT_RE = re.compile(
    r"(?i)(proposed|namespaced(?:-only)?|not\s+(?:a\s+)?(?:shipped|live|implemented)|"
    r"do\s+not\s+treat|not\s+mint|ideation\s+only|packet\s+opportunity|"
    r"until\s+(?:that\s+package|authored|published)|remains\s+a\s+packet|"
    r"inventing\s+a\s+duplicate|rather\s+than\s+inventing|"
    r"as\s+if\s+published|non-?claims?|explicit\s+non)",
)
META_RE = re.compile(
    r"(?i)planned conceptual|planned comparative|future figure|figure to be added|"
    r"\[INSERT\]|\bTODO\b|\bTBD\b|vscode-file://|integrator merge|worktree|Batch [123]\b|Wave 1\b"
)
PLACEHOLDER_RE = re.compile(r"\bTODO\b|\bTBD\b|\[INSERT[^\]]*\]", re.I)


def prose(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    return re.sub(r"```.*?```", "", text, flags=re.S)


def word_count(text: str) -> int:
    return len(WORD_RE.findall(prose(text)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if inventory stale")
    parser.add_argument(
        "--write",
        action="store_true",
        help="write publication/full31/FULL31_MANUSCRIPT_INVENTORY.md (+ yaml)",
    )
    args = parser.parse_args()
    if not args.check and not args.write:
        args.write = True

    registry = load_yaml(ROOT / "publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml") or {}
    chapters = registry.get("chapters") or []
    title_by = {
        int(c.get("chapter_number") or 0): str(c.get("title") or "")
        for c in chapters
        if isinstance(c, dict)
    }

    fig_reg = load_yaml(ROOT / "figures/figure_registry.yaml") or {}
    fig_ids = {
        str(i.get("figure_id") or i.get("id") or "").upper()
        for i in (fig_reg.get("figures") or [])
        if isinstance(i, dict)
    }
    labs = {
        p.name
        for p in (ROOT / "labs").iterdir()
        if p.is_dir() and p.name.startswith("LAB-")
    } if (ROOT / "labs").is_dir() else set()

    rows = []
    words = []
    for n in range(1, 32):
        path = ROOT / f"book/chapters/ch{n:02d}/chapter.md"
        meta = load_yaml(ROOT / f"book/chapters/ch{n:02d}/metadata.yaml") or {}
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        body = prose(text)
        wc = word_count(text) if text else 0
        words.append(wc)
        figs = sorted(set(FIG_RE.findall(body)))
        labrefs = sorted(set(LAB_RE.findall(body)))
        cites = CITATION_RE.findall(body)
        unresolved_figs = [f for f in figs if f not in fig_ids and not list((ROOT / "figures").rglob(f"{f.lower()}*.svg"))]
        # also try stem match
        unresolved_figs = []
        for f in figs:
            if f == "FIG-CE3-009":
                unresolved_figs.append(f)
                continue
            hits = list((ROOT / "figures").rglob(f"{f.lower()}.svg"))
            if not hits:
                m = re.match(r"FIG-CH(\d{2})-(\d{3})", f)
                if m:
                    hits = list((ROOT / "figures").rglob(f"fig-ch{m.group(1)}-{m.group(2)}*.svg"))
            if not hits and f not in fig_ids:
                unresolved_figs.append(f)
        unknown_labs = []
        for lab in labrefs:
            if lab in labs:
                continue
            # proposed-only mentions are not unresolved live assets
            proposed = False
            for m in LAB_RE.finditer(body):
                if m.group(0) != lab:
                    continue
                window = body[max(0, m.start() - 160) : min(len(body), m.end() + 160)]
                if PROPOSED_LAB_CONTEXT_RE.search(window):
                    proposed = True
                    break
            if not proposed:
                unknown_labs.append(lab)
        status = str(meta.get("manuscript_status") or meta.get("status") or "unknown")
        rows.append(
            {
                "id": f"CH{n:02d}",
                "title": title_by.get(n) or str(meta.get("title") or ""),
                "status": status,
                "words": wc,
                "citation_occurrences": len(cites),
                "unique_citation_keys": len(set(cites)),
                "figure_refs": len(figs),
                "figure_refs_list": figs,
                "resolved_figures": len(figs) - len(unresolved_figs),
                "unresolved_figures": unresolved_figs,
                "lab_refs": len(labrefs),
                "lab_refs_list": labrefs,
                "unknown_labs": unknown_labs,
                "try_it": bool(re.search(r"(?i)try it", body)),
                "build_it": bool(re.search(r"(?i)build it", body)),
                "placeholders": len(PLACEHOLDER_RE.findall(body)),
                "meta_findings": len(META_RE.findall(body)),
                "unresolved_reader_assets": len(unresolved_figs) + len(unknown_labs),
            }
        )

    total = sum(words)
    md_lines = [
        "# Full31 manuscript inventory",
        "",
        "Generated deterministically from `book/chapters/chNN/chapter.md`.",
        "Not a human validation report. Gate 3 remains READER_EVIDENCE_PENDING.",
        "",
        "## Word-count summary",
        "",
        f"- total: **{total}**",
        f"- min: **{min(words)}**",
        f"- max: **{max(words)}**",
        f"- mean: **{statistics.mean(words):.1f}**",
        f"- median: **{statistics.median(words):.1f}**",
        "",
        "Chapters under 2500 words (editorial review flag only):",
        "",
    ]
    short = [r for r in rows if r["words"] < 2500]
    if not short:
        md_lines.append("- none")
    else:
        for r in short:
            md_lines.append(f"- {r['id']}: {r['words']} words")
    md_lines += ["", "## Per-chapter", ""]
    for r in rows:
        md_lines += [
            f"### {r['id']} — {r['title']}",
            "",
            f"- status: `{r['status']}`",
            f"- words: {r['words']}",
            f"- citations: {r['citation_occurrences']} occurrences / {r['unique_citation_keys']} unique keys",
            f"- figures: {r['figure_refs']} refs / {r['resolved_figures']} resolved / unresolved={r['unresolved_figures'] or '[]'}",
            f"- labs: {r['lab_refs']} refs {r['lab_refs_list']}; unknown={r['unknown_labs'] or '[]'}",
            f"- Try It: {r['try_it']} · Build It: {r['build_it']}",
            f"- placeholders: {r['placeholders']} · meta findings: {r['meta_findings']} · unresolved reader assets: {r['unresolved_reader_assets']}",
            "",
        ]

    out_md = ROOT / "publication/full31/FULL31_MANUSCRIPT_INVENTORY.md"
    out_yaml = ROOT / "publication/full31/FULL31_MANUSCRIPT_INVENTORY.yaml"
    payload = {
        "schema_version": "1.0.0",
        "total_words": total,
        "word_min": min(words),
        "word_max": max(words),
        "word_mean": float(statistics.mean(words)),
        "word_median": float(statistics.median(words)),
        "chapters": rows,
    }

    # compact yaml without pyyaml dependency for write
    import json

    yaml_blob = "schema_version: \"1.0.0\"\n"
    yaml_blob += f"total_words: {total}\n"
    yaml_blob += f"word_min: {min(words)}\n"
    yaml_blob += f"word_max: {max(words)}\n"
    yaml_blob += f"word_mean: {statistics.mean(words):.2f}\n"
    yaml_blob += f"word_median: {statistics.median(words):.2f}\n"
    yaml_blob += "chapters:\n"
    for r in rows:
        yaml_blob += f"  - id: {r['id']}\n"
        yaml_blob += f"    title: {json.dumps(r['title'])}\n"
        yaml_blob += f"    status: {json.dumps(r['status'])}\n"
        yaml_blob += f"    words: {r['words']}\n"
        yaml_blob += f"    citation_occurrences: {r['citation_occurrences']}\n"
        yaml_blob += f"    unique_citation_keys: {r['unique_citation_keys']}\n"
        yaml_blob += f"    figure_refs: {r['figure_refs']}\n"
        yaml_blob += f"    resolved_figures: {r['resolved_figures']}\n"
        yaml_blob += f"    unresolved_figures: {json.dumps(r['unresolved_figures'])}\n"
        yaml_blob += f"    lab_refs: {r['lab_refs']}\n"
        yaml_blob += f"    unknown_labs: {json.dumps(r['unknown_labs'])}\n"
        yaml_blob += f"    try_it: {str(r['try_it']).lower()}\n"
        yaml_blob += f"    build_it: {str(r['build_it']).lower()}\n"
        yaml_blob += f"    placeholders: {r['placeholders']}\n"
        yaml_blob += f"    meta_findings: {r['meta_findings']}\n"
        yaml_blob += f"    unresolved_reader_assets: {r['unresolved_reader_assets']}\n"

    md_text = "\n".join(md_lines) + "\n"

    if args.check:
        if not out_md.exists() or not out_yaml.exists():
            print("FAIL: inventory files missing; run with --write")
            return 1
        if out_md.read_text(encoding="utf-8") != md_text:
            print("FAIL: FULL31_MANUSCRIPT_INVENTORY.md is stale")
            return 1
        if out_yaml.read_text(encoding="utf-8") != yaml_blob:
            print("FAIL: FULL31_MANUSCRIPT_INVENTORY.yaml is stale")
            return 1
        if any(r["unresolved_reader_assets"] for r in rows):
            print("FAIL: unresolved reader-facing assets remain")
            return 1
        print("PASS: manuscript inventory up to date")
        return 0

    out_md.write_text(md_text, encoding="utf-8")
    out_yaml.write_text(yaml_blob, encoding="utf-8")
    print(f"wrote {out_md}")
    print(f"wrote {out_yaml}")
    print(f"total_words={total} min={min(words)} max={max(words)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
