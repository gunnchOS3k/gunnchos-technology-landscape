#!/usr/bin/env python3
"""Shared Full31 packet semantics, state derivation, and WAIKE parsing."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "publication/full31/chapters"
ACCEPTED_MAIN = "0e694176652d4729c7f2b71df08b871a863afb8c"
WAIKE_ACCEPTED_MAIN = "e97e74fc9bfb44b1cdc26b272dc4848264f15fe0"
GATE = "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING"

PACKET_FILES = [
    "CHAPTER_BRIEF.md",
    "CONCEPT_GRAPH.yaml",
    "CLAIM_PLAN.yaml",
    "SOURCE_NEEDS.md",
    "FIGURE_PLAN.yaml",
    "LAB_OPPORTUNITIES.md",
    "GLOSSARY_CANDIDATES.yaml",
    "WAIKE_CROSSWALK.md",
    "DEPENDENCY_MAP.yaml",
]

PREPRODUCTION_SUBSTATES = [
    "concept_preproduction_state",
    "source_state",
    "claim_state",
    "figure_state",
    "lab_state",
    "glossary_state",
    "waike_state",
]

STARTED_TOKENS = frozenset(
    {
        "PREPRODUCTION_STARTED",
        "PREPRODUCTION_COMPLETE",
        "DRAFT_STARTED",
        "DRAFT_COMPLETE",
        "TECH_REVIEW_PENDING",
        "HUMAN_VALIDATION_PENDING",
        "REVISION_REQUIRED",
        "READY_FOR_EDITORIAL",
        "PUBLICATION_READY",
    }
)

ALLOWED_CLAIM_STATUS = frozenset(
    {
        "SOURCE_IDENTIFIED",
        "SOURCE_NEEDED",
        "PROJECT_EVIDENCE_NEEDED",
        "ILLUSTRATIVE_ONLY",
        "PHYSICAL_PENDING",
    }
)

ALLOWED_CLAIM_CLASS = frozenset(
    {
        "general_technical",
        "standards_based",
        "peer_reviewed",
        "project_specific",
        "illustrative",
        "measured_later",
        "publication_internal",
    }
)

CLAIM_CLASS_ALIASES = {
    "policy": "publication_internal",
    "teaching_model": "illustrative",
    "general technical": "general_technical",
    "standards-based": "standards_based",
    "peer-reviewed": "peer_reviewed",
    "project-specific": "project_specific",
    "measured later": "measured_later",
    "publication-internal": "publication_internal",
}

BRIEF_MATCHERS = {
    "reader_promise": ["reader promise", "primary reader promise"],
    "anchor_human_moment": [
        "anchor human moment",
        "experience-first opening",
        "human moment",
        "opening moment",
    ],
    "measurable_outcomes": ["measurable outcomes"],
    "stability_contract": ["stability contract"],
    "security_equity_accessibility": [
        "security / equity / accessibility",
        "secure / include",
        "secure and include",
        "equity",
        "accessibility",
    ],
    "career_lens": ["career lens"],
    "non_goals": ["non-goals", "explicit non-goals", "non goals"],
    "next_action": [
        "next automatable",
        "next action",
        "integrator handoff",
        "handoff",
        "next steps",
    ],
}

SOURCE_NEEDS_IDENTIFIED = ["identified", "sources identified", "candidate sources", "known sources"]
SOURCE_NEEDS_GAPS = ["gap", "needed", "missing", "still needed", "source needs", "to find"]


def _load_yaml(path: Path) -> Any:
    from yaml_util import load_yaml

    return load_yaml(path)


def derive_current_state(chapter: dict[str, Any]) -> str:
    """Honest current_state from canonical prose + preproduction substates."""
    prose = str(chapter.get("canonical_prose_state") or "SCAFFOLD")
    gate_deps = " ".join(str(x) for x in (chapter.get("gate_dependencies") or []))
    human_deps = " ".join(str(x) for x in (chapter.get("human_dependencies") or []))
    under_human = (
        prose in {"DRAFT_COMPLETE", "DRAFT_STARTED"}
        and (
            "Gate 3" in gate_deps
            or "reader" in gate_deps.lower()
            or "Explorer" in human_deps
            or "Builder" in human_deps
            or "Engineer" in human_deps
            or chapter.get("claim_state") == "HUMAN_VALIDATION_PENDING"
            or chapter.get("current_state") == "HUMAN_VALIDATION_PENDING"
        )
    )
    # CH02 (and any draft under Gate 3 reader validation) stays HUMAN_VALIDATION_PENDING.
    if under_human and prose == "DRAFT_COMPLETE":
        return "HUMAN_VALIDATION_PENDING"

    dims = [str(chapter.get(k) or "SCAFFOLD") for k in PREPRODUCTION_SUBSTATES]
    if all(s == "PREPRODUCTION_COMPLETE" for s in dims):
        return "PREPRODUCTION_COMPLETE"
    if any(s in STARTED_TOKENS for s in dims) or prose in STARTED_TOKENS:
        return "PREPRODUCTION_STARTED"
    return "SCAFFOLD"


def _text_has_any(text: str, needles: list[str]) -> bool:
    low = text.lower()
    return any(n.lower() in low for n in needles)


def validate_chapter_brief(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 200:
        errors.append(f"{path.name}: too short to be a substantive brief")
    for topic, matchers in BRIEF_MATCHERS.items():
        if not _text_has_any(text, matchers):
            errors.append(f"{path.name}: missing topic {topic}")
    return errors


def validate_source_needs(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 80:
        errors.append(f"{path.name}: too short")
    if not _text_has_any(text, SOURCE_NEEDS_IDENTIFIED):
        errors.append(f"{path.name}: must distinguish identified sources")
    if not _text_has_any(text, SOURCE_NEEDS_GAPS):
        errors.append(f"{path.name}: must distinguish source gaps / needs")
    return errors


def validate_lab_opportunities(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 80:
        errors.append(f"{path.name}: too short")
    has_activity = bool(
        re.search(r"LAB-|lab opportunity|plausible|activity|fixture|route", text, re.I)
    )
    has_none = bool(re.search(r"no lab|none required|explicit(?:ly)? none|reason none", text, re.I))
    if not (has_activity or has_none):
        errors.append(f"{path.name}: need at least one plausible activity or explicit none reason")
    return errors


def validate_concept_graph(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    doc = _load_yaml(path) or {}
    if "nodes" in doc:
        errors.append(f"{path.name}: forbidden top-level key nodes")
    concepts = doc.get("concepts") or []
    if not concepts:
        errors.append(f"{path.name}: concepts must be non-empty")
        return errors
    required = [
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
    ]
    for c in concepts:
        cid = c.get("concept_id") or "<missing>"
        for field in required:
            if field not in c:
                errors.append(f"{path.name}:{cid}: missing {field}")
        if not str(c.get("canonical_term") or "").strip():
            errors.append(f"{path.name}:{cid}: empty canonical_term")
        if not str(c.get("plain_language_definition") or "").strip():
            errors.append(f"{path.name}:{cid}: empty definition")
        if not str(c.get("likely_misconception") or "").strip():
            errors.append(f"{path.name}:{cid}: empty likely_misconception")
        if not isinstance(c.get("depends_on"), list):
            errors.append(f"{path.name}:{cid}: depends_on must be a list")
    return errors


def _project_evidence_ok(pe: Any) -> bool:
    if not isinstance(pe, dict):
        return False
    repo = str(pe.get("repo") or pe.get("repository") or "").strip()
    commit = str(pe.get("commit") or pe.get("sha") or pe.get("accepted_main_sha") or "").strip()
    path = str(pe.get("path") or pe.get("paths") or "").strip()
    if isinstance(pe.get("paths"), list) and pe.get("paths"):
        path = "ok"
    return bool(repo and commit and path)


def validate_claim_plan(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    doc = _load_yaml(path) or {}
    claims = doc.get("claims") or []
    if not claims:
        errors.append(f"{path.name}: claims must be non-empty")
        return errors
    required = [
        "provisional_id",
        "text",
        "claim_class",
        "evidence_required",
        "status",
        "citation_keys",
        "overclaim_risk",
        "wording_boundary",
    ]
    for c in claims:
        cid = c.get("provisional_id") or "<missing>"
        for field in required:
            if field not in c or c.get(field) in (None, ""):
                if field == "citation_keys" and isinstance(c.get("citation_keys"), list):
                    continue
                errors.append(f"{path.name}:{cid}: missing {field}")
        status = c.get("status")
        if status not in ALLOWED_CLAIM_STATUS:
            errors.append(f"{path.name}:{cid}: invalid status {status!r}")
        klass = c.get("claim_class")
        if klass not in ALLOWED_CLAIM_CLASS:
            errors.append(f"{path.name}:{cid}: unknown claim_class {klass!r}")
        keys = c.get("citation_keys") or []
        if not isinstance(keys, list):
            errors.append(f"{path.name}:{cid}: citation_keys must be a list")
            keys = []
        if status == "SOURCE_IDENTIFIED":
            if not keys and not _project_evidence_ok(c.get("project_evidence")):
                errors.append(
                    f"{path.name}:{cid}: SOURCE_IDENTIFIED requires citation_keys or project_evidence"
                )
        if status == "SOURCE_NEEDED":
            blob = " ".join(
                str(c.get(k) or "")
                for k in ("text", "wording_boundary", "overclaim_risk", "evidence_required")
            ).lower()
            if re.search(r"\b(verified|proven|measured fact)\b", blob):
                errors.append(f"{path.name}:{cid}: SOURCE_NEEDED must not pretend verified")
        if status == "ILLUSTRATIVE_ONLY":
            blob = " ".join(str(c.get(k) or "") for k in ("text", "wording_boundary")).lower()
            if re.search(r"\b(measured|empirical fact|general fact)\b", blob) and "not" not in blob:
                # soft: only flag if wording presents as measured without hedge
                if "illustrative" not in blob and "not measured" not in blob:
                    errors.append(
                        f"{path.name}:{cid}: ILLUSTRATIVE_ONLY presented without illustrative boundary"
                    )
        if status == "PHYSICAL_PENDING":
            blob = " ".join(
                str(c.get(k) or "")
                for k in ("text", "evidence_required", "overclaim_risk", "wording_boundary")
            )
            if "PHYSICAL" not in blob and "physical" not in blob.lower() and "Quartet" not in blob:
                errors.append(f"{path.name}:{cid}: PHYSICAL_PENDING must identify physical dependency")
        if status == "PROJECT_EVIDENCE_NEEDED":
            blob = " ".join(str(c.get(k) or "") for k in ("text", "evidence_required")).lower()
            if "project" not in blob and "repository" not in blob and "accepted" not in blob:
                if not c.get("project_evidence"):
                    errors.append(
                        f"{path.name}:{cid}: PROJECT_EVIDENCE_NEEDED must identify missing project evidence"
                    )
    return errors


def validate_figure_plan(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    doc = _load_yaml(path) or {}
    figs = doc.get("figures") or []
    none_reason = (
        doc.get("no_figures_reason")
        or doc.get("explicit_none_reason")
        or doc.get("none_reason")
    )
    if not figs and not none_reason:
        errors.append(f"{path.name}: need figures or explicit none reason")
    for f in figs:
        fid = f.get("provisional_id") or "<missing>"
        for field in ("provisional_id", "figure_type", "pedagogical_purpose", "truth_classification"):
            if not f.get(field):
                errors.append(f"{path.name}:{fid}: missing {field}")
    return errors


def _glossary_entries(doc: dict[str, Any]) -> list[Any]:
    for key in ("candidates", "entries", "terms", "glossary_candidates"):
        val = doc.get(key)
        if isinstance(val, list):
            return val
    return []


def validate_glossary(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    doc = _load_yaml(path) or {}
    entries = _glossary_entries(doc)
    inherited = (
        doc.get("inherited_from")
        or doc.get("inheritance_note")
        or doc.get("inherits_from")
    )
    if not entries and not inherited:
        errors.append(f"{path.name}: non-empty glossary candidates or inheritance note required")
    for e in entries:
        if not isinstance(e, dict):
            errors.append(f"{path.name}: glossary entry must be mapping")
            continue
        has_id = any(e.get(k) for k in ("provisional_id", "term_id", "canonical_term", "proposed_term", "term"))
        has_def = any(e.get(k) for k in ("plain_language_definition", "definition"))
        if not has_id or not has_def:
            errors.append(f"{path.name}: glossary entry needs term id/name and definition")
    return errors


def validate_dependency_map(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    doc = _load_yaml(path) or {}
    keys = (
        "prerequisites",
        "depends_on",
        "upstream_chapters",
        "later_links",
        "downstream_chapters",
        "reinforces",
        "inherits_from",
        "related_chapters",
        "dependencies",
        "ce_inheritance",
        "labs",
        "upstream",
        "downstream",
    )
    present = []
    for k in keys:
        v = doc.get(k)
        if v:
            present.append(k)
    if not present and not doc.get("no_dependencies_reason"):
        # also accept nested maps under dependency_map
        if not any(isinstance(v, (list, dict)) and v for k, v in doc.items() if k not in {"schema_version", "chapter_id", "gate_note", "status"}):
            errors.append(f"{path.name}: missing real prerequisites/later links")
    return errors


def validate_waike_crosswalk(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing {path.name}"]
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 80:
        errors.append(f"{path.name}: too short")
    # Disallow invented relationship labels outside allowed set in status cells.
    # Allow legend prose; check mapping rows with backticks / table status cells.
    for m in re.finditer(r"\|\s*\*?\*?(exact|adjacent|proposed|no-map|no_map|invented|approx)\*?\*?\s*\|", text, re.I):
        rel = m.group(1).lower().replace("_", "-")
        if rel not in {"exact", "adjacent", "proposed", "no-map"}:
            errors.append(f"{path.name}: disallowed WAIKE relationship {m.group(1)!r}")
    return errors


def validate_packet_dir(packet: Path) -> tuple[str, list[str]]:
    """Return (packet_state, errors)."""
    errors: list[str] = []
    existing = [name for name in PACKET_FILES if (packet / name).exists()]
    if not existing:
        return "PACKET_MISSING", [f"{packet}: no packet files"]
    missing = [name for name in PACKET_FILES if not (packet / name).exists()]
    for name in missing:
        errors.append(f"missing {name}")

    errors.extend(validate_chapter_brief(packet / "CHAPTER_BRIEF.md"))
    errors.extend(validate_concept_graph(packet / "CONCEPT_GRAPH.yaml"))
    errors.extend(validate_claim_plan(packet / "CLAIM_PLAN.yaml"))
    errors.extend(validate_source_needs(packet / "SOURCE_NEEDS.md"))
    errors.extend(validate_figure_plan(packet / "FIGURE_PLAN.yaml"))
    errors.extend(validate_lab_opportunities(packet / "LAB_OPPORTUNITIES.md"))
    errors.extend(validate_glossary(packet / "GLOSSARY_CANDIDATES.yaml"))
    errors.extend(validate_waike_crosswalk(packet / "WAIKE_CROSSWALK.md"))
    errors.extend(validate_dependency_map(packet / "DEPENDENCY_MAP.yaml"))

    if missing or errors:
        # files present but incomplete/invalid
        if existing and (missing or errors):
            # If all files exist but semantic errors → still STARTED until fixed;
            # COMPLETE only when zero errors and no missing.
            if missing:
                return "PACKET_STARTED", errors
            return "PACKET_STARTED", errors
    return "PACKET_COMPLETE", []


def parse_waike_crosswalk(path: Path) -> dict[str, Any]:
    """Deterministic per-chapter WAIKE counts + unique upstream IDs."""
    text = path.read_text(encoding="utf-8")
    counts = {"exact": 0, "adjacent": 0, "proposed": 0, "no_map": 0}
    ids: set[str] = set()

    # Prefer explicit count tables when present.
    table_counts: dict[str, int] = {}
    for cls in ("exact", "adjacent", "proposed", "no-map", "no_map"):
        m = re.search(rf"\|\s*`?{cls}`?\s*\|\s*(\d+)\s*\|", text, re.I)
        if m:
            key = "no_map" if cls in {"no-map", "no_map"} else cls.lower()
            table_counts[key] = int(m.group(1))

    row_counts: Counter[str] = Counter()
    status_idx: int | None = None
    in_mapping_table = False

    def norm_rel(token: str) -> str | None:
        t = token.strip().lower().replace("*", "").replace("`", "").replace("_", "-")
        t = re.sub(r"[^a-z\-]", "", t)
        if t in {"exact", "adjacent", "proposed"}:
            return t
        if t in {"no-map", "nomap"}:
            return "no_map"
        return None

    def pure_rel_cell(cell: str) -> str | None:
        if re.fullmatch(
            r"\*{0,2}`?(exact|adjacent|proposed|no-map|no_map)`?\*{0,2}",
            cell.strip(),
            re.I,
        ):
            return norm_rel(cell)
        return None

    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        if all(re.fullmatch(r"[\-:]+", c or "") for c in cells):
            continue

        low_cells = [re.sub(r"[*`]", "", c).strip().lower() for c in cells]
        low0 = low_cells[0]

        if low0 in {"book object", "waike id"} or (
            low0.startswith("book object") and any("waike" in h for h in low_cells)
        ):
            in_mapping_table = True
            status_idx = None
            for i, h in enumerate(low_cells):
                if h in {"relationship", "status", "map class"} or "relationship" in h:
                    status_idx = i
                    break
            continue

        # Legend / vocabulary / count tables
        if low0 in {"exact", "adjacent", "proposed", "no-map", "nomap", "class", "status"}:
            continue
        if len(low_cells) > 1 and (low_cells[1] == "meaning" or low_cells[1] == "count"):
            continue

        if not in_mapping_table:
            continue

        rel = None
        if status_idx is not None and status_idx < len(cells):
            rel = pure_rel_cell(cells[status_idx]) or norm_rel(cells[status_idx])
            # Status cell may include bold markers only
            if rel is None and pure_rel_cell(cells[status_idx].replace(" ", "")):
                rel = pure_rel_cell(cells[status_idx])
        if rel is None:
            for cell in cells:
                maybe = pure_rel_cell(cell)
                if maybe:
                    rel = maybe
                    break
        if rel:
            row_counts[rel] += 1

        for mid in re.findall(r"`([^`]+)`", line):
            token = mid.strip()
            if token in {"—", "-", ""}:
                continue
            if token.upper().startswith("CH") and re.match(r"CH\d+", token.upper()):
                continue
            if token.startswith("LAB-"):
                continue
            if (
                re.search(r"digital_rc|catalog|lab_|[A-Z]{3,}_", token)
                or "_" in token
                or token.isupper()
                or token.islower()
            ):
                for part in re.split(r"\s*,\s*|\s*/\s*", token):
                    part = part.strip()
                    if not part or part in {"—", "-"}:
                        continue
                    if part.upper().startswith("CH") or part.startswith("LAB-"):
                        continue
                    ids.add(part)

    # Section-style lists when no count table and no mapping-table rows
    if not table_counts and sum(row_counts.values()) == 0:
        for section, key in (
            (r"##\s*Exact\b(.*?)(?=##|\Z)", "exact"),
            (r"##\s*Adjacent\b(.*?)(?=##|\Z)", "adjacent"),
            (r"##\s*Proposed\b(.*?)(?=##|\Z)", "proposed"),
            (r"##\s*No-?map\b(.*?)(?=##|\Z)", "no_map"),
        ):
            m = re.search(section, text, re.I | re.S)
            if not m:
                continue
            body = m.group(1)
            if re.search(r"_None\.?_|^\s*_None", body, re.M) and key == "exact":
                row_counts[key] = 0
                continue
            rows = [
                ln
                for ln in body.splitlines()
                if ln.strip().startswith("|")
                and "---" not in ln
                and "WAIKE ID" not in ln
                and "Notes" not in ln
                and "Proposal" not in ln
            ]
            bullets = [
                ln
                for ln in body.splitlines()
                if re.match(r"\s*[-*]", ln) and not re.search(r"_None|None\.", ln)
            ]
            n = len([r for r in rows if "`" in r or "—" in r or re.search(r"[A-Za-z]", r)]) + len(
                bullets
            )
            row_counts[key] = n

    if table_counts:
        counts.update({k: int(v) for k, v in table_counts.items()})
    else:
        counts.update({k: int(v) for k, v in row_counts.items()})

    try:
        rel_path = str(path.resolve().relative_to(ROOT))
    except Exception:
        rel_path = str(path)

    return {
        "counts": counts,
        "unique_waike_ids": sorted(ids),
        "unique_waike_id_count": len(ids),
        "path": rel_path,
    }


def aggregate_all_waike() -> dict[str, Any]:
    per_chapter: dict[str, Any] = {}
    totals: Counter[str] = Counter()
    all_ids: set[str] = set()
    per_part: dict[str, Counter[str]] = {}

    registry_path = ROOT / "publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml"
    part_by_ch: dict[str, str] = {}
    if registry_path.exists():
        reg = _load_yaml(registry_path) or {}
        for ch in reg.get("chapters") or []:
            part_by_ch[ch["chapter_id"]] = str(ch.get("part") or "?")

    for packet in sorted(CHAPTERS_DIR.glob("ch*/")):
        cross = packet / "WAIKE_CROSSWALK.md"
        if not cross.exists():
            continue
        m = re.match(r"ch(\d+)$", packet.name, re.I)
        cid = f"CH{int(m.group(1)):02d}" if m else packet.name.upper()
        parsed = parse_waike_crosswalk(cross)
        per_chapter[cid] = parsed
        for k, v in parsed["counts"].items():
            totals[k] += int(v)
        all_ids.update(parsed["unique_waike_ids"])
        part = part_by_ch.get(cid, "?")
        per_part.setdefault(part, Counter())
        for k, v in parsed["counts"].items():
            per_part[part][k] += int(v)

    return {
        "waike_accepted_main_sha": WAIKE_ACCEPTED_MAIN,
        "totals": {
            "exact": int(totals.get("exact", 0)),
            "adjacent": int(totals.get("adjacent", 0)),
            "proposed": int(totals.get("proposed", 0)),
            "no_map": int(totals.get("no_map", 0)),
        },
        "unique_upstream_waike_objects": len(all_ids),
        "unique_upstream_waike_ids": sorted(all_ids),
        "per_chapter": per_chapter,
        "per_part": {p: dict(c) for p, c in sorted(per_part.items())},
    }
