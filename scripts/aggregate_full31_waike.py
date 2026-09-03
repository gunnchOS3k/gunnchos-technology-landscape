#!/usr/bin/env python3
"""Deterministic WAIKE crosswalk aggregation for Full31 packets.

Usage:
  python scripts/aggregate_full31_waike.py           # write report JSON/MD
  python scripts/aggregate_full31_waike.py --check   # fail if stale / mismatch
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from full31_common import WAIKE_ACCEPTED_MAIN, aggregate_all_waike  # noqa: E402
from yaml_util import load_yaml  # noqa: E402

OUT_JSON = ROOT / "publication/full31/WAIKE_AGGREGATION.json"
OUT_MD = ROOT / "publication/full31/WAIKE_AGGREGATION.md"
REGISTRY = ROOT / "publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml"
REPORT = ROOT / "publication/full31/FULL31_PROGRESS_REPORT.md"


def render_md(agg: dict) -> str:
    lines = [
        "# Full31 WAIKE Aggregation",
        "",
        "**Deterministic parser over** `publication/full31/chapters/chNN/WAIKE_CROSSWALK.md`.",
        "",
        f"**WAIKE accepted main:** `{agg['waike_accepted_main_sha']}`  ",
        f"**Unique upstream WAIKE objects:** **{agg['unique_upstream_waike_objects']}**  ",
        "",
        "## Totals",
        "",
        "| Class | Count |",
        "|---|---:|",
    ]
    for key in ("exact", "adjacent", "proposed", "no_map"):
        lines.append(f"| `{key}` | {agg['totals'][key]} |")
    lines.extend(["", "## Per-part", "", "| Part | exact | adjacent | proposed | no_map |", "|---|---:|---:|---:|---:|"])
    for part, counts in agg["per_part"].items():
        lines.append(
            f"| {part} | {counts.get('exact', 0)} | {counts.get('adjacent', 0)} | "
            f"{counts.get('proposed', 0)} | {counts.get('no_map', 0)} |"
        )
    lines.extend(
        [
            "",
            "## Per-chapter",
            "",
            "| Chapter | exact | adjacent | proposed | no_map | unique IDs |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for cid, parsed in sorted(agg["per_chapter"].items(), key=lambda kv: kv[0]):
        c = parsed["counts"]
        lines.append(
            f"| {cid} | {c.get('exact', 0)} | {c.get('adjacent', 0)} | "
            f"{c.get('proposed', 0)} | {c.get('no_map', 0)} | {parsed['unique_waike_id_count']} |"
        )
    lines.extend(
        [
            "",
            "## Method notes",
            "",
            "- Counts come from per-chapter count tables when present; otherwise from mapping rows/sections.",
            "- Does not count prose mentions or registry-fragment duplicate totals.",
            "- Unique upstream IDs are backtick tokens that look like WAIKE course/lab/catalog IDs.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    agg = aggregate_all_waike()
    if agg["waike_accepted_main_sha"] != WAIKE_ACCEPTED_MAIN:
        print("aggregate_full31_waike: FAIL unexpected SHA constant")
        return 1

    payload = json.dumps(agg, indent=2, sort_keys=True) + "\n"
    md = render_md(agg)

    if args.check:
        errors: list[str] = []
        if not OUT_JSON.exists() or OUT_JSON.read_text(encoding="utf-8") != payload:
            errors.append(f"{OUT_JSON.relative_to(ROOT)} stale; re-run without --check")
        if not OUT_MD.exists() or OUT_MD.read_text(encoding="utf-8") != md:
            errors.append(f"{OUT_MD.relative_to(ROOT)} stale; re-run without --check")
        if REGISTRY.exists():
            reg = load_yaml(REGISTRY) or {}
            totals = reg.get("waike_mapping_totals") or {}
            for key in ("exact", "adjacent", "proposed", "no_map"):
                if int(totals.get(key, -1)) != int(agg["totals"][key]):
                    errors.append(
                        f"registry waike_mapping_totals.{key}={totals.get(key)!r} "
                        f"!= aggregated {agg['totals'][key]}"
                    )
            if str(reg.get("waike_accepted_main_sha")) != WAIKE_ACCEPTED_MAIN:
                errors.append("registry waike_accepted_main_sha mismatch")
        if REPORT.exists():
            report = REPORT.read_text(encoding="utf-8")
            for key, label in (
                ("exact", "exact"),
                ("adjacent", "adjacent"),
                ("proposed", "proposed"),
                ("no_map", "no_map"),
            ):
                needle = f"{label}={agg['totals'][key]}"
                # accept either key=value or markdown backticks
                if needle not in report and f"`{key}` | {agg['totals'][key]}" not in report:
                    if f"| `{key}` | {agg['totals'][key]} |" not in report:
                        errors.append(f"progress report missing authoritative {key} total")
        if errors:
            print("aggregate_full31_waike: FAIL")
            for e in errors:
                print(" -", e)
            return 1
        print("aggregate_full31_waike: PASS")
        print(f" - totals={agg['totals']}")
        print(f" - unique_upstream_waike_objects={agg['unique_upstream_waike_objects']}")
        return 0

    OUT_JSON.write_text(payload, encoding="utf-8")
    OUT_MD.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(f"totals={agg['totals']} unique={agg['unique_upstream_waike_objects']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
