#!/usr/bin/env python3
"""Validate Concept Edition preproduction packages against schema_version 1.0.0.

Enforces canonical contracts. Does not tolerate agent-specific schema drift.
Does not modify publication/gates/gate-3/.
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
SCHEMA_VERSION = "1.0.0"

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

REQUIRED_CLAIM_FIELDS = (
    "provisional_id",
    "text",
    "claim_class",
    "evidence_required",
    "preferred_source_type",
    "status",
    "citation_keys",
    "overclaim_risk",
    "wording_boundary",
)
ALLOWED_CLAIM_STATUS = {
    "SOURCE_IDENTIFIED",
    "SOURCE_NEEDED",
    "PROJECT_EVIDENCE_NEEDED",
    "ILLUSTRATIVE_ONLY",
    "PHYSICAL_PENDING",
}
FORBIDDEN_CLAIM_STATUS = {"verified", "planned"}
ALLOWED_CLAIM_CLASS = {
    "general_technical",
    "standards_based",
    "peer_reviewed",
    "project_specific",
    "illustrative",
    "measured_later",
    "publication_internal",
}

REQUIRED_CONCEPT_FIELDS = (
    "concept_id",
    "canonical_term",
    "plain_language_definition",
    "depends_on",
    "introduced_here",
    "reinforced_here",
    "reader_pathways",
    "likely_misconception",
    "glossary_candidate",
    "requires_citation",
    "requires_figure",
    "requires_lab",
)
FORBIDDEN_CONCEPT_FIELDS = {"plain_language", "name", "id"}

REQUIRED_FIGURE_FIELDS = (
    "provisional_id",
    "figure_type",
    "pedagogical_purpose",
    "reader_should_notice",
    "data_or_evidence_source",
    "truth_classification",
    "expected_geometry",
    "accessibility_description_requirement",
    "color_independent_encoding",
    "dependencies",
    "edition_scope",
)
ALLOWED_TRUTH = {"conceptual", "illustrative", "measured", "project_specific", "mixed"}
FORBIDDEN_FIGURE_TRUTH_FIELDS = {"truth_class", "conceptual_vs_measured"}

REQUIRED_OBJECTIVE_FIELDS = ("objective_id", "text", "reader_pathways")
REQUIRED_CAREER_FIELDS = (
    "role_family",
    "chapter_work",
    "technical_skill",
    "student_evidence",
    "portfolio_artifact",
)

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

PASS_MENTION = re.compile(r"(?i)\bGATE_3_PASS\b|\bGate\s*3\s+PASS\b|gate\s*3\s+is\s+pass|closed?\s+gate\s*3")
PASS_NEGATION = re.compile(
    r"(?i)\b(not|never|don't|do not|must not|without|forbidden|prohibited|"
    r"declaring|do\s+not\s+claim|non-?goals?|reader_evidence_pending|gate_3_in_progress)\b"
)


def err(path: str, field: str, value: object, msg: str) -> str:
    return f"{path}: field={field} value={value!r}: {msg}"


def gate3_pass_violations(path: Path, text: str) -> list[str]:
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
    for line in text.splitlines():
        if not re.search(r"\bexact\b", line, re.I):
            continue
        for tok in re.findall(r"\b([A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+)\b", line):
            if tok in KNOWN_WAIKE_COURSES or tok in WAIKE_NOISE:
                continue
            if tok.startswith(("LAB-", "FIG-", "CLM-", "SRC-", "CE-")):
                continue
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


def lab_ok(text: str) -> list[str]:
    errs: list[str] = []
    if not re.search(r"(evidence|portfolio|artifact)", text, re.I):
        errs.append("LAB_PLAN.md missing evidence/portfolio/artifact language")
    if not re.search(r"(fallback|fixture|offline)", text, re.I):
        errs.append("LAB_PLAN.md missing fallback/fixture/offline route")
    if not re.search(r"LAB-[A-Z0-9-]+", text):
        errs.append("LAB_PLAN.md missing provisional LAB-* id")
    return errs


def validate_claims(ce: str, data: dict) -> list[str]:
    errs: list[str] = []
    path = f"{ce}/CLAIM_PLAN.yaml"
    if data.get("schema_version") != SCHEMA_VERSION:
        errs.append(err(path, "schema_version", data.get("schema_version"), f"must be {SCHEMA_VERSION}"))
    if "nodes" in data:
        errs.append(err(path, "nodes", True, "forbidden; use claims only"))
    claims = data.get("claims")
    if not isinstance(claims, list) or not claims:
        errs.append(err(path, "claims", claims, "must be a non-empty list"))
        return errs
    for claim in claims:
        if not isinstance(claim, dict):
            errs.append(err(path, "claims[]", claim, "must be a mapping"))
            continue
        cid = claim.get("provisional_id", "<missing>")
        for field in REQUIRED_CLAIM_FIELDS:
            if field not in claim:
                errs.append(err(path, f"claims[{cid}].{field}", None, "missing required field"))
        status = claim.get("status")
        if status in FORBIDDEN_CLAIM_STATUS:
            errs.append(err(path, f"claims[{cid}].status", status, "forbidden legacy status"))
        elif status not in ALLOWED_CLAIM_STATUS:
            errs.append(err(path, f"claims[{cid}].status", status, "unknown claim status"))
        cclass = claim.get("claim_class")
        if cclass not in ALLOWED_CLAIM_CLASS:
            errs.append(err(path, f"claims[{cid}].claim_class", cclass, "unknown claim_class"))
        if not isinstance(claim.get("citation_keys"), list):
            errs.append(err(path, f"claims[{cid}].citation_keys", claim.get("citation_keys"), "must be a list"))
    return errs


def validate_concepts(ce: str, data: dict) -> list[str]:
    errs: list[str] = []
    path = f"{ce}/CONCEPT_GRAPH.yaml"
    if data.get("schema_version") != SCHEMA_VERSION:
        errs.append(err(path, "schema_version", data.get("schema_version"), f"must be {SCHEMA_VERSION}"))
    if "nodes" in data:
        errs.append(err(path, "nodes", True, "forbidden collection name; use concepts:"))
    concepts = data.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        errs.append(err(path, "concepts", concepts, "must be a non-empty list"))
        return errs
    for node in concepts:
        if not isinstance(node, dict):
            errs.append(err(path, "concepts[]", node, "must be a mapping"))
            continue
        cid = node.get("concept_id", "<missing>")
        for field in REQUIRED_CONCEPT_FIELDS:
            if field not in node:
                errs.append(err(path, f"concepts[{cid}].{field}", None, "missing required field"))
        for bad in FORBIDDEN_CONCEPT_FIELDS:
            if bad in node:
                errs.append(err(path, f"concepts[{cid}].{bad}", node.get(bad), "forbidden legacy field"))
        for flag in ("introduced_here", "reinforced_here", "glossary_candidate", "requires_citation", "requires_figure", "requires_lab"):
            if flag in node and not isinstance(node[flag], bool):
                errs.append(err(path, f"concepts[{cid}].{flag}", node[flag], "must be boolean"))
        if not isinstance(node.get("depends_on"), list):
            errs.append(err(path, f"concepts[{cid}].depends_on", node.get("depends_on"), "must be a list"))
        if not isinstance(node.get("reader_pathways"), list):
            errs.append(err(path, f"concepts[{cid}].reader_pathways", node.get("reader_pathways"), "must be a list"))
    return errs


def validate_figures(ce: str, data: dict) -> list[str]:
    errs: list[str] = []
    path = f"{ce}/FIGURE_PLAN.yaml"
    if data.get("schema_version") != SCHEMA_VERSION:
        errs.append(err(path, "schema_version", data.get("schema_version"), f"must be {SCHEMA_VERSION}"))
    if "figure_plans" in data:
        errs.append(err(path, "figure_plans", True, "forbidden; use figures:"))
    figures = data.get("figures")
    if not isinstance(figures, list) or not figures:
        errs.append(err(path, "figures", figures, "must be a non-empty list"))
        return errs
    for fig in figures:
        if not isinstance(fig, dict):
            errs.append(err(path, "figures[]", fig, "must be a mapping"))
            continue
        fid = fig.get("provisional_id", "<missing>")
        for field in REQUIRED_FIGURE_FIELDS:
            if field not in fig:
                errs.append(err(path, f"figures[{fid}].{field}", None, "missing required field"))
        for bad in FORBIDDEN_FIGURE_TRUTH_FIELDS:
            if bad in fig:
                errs.append(err(path, f"figures[{fid}].{bad}", fig.get(bad), "forbidden legacy truth field"))
        truth = fig.get("truth_classification")
        if truth not in ALLOWED_TRUTH:
            errs.append(err(path, f"figures[{fid}].truth_classification", truth, "unknown truth_classification"))
        if not isinstance(fig.get("dependencies"), list):
            errs.append(err(path, f"figures[{fid}].dependencies", fig.get("dependencies"), "must be a list"))
    return errs


def validate_objectives(ce: str, data: dict) -> list[str]:
    errs: list[str] = []
    path = f"{ce}/LEARNING_OBJECTIVES.yaml"
    if data.get("schema_version") != SCHEMA_VERSION:
        errs.append(err(path, "schema_version", data.get("schema_version"), f"must be {SCHEMA_VERSION}"))
    if isinstance(data.get("pathways"), dict) and "objectives" not in data:
        errs.append(err(path, "pathways", True, "pathway dict alone forbidden; use objectives: list"))
    objs = data.get("objectives")
    if not isinstance(objs, list) or not objs:
        errs.append(err(path, "objectives", objs, "must be a non-empty list"))
        return errs
    for obj in objs:
        oid = obj.get("objective_id", "<missing>") if isinstance(obj, dict) else "<missing>"
        if not isinstance(obj, dict):
            errs.append(err(path, "objectives[]", obj, "must be a mapping"))
            continue
        for field in REQUIRED_OBJECTIVE_FIELDS:
            if field not in obj:
                errs.append(err(path, f"objectives[{oid}].{field}", None, "missing required field"))
        if not isinstance(obj.get("reader_pathways"), list):
            errs.append(err(path, f"objectives[{oid}].reader_pathways", obj.get("reader_pathways"), "must be a list"))
    return errs


def validate_careers(ce: str, data: dict) -> list[str]:
    errs: list[str] = []
    path = f"{ce}/CAREER_MAP.yaml"
    if data.get("schema_version") != SCHEMA_VERSION:
        errs.append(err(path, "schema_version", data.get("schema_version"), f"must be {SCHEMA_VERSION}"))
    if "roles" in data and "careers" not in data:
        errs.append(err(path, "roles", True, "forbidden primary collection; use careers:"))
    if "employment_guarantee" not in data:
        errs.append(err(path, "employment_guarantee", None, "missing required field"))
    careers = data.get("careers")
    if not isinstance(careers, list) or not careers:
        errs.append(err(path, "careers", careers, "must be a non-empty list"))
        return errs
    for row in careers:
        if not isinstance(row, dict):
            errs.append(err(path, "careers[]", row, "must be a mapping"))
            continue
        rf = row.get("role_family", "<missing>")
        for field in REQUIRED_CAREER_FIELDS:
            if field not in row:
                errs.append(err(path, f"careers[{rf}].{field}", None, "missing required field"))
    return errs


def validate_package(ce: str) -> list[str]:
    errs: list[str] = []
    d = PREPROD / ce
    if not d.is_dir():
        return [f"missing package directory publication/preproduction/{ce}/"]
    for name in REQUIRED_ARTIFACTS:
        if not (d / name).exists():
            errs.append(f"{ce}: missing required artifact {name}")

    claims_path = d / "CLAIM_PLAN.yaml"
    if claims_path.exists():
        errs.extend(validate_claims(ce, load_yaml(claims_path) or {}))
    concept_path = d / "CONCEPT_GRAPH.yaml"
    if concept_path.exists():
        errs.extend(validate_concepts(ce, load_yaml(concept_path) or {}))
    fig_path = d / "FIGURE_PLAN.yaml"
    if fig_path.exists():
        errs.extend(validate_figures(ce, load_yaml(fig_path) or {}))
    lo_path = d / "LEARNING_OBJECTIVES.yaml"
    if lo_path.exists():
        errs.extend(validate_objectives(ce, load_yaml(lo_path) or {}))
    career_path = d / "CAREER_MAP.yaml"
    if career_path.exists():
        errs.extend(validate_careers(ce, load_yaml(career_path) or {}))

    lab_path = d / "LAB_PLAN.md"
    if lab_path.exists():
        errs.extend(f"{ce}: {e}" for e in lab_ok(lab_path.read_text(encoding="utf-8")))
    wx = d / "WAIKE_CROSSWALK.md"
    if wx.exists():
        errs.extend(waike_errors(wx, wx.read_text(encoding="utf-8")))

    for path in d.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".bib", ".txt"}:
            continue
        errs.extend(gate3_pass_violations(path, path.read_text(encoding="utf-8", errors="ignore")))
    return errs


def validate_candidate_indexes() -> list[str]:
    errs: list[str] = []
    for name in (
        "CANDIDATE_CLAIM_INDEX.yaml",
        "CANDIDATE_FIGURE_INDEX.yaml",
        "CANDIDATE_GLOSSARY.yaml",
        "CANDIDATE_LAB_INDEX.yaml",
        "CANDIDATE_SOURCE_INDEX.yaml",
        "CANDIDATE_WAIKE_CROSSWALK.yaml",
    ):
        path = PREPROD / name
        if not path.exists():
            errs.append(f"missing {name}")
            continue
        data = load_yaml(path) or {}
        if data.get("schema_version") != SCHEMA_VERSION:
            errs.append(err(name, "schema_version", data.get("schema_version"), f"must be {SCHEMA_VERSION}"))
        if data.get("gate_note") != "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING":
            errs.append(err(name, "gate_note", data.get("gate_note"), "must remain READER_EVIDENCE_PENDING"))
    return errs


def main() -> int:
    errors: list[str] = []
    if not PREPROD.exists():
        print("validate_ce_preproduction: FAIL")
        print(" - missing publication/preproduction/")
        return 1
    for ce in CE_DIRS:
        errors.extend(validate_package(ce))
    errors.extend(validate_candidate_indexes())
    errors.extend(synthetic_in_gate3_responses())
    if errors:
        print("validate_ce_preproduction: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_ce_preproduction: PASS")
    print(f" - schema_version={SCHEMA_VERSION}; packages={', '.join(CE_DIRS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
