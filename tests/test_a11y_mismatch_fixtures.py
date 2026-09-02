from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "tests/fixtures/invalid"


def _desc(svg: str) -> str:
    m = re.search(r"<desc>(.*?)</desc>", svg, flags=re.S)
    assert m
    return m.group(1).lower()


def test_arrows_mismatch_fixture():
    svg = (INV / "figure_claims_arrows_without_arrows.svg").read_text()
    assert "arrows" in _desc(svg)
    assert "marker-end=" not in svg


def test_dashed_mismatch_fixture():
    svg = (INV / "figure_claims_dashed_without_dash.svg").read_text()
    assert "dashed" in _desc(svg)
    assert "stroke-dasharray" not in svg


def test_stacked_bar_mismatch_fixture():
    svg = (INV / "figure_claims_stacked_bar_without_bar.svg").read_text()
    assert "stacked bar" in _desc(svg)
    assert svg.count("<rect") == 0


def test_exploded_mismatch_fixture():
    svg = (INV / "figure_claims_exploded_but_list_only.svg").read_text()
    assert "exploded" in _desc(svg)
    assert svg.count("<rect") + svg.count("<path") < 8
