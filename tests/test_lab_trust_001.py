#!/usr/bin/env python3
"""Validate LAB-TRUST-001 package structure, statuses, and safe fixtures."""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labs" / "LAB-TRUST-001"
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REQUIRED_FILES = [
    "lab.yaml",
    "README.md",
    "STATUS.md",
    "A11Y_PRIVACY_SAFETY.md",
    "browser/index.html",
    "local_app/trust_sim.py",
    "fixtures/route_l_transcript.md",
    "fixtures/route_c_transcript.md",
    "fixtures/sample_comparison_table.csv",
    "fixtures/sample_consent_card.md",
    "fixtures/sample_log_line.txt",
    "fixtures/safety_contract.yaml",
    "portfolio/README.md",
    "portfolio/comparison_table.csv",
    "portfolio/consent_trust_card.md",
    "portfolio/dual_ledger.md",
    "portfolio/uncertainty_note.md",
    "portfolio/diagram.md",
    "portfolio/reflection.md",
    "portfolio/teach_back.md",
    "portfolio/evidence/NOTE.md",
    "extensions/README.md",
]

REQUIRED_STATUS = {
    "IMPLEMENTED_DIGITAL",
    "FIXTURE_VALIDATED",
    "PHYSICAL_PENDING",
    "EXTERNAL_DEPENDENCY",
}

LAB_YAML_REQUIRED = [
    "lab_id",
    "title",
    "chapter",
    "question",
    "prerequisites",
    "accessible_routes",
    "prediction",
    "procedure",
    "evidence",
    "interpretation",
    "limits",
    "portfolio",
    "teach_back",
    "status_tags",
    "routes",
    "concepts_taught",
]

FIXTURE_SCAN_FILES = [
    "fixtures/route_l_transcript.md",
    "fixtures/route_c_transcript.md",
    "fixtures/sample_comparison_table.csv",
    "fixtures/sample_consent_card.md",
    "fixtures/sample_log_line.txt",
]


def test_required_files_exist():
    missing = [rel for rel in REQUIRED_FILES if not (LAB / rel).exists()]
    assert not missing, f"missing files: {missing}"


def test_lab_yaml_contract():
    lab = load_yaml(LAB / "lab.yaml")
    for key in LAB_YAML_REQUIRED:
        assert key in lab, f"lab.yaml missing {key}"
    assert lab["lab_id"] == "LAB-TRUST-001"
    assert lab["chapter"] == "CE-5"
    assert set(lab["status_tags"]) == REQUIRED_STATUS
    routes = lab.get("accessible_routes") or {}
    assert routes.get("no_specialized_hardware") is True
    assert routes.get("supplied_trace") is True
    interp = lab.get("interpretation") or {}
    for k in ("observation_required", "inference_required", "causation_warning"):
        assert interp.get(k) is True
    assert (lab.get("evidence") or {}).get("required_artifacts")
    assert "GATE_3_IN_PROGRESS" in lab.get("gate_posture", "")
    assert "READER_EVIDENCE_PENDING" in lab.get("gate_posture", "")


def test_status_doc_lists_tags():
    text = (LAB / "STATUS.md").read_text(encoding="utf-8")
    for tag in REQUIRED_STATUS:
        assert tag in text


def test_a11y_privacy_safety_doc():
    text = (LAB / "A11Y_PRIVACY_SAFETY.md").read_text(encoding="utf-8")
    for needle in ("Accessibility", "Privacy", "Safety", "keyboard", "fixture"):
        assert needle.lower() in text.lower()
    assert "GATE_3_IN_PROGRESS" in text


def test_fixtures_labeled_and_safe():
    contract = load_yaml(LAB / "fixtures" / "safety_contract.yaml")
    patterns = [re.compile(p, re.I) for p in contract["patterns"]]
    for rel in FIXTURE_SCAN_FILES:
        text = (LAB / rel).read_text(encoding="utf-8")
        if rel.endswith(".md"):
            assert "FIXTURE" in text or "illustrative" in text.lower()
        for pat in patterns:
            assert not pat.search(text), f"{rel} matched forbidden pattern {pat.pattern}"


def test_comparison_fixture_csv():
    path = LAB / "fixtures" / "sample_comparison_table.csv"
    with path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) >= 2
    routes = {r["route"] for r in rows}
    assert "Route L" in routes and "Route C" in routes


def test_consent_card_fields():
    text = (LAB / "fixtures" / "sample_consent_card.md").read_text(encoding="utf-8")
    for field in ("Audience", "Purpose", "Data classes", "Retention", "Opt-out", "AI disclosure"):
        assert field in text


def test_browser_a11y_hooks():
    html = (LAB / "browser" / "index.html").read_text(encoding="utf-8")
    assert 'lang="en"' in html
    assert "aria-live" in html
    assert "aria-label" in html
    assert "Do not enter secrets" in html or "No real secrets" in html
    assert "IMPLEMENTED_DIGITAL" in html


def test_local_sim_offline_and_refuses_freeform():
    script = LAB / "local_app" / "trust_sim.py"
    ok = subprocess.run(
        [sys.executable, str(script), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert ok.returncode == 0, ok.stderr
    assert "SIMULATED_LOCAL_INFERENCE" in ok.stdout
    assert "network_required" in ok.stdout
    bad = subprocess.run(
        [sys.executable, str(script), "--question", "here is my password=hunter2"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert bad.returncode != 0
    assert "safe practical question" in (bad.stderr + bad.stdout).lower() or "Refusing" in (
        bad.stderr + bad.stdout
    )


def test_concepts_taught_cover_brief():
    lab = load_yaml(LAB / "lab.yaml")
    blob = " ".join(lab.get("concepts_taught") or []).lower()
    for needle in (
        "data",
        "model",
        "inference",
        "local",
        "remote",
        "authentication",
        "authorization",
        "lifecycle",
        "privacy",
        "least privilege",
        "uncertainty",
    ):
        assert needle in blob, f"concepts_taught missing {needle}"


def test_lab_registry_not_required_for_this_wave():
    """LAB_PLAN: do not invent registry coupling in this agent wave."""
    reg = load_yaml(ROOT / "labs" / "lab_registry.yaml")
    ids = {item["lab_id"] for item in reg.get("labs") or []}
    # Soft expectation: TAP remains; TRUST may be absent until integrator wave.
    assert "LAB-TAP-001" in ids
