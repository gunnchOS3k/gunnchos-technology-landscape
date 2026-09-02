#!/usr/bin/env python3
"""Validate Gate 3 reader-review infrastructure.

Checks:
- reader_feedback_schema.yaml is loadable and has required keys
- REVIEW_SNAPSHOT.yaml points at a real git commit
- response YAML files (if any) roughly conform
- no synthetic fixture markers under publication/gates/gate-3/responses/
- analyze_reader_feedback reports NO_READER_EVIDENCE when responses empty
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

GATE3 = ROOT / "publication" / "gates" / "gate-3"
SCHEMA = GATE3 / "reader_feedback_schema.yaml"
SNAPSHOT = GATE3 / "REVIEW_SNAPSHOT.yaml"
RESPONSES = GATE3 / "responses"
SYNTHETIC_MARKERS = (
    "SYNTHETIC",
    "synthetic_fixture",
    "DO_NOT_USE_AS_EVIDENCE",
    "tests/fixtures",
)


def git_commit_exists(sha: str) -> bool:
    if not sha or not re.fullmatch(r"[0-9a-f]{7,40}", sha):
        return False
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-t", sha],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0 and proc.stdout.strip() == "commit"


def validate_schema(data: dict) -> list[str]:
    errs: list[str] = []
    if data.get("schema_id") != "gate3-reader-feedback-v1":
        errs.append("schema_id must be gate3-reader-feedback-v1")
    record = data.get("response_record")
    if not isinstance(record, dict):
        errs.append("response_record missing")
        return errs
    required = record.get("required")
    if not isinstance(required, list) or "review_id" not in required or "reader_level" not in required:
        errs.append("response_record.required must include review_id and reader_level")
    props = record.get("properties")
    if not isinstance(props, dict):
        errs.append("response_record.properties missing")
    else:
        for key in (
            "review_id",
            "reader_level",
            "date",
            "chapter_version",
            "lab_route",
            "comprehension",
            "teach_back",
            "figures",
            "lab",
            "terminology",
            "technical_accuracy",
            "accessibility",
            "revision_recommendations",
        ):
            if key not in props:
                errs.append(f"missing property description: {key}")
    return errs


def validate_snapshot(data: dict) -> list[str]:
    errs: list[str] = []
    if data.get("review_id") != "CH02-REVIEW-R1":
        errs.append("review_id must be CH02-REVIEW-R1 for this wave")
    sha = str(data.get("source_commit") or "")
    if not git_commit_exists(sha):
        errs.append(f"source_commit is not a real git commit: {sha!r}")
    if "READER_EVIDENCE_PENDING" not in str(data.get("gate_status") or ""):
        errs.append("gate_status must remain READER_EVIDENCE_PENDING during prep")
    return errs


def validate_response(path: Path, snapshot_id: str) -> list[str]:
    errs: list[str] = []
    data = load_yaml(path)
    if not isinstance(data, dict):
        return [f"{path.name}: not a mapping"]
    text = path.read_text(encoding="utf-8")
    for marker in SYNTHETIC_MARKERS:
        if marker in text:
            errs.append(f"{path.name}: synthetic marker {marker!r} forbidden in responses/")
    for key in ("review_id", "reader_level", "date", "chapter_version", "lab_route", "reviewer_code"):
        if key not in data:
            errs.append(f"{path.name}: missing required field {key}")
    if data.get("review_id") != snapshot_id:
        errs.append(f"{path.name}: review_id must match snapshot {snapshot_id}")
    level = data.get("reader_level")
    if level not in {"explorer", "builder", "engineer", "educator"}:
        errs.append(f"{path.name}: invalid reader_level {level!r}")
    for forbidden in ("password", "token", "device_serial", "precise_location"):
        if forbidden in data:
            errs.append(f"{path.name}: forbidden field {forbidden}")
    return errs


def scan_responses_for_synthetic() -> list[str]:
    errs: list[str] = []
    if not RESPONSES.is_dir():
        return [f"missing directory: {RESPONSES}"]
    for path in RESPONSES.rglob("*"):
        if not path.is_file():
            continue
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in SYNTHETIC_MARKERS:
            if marker in text:
                errs.append(f"synthetic content forbidden in {path.relative_to(ROOT)} ({marker})")
        # Any non-README file that looks like a test fixture dump
        if "SYNTHETIC_TEST_FIXTURE" in text:
            errs.append(f"synthetic fixture marker in {path.relative_to(ROOT)}")
    return errs


def analyze_no_evidence_when_empty() -> list[str]:
    from analyze_reader_feedback import NO_READER_EVIDENCE, analyze, response_files

    files = response_files(RESPONSES)
    result = analyze(RESPONSES)
    if files:
        # Real responses present — analysis must not claim NO_READER_EVIDENCE.
        if result.get("status") == NO_READER_EVIDENCE:
            return ["analysis incorrectly reports NO_READER_EVIDENCE while responses exist"]
        return []
    if result.get("status") != NO_READER_EVIDENCE:
        return [f"expected {NO_READER_EVIDENCE} while responses empty, got {result.get('status')!r}"]
    return []


def main() -> int:
    errors: list[str] = []
    if not SCHEMA.is_file():
        errors.append(f"missing {SCHEMA}")
    else:
        schema = load_yaml(SCHEMA)
        if not isinstance(schema, dict):
            errors.append("schema is not a mapping")
        else:
            errors.extend(validate_schema(schema))

    if not SNAPSHOT.is_file():
        errors.append(f"missing {SNAPSHOT}")
        snapshot_id = "CH02-REVIEW-R1"
    else:
        snap = load_yaml(SNAPSHOT)
        if not isinstance(snap, dict):
            errors.append("snapshot is not a mapping")
            snapshot_id = "CH02-REVIEW-R1"
        else:
            errors.extend(validate_snapshot(snap))
            snapshot_id = str(snap.get("review_id") or "CH02-REVIEW-R1")

    errors.extend(scan_responses_for_synthetic())

    if RESPONSES.is_dir():
        for path in sorted(RESPONSES.glob("RESP-*.yaml")):
            errors.extend(validate_response(path, snapshot_id))

    errors.extend(analyze_no_evidence_when_empty())

    if errors:
        print("validate_gate3_review: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("validate_gate3_review: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
