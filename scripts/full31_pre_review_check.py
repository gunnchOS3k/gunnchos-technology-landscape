#!/usr/bin/env python3
"""Validate Full31 pre-human-review candidate readiness + provenance freeze.

Requires:
  - QUALITY_ISSUES.yaml with open BLOCKER=0, open MAJOR=0, OPEN automatable=0
  - review-candidate package with consistent verified_candidate_content_sha
  - Gate 3 tree unchanged vs accepted main
  - No fabricated human validation claims
  - Manifest hashes match live sources
  - Files changed after verified content SHA limited to provenance allowlist
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUALITY_ISSUES = ROOT / "publication/full31/quality/QUALITY_ISSUES.yaml"
CANDIDATE = ROOT / "publication/review-candidates/FULL31-PRE-REVIEW-001"
PROVENANCE = CANDIDATE / "CANDIDATE_PROVENANCE.yaml"
# Accepted main after PR #6 (quality convergence). Gate 3 must remain empty-diff vs this.
ACCEPTED_MAIN = "82284cd8f41d750ff508cd6ea5bad0a9534d8162"

sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REQUIRED_CANDIDATE_FILES = [
    "README.md",
    "SOURCE_COMMIT.txt",
    "CANDIDATE_PROVENANCE.yaml",
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

# Only these paths may change after verified_candidate_content_sha.
# Parallel publication-family tracks are additive and must not rewrite freeze semantics;
# manuscript chapters / labs / glossary remain non-allowlisted.
PROVENANCE_ALLOWLIST_PREFIXES = (
    "publication/review-candidates/FULL31-PRE-REVIEW-001/",
    "publication/review-candidates/FULL31-REVIEW-R1/",
    "publication/review-candidates/FULL31_REVIEW_R1_STATUS.md",
    "publication/review-candidates/HUMAN_VALIDATION_OWNER_GUIDE.md",
    "publication/reviews/",
    "publication/full31/FULL31_PRE_HUMAN_REVIEW_CANDIDATE.md",
    "publication/full31/quality/",
    "publication/full31/FULL31_MANUSCRIPT_INVENTORY.md",
    "publication/full31/FULL31_MANUSCRIPT_INVENTORY.yaml",
    "publication/full31/FULL31_PROGRESS_REPORT.md",
    # Parallel publication-family wave (adult distribution + Kids Edition foundation)
    "publication/family/",
    "publication/distribution/",
    "publication/metadata/",
    "release-packages/",
    "kids/",
    "_quarto-print-",
    "Makefile",
    ".gitignore",
    ".github/workflows/ci.yml",
    "scripts/check_distribution_requirements.py",
    "scripts/check_adult_release_packages.py",
    "scripts/check_publication_family.py",
    "scripts/scan_publication_secrets.py",
    "scripts/cover_geometry.py",
    "scripts/adult_package_common.py",
    "scripts/build_adult_artifact_packages.py",
    "scripts/check_adult_artifact_packages.py",
    "scripts/render_print_profiles.sh",
    "scripts/write_print_profile_results.py",
    "scripts/check_print_profiles.py",
    "scripts/apply_track2a_",
    "scripts/apply_track2b_",
    "scripts/apply_track2c_",
    "scripts/kids_standards_",
    "scripts/build_kids_",
    "scripts/validate_kids_",
    "scripts/generate_kids_",
    "scripts/kids_full_manuscript_",
    "scripts/full31_pre_review_check.py",
    "scripts/build_full31_review_r1_candidate.py",
    "scripts/validate_full31_review_r1_freeze.py",
    "scripts/build_kids_family_review_r1_candidate.py",
    "scripts/validate_kids_family_review_r1_freeze.py",
    "scripts/review_intake.py",
    "scripts/validate_links.py",
    "tests/test_adult_",
    "tests/test_kids_",
    "tests/test_full31_pre_review_provenance.py",
    "tests/test_human_validation_launch_prep.py",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def git_ok(sha: str) -> bool:
    try:
        subprocess.check_output(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"], cwd=ROOT, stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def is_ancestor(anc: str, tip: str) -> bool:
    try:
        subprocess.check_output(
            ["git", "merge-base", "--is-ancestor", anc, tip],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def files_changed_after(content_sha: str, tip: str = "HEAD") -> list[str]:
    out = subprocess.check_output(
        ["git", "diff", "--name-only", f"{content_sha}..{tip}"],
        cwd=ROOT,
        text=True,
    )
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def extract_sha_from_readme(text: str) -> str | None:
    patterns = [
        r"verified_candidate_content_sha:\s*`?([0-9a-f]{40})`?",
        r"Verified candidate content SHA:\s*`?([0-9a-f]{40})`?",
        r"Source commit:\s*`?([0-9a-f]{40})`?",
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.I)
        if m:
            return m.group(1)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-missing-candidate", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []

    print("full31_pre_review_check:")

    open_automatable = 0
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
        open_automatable = sum(1 for i in issues if i.get("fix_status") == "OPEN")
        print(f"  open_blocker: {open_blocker} (summary={summary.get('open_blocker')})")
        print(f"  open_major: {open_major} (summary={summary.get('open_major')})")
        print(f"  open_automatable: {open_automatable}")
        if open_blocker:
            errors.append(f"open BLOCKER count is {open_blocker}, require 0")
        if open_major:
            errors.append(f"open MAJOR count is {open_major}, require 0")
        if open_automatable:
            for i in issues:
                if i.get("fix_status") == "OPEN":
                    errors.append(
                        f"OPEN issue remains: {i.get('issue_id')} "
                        f"({i.get('severity')}) — close or defer explicitly"
                    )

    ok, msg = gate3_unchanged()
    print(f"  gate3_diff: {msg}")
    if not ok:
        errors.append(msg)

    if not args.allow_missing_candidate:
        if not CANDIDATE.is_dir():
            errors.append(f"missing candidate dir {CANDIDATE.relative_to(ROOT)}")
        else:
            for name in REQUIRED_CANDIDATE_FILES:
                if not (CANDIDATE / name).exists():
                    errors.append(f"missing candidate file {name}")

            readme = (
                (CANDIDATE / "README.md").read_text(encoding="utf-8")
                if (CANDIDATE / "README.md").exists()
                else ""
            )
            source_txt = (
                (CANDIDATE / "SOURCE_COMMIT.txt").read_text(encoding="utf-8").strip()
                if (CANDIDATE / "SOURCE_COMMIT.txt").exists()
                else ""
            )
            prov = load_yaml(PROVENANCE) if PROVENANCE.exists() else {}
            content_sha = str(prov.get("verified_candidate_content_sha") or "").strip()
            readme_sha = extract_sha_from_readme(readme) or ""

            print(f"  verified_candidate_content_sha: {content_sha or 'MISSING'}")
            print(f"  SOURCE_COMMIT.txt: {source_txt or 'MISSING'}")
            print(f"  README source SHA: {readme_sha or 'MISSING'}")

            if not content_sha:
                errors.append("CANDIDATE_PROVENANCE.yaml missing verified_candidate_content_sha")
            if source_txt != content_sha:
                errors.append(
                    f"SOURCE_COMMIT.txt ({source_txt}) != verified_candidate_content_sha ({content_sha})"
                )
            if readme_sha and readme_sha != content_sha:
                errors.append(
                    f"README source SHA ({readme_sha}) != verified_candidate_content_sha ({content_sha})"
                )
            if "PRE-HUMAN-REVIEW CANDIDATE" not in readme:
                errors.append("candidate README missing PRE-HUMAN-REVIEW CANDIDATE label")
            if "NO HUMAN VALIDATION HAS OCCURRED" not in readme:
                errors.append("candidate README missing NO HUMAN VALIDATION HAS OCCURRED label")
            if prov.get("human_validation_status") not in {None, "NOT_RUN"}:
                if prov.get("human_validation_status") != "NOT_RUN":
                    errors.append(
                        f"provenance human_validation_status must be NOT_RUN, got {prov.get('human_validation_status')}"
                    )
            if prov.get("gate_3_status") not in {
                None,
                "READER_EVIDENCE_PENDING",
                "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING",
            }:
                # allow either short or long form
                g3 = str(prov.get("gate_3_status") or "")
                if "READER_EVIDENCE_PENDING" not in g3:
                    errors.append(f"provenance gate_3_status unexpected: {g3}")
            if prov.get("publication_status") not in {None, "NOT_PUBLICATION_READY"}:
                errors.append(
                    f"provenance publication_status must be NOT_PUBLICATION_READY, got {prov.get('publication_status')}"
                )

            head = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip()
            if content_sha:
                if not git_ok(content_sha):
                    errors.append(f"verified_candidate_content_sha not in git history: {content_sha}")
                elif not is_ancestor(content_sha, head):
                    errors.append(
                        f"verified_candidate_content_sha {content_sha} is not an ancestor of HEAD {head}"
                    )
                else:
                    changed = files_changed_after(content_sha, head)
                    bad = [
                        p
                        for p in changed
                        if not any(p.startswith(pref) for pref in PROVENANCE_ALLOWLIST_PREFIXES)
                    ]
                    print(f"  files_changed_after_content_sha: {len(changed)}")
                    if bad:
                        errors.append(
                            "substantive paths changed after verified_candidate_content_sha: "
                            + ", ".join(bad[:20])
                        )

            # Hash agreement vs live sources
            def check_hash_field(field: str, path: Path) -> None:
                expected = str(prov.get(field) or "").strip()
                if not expected:
                    errors.append(f"provenance missing {field}")
                    return
                if not path.exists():
                    errors.append(f"cannot hash missing {path}")
                    return
                actual = sha256_file(path)
                if actual != expected:
                    errors.append(f"{field} mismatch: provenance={expected} live={actual}")

            check_hash_field("bibliography_sha256", ROOT / "book/references/references.bib")
            check_hash_field("lab_registry_sha256", ROOT / "labs/lab_registry.yaml")
            check_hash_field("quality_issues_sha256", QUALITY_ISSUES)
            # glossary+terminology combined hash stored by builder
            gloss = ROOT / "glossary/glossary.yaml"
            term = ROOT / "book/terminology.yaml"
            if gloss.exists() and term.exists() and prov.get("glossary_terminology_sha256"):
                combined = hashlib.sha256()
                combined.update(gloss.read_bytes())
                combined.update(b"\n")
                combined.update(term.read_bytes())
                actual = combined.hexdigest()
                if actual != prov.get("glossary_terminology_sha256"):
                    errors.append(
                        "glossary_terminology_sha256 mismatch against live glossary+terminology"
                    )

            # Chapter manifest hash field may be sha of CHAPTER_MANIFEST.yaml itself
            ch_man = CANDIDATE / "CHAPTER_MANIFEST.yaml"
            if prov.get("chapter_manifest_sha256") and ch_man.exists():
                if sha256_file(ch_man) != prov.get("chapter_manifest_sha256"):
                    errors.append("chapter_manifest_sha256 mismatch vs CHAPTER_MANIFEST.yaml")
            fig_man = CANDIDATE / "FIGURE_MANIFEST.yaml"
            if prov.get("figure_manifest_sha256") and fig_man.exists():
                if sha256_file(fig_man) != prov.get("figure_manifest_sha256"):
                    errors.append("figure_manifest_sha256 mismatch vs FIGURE_MANIFEST.yaml")
            art = CANDIDATE / "ARTIFACT_MANIFEST.yaml"
            if prov.get("artifact_manifest_sha256") and art.exists():
                if sha256_file(art) != prov.get("artifact_manifest_sha256"):
                    errors.append("artifact_manifest_sha256 mismatch vs ARTIFACT_MANIFEST.yaml")

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
