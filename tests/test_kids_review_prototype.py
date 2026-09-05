"""Negative and semantic tests for kids review-prototype child-facing meta guards."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "scripts" / "validate_kids_review_prototype.py"


def _load():
    spec = importlib.util.spec_from_file_location("validate_kids_review_prototype", MOD_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_extract_child_facing_blocks_only():
    mod = _load()
    sample = """
```
KIDS DEVELOPMENTAL PROTOTYPE
NOT CHILD-VALIDATED
NOT PUBLICATION-READY
```

**Child-facing text:** Hello world for kids.

**Talk together:** This is a developmental prototype for reviewers.
"""
    blocks = mod.extract_child_facing_blocks(sample)
    assert blocks == ["Hello world for kids."]
    assert not mod.find_child_facing_project_meta(sample)


def test_banner_meta_outside_child_facing_allowed():
    mod = _load()
    sample = """
```
KIDS DEVELOPMENTAL PROTOTYPE
NOT CHILD-VALIDATED
NOT PUBLICATION-READY
```

**Child-facing text:** Tap and watch the change.
"""
    assert mod.find_child_facing_project_meta(sample) == []


def test_negative_child_validated_phrase_fails():
    mod = _load()
    sample = (
        "**Child-facing text:** Say aloud that this is not child-validated and not publication-ready.\n\n"
        "**Talk together:** ok\n"
    )
    hits = mod.find_child_facing_project_meta(sample)
    assert hits, "expected project-meta hit in child-facing block"
    assert any("child-validated" in h.lower() or "publication" in h.lower() for h in hits)


def test_negative_adult_chapter_prose_fails():
    mod = _load()
    sample = (
        "**Child-facing text:** Do not copy adult chapter prose; define words with examples.\n\n"
    )
    hits = mod.find_child_facing_project_meta(sample)
    joined = " ".join(hits).lower()
    assert hits
    assert "do not copy adult" in joined or "adult chapter prose" in joined


def test_negative_developmental_prototype_in_body_fails():
    mod = _load()
    sample = (
        "**Child-facing text:** This is a kids developmental prototype for learning.\n\n"
    )
    hits = mod.find_child_facing_project_meta(sample)
    assert hits


def test_negative_magic_megahertz_fails():
    mod = _load()
    sample = "**Child-facing text:** We do not invent magic megahertz.\n\n"
    hits = mod.find_child_facing_project_meta(sample)
    assert any("megahertz" in h.lower() for h in hits)


def test_legitimate_vocab_not_flagged():
    mod = _load()
    sample = (
        "**Child-facing text:** Ask what was actually measured. "
        "This activity is for practice, not for ranking anyone. "
        "Do not invent evidence.\n\n"
    )
    assert mod.find_child_facing_project_meta(sample) == []


def test_live_elem2_child_facing_clean_after_closure():
    mod = _load()
    ms = ROOT / "kids" / "pilots" / "ONE_TAP" / "KIDS-ELEM2" / "MANUSCRIPT.md"
    if not ms.is_file():
        return
    hits = mod.find_child_facing_project_meta(ms.read_text(encoding="utf-8"))
    assert hits == [], f"unexpected child-facing project meta: {hits}"


def test_live_elem1_child_facing_clean_after_closure():
    mod = _load()
    ms = ROOT / "kids" / "pilots" / "ONE_TAP" / "KIDS-ELEM1" / "MANUSCRIPT.md"
    if not ms.is_file():
        return
    hits = mod.find_child_facing_project_meta(ms.read_text(encoding="utf-8"))
    assert hits == [], f"unexpected child-facing project meta: {hits}"
