#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402


def main() -> int:
    errors: list[str] = []
    reg = load_yaml(ROOT / "figures/figure_registry.yaml")
    figure_ids = []
    for fig in reg.get("figures") or []:
        fid = fig.get("figure_id")
        figure_ids.append(fid)
        path = ROOT / fig["path"]
        if not path.exists():
            errors.append(f"{fid}: missing asset {fig['path']}")
        acc_path = ROOT / fig["accessibility"]
        if not acc_path.exists():
            errors.append(f"{fid}: missing accessibility sidecar")
            continue
        acc = load_yaml(acc_path)
        for field in ("alt_text", "text_equivalent", "caption", "reading_order", "status"):
            if not acc.get(field):
                errors.append(f"{fid}: accessibility missing {field}")
        if acc.get("status") not in {"conceptual", "illustrative", "implemented", "mixed"}:
            errors.append(f"{fid}: invalid status {acc.get('status')}")
    if len(figure_ids) != len(set(figure_ids)):
        errors.append("duplicate figure ids")
    # CH02 required figures
    meta = load_yaml(ROOT / "book/chapters/ch02/metadata.yaml")
    for fid in meta.get("figures") or []:
        if fid not in figure_ids:
            errors.append(f"CH02 references missing figure {fid}")
    if errors:
        print("validate_figures: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_figures: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
