"""Tests for Gate 3 reader-feedback analysis using synthetic fixtures only."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_reader_feedback import NO_READER_EVIDENCE, analyze  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "reader_feedback"
RESPONSES = ROOT / "publication" / "gates" / "gate-3" / "responses"


def test_empty_publication_responses_report_no_evidence():
    result = analyze(RESPONSES)
    assert result["status"] == NO_READER_EVIDENCE
    assert result["n_responses"] == 0


def test_analyze_synthetic_fixtures_dir(tmp_path: Path):
    # Copy synthetic fixtures into a temp dir with RESP- names
    for src in FIXTURES.glob("SYNTHETIC_*.yaml"):
        level = "explorer"
        if "builder" in src.name:
            level = "builder"
        elif "engineer" in src.name:
            level = "engineer"
        dest = tmp_path / f"RESP-{level}-synthetic.yaml"
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    result = analyze(tmp_path)
    assert result["status"] == "OK"
    assert result["n_responses"] == 3
    assert result["n_by_reader_level"]["explorer"] == 1
    assert result["n_by_reader_level"]["builder"] == 1
    assert result["n_by_reader_level"]["engineer"] == 1
    # Explicit true completions only
    assert result["lab_completion"]["completed_true"] == 2
    assert result["lab_completion"]["field_missing"] == 1
    assert result["teach_back_completion"]["completed_true"] == 2
    assert "interrupt" in result["confusing_terminology"]
    assert result["figures_most_helpful"]["FIG-CH02-001"] == 1
    assert any("scheduling" in x for x in result["technical_issues"])


def test_cli_no_evidence_on_publication_dir():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "analyze_reader_feedback.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert NO_READER_EVIDENCE in proc.stdout


def test_synthetic_fixtures_not_in_publication_responses():
    pub_files = list(RESPONSES.glob("*.yaml")) if RESPONSES.is_dir() else []
    assert pub_files == []
    for path in FIXTURES.glob("*.yaml"):
        text = path.read_text(encoding="utf-8")
        assert "SYNTHETIC_TEST_FIXTURE" in text
        assert "DO_NOT_USE_AS_EVIDENCE" in text
