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
from collections import defaultdict
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


def parse_bib(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    entries: list[dict[str, str]] = []
    for match in re.finditer(
        r"@(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\}",
        text,
        flags=re.S,
    ):
        entry_type, key, body = match.group(1), match.group(2).strip(), match.group(3)
        fields: dict[str, str] = {"entry_type": entry_type, "key": key}
        for fm in re.finditer(r"(\w+)\s*=\s*\{([^{}]*)\}", body):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        entries.append(fields)
    return entries


def classify_bib(entry: dict[str, str]) -> str:
    et = entry.get("entry_type", "").lower()
    how = (entry.get("howpublished") or "").lower()
    note = (entry.get("note") or "").lower()
    title = (entry.get("title") or "").lower()
    if et == "book":
        return "textbooks"
    if "rfc" in how or how.startswith("ietf") or "3gpp" in how or "nist" in how or "iso" in how or "w3c" in how:
        return "standards_specifications"
    if "rfc" in key_safe(entry) or "nist" in key_safe(entry) or "iso" in key_safe(entry):
        return "standards_specifications"
    if "doi" in note or "ieee" in how or "journal" in how or et in {"article"}:
        return "peer_reviewed"
    if "github.com" in (entry.get("url") or "") or "accepted" in note or "repository" in how:
        return "project_accepted_main"
    if "kernel.org" in (entry.get("url") or "") or "docs." in (entry.get("url") or "") or "living" in how:
        return "official_technical_documentation"
    if et == "misc" and ("mdn" in title or "documentation" in how or "standard" in how):
        return "official_technical_documentation"
    return "other_explanatory"


def key_safe(entry: dict[str, str]) -> str:
    return entry.get("key", "").lower()


def build_indexes() -> dict[str, dict[str, Any]]:
    claims: list[dict] = []
    figures: list[dict] = []
    glossary: list[dict] = []
    labs: list[dict] = []
    sources: list[dict] = []
    waike: list[dict] = []
    source_occurrences = 0
    unique_keys: dict[str, dict] = {}
    conflicts: list[str] = []

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

        bib_path = d / "references.local.bib"
        for entry in parse_bib(bib_path):
            source_occurrences += 1
            cls = classify_bib(entry)
            rec = {
                "source_package": ce,
                "bib_key": entry["key"],
                "entry_type": entry.get("entry_type"),
                "title": entry.get("title"),
                "year": entry.get("year"),
                "url": entry.get("url"),
                "source_class": cls,
                "verification_status": (
                    "REPOSITORY_EVIDENCE_VERIFIED"
                    if cls == "project_accepted_main"
                    else "PRIMARY_METADATA_VERIFIED"
                    if entry.get("url") or entry.get("year")
                    else "NEEDS_PRIMARY_VERIFICATION"
                ),
            }
            sources.append(rec)
            k = entry["key"].lower()
            if k in unique_keys:
                prev = unique_keys[k]
                for field in ("title", "year", "url"):
                    a, b = (prev.get(field) or "").strip(), (entry.get(field) or "").strip()
                    if a and b and a.lower() != b.lower():
                        conflicts.append(f"{entry['key']}: conflicting {field}: {a!r} vs {b!r}")
            else:
                unique_keys[k] = entry

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

    class_counts: dict[str, int] = defaultdict(int)
    for e in unique_keys.values():
        class_counts[classify_bib(e)] += 1

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

    source_index = header()
    source_index["chapter_source_occurrences"] = source_occurrences
    source_index["unique_source_records"] = len(unique_keys)
    source_index["unique_by_class"] = dict(sorted(class_counts.items()))
    source_index["metadata_conflicts"] = conflicts
    source_index["sources"] = sources

    waike_index = header()
    waike_index["packages"] = waike

    return {
        "CANDIDATE_CLAIM_INDEX.yaml": claim_index,
        "CANDIDATE_FIGURE_INDEX.yaml": figure_index,
        "CANDIDATE_GLOSSARY.yaml": glossary_index,
        "CANDIDATE_LAB_INDEX.yaml": lab_index,
        "CANDIDATE_SOURCE_INDEX.yaml": source_index,
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
