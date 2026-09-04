#!/usr/bin/env python3
"""Detect cross-surface figure truth-class drift (SVG / a11y / registry).

Canonical classroom-fixture wording family:
  illustrative-classroom-fixture | illustrative_classroom_fixture | illustrative

Fails when surfaces disagree after normalization, or when a classroom fixture
uses a 'measured' truth class that implies validated product evidence.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

ILLUSTRATIVE_FAMILY = {
    "illustrative",
    "illustrative-classroom-fixture",
    "illustrative_classroom_fixture",
    "illustrative classroom fixture",
    "illustrative classroom fixture (n=1)",
}


def norm(raw: str | None) -> str:
    s = (raw or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = s.replace("_", "-")
    return s


def family(raw: str | None) -> str:
    n = norm(raw)
    if not n:
        return ""
    if n in ILLUSTRATIVE_FAMILY or n.startswith("illustrative"):
        return "illustrative"
    if n.startswith("measured"):
        return "measured"
    if "blocked" in n:
        return "blocked"
    return n


def svg_truth(path: Path) -> str | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'data-truth-classification="([^"]+)"', text)
    return m.group(1) if m else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", default=True)
    args = parser.parse_args()
    del args  # unused; always check
    reg = load_yaml(ROOT / "figures/figure_registry.yaml") or {}
    errors: list[str] = []
    checked = 0
    for item in reg.get("figures") or []:
        fid = str(item.get("figure_id") or item.get("id") or "")
        svg_rel = item.get("path")
        a11y_rel = item.get("accessibility")
        reg_truth = item.get("truth_classification")
        reg_status = item.get("status")
        if not svg_rel:
            continue
        svg_path = ROOT / str(svg_rel)
        svg_t = svg_truth(svg_path)
        a11y_t = None
        if a11y_rel:
            a11y_path = ROOT / str(a11y_rel)
            if a11y_path.is_file():
                a11y = load_yaml(a11y_path) or {}
                a11y_t = a11y.get("truth_classification") or a11y.get("status")
        # Only enforce cross-surface agreement when registry declares truth_classification
        # (or for critical classroom fixtures). Avoid false positives on status-only rows.
        critical = fid in {"FIG-CH12-004"}
        if not reg_truth and not critical:
            continue
        surfaces = {
            "registry": family(str(reg_truth or reg_status) if (reg_truth or reg_status) else None),
            "svg": family(svg_t),
            "a11y": family(str(a11y_t) if a11y_t else None),
        }
        present = {k: v for k, v in surfaces.items() if v}
        if len(present) < 2:
            continue
        checked += 1
        families = set(present.values())
        if len(families) > 1:
            errors.append(
                f"{fid}: truth-class drift across surfaces {present} "
                f"(raw registry={reg_truth!r} svg={svg_t!r} a11y={a11y_t!r})"
            )
        # Classroom fixture hard rule for CH12-004 and similar n=1 plates
        if fid == "FIG-CH12-004" and "measured" in families:
            errors.append(
                f"{fid}: must not use measured truth class "
                "(illustrative classroom fixture n=1 only)"
            )
    print(f"validate_figure_truth_drift: checked={checked}")
    if errors:
        print("validate_figure_truth_drift: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_figure_truth_drift: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
