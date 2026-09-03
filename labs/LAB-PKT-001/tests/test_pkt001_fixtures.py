"""Fixture and contract tests for LAB-PKT-001."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
ROOT = LAB.parents[1]
FIXTURE_JSON = LAB / "fixtures" / "sample_path_trace.json"
FIXTURE_CSV = LAB / "fixtures" / "sample_timing_table.csv"
FIXTURE_MD = LAB / "fixtures" / "sample_observation.md"
REQUIRED_STATUSES = {
    "IMPLEMENTED_DIGITAL",
    "FIXTURE_VALIDATED",
    "PHYSICAL_PENDING",
    "EXTERNAL_DEPENDENCY",
}


def test_required_files_exist():
    for rel in [
        "lab.yaml",
        "README.md",
        "STATUS.yaml",
        "ACCESSIBILITY.md",
        "PRIVACY_AND_SAFETY.md",
        "browser/index.html",
        "cli/path_inspect.py",
        "fixtures/sample_path_trace.json",
        "fixtures/sample_timing_table.csv",
        "fixtures/sample_observation.md",
        "portfolio/README.md",
        "portfolio/diagram.md",
        "portfolio/observation_table.csv",
        "portfolio/reflection.md",
        "portfolio/teach_back.md",
        "portfolio/evidence/NOTE.md",
        "portfolio/evidence/FIXTURE_ROUTE_NOTE.md",
    ]:
        assert (LAB / rel).is_file(), rel


def test_status_labels_present():
    text = (LAB / "lab.yaml").read_text(encoding="utf-8")
    status = (LAB / "STATUS.yaml").read_text(encoding="utf-8")
    for label in REQUIRED_STATUSES:
        assert label in text
        assert label in status


def test_gate_note_not_pass():
    for rel in ("lab.yaml", "STATUS.yaml", "README.md"):
        text = (LAB / rel).read_text(encoding="utf-8")
        assert "GATE_3_IN_PROGRESS" in text
        assert "READER_EVIDENCE_PENDING" in text
        assert "GATE_3_PASS" not in text


def test_path_trace_fixture():
    data = json.loads(FIXTURE_JSON.read_text(encoding="utf-8"))
    assert data["lab_id"] == "LAB-PKT-001"
    assert data["label"] == "ILLUSTRATIVE_FIXTURE"
    assert "NOT" in data["honesty"].upper() or "not" in data["honesty"]
    assert data["frame"]["ethernet"]["ethertype"] == "0x0800"
    assert data["frame"]["ipv4"]["ttl"] == 64
    assert data["frame"]["ipv4"]["src"].startswith("192.0.2.")
    assert data["frame"]["ipv4"]["dst"].startswith("203.0.113.")
    for scope in ("device", "lan", "internet", "dns", "service"):
        assert scope in data["scopes"]
    assert data["access_network"]["mode"] == "wifi"
    assert data["placement_hypothesis"]["confidence"] == "inference"
    answers = {q["id"]: q["answer"] for q in data["parse_questions"]}
    assert answers["q_ttl"] == 64
    assert answers["q_ethertype"] is True
    assert answers["q_wifi_eq_internet"] is False
    assert answers["q_placement"] == "inference"


def test_timing_fixture_rows():
    with FIXTURE_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) >= 6
    for row in rows:
        assert row["label"] == "ILLUSTRATIVE_FIXTURE"
        assert row["access_mode"] in {"wifi", "cellular"}
        assert row["metric_family"] in {"latency", "throughput", "reliability"}
        assert row["phase"]
        # Ban bare PASS as evidence value
        assert row.get("ms", "").strip().upper() != "PASS"
        assert "PASS" not in row["phase"].upper()


def test_observation_fixture_honesty():
    text = FIXTURE_MD.read_text(encoding="utf-8")
    assert "ILLUSTRATIVE_FIXTURE" in text or "fixture" in text.lower()
    assert "not" in text.lower()
    assert "PASS" not in text.split()


def test_browser_a11y_hooks():
    html = (LAB / "browser" / "index.html").read_text(encoding="utf-8")
    assert 'aria-live="polite"' in html
    assert "accessMode" in html
    assert "Wi-Fi" in html and "Cellular" in html
    assert "EXTERNAL_DEPENDENCY" in html
    assert "password" not in html.lower() or "Do not enter secrets" in html


def test_privacy_safety_docs():
    privacy = (LAB / "PRIVACY_AND_SAFETY.md").read_text(encoding="utf-8")
    a11y = (LAB / "ACCESSIBILITY.md").read_text(encoding="utf-8")
    assert "other users" in privacy.lower() or "other users’" in privacy
    assert "fixture" in a11y.lower()
    assert "color" in a11y.lower()


def test_cli_fixture_runs():
    proc = subprocess.run(
        [sys.executable, str(LAB / "cli" / "path_inspect.py"), "--fixture", "--quiz", "--timing"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ILLUSTRATIVE_FIXTURE" in proc.stdout or "ttl=64" in proc.stdout
    assert "quiz_items_ready=" in proc.stdout
    assert "PASS" not in proc.stdout.split()


def test_lab_yaml_contract_keys():
    # Light structural check without requiring PyYAML in this isolated test path
    text = (LAB / "lab.yaml").read_text(encoding="utf-8")
    for key in (
        "lab_id:",
        "title:",
        "chapter:",
        "question:",
        "prerequisites:",
        "accessible_routes:",
        "prediction:",
        "procedure:",
        "evidence:",
        "interpretation:",
        "limits:",
        "portfolio:",
        "teach_back:",
        "no_specialized_hardware:",
        "observation_required:",
        "inference_required:",
        "causation_warning:",
    ):
        assert key in text
