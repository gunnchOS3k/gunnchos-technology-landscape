"""Tests for Prompt 28 human-validation launch prep freezes + intake."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)


def test_adult_review_freeze_valid() -> None:
    proc = run([sys.executable, "scripts/validate_full31_review_r1_freeze.py"])
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "FULL31_REVIEW_R1_FREEZE_VALID" in proc.stdout
    assert "NO_REVIEW_RESPONSES_YET" in proc.stdout


def test_kids_review_freeze_valid() -> None:
    proc = run([sys.executable, "scripts/validate_kids_family_review_r1_freeze.py"])
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "KIDS_FAMILY_REVIEW_R1_FREEZE_VALID" in proc.stdout
    assert "NO_CHILD_VALIDATION_EVIDENCE" in proc.stdout


def test_review_intake_empty() -> None:
    for cmd in ("schema-check", "coverage-report", "integrity-check"):
        proc = run([sys.executable, "scripts/review_intake.py", cmd])
        assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (ROOT / "publication/reviews/REVIEW_ISSUES.yaml").exists()
    assert (ROOT / "kids/reviews/REVIEW_ISSUES.yaml").exists()


def test_pre_review_untouched() -> None:
    assert (ROOT / "publication/review-candidates/FULL31-PRE-REVIEW-001/CANDIDATE_PROVENANCE.yaml").is_file()
    assert (ROOT / "publication/review-candidates/FULL31-REVIEW-R1/CANDIDATE_PROVENANCE.yaml").is_file()


def test_no_fabricated_gate3_pass() -> None:
    text = (ROOT / "publication/review-candidates/FULL31-REVIEW-R1/README.md").read_text(encoding="utf-8")
    assert "NO HUMAN VALIDATION HAS OCCURRED" in text
    assert "GATE_3_PASS" not in text
