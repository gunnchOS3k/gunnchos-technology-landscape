#!/usr/bin/env python3
"""Validate FULL31-REVIEW-R1 freeze immutability + honesty sentinels.

Prints FULL31_REVIEW_R1_FREEZE_VALID on success.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "publication/review-candidates/FULL31-REVIEW-R1"
PROVENANCE = CANDIDATE / "CANDIDATE_PROVENANCE.yaml"
PRE_REVIEW = ROOT / "publication/review-candidates/FULL31-PRE-REVIEW-001"

sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

REQUIRED = [
    "README.md",
    "SOURCE_COMMIT.txt",
    "CANDIDATE_PROVENANCE.yaml",
    "CHAPTER_MANIFEST.yaml",
    "FRONT_BACK_MATTER_MANIFEST.yaml",
    "BIBLIOGRAPHY_HASH.txt",
    "FIGURE_MANIFEST.yaml",
    "LAB_REGISTRY_HASH.txt",
    "GLOSSARY_TERMINOLOGY_HASH.txt",
    "WAIKE_SOURCE_SHA.txt",
    "DEVICE_QUARTET_PHYSICAL_PENDING.md",
    "KNOWN_ISSUES_SUMMARY.md",
    "ARTIFACT_MANIFEST.yaml",
    "BUILD_TOOL_VERSIONS.yaml",
]

REQUIRED_LABELS = [
    "FULL31-REVIEW-R1",
    "HUMAN REVIEW CANDIDATE",
    "NO HUMAN VALIDATION HAS OCCURRED",
    "NOT PUBLICATION-READY",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    errors: list[str] = []
    print("validate_full31_review_r1_freeze:")

    if not PRE_REVIEW.is_dir():
        errors.append("historical FULL31-PRE-REVIEW-001 missing")

    if not CANDIDATE.is_dir():
        errors.append(f"missing candidate {CANDIDATE.relative_to(ROOT)}")
        for e in errors:
            print(f"  FAIL: {e}")
        return 1

    for rel in REQUIRED:
        if not (CANDIDATE / rel).is_file():
            errors.append(f"missing {rel}")

    readme = (CANDIDATE / "README.md").read_text(encoding="utf-8") if (CANDIDATE / "README.md").exists() else ""
    for label in REQUIRED_LABELS:
        if label not in readme:
            errors.append(f"README missing label: {label}")

    prov = load_yaml(PROVENANCE) or {} if PROVENANCE.exists() else {}
    if prov.get("candidate_id") != "FULL31-REVIEW-R1":
        errors.append("candidate_id must be FULL31-REVIEW-R1")
    if prov.get("human_validation_status") != "NOT_RUN":
        errors.append("human_validation_status must be NOT_RUN")
    if prov.get("gate_3_status") != "READER_EVIDENCE_PENDING":
        errors.append("gate_3_status must be READER_EVIDENCE_PENDING")
    if prov.get("publication_status") != "NOT_PUBLICATION_READY":
        errors.append("publication_status must be NOT_PUBLICATION_READY")
    if int(prov.get("response_count") or 0) != 0:
        errors.append("response_count must be 0")

    src = (CANDIDATE / "SOURCE_COMMIT.txt").read_text(encoding="utf-8").strip() if (CANDIDATE / "SOURCE_COMMIT.txt").exists() else ""
    if src and prov.get("verified_candidate_content_sha") and src != prov.get("verified_candidate_content_sha"):
        errors.append("SOURCE_COMMIT.txt != verified_candidate_content_sha")

    # Drift: recompute chapter manifest hash from frozen file vs provenance
    ch_path = CANDIDATE / "CHAPTER_MANIFEST.yaml"
    if ch_path.exists() and prov.get("chapter_manifest_sha256"):
        live = sha256_text(ch_path.read_text(encoding="utf-8"))
        if live != prov["chapter_manifest_sha256"]:
            errors.append("chapter_manifest_sha256 drift vs frozen CHAPTER_MANIFEST.yaml")

    # Live chapter files must match frozen manifest entries
    if ch_path.exists():
        man = load_yaml(ch_path) or {}
        chapters = man.get("chapters") or []
        if len(chapters) != 31:
            errors.append(f"chapter count {len(chapters)} != 31")
        for ch in chapters:
            rel = ch.get("path")
            expected = ch.get("sha256")
            if not rel or not expected:
                errors.append(f"chapter entry incomplete: {ch.get('chapter_id')}")
                continue
            p = ROOT / rel
            if not p.is_file():
                errors.append(f"missing live chapter {rel}")
            elif sha256_file(p) != expected:
                errors.append(f"chapter content drift: {rel} (requires R2+ candidate)")

    # No fabricated responses
    resp = CANDIDATE / "responses"
    if resp.is_dir():
        bad = [p for p in resp.rglob("*") if p.is_file() and p.name != ".gitkeep"]
        # allow only empty placeholders / README saying empty
        for p in bad:
            if p.suffix.lower() in {".yaml", ".yml", ".json"}:
                errors.append(f"forbidden response artifact: {p.relative_to(ROOT)}")
            text = p.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"finding_id|overall_completion_state:\s*COMPLETE", text):
                errors.append(f"possible fabricated response content: {p.relative_to(ROOT)}")

    forbidden_claims = re.compile(
        r"GATE_3_PASS|HUMAN_VALIDATED\s*=\s*31/31|PUBLICATION_READY\s*=\s*31/31",
        re.I,
    )
    for p in CANDIDATE.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml", ".txt"}:
            if forbidden_claims.search(p.read_text(encoding="utf-8", errors="ignore")):
                errors.append(f"forbidden validation claim in {p.relative_to(ROOT)}")

    if errors:
        for e in errors:
            print(f"  FAIL: {e}")
        return 1

    print("  FULL31_REVIEW_R1_FREEZE_VALID")
    print("  NO_REVIEW_RESPONSES_YET")
    print("  GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
