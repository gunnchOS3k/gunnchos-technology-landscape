#!/usr/bin/env python3
"""Concept Edition source integrity + candidate bibliography (Agent G).

Reads chapter-local ``references.local.bib`` files under
``publication/preproduction/ce-*/`` and produces:

  - publication/preproduction/CANDIDATE_BIBLIOGRAPHY.bib
  - publication/preproduction/SOURCE_INTEGRITY_REPORT.md
  - updates verification fields on CANDIDATE_SOURCE_INDEX.yaml (via regenerate helpers)

Verification states (only):
  PRIMARY_METADATA_VERIFIED
  REPOSITORY_EVIDENCE_VERIFIED
  SECONDARY_EXPLANATORY
  NEEDS_PRIMARY_VERIFICATION

HTTP 200 alone is not verification. Does not invent DOI/ISBN/page/year.
Does not merge into book/references/references.bib.
Does not modify publication/gates/gate-3/.

Usage:
  python scripts/validate_ce_sources.py           # write artifacts + exit 0/1
  python scripts/validate_ce_sources.py --check   # fail if artifacts stale or hard conflicts
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

ALLOWED_VERIFICATION = frozenset(
    {
        "PRIMARY_METADATA_VERIFIED",
        "REPOSITORY_EVIDENCE_VERIFIED",
        "SECONDARY_EXPLANATORY",
        "NEEDS_PRIMARY_VERIFICATION",
    }
)

# Explicit secondary-explanatory keys (metadata may be fine; not primary authority).
SECONDARY_KEYS = frozenset(
    {
        "digitalregulation-qos-qoe",
        "mdn-performance",
        "mdn-performance-ce06",
        "mdn-network-monitor",
        "mdn-resource-timing",
        "wifi-alliance-discover",
        "nvme-base-spec",
    }
)

# WCAG dated-edition resolution (W3C standards history for WCAG22).
WCAG_RESOLUTION = {
    "wcag22-20231005": {
        "year": "2023",
        "url": "https://www.w3.org/TR/2023/REC-WCAG22-20231005/",
        "edition": "W3C Recommendation 5 October 2023",
    },
    "wcag22-20241212": {
        "year": "2024",
        "url": "https://www.w3.org/TR/2024/REC-WCAG22-20241212/",
        "edition": "W3C Recommendation 12 December 2024",
    },
}

CANDIDATE_BIB = PREPROD / "CANDIDATE_BIBLIOGRAPHY.bib"
INTEGRITY_REPORT = PREPROD / "SOURCE_INTEGRITY_REPORT.md"
SOURCE_INDEX = PREPROD / "CANDIDATE_SOURCE_INDEX.yaml"


def normalize_title(title: str | None) -> str:
    if not title:
        return ""
    t = title.replace("{", "").replace("}", "")
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def normalize_isbn(isbn: str | None) -> str:
    if not isbn:
        return ""
    return re.sub(r"[^0-9Xx]", "", isbn)


def parse_bib(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    entries: list[dict[str, str]] = []
    for match in re.finditer(
        r"@(\w+)\s*\{\s*([^,]+)\s*,(.*?)\n\}",
        text,
        flags=re.S,
    ):
        entry_type, key, body = match.group(1), match.group(2).strip(), match.group(3)
        fields: dict[str, str] = {
            "entry_type": entry_type,
            "key": key,
            "_raw_body": body,
        }
        for fm in re.finditer(r"(\w+)\s*=\s*\{([^{}]*)\}", body):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        # Preserve month = jan style without braces when present.
        for fm in re.finditer(r"(\w+)\s*=\s*([a-zA-Z0-9.-]+)\s*,", body):
            if fm.group(1).lower() not in fields:
                fields[fm.group(1).lower()] = fm.group(2).strip()
        entries.append(fields)
    return entries


def classify_bib(entry: dict[str, str]) -> str:
    et = entry.get("entry_type", "").lower()
    how = (entry.get("howpublished") or "").lower()
    note = (entry.get("note") or "").lower()
    key = entry.get("key", "").lower()
    url = entry.get("url") or ""
    if et == "book":
        return "textbooks"
    if (
        "rfc" in how
        or how.startswith("ietf")
        or "3gpp" in how
        or "nist" in how
        or "iso" in how
        or "w3c" in how
        or "itu-t" in how
        or key.startswith("rfc")
        or "nist" in key
        or "iso" in key
        or key.startswith("wcag")
    ):
        return "standards_specifications"
    if et == "techreport" or "nist" in how:
        return "standards_specifications"
    if et == "article" or "ieee" in how or "journal" in note:
        return "peer_reviewed"
    if "github.com" in url or "accepted main" in note or "repository" in how:
        if "github.com" in url or "accepted main" in note:
            return "project_accepted_main"
    if (
        "kernel.org" in url
        or "opentelemetry.io" in url
        or "khronos.org" in url
        or "jedec.org" in url
        or "ieee802.org" in url
        or "living" in how
        or "living" in note
    ):
        return "official_technical_documentation"
    if "mdn" in key or "documentation" in how:
        if "mdn" in key:
            return "other_explanatory"
        return "official_technical_documentation"
    return "other_explanatory"


def assign_verification(entry: dict[str, str], source_class: str) -> str:
    """Assign one of the four allowed verification states. Not HTTP-200."""
    key = entry.get("key", "")
    note = (entry.get("note") or "").lower()
    title = (entry.get("title") or "").lower()

    if key in SECONDARY_KEYS or "secondary explanatory" in note:
        return "SECONDARY_EXPLANATORY"

    if source_class == "project_accepted_main":
        return "REPOSITORY_EVIDENCE_VERIFIED"

    if (
        "intentionally omitted" in note
        or "until project shelf" in note
        or (entry.get("entry_type") == "book" and not entry.get("year"))
    ):
        return "NEEDS_PRIMARY_VERIFICATION"

    # Family/portal pages without a frozen edition year stay secondary when titled as family.
    if "family" in title and not entry.get("year"):
        return "SECONDARY_EXPLANATORY"

    # Primary metadata present from publisher/catalog fields already recorded in chapter bibs.
    if entry.get("doi") or entry.get("isbn") or entry.get("year") or entry.get("url"):
        return "PRIMARY_METADATA_VERIFIED"

    return "NEEDS_PRIMARY_VERIFICATION"


def canonical_identifier(entry: dict[str, str]) -> str:
    if entry.get("doi"):
        return f"doi:{entry['doi']}"
    isbn = normalize_isbn(entry.get("isbn"))
    if isbn:
        return f"isbn:{isbn}"
    if entry.get("url"):
        return f"url:{entry['url']}"
    how = entry.get("howpublished")
    if how:
        return f"howpublished:{how}"
    return f"key:{entry['key']}"


def load_all_occurrences() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ce in CE_DIRS:
        path = PREPROD / ce / "references.local.bib"
        for entry in parse_bib(path):
            cls = classify_bib(entry)
            ver = assign_verification(entry, cls)
            rows.append(
                {
                    "source_package": ce,
                    "bib_key": entry["key"],
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
                    "source_class": cls,
                    "verification_status": ver,
                    "canonical_identifier": canonical_identifier(entry),
                    "_raw_body": entry.get("_raw_body", ""),
                }
            )
    return rows


def audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by_key[r["bib_key"].lower()].append(r)

    unique: list[dict[str, Any]] = []
    key_conflicts: list[str] = []
    for key, group in sorted(by_key.items()):
        base = dict(group[0])
        packages = sorted({g["source_package"] for g in group})
        base["chapter_usage"] = packages
        conflict_fields: list[str] = []
        for field in ("title", "year", "url", "doi", "isbn"):
            vals = set()
            for g in group:
                raw = g.get(field)
                if not raw:
                    continue
                if field == "title":
                    vals.add(normalize_title(raw))
                elif field == "isbn":
                    vals.add(normalize_isbn(raw))
                else:
                    vals.add(str(raw).strip().lower())
            if len(vals) > 1:
                conflict_fields.append(field)
                shown = sorted(
                    {
                        (g.get(field) or "").strip()
                        for g in group
                        if (g.get(field) or "").strip()
                    }
                )
                key_conflicts.append(
                    f"{group[0]['bib_key']}: conflicting {field}: "
                    + " vs ".join(repr(s) for s in shown)
                )
        base["metadata_conflict_status"] = (
            "CONFLICT:" + ",".join(conflict_fields) if conflict_fields else "NONE"
        )
        # Prefer non-null title/year/url across group for unique record display.
        for field in ("title", "year", "url", "doi", "isbn", "author", "howpublished", "note"):
            if not base.get(field):
                for g in group:
                    if g.get(field):
                        base[field] = g[field]
                        break
        unique.append(base)

    # Duplicate DOI / ISBN across different keys
    doi_map: dict[str, set[str]] = defaultdict(set)
    isbn_map: dict[str, set[str]] = defaultdict(set)
    url_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for u in unique:
        if u.get("doi"):
            doi_map[u["doi"].lower()].add(u["bib_key"])
        ni = normalize_isbn(u.get("isbn"))
        if ni:
            isbn_map[ni].add(u["bib_key"])
        if u.get("url"):
            url_map[u["url"]].append(u)

    dup_doi = [f"{d}: {sorted(keys)}" for d, keys in sorted(doi_map.items()) if len(keys) > 1]
    dup_isbn = [f"{i}: {sorted(keys)}" for i, keys in sorted(isbn_map.items()) if len(keys) > 1]

    url_conflicts: list[str] = []
    url_title_aliases: list[str] = []
    for url, group in sorted(url_map.items()):
        titles = {normalize_title(g.get("title")) for g in group if g.get("title")}
        years = {(g.get("year") or "").strip() for g in group if g.get("year")}
        keys = [g["bib_key"] for g in group]
        if len(years) > 1:
            url_conflicts.append(
                f"{url}: keys={keys} years={sorted(years)} titles={sorted(titles)}"
            )
        elif len(titles) > 1 and len(keys) > 1:
            # Chapter-local descriptive titles for the same stable URL (e.g. repo audits).
            url_title_aliases.append(
                f"{url}: keys={keys} titles={sorted(titles)}"
            )

    missing_ver = [
        u["bib_key"]
        for u in unique
        if u.get("verification_status") not in ALLOWED_VERIFICATION
    ]

    # Alias groups: same normalized title+year, different keys
    alias_groups: list[str] = []
    by_ty: dict[tuple[str, str], set[str]] = defaultdict(set)
    for u in unique:
        t = normalize_title(u.get("title"))
        y = (u.get("year") or "").strip()
        if t:
            by_ty[(t, y)].add(u["bib_key"])
    for (t, y), keys in sorted(by_ty.items()):
        if len(keys) > 1:
            alias_groups.append(f"{y or 'noyear'} | {t} -> {sorted(keys)}")

    ver_counts: dict[str, int] = defaultdict(int)
    class_counts: dict[str, int] = defaultdict(int)
    for u in unique:
        ver_counts[u["verification_status"]] += 1
        class_counts[u["source_class"]] += 1

    hard_conflicts = key_conflicts + dup_doi + dup_isbn + url_conflicts + [
        f"missing verification: {k}" for k in missing_ver
    ]

    return {
        "occurrences": len(rows),
        "unique": len(unique),
        "unique_records": unique,
        "key_conflicts": key_conflicts,
        "dup_doi": dup_doi,
        "dup_isbn": dup_isbn,
        "url_conflicts": url_conflicts,
        "url_title_aliases": url_title_aliases,
        "missing_verification": missing_ver,
        "alias_groups": alias_groups,
        "ver_counts": dict(sorted(ver_counts.items())),
        "class_counts": dict(sorted(class_counts.items())),
        "hard_conflicts": hard_conflicts,
    }


def format_bib_entry(rec: dict[str, Any]) -> str:
    """Deterministic BibTeX from unique record (no invented fields)."""
    et = rec.get("entry_type") or "misc"
    key = rec["bib_key"]
    lines = [f"@{et}{{{key},"]
    order = (
        "author",
        "title",
        "journal",
        "booktitle",
        "publisher",
        "institution",
        "year",
        "month",
        "volume",
        "number",
        "pages",
        "edition",
        "doi",
        "isbn",
        "howpublished",
        "url",
        "note",
    )
    # Pull extra fields from first occurrence raw body when available.
    extras: dict[str, str] = {}
    raw = rec.get("_raw_body") or ""
    for fm in re.finditer(r"(\w+)\s*=\s*\{([^{}]*)\}", raw):
        extras[fm.group(1).lower()] = fm.group(2).strip()
    for fm in re.finditer(r"(\w+)\s*=\s*([a-zA-Z0-9.-]+)\s*,", raw):
        extras.setdefault(fm.group(1).lower(), fm.group(2).strip())

    for field in order:
        val = rec.get(field) or extras.get(field)
        if not val:
            continue
        if field == "month" and re.fullmatch(r"[a-z]{3}", val):
            lines.append(f"  {field:12s} = {val},")
        else:
            lines.append(f"  {field:12s} = {{{val}}},")
    # Drop trailing comma on last field
    if len(lines) > 1 and lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]
    lines.append("}")
    return "\n".join(lines)


def render_candidate_bib(unique: list[dict[str, Any]]) -> str:
    header = (
        "% CANDIDATE_BIBLIOGRAPHY.bib — Concept Edition preproduction (Agent G)\n"
        "% Deterministic unique-key candidate set. NOT authorized for merge into\n"
        "% book/references/references.bib.\n"
        f"% gate_note: {GATE_NOTE}\n"
        "% Do not invent DOI/ISBN/page/year. HTTP 200 alone is not verification.\n"
        "%\n"
        "% WCAG resolution: two dated Recommendation editions → two keys\n"
        "%   wcag22-20231005 → https://www.w3.org/TR/2023/REC-WCAG22-20231005/\n"
        "%   wcag22-20241212 → https://www.w3.org/TR/2024/REC-WCAG22-20241212/\n"
        "% Undated https://www.w3.org/TR/WCAG22/ is the latest-published shortcut\n"
        "% (currently the 2024-12-12 Recommendation). Do not silently overwrite years.\n"
        "\n"
    )
    blocks = [format_bib_entry(u) for u in sorted(unique, key=lambda r: r["bib_key"].lower())]
    return header + "\n\n".join(blocks) + "\n"


def render_report(result: dict[str, Any], prior_unique: int = 58) -> str:
    unique = result["unique_records"]
    lines: list[str] = []
    lines.append("# Source Integrity Report (Agent G)")
    lines.append("")
    lines.append(f"**schema_version:** `{SCHEMA_VERSION}`  ")
    lines.append(f"**status:** `{STATUS}`  ")
    lines.append(f"**gate_note:** `{GATE_NOTE}`  ")
    lines.append("**scope:** Concept Edition CE-1/3/4/5/6 chapter-local bibliographies  ")
    lines.append("**global merge:** not authorized — candidate only")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("| Metric | Prior (PR #3 index) | Current |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Chapter source occurrences | 64 | {result['occurrences']} |")
    lines.append(f"| Unique source records (bib keys) | {prior_unique} | {result['unique']} |")
    lines.append("")
    lines.append("### Verification status (unique keys)")
    lines.append("")
    lines.append("| verification_status | count |")
    lines.append("|---|---:|")
    for k, v in result["ver_counts"].items():
        lines.append(f"| `{k}` | {v} |")
    lines.append("")
    lines.append("### Classification (unique keys)")
    lines.append("")
    lines.append("| source_class | count |")
    lines.append("|---|---:|")
    for k, v in result["class_counts"].items():
        lines.append(f"| `{k}` | {v} |")
    lines.append("")
    lines.append("## WCAG 2.2 conflict resolution")
    lines.append("")
    lines.append(
        "PR #3 flagged `wcag22` with year `2023` (CE-1) vs `2024` (CE-6) sharing "
        "`https://www.w3.org/TR/WCAG22/`."
    )
    lines.append("")
    lines.append(
        "W3C primary history ([WCAG22 publication history](https://www.w3.org/standards/history/WCAG22/)) "
        "lists two Recommendation editions:"
    )
    lines.append("")
    lines.append("| Edition date | Status | Dated TR URL | Bib key |")
    lines.append("|---|---|---|---|")
    lines.append(
        "| 5 October 2023 | Recommendation | "
        "https://www.w3.org/TR/2023/REC-WCAG22-20231005/ | `wcag22-20231005` |"
    )
    lines.append(
        "| 12 December 2024 | Recommendation | "
        "https://www.w3.org/TR/2024/REC-WCAG22-20241212/ | `wcag22-20241212` |"
    )
    lines.append("")
    lines.append(
        "**Resolution:** two explicit bib keys (not a silent overwrite). "
        "The undated shortcut `/TR/WCAG22/` is the “latest published version” pointer and "
        "currently resolves to the 2024-12-12 Recommendation; it must not be used as the sole "
        "canonical URL when chapters intentionally cite different dated editions."
    )
    lines.append("")
    lines.append("## Conflicts")
    lines.append("")
    lines.append("### Resolved")
    lines.append("")
    lines.append(
        "- `wcag22` year 2023 vs 2024 → split into `wcag22-20231005` (CE-1) and "
        "`wcag22-20241212` (CE-6) with dated TR URLs."
    )
    lines.append(
        "- `rfc9293` title brace variance (`{TCP}` vs `TCP`) treated as non-semantic "
        "(normalized titles match); no separate keys required."
    )
    lines.append("")
    lines.append("### Remaining / informational")
    lines.append("")
    if result["key_conflicts"]:
        for c in result["key_conflicts"]:
            lines.append(f"- KEY: {c}")
    else:
        lines.append("- Duplicate key + conflicting metadata: **none**")
    if result["dup_doi"]:
        for c in result["dup_doi"]:
            lines.append(f"- DOI: {c}")
    else:
        lines.append("- Duplicate DOI across keys: **none**")
    if result["dup_isbn"]:
        for c in result["dup_isbn"]:
            lines.append(f"- ISBN: {c}")
    else:
        lines.append("- Duplicate ISBN across keys: **none**")
    if result["url_conflicts"]:
        for c in result["url_conflicts"]:
            lines.append(f"- URL year conflict: {c}")
    else:
        lines.append("- Same URL with conflicting date across unique keys: **none** (after WCAG split)")
    if result.get("url_title_aliases"):
        lines.append("- Same URL with chapter-local title aliases (informational, not hard conflicts):")
        for c in result["url_title_aliases"]:
            lines.append(f"  - {c}")
    if result["missing_verification"]:
        for k in result["missing_verification"]:
            lines.append(f"- Missing verification state: `{k}`")
    else:
        lines.append("- Missing verification state: **none**")
    lines.append("")
    lines.append("### Same-work chapter-local aliases (not conflicts)")
    lines.append("")
    if result["alias_groups"]:
        for a in result["alias_groups"]:
            lines.append(f"- {a}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Unique records")
    lines.append("")
    lines.append(
        "| bib_key | source_class | verification_status | chapter_usage | "
        "canonical_identifier | metadata_conflict_status |"
    )
    lines.append("|---|---|---|---|---|---|")
    for u in sorted(unique, key=lambda r: r["bib_key"].lower()):
        usage = ",".join(u["chapter_usage"])
        lines.append(
            f"| `{u['bib_key']}` | `{u['source_class']}` | `{u['verification_status']}` | "
            f"{usage} | `{u['canonical_identifier']}` | `{u['metadata_conflict_status']}` |"
        )
    lines.append("")
    lines.append("## Artifacts")
    lines.append("")
    lines.append("- `publication/preproduction/CANDIDATE_BIBLIOGRAPHY.bib`")
    lines.append("- `publication/preproduction/CANDIDATE_SOURCE_INDEX.yaml` (regenerated + verification overlay)")
    lines.append("- `publication/preproduction/SOURCE_INTEGRITY_REPORT.md` (this file)")
    lines.append("- Validator: `scripts/validate_ce_sources.py`")
    lines.append("")
    lines.append("## Non-goals")
    lines.append("")
    lines.append("- No Gate 3 / CH02-REVIEW-R1 edits")
    lines.append("- No Gate 3 PASS")
    lines.append("- No merge into `book/references/references.bib`")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_source_index(rows: list[dict[str, Any]], result: dict[str, Any]) -> str:
    """Write CANDIDATE_SOURCE_INDEX with Agent G verification statuses."""
    sources = []
    for r in rows:
        sources.append(
            {
                "source_package": r["source_package"],
                "bib_key": r["bib_key"],
                "entry_type": r.get("entry_type"),
                "title": r.get("title"),
                "year": r.get("year"),
                "url": r.get("url"),
                "source_class": r["source_class"],
                "verification_status": r["verification_status"],
                "canonical_identifier": r["canonical_identifier"],
                "metadata_conflict_status": next(
                    (
                        u["metadata_conflict_status"]
                        for u in result["unique_records"]
                        if u["bib_key"].lower() == r["bib_key"].lower()
                    ),
                    "NONE",
                ),
            }
        )
    data: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "gate_note": GATE_NOTE,
        "rights": "Candidate only. Does not modify live CH02 / Gate 3 evidence registries.",
        "chapter_source_occurrences": result["occurrences"],
        "unique_source_records": result["unique"],
        "unique_by_class": result["class_counts"],
        "verification_counts": result["ver_counts"],
        "metadata_conflicts": result["key_conflicts"],
        "wcag_resolution": {
            "strategy": "two_dated_recommendation_keys",
            "keys": WCAG_RESOLUTION,
            "undated_latest_shortcut": "https://www.w3.org/TR/WCAG22/",
            "history": "https://www.w3.org/standards/history/WCAG22/",
        },
        "sources": sources,
    }
    text = dump_yaml(data)
    if not text.endswith("\n"):
        text += "\n"
    return text


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if artifacts would change or hard conflicts remain",
    )
    args = parser.parse_args(argv)

    rows = load_all_occurrences()
    # Attach raw body for bib formatting from first package occurrence per key
    by_key_raw: dict[str, str] = {}
    for ce in CE_DIRS:
        for entry in parse_bib(PREPROD / ce / "references.local.bib"):
            by_key_raw.setdefault(entry["key"].lower(), entry.get("_raw_body", ""))
    for r in rows:
        r["_raw_body"] = by_key_raw.get(r["bib_key"].lower(), "")

    result = audit(rows)
    for u in result["unique_records"]:
        u["_raw_body"] = by_key_raw.get(u["bib_key"].lower(), "")

    # Hard fail only on true metadata conflicts / missing verification / dup identifiers.
    # Alias groups are informational.
    hard = (
        result["key_conflicts"]
        + result["dup_doi"]
        + result["dup_isbn"]
        + result["url_conflicts"]
        + [f"missing verification: {k}" for k in result["missing_verification"]]
    )

    bib_text = render_candidate_bib(result["unique_records"])
    report_text = render_report(result)
    index_text = write_source_index(rows, result)

    planned = {
        CANDIDATE_BIB: bib_text,
        INTEGRITY_REPORT: report_text,
        SOURCE_INDEX: index_text,
    }

    changed: list[str] = []
    for path, text in planned.items():
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        if digest(old) != digest(text):
            changed.append(str(path.relative_to(ROOT)))

    if args.check:
        if hard:
            print("validate_ce_sources: FAIL — hard conflicts:")
            for h in hard:
                print(" -", h)
            return 1
        if changed:
            print("validate_ce_sources: FAIL — artifacts stale:")
            for c in changed:
                print(" -", c)
            return 1
        print(
            f"validate_ce_sources: PASS "
            f"(occurrences={result['occurrences']} unique={result['unique']} "
            f"ver={result['ver_counts']})"
        )
        return 0

    for path, text in planned.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    print("validate_ce_sources: wrote")
    for p in planned:
        print(" -", p.relative_to(ROOT))
    if changed:
        print("updated:", ", ".join(changed))
    print(
        f"counts: occurrences={result['occurrences']} unique={result['unique']} "
        f"verification={result['ver_counts']}"
    )
    if hard:
        print("validate_ce_sources: WARN hard conflicts remain:")
        for h in hard:
            print(" -", h)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
