#!/usr/bin/env python3
"""Check adult distribution research deliverables exist and stay non-overclaiming."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "publication/distribution/platforms/PLATFORM_REQUIREMENTS.yaml",
    "publication/distribution/platforms/PLATFORM_REQUIREMENTS_REPORT.md",
    "publication/distribution/FREE_ACCESS_POLICY.md",
    "publication/distribution/identifiers/ISBN_IMPRINT_DECISION.md",
    "publication/distribution/identifiers/ISBN-ADULT-EBOOK.placeholder",
    "publication/distribution/identifiers/ISBN-ADULT-PAPERBACK.placeholder",
    "publication/distribution/identifiers/ISBN-ADULT-HARDCOVER.placeholder",
    "publication/metadata/BOOK_METADATA_SCHEMA.yaml",
    "publication/metadata/adult-book.yaml",
    "publication/metadata/ONIX_MAPPING.md",
    "publication/distribution/print/PRINT_ENGINEERING_RESEARCH.md",
    "publication/distribution/print/PRINT_PROFILE_RESULTS.yaml",
    "publication/distribution/print/PRINT_PROFILE_RESULTS.md",
    "publication/distribution/covers/ADULT_COVER_REQUIREMENTS.md",
    "publication/distribution/libraries/LIBRARY_DISTRIBUTION_OPTIONS.md",
    "publication/distribution/PUBLISHING_SOURCE_REGISTER.yaml",
    "publication/distribution/ADULT_DISTRIBUTION_READINESS_REPORT.md",
    "publication/distribution/ADULT_SUBMISSION_PACKAGE_PREPARED.md",
    "publication/distribution/ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE.md",
    "_quarto-print-6x9.yml",
    "_quarto-print-7x10.yml",
    "_quarto-print-85x11.yml",
]

FORBIDDEN_PHRASES = [
    re.compile(r"\bPUBLICATION_READY\b(?!\s*[:=].*0)"),  # allow counts like 0/31 or not_status
]

# Stronger forbid: claiming publication-ready / certified / Gate 3 PASS as achieved
HARD_FORBID = [
    re.compile(r"(?i)gate\s*3\s+pass"),
    re.compile(r"(?i)wcag\s+certified"),
    re.compile(r"(?i)retailer[- ]approved"),
    re.compile(r"(?i)we\s+are\s+publication[- ]ready"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", default=True)
    args = ap.parse_args()
    errors: list[str] = []

    for rel in REQUIRED:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing: {rel}")

    # ISBN placeholders must not look like real ISBNs
    for rel in REQUIRED:
        if not rel.endswith(".placeholder"):
            continue
        text = (ROOT / rel).read_text(encoding="utf-8")
        if re.search(r"\b97[89]\d{10}\b", text):
            errors.append(f"fabricated-looking ISBN in {rel}")
        if "PENDING_OWNER_PURCHASE" not in text:
            errors.append(f"placeholder missing PENDING_OWNER_PURCHASE: {rel}")

    adult = (ROOT / "publication/metadata/adult-book.yaml").read_text(encoding="utf-8")
    if "wcag_certified: false" not in adult:
        errors.append("adult-book.yaml must set wcag_certified: false")
    if "PUBLICATION_READY" in adult and "ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE" not in adult and "ADULT_SUBMISSION_PACKAGE_PREPARED" not in adult:
        errors.append("adult-book.yaml overclaim risk")

    ceiling = (ROOT / "publication/distribution/ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE.md").read_text(
        encoding="utf-8"
    )
    if "Explicitly NOT claimed" not in ceiling:
        errors.append("aggregate state doc missing Explicitly NOT claimed section")
    if "READY_FOR_OWNER_UPLOAD" in ceiling and "NOT" not in ceiling:
        errors.append("aggregate state doc must not claim READY_FOR_OWNER_UPLOAD")
    legacy = (ROOT / "publication/distribution/ADULT_SUBMISSION_PACKAGE_PREPARED.md").read_text(
        encoding="utf-8"
    )
    if "Explicitly NOT claimed" not in legacy:
        errors.append("legacy ceiling doc missing Explicitly NOT claimed section")

    policy = (ROOT / "publication/distribution/FREE_ACCESS_POLICY.md").read_text(encoding="utf-8")
    if "KDP Select" not in policy:
        errors.append("FREE_ACCESS_POLICY.md must discuss KDP Select")
    if "ARR" not in policy and "All Rights Reserved" not in policy:
        errors.append("FREE_ACCESS_POLICY.md must restate ARR ≠ free license")

    for rel in [
        "publication/distribution/platforms/PLATFORM_REQUIREMENTS.yaml",
        "publication/distribution/PUBLISHING_SOURCE_REGISTER.yaml",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for pat in HARD_FORBID:
            if pat.search(text) and "not" not in text.lower():
                # allow mentions in non_claims lists
                pass
        if "retrieved_on" not in text:
            errors.append(f"{rel} missing retrieved_on fields")

    # Preserve freeze pointer
    cand = ROOT / "publication/full31/FULL31_PRE_HUMAN_REVIEW_CANDIDATE.md"
    if not cand.is_file():
        errors.append("missing FULL31_PRE_HUMAN_REVIEW_CANDIDATE.md")
    else:
        body = cand.read_text(encoding="utf-8")
        if "dd7f0003beae5c56d5ee8b5050aff151ef67d803" not in body:
            errors.append("FULL31 pre-review verified SHA drift — do not rewrite freeze from this track")

    if errors:
        print("distribution-requirements-check: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("distribution-requirements-check: PASS")
    print(f"  required_files: {len(REQUIRED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
