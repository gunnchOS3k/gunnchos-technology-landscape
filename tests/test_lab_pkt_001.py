"""Repo-level pytest wrapper for LAB-PKT-001."""
from __future__ import annotations

import importlib.util
from pathlib import Path

LAB_TEST = (
    Path(__file__).resolve().parents[1]
    / "labs"
    / "LAB-PKT-001"
    / "tests"
    / "test_pkt001_fixtures.py"
)


def _load():
    spec = importlib.util.spec_from_file_location("pkt001_fixtures", LAB_TEST)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_lab = _load()

test_required_files_exist = _lab.test_required_files_exist
test_status_labels_present = _lab.test_status_labels_present
test_gate_note_not_pass = _lab.test_gate_note_not_pass
test_path_trace_fixture = _lab.test_path_trace_fixture
test_timing_fixture_rows = _lab.test_timing_fixture_rows
test_observation_fixture_honesty = _lab.test_observation_fixture_honesty
test_browser_a11y_hooks = _lab.test_browser_a11y_hooks
test_privacy_safety_docs = _lab.test_privacy_safety_docs
test_cli_fixture_runs = _lab.test_cli_fixture_runs
test_lab_yaml_contract_keys = _lab.test_lab_yaml_contract_keys
