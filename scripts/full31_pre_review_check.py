#!/usr/bin/env python3
"""Validate Full31 pre-human-review candidate readiness.

Requires:
  - QUALITY_ISSUES.yaml present with open BLOCKER=0 and open MAJOR=0
  - review-candidate package present with required manifests
  - Gate 3 tree unchanged vs accepted main
  - No fabricated human validation claims in candidate package
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUALITY_ISSUES = ROOT / "publication/full31/quality/QUALITY_ISSUES.yaml"
CANDIDATE = ROOT / "publication/review-candidates/FULL31-PRE-REVIEW-001"
ACCEPTED_MAIN = "76bee2e67c35ff445f46c83af30809e5b307f06e"

sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REQUIRED_CANDIDATE_FILES = [
    "README.md",
    "SOURCE_COMMIT.txt",
    "CHAPTER_MANIFEST.yaml",
    "BIBLIOGRAPHY_HASH.txt",
    "FIGURE_MANIFEST.yaml",
    "LAB_REGISTRY_HASH.txt",
    "GLOSSARY_TERMINOLOGY_HASH.txt",
    "WAIKE_SOURCE_SHA.txt",
    "DEVICE_QUARTET_PHYSICAL_PENDING.md",
    "KNOWN_ISSUES_SUMMARY.md",
    "ARTIFACT_MANIFEST.yaml",
    "REVIEW_ROLE_PLAN.md",
]


def gate3_unchanged() -> tuple[bool, str]:
    try:
        out = subprocess.check_output(
            ["git", "diff", ACCEPTED_MAIN, "--", "publication/gates/gate-3/"],
            cwd=ROOT,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        return False, f"git diff failed: {exc}"
    if out.strip():
        return False, "publication/gates/gate-3/ differs from accepted main"
    return True, "empty diff vs accepted main"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-candidate",
        action="store_true",
        default=True,
        help="Require FULL31-PRE-REVIEW-001 package (default)",
    )
    parser.add_argument(
        "--allow-missing-candidate",
        action="store_true",
        help="Only enforce QUALITY_ISSUES open BLOCKER/MAJOR gates",
    )
    args = parser.parse_args()
    errors: list[str] = []

    if not QUALITY_ISSUES.exists():
        errors.append(f"missing {QUALITY_ISSUES.relative_to(ROOT)}")
    else:
        data = load_yaml(QUALITY_ISSUES) or {}
        issues = data.get("issues") or []
        summary = data.get("summary") or {}
        open_blocker = sum(
            1
            for i in issues
            if i.get("severity") == "BLOCKER" and i.get("fix_status") == "OPEN"
        )
        open_major = sum(
            1
            for i in issues
            if i.get("severity") == "MAJOR" and i.get("fix_status") == "OPEN"
        )
        # prefer live recount over stale summary
        print("full31_pre_review_check:")
        print(f"  open_blocker: {open_blocker} (summary={summary.get('open_blocker')})")
        print(f"  open_major: {open_major} (summary={summary.get('open_major')})")
        if open_blocker:
            errors.append(f"open BLOCKER count is {open_blocker}, require 0")
            for i in issues:
                if i.get("severity") == "BLOCKER" and i.get("fix_status") == "OPEN":
                    errors.append(f"  BLOCKER {i.get('issue_id')}: {i.get('finding')}")
        if open_major:
            errors.append(f"open MAJOR count is {open_major}, require 0")
            for i in issues:
                if i.get("severity") == "MAJOR" and i.get("fix_status") == "OPEN":
                    errors.append(f"  MAJOR {i.get('issue_id')}: {str(i.get('finding'))[:160]}")

    ok, msg = gate3_unchanged()
    print(f"  gate3_diff: {msg}")
    if not ok:
        errors.append(msg)

    require_cand = args.require_candidate and not args.allow_missing_candidate
    if require_cand:
        if not CANDIDATE.is_dir():
            errors.append(f"missing candidate dir {CANDIDATE.relative_to(ROOT)}")
        else:
            for name in REQUIRED_CANDIDATE_FILES:
                if not (CANDIDATE / name).exists():
                    errors.append(f"missing candidate file {name}")
            readme = (CANDIDATE / "README.md").read_text(encoding="utf-8") if (CANDIDATE / "README.md").exists() else ""
            if "PRE-HUMAN-REVIEW CANDIDATE" not in readme:
                errors.append("candidate README missing PRE-HUMAN-REVIEW CANDIDATE label")
            if "NO HUMAN VALIDATION HAS OCCURRED" not in readme:
                errors.append("candidate README missing NO HUMAN VALIDATION HAS OCCURRED label")
            forbidden_claims = [
                "GATE_3_PASS",
                "HUMAN_VALIDATED = 31/31",
                "PUBLICATION_READY = 31/31",
            ]
            blob = "\n".join(
                p.read_text(encoding="utf-8", errors="replace")
                for p in CANDIDATE.rglob("*")
                if p.is_file() and p.suffix in {".md", ".yaml", ".txt", ".yml"}
            )
            for token in forbidden_claims:
                if token in blob:
                    errors.append(f"candidate package contains forbidden claim/token: {token}")
            # Do not allow this package to present itself as the human review freeze.
            if re.search(
                r"(?i)this package is\s+FULL31-REVIEW-R1|named\s+FULL31-REVIEW-R1",
                blob,
            ):
                errors.append("candidate package must not claim to be FULL31-REVIEW-R1")

    if errors:
        print("full31_pre_review_check: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("full31_pre_review_check: PASS")
    print("NOTE: PASS means automated pre-review gates only — not human validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
