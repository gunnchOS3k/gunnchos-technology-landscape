"""Fixture and contract validation for LAB-SYS-001 (systems readiness lab)."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labs" / "LAB-SYS-001"
CONTRACT = ROOT / "labs" / "contracts" / "ce_lab_contract.schema.yaml"
ALLOWED_STATUS = {
    "IMPLEMENTED_DIGITAL",
    "FIXTURE_VALIDATED",
    "PHYSICAL_PENDING",
    "EXTERNAL_DEPENDENCY",
}
REQUIRED_CONTRACT_FIELDS = [
    "lab_id",
    "chapter",
    "version",
    "status",
    "reader_levels",
    "routes",
    "fixture_available",
    "evidence_artifacts",
    "privacy_boundary",
    "safety_boundary",
    "accessibility_notes",
    "observation_inference_boundary",
    "portfolio_output",
]


def _load_lab() -> dict:
    return yaml.safe_load((LAB / "lab.yaml").read_text(encoding="utf-8"))


def test_contract_schema_file_exists():
    assert CONTRACT.is_file()
    schema = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert "required_fields" in schema
    assert "PASS" in (schema.get("forbidden_status") or [])
    for field in REQUIRED_CONTRACT_FIELDS:
        assert field in schema["required_fields"]


def test_lab_yaml_matches_contract_fields():
    lab = _load_lab()
    for field in REQUIRED_CONTRACT_FIELDS:
        assert field in lab, f"missing contract field: {field}"
    assert lab["lab_id"] == "LAB-SYS-001"
    assert lab["chapter"] in {"CH01", "CE-1", "CE1"}
    assert lab["status"] in ALLOWED_STATUS
    assert lab["status"] != "PASS"
    assert lab["fixture_available"] is True
    assert "explorer" in lab["reader_levels"]
    assert "researcher" in lab["reader_levels"]
    routes = lab["routes"]
    assert "browser" in routes
    assert "local" in routes
    assert "fixture_offline" in routes


def test_not_duplicate_of_lab_tap_001():
    lab = _load_lab()
    tap = yaml.safe_load((ROOT / "labs/LAB-TAP-001/lab.yaml").read_text(encoding="utf-8"))
    assert lab["question"] != tap["question"]
    assert lab.get("not_a_duplicate_of") == "LAB-TAP-001"
    text = (LAB / "README.md").read_text(encoding="utf-8").lower()
    assert "tap-to-response" in text or "lab-tap-001" in text
    assert "chrome" in text and "content" in text


def test_fixture_readiness_demo_exists_and_is_offline_capable():
    fixture = LAB / "fixtures" / "readiness_demo.html"
    assert fixture.is_file()
    html = fixture.read_text(encoding="utf-8")
    assert "chrome visible" in html.lower() or "chrome" in html.lower()
    assert "content usable" in html.lower() or "content failed" in html.lower()
    assert "Simulate offline" in html or "offline" in html.lower()
    assert "aria-live" in html
    assert "fixture" in html.lower()
    # Must not be a tap-timer clone
    assert "Fetch remote sample" not in html
    assert "Local only" not in html


def test_browser_route_exists():
    browser = LAB / "browser" / "index.html"
    assert browser.is_file()
    html = browser.read_text(encoding="utf-8")
    assert "LAB-SYS-001" in html
    assert "aria-live" in html
    assert "Simulate offline" in html


def test_scenario_card_labeled_fixture():
    card = (LAB / "fixtures" / "scenario_card.md").read_text(encoding="utf-8").lower()
    assert "fixture" in card
    assert "illustrative" in card
    assert "not measured" in card or "not measured device evidence" in card


def test_sample_observation_table_fixture():
    csv_path = LAB / "fixtures" / "sample_observation_table.csv"
    text = csv_path.read_text(encoding="utf-8")
    assert "chrome_visible" in text
    assert "observation" in text
    assert "inference" in text


def test_local_observation_sheet_runs():
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, str(LAB / "local" / "observation_sheet.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "chrome" in proc.stdout.lower()
    assert "LAB-SYS-001" in proc.stdout
    assert "tap-to-response" in proc.stdout.lower() or "NOT tap" in proc.stdout


def test_portfolio_templates_present():
    for rel in [
        "portfolio/README.md",
        "portfolio/readiness_observation_table.csv",
        "portfolio/ecosystem_map.md",
        "portfolio/observation_vs_inference.md",
        "portfolio/teach_back.md",
        "portfolio/evidence/NOTE.md",
    ]:
        assert (LAB / rel).is_file(), rel


def test_registry_lists_lab_sys_001():
    reg = yaml.safe_load((ROOT / "labs/lab_registry.yaml").read_text(encoding="utf-8"))
    ids = [item["lab_id"] for item in reg.get("labs") or []]
    assert "LAB-SYS-001" in ids
    entry = next(i for i in reg["labs"] if i["lab_id"] == "LAB-SYS-001")
    assert entry.get("fixture_available") is True
    assert entry.get("no_specialized_hardware") is True


def test_validate_labs_still_passes():
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_labs.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
