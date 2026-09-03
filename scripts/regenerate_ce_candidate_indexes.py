#!/usr/bin/env python3
"""Deterministically regenerate publication/preproduction/CANDIDATE_*.yaml indexes.

Usage:
  python scripts/regenerate_ce_candidate_indexes.py
  python scripts/regenerate_ce_candidate_indexes.py --check   # fail if would change files
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

PREPROD = ROOT / "publication" / "preproduction"
CE_DIRS = ("ce-01", "ce-03", "ce-04", "ce-05", "ce-06")
SCHEMA_VERSION = "1.0.0"
GATE_NOTE = "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING"
STATUS = "CANDIDATE_PREPRODUCTION"

INDEX_FILES = (
    "CANDIDATE_CLAIM_INDEX.yaml",
    "CANDIDATE_FIGURE_INDEX.yaml",
    "CANDIDATE_GLOSSARY.yaml",
    "CANDIDATE_LAB_INDEX.yaml",
    "CANDIDATE_SOURCE_INDEX.yaml",
    "CANDIDATE_WAIKE_CROSSWALK.yaml",
)


def header() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "gate_note": GATE_NOTE,
        "rights": "Candidate only. Does not modify live CH02 / Gate 3 evidence registries.",
    }


def build_indexes() -> dict[str, Any]:
    claims: list[dict] = []
    figures: list[dict] = []
    glossary: list[dict] = []
    labs: list[dict] = []
    waike: list[dict] = []

    for ce in CE_DIRS:
        d = PREPROD / ce
        claim_data = load_yaml(d / "CLAIM_PLAN.yaml")
        for c in claim_data.get("claims") or []:
            claims.append(
                {
                    "source_package": ce,
                    "provisional_id": c["provisional_id"],
                    "status": c["status"],
                    "claim_class": c["claim_class"],
                    "text": c["text"],
                }
            )
        fig_data = load_yaml(d / "FIGURE_PLAN.yaml")
        for f in fig_data.get("figures") or []:
            figures.append(
                {
                    "source_package": ce,
                    "provisional_id": f["provisional_id"],
                    "truth_classification": f["truth_classification"],
                    "qualification": f.get("qualification"),
                    "figure_type": f["figure_type"],
                    "edition_scope": f["edition_scope"],
                }
            )
        concept_data = load_yaml(d / "CONCEPT_GRAPH.yaml")
        for n in concept_data.get("concepts") or []:
            if n.get("glossary_candidate"):
                glossary.append(
                    {
                        "source_package": ce,
                        "concept_id": n["concept_id"],
                        "canonical_term": n["canonical_term"],
                        "plain_language_definition": n["plain_language_definition"],
                    }
                )

        lab_text = (d / "LAB_PLAN.md").read_text(encoding="utf-8")
        lab_ids = sorted(set(re.findall(r"LAB-[A-Z0-9-]+", lab_text)))
        for lid in lab_ids:
            labs.append({"source_package": ce, "lab_id": lid})

        wx = (d / "WAIKE_CROSSWALK.md").read_text(encoding="utf-8")
        sha_m = re.search(r"\b([0-9a-f]{40})\b", wx)
        waike.append(
            {
                "source_package": ce,
                "waike_accepted_main_sha": sha_m.group(1) if sha_m else None,
                "relationship_vocabulary": ["exact", "adjacent", "proposed", "no-map"],
                "mentions_exact": bool(re.search(r"\bexact\b", wx, re.I)),
                "mentions_adjacent": bool(re.search(r"\badjacent\b", wx, re.I)),
                "mentions_proposed": bool(re.search(r"\bproposed\b", wx, re.I)),
                "mentions_no_map": bool(re.search(r"\bno-map\b", wx, re.I)),
            }
        )

    # Source index owned by Agent G verification tooling (raw YAML text; avoid round-trip drift).
    from validate_ce_sources import audit, load_all_occurrences, write_source_index  # noqa: E402

    src_rows = load_all_occurrences()
    source_index_text = write_source_index(src_rows, audit(src_rows))

    claim_index = header()
    claim_index["claims"] = claims
    claim_index["counts_by_status"] = dict(
        sorted(
            {
                s: sum(1 for c in claims if c["status"] == s)
                for s in sorted({c["status"] for c in claims})
            }.items()
        )
    )

    figure_index = header()
    figure_index["figures"] = figures
    figure_index["counts_by_truth_classification"] = dict(
        sorted(
            {
                t: sum(1 for f in figures if f["truth_classification"] == t)
                for t in sorted({f["truth_classification"] for f in figures})
            }.items()
        )
    )

    glossary_index = header()
    glossary_index["entries"] = glossary
    glossary_index["n_entries"] = len(glossary)

    lab_index = header()
    lab_index["labs"] = labs

    waike_index = header()
    waike_index["packages"] = waike

    return {
        "CANDIDATE_CLAIM_INDEX.yaml": claim_index,
        "CANDIDATE_FIGURE_INDEX.yaml": figure_index,
        "CANDIDATE_GLOSSARY.yaml": glossary_index,
        "CANDIDATE_LAB_INDEX.yaml": lab_index,
        "CANDIDATE_SOURCE_INDEX.yaml": source_index_text,
        "CANDIDATE_WAIKE_CROSSWALK.yaml": waike_index,
    }


def file_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if regenerate would change files")
    args = parser.parse_args(argv)

    indexes = build_indexes()
    changed = []
    for name, data in indexes.items():
        path = PREPROD / name
        if isinstance(data, str):
            new_text = data if data.endswith("\n") else data + "\n"
        else:
            new_text = dump_yaml(data)
            if not new_text.endswith("\n"):
                new_text += "\n"
        old_text = path.read_text(encoding="utf-8") if path.exists() else ""
        if file_digest(old_text) != file_digest(new_text):
            changed.append(name)
            if not args.check:
                path.write_text(new_text, encoding="utf-8")
    if args.check:
        if changed:
            print("regenerate_ce_candidate_indexes: FAIL — would change:")
            for n in changed:
                print(" -", n)
            return 1
        print("regenerate_ce_candidate_indexes: PASS (no diff)")
        return 0
    print("regenerate_ce_candidate_indexes: wrote", ", ".join(INDEX_FILES))
    if changed:
        print("updated:", ", ".join(changed))
    else:
        print("already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
