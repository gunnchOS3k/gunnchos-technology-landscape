#!/usr/bin/env python3
"""Validate ONE TAP kids review-prototype quality gates (Track 3)."""
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
PILOT = ROOT / "kids" / "pilots" / "ONE_TAP"
ATLAS = ROOT / "kids" / "standards" / "GLOBAL_STANDARDS_ATLAS.yaml"
BANDS = ["BABY", "TODDLER", "PRESCHOOL", "PREK", "ELEM1", "ELEM2"]
BANNER_LINES = [
    "KIDS DEVELOPMENTAL PROTOTYPE",
    "NOT CHILD-VALIDATED",
    "NOT PUBLICATION-READY",
]
FORBIDDEN_BODY = re.compile(
    r"Use pilot figure|No false GHz|Link to adult CH02|Honesty label required|"
    r"NOT_YET_MAPPED|sentence simplification|82284cd8f41d750ff508cd6ea5bad0a9534d8162",
    re.I,
)
PLACEHOLDER_RE = re.compile(r"image here|TODO_IMAGE|lorem ipsum|IMAGE HERE", re.I)
MIN_WORDS = {
    "BABY": 8,
    "TODDLER": 20,
    "PRESCHOOL": 60,
    "PREK": 80,
    "ELEM1": 400,
    "ELEM2": 800,
}
MAX_WORDS = {
    "BABY": 40,  # developmental restraint
    "TODDLER": 80,
}


def load_atlas_ids() -> set[str]:
    text = ATLAS.read_text(encoding="utf-8")
    return set(re.findall(r"mapping_id:\s*(MAP-[A-Z0-9-]+)", text))


def child_facing_words(ms: Path) -> int:
    text = ms.read_text(encoding="utf-8")
    words: list[str] = []
    for m in re.finditer(r"\*\*Child-facing text:\*\*\s*(.+?)(?=\n\n|\n\*\*|$)", text, re.S):
        words.extend(m.group(1).split())
    return len(words)


def main() -> int:
    errors: list[str] = []
    if not PILOT.is_dir():
        print(f"FAIL: missing {PILOT}")
        return 1

    atlas_ids = load_atlas_ids()
    if len(atlas_ids) < 5:
        errors.append("atlas mapping IDs could not be loaded")

    fmt = PILOT / "FORMAT_TRUTH_VOCABULARY.yaml"
    if not fmt.is_file():
        errors.append("missing FORMAT_TRUTH_VOCABULARY.yaml")
    else:
        ft = yaml.safe_load(fmt.read_text(encoding="utf-8"))
        if not (ft or {}).get("bands"):
            errors.append("FORMAT_TRUTH_VOCABULARY missing bands")

    report = PILOT / "PILOT_REPORT.md"
    if not report.is_file():
        errors.append("missing PILOT_REPORT.md")
    else:
        rt = report.read_text(encoding="utf-8")
        if "KIDS_REVIEW_PROTOTYPE_COMPLETE" not in rt:
            errors.append("PILOT_REPORT missing KIDS_REVIEW_PROTOTYPE_COMPLETE claim ceiling")
        if "KIDS_GLOBAL_FOUNDATION_AND_REVIEW_PROTOTYPE_COMPLETE" in rt and "Not claimed" not in rt:
            errors.append("PILOT_REPORT must not claim global foundation complete")
        if "NOT_YET_MAPPED" in rt and "dangling" not in rt.lower() and "superseded" not in rt.lower():
            # allow historical mention if superseded
            if "All pilot spread standards entries: **NOT_YET_MAPPED**" in rt:
                errors.append("PILOT_REPORT still claims all spreads NOT_YET_MAPPED")

    for short in BANDS:
        band_dir = PILOT / f"KIDS-{short}"
        for req in ["MANUSCRIPT.md", "TRACEABILITY.yaml", "AUTHOR_NOTES.yaml", "README.md"]:
            if not (band_dir / req).is_file():
                errors.append(f"{short}: missing {req}")
        ms = band_dir / "MANUSCRIPT.md"
        if ms.is_file():
            text = ms.read_text(encoding="utf-8")
            for line in BANNER_LINES:
                if line not in text:
                    errors.append(f"{short}: manuscript missing banner line {line}")
            if PLACEHOLDER_RE.search(text):
                errors.append(f"{short}: placeholder in manuscript")
            # Forbidden editor meta in child/caregiver body (allow Facilitator pointer section)
            body = text.split("## Facilitator pointer")[0]
            if FORBIDDEN_BODY.search(body):
                errors.append(f"{short}: editor/integrator meta still in caregiver-facing body")
            wc = child_facing_words(ms)
            if wc < MIN_WORDS[short]:
                errors.append(f"{short}: child-facing words {wc} < min {MIN_WORDS[short]}")
            if short in MAX_WORDS and wc > MAX_WORDS[short]:
                errors.append(f"{short}: child-facing words {wc} > max {MAX_WORDS[short]} (restraint)")

        figs = list((band_dir / "figures").glob("FIG-ONE-TAP-*.svg"))
        if len(figs) < 10:
            errors.append(f"{short}: expected 10 figures, found {len(figs)}")
        for fig in figs:
            raw = fig.read_text(encoding="utf-8")
            if PLACEHOLDER_RE.search(raw):
                errors.append(f"{fig.name}: placeholder graphics")
            if 'role="img"' not in raw or "-title" not in raw:
                errors.append(f"{fig.name}: missing a11y title/role")
            meta = fig.with_suffix(".meta.yaml")
            if not meta.is_file():
                errors.append(f"{fig.name}: missing .meta.yaml")

        html = band_dir / "builds" / "caregiver-preview.html"
        pdf = band_dir / "builds" / f"ONE_TAP_{short}.pdf"
        if not html.is_file():
            errors.append(f"{short}: missing HTML")
        else:
            ht = html.read_text(encoding="utf-8")
            for line in BANNER_LINES:
                if line not in ht:
                    errors.append(f"{short}: HTML missing {line}")
            if "Easy exit" not in ht and "easy exit" not in ht.lower():
                errors.append(f"{short}: HTML missing easy exit")
            if 'lang=' not in ht:
                errors.append(f"{short}: HTML missing lang")
        if not pdf.is_file() or pdf.stat().st_size < 800:
            errors.append(f"{short}: missing/empty PDF")

        tr = band_dir / "TRACEABILITY.yaml"
        if tr.is_file():
            data = yaml.safe_load(tr.read_text(encoding="utf-8"))
            spreads = data.get("spreads") or []
            if len(spreads) < 10:
                errors.append(f"{short}: traceability spreads < 10")
            for sp in spreads:
                stds = sp.get("standards") or []
                if not stds:
                    errors.append(f"{short}: spread missing standards")
                    continue
                st = stds[0]
                status = st.get("status")
                if status not in {
                    "ADJACENT",
                    "EXACT",
                    "PROPOSED",
                    "NO_MAP",
                    "TRANSLATION_REQUIRED",
                    "VERSION_UNCLEAR",
                    "NOT_YET_MAPPED",
                }:
                    errors.append(f"{short}: bad status {status}")
                maps = st.get("atlas_mapping_ids") or []
                # Dangling STD-WIRE-only is forbidden when status claims a map
                if status in {"ADJACENT", "EXACT", "PROPOSED"}:
                    if not maps:
                        errors.append(
                            f"{short} {sp.get('page_or_spread_id')}: {status} without atlas_mapping_ids"
                        )
                    for mid in maps:
                        if mid not in atlas_ids:
                            errors.append(
                                f"{short}: atlas id {mid} not found in GLOBAL_STANDARDS_ATLAS.yaml"
                            )
                # wire key alone is OK only as registry index
                if st.get("wire_id") and not maps and status not in {
                    "NO_MAP",
                    "TRANSLATION_REQUIRED",
                    "VERSION_UNCLEAR",
                    "NOT_YET_MAPPED",
                }:
                    errors.append(f"{short}: dangling wire_id without atlas maps")

    # No fabricated child validation artifacts
    for p in PILOT.rglob("*"):
        if p.is_file() and re.search(r"child[_-]validat|reader[_-]evidence[_-]kids", p.name, re.I):
            if p.name.upper().startswith("NOT"):
                continue
            errors.append(f"forbidden child-validation artifact name: {p}")

    if errors:
        print("kids-review-prototype-check FAIL")
        for e in errors:
            print(f" - {e}")
        return 1
    print("kids-review-prototype-check PASS")
    print(f" bands={len(BANDS)} claim=KIDS_REVIEW_PROTOTYPE_COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
