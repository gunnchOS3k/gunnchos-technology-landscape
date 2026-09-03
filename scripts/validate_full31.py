#!/usr/bin/env python3
"""Validate Full31 registry + packet semantic completeness + honest state derivation."""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from full31_common import (  # noqa: E402
    GATE,
    PACKET_FILES,
    PREPRODUCTION_SUBSTATES,
    aggregate_all_waike,
    derive_current_state,
    validate_packet_dir,
)
from yaml_util import load_yaml  # noqa: E402

REGISTRY = ROOT / "publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml"
REPORT = ROOT / "publication/full31/FULL31_PROGRESS_REPORT.md"
SCHEMA_DIR = ROOT / "publication/full31/schema"

REQUIRED_SCHEMAS = [
    "README.md",
    "chapter_registry.schema.yaml",
    "chapter_packet.schema.yaml",
    "full31_claim_plan.schema.yaml",
    "full31_concept_graph.schema.yaml",
    "full31_figure_plan.schema.yaml",
    "full31_glossary.schema.yaml",
    "full31_dependency_map.schema.yaml",
]

REQUIRED_FIELDS = [
    "chapter_number",
    "chapter_id",
    "title",
    "part",
    "packet_state",
    "current_state",
    "canonical_prose_state",
    *PREPRODUCTION_SUBSTATES,
    "next_automatable_action",
    "packet_path",
]


def main() -> int:
    errors: list[str] = []

    for name in REQUIRED_SCHEMAS:
        if not (SCHEMA_DIR / name).exists():
            errors.append(f"missing schema {name}")

    if not REGISTRY.exists():
        print("validate_full31: FAIL")
        print(" - missing CHAPTER_PRODUCTION_REGISTRY.yaml")
        return 1
    if not REPORT.exists():
        errors.append("missing FULL31_PROGRESS_REPORT.md")

    doc = load_yaml(REGISTRY)
    if str(doc.get("schema_version")) != "1.0.0":
        errors.append(f"schema_version must be 1.0.0, got {doc.get('schema_version')!r}")
    gate = str(doc.get("gate_posture") or "")
    if gate != GATE:
        errors.append(f"gate_posture must remain READER_EVIDENCE_PENDING, got {gate!r}")
    if "PASS" in gate and "IN_PROGRESS" not in gate:
        errors.append("Gate 3 PASS is forbidden")

    chapters = doc.get("chapters") or []
    if len(chapters) != 31:
        errors.append(f"expected 31 chapters, found {len(chapters)}")

    nums = [int(c.get("chapter_number")) for c in chapters]
    ids = [c.get("chapter_id") for c in chapters]
    titles = [c.get("title") for c in chapters]
    if sorted(nums) != list(range(1, 32)):
        errors.append(f"chapter_number set must be 1..31, got {sorted(nums)}")
    if len(set(ids)) != len(ids):
        errors.append("duplicate chapter_id values")
    if len(set(titles)) != len(titles):
        errors.append("duplicate chapter titles")

    packet_states: Counter[str] = Counter()
    derived_states: Counter[str] = Counter()
    claim_status: Counter[str] = Counter()
    claim_class: Counter[str] = Counter()
    invalid_source_identified = 0

    for ch in chapters:
        cid = ch.get("chapter_id")
        for field in REQUIRED_FIELDS:
            if field not in ch or ch.get(field) in (None, ""):
                errors.append(f"{cid}: missing {field}")
        action = str(ch.get("next_automatable_action") or "").strip()
        if not action:
            errors.append(f"{cid}: next_automatable_action empty")

        packet = ROOT / str(ch.get("packet_path") or "")
        if not packet.is_dir():
            errors.append(f"{cid}: packet_path missing directory {ch.get('packet_path')}")
            packet_states["PACKET_MISSING"] += 1
            continue

        expected_packet, packet_errors = validate_packet_dir(packet)
        packet_states[expected_packet] += 1
        if ch.get("packet_state") != expected_packet:
            errors.append(
                f"{cid}: packet_state={ch.get('packet_state')!r} expected {expected_packet!r}"
            )
        for e in packet_errors:
            errors.append(f"{cid}: {e}")

        expected_current = derive_current_state(ch)
        derived_states[expected_current] += 1
        if ch.get("current_state") != expected_current:
            errors.append(
                f"{cid}: current_state={ch.get('current_state')!r} expected {expected_current!r} "
                f"(substates do not support claimed maturity)"
            )

        # Aggregate claim integrity stats (also enforced in packet validator)
        claim_path = packet / "CLAIM_PLAN.yaml"
        if claim_path.exists():
            cdoc = load_yaml(claim_path) or {}
            for claim in cdoc.get("claims") or []:
                claim_status[claim.get("status")] += 1
                claim_class[claim.get("claim_class")] += 1
                if claim.get("status") == "SOURCE_IDENTIFIED":
                    keys = claim.get("citation_keys") or []
                    pe = claim.get("project_evidence")
                    if not keys and not isinstance(pe, dict):
                        invalid_source_identified += 1

    # Registry count blocks must match derived truth
    reported_current = doc.get("current_state_counts") or {}
    if dict(sorted(Counter(c.get("current_state") for c in chapters).items())) != dict(
        sorted(reported_current.items())
    ):
        errors.append("current_state_counts does not match chapter current_state values")

    reported_packet = doc.get("packet_state_counts") or {}
    if dict(sorted(Counter(c.get("packet_state") for c in chapters).items())) != dict(
        sorted(reported_packet.items())
    ):
        errors.append("packet_state_counts does not match chapter packet_state values")

    # WAIKE totals must match deterministic aggregation
    agg = aggregate_all_waike()
    reg_waike = doc.get("waike_mapping_totals") or {}
    for key in ("exact", "adjacent", "proposed", "no_map"):
        if int(reg_waike.get(key, -1)) != int(agg["totals"].get(key, 0)):
            errors.append(
                f"waike_mapping_totals.{key}={reg_waike.get(key)!r} "
                f"expected {agg['totals'].get(key)}"
            )

    report = REPORT.read_text(encoding="utf-8") if REPORT.exists() else ""
    if "GATE_3_IN_PROGRESS" not in report:
        errors.append("progress report must retain GATE_3_IN_PROGRESS")
    if "Gate 3 PASS" in report and "Never claim Gate 3 PASS" not in report:
        errors.append("progress report must not claim Gate 3 PASS")
    working_n = int((doc.get("counts") or {}).get("canonical_full_drafts") or 0)
    draft_needles = [
        f"{working_n}/31 WORKING_DRAFT_COMPLETE",
        f"{working_n}/31 canonical full drafts",
        f"WORKING_DRAFT_COMPLETE = {working_n}",
    ]
    if not any(n in report for n in draft_needles):
        errors.append(
            "progress report missing truthful working-draft coverage "
            f"(expected one of {draft_needles})"
        )
    for needle in (
        "31/31 architecture registered",
        "31/31 minimum packet coverage",
        "0/31 HUMAN_VALIDATED",
        "0/31 human-validated",
        "0/31 PUBLICATION_READY",
        "0/31 publication-ready",
        "architecture:",
        "packet:",
        "substantive_preproduction:",
        "working_draft:",
        "technical_review:",
        "human_validation:",
        "publication_readiness:",
    ):
        # Accept either legacy lowercase or UPPER maturity labels for 0/31 lines.
        if needle.startswith("0/31 ") and needle not in report:
            alt = needle.replace("HUMAN_VALIDATED", "human-validated").replace(
                "PUBLICATION_READY", "publication-ready"
            )
            alt2 = needle.replace("human-validated", "HUMAN_VALIDATED").replace(
                "publication-ready", "PUBLICATION_READY"
            )
            if alt not in report and alt2 not in report and needle not in report:
                # only error once per concept
                if "human" in needle.lower() and (
                    "0/31 HUMAN_VALIDATED" in report or "0/31 human-validated" in report
                ):
                    continue
                if "publication" in needle.lower() and (
                    "0/31 PUBLICATION_READY" in report or "0/31 publication-ready" in report
                ):
                    continue
                errors.append(f"progress report missing truthful coverage line: {needle}")
            continue
        if needle not in report and not needle.startswith("0/31 "):
            errors.append(f"progress report missing truthful coverage line: {needle}")

    if invalid_source_identified:
        errors.append(f"invalid SOURCE_IDENTIFIED-without-evidence count={invalid_source_identified}")

    if errors:
        print("validate_full31: FAIL")
        for e in errors:
            print(" -", e)
        return 1

    print("validate_full31: PASS")
    print(f" - chapters={len(chapters)}")
    print(f" - gate={gate}")
    print(f" - packet_states={dict(sorted(packet_states.items()))}")
    print(f" - current_states={dict(sorted(derived_states.items()))}")
    print(f" - claim_status={dict(sorted(claim_status.items()))}")
    print(f" - claim_class={dict(sorted(claim_class.items()))}")
    print(f" - waike_totals={agg['totals']}")
    print(f" - unique_upstream_waike_objects={agg['unique_upstream_waike_objects']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
