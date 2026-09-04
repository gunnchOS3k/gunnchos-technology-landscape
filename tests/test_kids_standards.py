"""Tests for Kids Global Standards Atlas validators."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_kids_standards_validate_passes():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_kids_standards.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
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
    ]:
        assert (base / name).is_file(), name


def test_regional_slices_exist():
    regional = ROOT / "kids" / "standards" / "regional"
    for name in ["americas.yaml", "europe.yaml", "africa.yaml", "middle_east.yaml", "asia_pacific.yaml"]:
        assert (regional / name).is_file(), name
