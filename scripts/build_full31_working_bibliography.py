#!/usr/bin/env python3
"""Build Full31 working bibliography from PR #4 CE source-integrity truth.

Starting truth:
  - publication/preproduction/CANDIDATE_BIBLIOGRAPHY.bib (+ CE local bibs)
  - scripts/validate_ce_sources.py classification / verification / canonical IDs

Promotes only records already present in CE candidate set or in the live
book/references/references.bib (accepted-main CH02 keys). Does not invent
DOI/ISBN/page/year. Does not modify publication/gates/gate-3/ or silently
overwrite book/references/references.bib.

Outputs (working set — Quarto-citable, not yet global-merge authorized):
  - publication/full31/WORKING_BIBLIOGRAPHY.bib
  - publication/full31/WORKING_BIBLIOGRAPHY_INDEX.yaml
  - publication/full31/WORKING_BIBLIOGRAPHY_REPORT.md

Usage:
  python scripts/build_full31_working_bibliography.py
  python scripts/build_full31_working_bibliography.py --check
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

from validate_ce_sources import (  # noqa: E402
    ALLOWED_VERIFICATION,
    GATE_NOTE,
    WCAG_RESOLUTION,
    assign_verification,
    audit,
    canonical_identifier,
    classify_bib,
    format_bib_entry,
    load_all_occurrences,
    parse_bib,
)
from yaml_util import dump_yaml  # noqa: E402

SCHEMA_VERSION = "1.0.0"
STATUS = "WORKING_FULL31_BIBLIOGRAPHY"
FULL31 = ROOT / "publication" / "full31"
OUT_BIB = FULL31 / "WORKING_BIBLIOGRAPHY.bib"
OUT_INDEX = FULL31 / "WORKING_BIBLIOGRAPHY_INDEX.yaml"
OUT_REPORT = FULL31 / "WORKING_BIBLIOGRAPHY_REPORT.md"
BOOK_BIB = ROOT / "book" / "references" / "references.bib"
CANDIDATE_BIB = ROOT / "publication" / "preproduction" / "CANDIDATE_BIBLIOGRAPHY.bib"

# Source-register IDs used in Full31 CLAIM_PLAN / SOURCE_NEEDS → bib keys already
# verified in CE candidate set. Prefer primary keys; siblings remain as aliases.
SOURCE_REGISTER_TO_BIB: dict[str, list[str]] = {
    "SRC-WAIKE": ["src-waike", "src-waike-ce3", "waike-research-ops-ce06"],
    "SRC-HARDWARE": ["src-hardware-quartet", "src-hardware-ce3"],
    "SRC-DEVICE-OS": ["src-device-os-ce3"],
    "SRC-CE06-02": ["itu-t-g1011"],
}

# Tokens that are project/lab/gate evidence IDs, not bibliography keys.
NON_BIB_TOKENS = frozenset(
    {
        "lab-tap-001",
        "gate3-review-snapshot",
        "gate3-evidence",
    }
)

# Undated WCAG shortcut must never enter the working bib as a key.
BLOCKED_KEYS = frozenset({"wcag22"})

CITE_TOKEN_RE = re.compile(r"`([A-Za-z][\w:-]*)`")
YAML_LIST_KEY_RE = re.compile(r"^\s*-\s+([A-Za-z][\w:-]*)\s*$")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_chapter_id(raw: str) -> str:
    raw = raw.strip().lower()
    m = re.match(r"ch0*(\d+)$", raw)
    if m:
        return f"ch{int(m.group(1)):02d}"
    if raw.startswith("ce-"):
        return raw
    return raw


def collect_full31_citation_tokens() -> list[dict[str, str]]:
    """Collect citation-like tokens from Full31 claim plans and source needs."""
    rows: list[dict[str, str]] = []
    chapters = FULL31 / "chapters"
    for ch_dir in sorted(chapters.glob("ch*")):
        if not ch_dir.is_dir():
            continue
        ch = normalize_chapter_id(ch_dir.name)
        claim = ch_dir / "CLAIM_PLAN.yaml"
        if claim.exists():
            in_keys = False
            for line in claim.read_text(encoding="utf-8").splitlines():
                if re.match(r"\s*citation_keys:\s*$", line):
                    in_keys = True
                    continue
                if in_keys:
                    m = YAML_LIST_KEY_RE.match(line)
                    if m:
                        rows.append(
                            {
                                "chapter": ch,
                                "token": m.group(1),
                                "origin": "claim_plan.citation_keys",
                            }
                        )
                        continue
                    if line.strip() and not line.strip().startswith("-"):
                        in_keys = False
        needs = ch_dir / "SOURCE_NEEDS.md"
        if needs.exists():
            text = needs.read_text(encoding="utf-8")
            # Only harvest backtick tokens from Planned sources / Needs tables.
            in_table = False
            for line in text.splitlines():
                if re.search(r"planned sources|needs table", line, re.I):
                    in_table = True
                    continue
                if in_table and line.startswith("## ") and "source" not in line.lower():
                    in_table = False
                if not in_table:
                    continue
                if not line.startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip("|").split("|")]
                if not cells:
                    continue
                first = cells[0]
                for m in CITE_TOKEN_RE.finditer(first):
                    rows.append(
                        {
                            "chapter": ch,
                            "token": m.group(1),
                            "origin": "source_needs.table",
                        }
                    )
                # Also accept bare first-cell keys without backticks when simple.
                if re.fullmatch(r"[A-Za-z][\w:-]*", first):
                    rows.append(
                        {
                            "chapter": ch,
                            "token": first,
                            "origin": "source_needs.table",
                        }
                    )
    return rows


def resolve_token_to_bib_keys(token: str) -> tuple[str, list[str]]:
    """Return (kind, bib_keys). kind in bib|source_register|non_bib|blocked|unknown."""
    if token in BLOCKED_KEYS:
        return "blocked", []
    if token in NON_BIB_TOKENS:
        return "non_bib", []
    if token in SOURCE_REGISTER_TO_BIB:
        return "source_register", list(SOURCE_REGISTER_TO_BIB[token])
    # Treat lowercase / mixed case as potential bib keys.
    return "bib_candidate", [token]


def load_ce_unique() -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, str]]:
    rows = load_all_occurrences()
    by_key_raw: dict[str, str] = {}
    for r in rows:
        by_key_raw.setdefault(r["bib_key"].lower(), r.get("_raw_body") or "")
    # Prefer raw bodies from candidate bib if present (deterministic formatting).
    if CANDIDATE_BIB.exists():
        for entry in parse_bib(CANDIDATE_BIB):
            by_key_raw[entry["key"].lower()] = entry.get("_raw_body", "")
    result = audit(rows)
    for u in result["unique_records"]:
        u["_raw_body"] = by_key_raw.get(u["bib_key"].lower(), "")
        # Preserve CE package usage; will extend with Full31 chapters.
        u["ce_chapter_usage"] = list(u.get("chapter_usage") or [])
        u["full31_chapter_usage"] = []
        u["promotion_origin"] = "ce_candidate"
    return result["unique_records"], result, by_key_raw


def load_book_only_records(
    existing_keys: set[str],
) -> list[dict[str, Any]]:
    """Promote accepted-main book/references keys missing from CE candidate."""
    if not BOOK_BIB.exists():
        return []
    out: list[dict[str, Any]] = []
    for entry in parse_bib(BOOK_BIB):
        key = entry["key"]
        if key.lower() in existing_keys:
            continue
        cls = classify_bib(entry)
        ver = assign_verification(entry, cls)
        rec: dict[str, Any] = {
            "bib_key": key,
            "entry_type": entry.get("entry_type"),
            "title": entry.get("title"),
            "year": entry.get("year"),
            "url": entry.get("url"),
            "doi": entry.get("doi"),
            "isbn": entry.get("isbn"),
            "author": entry.get("author"),
            "howpublished": entry.get("howpublished"),
            "note": entry.get("note"),
            "publisher": entry.get("publisher"),
            "edition": entry.get("edition"),
            "source_class": cls,
            "verification_status": ver,
            "canonical_identifier": canonical_identifier(entry),
            "metadata_conflict_status": "NONE",
            "ce_chapter_usage": [],
            "full31_chapter_usage": ["ch02"],
            "chapter_usage": ["book/references", "ch02"],
            "promotion_origin": "book_references_accepted_main",
            "_raw_body": entry.get("_raw_body", ""),
        }
        out.append(rec)
    return out


def overlay_full31_usage(
    unique: list[dict[str, Any]],
    tokens: list[dict[str, str]],
) -> dict[str, Any]:
    by_key = {u["bib_key"].lower(): u for u in unique}
    citation_occurrences = 0
    unresolved: list[dict[str, str]] = []
    blocked: list[dict[str, str]] = []
    non_bib: list[dict[str, str]] = []
    mapped_register: list[dict[str, str]] = []

    for row in tokens:
        token = row["token"]
        ch = row["chapter"]
        kind, keys = resolve_token_to_bib_keys(token)
        if kind == "blocked":
            blocked.append(row)
            citation_occurrences += 1
            continue
        if kind == "non_bib":
            non_bib.append(row)
            citation_occurrences += 1
            continue
        if kind == "source_register":
            mapped_register.append({**row, "mapped_bib_keys": ",".join(keys)})
            citation_occurrences += 1
            hit = False
            for k in keys:
                u = by_key.get(k.lower())
                if u:
                    hit = True
                    usage = set(u.get("full31_chapter_usage") or [])
                    usage.add(ch)
                    u["full31_chapter_usage"] = sorted(usage)
            if not hit:
                unresolved.append({**row, "reason": "source_register_unmapped_in_bib"})
            continue
        # bib_candidate
        citation_occurrences += 1
        u = by_key.get(token.lower())
        if not u:
            unresolved.append({**row, "reason": "bib_key_not_in_working_set"})
            continue
        usage = set(u.get("full31_chapter_usage") or [])
        usage.add(ch)
        u["full31_chapter_usage"] = sorted(usage)

    # Merge chapter_usage display: CE packages + Full31 chapters.
    for u in unique:
        merged = []
        for x in (u.get("ce_chapter_usage") or []) + (u.get("full31_chapter_usage") or []):
            if x not in merged:
                merged.append(x)
        # Keep book origin tag if present.
        for x in u.get("chapter_usage") or []:
            if x not in merged and x.startswith("book"):
                merged.insert(0, x)
        u["chapter_usage"] = merged

    return {
        "citation_occurrences": citation_occurrences,
        "unresolved": unresolved,
        "blocked": blocked,
        "non_bib": non_bib,
        "mapped_register": mapped_register,
    }


def recompute_canonical_stats(unique: list[dict[str, Any]]) -> dict[str, Any]:
    ver_counts: dict[str, int] = defaultdict(int)
    class_counts: dict[str, int] = defaultdict(int)
    by_canonical: dict[str, set[str]] = defaultdict(set)
    for u in unique:
        assert u["verification_status"] in ALLOWED_VERIFICATION
        ver_counts[u["verification_status"]] += 1
        class_counts[u["source_class"]] += 1
        by_canonical[u["canonical_identifier"]].add(u["bib_key"])
    aliases = [
        {"canonical_identifier": cid, "bib_keys": sorted(keys)}
        for cid, keys in sorted(by_canonical.items())
        if len(keys) > 1
    ]
    return {
        "ver_counts": dict(sorted(ver_counts.items())),
        "class_counts": dict(sorted(class_counts.items())),
        "unique_canonical_works": len(by_canonical),
        "same_work_aliases": aliases,
        "same_work_alias_count": len(aliases),
    }


def render_working_bib(unique: list[dict[str, Any]]) -> str:
    header = (
        "% WORKING_BIBLIOGRAPHY.bib — Full31 manuscript-wave working bibliography\n"
        "% Agent EVIDENCE-C. Quarto-compatible BibTeX.\n"
        f"% status: {STATUS}\n"
        f"% gate_note: {GATE_NOTE}\n"
        "% Starting truth: PR #4 CE candidate bibliography + validate_ce_sources.py.\n"
        "% Promote-only: CE candidate unique keys + accepted-main book/references gaps.\n"
        "% Do not invent DOI/ISBN/page/year. HTTP 200 alone is not verification.\n"
        "% NOT a silent overwrite of book/references/references.bib — integrator\n"
        "% must authorize promotion into the live book bibliography.\n"
        "%\n"
        "% WCAG 2.2 dated Recommendations (distinct; do not collapse):\n"
        "%   wcag22-20231005 → https://www.w3.org/TR/2023/REC-WCAG22-20231005/\n"
        "%   wcag22-20241212 → https://www.w3.org/TR/2024/REC-WCAG22-20241212/\n"
        "% Undated https://www.w3.org/TR/WCAG22/ is blocked as a bib key.\n"
        "\n"
    )
    blocks = [
        format_bib_entry(u) for u in sorted(unique, key=lambda r: r["bib_key"].lower())
    ]
    return header + "\n\n".join(blocks) + "\n"


def render_index(
    unique: list[dict[str, Any]],
    stats: dict[str, Any],
    overlay: dict[str, Any],
    ce_result: dict[str, Any],
) -> str:
    records = []
    for u in sorted(unique, key=lambda r: r["bib_key"].lower()):
        records.append(
            {
                "bib_key": u["bib_key"],
                "entry_type": u.get("entry_type"),
                "title": u.get("title"),
                "year": u.get("year"),
                "url": u.get("url"),
                "doi": u.get("doi"),
                "isbn": u.get("isbn"),
                "source_class": u["source_class"],
                "verification_status": u["verification_status"],
                "canonical_identifier": u["canonical_identifier"],
                "ce_chapter_usage": u.get("ce_chapter_usage") or [],
                "full31_chapter_usage": u.get("full31_chapter_usage") or [],
                "chapter_usage": u.get("chapter_usage") or [],
                "promotion_origin": u.get("promotion_origin"),
                "metadata_conflict_status": u.get("metadata_conflict_status", "NONE"),
                "dated_edition": WCAG_RESOLUTION.get(u["bib_key"]),
            }
        )
    data: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "gate_note": GATE_NOTE,
        "rights": (
            "Working Full31 bibliography. Does not modify Gate 3 evidence. "
            "Does not authorize silent merge into book/references/references.bib."
        ),
        "integration_path": {
            "working_bib": "publication/full31/WORKING_BIBLIOGRAPHY.bib",
            "quarto_cite_target": (
                "Point chapter Quarto bibliographies at WORKING_BIBLIOGRAPHY.bib "
                "during manuscript wave, or merge selected keys into "
                "book/references/references.bib after integrator authorization."
            ),
            "live_book_bib": "book/references/references.bib",
            "ce_candidate_truth": "publication/preproduction/CANDIDATE_BIBLIOGRAPHY.bib",
            "validator": "scripts/validate_ce_sources.py",
            "builder": "scripts/build_full31_working_bibliography.py",
        },
        "counts": {
            "ce_source_occurrences": ce_result["occurrences"],
            "full31_citation_token_occurrences": overlay["citation_occurrences"],
            "unique_bib_keys": len(unique),
            "unique_canonical_works": stats["unique_canonical_works"],
            "same_work_alias_groups": stats["same_work_alias_count"],
        },
        "verification_counts": stats["ver_counts"],
        "classification_counts": stats["class_counts"],
        "wcag_resolution": {
            "strategy": "two_dated_recommendation_keys",
            "keys": WCAG_RESOLUTION,
            "undated_latest_shortcut": "https://www.w3.org/TR/WCAG22/",
            "history": "https://www.w3.org/standards/history/WCAG22/",
            "blocked_bib_keys": sorted(BLOCKED_KEYS),
        },
        "source_register_alias_map": SOURCE_REGISTER_TO_BIB,
        "same_work_aliases": stats["same_work_aliases"],
        "blocked_undated_wcag_occurrences": overlay["blocked"],
        "non_bib_tokens": overlay["non_bib"],
        "unresolved_citation_tokens": overlay["unresolved"],
        "records": records,
    }
    text = dump_yaml(data)
    return text if text.endswith("\n") else text + "\n"


def render_report(
    unique: list[dict[str, Any]],
    stats: dict[str, Any],
    overlay: dict[str, Any],
    ce_result: dict[str, Any],
) -> str:
    lines: list[str] = []
    lines.append("# Working Full-Book Bibliography Report (Agent EVIDENCE-C)")
    lines.append("")
    lines.append(f"**schema_version:** `{SCHEMA_VERSION}`  ")
    lines.append(f"**status:** `{STATUS}`  ")
    lines.append(f"**gate_note:** `{GATE_NOTE}`  ")
    lines.append(
        "**scope:** Full31 manuscript-wave working bibliography "
        "(CE candidate truth + accepted-main book/references gaps + Full31 chapter overlay)  "
    )
    lines.append(
        "**global merge:** not authorized — working set only "
        "(see Integrator merge notes)"
    )
    lines.append("")
    lines.append("## Counts (report separately)")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| CE chapter-local source occurrences | {ce_result['occurrences']} |")
    lines.append(
        f"| Full31 citation-token occurrences "
        f"(CLAIM_PLAN + SOURCE_NEEDS) | {overlay['citation_occurrences']} |"
    )
    lines.append(f"| Unique bib keys (working set) | {len(unique)} |")
    lines.append(f"| Unique canonical works | {stats['unique_canonical_works']} |")
    lines.append(f"| Same-work alias groups | {stats['same_work_alias_count']} |")
    lines.append("")
    lines.append(
        "Canonical-work grouping priority: DOI → ISBN+edition → dated standards/RFC → "
        "URL+dated edition → repo+commit+role → title/author/year uncertain fallback. "
        "The two WCAG dated Recommendations remain distinct works."
    )
    lines.append("")
    lines.append("### Verification status (unique keys)")
    lines.append("")
    lines.append("| verification_status | count |")
    lines.append("|---|---:|")
    for k, v in stats["ver_counts"].items():
        lines.append(f"| `{k}` | {v} |")
    lines.append("")
    lines.append("### Classification (unique keys)")
    lines.append("")
    lines.append("| source_class | count |")
    lines.append("|---|---:|")
    for k, v in stats["class_counts"].items():
        lines.append(f"| `{k}` | {v} |")
    lines.append("")
    lines.append("## WCAG 2.2 confirmation")
    lines.append("")
    lines.append(
        "Working bibliography preserves **two** dated Recommendation records:"
    )
    lines.append("")
    lines.append("| Bib key | Year | Dated TR URL | In working set |")
    lines.append("|---|---|---|---|")
    present = {u["bib_key"] for u in unique}
    for key, meta in WCAG_RESOLUTION.items():
        lines.append(
            f"| `{key}` | {meta['year']} | {meta['url']} | "
            f"{'yes' if key in present else 'NO — FAIL'} |"
        )
    lines.append("")
    lines.append(
        f"Blocked undated key `{', '.join(sorted(BLOCKED_KEYS))}` occurrences in Full31 "
        f"packets: **{len(overlay['blocked'])}** "
        "(must remap to dated keys before prose cite)."
    )
    if overlay["blocked"]:
        for b in overlay["blocked"]:
            lines.append(
                f"- `{b['chapter']}` via `{b['origin']}` token `{b['token']}`"
            )
    lines.append("")
    lines.append("## Same-work aliases")
    lines.append("")
    if stats["same_work_aliases"]:
        for a in stats["same_work_aliases"]:
            lines.append(
                f"- `{a['canonical_identifier']}` → {a['bib_keys']}"
            )
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Unresolved / non-bib tokens")
    lines.append("")
    lines.append(
        f"- Non-bib project/gate tokens: **{len(overlay['non_bib'])}** "
        "(not promoted as bibliography entries)"
    )
    lines.append(
        f"- Unresolved citation tokens (no working bib key): "
        f"**{len(overlay['unresolved'])}**"
    )
    for u in overlay["unresolved"]:
        lines.append(
            f"  - `{u['chapter']}` `{u['token']}` ({u.get('reason')}; {u['origin']})"
        )
    lines.append("")
    lines.append("## Unique records")
    lines.append("")
    lines.append(
        "| bib_key | source_class | verification_status | chapter_usage | "
        "canonical_identifier | origin |"
    )
    lines.append("|---|---|---|---|---|---|")
    for u in sorted(unique, key=lambda r: r["bib_key"].lower()):
        usage = ",".join(u.get("chapter_usage") or [])
        lines.append(
            f"| `{u['bib_key']}` | `{u['source_class']}` | `{u['verification_status']}` | "
            f"{usage} | `{u['canonical_identifier']}` | `{u.get('promotion_origin')}` |"
        )
    lines.append("")
    lines.append("## Integrator merge notes (EVIDENCE-A/B coordination)")
    lines.append("")
    lines.append(
        "- **This agent (EVIDENCE-C)** owns `publication/full31/WORKING_BIBLIOGRAPHY.*` "
        "and `scripts/build_full31_working_bibliography.py`. Commits stay focused there."
    )
    lines.append(
        "- **Do not** edit `publication/gates/gate-3/` from this wave."
    )
    lines.append(
        "- **Do not** silently overwrite `book/references/references.bib`. "
        "Promotion into the live book bib requires integrator authorization after "
        "EVIDENCE-A/B source audits settle."
    )
    lines.append(
        "- **CE candidate** (`publication/preproduction/CANDIDATE_*`, "
        "`scripts/validate_ce_sources.py`) remains the Concept Edition integrity truth; "
        "regenerate CE artifacts with Agent G tooling before regenerating this working set "
        "if CE local bibs change."
    )
    lines.append(
        "- **EVIDENCE-A** (standards / accepted-main source audit under `evidence/`) may "
        "add or reclassify standards metadata — merge by regenerating CE candidate first, "
        "then re-run this builder; prefer additive updates to `WORKING_BIBLIOGRAPHY_INDEX.yaml` "
        "verification fields over hand-editing the `.bib` body."
    )
    lines.append(
        "- **EVIDENCE-B** (if touching chapter SOURCE_NEEDS / CLAIM_PLAN citation_keys): "
        "keep dated WCAG keys distinct; never introduce undated `wcag22` as a cite key; "
        "map `SRC-*` register IDs via `source_register_alias_map` rather than inventing "
        "parallel bib entries."
    )
    lines.append(
        "- **`russell_norvig_aima`** remains `NEEDS_PRIMARY_VERIFICATION` until a "
        "primary edition/ISBN/year is verified — do not invent metadata to clear the flag."
    )
    lines.append(
        "- **Quarto integration path:** manuscript chapters may temporarily set "
        "`bibliography: ../../publication/full31/WORKING_BIBLIOGRAPHY.bib` (adjust "
        "relative path) or cite from a merged live bib once promoted."
    )
    lines.append("")
    lines.append("## Artifacts")
    lines.append("")
    lines.append("- `publication/full31/WORKING_BIBLIOGRAPHY.bib`")
    lines.append("- `publication/full31/WORKING_BIBLIOGRAPHY_INDEX.yaml`")
    lines.append("- `publication/full31/WORKING_BIBLIOGRAPHY_REPORT.md` (this file)")
    lines.append("- Builder: `scripts/build_full31_working_bibliography.py`")
    lines.append("- Upstream validator: `scripts/validate_ce_sources.py`")
    lines.append("")
    lines.append("## Non-goals")
    lines.append("")
    lines.append("- No Gate 3 / CH02-REVIEW-R1 edits")
    lines.append("- No Gate 3 PASS")
    lines.append("- No unauthorized merge into `book/references/references.bib`")
    lines.append("- No invented DOI/ISBN/page/year")
    lines.append("")
    return "\n".join(lines) + "\n"


def build() -> tuple[dict[str, str], dict[str, Any]]:
    unique, ce_result, _raw = load_ce_unique()
    existing = {u["bib_key"].lower() for u in unique}
    book_only = load_book_only_records(existing)
    unique.extend(book_only)

    tokens = collect_full31_citation_tokens()
    overlay = overlay_full31_usage(unique, tokens)
    stats = recompute_canonical_stats(unique)

    planned = {
        OUT_BIB: render_working_bib(unique),
        OUT_INDEX: render_index(unique, stats, overlay, ce_result),
        OUT_REPORT: render_report(unique, stats, overlay, ce_result),
    }
    meta = {
        "unique": unique,
        "stats": stats,
        "overlay": overlay,
        "ce_result": ce_result,
    }
    return planned, meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if working bibliography artifacts are stale",
    )
    args = parser.parse_args(argv)

    planned, meta = build()
    unique = meta["unique"]
    stats = meta["stats"]
    present = {u["bib_key"] for u in unique}
    for key in WCAG_RESOLUTION:
        if key not in present:
            print(f"build_full31_working_bibliography: FAIL — missing WCAG key {key}")
            return 1
    russell = next((u for u in unique if u["bib_key"] == "russell_norvig_aima"), None)
    if russell and russell["verification_status"] != "NEEDS_PRIMARY_VERIFICATION":
        print(
            "build_full31_working_bibliography: FAIL — "
            "russell_norvig_aima must remain NEEDS_PRIMARY_VERIFICATION until primary verify"
        )
        return 1

    changed: list[str] = []
    for path, text in planned.items():
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if digest(old) != digest(text):
            changed.append(str(path.relative_to(ROOT)))

    if args.check:
        if changed:
            print("build_full31_working_bibliography: FAIL — artifacts stale:")
            for c in changed:
                print(" -", c)
            return 1
        print(
            "build_full31_working_bibliography: PASS "
            f"(keys={len(unique)} canonical={stats['unique_canonical_works']} "
            f"aliases={stats['same_work_alias_count']})"
        )
        return 0

    for path, text in planned.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    print("build_full31_working_bibliography: wrote")
    for p in planned:
        print(" -", p.relative_to(ROOT))
    print(
        f"counts: bib_keys={len(unique)} "
        f"canonical={stats['unique_canonical_works']} "
        f"aliases={stats['same_work_alias_count']} "
        f"verification={stats['ver_counts']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
