#!/usr/bin/env python3
"""Validate Kids Global Standards Atlas YAML artifacts.

Modes:
  --architecture       Structure, mandatory pins, census floor (default when no mode flag).
  --research-complete  Fail if any jurisdiction remains NOT_YET_RESEARCHED.
  --pilot-mapped       Fail dangling STD-WIRE-* atlas refs unless justified NOT_YET_MAPPED/NO_MAP.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STANDARDS = ROOT / "kids" / "standards"

REQUIRED_FILES = [
    "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml",
    "GLOBAL_STANDARDS_SOURCE_REGISTER.yaml",
    "GLOBAL_STANDARDS_ATLAS.yaml",
    "GLOBAL_STANDARDS_COVERAGE_REPORT.md",
    "STANDARD_MAPPING_SCHEMA.md",
]

JUR_STATUSES = {
    "OFFICIAL_VERIFIED",
    "OFFICIAL_SOURCE_VERIFIED",
    "OFFICIAL_PORTAL_IDENTIFIED",
    "IDENTIFIED",
    "TRANSLATION_REQUIRED",
    "ACCESS_BLOCKED",
    "NOT_YET_RESEARCHED",
    "SOURCE_VERSION_UNCLEAR",
    "NO_CENTRAL_NATIONAL_CURRICULUM",
    "SUBNATIONAL_RESEARCH_REQUIRED",
}

FIDELITIES = {"EXACT", "ADJACENT", "PROPOSED", "NO_MAP", "NOT_YET_MAPPED"}
RELATIONSHIPS = {"CROSSWALKED_AGAINST", "MAPPED_TO", "INFORMED_BY"}
WIRE_JUSTIFIED_UNMAPPED = {"NOT_YET_MAPPED", "NO_MAP"}

FORBIDDEN_CLAIM = re.compile(
    r"\b(officially aligned|certified against|accredited to)\b",
    re.IGNORECASE,
)

# Mandatory baseline pins (authority / national / subnational anchors).
MANDATORY_IDS = {
    "FW-UNESCO-AI-STUDENTS-2024",
    "FW-UNESCO-AI-TEACHERS-2024",
    "FW-OECD-LEARNING-COMPASS-2030",
    "FW-IB-PYP-PUBLIC",
    "FW-US-HS-ELOF",
    "FW-US-CCSS-2010",
    "FW-CSTA-PK12-2026",
    "FW-US-NGSS",
    "FW-GB-ENG-EYFS-2026",
    "FW-GB-ENG-NC-PRIMARY",
    "FW-GB-SCT-CFE",
    "FW-GB-WLS-CFW",
    "FW-GB-NIR-CURRICULUM",
    "FW-AU-EYLF-V2",
    "FW-AU-AC-V9",
    "FW-NZ-TE-WHARIKI",
    "FW-FI-ECEC",
    "FW-FI-BASIC",
    "FW-IN-NCF-FOUNDATIONAL",
    "FW-SG-NEL-2022",
    "FW-JP-MEXT-COS",
    "FW-ZA-CAPS",
    "FW-CA-ON-KINDERGARTEN-2016",
}


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a mapping at top level")
    return data


def validate_architecture() -> list[str]:
    errors: list[str] = []

    for name in REQUIRED_FILES:
        if not (STANDARDS / name).is_file():
            errors.append(f"missing required file: kids/standards/{name}")
    if errors:
        return errors

    jur = load_yaml(STANDARDS / "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml")
    src = load_yaml(STANDARDS / "GLOBAL_STANDARDS_SOURCE_REGISTER.yaml")
    atlas = load_yaml(STANDARDS / "GLOBAL_STANDARDS_ATLAS.yaml")

    jurisdictions = jur.get("jurisdictions") or []
    frameworks = src.get("frameworks") or []
    targets = atlas.get("kids_targets") or []
    mappings = atlas.get("mappings") or []

    jur_ids = {}
    for row in jurisdictions:
        jid = row.get("jurisdiction_id")
        if not jid:
            errors.append("jurisdiction missing jurisdiction_id")
            continue
        if jid in jur_ids:
            errors.append(f"duplicate jurisdiction_id: {jid}")
        jur_ids[jid] = row
        status = row.get("research_status")
        if status not in JUR_STATUSES:
            errors.append(f"{jid}: invalid research_status {status!r}")

    fw_ids = {}
    for row in frameworks:
        fid = row.get("framework_id")
        if not fid:
            errors.append("framework missing framework_id")
            continue
        if fid in fw_ids:
            errors.append(f"duplicate framework_id: {fid}")
        fw_ids[fid] = row
        for jid in row.get("jurisdiction_ids") or []:
            if jid not in jur_ids:
                errors.append(f"{fid}: unknown jurisdiction_id {jid}")
        if row.get("verification") == "OFFICIAL_VERIFIED":
            for field in ("url", "authority", "retrieved_on", "version"):
                if not row.get(field):
                    errors.append(f"{fid}: OFFICIAL_VERIFIED missing {field}")
        text_blob = " ".join(
            str(row.get(k) or "")
            for k in ("title", "notes", "license_note")
        )
        if FORBIDDEN_CLAIM.search(text_blob) and "AUTHORITY_CLAIMS:" not in text_blob:
            errors.append(f"{fid}: forbidden certification/alignment claim language")

    for row in jurisdictions:
        for fid in row.get("framework_ids") or []:
            if fid not in fw_ids:
                errors.append(f"{row.get('jurisdiction_id')}: unknown framework_id {fid}")

    target_ids = {}
    for row in targets:
        tid = row.get("kids_target_id")
        if not tid:
            errors.append("kids_target missing kids_target_id")
            continue
        target_ids[tid] = row

    map_ids = set()
    for row in mappings:
        mid = row.get("mapping_id")
        if not mid:
            errors.append("mapping missing mapping_id")
            continue
        if mid in map_ids:
            errors.append(f"duplicate mapping_id: {mid}")
        map_ids.add(mid)
        rel = row.get("relationship")
        if rel not in RELATIONSHIPS:
            errors.append(f"{mid}: invalid relationship {rel!r}")
        fid_level = row.get("fidelity")
        if fid_level not in FIDELITIES:
            errors.append(f"{mid}: invalid fidelity {fid_level!r}")
        ff = row.get("from_framework_id")
        if ff not in fw_ids:
            errors.append(f"{mid}: unknown from_framework_id {ff}")
        tid = row.get("to_kids_target_id")
        if tid not in target_ids:
            errors.append(f"{mid}: unknown to_kids_target_id {tid}")
        if fid_level in {"EXACT", "ADJACENT", "PROPOSED"}:
            notes = (row.get("notes") or "").strip()
            if not notes:
                errors.append(f"{mid}: {fid_level} mapping requires notes disclaimer")
            elif FORBIDDEN_CLAIM.search(notes) and "AUTHORITY_CLAIMS:" not in notes:
                errors.append(f"{mid}: forbidden certification/alignment claim language")

    if len(jurisdictions) < 200:
        errors.append(
            f"jurisdiction census too small ({len(jurisdictions)}); "
            "expected exhaustive world architecture (≥200)"
        )

    missing_mandatory = sorted(MANDATORY_IDS - set(fw_ids))
    if missing_mandatory:
        errors.append(f"missing mandatory frameworks: {missing_mandatory}")

    report = (STANDARDS / "GLOBAL_STANDARDS_COVERAGE_REPORT.md").read_text(encoding="utf-8")
    for needle in (
        "Jurisdiction metrics",
        "Mapping metrics",
        "Mandatory framework baseline status",
        "Honest gaps",
        "NOT_YET_RESEARCHED",
    ):
        if needle not in report:
            errors.append(f"coverage report missing section/metric: {needle}")

    # Forbid vanity aggregate phrasing that collapses census into "researched standards".
    # Allow explicit rejection / example lines that warn against the phrase.
    vanity = re.compile(
        r"\b(\d{2,4})\s+standards\s+researched\b",
        re.IGNORECASE,
    )
    for m in vanity.finditer(report):
        window = report[max(0, m.start() - 100) : m.end() + 80]
        if re.search(
            r"(?i)(vanity|do\s+\*\*not\*\*|do not|never|≠|not\s+collapse|forbid|reject|example)",
            window,
        ):
            continue
        errors.append(
            "coverage report uses vanity phrasing like 'N standards researched'; "
            "keep separate census / researched / portal / pinned / deep-mapped metrics"
        )
        break

    # US 50+DC (+ optional federal JUR-US), Canada P/T present
    us_states = [
        jid
        for jid in jur_ids
        if jid.startswith("JUR-US-") and jid != "JUR-US-DC"
    ]
    if "JUR-US-DC" not in jur_ids:
        errors.append("missing JUR-US-DC (District of Columbia)")
    if len(us_states) < 50:
        errors.append(f"US state rows expected ≥50, found {len(us_states)}")
    ca_pt = [jid for jid in jur_ids if jid.startswith("JUR-CA-")]
    if len(ca_pt) < 13:
        errors.append(f"Canada province/territory rows expected ≥13, found {len(ca_pt)}")

    return errors


def validate_research_complete() -> list[str]:
    errors = validate_architecture()
    jur = load_yaml(STANDARDS / "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml")
    jurisdictions = jur.get("jurisdictions") or []
    nyr = [
        row.get("jurisdiction_id")
        for row in jurisdictions
        if row.get("research_status") == "NOT_YET_RESEARCHED"
    ]
    if nyr:
        errors.append(
            f"research-complete FAIL: NOT_YET_RESEARCHED={len(nyr)} "
            f"(examples: {', '.join(nyr[:12])}{'…' if len(nyr) > 12 else ''})"
        )
    return errors


def validate_pilot_mapped() -> list[str]:
    """Pilot/wire integrity: mapped hooks must resolve; unmapped must be justified."""
    errors: list[str] = []
    wire_path = STANDARDS / "WIRE_HOOK_REGISTRY.yaml"
    if not wire_path.is_file():
        return ["missing kids/standards/WIRE_HOOK_REGISTRY.yaml"]

    atlas = load_yaml(STANDARDS / "GLOBAL_STANDARDS_ATLAS.yaml")
    map_ids = {m.get("mapping_id") for m in (atlas.get("mappings") or []) if m.get("mapping_id")}
    wire = load_yaml(wire_path)
    hooks = wire.get("hooks") or []
    if not hooks:
        errors.append("WIRE_HOOK_REGISTRY has no hooks")
        return errors

    for hook in hooks:
        wid = hook.get("wire_id") or "<missing-wire_id>"
        status = hook.get("status")
        mids = hook.get("atlas_mapping_ids") or []
        rationale = (hook.get("rationale") or "").strip()

        if status in WIRE_JUSTIFIED_UNMAPPED:
            if not rationale:
                errors.append(f"{wid}: status={status} requires non-empty rationale")
            if mids:
                # Allow empty only; dangling IDs on unmapped are dishonest
                bad = [m for m in mids if m not in map_ids]
                if bad:
                    errors.append(f"{wid}: {status} hook has unknown atlas_mapping_ids {bad}")
            continue

        if not mids:
            errors.append(
                f"{wid}: status={status!r} missing atlas_mapping_ids "
                f"(use NOT_YET_MAPPED/NO_MAP + rationale if no honest map)"
            )
            continue
        bad = [m for m in mids if m not in map_ids]
        if bad:
            errors.append(f"{wid}: dangling atlas_mapping_ids {bad}")

    summary = wire.get("summary") or {}
    if summary.get("official_alignment_claims", 1) != 0:
        errors.append("wire registry must record official_alignment_claims: 0")

    return errors


def print_metrics() -> None:
    jur = load_yaml(STANDARDS / "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml")
    src = load_yaml(STANDARDS / "GLOBAL_STANDARDS_SOURCE_REGISTER.yaml")
    atlas = load_yaml(STANDARDS / "GLOBAL_STANDARDS_ATLAS.yaml")
    wire = load_yaml(STANDARDS / "WIRE_HOOK_REGISTRY.yaml")
    rows = jur.get("jurisdictions") or []
    status_counts = Counter(r.get("research_status") for r in rows)
    maps = atlas.get("mappings") or []
    fid_counts = Counter(m.get("fidelity") for m in maps)
    deep = sum(1 for m in maps if m.get("fidelity") in {"EXACT", "ADJACENT", "PROPOSED"})
    hooks = wire.get("hooks") or []
    hook_status = Counter(h.get("status") for h in hooks)
    pilot_hooks = [h for h in hooks if h.get("scope") == "pilot_spread" or h.get("pilot")]
    print(
        "metrics:",
        f"census={len(rows)}",
        f"researched(non-NYR)={sum(1 for r in rows if r.get('research_status') != 'NOT_YET_RESEARCHED')}",
        f"NYR={status_counts.get('NOT_YET_RESEARCHED', 0)}",
        f"portals={status_counts.get('OFFICIAL_PORTAL_IDENTIFIED', 0)}",
        f"frameworks_pinned={len(src.get('frameworks') or [])}",
        f"deep_mapped={deep}",
        f"fidelity={dict(fid_counts)}",
        f"wire_hooks={len(hooks)}",
        f"wire_by_status={dict(hook_status)}",
        f"pilot_hooks={len(pilot_hooks)}",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--architecture",
        action="store_true",
        help="Validate atlas architecture + mandatory pins (default)",
    )
    mode.add_argument(
        "--research-complete",
        action="store_true",
        help="Fail if any NOT_YET_RESEARCHED jurisdictions remain",
    )
    mode.add_argument(
        "--pilot-mapped",
        action="store_true",
        help="Fail dangling STD-WIRE atlas refs unless justified NOT_YET_MAPPED/NO_MAP",
    )
    parser.add_argument("--metrics", action="store_true", help="Print separate coverage metrics")
    args = parser.parse_args(argv)

    if args.research_complete:
        label = "kids-standards-research-complete-check"
        errors = validate_research_complete()
    elif args.pilot_mapped:
        label = "kids-pilot-mapped-check"
        errors = validate_pilot_mapped()
    else:
        label = "kids-standards-check"
        errors = validate_architecture()

    if args.metrics and not errors:
        try:
            print_metrics()
        except Exception as exc:  # noqa: BLE001 — diagnostics only
            print(f"metrics unavailable: {exc}", file=sys.stderr)

    if errors:
        print(f"{label} FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"{label} PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
