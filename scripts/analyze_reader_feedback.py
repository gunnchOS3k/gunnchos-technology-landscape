#!/usr/bin/env python3
"""Analyze Gate 3 reader feedback responses.

Reports NO_READER_EVIDENCE when no real response YAML files exist.
Never manufactures placeholder statistics.
Distinguishes missing optional fields from explicit zeros/false.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

DEFAULT_RESPONSES = ROOT / "publication" / "gates" / "gate-3" / "responses"
NO_READER_EVIDENCE = "NO_READER_EVIDENCE"


def response_files(responses_dir: Path) -> list[Path]:
    if not responses_dir.is_dir():
        return []
    return sorted(
        p
        for p in responses_dir.glob("RESP-*.yaml")
        if p.is_file()
    )


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def most_common_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(counter.most_common())


def analyze(responses_dir: Path) -> dict[str, Any]:
    files = response_files(responses_dir)
    if not files:
        return {
            "status": NO_READER_EVIDENCE,
            "n_responses": 0,
            "message": "No real response YAML files found under responses/.",
        }

    by_level: Counter[str] = Counter()
    lab_completed = 0
    lab_completed_observed = 0
    teach_completed = 0
    teach_completed_observed = 0
    confusing_terms: Counter[str] = Counter()
    most_helpful: Counter[str] = Counter()
    confusing_figs: Counter[str] = Counter()
    technical_issues: list[str] = []
    accessibility: list[str] = []
    revisions: list[str] = []
    missing_fields: Counter[str] = Counter()
    records: list[dict[str, Any]] = []

    for path in files:
        data = load_yaml(path)
        if not isinstance(data, dict):
            raise SystemExit(f"Invalid response (not a mapping): {path}")
        records.append(data)

        level = data.get("reader_level")
        if level:
            by_level[str(level)] += 1
        else:
            missing_fields["reader_level"] += 1

        lab = data.get("lab") if isinstance(data.get("lab"), dict) else {}
        if "completed" in lab:
            lab_completed_observed += 1
            if lab.get("completed") is True:
                lab_completed += 1
        else:
            missing_fields["lab.completed"] += 1

        tb = data.get("teach_back") if isinstance(data.get("teach_back"), dict) else {}
        if "completed" in tb:
            teach_completed_observed += 1
            if tb.get("completed") is True:
                teach_completed += 1
        else:
            missing_fields["teach_back.completed"] += 1

        figures = data.get("figures") if isinstance(data.get("figures"), dict) else {}
        if figures.get("most_helpful"):
            most_helpful[str(figures["most_helpful"])] += 1
        if figures.get("confusing"):
            confusing_figs[str(figures["confusing"])] += 1

        terms = data.get("terminology") if isinstance(data.get("terminology"), dict) else {}
        for term in _as_list(terms.get("confusing_terms")):
            if term:
                confusing_terms[str(term)] += 1

        tech = data.get("technical_accuracy") if isinstance(data.get("technical_accuracy"), dict) else {}
        for issue in _as_list(tech.get("issues")):
            if issue:
                technical_issues.append(str(issue))

        acc = data.get("accessibility") if isinstance(data.get("accessibility"), dict) else {}
        for obs in _as_list(acc.get("observations")):
            if obs:
                accessibility.append(str(obs))

        for rec in _as_list(data.get("revision_recommendations")):
            if rec:
                revisions.append(str(rec))

    return {
        "status": "OK",
        "n_responses": len(records),
        "n_by_reader_level": dict(by_level),
        "lab_completion": {
            "completed_true": lab_completed,
            "field_present": lab_completed_observed,
            "field_missing": missing_fields.get("lab.completed", 0),
            "note": "completed_true counts only explicit true; missing is not treated as false/zero success",
        },
        "teach_back_completion": {
            "completed_true": teach_completed,
            "field_present": teach_completed_observed,
            "field_missing": missing_fields.get("teach_back.completed", 0),
        },
        "confusing_terminology": most_common_dict(confusing_terms),
        "figures_most_helpful": most_common_dict(most_helpful),
        "figures_confusing": most_common_dict(confusing_figs),
        "technical_issues": technical_issues,
        "accessibility_observations": accessibility,
        "revision_themes": revisions,
        "missing_fields": dict(missing_fields),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--responses-dir", type=Path, default=DEFAULT_RESPONSES)
    parser.add_argument("--json", action="store_true", help="Emit JSON only")
    args = parser.parse_args(argv)

    result = analyze(args.responses_dir)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=False))
    else:
        if result["status"] == NO_READER_EVIDENCE:
            print(NO_READER_EVIDENCE)
            print(result["message"])
        else:
            print(json.dumps(result, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
