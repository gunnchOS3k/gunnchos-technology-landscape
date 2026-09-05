#!/usr/bin/env python3
"""Validate KIDS-FAMILY-REVIEW-R1 freeze immutability + honesty sentinels.

Prints KIDS_FAMILY_REVIEW_R1_FREEZE_VALID on success.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "kids/review-candidates/KIDS-FAMILY-REVIEW-R1"
PROVENANCE = CANDIDATE / "CANDIDATE_PROVENANCE.yaml"
BOOKS_ROOT = ROOT / "kids/books"

sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

BOOK_IDS = [
    "KIDS-BABY",
    "KIDS-TODDLER",
    "KIDS-PRESCHOOL",
    "KIDS-PREK",
    "KIDS-ELEM1",
    "KIDS-ELEM2",
]
SUBCANDIDATES = {
    "KIDS-BABY": "KIDS-BABY-R1",
    "KIDS-TODDLER": "KIDS-TODDLER-R1",
    "KIDS-PRESCHOOL": "KIDS-PRESCHOOL-R1",
    "KIDS-PREK": "KIDS-PREK-R1",
    "KIDS-ELEM1": "KIDS-ELEM1-R1",
    "KIDS-ELEM2": "KIDS-ELEM2-R1",
}

REQUIRED_LABELS = [
    "KIDS FULL FAMILY HUMAN REVIEW CANDIDATE",
    "NOT CHILD-VALIDATED",
    "NOT PUBLICATION-READY",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    errors: list[str] = []
    print("validate_kids_family_review_r1_freeze:")

    if not CANDIDATE.is_dir():
        print(f"  FAIL: missing {CANDIDATE.relative_to(ROOT)}")
        return 1

    readme = (CANDIDATE / "README.md").read_text(encoding="utf-8") if (CANDIDATE / "README.md").exists() else ""
    for label in REQUIRED_LABELS:
        if label not in readme:
            errors.append(f"README missing label: {label}")

    prov = load_yaml(PROVENANCE) or {} if PROVENANCE.exists() else {}
    if prov.get("candidate_id") != "KIDS-FAMILY-REVIEW-R1":
        errors.append("candidate_id must be KIDS-FAMILY-REVIEW-R1")
    if prov.get("child_validation_status") != "NOT_RUN":
        errors.append("child_validation_status must be NOT_RUN")
    if prov.get("publication_status") != "NOT_PUBLICATION_READY":
        errors.append("publication_status must be NOT_PUBLICATION_READY")
    if prov.get("stage_2_status") != "PROTOCOL_PREPARED_NOT_EXECUTED":
        errors.append("stage_2_status must be PROTOCOL_PREPARED_NOT_EXECUTED")
    if int(prov.get("response_count") or 0) != 0:
        errors.append("response_count must be 0")
    if int(prov.get("book_count") or 0) != 6:
        errors.append("book_count must be 6")

    books = prov.get("books") or {}
    total_units = 0
    for book_id in BOOK_IDS:
        sub = SUBCANDIDATES[book_id]
        sub_dir = CANDIDATE / sub
        if not sub_dir.is_dir():
            errors.append(f"missing subcandidate {sub}")
            continue
        ms = sub_dir / "BOOK_MANUSCRIPT.md"
        live = BOOKS_ROOT / book_id / "BOOK_MANUSCRIPT.md"
        if not ms.is_file():
            errors.append(f"{sub}: missing frozen BOOK_MANUSCRIPT.md")
        if not live.is_file():
            errors.append(f"{book_id}: missing live BOOK_MANUSCRIPT.md")
        elif ms.is_file() and sha256_file(ms) != sha256_file(live):
            errors.append(f"{book_id}: manuscript drift vs freeze (requires R2+)")
        bp = books.get(book_id) or {}
        expected = bp.get("manuscript_sha256")
        if expected and live.is_file() and sha256_file(live) != expected:
            errors.append(f"{book_id}: provenance manuscript_sha256 drift")
        # unit counts from frozen UNIT_REGISTRY
        ureg = sub_dir / "UNIT_REGISTRY.yaml"
        if ureg.exists():
            u = load_yaml(ureg) or {}
            units = len(u.get("units") or u.get("unit_registry") or [])
            if units == 0 and isinstance(u.get("units_by_strand"), dict):
                for v in u["units_by_strand"].values():
                    if isinstance(v, list):
                        units += len(v)
            total_units += units
            if units != 7:
                errors.append(f"{book_id}: expected 7 units, found {units}")

    if total_units and total_units != 42:
        errors.append(f"total units {total_units} != 42")

    # Empty responses
    resp = CANDIDATE / "responses"
    if resp.is_dir():
        for p in resp.rglob("*"):
            if p.is_file() and p.name != ".gitkeep":
                if p.suffix.lower() in {".yaml", ".yml", ".json"}:
                    errors.append(f"forbidden response artifact: {p.relative_to(ROOT)}")

    forbidden = re.compile(
        r"CHILD[- ]VALIDATED\s*=\s*YES|CHILD_VALIDATION_COMPLETE|PUBLICATION_READY\b(?!\s*=\s*0)",
        re.I,
    )
    for p in CANDIDATE.rglob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        # allow explicit NOT CHILD-VALIDATED / NOT PUBLICATION-READY
        cleaned = text.replace("NOT CHILD-VALIDATED", "").replace("NOT PUBLICATION-READY", "")
        cleaned = cleaned.replace("NOT_PUBLICATION_READY", "")
        if forbidden.search(cleaned) and "NOT_RUN" not in text:
            if re.search(r"\bCHILD_VALIDATION_COMPLETE\b|\bCHILD-VALIDATED\b", cleaned):
                errors.append(f"forbidden child-validation claim in {p.relative_to(ROOT)}")

    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        return 1

    print("  KIDS_FAMILY_REVIEW_R1_FREEZE_VALID")
    print("  NO_CHILD_VALIDATION_EVIDENCE")
    print("  NO_REVIEW_RESPONSES_YET")
    print("  KIDS_CHILD_VALIDATION_PENDING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
