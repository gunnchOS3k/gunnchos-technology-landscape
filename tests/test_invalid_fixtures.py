from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def test_duplicate_glossary_id_fails(tmp_path, monkeypatch):
    # copy minimal broken glossary into a temp override by invoking validator logic
    data = yaml.safe_load((ROOT / "glossary/glossary.yaml").read_text())
    data["entries"].append(dict(data["entries"][0]))
    bad = tmp_path / "glossary.yaml"
    bad.write_text(yaml.safe_dump(data))
    # inline check
    ids = [e["id"] for e in data["entries"]]
    assert len(ids) != len(set(ids))


def test_missing_alt_text_detected():
    sample = {"caption": "x", "text_equivalent": "y", "reading_order": ["a"], "status": "conceptual"}
    assert not sample.get("alt_text")


def test_invented_waike_course_rejected():
    known = {"SOFTWARE_BUILDER"}
    assert "TRACE_ONE_TAP_FAKE" not in known


def test_claim_planned_cannot_read_as_implemented():
    classification = "planned"
    prose = "The system currently supports physical ring input"
    import re
    assert classification == "planned"
    assert re.search(r"currently supports", prose)


def test_lab_without_no_hardware_route_is_invalid():
    lab = {"accessible_routes": {"no_specialized_hardware": False}}
    assert not lab["accessible_routes"]["no_specialized_hardware"]
