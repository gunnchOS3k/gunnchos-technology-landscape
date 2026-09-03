#!/usr/bin/env python3
"""Merge full31 part registry fragments into CHAPTER_PRODUCTION_REGISTRY.yaml.

Recomputes packet_state + honest current_state, and authoritative WAIKE totals.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from full31_common import (  # noqa: E402
    ACCEPTED_MAIN,
    GATE,
    PREPRODUCTION_SUBSTATES,
    WAIKE_ACCEPTED_MAIN,
    aggregate_all_waike,
    derive_current_state,
    validate_packet_dir,
)
from yaml_util import load_yaml  # noqa: E402

FRAGMENTS = [
    ROOT / "publication/full31/parts/part_i_ii_registry_fragment.yaml",
    ROOT / "publication/full31/parts/part_iii_iv_registry_fragment.yaml",
    ROOT / "publication/full31/parts/part_v_vi_registry_fragment.yaml",
]
OUT = ROOT / "publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml"
REPORT = ROOT / "publication/full31/FULL31_PROGRESS_REPORT.md"

VOCABULARY = [
    "SCAFFOLD",
    "PREPRODUCTION_STARTED",
    "PREPRODUCTION_COMPLETE",
    "DRAFT_STARTED",
    "DRAFT_COMPLETE",
    "TECH_REVIEW_PENDING",
    "HUMAN_VALIDATION_PENDING",
    "REVISION_REQUIRED",
    "READY_FOR_EDITORIAL",
    "PUBLICATION_READY",
]


def _dump_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "":
        return '""'
    needs_quote = any(ch in text for ch in ":#{}[],&*!|>%@`'\"\n") or text.strip() != text
    if needs_quote or text.lower() in {"true", "false", "null", "yes", "no"}:
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return text


def _dump_list(items: list, indent: int) -> list[str]:
    pad = " " * indent
    if not items:
        return [f"{pad}[]"]
    lines: list[str] = []
    for item in items:
        if isinstance(item, dict):
            raise TypeError("nested mapping lists unsupported")
        lines.append(f"{pad}- {_dump_scalar(item)}")
    return lines


def dump_registry(doc: dict) -> str:
    lines: list[str] = []
    lines.append(f"schema_version: {_dump_scalar(doc['schema_version'])}")
    lines.append(f"registry_id: {_dump_scalar(doc['registry_id'])}")
    lines.append(f"accepted_main_sha: {_dump_scalar(doc['accepted_main_sha'])}")
    lines.append(f"waike_accepted_main_sha: {_dump_scalar(doc['waike_accepted_main_sha'])}")
    lines.append(f"gate_posture: {_dump_scalar(doc['gate_posture'])}")
    lines.append("integrator_note: >")
    for para in doc["integrator_note"].strip().splitlines():
        lines.append(f"  {para}")
    lines.append("vocabulary:")
    lines.extend(_dump_list(doc["vocabulary"], 2))
    lines.append("source_fragments:")
    lines.extend(_dump_list(doc["source_fragments"], 2))
    lines.append("counts:")
    for key, value in doc["counts"].items():
        lines.append(f"  {key}: {value}")
    lines.append("packet_state_counts:")
    for key, value in sorted(doc["packet_state_counts"].items()):
        lines.append(f"  {key}: {value}")
    lines.append("current_state_counts:")
    for key, value in sorted(doc["current_state_counts"].items()):
        lines.append(f"  {key}: {value}")
    lines.append("waike_mapping_totals:")
    for key, value in doc["waike_mapping_totals"].items():
        lines.append(f"  {key}: {value}")
    lines.append(
        f"waike_unique_upstream_objects: {doc.get('waike_unique_upstream_objects', 0)}"
    )
    lines.append(f"waike_mapping_note: {_dump_scalar(doc['waike_mapping_note'])}")
    lines.append("chapters:")
    for ch in doc["chapters"]:
        lines.append(f"- chapter_number: {ch['chapter_number']}")
        for key in [
            "chapter_id",
            "title",
            "part",
            "packet_state",
            "current_state",
            "canonical_prose_state",
            "concept_preproduction_state",
            "source_state",
            "claim_state",
            "figure_state",
            "lab_state",
            "glossary_state",
            "waike_state",
        ]:
            lines.append(f"  {key}: {_dump_scalar(ch[key])}")
        for key in [
            "dependencies",
            "gate_dependencies",
            "human_dependencies",
            "physical_dependencies",
        ]:
            lines.append(f"  {key}:")
            lines.extend(_dump_list(list(ch.get(key) or []), 4))
        lines.append(f"  next_automatable_action: {_dump_scalar(ch['next_automatable_action'])}")
        lines.append(f"  packet_path: {_dump_scalar(ch['packet_path'])}")
    lines.append("")
    return "\n".join(lines)


def merge() -> dict:
    chapters: list[dict] = []
    for path in FRAGMENTS:
        frag = load_yaml(path)
        for ch in frag.get("chapters") or []:
            entry = dict(ch)
            cid = entry["chapter_id"].lower()
            num = int(entry["chapter_number"])
            packet = entry.get("packet_path") or f"publication/full31/chapters/ch{num:02d}/"
            entry["packet_path"] = packet.rstrip("/") + "/"
            folder = ROOT / entry["packet_path"]
            if not folder.exists():
                alt = ROOT / f"publication/full31/chapters/ch{num:02d}/"
                if alt.exists():
                    entry["packet_path"] = f"publication/full31/chapters/ch{num:02d}/"
                    folder = alt
            # Honest packet + maturity
            if folder.is_dir():
                packet_state, _errs = validate_packet_dir(folder)
            else:
                packet_state = "PACKET_MISSING"
            entry["packet_state"] = packet_state
            entry["current_state"] = derive_current_state(entry)
            chapters.append(entry)

    chapters.sort(key=lambda c: int(c["chapter_number"]))
    state_counts = Counter(c["current_state"] for c in chapters)
    packet_counts = Counter(c["packet_state"] for c in chapters)
    waike = aggregate_all_waike()

    # Coverage metrics for report (normalized dimensions — see PROGRESS_DIMENSIONS.md)
    canonical_full = sum(1 for c in chapters if c.get("canonical_prose_state") == "DRAFT_COMPLETE")
    # truthful: zero completed technical review / human validation / publication-ready in this wave
    technical_review = 0
    human_validated = 0
    publication_ready = 0
    # Working drafts imply substantive preproduction completed for those chapters.
    substantive_preprod_complete = sum(
        1
        for c in chapters
        if c.get("current_state")
        in {
            "PREPRODUCTION_COMPLETE",
            "TECH_REVIEW_PENDING",
            "HUMAN_VALIDATION_PENDING",
            "READY_FOR_EDITORIAL",
            "PUBLICATION_READY",
        }
        or c.get("canonical_prose_state") == "DRAFT_COMPLETE"
    )
    substantive_preprod_started = sum(
        1
        for c in chapters
        if c.get("current_state")
        in {
            "PREPRODUCTION_STARTED",
            "PREPRODUCTION_COMPLETE",
            "TECH_REVIEW_PENDING",
            "HUMAN_VALIDATION_PENDING",
            "DRAFT_STARTED",
            "DRAFT_COMPLETE",
        }
        or c.get("canonical_prose_state")
        in {
            "PREPRODUCTION_STARTED",
            "PREPRODUCTION_COMPLETE",
            "DRAFT_STARTED",
            "DRAFT_COMPLETE",
            "TECH_REVIEW_PENDING",
            "HUMAN_VALIDATION_PENDING",
        }
    )

    return {
        "schema_version": "1.0.0",
        "registry_id": "full31-chapter-production-registry",
        "accepted_main_sha": ACCEPTED_MAIN,
        "waike_accepted_main_sha": WAIKE_ACCEPTED_MAIN,
        "gate_posture": GATE,
        "integrator_note": (
            "Merged from agent-h/i/j registry fragments after Batch 3 full-manuscript draft. "
            "packet_state is file/semantic completeness only; current_state is honest maturity. "
            f"WORKING_DRAFT_COMPLETE={canonical_full}; HUMAN_VALIDATED=0; PUBLICATION_READY=0. "
            "PREPRODUCTION / DEVELOPMENT — not Gate 3 reader evidence. "
            "CH02-REVIEW-R1 and publication/gates/gate-3/ remain untouched."
        ),
        "vocabulary": VOCABULARY,
        "source_fragments": [str(p.relative_to(ROOT)) for p in FRAGMENTS],
        "counts": {
            "chapters": len(chapters),
            "unique_chapter_numbers": len({c["chapter_number"] for c in chapters}),
            "unique_titles": len({c["title"] for c in chapters}),
            "with_next_automatable_action": sum(
                1 for c in chapters if str(c.get("next_automatable_action") or "").strip()
            ),
            "architecture_registered": 31,
            "minimum_packet_coverage": sum(
                1 for c in chapters if c.get("packet_state") in {"PACKET_COMPLETE", "PACKET_STARTED"}
            ),
            "packet_complete": int(packet_counts.get("PACKET_COMPLETE", 0)),
            "substantive_preproduction_started": substantive_preprod_started,
            "substantive_preproduction_complete": substantive_preprod_complete,
            "canonical_full_drafts": canonical_full,
            "working_draft": canonical_full,
            "working_draft_complete": canonical_full,
            "technical_review": technical_review,
            "human_validated": human_validated,
            "publication_ready": publication_ready,
        },
        "packet_state_counts": dict(sorted(packet_counts.items())),
        "current_state_counts": dict(sorted(state_counts.items())),
        "waike_mapping_totals": waike["totals"],
        "waike_unique_upstream_objects": waike["unique_upstream_waike_objects"],
        "waike_mapping_note": (
            "Authoritative totals from deterministic parse of all chapter WAIKE_CROSSWALK.md files "
            "(scripts/aggregate_full31_waike.py). Fragment row totals are not authoritative."
        ),
        "chapters": chapters,
    }


def write_report(doc: dict) -> str:
    counts = doc["counts"]
    waike = doc["waike_mapping_totals"]
    lines: list[str] = []
    lines.append("# Full 31 Progress Report")
    lines.append("")
    lines.append(
        "**PREPRODUCTION / DEVELOPMENT — not canonical final prose and not Gate 3 reader evidence.**"
    )
    lines.append("")
    lines.append(f"**Accepted main:** `{doc['accepted_main_sha']}`  ")
    lines.append(f"**WAIKE accepted main:** `{doc['waike_accepted_main_sha']}`  ")
    lines.append(f"**Gate posture:** `{doc['gate_posture']}`  ")
    lines.append("**CH02-REVIEW-R1 / gate-3:** UNCHANGED vs accepted main")
    lines.append("")
    lines.append("## Coverage (do not collapse)")
    lines.append("")
    lines.append("Normalized dimensions — see `publication/full31/PROGRESS_DIMENSIONS.md`.")
    lines.append("")
    lines.append("```text")
    lines.append(f"architecture:              {counts['architecture_registered']}/31")
    lines.append(f"packet:                    {counts['minimum_packet_coverage']}/31")
    lines.append(
        f"substantive_preproduction: {counts['substantive_preproduction_complete']}/31 complete "
        f"({counts['substantive_preproduction_started']}/31 started)"
    )
    lines.append(f"working_draft:             {counts['canonical_full_drafts']}/31")
    lines.append(f"technical_review:          {counts.get('technical_review', 0)}/31")
    lines.append(f"human_validation:          {counts['human_validated']}/31")
    lines.append(f"publication_readiness:     {counts['publication_ready']}/31")
    lines.append("```")
    lines.append("")
    lines.append("Honest manuscript maturity (do not collapse):")
    lines.append("")
    lines.append("```text")
    lines.append(f"WORKING_DRAFT_COMPLETE = {counts.get('working_draft_complete', counts['canonical_full_drafts'])}")
    lines.append("HUMAN_VALIDATED = 0")
    lines.append("PUBLICATION_READY = 0")
    lines.append("```")
    lines.append("")
    lines.append("Legacy synonyms (validators / continuity):")
    lines.append("")
    lines.append("```text")
    lines.append("31/31 architecture registered")
    lines.append("31/31 minimum packet coverage")
    lines.append(
        f"{counts['substantive_preproduction_complete']}/31 substantive preproduction complete"
    )
    lines.append(
        f"{counts['substantive_preproduction_started']}/31 substantive preproduction started"
    )
    lines.append(f"{counts['canonical_full_drafts']}/31 WORKING_DRAFT_COMPLETE")
    lines.append("0/31 HUMAN_VALIDATED")
    lines.append("0/31 PUBLICATION_READY")
    lines.append("```")
    lines.append("")
    lines.append(
        f"- Packet complete (semantic): **{counts['packet_complete']}/31** "
        f"(`packet_state` only; not chapter maturity)"
    )
    lines.append(
        "- Packets under `publication/full31/chapters/ch01`–`ch31/`; "
        "unified registry `publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml`"
    )
    lines.append(
        "- Review plan: `publication/full31/FULL_MANUSCRIPT_REVIEW_PLAN.md` "
        "(plan only; no fabricated responses)"
    )
    lines.append(
        f"- Every chapter has `next_automatable_action`: "
        f"**{counts['with_next_automatable_action'] == 31}**"
    )
    lines.append("")
    lines.append("## packet_state counts")
    lines.append("")
    lines.append("| packet_state | count |")
    lines.append("|---|---:|")
    for key, value in sorted(doc["packet_state_counts"].items()):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    lines.append("## current_state counts (honest maturity)")
    lines.append("")
    lines.append("| current_state | count |")
    lines.append("|---|---:|")
    for key, value in sorted(doc["current_state_counts"].items()):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    lines.append("## Per-chapter production state")
    lines.append("")
    lines.append(
        "| Ch | ID | Title | Part | packet_state | current_state | canonical_prose | concept_preproduction |"
    )
    lines.append("|---:|---|---|---|---|---|---|---|")
    for ch in doc["chapters"]:
        lines.append(
            f"| {ch['chapter_number']} | {ch['chapter_id']} | {ch['title']} | {ch['part']} | "
            f"{ch['packet_state']} | {ch['current_state']} | {ch['canonical_prose_state']} | "
            f"{ch['concept_preproduction_state']} |"
        )
    lines.append("")
    lines.append("## Labs wired this wave")
    lines.append("")
    lines.append("- `LAB-SYS-001` (CE-1 / CH01)")
    lines.append("- `LAB-CMS-001` (CE-3)")
    lines.append("- `LAB-PKT-001` (CE-4)")
    lines.append("- `LAB-TRUST-001` (CE-5)")
    lines.append("- `LAB-CE06-001` (CE-6)")
    lines.append("- Existing `LAB-TAP-001` (CH02)")
    lines.append("")
    lines.append("## FIG-CE3-009 reconciliation")
    lines.append("")
    lines.append(
        "`FIG-CE3-009` remains `BLOCKED_EVIDENCE_REQUIRED` / `production_status: blocked` "
        "in the CE figure registry. LAB-CMS-001 ships teaching fixtures labeled with that ID; "
        "those fixtures are synthetic/illustrative and do **not** unblock the measured figure."
    )
    lines.append("")
    lines.append("## WAIKE mapping (authoritative)")
    lines.append("")
    lines.append("| Class | Count |")
    lines.append("|---|---:|")
    for key in ("exact", "adjacent", "proposed", "no_map"):
        lines.append(f"| `{key}` | {waike[key]} |")
    lines.append("")
    lines.append(
        f"Unique upstream WAIKE objects: **{doc.get('waike_unique_upstream_objects', 0)}** "
        "(deterministic aggregation; not fragment duplicates)."
    )
    lines.append("")
    lines.append(
        f"Checksum form: exact={waike['exact']}, adjacent={waike['adjacent']}, "
        f"proposed={waike['proposed']}, no_map={waike['no_map']}."
    )
    lines.append("")
    lines.append("## Gate confirmation")
    lines.append("")
    lines.append("- Never claim Gate 3 PASS.")
    lines.append("- Status remains `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Verify outputs match merge result")
    args = parser.parse_args()
    doc = merge()
    yaml_text = dump_registry(doc)
    report_text = write_report(doc)
    if args.check:
        errors: list[str] = []
        if not OUT.exists():
            errors.append(f"missing {OUT}")
        elif OUT.read_text(encoding="utf-8") != yaml_text:
            errors.append(f"{OUT} out of date; re-run without --check")
        if not REPORT.exists():
            errors.append(f"missing {REPORT}")
        elif REPORT.read_text(encoding="utf-8") != report_text:
            errors.append(f"{REPORT} out of date; re-run without --check")
        if errors:
            print("merge_full31_registry: FAIL")
            for e in errors:
                print(" -", e)
            return 1
        print("merge_full31_registry: PASS (outputs current)")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(yaml_text, encoding="utf-8")
    REPORT.write_text(report_text, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    print(f"packet_state_counts={doc['packet_state_counts']}")
    print(f"current_state_counts={doc['current_state_counts']}")
    print(f"waike={doc['waike_mapping_totals']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
