"""Fixture and contract validation for LAB-CMS-001."""
from __future__ import annotations

import csv
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

LAB_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_ROOT.parents[1]
CONTRACT = REPO_ROOT / "labs" / "contracts" / "ce_lab_contract.schema.yaml"
LAB_YAML = LAB_ROOT / "lab.yaml"

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


def _load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover
        pytest.skip(f"PyYAML required: {exc}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_contract_schema_exists_and_lists_status_vocabulary():
    assert CONTRACT.is_file(), "ce_lab_contract.schema.yaml must exist"
    text = CONTRACT.read_text(encoding="utf-8")
    for status in ALLOWED_STATUS:
        assert status in text
    assert "PASS" in text  # disallowed list documents PASS
    data = _load_yaml(CONTRACT)
    assert "PASS" in (data.get("disallowed_status") or [])


def test_lab_yaml_matches_contract_and_legacy_keys():
    lab = _load_yaml(LAB_YAML)
    for key in REQUIRED_CONTRACT_FIELDS:
        assert key in lab, f"missing contract field: {key}"
    assert lab["lab_id"] == "LAB-CMS-001"
    assert lab["chapter"] == "CE-3"
    assert lab["fixture_available"] is True

    statuses = lab["status"]
    if isinstance(statuses, str):
        statuses = [statuses]
    assert set(statuses) <= ALLOWED_STATUS
    assert "IMPLEMENTED_DIGITAL" in statuses
    assert "FIXTURE_VALIDATED" in statuses
    assert "PHYSICAL_PENDING" in statuses
    assert "PASS" not in statuses

    # Legacy validate_labs-compatible sections
    for key in (
        "title",
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
    ):
        assert key in lab, f"missing legacy field: {key}"
    assert lab["accessible_routes"].get("no_specialized_hardware") is True
    interp = lab["interpretation"]
    assert interp.get("observation_required") is True
    assert interp.get("inference_required") is True
    assert interp.get("causation_warning") is True


def test_required_files_present():
    required = [
        "README.md",
        "lab.yaml",
        "routes/commodity_computer.md",
        "local_app/safe_snapshot.py",
        "fixtures/FIG-CE3-009-monitor-transcript.md",
        "fixtures/sample_top_transcript.txt",
        "fixtures/sample_observation_table.csv",
        "fixtures/README.md",
        "portfolio/README.md",
        "portfolio/observation_table.csv",
        "portfolio/teach_back.md",
        "portfolio/hierarchy_map.md",
        "portfolio/diagnosis_plan.md",
        "portfolio/hypothesis_note.md",
        "portfolio/facilitation_sheet.md",
        "portfolio/evidence/NOTE.md",
    ]
    missing = [rel for rel in required if not (LAB_ROOT / rel).is_file()]
    assert not missing, f"missing files: {missing}"


def test_fixture_observation_table_has_observation_inference_column():
    path = LAB_ROOT / "fixtures" / "sample_observation_table.csv"
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows, "fixture table must not be empty"
    assert "observation_or_inference" in rows[0]
    kinds = {r["observation_or_inference"] for r in rows}
    assert "observation" in kinds
    assert "inference" in kinds
    # Thrashing must not be asserted as bare observation
    for row in rows:
        if row.get("metric") == "thrashing":
            assert row["observation_or_inference"] == "inference"


def test_fixture_transcript_teaches_core_concepts():
    text = (LAB_ROOT / "fixtures" / "FIG-CE3-009-monitor-transcript.md").read_text(
        encoding="utf-8"
    )
    for needle in (
        "CPU",
        "RAM",
        "storage",
        "Process",
        "schedule",
        "thrashing",
        "thermal",
    ):
        assert needle.lower() in text.lower()
    assert "FIG-CE3-009" in text


def test_readme_privacy_safety_accessibility():
    readme = (LAB_ROOT / "README.md").read_text(encoding="utf-8")
    for needle in ("Privacy", "Safety", "accessibility", "fixture", "commodity"):
        assert needle.lower() in readme.lower()
    assert "Gate 3 PASS" not in readme or "does **not** claim Gate 3 PASS" in readme
    assert "GATE_3_IN_PROGRESS" in readme


def test_safe_snapshot_runs_and_fixture_demo():
    script = LAB_ROOT / "local_app" / "safe_snapshot.py"
    demo = subprocess.run(
        [sys.executable, str(script), "--fixture-demo"],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert demo.returncode == 0, demo.stdout + demo.stderr
    assert "fixture_fallback" in demo.stdout
    assert "FIXTURE_VALIDATED" in demo.stdout

    live = subprocess.run(
        [sys.executable, str(script), "--label", "before", "--json"],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert live.returncode == 0, live.stdout + live.stderr
    assert "cpu_percent" in live.stdout
    # Reject fabricated numeric thermal fields; educational notes may mention thermal limits.
    assert '"temperature"' not in live.stdout.lower()
    assert "thermal_celsius" not in live.stdout.lower()


def test_safe_snapshot_module_importable():
    script = LAB_ROOT / "local_app" / "safe_snapshot.py"
    spec = importlib.util.spec_from_file_location("lab_cms_safe_snapshot", script)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    snap = mod.take_snapshot("unit")
    assert snap.label == "unit"
    assert snap.cpu_percent == mod.UNAVAILABLE or isinstance(snap.cpu_percent, (int, float))


def test_no_gate3_or_review_paths_modified_by_package_layout():
    """Package must not ship gate-3 or CH02 review mutations."""
    forbidden_names = ("gate-3", "CH02-REVIEW-R1", "gate_3")
    for path in LAB_ROOT.rglob("*"):
        joined = "/".join(path.parts)
        for bad in forbidden_names:
            assert bad not in joined
