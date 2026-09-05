#!/usr/bin/env python3
"""Validate Kids full-manuscript figure asset graph + hygiene (Prompt 27).

Fails on:
- manuscript figure refs missing on disk
- manuscript refs unregistered in FIGURE_PLAN
- registered live figures missing on disk
- unexplained orphan SVGs
- duplicate figure IDs in FIGURE_PLAN
- missing accessibility metadata for live figures
- artifact/inventory live-figure count drift
- integration sentinels (.write_ok) under kids/books
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from kids_full_manuscript_asset_lib import (  # noqa: E402
    entry_has_a11y,
    iter_figure_plan_entries,
    live_registered_ids,
    load_yaml,
    manuscript_figure_refs,
    physical_svg_ids,
    registered_figure_ids,
)

BOOKS = ROOT / "kids" / "books"
BANDS = [
    "KIDS-BABY",
    "KIDS-TODDLER",
    "KIDS-PRESCHOOL",
    "KIDS-PREK",
    "KIDS-ELEM1",
    "KIDS-ELEM2",
]
FORBIDDEN_SENTINELS = {".write_ok", ".DS_Store"}
FORBIDDEN_SUFFIXES = {".bak", ".orig", ".tmp"}


def artifact_live_count(art: dict | None, live: set[str]) -> int | None:
    if not isinstance(art, dict):
        return None
    if "figure_count" in art and art["figure_count"] is not None:
        return int(art["figure_count"])
    meta = art.get("meta") if isinstance(art.get("meta"), dict) else {}
    if "figure_count" in meta and meta["figure_count"] is not None:
        return int(meta["figure_count"])
    figs = art.get("figures")
    if isinstance(figs, list):
        # Count only entries that correspond to live SVGs when figure_id present.
        ids = set()
        for f in figs:
            if isinstance(f, dict):
                fid = f.get("figure_id") or f.get("id")
                if fid:
                    ids.add(fid)
            elif isinstance(f, str):
                ids.add(Path(f).stem)
        if ids:
            return len(ids & live) if live else len(ids)
        return len(figs)
    return None


def validate_band(band: str) -> list[str]:
    errors: list[str] = []
    root = BOOKS / band
    figs_dir = root / "figures"
    plan = load_yaml(root / "FIGURE_PLAN.yaml") or {}
    entries = iter_figure_plan_entries(plan)
    registered = registered_figure_ids(plan)
    live = live_registered_ids(plan, figs_dir)
    physical = physical_svg_ids(figs_dir)
    ms = (root / "BOOK_MANUSCRIPT.md").read_text(encoding="utf-8")
    refs = manuscript_figure_refs(ms)

    # Duplicate IDs in plan
    seen: set[str] = set()
    for e in entries:
        fid = e.get("figure_id")
        if not fid:
            continue
        if fid in seen:
            errors.append(f"{band}: duplicate figure_id in FIGURE_PLAN: {fid}")
        seen.add(fid)

    # Manuscript refs
    for fid in sorted(refs):
        if not (figs_dir / f"{fid}.svg").is_file():
            errors.append(f"{band}: manuscript ref missing SVG: {fid}")
        if fid not in registered:
            errors.append(f"{band}: manuscript ref not registered in FIGURE_PLAN: {fid}")

    # Live registered must exist
    for fid in sorted(live):
        if not (figs_dir / f"{fid}.svg").is_file():
            errors.append(f"{band}: registered live figure missing SVG: {fid}")

    # Orphans
    orphans = physical - registered
    for fid in sorted(orphans):
        errors.append(f"{band}: orphan/unregistered SVG: {fid}")

    # Accessibility for live figures
    entry_by_id = {e["figure_id"]: e for e in entries if e.get("figure_id")}
    for fid in sorted(live):
        entry = entry_by_id.get(fid) or {"figure_id": fid}
        if not entry_has_a11y(entry, figs_dir):
            errors.append(f"{band}: live figure missing accessibility alt/meta: {fid}")

    # Artifact manifest count
    art = load_yaml(root / "ARTIFACT_MANIFEST.yaml") or {}
    art_count = artifact_live_count(art if isinstance(art, dict) else None, live)
    if art_count is not None and art_count != len(live):
        errors.append(
            f"{band}: ARTIFACT_MANIFEST figure_count {art_count} != live_registered {len(live)}"
        )

    return errors


def validate_inventory_alignment() -> list[str]:
    errors: list[str] = []
    inv_path = BOOKS / "KIDS_MANUSCRIPT_INVENTORY.yaml"
    inv = load_yaml(inv_path)
    if not isinstance(inv, dict):
        return ["missing or invalid KIDS_MANUSCRIPT_INVENTORY.yaml"]
    books = inv.get("books") or []
    by_band = {b.get("age_band"): b for b in books if isinstance(b, dict)}
    for band in BANDS:
        root = BOOKS / band
        plan = load_yaml(root / "FIGURE_PLAN.yaml") or {}
        live = live_registered_ids(plan, root / "figures")
        row = by_band.get(band)
        if not row:
            errors.append(f"inventory missing band {band}")
            continue
        inv_live = row.get("live_registered_figures")
        if inv_live is None:
            inv_live = row.get("figures_svg")
        if inv_live != len(live):
            errors.append(
                f"{band}: inventory live figures {inv_live} != actual {len(live)}"
            )
        if int(row.get("orphan_svg_files") or 0) != 0:
            errors.append(f"{band}: inventory reports orphan_svg_files={row.get('orphan_svg_files')}")
    return errors


def validate_hygiene() -> list[str]:
    errors: list[str] = []
    if not BOOKS.is_dir():
        return ["kids/books missing"]
    for p in BOOKS.rglob("*"):
        if not p.is_file():
            continue
        if p.name in FORBIDDEN_SENTINELS:
            errors.append(f"integration sentinel forbidden: {p.relative_to(ROOT)}")
        if p.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"scratch suffix forbidden: {p.relative_to(ROOT)}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    errors: list[str] = []
    report = {}
    for band in BANDS:
        be = validate_band(band)
        errors.extend(be)
        root = BOOKS / band
        plan = load_yaml(root / "FIGURE_PLAN.yaml") or {}
        live = live_registered_ids(plan, root / "figures")
        physical = physical_svg_ids(root / "figures")
        registered = registered_figure_ids(plan)
        report[band] = {
            "registered": len(registered),
            "live_registered": len(live),
            "physical": len(physical),
            "orphans": sorted(physical - registered),
            "missing_live": sorted(live - physical),
            "band_errors": be,
        }
    errors.extend(validate_inventory_alignment())
    errors.extend(validate_hygiene())
    if args.json:
        print(yaml.safe_dump({"report": report, "errors": errors}, sort_keys=False))
    if errors:
        print(f"kids-full-manuscript-assets-check FAIL ({len(errors)})")
        for e in errors[:100]:
            print(f" - {e}")
        if len(errors) > 100:
            print(f" … {len(errors) - 100} more")
        return 1
    print("kids-full-manuscript-assets-check PASS")
    for band, row in report.items():
        print(
            f"  {band}: live={row['live_registered']} physical={row['physical']} "
            f"registered={row['registered']} orphans=0"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
