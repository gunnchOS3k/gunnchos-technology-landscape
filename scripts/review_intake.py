#!/usr/bin/env python3
"""Review response schema, coverage, integrity, and ingest helpers.

Honesty rules:
- Empty issues/responses are correct before human review.
- Do not auto-resolve findings.
- Reject obvious PII in child response artifacts.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

ADULT_ISSUES = ROOT / "publication/reviews/REVIEW_ISSUES.yaml"
KIDS_ISSUES = ROOT / "kids/reviews/REVIEW_ISSUES.yaml"
ADULT_COVERAGE = ROOT / "publication/reviews/ADULT_REVIEW_COVERAGE_MATRIX.yaml"
KIDS_COVERAGE = ROOT / "kids/reviews/KIDS_REVIEW_COVERAGE_MATRIX.yaml"
ADULT_RESPONSES = ROOT / "publication/reviews/responses"
KIDS_RESPONSES = ROOT / "kids/reviews/responses"
ADULT_CANDIDATE_RESP = ROOT / "publication/review-candidates/FULL31-REVIEW-R1/responses"
KIDS_CANDIDATE_RESP = ROOT / "kids/review-candidates/KIDS-FAMILY-REVIEW-R1/responses"

SEVERITIES = {"BLOCKER", "MAJOR", "MODERATE", "MINOR", "EDITORIAL"}
STATUSES = {"OPEN", "FIXED", "DEFERRED_HUMAN_REVIEW", "DEFERRED_PHYSICAL_EVIDENCE", "NOT_AN_ISSUE"}
CATEGORIES = {
    "TECHNICAL",
    "CLARITY",
    "DEVELOPMENTAL",
    "PEDAGOGY",
    "ACCESSIBILITY",
    "SAFETY",
    "PRIVACY",
    "CULTURAL",
    "VISUAL",
    "NAVIGATION",
    "LAB_ACTIVITY",
    "STANDARDS",
    "TERMINOLOGY",
    "EVIDENCE",
    "PRINT",
}

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b")
# Crude address heuristic: number + street suffix
ADDRESS_RE = re.compile(
    r"\b\d{1,5}\s+\w+(?:\s\w+){0,3}\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b",
    re.I,
)


def response_files(roots: list[Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.name != ".gitkeep" and p.suffix.lower() in {".yaml", ".yml"}:
                files.append(p)
    return files


def validate_response_doc(path: Path, errors: list[str], *, child_context: bool) -> None:
    data = load_yaml(path) or {}
    required = [
        "review_id",
        "candidate_id",
        "reviewer_role",
        "scope",
        "overall_completion_state",
        "findings",
    ]
    for key in required:
        if key not in data:
            errors.append(f"{path}: missing field {key}")
    findings = data.get("findings")
    if findings is None:
        return
    if not isinstance(findings, list):
        errors.append(f"{path}: findings must be a list")
        return
    for i, f in enumerate(findings):
        if not isinstance(f, dict):
            errors.append(f"{path}: finding[{i}] must be object")
            continue
        for key in ("finding_id", "location", "severity", "category", "observation"):
            if not f.get(key):
                errors.append(f"{path}: finding[{i}] missing {key}")
        if f.get("severity") and f["severity"] not in SEVERITIES:
            errors.append(f"{path}: finding[{i}] bad severity {f.get('severity')}")
        if f.get("category") and f["category"] not in CATEGORIES:
            errors.append(f"{path}: finding[{i}] bad category {f.get('category')}")
    if child_context:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if EMAIL_RE.search(text):
            errors.append(f"{path}: CHILD_SENSITIVE email-like content rejected")
        if PHONE_RE.search(text):
            errors.append(f"{path}: CHILD_SENSITIVE phone-like content rejected")
        if ADDRESS_RE.search(text):
            errors.append(f"{path}: CHILD_SENSITIVE address-like content rejected")


def validate_issues(path: Path, errors: list[str]) -> int:
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return 0
    data = load_yaml(path) or {}
    issues = data.get("issues")
    if issues is None:
        errors.append(f"{path}: missing issues array")
        return 0
    if not isinstance(issues, list):
        errors.append(f"{path}: issues must be a list")
        return 0
    for i, issue in enumerate(issues):
        if not isinstance(issue, dict):
            errors.append(f"{path}: issue[{i}] must be object")
            continue
        for key in ("source_review_id", "source_finding_id", "candidate_id", "status", "severity"):
            if not issue.get(key):
                errors.append(f"{path}: issue[{i}] missing {key}")
        if issue.get("status") and issue["status"] not in STATUSES:
            errors.append(f"{path}: issue[{i}] bad status")
        if issue.get("severity") and issue["severity"] not in SEVERITIES:
            errors.append(f"{path}: issue[{i}] bad severity")
    return len(issues)


def schema_check() -> int:
    errors: list[str] = []
    adult_files = response_files([ADULT_RESPONSES, ADULT_CANDIDATE_RESP])
    kids_files = response_files([KIDS_RESPONSES, KIDS_CANDIDATE_RESP])
    for p in adult_files:
        validate_response_doc(p, errors, child_context=False)
    for p in kids_files:
        validate_response_doc(p, errors, child_context=True)
    # Always validate empty issues files exist and are valid
    validate_issues(ADULT_ISSUES, errors)
    validate_issues(KIDS_ISSUES, errors)
    # Form schemas must exist
    for rel in (
        "publication/reviews/forms/RESPONSE_SCHEMA.yaml",
        "kids/reviews/forms/RESPONSE_SCHEMA.yaml",
    ):
        if not (ROOT / rel).is_file():
            errors.append(f"missing {rel}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("review-response-schema-check: PASS")
    print(f"  adult_response_files: {len(adult_files)}")
    print(f"  kids_response_files: {len(kids_files)}")
    return 0


def coverage_report() -> int:
    errors: list[str] = []
    if not ADULT_COVERAGE.exists():
        errors.append("missing adult coverage matrix")
    else:
        data = load_yaml(ADULT_COVERAGE) or {}
        chapters = data.get("chapters") or []
        if len(chapters) != 31:
            errors.append(f"adult chapters tracked {len(chapters)} != 31")
        completed = 0
        planned = 0
        for ch in chapters:
            state = str(ch.get("response_state") or "")
            if state in {"COMPLETE", "RESPONDED"}:
                completed += 1
            if state in {"PLANNED", "ASSIGNED", "NOT_ASSIGNED", "COMPLETE", "RESPONDED"}:
                planned += 1
            roles = ch.get("planned_roles") or []
            if not roles:
                errors.append(f"chapter {ch.get('chapter_id')} missing planned_roles")
        print("adult coverage:")
        print(f"  chapters: {len(chapters)}")
        print(f"  planned_rows: {planned}")
        print(f"  actual_responses_complete: {completed}")
        if completed != 0:
            # Not an error forever — but for prep wave we expect 0
            print("  note: some chapters marked complete — verify real responses exist")

    if not KIDS_COVERAGE.exists():
        errors.append("missing kids coverage matrix")
    else:
        data = load_yaml(KIDS_COVERAGE) or {}
        books = data.get("books") or []
        units = data.get("units") or []
        print("kids coverage:")
        print(f"  books: {len(books)}")
        print(f"  units: {len(units)}")
        if len(books) != 6:
            errors.append(f"kids books {len(books)} != 6")
        if len(units) != 42:
            errors.append(f"kids units {len(units)} != 42")
        completed = sum(1 for u in units if str(u.get("response_state")) in {"COMPLETE", "RESPONDED"})
        print(f"  actual_unit_responses_complete: {completed}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("review-coverage-report: PASS")
    return 0


def integrity_check() -> int:
    errors: list[str] = []
    adult_n = validate_issues(ADULT_ISSUES, errors)
    kids_n = validate_issues(KIDS_ISSUES, errors)
    adult_files = response_files([ADULT_RESPONSES, ADULT_CANDIDATE_RESP])
    kids_files = response_files([KIDS_RESPONSES, KIDS_CANDIDATE_RESP])

    # No issue may claim review received without a response file
    for path, files in ((ADULT_ISSUES, adult_files), (KIDS_ISSUES, kids_files)):
        if not path.exists():
            continue
        data = load_yaml(path) or {}
        known_ids = set()
        for f in files:
            doc = load_yaml(f) or {}
            if doc.get("review_id"):
                known_ids.add(doc["review_id"])
        for issue in data.get("issues") or []:
            rid = issue.get("source_review_id")
            if rid and rid not in known_ids:
                errors.append(
                    f"{path.name}: issue cites source_review_id={rid} without response file"
                )

    if adult_n == 0 and kids_n == 0 and not adult_files and not kids_files:
        print("NO_REVIEW_RESPONSES_YET")
    else:
        print(f"adult_issues={adult_n} kids_issues={kids_n}")
        print(f"adult_responses={len(adult_files)} kids_responses={len(kids_files)}")

    # Child PII scan on any kids response-like yaml under kids/reviews
    for p in kids_files:
        validate_response_doc(p, errors, child_context=True)

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    print("review-integrity-check: PASS")
    print("NO_CHILD_VALIDATION_EVIDENCE")
    return 0


def ingest(path: Path, family: str) -> int:
    """Derive issue stubs from a sanitized response file (does not auto-resolve)."""
    errors: list[str] = []
    child = family == "kids"
    validate_response_doc(path, errors, child_context=child)
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1
    data = load_yaml(path) or {}
    issues_path = KIDS_ISSUES if child else ADULT_ISSUES
    store = load_yaml(issues_path) or {"schema_version": 1, "issues": []}
    existing = store.setdefault("issues", [])
    existing_ids = {(i.get("source_review_id"), i.get("source_finding_id")) for i in existing}
    added = 0
    for f in data.get("findings") or []:
        key = (data.get("review_id"), f.get("finding_id"))
        if key in existing_ids:
            continue
        existing.append(
            {
                "issue_id": f"REV-{data.get('review_id')}-{f.get('finding_id')}",
                "source_review_id": data.get("review_id"),
                "source_finding_id": f.get("finding_id"),
                "candidate_id": data.get("candidate_id"),
                "severity": f.get("severity"),
                "category": f.get("category"),
                "location": f.get("location"),
                "summary": f.get("observation"),
                "status": "OPEN",
                "adjudication": None,
            }
        )
        added += 1
    issues_path.parent.mkdir(parents=True, exist_ok=True)
    issues_path.write_text(dump_yaml(store), encoding="utf-8")
    print(f"ingest: added {added} issues into {issues_path.relative_to(ROOT)}")
    print("note: findings are not auto-resolved")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("schema-check")
    sub.add_parser("coverage-report")
    sub.add_parser("integrity-check")
    ing = sub.add_parser("ingest")
    ing.add_argument("response_path")
    ing.add_argument("--family", choices=["adult", "kids"], required=True)
    args = parser.parse_args()
    if args.cmd == "schema-check":
        return schema_check()
    if args.cmd == "coverage-report":
        return coverage_report()
    if args.cmd == "integrity-check":
        return integrity_check()
    if args.cmd == "ingest":
        return ingest(Path(args.response_path), args.family)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
