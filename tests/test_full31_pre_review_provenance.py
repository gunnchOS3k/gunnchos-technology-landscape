"""Negative / positive tests for Full31 pre-review provenance freeze."""
from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_pre_review_check_script_exists():
    assert (ROOT / "scripts/full31_pre_review_check.py").is_file()
    assert (ROOT / "scripts/build_full31_pre_review_candidate.py").is_file()


def test_provenance_allowlist_rejects_chapter_change(tmp_path, monkeypatch):
    """Simulate that a chapter path after content SHA is not allowlisted."""
    # Import allowlist from the checker module
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "full31_pre_review_check",
        ROOT / "scripts/full31_pre_review_check.py",
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    prefixes = mod.PROVENANCE_ALLOWLIST_PREFIXES
    assert not any(
        "book/chapters/ch12/chapter.md".startswith(p) for p in prefixes
    )
    assert any(
        "publication/review-candidates/FULL31-PRE-REVIEW-001/README.md".startswith(p)
        for p in prefixes
    )


def test_source_commit_policy_mentions_verified_sha():
    builder = (ROOT / "scripts/build_full31_pre_review_candidate.py").read_text(
        encoding="utf-8"
    )
    assert "verified_candidate_content_sha" in builder
    assert "--content-sha" in builder
