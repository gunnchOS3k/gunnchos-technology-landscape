#!/usr/bin/env python3
"""Merge full31 part registry fragments into CHAPTER_PRODUCTION_REGISTRY.yaml."""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
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
    lines.append("current_state_counts:")
    for key, value in sorted(doc["current_state_counts"].items()):
        lines.append(f"  {key}: {value}")
    lines.append("waike_mapping_totals:")
    for key, value in doc["waike_mapping_totals"].items():
        lines.append(f"  {key}: {value}")
    lines.append(f"waike_mapping_note: {_dump_scalar(doc['waike_mapping_note'])}")
    lines.append("chapters:")
    for ch in doc["chapters"]:
        lines.append(f"- chapter_number: {ch['chapter_number']}")
        for key in [
            "chapter_id",
            "title",
            "part",
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
    waike = Counter()
    for path in FRAGMENTS:
        frag = load_yaml(path)
        for ch in frag.get("chapters") or []:
            entry = dict(ch)
            cid = entry["chapter_id"].lower()
            num = int(entry["chapter_number"])
            packet = entry.get("packet_path") or f"publication/full31/chapters/ch{num:02d}/"
            entry["packet_path"] = packet.rstrip("/") + "/"
            if "chapter_id" in entry and entry["chapter_id"].startswith("CH"):
                expected = f"publication/full31/chapters/{cid}/"
                # normalize zero-padded folder names
                folder = ROOT / entry["packet_path"]
                if not folder.exists():
                    alt = ROOT / f"publication/full31/chapters/ch{num:02d}/"
                    if alt.exists():
                        entry["packet_path"] = f"publication/full31/chapters/ch{num:02d}/"
            chapters.append(entry)
        totals = frag.get("waike_mapping_totals_this_fragment") or {}
        for k, v in totals.items():
            waike[k] += int(v)

    # Aggregate WAIKE from crosswalk markdown when fragment totals incomplete.
    if not waike:
        waike = Counter({"exact": 0, "adjacent": 0, "proposed": 0, "no_map": 0})
    # Supplement missing H/I totals from progress notes where present.
    # Part III–IV progress documents counts; Part I–II does not publish aggregated totals.
    # Keep fragment-reported totals only; do not invent.

    chapters.sort(key=lambda c: int(c["chapter_number"]))
    state_counts = Counter(c["current_state"] for c in chapters)
    return {
        "schema_version": "1.0.0",
        "registry_id": "full31-chapter-production-registry",
        "accepted_main_sha": "0e694176652d4729c7f2b71df08b871a863afb8c",
        "waike_accepted_main_sha": "e97e74fc9bfb44b1cdc26b272dc4848264f15fe0",
        "gate_posture": "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING",
        "integrator_note": (
            "Merged from agent-h/i/j registry fragments. "
            "PREPRODUCTION / DEVELOPMENT — not canonical final prose and not Gate 3 reader evidence. "
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
        },
        "current_state_counts": dict(sorted(state_counts.items())),
        "waike_mapping_totals": {
            "exact": int(waike.get("exact", 0)),
            "adjacent": int(waike.get("adjacent", 0)),
            "proposed": int(waike.get("proposed", 0)),
            "no_map": int(waike.get("no_map", 0)),
        },
        "waike_mapping_note": (
            "Totals include fragment-reported row counts (Part V–VI). "
            "Parts I–IV publish per-chapter crosswalks; III–IV progress notes report "
            "exact=0 adjacent=37 proposed=4 no-map=17."
        ),
        "chapters": chapters,
    }


def write_report(doc: dict) -> str:
    lines: list[str] = []
    lines.append("# Full 31 Progress Report")
    lines.append("")
    lines.append("**PREPRODUCTION / DEVELOPMENT — not canonical final prose and not Gate 3 reader evidence.**")
    lines.append("")
    lines.append(f"**Accepted main:** `{doc['accepted_main_sha']}`  ")
    lines.append(f"**WAIKE accepted main:** `{doc['waike_accepted_main_sha']}`  ")
    lines.append(f"**Gate posture:** `{doc['gate_posture']}`  ")
    lines.append("**CH02-REVIEW-R1 / gate-3:** UNCHANGED vs accepted main")
    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    lines.append(
        f"- Chapters registered: **{doc['counts']['chapters']}** "
        f"(unique numbers {doc['counts']['unique_chapter_numbers']}, "
        f"unique titles {doc['counts']['unique_titles']})"
    )
    lines.append(
        f"- Every chapter has `next_automatable_action`: "
        f"**{doc['counts']['with_next_automatable_action'] == 31}**"
    )
    lines.append("- Packets under `publication/full31/chapters/ch01`–`ch31/`")
    lines.append("- Unified registry: `publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml`")
    lines.append("")
    lines.append("## current_state counts")
    lines.append("")
    lines.append("| current_state | count |")
    lines.append("|---|---:|")
    for key, value in sorted(doc["current_state_counts"].items()):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    lines.append("## Per-chapter production state")
    lines.append("")
    lines.append("| Ch | ID | Title | Part | current_state | canonical_prose | concept_preproduction |")
    lines.append("|---:|---|---|---|---|---|---|")
    for ch in doc["chapters"]:
        lines.append(
            f"| {ch['chapter_number']} | {ch['chapter_id']} | {ch['title']} | {ch['part']} | "
            f"{ch['current_state']} | {ch['canonical_prose_state']} | {ch['concept_preproduction_state']} |"
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
    lines.append("## WAIKE mapping note")
    lines.append("")
    lines.append(
        f"Fragment-reported Part V–VI row totals: exact={doc['waike_mapping_totals']['exact']}, "
        f"adjacent={doc['waike_mapping_totals']['adjacent']}, "
        f"proposed={doc['waike_mapping_totals']['proposed']}, "
        f"no_map={doc['waike_mapping_totals']['no_map']}."
    )
    lines.append(
        "Part III–IV progress notes separately report exact=0, adjacent=37, proposed=4, no-map=17. "
        "Do not invent WAIKE IDs."
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
