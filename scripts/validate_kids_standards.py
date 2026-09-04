#!/usr/bin/env python3
"""Validate Kids Global Standards Atlas YAML artifacts."""

from __future__ import annotations

import argparse
import re
import sys
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
    "IDENTIFIED",
    "TRANSLATION_REQUIRED",
    "ACCESS_BLOCKED",
    "NOT_YET_RESEARCHED",
    "SOURCE_VERSION_UNCLEAR",
}

FIDELITIES = {"EXACT", "ADJACENT", "PROPOSED", "NO_MAP", "NOT_YET_MAPPED"}
RELATIONSHIPS = {"CROSSWALKED_AGAINST", "MAPPED_TO", "INFORMED_BY"}

FORBIDDEN_CLAIM = re.compile(
    r"\b(officially aligned|certified against|accredited to)\b",
    re.IGNORECASE,
)


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a mapping at top level")
    return data


def validate() -> list[str]:
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
            gaps = row.get("gaps") or []
            if row.get("version") == "SOURCE_VERSION_UNCLEAR" and "SOURCE_VERSION_UNCLEAR" not in gaps:
                # allow version literal as the gap signal
                pass
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

    # Coverage architecture minimum: world census should be large
    if len(jurisdictions) < 200:
        errors.append(
            f"jurisdiction census too small ({len(jurisdictions)}); expected exhaustive world architecture (≥200)"
        )

    # Mandatory baselines present
    mandatory_ids = {
        "FW-UNESCO-AI-STUDENTS-2024",
        "FW-OECD-LEARNING-COMPASS-2030",
        "FW-US-HS-ELOF",
        "FW-CSTA-PK12-2026",
        "FW-US-NGSS",
        "FW-GB-ENG-EYFS-2026",
        "FW-AU-EYLF-V2",
        "FW-AU-AC-V9",
        "FW-NZ-TE-WHARIKI",
        "FW-SG-NEL-2022",
        "FW-IN-NCF-FOUNDATIONAL",
        "FW-ZA-CAPS",
        "FW-CA-ON-KINDERGARTEN-2016",
    }
    missing_mandatory = sorted(mandatory_ids - set(fw_ids))
    if missing_mandatory:
        errors.append(f"missing mandatory frameworks: {missing_mandatory}")

    report = (STANDARDS / "GLOBAL_STANDARDS_COVERAGE_REPORT.md").read_text(encoding="utf-8")
    for needle in (
        "Jurisdiction metrics",
        "Mapping metrics",
        "Mandatory framework baseline status",
        "Honest gaps",
    ):
        if needle not in report:
            errors.append(f"coverage report missing section: {needle}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    errors = validate()
    if errors:
        print("kids-standards-check FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("kids-standards-check PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
