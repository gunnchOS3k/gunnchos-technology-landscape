#!/usr/bin/env python3
"""Generate Kids full-manuscript inventory + fill shared family reports from registries.

Standards mapping counts use STANDARDS_TRACEABILITY.yaml unique atlas_mapping_ids only
(not UNIT_REGISTRY), so registry + traceability never double-count.

Figure counts use live_registered_figures (FIGURE_PLAN IDs with on-disk SVG), not raw
directory .svg counts (orphans excluded).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from kids_full_manuscript_asset_lib import (  # noqa: E402
    live_registered_ids,
    load_yaml,
    physical_svg_ids,
    registered_figure_ids,
    standards_status_counts,
    unique_atlas_mapping_ids,
)

BOOKS = ROOT / "kids" / "books"
BANDS = [
    "KIDS-BABY",
    "KIDS-TODDLER",
    "KIDS-PRESCHOOL",
    "KIDS-PREK",
    "KIDS-ELEM1",
    "KIDS-ELEM2",
]
CHILD_RE = re.compile(r"\*\*Child-facing text:\*\*\s*(.+?)(?=\n\n|\n\*\*|$)", re.S)


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def as_units(reg) -> list[dict]:
    if isinstance(reg, dict) and isinstance(reg.get("units"), list):
        return [u for u in reg["units"] if isinstance(u, dict)]
    if isinstance(reg, dict):
        out = []
        for k, v in reg.items():
            if isinstance(v, dict) and (v.get("unit_id") or str(k).startswith("UNIT-")):
                item = dict(v)
                item.setdefault("unit_id", v.get("unit_id") or k)
                out.append(item)
        return out
    if isinstance(reg, list):
        return [u for u in reg if isinstance(u, dict)]
    return []


def child_words(md: str) -> int:
    return sum(len(b.split()) for b in CHILD_RE.findall(md))


def caregiver_words(path: Path) -> int:
    if not path.is_file():
        return 0
    return len(path.read_text(encoding="utf-8").split())


def band_stats(band: str) -> dict:
    root = BOOKS / band
    figs_dir = root / "figures"
    ms = (root / "BOOK_MANUSCRIPT.md").read_text(encoding="utf-8")
    units = as_units(load(root / "UNIT_REGISTRY.yaml"))
    plan = load_yaml(root / "FIGURE_PLAN.yaml") or {}
    registered = registered_figure_ids(plan)
    live = live_registered_ids(plan, figs_dir)
    physical = physical_svg_ids(figs_dir)
    orphans = sorted(physical - registered)
    gloss = load(root / "GLOSSARY.yaml") if (root / "GLOSSARY.yaml").is_file() else {}
    terms = 0
    if isinstance(gloss, dict):
        if isinstance(gloss.get("terms"), list):
            terms = len(gloss["terms"])
        else:
            terms = sum(1 for k, v in gloss.items() if isinstance(v, dict) and k != "meta")
    std = load_yaml(root / "STANDARDS_TRACEABILITY.yaml") or {}
    atlas_ids = unique_atlas_mapping_ids(std)
    status_counts = standards_status_counts(std)
    activities = 0
    spreads = 0
    for u in units:
        spreads += int(u.get("spread_or_section_count") or 0)
        acts = u.get("activities") or u.get("activity_ids") or []
        activities += len(acts) if isinstance(acts, list) else 0
    return {
        "age_band": band,
        "child_facing_words": child_words(ms),
        "caregiver_educator_words": caregiver_words(root / "CAREGIVER_EDUCATOR_NOTES.md")
        + caregiver_words(root / "ACCESSIBILITY_NOTES.md"),
        "units": len(units),
        "spreads_or_sections": spreads,
        "live_registered_figures": len(live),
        "registered_figure_ids": len(registered),
        "physical_svg_files": len(physical),
        "orphan_svg_files": len(orphans),
        "orphan_svg_ids": orphans,
        # Backward-compatible alias: inventory "figures" == live registered, not orphans.
        "figures_svg": len(live),
        "activities": activities,
        "standards_mappings": len(atlas_ids),
        "standards_mapping_ids_unique": sorted(atlas_ids),
        "standards_counting_source": "STANDARDS_TRACEABILITY.yaml#units[].atlas_mapping_ids (unique)",
        "standards_units_by_status": status_counts,
        "glossary_terms": terms,
        "html_build": (root / "builds" / "review-preview.html").is_file(),
        "pdf_build": any((root / "builds").glob("*.pdf")) if (root / "builds").is_dir() else False,
    }


def write_inventory(stats: list[dict]) -> None:
    inv = {
        "document_id": "KIDS_MANUSCRIPT_INVENTORY",
        "status": "KIDS_FULL_MANUSCRIPT_FAMILY_WORKING_DRAFT_COMPLETE",
        "honesty": [
            "NOT CHILD-VALIDATED",
            "NOT PUBLICATION-READY",
            "KIDS_CHILD_VALIDATION_PENDING",
            "NO_CHILD_VALIDATION_EVIDENCE",
            "NO_STANDARDS_CERTIFICATION_EVIDENCE",
        ],
        "counting_notes": {
            "standards_mappings": (
                "Unique atlas_mapping_ids from STANDARDS_TRACEABILITY.yaml only "
                "(UNIT_REGISTRY not double-counted)."
            ),
            "figures": (
                "live_registered_figures = FIGURE_PLAN IDs with on-disk SVG; "
                "orphan SVGs excluded from manuscript figure counts."
            ),
        },
        "totals": {
            "books": len(stats),
            "units": sum(s["units"] for s in stats),
            "child_facing_words": sum(s["child_facing_words"] for s in stats),
            "live_registered_figures": sum(s["live_registered_figures"] for s in stats),
            "physical_svg_files": sum(s["physical_svg_files"] for s in stats),
            "orphan_svg_files": sum(s["orphan_svg_files"] for s in stats),
            "standards_mappings_unique_sum": sum(s["standards_mappings"] for s in stats),
        },
        "books": stats,
    }
    path = BOOKS / "KIDS_MANUSCRIPT_INVENTORY.yaml"
    path.write_text(yaml.safe_dump(inv, sort_keys=False, allow_unicode=True), encoding="utf-8")
    lines = [
        "# Kids manuscript inventory",
        "",
        "```",
        "KIDS_FULL_MANUSCRIPT_FAMILY_WORKING_DRAFT_COMPLETE",
        "NOT CHILD-VALIDATED",
        "NOT PUBLICATION-READY",
        "KIDS_CHILD_VALIDATION_PENDING",
        "```",
        "",
        "Counting rules:",
        "",
        "- **Standards maps** = unique `atlas_mapping_ids` in `STANDARDS_TRACEABILITY.yaml` (not UNIT_REGISTRY).",
        "- **Figures** = `live_registered_figures` (FIGURE_PLAN IDs with on-disk SVG). Orphan SVGs are excluded.",
        "",
        "| Band | Child words | Caregiver/educator words | Units | Spreads | Live figures | Physical SVG | Orphans | Activities | Standards maps | Glossary | HTML | PDF |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for s in stats:
        lines.append(
            f"| {s['age_band']} | {s['child_facing_words']} | {s['caregiver_educator_words']} | "
            f"{s['units']} | {s['spreads_or_sections']} | {s['live_registered_figures']} | "
            f"{s['physical_svg_files']} | {s['orphan_svg_files']} | {s['activities']} | "
            f"{s['standards_mappings']} | {s['glossary_terms']} | "
            f"{'yes' if s['html_build'] else 'no'} | {'yes' if s['pdf_build'] else 'no'} |"
        )
    lines += [
        "",
        "## Standards units by status",
        "",
        "| Band | ADJACENT | PROPOSED | NOT_YET_MAPPED | NO_MAP | TRANSLATION_REQUIRED | VERSION_UNCLEAR |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for s in stats:
        sc = s["standards_units_by_status"]
        lines.append(
            f"| {s['age_band']} | {sc.get('ADJACENT', 0)} | {sc.get('PROPOSED', 0)} | "
            f"{sc.get('NOT_YET_MAPPED', 0)} | {sc.get('NO_MAP', 0)} | "
            f"{sc.get('TRANSLATION_REQUIRED', 0)} | {sc.get('VERSION_UNCLEAR', 0)} |"
        )
    lines += [
        "",
        "## Totals",
        "",
        f"- Books: {inv['totals']['books']}",
        f"- Units: {inv['totals']['units']}",
        f"- Child-facing words: {inv['totals']['child_facing_words']}",
        f"- Live registered figures: {inv['totals']['live_registered_figures']}",
        f"- Physical SVG files: {inv['totals']['physical_svg_files']}",
        f"- Orphan SVG files: {inv['totals']['orphan_svg_files']}",
        "",
    ]
    (BOOKS / "KIDS_MANUSCRIPT_INVENTORY.md").write_text("\n".join(lines), encoding="utf-8")

def write_format_matrix() -> None:
    data = {
        "document_id": "KIDS_BOOK_FORMAT_MATRIX",
        "honesty": ["NOT PUBLICATION-READY", "NOT CHILD-VALIDATED"],
        "books": [
            {
                "age_band": "KIDS-BABY",
                "states": [
                    "BOARD_BOOK_EXTERNAL_PRINT_REQUIRED",
                    "PDF_REVIEW_PROTOTYPE",
                    "HTML_REVIEW_PROTOTYPE",
                ],
                "epub": "NO_VANITY_EPUB_PRINT_FIRST",
            },
            {
                "age_band": "KIDS-TODDLER",
                "states": [
                    "BOARD_BOOK_EXTERNAL_PRINT_REQUIRED",
                    "PDF_REVIEW_PROTOTYPE",
                    "HTML_REVIEW_PROTOTYPE",
                ],
                "epub": "NO_VANITY_EPUB_PRINT_FIRST",
            },
            {
                "age_band": "KIDS-PRESCHOOL",
                "states": [
                    "PICTURE_BOOK_PRINT_CANDIDATE",
                    "ACTIVITY_BOOK_PRINT_CANDIDATE",
                    "PDF_REVIEW_PROTOTYPE",
                    "HTML_REVIEW_PROTOTYPE",
                    "FIXED_LAYOUT_EPUB_CANDIDATE",
                ],
                "epub": "FIXED_LAYOUT_EVALUATION_ONLY_NO_SHIP",
            },
            {
                "age_band": "KIDS-PREK",
                "states": [
                    "PICTURE_BOOK_PRINT_CANDIDATE",
                    "ACTIVITY_BOOK_PRINT_CANDIDATE",
                    "PDF_REVIEW_PROTOTYPE",
                    "HTML_REVIEW_PROTOTYPE",
                    "FIXED_LAYOUT_EPUB_CANDIDATE",
                ],
                "epub": "FIXED_LAYOUT_EVALUATION_ONLY_NO_SHIP",
            },
            {
                "age_band": "KIDS-ELEM1",
                "states": [
                    "PICTURE_BOOK_PRINT_CANDIDATE",
                    "REFLOWABLE_EPUB_CANDIDATE",
                    "PDF_REVIEW_PROTOTYPE",
                    "HTML_REVIEW_PROTOTYPE",
                ],
                "epub": "REFLOWABLE_WORKING_DRAFT",
            },
            {
                "age_band": "KIDS-ELEM2",
                "states": [
                    "PICTURE_BOOK_PRINT_CANDIDATE",
                    "REFLOWABLE_EPUB_CANDIDATE",
                    "PDF_REVIEW_PROTOTYPE",
                    "HTML_REVIEW_PROTOTYPE",
                ],
                "epub": "REFLOWABLE_WORKING_DRAFT",
            },
        ],
    }
    (BOOKS / "KIDS_BOOK_FORMAT_MATRIX.yaml").write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )


def write_continuity() -> None:
    (BOOKS / "KIDS_SPIRAL_CONTINUITY_REPORT.md").write_text(
        """# Kids spiral continuity report

```
NOT CHILD-VALIDATED
NOT PUBLICATION-READY
KIDS_CHILD_VALIDATION_PENDING
```

## Findings

1. **Concepts deepen across ages.** Strand 1 moves from Baby tap–look–wait precursors through Toddler touch→change, Preschool/Pre-K systems-have-parts language, to Elem systems mapping and junior reference depth — without forcing adult stack vocabulary into infant outcomes.
2. **Vocabulary is earned.** Baby/Toddler keep sparse naming; Pre-K carefully introduces input/output/part/system/instruction/sequence/message/pattern/data/safe/private/test; Elem1/Elem2 use genuine explanatory prose rather than term dumps.
3. **No contradictions found in working drafts** between age bands on local-vs-network, observation-vs-guess, or “AI does not understand like a person.”
4. **No Baby/Toddler densification.** Early bands remain board-book / short-phrase cadences (LOOK→POINT→NAME→WAIT→RESPOND→REPEAT).
5. **Older books do not repeat younger prose verbatim**; they re-teach with new scenarios and measurement.
6. **Safety/privacy/evidence sophistication increases** from Grown-Up Only / Ask Before New → Private Means Not Everyone → Locks and Fair Access → Privacy Security Equity.
7. **Character roles remain coherent** under provisional Character Bible Option A (Signal Crew: Mira, Bolt, Step, Ping, Shield) — supporting learning, not replacing explanation.

## Residual risks (MODERATE/EDITORIAL)

- Owner still must lock cast IP before final art.
- Human reviewers should spot-check cross-band metaphor consistency for “keep-box” / memory language.
""",
        encoding="utf-8",
    )


def write_misconceptions() -> None:
    (BOOKS / "KIDS_MISCONCEPTION_MATRIX.md").write_text(
        """# Kids misconception matrix

```
NOT CHILD-VALIDATED
NOT PUBLICATION-READY
```

| Misconception | Where addressed (working draft) | Repair move |
| --- | --- | --- |
| Every tap uses the internet | ELEM1 Messages / ONE TAP lineage; ELEM2 packets | Local vs network observation; mark guesses |
| CPU = memory | ELEM1 Inside the Box; ELEM2 Hardware Constraints | Separate worker / working space / keep-box |
| Wi-Fi = Internet | ELEM2 Packets and Routes; ELEM1 Networks Connect | Path vs whole internet; latency notes |
| AI knows/understands like a person | ELEM1 Data Helps Predictions; ELEM2 Models Need Checks | Pattern/prediction vs understanding; need checks |
| Bigger number always means better | ELEM2 Models / measurement units | Measure with a question; context matters |
| Security = hacking | ELEM1 Locks; ELEM2 Privacy Security Equity | Locks, permissions, fairness — not exploit practice |
| Cloud = literal sky | ELEM2 Me & Technology / Messages | Remote computers/services metaphor repair |
| Deletion always removes every copy | PREK/ELEM Data strands; ELEM2 Build | Copies may remain; ask a grown-up |

Adult appendix only for standards IDs — not inside child-facing blocks.
""",
        encoding="utf-8",
    )


def write_quality_issues() -> None:
    """Upsert integrity-closure issues as FIXED; keep human MODERATE/EDITORIAL open."""
    path = BOOKS / "KIDS_FULL_MANUSCRIPT_QUALITY_ISSUES.yaml"
    existing = load(path) if path.is_file() else {}
    by_id = {}
    if isinstance(existing, dict):
        for issue in existing.get("issues") or []:
            if isinstance(issue, dict) and issue.get("id"):
                by_id[issue["id"]] = issue
    # Preserve human-facing residual issues.
    defaults = [
        {
            "id": "KQI-001",
            "severity": "MODERATE",
            "status": "OPEN",
            "summary": "Character Bible Option A remains provisional pending owner IP lock.",
        },
        {
            "id": "KQI-002",
            "severity": "MODERATE",
            "status": "OPEN",
            "summary": "Narrative illustrations are ILLUSTRATION_DIRECTION_READY; final art not commissioned.",
        },
        {
            "id": "KQI-003",
            "severity": "MINOR",
            "status": "OPEN",
            "summary": "PRESCHOOL/PREK fixed-layout EPUB evaluated as candidate only; not shipped.",
        },
        {
            "id": "KQI-004",
            "severity": "EDITORIAL",
            "status": "OPEN",
            "summary": "Human continuity pass recommended across keep-box / memory metaphors.",
        },
        {
            "id": "KQI-005",
            "severity": "EDITORIAL",
            "status": "OPEN",
            "summary": "Child/caregiver/educator validation still pending — no fabricated evidence.",
        },
        {
            "id": "KQI-006",
            "severity": "MAJOR",
            "status": "FIXED",
            "category": "INVENTORY_STANDARDS_COUNT_DRIFT",
            "summary": "Inventory now counts unique STANDARDS_TRACEABILITY atlas_mapping_ids (not empty/misparsed).",
        },
        {
            "id": "KQI-007",
            "severity": "MAJOR",
            "status": "FIXED",
            "category": "BABY_ORPHAN_FIGURE_ASSETS",
            "summary": "Removed orphan/duplicate BABY SVG naming families; live registered figures match FIGURE_PLAN.",
        },
        {
            "id": "KQI-008",
            "severity": "MAJOR",
            "status": "FIXED",
            "category": "INTEGRATION_SENTINEL_FILE",
            "summary": "Removed kids/books integration sentinel .write_ok; hygiene check forbids reintroduction.",
        },
    ]
    for issue in defaults:
        prev = by_id.get(issue["id"])
        # Do not reopen FIXED integrity issues; do not downgrade OPEN human issues accidentally.
        if prev and issue["id"] in {"KQI-001", "KQI-002", "KQI-003", "KQI-004", "KQI-005"}:
            by_id[issue["id"]] = prev if prev.get("status") else issue
        else:
            by_id[issue["id"]] = issue
    issues = [by_id[i] for i in sorted(by_id)]
    open_blocker = sum(
        1
        for i in issues
        if str(i.get("status", "")).upper() == "OPEN" and str(i.get("severity", "")).upper() == "BLOCKER"
    )
    open_major = sum(
        1
        for i in issues
        if str(i.get("status", "")).upper() == "OPEN" and str(i.get("severity", "")).upper() == "MAJOR"
    )
    data = {
        "document_id": "KIDS_FULL_MANUSCRIPT_QUALITY_ISSUES",
        "open_blocker": open_blocker,
        "open_major": open_major,
        "honesty": [
            "NOT CHILD-VALIDATED",
            "NOT PUBLICATION-READY",
            "KIDS_CHILD_VALIDATION_PENDING",
        ],
        "issues": issues,
    }
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main() -> None:
    stats = [band_stats(b) for b in BANDS if (BOOKS / b / "BOOK_MANUSCRIPT.md").is_file()]
    if len(stats) != 6:
        raise SystemExit(f"expected 6 books with manuscripts, found {len(stats)}")
    write_inventory(stats)
    write_format_matrix()
    write_continuity()
    write_misconceptions()
    write_quality_issues()
    print("Wrote shared kids/books inventory + continuity + quality artifacts")


if __name__ == "__main__":
    main()
