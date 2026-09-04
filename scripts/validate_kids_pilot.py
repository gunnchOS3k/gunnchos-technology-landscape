#!/usr/bin/env python3
"""Validate ONE TAP kids pilot artifacts across all six age bands."""
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
BANDS = ["BABY", "TODDLER", "PRESCHOOL", "PREK", "ELEM1", "ELEM2"]
BANNER_SNIP = "NOT CHILD-VALIDATED"
PLACEHOLDER_RE = re.compile(r"image here|TODO_IMAGE|lorem ipsum", re.I)


def main() -> int:
    errors: list[str] = []
    if not PILOT.is_dir():
        print(f"FAIL: missing {PILOT}")
        return 1

    for short in BANDS:
        band_dir = PILOT / f"KIDS-{short}"
        if not band_dir.is_dir():
            errors.append(f"missing band dir {band_dir}")
            continue
        for req in ["MANUSCRIPT.md", "TRACEABILITY.yaml", "README.md"]:
            if not (band_dir / req).is_file():
                errors.append(f"{short}: missing {req}")
        ms = band_dir / "MANUSCRIPT.md"
        if ms.is_file():
            text = ms.read_text(encoding="utf-8")
            if BANNER_SNIP not in text:
                errors.append(f"{short}: manuscript missing prototype honesty banner")
            if PLACEHOLDER_RE.search(text):
                errors.append(f"{short}: placeholder text in manuscript")
            if "sentence simplification" in text.lower() and "not sentence" not in text.lower():
                pass
        figs = list((band_dir / "figures").glob("FIG-ONE-TAP-*.svg"))
        if len(figs) < 8:
            errors.append(f"{short}: expected ≥8 figures, found {len(figs)}")
        for fig in figs:
            raw = fig.read_text(encoding="utf-8")
            if PLACEHOLDER_RE.search(raw) or "IMAGE HERE" in raw.upper():
                errors.append(f"{fig.name}: placeholder graphics")
            meta = fig.with_suffix(".meta.yaml")
            if not meta.is_file():
                errors.append(f"{fig.name}: missing .meta.yaml")
            else:
                m = yaml.safe_load(meta.read_text(encoding="utf-8"))
                for k in ["asset_id", "truth_class", "age_band", "alt", "print_dimensions_px"]:
                    if k not in m:
                        errors.append(f"{meta.name}: missing {k}")
        html = band_dir / "builds" / "caregiver-preview.html"
        pdf = band_dir / "builds" / f"ONE_TAP_{short}.pdf"
        if not html.is_file():
            errors.append(f"{short}: missing HTML preview")
        elif BANNER_SNIP not in html.read_text(encoding="utf-8"):
            errors.append(f"{short}: HTML missing honesty banner")
        if not pdf.is_file() or pdf.stat().st_size < 500:
            errors.append(f"{short}: missing/empty PDF")

        tr = band_dir / "TRACEABILITY.yaml"
        if tr.is_file():
            data = yaml.safe_load(tr.read_text(encoding="utf-8"))
            spreads = data.get("spreads") or []
            if len(spreads) < 8:
                errors.append(f"{short}: traceability spreads < 8")
            for sp in spreads:
                stds = sp.get("standards") or []
                if not stds:
                    errors.append(f"{short}: spread missing standards block")
                else:
                    st = stds[0].get("status")
                    if st not in {"NOT_YET_MAPPED", "PROPOSED", "EXACT", "ADJACENT", "NO_MAP"}:
                        errors.append(f"{short}: bad standards status {st}")

    report = PILOT / "PILOT_REPORT.md"
    if not report.is_file():
        errors.append("missing PILOT_REPORT.md")
    elif "NOT CHILD-VALIDATED" not in report.read_text(encoding="utf-8"):
        errors.append("PILOT_REPORT missing honesty label")

    # No fabricated child validation evidence files
    for p in PILOT.rglob("*"):
        if p.is_file() and re.search(r"child[_-]validat|reader[_-]evidence[_-]kids", p.name, re.I):
            errors.append(f"forbidden child-validation artifact name: {p}")

    if errors:
        print("kids-pilot-check FAIL")
        for e in errors:
            print(f" - {e}")
        return 1
    print("kids-pilot-check PASS")
    print(f" bands={len(BANDS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
