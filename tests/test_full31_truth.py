#!/usr/bin/env python3
"""Negative / positive tests for Full31 truth closure."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_source_identified_without_evidence_rejected(tmp_path: Path):
    common = _load("full31_common", "scripts/full31_common.py")
    bad = tmp_path / "CLAIM_PLAN.yaml"
    bad.write_text(
        """
schema_version: 1.0.0
chapter_id: CH99
claims:
  - provisional_id: CLM-BAD
    text: Something
    claim_class: general_technical
    evidence_required: needed
    status: SOURCE_IDENTIFIED
    citation_keys: []
    overclaim_risk: risk
    wording_boundary: boundary
""",
        encoding="utf-8",
    )
    errs = common.validate_claim_plan(bad)
    assert any("SOURCE_IDENTIFIED requires" in e for e in errs)


def test_unknown_claim_class_rejected(tmp_path: Path):
    common = _load("full31_common", "scripts/full31_common.py")
    bad = tmp_path / "CLAIM_PLAN.yaml"
    bad.write_text(
        """
schema_version: 1.0.0
chapter_id: CH99
claims:
  - provisional_id: CLM-BAD
    text: Something
    claim_class: policy
    evidence_required: needed
    status: SOURCE_NEEDED
    citation_keys: []
    overclaim_risk: risk
    wording_boundary: boundary
""",
        encoding="utf-8",
    )
    errs = common.validate_claim_plan(bad)
    assert any("unknown claim_class" in e for e in errs)


def test_derive_current_state_not_blind_complete():
    common = _load("full31_common", "scripts/full31_common.py")
    ch = {
        "canonical_prose_state": "SCAFFOLD",
        "concept_preproduction_state": "PREPRODUCTION_COMPLETE",
        "source_state": "PREPRODUCTION_STARTED",
        "claim_state": "PREPRODUCTION_STARTED",
        "figure_state": "PREPRODUCTION_COMPLETE",
        "lab_state": "PREPRODUCTION_STARTED",
        "glossary_state": "PREPRODUCTION_COMPLETE",
        "waike_state": "PREPRODUCTION_COMPLETE",
        "gate_dependencies": [],
        "human_dependencies": [],
    }
    assert common.derive_current_state(ch) == "PREPRODUCTION_STARTED"


def test_ch02_human_validation_pending():
    common = _load("full31_common", "scripts/full31_common.py")
    ch = {
        "canonical_prose_state": "DRAFT_COMPLETE",
        "concept_preproduction_state": "DRAFT_COMPLETE",
        "source_state": "DRAFT_COMPLETE",
        "claim_state": "HUMAN_VALIDATION_PENDING",
        "figure_state": "DRAFT_COMPLETE",
        "lab_state": "DRAFT_COMPLETE",
        "glossary_state": "DRAFT_COMPLETE",
        "waike_state": "PREPRODUCTION_COMPLETE",
        "gate_dependencies": ["CH02-REVIEW-R1 reader responses REQUIRED"],
        "human_dependencies": ["Explorer / Builder / Engineer reviews"],
    }
    assert common.derive_current_state(ch) == "HUMAN_VALIDATION_PENDING"


def test_waike_aggregation_exact_zero_and_deterministic():
    common = _load("full31_common", "scripts/full31_common.py")
    a = common.aggregate_all_waike()
    b = common.aggregate_all_waike()
    assert a["totals"] == b["totals"]
    assert a["totals"]["exact"] == 0
    assert a["unique_upstream_waike_objects"] == b["unique_upstream_waike_objects"]


def test_ieee80211_classified_as_standard():
    mod = _load("validate_ce_sources", "scripts/validate_ce_sources.py")
    entry = {
        "key": "ieee80211-2020",
        "entry_type": "misc",
        "title": "IEEE Standard for Information Technology 802.11",
        "howpublished": "IEEE Std 802.11-2020 listing",
        "url": "https://standards.ieee.org/standard/802_11-2020.html",
        "year": "2020",
    }
    assert mod.classify_bib(entry) == "standards_specifications"


def test_wcag_dated_editions_remain_distinct():
    mod = _load("validate_ce_sources", "scripts/validate_ce_sources.py")
    a = {
        "key": "wcag22-20231005",
        "year": "2023",
        "url": "https://www.w3.org/TR/2023/REC-WCAG22-20231005/",
        "howpublished": "W3C Recommendation",
    }
    b = {
        "key": "wcag22-20241212",
        "year": "2024",
        "url": "https://www.w3.org/TR/2024/REC-WCAG22-20241212/",
        "howpublished": "W3C Recommendation",
    }
    assert mod.canonical_identifier(a) != mod.canonical_identifier(b)


def test_midword_title_cut_detected():
    mod = _load("validate_visual_text_integrity", "scripts/validate_visual_text_integrity.py")
    assert mod.midword_cut(
        "FIG-CE4-003 — Separate Wi-Fi access, cellular access, and Internet backbone as diffe",
        "FIG-CE4-003: Separate Wi-Fi access, cellular access, and Internet backbone as different boxes.",
    )
    assert not mod.midword_cut(
        "FIG-CE4-003 — Access vs backbone layers",
        "FIG-CE4-003: Separate Wi-Fi access, cellular access, and Internet backbone as different boxes.",
    )
