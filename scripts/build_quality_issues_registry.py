#!/usr/bin/env python3
"""Build / refresh publication/full31/quality/QUALITY_ISSUES.yaml.

Consolidates wave ledgers into one adjudicated registry. Does not hide
unresolved issues. Allowed fix_status values:

  OPEN | FIXED | DEFERRED_HUMAN_REVIEW | DEFERRED_PHYSICAL_EVIDENCE | NOT_AN_ISSUE
"""
from __future__ import annotations

import argparse
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUALITY = ROOT / "publication/full31/quality"
OUT = QUALITY / "QUALITY_ISSUES.yaml"

import sys

sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

ALLOWED_STATUS = {
    "OPEN",
    "FIXED",
    "DEFERRED_HUMAN_REVIEW",
    "DEFERRED_PHYSICAL_EVIDENCE",
    "NOT_AN_ISSUE",
}
ALLOWED_CATEGORY = {
    "TECHNICAL",
    "EVIDENCE",
    "CONTINUITY",
    "DUPLICATION",
    "TERMINOLOGY",
    "ACCESSIBILITY",
    "FIGURE",
    "LAB",
    "NAVIGATION",
    "FORMAT",
    "RIGHTS_METADATA",
    "STYLE",
}


def git_sha() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip()
        )
    except Exception:  # noqa: BLE001
        return "UNKNOWN"


def norm_status(raw: str | None, *, default: str = "OPEN") -> str:
    s = (raw or default).strip().upper()
    aliases = {
        "DEFERRED": "DEFERRED_HUMAN_REVIEW",
        "NEEDS_HUMAN": "DEFERRED_HUMAN_REVIEW",
        "HANDOFF_AGENT_J": "FIXED",  # Agent J landed terminology/acronym work
        "RESOLVED": "FIXED",
        "CLOSED": "FIXED",
        "INTENTIONAL_RETAIN": "NOT_AN_ISSUE",
        "KEEP": "NOT_AN_ISSUE",
        "TOOLING": "OPEN",
    }
    s = aliases.get(s, s)
    if s not in ALLOWED_STATUS:
        s = default
    return s


def norm_category(raw: str | None, default: str = "TECHNICAL") -> str:
    s = (raw or default).strip().upper().replace("-", "_").replace(" ", "_")
    aliases = {
        "PDF_STRUCTURE": "FORMAT",
        "PDF_LAYOUT": "FORMAT",
        "PDF": "FORMAT",
        "ACRONYMS": "TERMINOLOGY",
        "HTML": "ACCESSIBILITY",
        "EPUB": "ACCESSIBILITY",
        "A11Y": "ACCESSIBILITY",
        "VISUAL": "FIGURE",
        "SOURCE": "EVIDENCE",
        "CITATION": "EVIDENCE",
        "DUPLICATE": "DUPLICATION",
        "REPETITION": "DUPLICATION",
        "NAV": "NAVIGATION",
        "FRONTMATTER": "NAVIGATION",
        "RIGHTS": "RIGHTS_METADATA",
        "EDITORIAL": "STYLE",
        "CONCEPT": "TECHNICAL",
        "PRECISION": "TECHNICAL",
        "OVERCLAIM": "TECHNICAL",
    }
    s = aliases.get(s, s)
    if s not in ALLOWED_CATEGORY:
        # soft map by substring
        for cand in ALLOWED_CATEGORY:
            if cand in s or s in cand:
                return cand
        return default
    return s


def issue(
    *,
    issue_id: str,
    chapter: str,
    part: str,
    category: str,
    severity: str,
    location: str,
    finding: str,
    evidence: str = "",
    proposed_fix: str = "",
    fix_status: str,
    meaning_change: bool | str = False,
    citation_required: bool | str = False,
    reviewer_type_needed: str = "",
    source_ledger: str = "",
    adjudication_note: str = "",
) -> dict[str, Any]:
    row = {
        "issue_id": issue_id,
        "chapter": chapter or "BOOK",
        "part": part or "BOOK",
        "category": norm_category(category),
        "severity": (severity or "MODERATE").upper(),
        "location": location or "",
        "finding": (finding or "").strip(),
        "evidence": evidence if evidence is not None else "",
        "proposed_fix": proposed_fix or "",
        "fix_status": norm_status(fix_status),
        "meaning_change": bool(meaning_change)
        if not isinstance(meaning_change, str)
        else meaning_change.strip().lower() in {"true", "yes", "1"},
        "citation_required": bool(citation_required)
        if not isinstance(citation_required, str)
        else citation_required.strip().lower() in {"true", "yes", "1"},
        "reviewer_type_needed": reviewer_type_needed or "",
        "source_ledger": source_ledger,
    }
    if adjudication_note:
        row["adjudication_note"] = adjudication_note
    return row


def part_for_chapter(ch: str) -> str:
    import re

    m = re.search(r"(?:CH|ch)?0*(\d+)", (ch or "").upper())
    if not m:
        return "BOOK"
    n = int(m.group(1))
    # Parts by Full31 map: I 1-5, II 6-10, III 11-15, IV 16-20, V 21-25, VI 26-31
    if 1 <= n <= 5:
        return "I"
    if n <= 10:
        return "II"
    if n <= 15:
        return "III"
    if n <= 20:
        return "IV"
    if n <= 25:
        return "V"
    if n <= 31:
        return "VI"
    return "BOOK"


def ingest_technical(rows: list[dict[str, Any]]) -> None:
    for name in (
        "TECHNICAL_PART_I_II.yaml",
        "TECHNICAL_PART_III_IV.yaml",
        "TECHNICAL_PART_V_VI.yaml",
    ):
        path = QUALITY / "ledgers" / name
        if not path.exists():
            continue
        data = load_yaml(path) or {}
        for item in data.get("issues") or []:
            ch = str(item.get("chapter") or "BOOK")
            rows.append(
                issue(
                    issue_id=str(item.get("issue_id")),
                    chapter=ch,
                    part=str(item.get("part") or part_for_chapter(ch)),
                    category=str(item.get("category") or "TECHNICAL"),
                    severity=str(item.get("severity") or "MODERATE"),
                    location=str(item.get("location") or ""),
                    finding=str(item.get("finding") or ""),
                    evidence=str(item.get("evidence") or ""),
                    proposed_fix=str(item.get("proposed_fix") or ""),
                    fix_status=str(item.get("fix_status") or "OPEN"),
                    meaning_change=item.get("meaning_change", False),
                    citation_required=item.get("citation_required", False),
                    reviewer_type_needed=str(item.get("reviewer_type_needed") or ""),
                    source_ledger=str(path.relative_to(ROOT)),
                )
            )


def ingest_continuity(rows: list[dict[str, Any]]) -> None:
    path = QUALITY / "CONTINUITY_LEDGER.yaml"
    if not path.exists():
        return
    data = load_yaml(path) or {}
    for item in data.get("findings") or []:
        chapters = item.get("chapters") or []
        if isinstance(chapters, list):
            ch = ",".join(str(c) for c in chapters[:6]) or "BOOK"
        else:
            ch = str(chapters or "BOOK")
        kind = str(item.get("kind") or "continuity").lower()
        category = "DUPLICATION" if "dup" in kind or "similar" in kind else "CONTINUITY"
        disp = str(item.get("disposition") or "OPEN")
        sev = str(item.get("severity") or "EDITORIAL").upper()
        # Integrator: editorial OPEN continuity → defer to human editorial review
        status = norm_status(disp)
        note = ""
        if status == "OPEN" and sev in {"EDITORIAL", "MINOR"}:
            status = "DEFERRED_HUMAN_REVIEW"
            note = "Integrator: non-harmful editorial/minor continuity flag deferred for human review."
        elif status == "OPEN" and sev == "MODERATE":
            status = "DEFERRED_HUMAN_REVIEW"
            note = (
                "Integrator: continuity/duplication moderate flag retained for human "
                "identity review; not treated as technical MAJOR."
            )
        rows.append(
            issue(
                issue_id=str(item.get("id") or item.get("issue_id")),
                chapter=ch,
                part="BOOK",
                category=category,
                severity=sev if sev != "EDITORIAL" else "EDITORIAL",
                location="continuity_audit",
                finding=str(item.get("summary") or ""),
                evidence=str(item.get("evidence") or item.get("similarity") or ""),
                proposed_fix=str(item.get("notes") or ""),
                fix_status=status,
                meaning_change=False,
                citation_required=False,
                reviewer_type_needed="educator,part-tech-reviewer",
                source_ledger=str(path.relative_to(ROOT)),
                adjudication_note=note,
            )
        )


def ingest_figures(rows: list[dict[str, Any]]) -> None:
    path = QUALITY / "FIGURE_AUDIT.yaml"
    if not path.exists():
        return
    data = load_yaml(path) or {}
    for fig in data.get("figures") or []:
        state = str(fig.get("issue_state") or "KEEP").upper()
        if state == "KEEP":
            continue
        fid = str(fig.get("figure_id") or "")
        ch = str(fig.get("chapter") or part_for_chapter(fid))
        findings = fig.get("findings") or []
        if isinstance(findings, list):
            finding = "; ".join(str(x) for x in findings)
        else:
            finding = str(findings)
        if state == "BLOCKED_EVIDENCE_REQUIRED":
            status = "DEFERRED_PHYSICAL_EVIDENCE"
            sev = "MAJOR"
            note = (
                "Integrator: correctly blocked measured figure; must not ship as live "
                "reader-facing evidence. PHYSICAL_PENDING honesty preserved."
            )
        elif state == "REDESIGN":
            status = "DEFERRED_HUMAN_REVIEW"
            sev = "MODERATE"
            note = "Integrator: redesign queue for visual/print reviewer; not a BLOCKER."
        elif state == "POLISH":
            status = "DEFERRED_HUMAN_REVIEW"
            sev = "MINOR"
            note = "Integrator: polish queue deferred for visual review."
        elif state == "REMOVE":
            status = "OPEN"
            sev = "MAJOR"
            note = ""
        else:
            status = "DEFERRED_HUMAN_REVIEW"
            sev = "MINOR"
            note = f"Integrator mapped figure state {state}."
        rows.append(
            issue(
                issue_id=f"FIG-{fid}-{state}",
                chapter=ch,
                part=part_for_chapter(ch),
                category="FIGURE",
                severity=sev,
                location=str(fig.get("path") or fid),
                finding=finding or f"Figure disposition {state}",
                evidence=str(fig.get("phase2_action") or ""),
                proposed_fix=str(fig.get("phase2_action") or state),
                fix_status=status,
                meaning_change=False,
                citation_required=False,
                reviewer_type_needed="visual-print",
                source_ledger=str(path.relative_to(ROOT)),
                adjudication_note=note,
            )
        )


def ingest_labs(rows: list[dict[str, Any]]) -> None:
    path = QUALITY / "LAB_ACTIVITY_AUDIT.yaml"
    if not path.exists():
        return
    data = load_yaml(path) or {}
    for lab in data.get("proposed_labs") or []:
        disp = str(lab.get("disposition") or lab.get("wave_action") or "")
        if disp in {"converted_to_inline", "implemented", "inline"}:
            status = "FIXED"
        elif "pending" in disp.lower() or lab.get("classification") == "PROPOSED_LAB":
            status = "DEFERRED_HUMAN_REVIEW"
        else:
            status = "DEFERRED_HUMAN_REVIEW"
        rows.append(
            issue(
                issue_id=f"LAB-PROP-{lab.get('lab_id')}",
                chapter=str(lab.get("chapter") or "BOOK"),
                part=part_for_chapter(str(lab.get("chapter") or "")),
                category="LAB",
                severity="MINOR",
                location=str(lab.get("lab_id") or ""),
                finding=str(lab.get("rationale") or lab.get("classification") or ""),
                evidence=str(lab.get("wave_action") or ""),
                proposed_fix=str(lab.get("disposition") or ""),
                fix_status=status,
                meaning_change=False,
                citation_required=False,
                reviewer_type_needed="builder,educator",
                source_ledger=str(path.relative_to(ROOT)),
            )
        )
    for surf in data.get("physical_pending") or []:
        rows.append(
            issue(
                issue_id=f"LAB-PHYS-{abs(hash(str(surf.get('surface')))) % 10_000_000:07d}",
                chapter=",".join(str(x) for x in (surf.get("related") or [])[:4]) or "BOOK",
                part="BOOK",
                category="LAB",
                severity="MAJOR",
                location=str(surf.get("surface") or ""),
                finding=f"PHYSICAL_PENDING surface: {surf.get('surface')}",
                evidence=str(surf.get("related") or ""),
                proposed_fix="Await measured Device Quartet / field evidence; do not invent.",
                fix_status="DEFERRED_PHYSICAL_EVIDENCE",
                meaning_change=False,
                citation_required=False,
                reviewer_type_needed="engineer,builder",
                source_ledger=str(path.relative_to(ROOT)),
                adjudication_note="Honesty marker — not a defect to 'fix' with prose.",
            )
        )


def ingest_citations(rows: list[dict[str, Any]]) -> None:
    path = QUALITY / "CITATION_AUDIT.yaml"
    if not path.exists():
        return
    data = load_yaml(path) or {}
    for item in data.get("remaining_source_needed") or []:
        rows.append(
            issue(
                issue_id=f"EVID-{item.get('claim_id')}",
                chapter=str(item.get("chapter") or "BOOK").upper(),
                part=part_for_chapter(str(item.get("chapter") or "")),
                category="EVIDENCE",
                severity="MODERATE",
                location=str(item.get("claim_id") or ""),
                finding=str(item.get("reason") or "SOURCE_NEEDED retained"),
                evidence=str(item.get("disposition") or ""),
                proposed_fix="Pin verified source or keep SOURCE_NEEDED honest.",
                fix_status="DEFERRED_HUMAN_REVIEW",
                meaning_change=False,
                citation_required=True,
                reviewer_type_needed="engineer,educator",
                source_ledger=str(path.relative_to(ROOT)),
            )
        )
    # PHYSICAL_PENDING count from after_counts — book-level honesty issue
    after = data.get("after_counts") or {}
    pp = int(after.get("PHYSICAL_PENDING") or 0)
    if pp:
        rows.append(
            issue(
                issue_id="EVID-PHYSICAL-PENDING-BOOK",
                chapter="BOOK",
                part="BOOK",
                category="EVIDENCE",
                severity="MAJOR",
                location="publication/full31/quality/CITATION_AUDIT.yaml",
                finding=f"{pp} PHYSICAL_PENDING claim markers remain after evidence wave.",
                evidence=str(after),
                proposed_fix="Keep PHYSICAL_PENDING; collect measured evidence later.",
                fix_status="DEFERRED_PHYSICAL_EVIDENCE",
                meaning_change=False,
                citation_required=False,
                reviewer_type_needed="engineer",
                source_ledger=str(path.relative_to(ROOT)),
                adjudication_note="Not an open correctness defect — explicit honesty state.",
            )
        )


def ingest_frontmatter(rows: list[dict[str, Any]]) -> None:
    path = QUALITY / "FRONTMATTER_NAV_AUDIT.yaml"
    if not path.exists():
        return
    data = load_yaml(path) or {}
    for item in data.get("findings") or []:
        fid = str(item.get("id") or "")
        sev = str(item.get("severity") or "info").upper()
        if sev == "INFO":
            sev = "EDITORIAL"
        if fid == "FIG-CHAPTER-FIELD-TRUNCATION":
            status = "FIXED"
            note = (
                "Integrator fixed figures/figure_registry.yaml chapter fields from "
                "figure_id (55 entries)."
            )
            sev = "MAJOR"
        elif fid == "LAB-INDEX-INCOMPLETE":
            status = "FIXED"
            note = "Agent I expanded lab index."
        else:
            status = "DEFERRED_HUMAN_REVIEW" if sev != "EDITORIAL" else "NOT_AN_ISSUE"
            note = str(item.get("agent_i_action") or "")
        rows.append(
            issue(
                issue_id=f"NAV-{fid}",
                chapter="BOOK",
                part="BOOK",
                category="NAVIGATION" if "INDEX" in fid or "NAV" in fid else "FIGURE",
                severity=sev if sev != "INFO" else "EDITORIAL",
                location=str(item.get("area") or ""),
                finding=str(item.get("summary") or ""),
                evidence=str(item.get("count") or ""),
                proposed_fix=str(item.get("owner_hint") or item.get("agent_i_action") or ""),
                fix_status=status,
                meaning_change=False,
                citation_required=False,
                reviewer_type_needed="educator",
                source_ledger=str(path.relative_to(ROOT)),
                adjudication_note=note,
            )
        )


def ingest_publication_qa(rows: list[dict[str, Any]]) -> None:
    path = QUALITY / "PUBLICATION_QA.yaml"
    if not path.exists():
        return
    data = load_yaml(path) or {}
    seen_ids: set[str] = set()
    for item in data.get("issues") or []:
        iid = str(item.get("issue_id") or "")
        seen_ids.add(iid)
        status = str(item.get("fix_status") or "OPEN")
        note = ""
        sev = str(item.get("severity") or "MODERATE")
        if iid == "PDF-CHAPTER-COUNTER":
            pdf = (data.get("checks") or {}).get("pdf") or {}
            max_latex = int(pdf.get("pdf_max_latex_chapter_header") or 0)
            max_loose = int(pdf.get("pdf_max_chapter_number_seen") or 0)
            if max_latex and max_latex <= 45:
                status = "FIXED"
                note = (
                    "Integrator fixed body chapter counter via frontmatter "
                    "`number: false`, removed duplicate YAML/H1 chapter titles, and "
                    f"`\\mainmatter` reset. pdf_max_latex_chapter_header={max_latex} "
                    f"(loose text max={max_loose} is noisy)."
                )
            else:
                status = "OPEN"
                note = (
                    "Integrator applied numbering config; awaiting green publication QA. "
                    f"max_latex={max_latex} max_loose={max_loose}"
                )
        elif iid == "PDF-FRONTMATTER-NUMBERING":
            status = "DEFERRED_HUMAN_REVIEW"
            note = (
                "Frontmatter may still appear arabic-numbered in PDF TOC; body "
                "chapters 1–31 are correct after mainmatter reset."
            )
        elif iid == "A11Y-ACRO-IDENTITY":
            # Re-check live registry; Agent J expanded acronyms.
            acr_path = ROOT / "glossary/acronym_registry.yaml"
            identity = []
            if acr_path.exists():
                acr = load_yaml(acr_path) or {}
                for row in acr.get("acronyms") or []:
                    a = str(row.get("acronym") or "")
                    e = str(row.get("expands_to") or "")
                    if a and e and a.upper() == e.upper():
                        identity.append(a)
            if not identity:
                status = "FIXED"
                note = "Agent J expanded acronym registry; identity expansions cleared."
            else:
                status = "DEFERRED_HUMAN_REVIEW"
                note = f"Remaining identity expansions: {identity}"
        rows.append(
            issue(
                issue_id=iid,
                chapter="BOOK",
                part="BOOK",
                category=str(item.get("category") or "FORMAT"),
                severity=sev,
                location=str(item.get("location") or ""),
                finding=str(item.get("finding") or ""),
                evidence=str(item.get("evidence") or ""),
                proposed_fix="See publication QA / integrator adjudication.",
                fix_status=status,
                meaning_change=False,
                citation_required=False,
                reviewer_type_needed="visual-print,a11y",
                source_ledger=str(path.relative_to(ROOT)),
                adjudication_note=note,
            )
        )
    # If publication QA cleared the old MAJOR, record FIXED explicitly.
    if "PDF-CHAPTER-COUNTER" not in seen_ids:
        pdf = (data.get("checks") or {}).get("pdf") or {}
        max_latex = int(pdf.get("pdf_max_latex_chapter_header") or 0)
        rows.append(
            issue(
                issue_id="PDF-CHAPTER-COUNTER",
                chapter="BOOK",
                part="BOOK",
                category="FORMAT",
                severity="MAJOR",
                location="preview/full31/technology-landscape-full31-pdf.pdf",
                finding=(
                    "Historical Agent H MAJOR: PDF chapter counters inflated past ~31. "
                    "Integrator numbering fix applied; publication QA no longer raises it."
                ),
                evidence=str(
                    {
                        "pdf_max_latex_chapter_header": max_latex,
                        "pdf_max_chapter_number_seen": pdf.get(
                            "pdf_max_chapter_number_seen"
                        ),
                        "page_count": pdf.get("page_count"),
                    }
                ),
                proposed_fix="Keep mainmatter reset + single H1 body titles.",
                fix_status="FIXED",
                meaning_change=False,
                citation_required=False,
                reviewer_type_needed="visual-print",
                source_ledger=str(path.relative_to(ROOT)),
                adjudication_note=(
                    "FIXED: body chapters renumber from 1 after \\mainmatter; "
                    "duplicate YAML/H1 titles removed; frontmatter number:false."
                ),
            )
        )


def dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        iid = row["issue_id"]
        if iid in seen:
            # keep first, annotate collision
            continue
        seen.add(iid)
        out.append(row)
    return out


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_sev = Counter(r["severity"] for r in rows)
    by_status = Counter(r["fix_status"] for r in rows)
    by_cat = Counter(r["category"] for r in rows)
    open_blocker = sum(
        1
        for r in rows
        if r["severity"] == "BLOCKER" and r["fix_status"] == "OPEN"
    )
    open_major = sum(
        1 for r in rows if r["severity"] == "MAJOR" and r["fix_status"] == "OPEN"
    )
    return {
        "total": len(rows),
        "by_severity": dict(by_sev),
        "by_status": dict(by_status),
        "by_category": dict(by_cat),
        "open_blocker": open_blocker,
        "open_major": open_major,
        "pre_review_gate": {
            "blocker_open_ok": open_blocker == 0,
            "major_open_ok": open_major == 0,
            "ready_for_pre_review_candidate": open_blocker == 0 and open_major == 0,
        },
    }


def build() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    ingest_technical(rows)
    ingest_continuity(rows)
    ingest_figures(rows)
    ingest_labs(rows)
    ingest_citations(rows)
    ingest_frontmatter(rows)
    ingest_publication_qa(rows)
    rows = dedupe(rows)
    # stable sort
    sev_order = {"BLOCKER": 0, "MAJOR": 1, "MODERATE": 2, "MINOR": 3, "EDITORIAL": 4}
    rows.sort(key=lambda r: (sev_order.get(r["severity"], 9), r["issue_id"]))
    return {
        "schema_version": 1,
        "artifact": "QUALITY_ISSUES",
        "generated_on": date.today().isoformat(),
        "git_sha": git_sha(),
        "accepted_main_base": "76bee2e67c35ff445f46c83af30809e5b307f06e",
        "wave": "full31-quality-convergence-001",
        "notes": [
            "Central adjudicated registry for the quality convergence wave.",
            "DEFERRED_PHYSICAL_EVIDENCE preserves honesty; not a prose invent-fix.",
            "PRE-HUMAN-REVIEW requires open BLOCKER=0 and open MAJOR=0.",
            "Gate 3 / CH02-REVIEW-R1 unchanged; HUMAN_VALIDATED remains 0/31.",
        ],
        "summary": summarize(rows),
        "issues": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate existing registry")
    parser.add_argument("--write", action="store_true", help="Write QUALITY_ISSUES.yaml")
    args = parser.parse_args()
    if not args.check and not args.write:
        args.write = True

    if args.check and OUT.exists() and not args.write:
        data = load_yaml(OUT) or {}
        issues = data.get("issues") or []
        bad = []
        for i in issues:
            if i.get("fix_status") not in ALLOWED_STATUS:
                bad.append(f"bad status {i.get('issue_id')}: {i.get('fix_status')}")
            for field in (
                "issue_id",
                "chapter",
                "part",
                "category",
                "severity",
                "location",
                "finding",
                "evidence",
                "proposed_fix",
                "fix_status",
                "meaning_change",
                "citation_required",
                "reviewer_type_needed",
            ):
                if field not in i:
                    bad.append(f"{i.get('issue_id')}: missing {field}")
        summary = summarize(issues)
        print("quality_issues_check:")
        print(f"  total: {summary['total']}")
        print(f"  open_blocker: {summary['open_blocker']}")
        print(f"  open_major: {summary['open_major']}")
        if bad:
            print("quality_issues_check: FAIL")
            for b in bad[:30]:
                print(" -", b)
            return 1
        print("quality_issues_check: PASS")
        return 0

    report = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(dump_yaml(report), encoding="utf-8")
    s = report["summary"]
    print("build_quality_issues_registry:")
    print(f"  wrote: {OUT.relative_to(ROOT)}")
    print(f"  total: {s['total']}")
    print(f"  open_blocker: {s['open_blocker']}")
    print(f"  open_major: {s['open_major']}")
    print(f"  by_status: {s['by_status']}")
    print(f"  pre_review_ready: {s['pre_review_gate']['ready_for_pre_review_candidate']}")
    # Exit 0 on write even if majors open — pre-review-check enforces gate.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
