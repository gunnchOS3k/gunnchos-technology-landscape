from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run_draft_check(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(ROOT / "scripts" / "validate_full31_draft.py"), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_full31_draft_check_infra_passes():
    proc = run_draft_check("--mode", "infra")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "full31-draft-check: PASS" in proc.stdout
    assert "mode=infra" in proc.stdout
    assert "DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT" in proc.stdout
    assert "GATE_3_IN_PROGRESS" in proc.stdout


def test_full31_draft_check_strict_passes_when_manuscript_complete():
    """After all 31 working drafts land, strict mode must PASS (no scaffold leftover)."""
    proc = run_draft_check("--mode", "strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "full31-draft-check: PASS" in proc.stdout
    assert "structure_complete: 31/31" in proc.stdout
    assert "WORKING_DRAFT_COMPLETE criteria satisfied" in proc.stdout


def test_validation_sequence_decision_exists():
    path = ROOT / "publication/full31/VALIDATION_SEQUENCE_DECISION.md"
    text = path.read_text(encoding="utf-8")
    assert "DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT" in text
    assert "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING" in text
    assert "FULL31-REVIEW-R1" in text
    assert "CH02-REVIEW-R1" in text


def test_publication_banner_present():
    meta = (ROOT / "book/metadata.yaml").read_text(encoding="utf-8")
    status = (ROOT / "book/frontmatter/status.qmd").read_text(encoding="utf-8")
    for line in (
        "WORKING FULL-MANUSCRIPT DRAFT",
        "Human reader validation pending.",
        "Technical/editorial revision pending.",
        "Not publication-ready.",
    ):
        assert line in meta or line in status


def test_quarto_lists_all_31_chapters():
    yml = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
    for n in range(1, 32):
        assert f"book/chapters/ch{n:02d}/chapter.md" in yml


def test_render_full31_artifact_names():
    script = (ROOT / "scripts/render_full31.sh").read_text(encoding="utf-8")
    assert "technology-landscape-full31-html" in script
    assert "technology-landscape-full31-pdf" in script
    assert "technology-landscape-full31-epub" in script
