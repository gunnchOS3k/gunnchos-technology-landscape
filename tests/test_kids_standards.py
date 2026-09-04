"""Tests for Kids Global Standards Atlas validators."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(*args: str):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_kids_standards.py"), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_kids_standards_validate_passes():
    result = _run("--architecture")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_kids_standards_research_complete_passes_when_nyr_zero():
    result = _run("--research-complete", "--metrics")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout
    assert "NYR=0" in result.stdout


def test_kids_standards_pilot_mapped_passes():
    result = _run("--pilot-mapped")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS" in result.stdout


def test_required_artifacts_exist():
    base = ROOT / "kids" / "standards"
    for name in [
        "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml",
        "GLOBAL_STANDARDS_SOURCE_REGISTER.yaml",
        "GLOBAL_STANDARDS_ATLAS.yaml",
        "GLOBAL_STANDARDS_COVERAGE_REPORT.md",
        "STANDARD_MAPPING_SCHEMA.md",
        "WIRE_HOOK_REGISTRY.yaml",
    ]:
        assert (base / name).is_file(), name


def test_regional_slices_exist():
    regional = ROOT / "kids" / "standards" / "regional"
    for name in ["americas.yaml", "europe.yaml", "africa.yaml", "middle_east.yaml", "asia_pacific.yaml"]:
        assert (regional / name).is_file(), name
