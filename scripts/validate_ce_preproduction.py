#!/usr/bin/env python3
"""Validate Concept Edition chapter-local preproduction packages.

Protects publication invariants only:
- required artifact set per CE package
- claims carry an evidence status
- figures carry a truth classification (schema variants allowed)
- labs describe evidence artifacts + fallback route
- WAIKE relationship vocabulary is constrained
- no CE preproduction file affirms Gate 3 PASS
- Gate 3 responses stay free of synthetic fixtures (delegates path check)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

PREPROD = ROOT / "publication" / "preproduction"
CE_DIRS = ("ce-01", "ce-03", "ce-04", "ce-05", "ce-06")

REQUIRED_ARTIFACTS = (
    "CHAPTER_BRIEF.md",
    "LEARNING_OBJECTIVES.yaml",
    "EXPERIENCE_MAP.md",
    "CONCEPT_GRAPH.yaml",
    "CLAIM_PLAN.yaml",
    "SOURCE_REGISTER.md",
    "references.local.bib",
    "FIGURE_PLAN.yaml",
    "LAB_PLAN.md",
    "STABILITY_CONTRACT.md",
    "SECURITY_EQUITY_ACCESSIBILITY.md",
    "CAREER_MAP.yaml",
    "WAIKE_CROSSWALK.md",
)

ALLOWED_CLAIM_STATUS = {
    "SOURCE_IDENTIFIED",
    "SOURCE_NEEDED",
    "PROJECT_EVIDENCE_NEEDED",
    "ILLUSTRATIVE_ONLY",
    "PHYSICAL_PENDING",
    # CE-5 used shared-registry style statuses; still countable evidence statuses.
    "verified",
    "planned",
}

ALLOWED_TRUTH = {
    "conceptual",
    "illustrative",
    "measured",
    "project-specific",
    "project_specific",
    "project_specific_conceptual",
    "conceptual_project_qualified",
    "measured_later_fixture",
    "mixed",
}

ALLOWED_WAIKE_REL = {"exact", "adjacent", "proposed", "no-map"}

KNOWN_WAIKE_COURSES = {
    "SOFTWARE_BUILDER",
    "GAME_DEV_INTERACTIVE",
    "COMPUTER_NETWORKING",
    "EMBEDDED_PROTOTYPING",
    "AI_ML_EDGE",
    "CLOUD_DEVOPS",
    "COMM_PD_ETHICS",
    "CYBERSECURITY",
    "DATA_DASHBOARDS",
    "DATA_VIZ_BI",
    "GENERAL_IT",
    "GUNNCHOS_PRODUCT_LAB",
    "HARDWARE_ENGINEERING",
    "PM_AGILE_LSS",
    "ROBOTICS_CONTROL",
    "WIRELESS_6G",
}

# Tokens that look like course IDs but are documentation noise, not invented courses.
WAIKE_NOISE = {
    "SCREAMING_SNAKE",
    "READER_EVIDENCE_PENDING",
    "ACCESSIBILITY_AND_LOW_COST",
    "CLAIMS_TO_EVIDENCE",
    "STABILITY_CONTRACT",
    "PHYSICAL_PENDING",
    "SOURCE_IDENTIFIED",
    "SOURCE_NEEDED",
    "PROJECT_EVIDENCE_NEEDED",
    "ILLUSTRATIVE_ONLY",
    "GATE_3_IN_PROGRESS",
}


def claim_list(data: dict) -> list:
    return data.get("claims") or []


def figure_list(data: dict) -> list:
    return data.get("figures") or data.get("figure_plans") or []


def figure_truth(fig: dict) -> str | None:
    for key in ("truth_classification", "truth_class", "conceptual_vs_measured"):
        val = fig.get(key)
        if val:
            return str(val).strip().lower().replace(" ", "_")
    return None


def figure_id(fig: dict) -> str:
    return str(fig.get("provisional_id") or fig.get("figure_id") or fig.get("id") or "<unknown>")


def claim_id(claim: dict) -> str:
    return str(
        claim.get("provisional_id")
        or claim.get("claim_id")
        or claim.get("id")
        or "<unknown>"
    )


def claim_status(claim: dict) -> str | None:
    status = claim.get("status")
    if status:
        return str(status).strip()
    evidence = claim.get("evidence")
    if isinstance(evidence, dict) and evidence.get("status"):
        return str(evidence["status"]).strip()
    return None


def lab_ok(text: str) -> list[str]:
    errs: list[str] = []
    if not re.search(r"(evidence|portfolio|artifact)", text, re.I):
        errs.append("LAB_PLAN.md missing evidence/portfolio/artifact language")
    if not re.search(r"(fallback|fixture|offline)", text, re.I):
        errs.append("LAB_PLAN.md missing fallback/fixture/offline route")
    if not re.search(r"LAB-[A-Z0-9-]+", text):
        errs.append("LAB_PLAN.md missing provisional LAB-* id")
    return errs


PASS_MENTION = re.compile(r"(?i)\bGATE_3_PASS\b|\bGate\s*3\s+PASS\b|gate\s*3\s+is\s+pass|closed?\s+gate\s*3")
PASS_NEGATION = re.compile(
    r"(?i)\b(not|never|don't|do not|must not|without|forbidden|prohibited|"
    r"declaring|do\s+not\s+claim|non-?goals?|reader_evidence_pending|gate_3_in_progress)\b"
)


def gate3_pass_violations(path: Path, text: str) -> list[str]:
    """Flag only affirmative PASS/close claims; allow non-goal / negation wording."""
    errs: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        if not PASS_MENTION.search(line):
            continue
        if PASS_NEGATION.search(line):
            continue
        errs.append(
            f"{path.relative_to(ROOT)}:{i}: affirmative Gate 3 PASS language: {line.strip()[:120]}"
        )
    return errs


def waike_errors(path: Path, text: str) -> list[str]:
    errs: list[str] = []
    rels = {m.lower() for m in re.findall(r"\b(exact|adjacent|proposed|no-map)\b", text, re.I)}
    if not rels:
        errs.append(f"{path.relative_to(ROOT)}: WAIKE_CROSSWALK.md missing exact/adjacent/proposed/no-map vocabulary")
    bad = rels - ALLOWED_WAIKE_REL
    if bad:
        errs.append(f"{path.relative_to(ROOT)}: unknown WAIKE relationship tokens {sorted(bad)}")

    # Invented course-ID heuristic: SCREAMING_SNAKE tokens with underscore asserted as exact.
    for line in text.splitlines():
        if not re.search(r"\bexact\b", line, re.I):
            continue
        for tok in re.findall(r"\b([A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+)\b", line):
            if tok in KNOWN_WAIKE_COURSES or tok in WAIKE_NOISE:
                continue
            if tok.startswith(("LAB-", "FIG-", "CLM-", "SRC-", "CE-")):
                continue
            # Allow path-like DOC names; flag only when line claims a course/module ID.
            if re.search(r"(?i)(course|module|lab_id|digital_rc)", line):
                errs.append(
                    f"{path.relative_to(ROOT)}: possible invented WAIKE course/module ID under exact mapping: {tok}"
                )
    return errs


def synthetic_in_gate3_responses() -> list[str]:
    errs: list[str] = []
    responses = ROOT / "publication" / "gates" / "gate-3" / "responses"
    if not responses.exists():
        return errs
    markers = ("SYNTHETIC", "synthetic_fixture", "DO_NOT_USE_AS_EVIDENCE", "SYNTHETIC_TEST_FIXTURE")
    for path in responses.rglob("*"):
        if not path.is_file() or path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in markers:
            if marker in text:
                errs.append(f"{path.relative_to(ROOT)}: synthetic fixture marker '{marker}' in Gate 3 responses")
    return errs


def validate_package(ce: str) -> list[str]:
    errs: list[str] = []
    d = PREPROD / ce
    if not d.is_dir():
        return [f"missing package directory publication/preproduction/{ce}/"]

    for name in REQUIRED_ARTIFACTS:
        if not (d / name).exists():
            errs.append(f"{ce}: missing required artifact {name}")

    # Claims
    claims_path = d / "CLAIM_PLAN.yaml"
    if claims_path.exists():
        claims = claim_list(load_yaml(claims_path))
        if not claims:
            errs.append(f"{ce}: CLAIM_PLAN.yaml has no claims")
        for claim in claims:
            status = claim_status(claim)
            cid = claim_id(claim)
            if not status:
                errs.append(f"{ce}: claim {cid} missing evidence status")
            elif status not in ALLOWED_CLAIM_STATUS:
                errs.append(f"{ce}: claim {cid} unknown status {status!r}")

    # Figures
    fig_path = d / "FIGURE_PLAN.yaml"
    if fig_path.exists():
        figures = figure_list(load_yaml(fig_path))
        if not figures:
            errs.append(f"{ce}: FIGURE_PLAN.yaml has no figures")
        for fig in figures:
            truth = figure_truth(fig)
            fid = figure_id(fig)
            if not truth:
                errs.append(f"{ce}: figure {fid} missing truth classification")
            elif truth not in ALLOWED_TRUTH and not truth.startswith("conceptual"):
                # Allow annotated variants like conceptual_project_qualified already listed.
                errs.append(f"{ce}: figure {fid} unknown truth classification {truth!r}")

    # Labs
    lab_path = d / "LAB_PLAN.md"
    if lab_path.exists():
        errs.extend(f"{ce}: {e}" for e in lab_ok(lab_path.read_text(encoding="utf-8")))

    # WAIKE
    wx = d / "WAIKE_CROSSWALK.md"
    if wx.exists():
        errs.extend(waike_errors(wx, wx.read_text(encoding="utf-8")))

    # Gate 3 PASS scan across package
    for path in d.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".bib", ".txt"}:
            continue
        errs.extend(gate3_pass_violations(path, path.read_text(encoding="utf-8", errors="ignore")))

    return errs


def main() -> int:
    errors: list[str] = []
    if not PREPROD.exists():
        print("validate_ce_preproduction: FAIL")
        print(" - missing publication/preproduction/")
        return 1

    for ce in CE_DIRS:
        errors.extend(validate_package(ce))
    errors.extend(synthetic_in_gate3_responses())

    if errors:
        print("validate_ce_preproduction: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_ce_preproduction: PASS")
    print(f" - packages checked: {', '.join(CE_DIRS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
