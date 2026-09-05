#!/usr/bin/env python3
"""Shared helpers for Kids full-manuscript figure plans and standards counts."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

FIG_ID_RE = re.compile(r"FIG-[A-Z0-9-]+|NARR-[A-Z0-9-]+")


def load_yaml(path: Path) -> Any:
    if yaml is None:
        raise RuntimeError("PyYAML required")
    if not path.is_file():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def iter_figure_plan_entries(data: Any) -> list[dict]:
    """Normalize FIGURE_PLAN schemas into dict entries with figure_id."""
    if not isinstance(data, dict):
        return []
    out: list[dict] = []
    figs = data.get("figures")
    if isinstance(figs, list):
        for f in figs:
            if isinstance(f, dict):
                fid = f.get("figure_id") or f.get("id") or f.get("asset_id")
                if fid:
                    item = dict(f)
                    item["figure_id"] = fid
                    out.append(item)
            elif isinstance(f, str):
                out.append({"figure_id": f})
    for key in ("deterministic_diagrams", "live_figures", "assets"):
        block = data.get(key)
        if not isinstance(block, list):
            continue
        for f in block:
            if not isinstance(f, dict):
                continue
            fid = f.get("asset_id") or f.get("figure_id") or f.get("id")
            if not fid:
                continue
            item = dict(f)
            item["figure_id"] = fid
            out.append(item)
    return out


def registered_figure_ids(plan_data: Any) -> set[str]:
    return {e["figure_id"] for e in iter_figure_plan_entries(plan_data) if e.get("figure_id")}


def is_direction_only(entry: dict) -> bool:
    """Narrative direction entries that intentionally lack shipped SVGs."""
    fid = str(entry.get("figure_id") or "")
    status = str(
        entry.get("production_status")
        or entry.get("status")
        or entry.get("illustration_status")
        or ""
    ).upper()
    if fid.startswith("NARR-"):
        return True
    if "ILLUSTRATION_DIRECTION" in status and "DETERMINISTIC" not in status:
        # PREK marks some STORY beats ILLUSTRATION_DIRECTION_READY but still ships SVG.
        # Direction-only only when no svg path / no physical expectation via NARR.
        path = str(entry.get("path") or "")
        if not path.endswith(".svg") and not fid.startswith("FIG-"):
            return True
    return False


def live_registered_ids(plan_data: Any, figures_dir: Path) -> set[str]:
    """Registered figure IDs that are live manuscript assets (have SVG on disk).

    Direction-only NARR-* entries without SVG are registered but not live.
    """
    live: set[str] = set()
    for e in iter_figure_plan_entries(plan_data):
        fid = e.get("figure_id")
        if not fid:
            continue
        svg = figures_dir / f"{fid}.svg"
        if svg.is_file():
            live.add(fid)
    return live


def physical_svg_ids(figures_dir: Path) -> set[str]:
    if not figures_dir.is_dir():
        return set()
    return {p.stem for p in figures_dir.glob("*.svg")}


def manuscript_figure_refs(ms_text: str) -> set[str]:
    # Prefer markdown image targets under figures/
    refs = set(re.findall(r"figures/(FIG-[A-Z0-9-]+)\.svg", ms_text))
    if not refs:
        refs = set(re.findall(r"!\[(FIG-[A-Z0-9-]+)\]", ms_text))
    return refs


def entry_has_a11y(entry: dict, figures_dir: Path) -> bool:
    for key in ("alt", "alt_description", "description", "alt_text"):
        val = entry.get(key)
        if isinstance(val, str) and val.strip():
            return True
    a11y = entry.get("a11y")
    if isinstance(a11y, dict) and a11y:
        return True
    fid = entry.get("figure_id")
    if fid and (figures_dir / f"{fid}.meta.yaml").is_file():
        meta = load_yaml(figures_dir / f"{fid}.meta.yaml") or {}
        if isinstance(meta, dict):
            for key in ("alt", "alt_description", "description"):
                if isinstance(meta.get(key), str) and meta.get(key).strip():
                    return True
            if isinstance(meta.get("a11y"), dict):
                return True
    return False


def unique_atlas_mapping_ids(std_data: Any) -> set[str]:
    """Canonical standards count source: STANDARDS_TRACEABILITY.yaml atlas_mapping_ids."""
    ids: set[str] = set()
    if not isinstance(std_data, dict):
        return ids
    units = std_data.get("units")
    if isinstance(units, list):
        for u in units:
            if not isinstance(u, dict):
                continue
            for mid in u.get("atlas_mapping_ids") or []:
                if isinstance(mid, str) and mid.startswith("MAP-") and not mid.startswith("MAP-UNIT-"):
                    ids.add(mid)
            # tolerate legacy key
            for mid in u.get("standards_mapping_ids") or []:
                if isinstance(mid, str) and mid.startswith("MAP-") and not mid.startswith("MAP-UNIT-"):
                    ids.add(mid)
            for m in u.get("mappings") or []:
                if isinstance(m, dict):
                    mid = m.get("mapping_id") or m.get("id")
                    if isinstance(mid, str) and mid.startswith("MAP-"):
                        ids.add(mid)
                elif isinstance(m, str) and m.startswith("MAP-"):
                    ids.add(m)
    mappings = std_data.get("mappings")
    if isinstance(mappings, list):
        for m in mappings:
            if isinstance(m, dict):
                mid = m.get("mapping_id") or m.get("id")
                if isinstance(mid, str) and mid.startswith("MAP-"):
                    ids.add(mid)
    return ids


def standards_status_counts(std_data: Any) -> dict[str, int]:
    counts = {
        "ADJACENT": 0,
        "EXACT": 0,
        "PROPOSED": 0,
        "NOT_YET_MAPPED": 0,
        "NO_MAP": 0,
        "TRANSLATION_REQUIRED": 0,
        "VERSION_UNCLEAR": 0,
        "OTHER": 0,
    }
    if not isinstance(std_data, dict):
        return counts
    units = std_data.get("units")
    if not isinstance(units, list):
        return counts
    for u in units:
        if not isinstance(u, dict):
            continue
        status = str(
            u.get("status") or u.get("standards_status") or u.get("fidelity") or "OTHER"
        ).upper()
        if status in counts:
            counts[status] += 1
        else:
            counts["OTHER"] += 1
    return counts
