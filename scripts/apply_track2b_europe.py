#!/usr/bin/env python3
"""Apply Track 2B Europe research onto existing atlas artifacts (preserves 2A/2C)."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml

from kids_standards_europe_research import (
    EUROPE_COVERAGE_GAPS,
    EUROPE_NATIONAL_OVERRIDES,
    EUROPE_REGIONAL_PRIORITY_NOTE,
    apply_framework_patches,
    europe_extra_frameworks,
    europe_framework_patches,
    europe_mappings,
    europe_transnational_rows,
    germany_lander_rows,
    merge_mappings,
    uk_nation_row_updates,
)

ROOT = Path(__file__).resolve().parents[1]
STANDARDS = ROOT / "kids" / "standards"
REVIEWED = "2026-09-03"


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a mapping")
    return data


def dump_yaml(path: Path, data: object) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True,
            width=100,
            default_flow_style=False,
        )


def region_counts(jurisdictions: list[dict], region: str) -> Counter:
    return Counter(
        j["research_status"]
        for j in jurisdictions
        if j.get("region") == region
    )


def patch_jurisdictions(jur: dict) -> tuple[Counter, Counter]:
    rows: list[dict] = jur["jurisdictions"]
    before = region_counts(rows, "europe")
    by_id = {j["jurisdiction_id"]: j for j in rows}

    # National Europe overrides
    for iso, ov in EUROPE_NATIONAL_OVERRIDES.items():
        jid = f"JUR-{iso}"
        if jid not in by_id:
            continue
        row = by_id[jid]
        row["research_status"] = ov["research_status"]
        row["education_authority"] = ov["education_authority"]
        row["framework_ids"] = list(ov.get("framework_ids") or [])
        row["notes"] = ov.get("notes") or ""
        row["last_reviewed_on"] = REVIEWED

    # UK nations
    for jid, upd in uk_nation_row_updates().items():
        if jid in by_id:
            by_id[jid].update(upd)
            by_id[jid]["last_reviewed_on"] = REVIEWED

    # Transnationals EU / IB
    for tr in europe_transnational_rows():
        jid = tr["jurisdiction_id"]
        if jid in by_id:
            by_id[jid].update(tr)
        else:
            rows.append(tr)
            by_id[jid] = tr

    # Germany Länder
    for land in germany_lander_rows():
        jid = land["jurisdiction_id"]
        if jid in by_id:
            by_id[jid].update(land)
        else:
            rows.append(land)
            by_id[jid] = land

    jur["jurisdictions"] = rows
    jur["counts"] = {
        "total": len(rows),
        "by_status": dict(Counter(j["research_status"] for j in rows)),
        "by_level": dict(Counter(j["level"] for j in rows)),
        "by_region": dict(Counter(j["region"] for j in rows)),
    }
    after = region_counts(rows, "europe")
    return before, after


def patch_sources(src: dict) -> None:
    frameworks = list(src.get("frameworks") or [])
    # Use apply_framework_patches which also appends extras, but only patch known + add missing
    patched = apply_framework_patches(frameworks)
    # Dedup by id preserving order
    seen = set()
    out = []
    for fw in patched:
        fid = fw["framework_id"]
        if fid in seen:
            continue
        seen.add(fid)
        out.append(fw)
    src["frameworks"] = out
    src["framework_count"] = len(out)
    src["mandatory_baseline_count"] = sum(1 for s in out if s.get("mandatory_baseline"))
    src["generated_on"] = REVIEWED


def patch_atlas(atlas: dict) -> None:
    maps = list(atlas.get("mappings") or [])
    atlas["mappings"] = merge_mappings(maps)
    atlas["mapping_counts_by_fidelity"] = dict(
        Counter(m["fidelity"] for m in atlas["mappings"])
    )
    atlas["generated_on"] = REVIEWED


def write_regional_europe(jurisdictions: list[dict]) -> None:
    rows = []
    for j in jurisdictions:
        if j.get("region") != "europe":
            continue
        if j.get("level") in {"transnational", "institutional"}:
            continue
        rows.append(
            {
                "jurisdiction_id": j["jurisdiction_id"],
                "name": j["name"],
                "level": j["level"],
                "research_status": j["research_status"],
                "framework_ids": j.get("framework_ids") or [],
            }
        )
    dump_yaml(
        STANDARDS / "regional" / "europe.yaml",
        {
            "schema": "kids.standards.regional/v1",
            "region": "europe",
            "generated_on": REVIEWED,
            "track_status": "DRAFT_INTERNAL",
            "jurisdiction_count": len(rows),
            "status_counts": dict(Counter(r["research_status"] for r in rows)),
            "priority_notes": EUROPE_REGIONAL_PRIORITY_NOTE,
            "jurisdictions": rows,
        },
    )


def write_coverage(jur: dict, src: dict, atlas: dict, before: Counter, after: Counter) -> None:
    jurisdictions = jur["jurisdictions"]
    sources = src["frameworks"]
    maps = atlas["mappings"]
    j_counts = Counter(j["research_status"] for j in jurisdictions)
    m_counts = Counter(m["fidelity"] for m in maps)
    mandatory = [s for s in sources if s.get("mandatory_baseline")]

    def fmt(c: Counter) -> str:
        return ", ".join(f"{k}={v}" for k, v in sorted(c.items()))

    lines = [
        "# Global Standards Coverage Report",
        "",
        f"**Generated:** {REVIEWED}  ",
        "**Track status:** `DRAFT_INTERNAL` (not PUBLICATION_READY)  ",
        "**Schema:** `kids/standards/STANDARD_MAPPING_SCHEMA.md`  ",
        "**Track 2B:** Europe exhaustive research (PR #7) — preserves Tracks 2A/2C artifacts  ",
        f"**Integration tip at apply:** `origin/cursor/publication-family-parallel-production-001`  ",
        f"**Accepted main:** `82284cd8f41d750ff508cd6ea5bad0a9534d8162`",
        "",
        "## Jurisdiction metrics",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Jurisdictions total | {len(jurisdictions)} |",
        f"| OFFICIAL_VERIFIED | {j_counts.get('OFFICIAL_VERIFIED', 0)} |",
        f"| OFFICIAL_SOURCE_VERIFIED | {j_counts.get('OFFICIAL_SOURCE_VERIFIED', 0)} |",
        f"| OFFICIAL_PORTAL_IDENTIFIED | {j_counts.get('OFFICIAL_PORTAL_IDENTIFIED', 0)} |",
        f"| IDENTIFIED | {j_counts.get('IDENTIFIED', 0)} |",
        f"| TRANSLATION_REQUIRED | {j_counts.get('TRANSLATION_REQUIRED', 0)} |",
        f"| ACCESS_BLOCKED | {j_counts.get('ACCESS_BLOCKED', 0)} |",
        f"| NOT_YET_RESEARCHED | {j_counts.get('NOT_YET_RESEARCHED', 0)} |",
        f"| SOURCE_VERSION_UNCLEAR | {j_counts.get('SOURCE_VERSION_UNCLEAR', 0)} |",
        f"| NO_CENTRAL_NATIONAL_CURRICULUM | {j_counts.get('NO_CENTRAL_NATIONAL_CURRICULUM', 0)} |",
        "",
        "## Track 2B Europe before → after",
        "",
        "| Region | Before | After |",
        "| --- | --- | --- |",
        f"| europe | {fmt(before)} | {fmt(after)} |",
        "",
        "## Mapping metrics",
        "",
        "| Fidelity | Count |",
        "| --- | ---: |",
        f"| EXACT | {m_counts.get('EXACT', 0)} |",
        f"| ADJACENT | {m_counts.get('ADJACENT', 0)} |",
        f"| PROPOSED | {m_counts.get('PROPOSED', 0)} |",
        f"| NO_MAP | {m_counts.get('NO_MAP', 0)} |",
        f"| NOT_YET_MAPPED | {m_counts.get('NOT_YET_MAPPED', 0)} |",
        f"| **Mappings total** | **{len(maps)}** |",
        "",
        "## Mandatory framework baseline status",
        "",
        "| Framework | Authority | Version | Verification | URL | Gaps |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for s in mandatory:
        gaps = "; ".join(s.get("gaps") or []) or "—"
        lines.append(
            f"| {s['title']} | {s['authority']} | {s.get('version')} | `{s.get('verification')}` | {s.get('url')} | {gaps} |"
        )
    lines.extend(
        [
            "",
            "## Honest gaps (priority)",
            "",
            *EUROPE_COVERAGE_GAPS,
            "",
            "## Non-claims",
            "",
            "- Crosswalks are `CROSSWALKED_AGAINST` / `MAPPED_TO` / `INFORMED_BY` — **not** official alignment or certification.",
            "- Presence of a jurisdiction row ≠ completed clause-level mapping.",
            "- This track does not advance Gate 3 or PUBLICATION_READY counts.",
            "",
        ]
    )
    (STANDARDS / "GLOBAL_STANDARDS_COVERAGE_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    jur = load_yaml(STANDARDS / "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml")
    src = load_yaml(STANDARDS / "GLOBAL_STANDARDS_SOURCE_REGISTER.yaml")
    atlas = load_yaml(STANDARDS / "GLOBAL_STANDARDS_ATLAS.yaml")

    before, after = patch_jurisdictions(jur)
    patch_sources(src)
    patch_atlas(atlas)
    write_regional_europe(jur["jurisdictions"])
    write_coverage(jur, src, atlas, before, after)

    dump_yaml(STANDARDS / "GLOBAL_STANDARDS_JURISDICTION_REGISTRY.yaml", jur)
    dump_yaml(STANDARDS / "GLOBAL_STANDARDS_SOURCE_REGISTER.yaml", src)
    dump_yaml(STANDARDS / "GLOBAL_STANDARDS_ATLAS.yaml", atlas)

    print("=== Track 2B Europe BEFORE ===", dict(before))
    print("=== Track 2B Europe AFTER ===", dict(after))
    leftover = [
        j
        for j in jur["jurisdictions"]
        if j.get("region") == "europe" and j.get("research_status") == "NOT_YET_RESEARCHED"
    ]
    print(f"Remaining NOT_YET Europe: {len(leftover)}")
    for j in leftover:
        print(f"  {j['jurisdiction_id']} {j['name']}")
    print("Frameworks:", src["framework_count"], "Mappings:", len(atlas["mappings"]))


if __name__ == "__main__":
    main()
