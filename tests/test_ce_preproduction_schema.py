"""Regression tests: CE preproduction schema rejects legacy drift patterns."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "ce_preproduction_invalid"
sys.path.insert(0, str(ROOT / "scripts"))

spec = importlib.util.spec_from_file_location(
    "validate_ce_preproduction",
    ROOT / "scripts" / "validate_ce_preproduction.py",
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def _load(name: str):
    from yaml_util import load_yaml

    return load_yaml(FIXTURES / name)


def test_rejects_verified_status():
    errs = mod.validate_claims("fixture", _load("claim_status_verified.yaml"))
    assert any("verified" in e and "forbidden" in e for e in errs)


def test_rejects_planned_status():
    errs = mod.validate_claims("fixture", _load("claim_status_planned.yaml"))
    assert any("planned" in e and "forbidden" in e for e in errs)


def test_rejects_nodes_collection():
    errs = mod.validate_concepts("fixture", _load("concept_nodes_collection.yaml"))
    assert any("nodes" in e and "forbidden" in e for e in errs)


def test_rejects_truth_class_field():
    errs = mod.validate_figures("fixture", _load("figure_truth_class_field.yaml"))
    assert any("truth_class" in e and "forbidden" in e for e in errs)


def test_rejects_conceptual_vs_measured_field():
    errs = mod.validate_figures("fixture", _load("figure_conceptual_vs_measured_field.yaml"))
    assert any("conceptual_vs_measured" in e and "forbidden" in e for e in errs)


def test_rejects_missing_provisional_id():
    errs = mod.validate_claims("fixture", _load("claim_missing_provisional_id.yaml"))
    assert any("provisional_id" in e and "missing" in e for e in errs)


def test_rejects_missing_status():
    errs = mod.validate_claims("fixture", _load("claim_missing_status.yaml"))
    assert any("status" in e and "missing" in e for e in errs)


def test_rejects_unknown_claim_class():
    errs = mod.validate_claims("fixture", _load("claim_unknown_class.yaml"))
    assert any("claim_class" in e and "unknown" in e for e in errs)


def test_rejects_unknown_truth_enum():
    errs = mod.validate_figures("fixture", _load("figure_unknown_truth_enum.yaml"))
    assert any("truth_classification" in e and "unknown" in e for e in errs)


def test_live_packages_pass_and_indexes_stable():
    assert mod.main() == 0
    import subprocess

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "regenerate_ce_candidate_indexes.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_synthetic_fixtures_not_in_publication_preproduction():
    markers = ("SYNTHETIC_TEST_FIXTURE", "DO_NOT_USE_AS_EVIDENCE")
    for path in (ROOT / "publication" / "preproduction").rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in markers:
            assert marker not in text, path
    # Live claim plans must not retain legacy statuses.
    for ce in ("ce-01", "ce-03", "ce-04", "ce-05", "ce-06"):
        text = (ROOT / "publication" / "preproduction" / ce / "CLAIM_PLAN.yaml").read_text(
            encoding="utf-8"
        )
        assert "\nstatus: verified\n" not in text
        assert "\nstatus: planned\n" not in text
        assert "\nnodes:\n" not in (
            ROOT / "publication" / "preproduction" / ce / "CONCEPT_GRAPH.yaml"
        ).read_text(encoding="utf-8")
