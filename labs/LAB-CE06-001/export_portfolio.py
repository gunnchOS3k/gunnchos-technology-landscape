#!/usr/bin/env python3
"""Export LAB-CE06-001 portfolio fields to a single markdown packet for sharing.

Default exports the blank template structure with an integrity banner.
Pass a portfolio directory to export a filled packet.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent

ORDERED = [
    "README.md",
    "portfolio_summary.md",
    "human_experience.md",
    "system_boundary.md",
    "components.md",
    "software_code_role.md",
    "network_role.md",
    "stability_contract.md",
    "observations.md",
    "inferences.md",
    "measurements.md",
    "evidence_limitations.md",
    "security_privacy_accessibility.md",
    "equity_societal_impact.md",
    "improve_plan.md",
    "teach_back.md",
    "diagram.md",
    "reflection.md",
    "evidence/NOTE.md",
    "result_table.csv",
]


def export_portfolio(src: Path, dest: Path) -> None:
    parts: list[str] = []
    parts.append("# LAB-CE06-001 portfolio export\n")
    parts.append(
        "> Integrity: commodity evidence only. Fixtures/illustrative packets are "
        "not human Gate evidence. Status vocabulary never means learner PASS.\n"
    )
    for name in ORDERED:
        path = src / name
        parts.append(f"\n---\n\n## {name}\n\n")
        if path.exists():
            text = path.read_text(encoding="utf-8")
            parts.append(text if text.endswith("\n") else text + "\n")
        else:
            parts.append(f"_Missing: {name}_\n")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("".join(parts), encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--src",
        type=Path,
        default=LAB_DIR / "portfolio",
        help="Portfolio directory to export (default: blank template)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=LAB_DIR / "export" / "portfolio_export.md",
        help="Output markdown path",
    )
    args = parser.parse_args(argv)
    if not args.src.is_dir():
        print(f"export_portfolio: missing source dir {args.src}", file=sys.stderr)
        return 1
    export_portfolio(args.src, args.out)
    print(f"export_portfolio: wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
