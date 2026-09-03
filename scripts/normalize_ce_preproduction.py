#!/usr/bin/env python3
"""Normalize CE preproduction YAML packages to schema_version 1.0.0.

Rewrites CLAIM_PLAN / CONCEPT_GRAPH / FIGURE_PLAN / LEARNING_OBJECTIVES / CAREER_MAP
under publication/preproduction/ce-0N/ into the canonical field vocabulary.
Does not touch publication/gates/gate-3/.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

PREPROD = ROOT / "publication" / "preproduction"
CE_DIRS = ("ce-01", "ce-03", "ce-04", "ce-05", "ce-06")
SCHEMA_VERSION = "1.0.0"

CLAIM_CLASS_ALIASES = {
    "general technical": "general_technical",
    "general-knowledge": "general_technical",
    "general_technical": "general_technical",
    "standards-based": "standards_based",
    "standards_based": "standards_based",
    "standards": "standards_based",
    "standard": "standards_based",
    "project-specific": "project_specific",
    "project_specific": "project_specific",
    "measured later": "measured_later",
    "measured_later": "measured_later",
    "publication-internal": "publication_internal",
    "publication_internal": "publication_internal",
    "illustrative": "illustrative",
    "peer-reviewed": "peer_reviewed",
    "peer_reviewed": "peer_reviewed",
    "textbook": "general_technical",
    "repository-implemented": "project_specific",
    "repository-documented": "project_specific",
    "planned": "publication_internal",
}

TRUTH_COMPOUND = {
    "conceptual_project_qualified": ("conceptual", "project_qualified"),
    "project_specific_conceptual": ("project_specific", "conceptual"),
    "measured_later_fixture": ("measured", "later_fixture"),
    "project-specific": ("project_specific", None),
}

ALLOWED_TRUTH = {"conceptual", "illustrative", "measured", "project_specific", "mixed"}
ALLOWED_STATUS = {
    "SOURCE_IDENTIFIED",
    "SOURCE_NEEDED",
    "PROJECT_EVIDENCE_NEEDED",
    "ILLUSTRATIVE_ONLY",
    "PHYSICAL_PENDING",
}
PATHWAYS = {"explorer", "operator", "builder", "engineer", "researcher", "educator"}


def write_yaml(path: Path, data: Any) -> None:
    text = dump_yaml(data)
    if not text.endswith("\n"):
        text += "\n"
    # Ensure schema_version present at top for structured files we own.
    path.write_text(text, encoding="utf-8")


def as_list(val: Any) -> list:
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def norm_claim_class(raw: Any) -> str:
    if raw is None:
        return "general_technical"
    key = str(raw).strip()
    return CLAIM_CLASS_ALIASES.get(key, CLAIM_CLASS_ALIASES.get(key.lower(), key.replace("-", "_").replace(" ", "_")))


def map_ce5_status(claim: dict) -> str:
    """Map CE-5 verified/planned into Wave-13 evidence statuses by meaning."""
    old = str(claim.get("status") or "").strip().lower()
    cid = str(claim.get("claim_id") or claim.get("provisional_id") or "")
    scope = str(claim.get("scope") or "").lower()
    classification = str(claim.get("classification") or "").lower()
    text = str(claim.get("text") or "").lower()

    if "physical fabrication pending" in text or "physical units pending" in text or cid.endswith("003"):
        if "quartet" in text or "fabrication" in text:
            return "PHYSICAL_PENDING"
    if classification in {"illustrative"} or "illustrative" in text and old == "planned":
        if cid.endswith("008") or "teaching aids" in text:
            return "ILLUSTRATIVE_ONLY"
    if cid.endswith("009") or ("lab-trust-001" in text and "proposed" in text):
        return "PROJECT_EVIDENCE_NEEDED"
    if old == "verified":
        return "SOURCE_IDENTIFIED"
    if old == "planned":
        # Textbook/standards with bib keys already identified → SOURCE_IDENTIFIED
        evidence = claim.get("evidence") if isinstance(claim.get("evidence"), dict) else {}
        if evidence.get("bib_keys"):
            return "SOURCE_IDENTIFIED"
        if scope in {"publication-internal"} or classification in {"planned", "illustrative"}:
            if "illustrative" in classification:
                return "ILLUSTRATIVE_ONLY"
            return "PROJECT_EVIDENCE_NEEDED"
        return "SOURCE_NEEDED"
    if old.upper() in ALLOWED_STATUS:
        return old.upper()
    raise ValueError(f"Cannot map claim status for {cid}: {old!r}")


def normalize_claim(claim: dict, chapter: str) -> dict:
    c = copy.deepcopy(claim)
    provisional = c.get("provisional_id") or c.get("claim_id") or c.get("id")
    text = c.get("text") or c.get("claim_text") or ""
    claim_class = norm_claim_class(c.get("claim_class") or c.get("scope") or c.get("classification"))

    # CE-5 nested evidence → citation_keys + status mapping
    citation_keys = as_list(c.get("citation_keys"))
    if not citation_keys and isinstance(c.get("sources"), list):
        citation_keys = [str(x) for x in c["sources"]]
    evidence = c.get("evidence") if isinstance(c.get("evidence"), dict) else {}
    if not citation_keys and evidence.get("bib_keys"):
        citation_keys = [str(x) for x in evidence["bib_keys"]]
    if not citation_keys and evidence.get("source_id"):
        citation_keys = [str(evidence["source_id"])]

    status = c.get("status")
    if status in ("verified", "planned") or (
        isinstance(status, str) and status.lower() in ("verified", "planned")
    ):
        status = map_ce5_status(c)
    elif isinstance(c.get("evidence"), dict) and c["evidence"].get("status") and not status:
        status = str(c["evidence"]["status"])
    status = str(status).strip()
    if status not in ALLOWED_STATUS:
        # try alias uppercase
        if status.upper() in ALLOWED_STATUS:
            status = status.upper()
        else:
            raise ValueError(f"{chapter}: claim {provisional} has non-canonical status {status!r}")

    wording = c.get("wording_boundary")
    if wording is None and isinstance(c.get("wording"), dict):
        approved = c["wording"].get("approved")
        prohibited = c["wording"].get("prohibited")
        parts = []
        if approved:
            parts.append(f"approved: {approved}")
        if prohibited:
            parts.append("prohibited: " + "; ".join(str(x) for x in as_list(prohibited)))
        wording = " | ".join(parts) if parts else ""
    if wording is None:
        wording = ""

    evidence_required = c.get("evidence_required")
    if evidence_required is None:
        evidence_required = (
            "Repository paths + SHA" if status == "SOURCE_IDENTIFIED" and evidence.get("commit") else
            "Primary source citation" if status == "SOURCE_IDENTIFIED" else
            "Additional primary verification" if status == "SOURCE_NEEDED" else
            "Project/lab evidence bundle" if status == "PROJECT_EVIDENCE_NEEDED" else
            "Illustrative teaching construct only" if status == "ILLUSTRATIVE_ONLY" else
            "Physical fabrication / measured validation"
        )

    preferred = c.get("preferred_source_type")
    if preferred is None:
        preferred = {
            "standards_based": "standards/specifications",
            "peer_reviewed": "peer-reviewed literature",
            "project_specific": "accepted-main repository evidence",
            "illustrative": "publication-internal teaching aid",
            "publication_internal": "publication-internal",
            "measured_later": "future measurement bundle",
            "general_technical": "textbook or official documentation",
        }.get(claim_class, "official technical documentation")

    out = {
        "provisional_id": str(provisional),
        "text": str(text).strip(),
        "claim_class": claim_class if claim_class in {
            "general_technical", "standards_based", "peer_reviewed", "project_specific",
            "illustrative", "measured_later", "publication_internal",
        } else norm_claim_class(claim_class),
        "evidence_required": str(evidence_required),
        "preferred_source_type": str(preferred),
        "status": status,
        "citation_keys": [str(x) for x in citation_keys],
        "overclaim_risk": str(c.get("overclaim_risk") or (c.get("wording") or {}).get("prohibited") or "See wording_boundary"),
        "wording_boundary": str(wording),
    }
    if claim_class == "project_specific" and evidence.get("commit"):
        out["project_evidence"] = {
            "repository": evidence.get("repository"),
            "commit": evidence.get("commit"),
            "paths": evidence.get("paths") or [],
            "source_id": evidence.get("source_id"),
        }
    # Ensure claim_class canonical
    out["claim_class"] = norm_claim_class(out["claim_class"])
    if out["claim_class"] not in {
        "general_technical", "standards_based", "peer_reviewed", "project_specific",
        "illustrative", "measured_later", "publication_internal",
    }:
        # last-resort map
        out["claim_class"] = "general_technical"
    return out


def normalize_claim_plan(path: Path, chapter: str) -> None:
    data = load_yaml(path) or {}
    claims = data.get("claims") or []
    out_claims = [normalize_claim(c, chapter) for c in claims]
    out = {
        "schema_version": SCHEMA_VERSION,
        "chapter_id": data.get("chapter_id") or data.get("chapter") or chapter.upper().replace("CE-0", "CE-").replace("CE-", "CE-"),
        "claims": out_claims,
    }
    # preserve useful meta
    for key in ("maps_to", "gate_note", "anchor_experience"):
        if key in data:
            out[key] = data[key]
    if "chapter_id" not in out or not out["chapter_id"]:
        out["chapter_id"] = chapter.replace("ce-0", "CE-").replace("ce-", "CE-").upper()
        # ce-01 -> CE-01 style
        out["chapter_id"] = {
            "ce-01": "CE-1",
            "ce-03": "CE-3",
            "ce-04": "CE-4",
            "ce-05": "CE-5",
            "ce-06": "CE-6",
        }.get(chapter, out["chapter_id"])
    write_yaml(path, out)


def normalize_concept(node: dict, chapter: str) -> dict:
    concept_id = node.get("concept_id") or node.get("id")
    term = node.get("canonical_term") or node.get("name")
    plain = node.get("plain_language_definition") or node.get("plain_language") or ""
    depends = as_list(node.get("depends_on") if "depends_on" in node else node.get("prerequisites"))
    depends = [str(x) for x in depends]

    chapter_label = {
        "ce-01": "CE-1",
        "ce-03": "CE-3",
        "ce-04": "CE-4",
        "ce-05": "CE-5",
        "ce-06": "CE-6",
    }[chapter]
    introduced = node.get("introduced_here")
    if introduced is None:
        intro_in = node.get("introduced_in")
        if intro_in is None:
            introduced = True
        else:
            introduced = str(intro_in) in {chapter_label, chapter, chapter.upper()}
    reinforced = node.get("reinforced_here")
    if reinforced is None:
        reinforced = False

    pathways = as_list(node.get("reader_pathways") or node.get("pathways") or list(PATHWAYS))
    pathways = [str(p).lower() for p in pathways if str(p).lower() in PATHWAYS]
    if not pathways:
        pathways = sorted(PATHWAYS)

    return {
        "concept_id": str(concept_id),
        "canonical_term": str(term),
        "plain_language_definition": str(plain),
        "depends_on": depends,
        "introduced_here": bool(introduced),
        "reinforced_here": bool(reinforced),
        "reader_pathways": pathways,
        "likely_misconception": str(node.get("likely_misconception") or node.get("wording_guard") or node.get("human_observable") or ""),
        "glossary_candidate": bool(node.get("glossary_candidate", True)),
        "requires_citation": bool(node.get("requires_citation", False)),
        "requires_figure": bool(node.get("requires_figure", False)),
        "requires_lab": bool(node.get("requires_lab", False)),
    }


def normalize_concept_graph(path: Path, chapter: str) -> None:
    data = load_yaml(path) or {}
    nodes = data.get("concepts") if "concepts" in data else data.get("nodes")
    if nodes is None:
        nodes = []
    concepts = [normalize_concept(n, chapter) for n in nodes]
    out = {
        "schema_version": SCHEMA_VERSION,
        "chapter_id": {
            "ce-01": "CE-1",
            "ce-03": "CE-3",
            "ce-04": "CE-4",
            "ce-05": "CE-5",
            "ce-06": "CE-6",
        }[chapter],
        "concepts": concepts,
    }
    for key in ("maps_to", "anchor_experience", "teaching_model", "edges"):
        if key in data:
            out[key] = data[key]
    write_yaml(path, out)


def map_truth(raw: Any) -> tuple[str, str | None]:
    if raw is None:
        return "conceptual", None
    s = str(raw).strip().lower().replace(" ", "_")
    if s in TRUTH_COMPOUND:
        return TRUTH_COMPOUND[s]
    if s in ALLOWED_TRUTH:
        return s, None
    if s.startswith("conceptual"):
        return "conceptual", s[len("conceptual_"):] or None
    if "illustrative" in s:
        return "illustrative", None
    if "measured" in s:
        return "measured", None
    if "project" in s:
        return "project_specific", None
    if "mixed" in s:
        return "mixed", None
    raise ValueError(f"Unknown truth classification {raw!r}")


def normalize_figure(fig: dict) -> dict:
    fid = fig.get("provisional_id") or fig.get("figure_id") or fig.get("id")
    ftype = fig.get("figure_type") or fig.get("type") or "diagram"
    purpose = fig.get("pedagogical_purpose") or fig.get("purpose") or ""
    notice = fig.get("reader_should_notice") or fig.get("what_reader_should_notice") or fig.get("title") or ""
    data_src = fig.get("data_or_evidence_source") or fig.get("data_evidence_source") or "educational original"
    raw_truth = None
    for k in ("truth_classification", "truth_class", "conceptual_vs_measured"):
        if fig.get(k) is not None:
            raw_truth = fig.get(k)
            break
    truth, qual = map_truth(raw_truth)
    geom = fig.get("expected_geometry") or fig.get("geometry_layout") or "TBD layout"
    a11y = fig.get("accessibility_description_requirement") or fig.get("accessibility") or fig.get("alt_text_draft") or fig.get("text_equivalent")
    if isinstance(a11y, dict):
        a11y = "; ".join(f"{k}: {v}" for k, v in a11y.items())
    if not a11y:
        a11y = "Long description required; color not sole cue."
    color = fig.get("color_independent_encoding") or fig.get("color_encoding") or "Shape + label; color never sole cue."
    deps = as_list(fig.get("dependencies") or fig.get("claims_touched") or [])
    edition = fig.get("edition_scope")
    if edition is None:
        if fig.get("full_edition_only"):
            edition = "full_edition"
        elif fig.get("concept_edition") is False:
            edition = "full_edition"
        else:
            edition = "concept_edition"
    out = {
        "provisional_id": str(fid),
        "figure_type": str(ftype),
        "pedagogical_purpose": str(purpose),
        "reader_should_notice": str(notice),
        "data_or_evidence_source": str(data_src),
        "truth_classification": truth,
        "expected_geometry": str(geom),
        "accessibility_description_requirement": str(a11y),
        "color_independent_encoding": str(color),
        "dependencies": [str(x) for x in deps],
        "edition_scope": str(edition),
    }
    if qual:
        out["qualification"] = qual
    if fig.get("production_status"):
        out["production_status"] = fig["production_status"]
    if fig.get("title_intent"):
        out["title_intent"] = fig["title_intent"]
    return out


def normalize_figure_plan(path: Path, chapter: str) -> None:
    data = load_yaml(path) or {}
    figs = data.get("figures") or data.get("figure_plans") or []
    out = {
        "schema_version": SCHEMA_VERSION,
        "chapter_id": {
            "ce-01": "CE-1",
            "ce-03": "CE-3",
            "ce-04": "CE-4",
            "ce-05": "CE-5",
            "ce-06": "CE-6",
        }[chapter],
        "figures": [normalize_figure(f) for f in figs],
    }
    for key in ("maps_to", "gate_note", "non_goals", "rights_policy", "accessibility_policy"):
        if key in data:
            out[key] = data[key]
    write_yaml(path, out)


def normalize_learning_objectives(path: Path, chapter: str) -> None:
    data = load_yaml(path) or {}
    objectives: list[dict] = []

    raw_objectives = data.get("objectives")
    # Shape A: objectives as pathway-keyed dict
    if isinstance(raw_objectives, dict):
        for pathway, items in raw_objectives.items():
            pw = str(pathway).lower()
            if not isinstance(items, list):
                continue
            for obj in items:
                oid = obj.get("objective_id") or obj.get("id")
                text = obj.get("text") or obj.get("statement") or obj.get("objective") or ""
                item = {
                    "objective_id": str(oid),
                    "text": str(text),
                    "reader_pathways": [pw] if pw in PATHWAYS else ["explorer"],
                }
                if obj.get("evidence_of_learning") or obj.get("evidence_artifact") or obj.get("evidence"):
                    item["evidence_artifact"] = str(
                        obj.get("evidence_of_learning")
                        or obj.get("evidence_artifact")
                        or obj.get("evidence")
                    )
                if obj.get("bloom"):
                    item["bloom"] = obj["bloom"]
                if obj.get("anatomy_sections"):
                    item["anatomy_sections"] = obj["anatomy_sections"]
                objectives.append(item)
    elif isinstance(raw_objectives, list):
        for obj in raw_objectives:
            oid = obj.get("objective_id") or obj.get("id")
            text = obj.get("text") or obj.get("statement") or obj.get("objective") or ""
            pathways = as_list(obj.get("reader_pathways") or obj.get("pathway_emphasis") or obj.get("pathways"))
            pathways = [str(p).lower() for p in pathways if str(p).lower() in PATHWAYS]
            if not pathways:
                pathways = ["explorer"]
            item = {
                "objective_id": str(oid),
                "text": str(text),
                "reader_pathways": pathways,
            }
            if obj.get("evidence_artifact") or obj.get("evidence_of_learning") or obj.get("evidence"):
                item["evidence_artifact"] = str(
                    obj.get("evidence_artifact")
                    or obj.get("evidence_of_learning")
                    or obj.get("evidence")
                )
            if obj.get("bloom"):
                item["bloom"] = obj["bloom"]
            if obj.get("anatomy_sections"):
                item["anatomy_sections"] = obj["anatomy_sections"]
            objectives.append(item)
    elif isinstance(data.get("pathways"), dict):
        for pathway, items in data["pathways"].items():
            pw = str(pathway).lower()
            if not isinstance(items, list):
                continue
            for obj in items:
                oid = obj.get("id") or obj.get("objective_id")
                text = obj.get("objective") or obj.get("text") or obj.get("statement") or ""
                item = {
                    "objective_id": str(oid),
                    "text": str(text),
                    "reader_pathways": [pw] if pw in PATHWAYS else ["explorer"],
                }
                if obj.get("evidence") or obj.get("evidence_of_learning"):
                    item["evidence_artifact"] = str(obj.get("evidence") or obj.get("evidence_of_learning"))
                objectives.append(item)

    out = {
        "schema_version": SCHEMA_VERSION,
        "chapter_id": {
            "ce-01": "CE-1",
            "ce-03": "CE-3",
            "ce-04": "CE-4",
            "ce-05": "CE-5",
            "ce-06": "CE-6",
        }[chapter],
        "objectives": objectives,
    }
    for key in ("maps_to", "teaching_model", "anchor_experience", "assessment_spine"):
        if key in data:
            out[key] = data[key]
    write_yaml(path, out)


def normalize_career_map(path: Path, chapter: str) -> None:
    data = load_yaml(path) or {}
    rows = data.get("careers") if isinstance(data.get("careers"), list) else data.get("roles") or []
    careers = []
    for row in rows:
        role_family = row.get("role_family") or row.get("title") or row.get("role") or row.get("name")
        chapter_work = row.get("chapter_work") or row.get("owns") or row.get("what_they_work_on") or []
        if isinstance(chapter_work, list):
            chapter_work = "; ".join(str(x) for x in chapter_work)
        skill = row.get("technical_skill") or row.get("tools") or row.get("skills") or []
        if isinstance(skill, list):
            skill = ", ".join(str(x) for x in skill)
        evidence = row.get("student_evidence") or row.get("professional_artifact") or row.get("evidence") or ""
        portfolio = row.get("portfolio_artifact") or row.get("learner_portfolio_analogue") or row.get("portfolio") or ""
        item = {
            "role_family": str(role_family),
            "chapter_work": str(chapter_work),
            "technical_skill": str(skill),
            "student_evidence": str(evidence),
            "portfolio_artifact": str(portfolio),
        }
        if row.get("next_deeper") or row.get("next"):
            item["next_deeper"] = str(row.get("next_deeper") or row.get("next"))
        if row.get("related_concepts"):
            item["related_concepts"] = row["related_concepts"]
        if row.get("role_id"):
            item["role_id"] = row["role_id"]
        careers.append(item)

    out = {
        "schema_version": SCHEMA_VERSION,
        "chapter_id": {
            "ce-01": "CE-1",
            "ce-03": "CE-3",
            "ce-04": "CE-4",
            "ce-05": "CE-5",
            "ce-06": "CE-6",
        }[chapter],
        "employment_guarantee": bool(data.get("employment_guarantee", False)),
        "careers": careers,
    }
    if data.get("disclaimer") or data.get("note"):
        out["disclaimer"] = data.get("disclaimer") or data.get("note")
    if data.get("lab_id"):
        out["lab_id"] = data["lab_id"]
    write_yaml(path, out)


def normalize_package(chapter: str) -> None:
    d = PREPROD / chapter
    normalize_claim_plan(d / "CLAIM_PLAN.yaml", chapter)
    normalize_concept_graph(d / "CONCEPT_GRAPH.yaml", chapter)
    normalize_figure_plan(d / "FIGURE_PLAN.yaml", chapter)
    normalize_learning_objectives(d / "LEARNING_OBJECTIVES.yaml", chapter)
    normalize_career_map(d / "CAREER_MAP.yaml", chapter)
    print(f"normalized {chapter}")


def main() -> int:
    for ce in CE_DIRS:
        normalize_package(ce)
    print("normalize_ce_preproduction: DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
