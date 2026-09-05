"""Regression tests for Kids full-manuscript inventory/asset counting (Prompt 27)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_unique_atlas_mapping_ids_reads_atlas_mapping_ids():
    lib = _load("asset_lib", ROOT / "scripts" / "kids_full_manuscript_asset_lib.py")
    sample = {
        "units": [
            {
                "unit_id": "U1",
                "status": "ADJACENT",
                "atlas_mapping_ids": ["MAP-A", "MAP-B", "MAP-A"],
            },
            {
                "unit_id": "U2",
                "status": "NOT_YET_MAPPED",
                "atlas_mapping_ids": [],
            },
            {
                "unit_id": "U3",
                "status": "ADJACENT",
                "standards_mapping_ids": ["MAP-B", "MAP-C"],
            },
        ]
    }
    ids = lib.unique_atlas_mapping_ids(sample)
    assert ids == {"MAP-A", "MAP-B", "MAP-C"}
    counts = lib.standards_status_counts(sample)
    assert counts["ADJACENT"] == 2
    assert counts["NOT_YET_MAPPED"] == 1


def test_live_registered_excludes_orphans_and_narr_without_svg(tmp_path: Path):
    lib = _load("asset_lib", ROOT / "scripts" / "kids_full_manuscript_asset_lib.py")
    figs = tmp_path / "figures"
    figs.mkdir()
    (figs / "FIG-A.svg").write_text("<svg/>", encoding="utf-8")
    (figs / "FIG-ORPHAN.svg").write_text("<svg/>", encoding="utf-8")
    plan = {
        "figures": [
            {"figure_id": "FIG-A", "production_status": "DETERMINISTIC_DIAGRAM_SHIPPED"},
            {"figure_id": "NARR-A", "production_status": "ILLUSTRATION_DIRECTION_READY"},
        ]
    }
    registered = lib.registered_figure_ids(plan)
    live = lib.live_registered_ids(plan, figs)
    physical = lib.physical_svg_ids(figs)
    assert registered == {"FIG-A", "NARR-A"}
    assert live == {"FIG-A"}
    assert "FIG-ORPHAN" in physical - registered


def test_elem2_deterministic_diagrams_schema_parsed():
    lib = _load("asset_lib", ROOT / "scripts" / "kids_full_manuscript_asset_lib.py")
    plan_path = ROOT / "kids" / "books" / "KIDS-ELEM2" / "FIGURE_PLAN.yaml"
    if not plan_path.is_file():
        return
    data = lib.load_yaml(plan_path)
    ids = lib.registered_figure_ids(data)
    assert any(i.startswith("FIG-ELEM2-") for i in ids)
    live = lib.live_registered_ids(data, ROOT / "kids" / "books" / "KIDS-ELEM2" / "figures")
    assert len(live) >= 1


def test_inventory_generator_band_stats_standards_nonzero_for_elem2():
    gen = _load("inv_gen", ROOT / "scripts" / "generate_kids_full_manuscript_inventory.py")
    if not (ROOT / "kids" / "books" / "KIDS-ELEM2" / "BOOK_MANUSCRIPT.md").is_file():
        return
    stats = gen.band_stats("KIDS-ELEM2")
    assert stats["standards_mappings"] > 0
    assert stats["orphan_svg_files"] == 0
    assert stats["live_registered_figures"] == stats["physical_svg_files"]


def test_baby_live_equals_physical_after_orphan_cleanup():
    gen = _load("inv_gen", ROOT / "scripts" / "generate_kids_full_manuscript_inventory.py")
    if not (ROOT / "kids" / "books" / "KIDS-BABY" / "BOOK_MANUSCRIPT.md").is_file():
        return
    stats = gen.band_stats("KIDS-BABY")
    assert stats["live_registered_figures"] == 42
    assert stats["physical_svg_files"] == 42
    assert stats["orphan_svg_files"] == 0
