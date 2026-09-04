#!/usr/bin/env python3
"""Build publication/review-candidates/FULL31-PRE-REVIEW-001 package.

PRE-HUMAN-REVIEW CANDIDATE — NO HUMAN VALIDATION HAS OCCURRED.
Does not create FULL31-REVIEW-R1. Does not modify Gate 3.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "publication/review-candidates/FULL31-PRE-REVIEW-001"
QUALITY = ROOT / "publication/full31/quality"
ACCEPTED_MAIN = "76bee2e67c35ff445f46c83af30809e5b307f06e"

sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def live_waike_sha() -> tuple[str, str]:
    """Return (sha, note). Prefer live GitHub main; fall back to recorded."""
    recorded = "e97e74fc9bfb44b1cdc26b272dc4848264f15fe0"
    try:
        import urllib.request

        req = urllib.request.Request(
            "https://api.github.com/repos/gunnchOS3k/waike-research-ops/commits/main",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "full31-integrator"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
            data = json.loads(resp.read().decode("utf-8"))
        sha = data.get("sha") or recorded
        return sha, "live GitHub API main tip"
    except Exception as exc:  # noqa: BLE001
        return recorded, f"fallback recorded SHA (live fetch failed: {exc})"


def chapter_manifest() -> dict[str, Any]:
    chapters = []
    for i in range(1, 32):
        cid = f"CH{i:02d}"
        path = ROOT / f"book/chapters/{cid.lower()}/chapter.md"
        meta = ROOT / f"book/chapters/{cid.lower()}/metadata.yaml"
        entry = {
            "chapter_id": cid,
            "path": str(path.relative_to(ROOT)),
            "exists": path.exists(),
            "sha256": sha256_file(path) if path.exists() else None,
            "metadata_sha256": sha256_file(meta) if meta.exists() else None,
        }
        if meta.exists():
            m = load_yaml(meta) or {}
            entry["title"] = m.get("title")
            entry["status"] = m.get("status")
        chapters.append(entry)
    return {
        "schema_version": 1,
        "count": len(chapters),
        "working_drafts_expected": 31,
        "chapters": chapters,
    }


def figure_manifest() -> dict[str, Any]:
    reg_path = ROOT / "figures/figure_registry.yaml"
    data = load_yaml(reg_path) or {}
    figs = []
    for fig in data.get("figures") or []:
        path = ROOT / str(fig.get("path") or "")
        figs.append(
            {
                "figure_id": fig.get("figure_id"),
                "chapter": fig.get("chapter"),
                "path": fig.get("path"),
                "status": fig.get("status"),
                "sha256": sha256_file(path) if path.is_file() else None,
            }
        )
    audit = QUALITY / "FIGURE_AUDIT.yaml"
    states: dict[str, int] = {}
    if audit.exists():
        a = load_yaml(audit) or {}
        for f in a.get("figures") or []:
            st = str(f.get("issue_state") or "UNKNOWN")
            states[st] = states.get(st, 0) + 1
    return {
        "registry_path": str(reg_path.relative_to(ROOT)),
        "registry_sha256": sha256_file(reg_path),
        "figure_count": len(figs),
        "audit_issue_states": states,
        "figures": figs,
    }


def artifact_manifest() -> dict[str, Any]:
    root = ROOT / "preview/full31"
    arts = {}
    candidates = {
        "html_dir": root / "technology-landscape-full31-html",
        "pdf": root / "technology-landscape-full31-pdf.pdf",
        "epub": root / "technology-landscape-full31-epub.epub",
    }
    for key, path in candidates.items():
        if path.is_file():
            arts[key] = {
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        elif path.is_dir():
            # hash a stable listing + index if present
            index = path / "index.html"
            arts[key] = {
                "path": str(path.relative_to(ROOT)),
                "index_sha256": sha256_file(index) if index.exists() else None,
                "present": True,
            }
        else:
            arts[key] = {"present": False, "path": str(path.relative_to(ROOT))}
    return {"generated_on": date.today().isoformat(), "artifacts": arts}


def known_issues_summary(qi: dict[str, Any]) -> str:
    summary = qi.get("summary") or {}
    lines = [
        "# Known issues summary — FULL31-PRE-REVIEW-001",
        "",
        "> PRE-HUMAN-REVIEW CANDIDATE",
        "> NO HUMAN VALIDATION HAS OCCURRED",
        "",
        f"- Registry SHA context: `{qi.get('git_sha')}`",
        f"- Total issues: **{summary.get('total')}**",
        f"- By severity: `{summary.get('by_severity')}`",
        f"- By status: `{summary.get('by_status')}`",
        f"- Open BLOCKER: **{summary.get('open_blocker')}**",
        f"- Open MAJOR: **{summary.get('open_major')}**",
        "",
        "## Deferred (not hidden)",
        "",
    ]
    issues = qi.get("issues") or []
    deferred = [
        i
        for i in issues
        if i.get("fix_status")
        in {"DEFERRED_HUMAN_REVIEW", "DEFERRED_PHYSICAL_EVIDENCE", "OPEN"}
    ]
    for i in deferred[:80]:
        lines.append(
            f"- `{i.get('issue_id')}` [{i.get('severity')}/{i.get('fix_status')}] "
            f"{str(i.get('finding') or '')[:160]}"
        )
    if len(deferred) > 80:
        lines.append(f"- … {len(deferred) - 80} more deferred/open rows in QUALITY_ISSUES.yaml")
    lines += [
        "",
        "## Integrity reminders",
        "",
        "- HUMAN_VALIDATED = 0/31",
        "- PUBLICATION_READY = 0/31",
        "- GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING",
        "- Device Quartet quantities remain PHYSICAL_PENDING where marked",
        "",
    ]
    return "\n".join(lines)


def physical_pending_doc() -> str:
    cit = QUALITY / "CITATION_AUDIT.yaml"
    lab = QUALITY / "LAB_ACTIVITY_AUDIT.yaml"
    pp_claims = None
    surfaces = []
    if cit.exists():
        after = (load_yaml(cit) or {}).get("after_counts") or {}
        pp_claims = after.get("PHYSICAL_PENDING")
    if lab.exists():
        surfaces = (load_yaml(lab) or {}).get("physical_pending") or []
    lines = [
        "# Device Quartet — PHYSICAL_PENDING summary",
        "",
        "> PRE-HUMAN-REVIEW CANDIDATE",
        "> NO HUMAN VALIDATION HAS OCCURRED",
        "",
        "Research form factors (not shipping-product claims):",
        "",
        "- Student 14.5\" → sustained desk learning/work",
        "- Handheld Hybrid → mobile/docked compute",
        "- DS-XL Coder → strongest learn-to-build device",
        "- Edge IO Wearables → embodied sensing/haptics/HUD/safety",
        "",
        f"Claim-plan PHYSICAL_PENDING markers: **{pp_claims}**",
        "",
        "## Surfaces still awaiting measured evidence",
        "",
    ]
    for s in surfaces:
        lines.append(f"- {s.get('surface')} — related: {s.get('related')}")
    if not surfaces:
        lines.append("- (see citation audit / lab audit for markers)")
    lines += [
        "",
        "Do not invent measurements. Do not convert research form factors into shipping SKUs.",
        "",
    ]
    return "\n".join(lines)


def review_role_plan() -> str:
    roles = [
        ("Explorer", "Comprehension / orientation / teach-back of ordinary-language paths"),
        ("Builder", "Lab/activity usability; modify-and-observe feasibility"),
        ("Engineer", "Technical correctness, precision, overclaim detection"),
        ("Educator", "Pathway fitness, sequencing, assessment fairness"),
        ("Part I/II technical reviewer", "CH01–CH10 domain depth"),
        ("Part III/IV technical reviewer", "CH11–CH20 systems/network depth"),
        ("Part V/VI technical reviewer", "CH21–CH31 AI/security/career/capstone depth"),
        ("Accessibility reviewer", "Semantic HTML/EPUB/PDF a11y — not auto-certified here"),
        ("Visual/print reviewer", "Figure pedagogy, print layout, page breaks, contrast"),
    ]
    lines = [
        "# Review role plan (forms/protocol stubs only)",
        "",
        "> PRE-HUMAN-REVIEW CANDIDATE",
        "> NO HUMAN VALIDATION HAS OCCURRED",
        "",
        "No responses are populated. No recruiting is performed in this wave.",
        "",
        "| Role | Focus | Form stub |",
        "|---|---|---|",
    ]
    for role, focus in roles:
        slug = role.lower().replace(" ", "-").replace("/", "-")
        lines.append(f"| {role} | {focus} | `forms/{slug}.md` |")
    lines += [
        "",
        "Protocol stub: `PROTOCOL.md` (requirements only).",
        "",
        "Historical CH02-REVIEW-R1 remains a Gate 3 snapshot and is **not** superseded by",
        "fabricated whole-book evidence. Future owner-approved freeze may create a",
        "whole-book human-review snapshot — **not** in this package.",
        "",
    ]
    return "\n".join(lines)


def write_form_stubs(forms_dir: Path) -> None:
    forms_dir.mkdir(parents=True, exist_ok=True)
    stubs = {
        "explorer.md": "Explorer",
        "builder.md": "Builder",
        "engineer.md": "Engineer",
        "educator.md": "Educator",
        "part-i-ii-technical-reviewer.md": "Part I/II technical reviewer",
        "part-iii-iv-technical-reviewer.md": "Part III/IV technical reviewer",
        "part-v-vi-technical-reviewer.md": "Part V/VI technical reviewer",
        "accessibility-reviewer.md": "Accessibility reviewer",
        "visual-print-reviewer.md": "Visual/print reviewer",
    }
    for fname, role in stubs.items():
        (forms_dir / fname).write_text(
            "\n".join(
                [
                    f"# {role} — review form stub",
                    "",
                    "> PRE-HUMAN-REVIEW CANDIDATE",
                    "> NO HUMAN VALIDATION HAS OCCURRED",
                    "",
                    "**Status:** empty form — do not populate in this wave.",
                    "",
                    "## Identity",
                    "",
                    "- Reviewer name: _unassigned_",
                    "- Date: _pending_",
                    "- Chapters in scope: _pending_",
                    "",
                    "## Findings",
                    "",
                    "_No responses._",
                    "",
                    "## Recommendation",
                    "",
                    "- [ ] Needs revision",
                    "- [ ] Conditionally acceptable after fixes",
                    "- [ ] Acceptable for next freeze (owner decision only)",
                    "",
                    "This stub is not evidence.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    (forms_dir.parent / "PROTOCOL.md").write_text(
        "\n".join(
            [
                "# Full31 pre-human-review protocol stub",
                "",
                "> PRE-HUMAN-REVIEW CANDIDATE",
                "> NO HUMAN VALIDATION HAS OCCURRED",
                "",
                "## Purpose",
                "",
                "Prepare recruitment-ready roles after automated convergence. This file is not Gate 3 evidence.",
                "",
                "## Rules",
                "",
                "1. Do not fabricate reader responses.",
                "2. Do not mark HUMAN_VALIDATED or PUBLICATION_READY from agent work.",
                "3. Preserve PHYSICAL_PENDING honesty.",
                "4. Keep CH02-REVIEW-R1 historical files unchanged.",
                "5. Recruit only after owner approval of this candidate package.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", default=True)
    parser.add_argument(
        "--content-sha",
        default="",
        help=(
            "verified_candidate_content_sha: commit containing converged manuscript/"
            "assets/QA before this provenance pin. Required for non-self-referential freeze."
        ),
    )
    args = parser.parse_args()
    if not args.write:
        return 0

    qi_path = QUALITY / "QUALITY_ISSUES.yaml"
    if not qi_path.exists():
        subprocess.check_call(
            [sys.executable, "scripts/build_quality_issues_registry.py", "--write"],
            cwd=ROOT,
        )
    qi = load_yaml(qi_path) or {}

    content_sha = (args.content_sha or "").strip() or git_sha()
    # SOURCE_COMMIT.txt is explicitly the verified candidate content SHA (not metadata HEAD).
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "SOURCE_COMMIT.txt").write_text(content_sha + "\n", encoding="utf-8")

    ch_man = chapter_manifest()
    ch_man_text = dump_yaml(ch_man)
    (OUT / "CHAPTER_MANIFEST.yaml").write_text(ch_man_text, encoding="utf-8")

    bib = ROOT / "book/references/references.bib"
    bib_hash = sha256_file(bib) if bib.exists() else "MISSING"
    (OUT / "BIBLIOGRAPHY_HASH.txt").write_text(
        f"{bib.relative_to(ROOT)}  sha256:{bib_hash}\n", encoding="utf-8"
    )

    fig_man = figure_manifest()
    fig_man_text = dump_yaml(fig_man)
    (OUT / "FIGURE_MANIFEST.yaml").write_text(fig_man_text, encoding="utf-8")

    lab_reg = ROOT / "labs/lab_registry.yaml"
    lab_hash = sha256_file(lab_reg) if lab_reg.exists() else "MISSING"
    (OUT / "LAB_REGISTRY_HASH.txt").write_text(
        f"{lab_reg.relative_to(ROOT)}  sha256:{lab_hash}\n",
        encoding="utf-8",
    )

    gloss = ROOT / "glossary/glossary.yaml"
    term = ROOT / "book/terminology.yaml"
    ghash = sha256_file(gloss) if gloss.exists() else "MISSING"
    thash = sha256_file(term) if term.exists() else "MISSING"
    combined = hashlib.sha256()
    if gloss.exists():
        combined.update(gloss.read_bytes())
    combined.update(b"\n")
    if term.exists():
        combined.update(term.read_bytes())
    gloss_term_hash = combined.hexdigest()
    (OUT / "GLOSSARY_TERMINOLOGY_HASH.txt").write_text(
        f"glossary/glossary.yaml  sha256:{ghash}\n"
        f"book/terminology.yaml  sha256:{thash}\n"
        f"combined_sha256:{gloss_term_hash}\n",
        encoding="utf-8",
    )

    waike_sha, waike_note = live_waike_sha()
    if "live" in waike_note.lower() and "fail" not in waike_note.lower():
        waike_line = (
            "WAIKE source SHA verified by integration:\n"
            f"{waike_sha}\n"
            f"mode: {waike_note}\n"
        )
    else:
        waike_line = (
            "recorded accepted-main WAIKE SHA:\n"
            f"{waike_sha}\n"
            "external live verification unavailable in this runtime\n"
            f"detail: {waike_note}\n"
        )
    (OUT / "WAIKE_SOURCE_SHA.txt").write_text(
        f"repo: gunnchOS3k/waike-research-ops\nref: main\n{waike_line}",
        encoding="utf-8",
    )

    (OUT / "DEVICE_QUARTET_PHYSICAL_PENDING.md").write_text(
        physical_pending_doc(), encoding="utf-8"
    )
    (OUT / "KNOWN_ISSUES_SUMMARY.md").write_text(known_issues_summary(qi), encoding="utf-8")
    art_text = dump_yaml(artifact_manifest())
    (OUT / "ARTIFACT_MANIFEST.yaml").write_text(art_text, encoding="utf-8")
    (OUT / "REVIEW_ROLE_PLAN.md").write_text(review_role_plan(), encoding="utf-8")
    write_form_stubs(OUT / "forms")

    qi_hash = sha256_file(qi_path) if qi_path.exists() else "MISSING"
    provenance = {
        "schema_version": 1,
        "candidate_id": "FULL31-PRE-REVIEW-001",
        "verified_candidate_content_sha": content_sha,
        "accepted_main_base_sha": ACCEPTED_MAIN,
        "generated_at": date.today().isoformat(),
        "human_validation_status": "NOT_RUN",
        "gate_3_status": "READER_EVIDENCE_PENDING",
        "publication_status": "NOT_PUBLICATION_READY",
        "waike_source_sha": waike_sha,
        "waike_verification_mode": waike_note,
        "chapter_manifest_sha256": sha256_text(ch_man_text),
        "bibliography_sha256": bib_hash,
        "figure_manifest_sha256": sha256_text(fig_man_text),
        "lab_registry_sha256": lab_hash,
        "glossary_terminology_sha256": gloss_term_hash,
        "quality_issues_sha256": qi_hash,
        "artifact_manifest_sha256": sha256_text(art_text),
        "source_commit_policy": (
            "SOURCE_COMMIT.txt and README verified_candidate_content_sha both mean "
            "the commit containing converged manuscript/assets/QA before the final "
            "provenance/report-only pin commit. They intentionally differ from final HEAD "
            "when only provenance metadata is pinned afterward."
        ),
    }
    (OUT / "CANDIDATE_PROVENANCE.yaml").write_text(
        dump_yaml(provenance), encoding="utf-8"
    )

    summary = qi.get("summary") or {}
    open_auto = sum(
        1 for i in (qi.get("issues") or []) if i.get("fix_status") == "OPEN"
    )
    ready = (
        summary.get("open_blocker", 1) == 0
        and summary.get("open_major", 1) == 0
        and open_auto == 0
        and ch_man.get("count") == 31
        and all(c.get("exists") for c in ch_man.get("chapters") or [])
    )
    state_path = ROOT / "publication/full31/FULL31_PRE_HUMAN_REVIEW_CANDIDATE.md"
    if ready:
        state_path.write_text(
            "\n".join(
                [
                    "# FULL31_PRE_HUMAN_REVIEW_CANDIDATE",
                    "",
                    "> PRE-HUMAN-REVIEW CANDIDATE",
                    "> NO HUMAN VALIDATION HAS OCCURRED",
                    "",
                    "Non-gate production state only. **Does not change Gate 3.**",
                    "",
                    f"- verified_candidate_content_sha: `{content_sha}`",
                    f"- Accepted main base: `{ACCEPTED_MAIN}`",
                    f"- Candidate package: `publication/review-candidates/FULL31-PRE-REVIEW-001/`",
                    f"- Open BLOCKER: {summary.get('open_blocker')}",
                    f"- Open MAJOR: {summary.get('open_major')}",
                    f"- Open automatable: {open_auto}",
                    "- HUMAN_VALIDATED: 0/31",
                    "- PUBLICATION_READY: 0/31",
                    "- GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING",
                    "",
                    "Criteria satisfied for automated pre-human-review candidacy only.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    elif state_path.exists():
        state_path.unlink()

    if "live" in waike_note.lower() and "fail" not in waike_note.lower():
        waike_readme = (
            f"- WAIKE source SHA verified by integration: `{waike_sha}`"
        )
    else:
        waike_readme = (
            f"- recorded accepted-main WAIKE SHA: `{waike_sha}` "
            "(external live verification unavailable in this runtime)"
        )

    readme = "\n".join(
        [
            "# FULL31-PRE-REVIEW-001",
            "",
            "```",
            "PRE-HUMAN-REVIEW CANDIDATE",
            "NO HUMAN VALIDATION HAS OCCURRED",
            "```",
            "",
            "This package freezes **automated** convergence inputs for later human review recruitment.",
            "It is **not** `FULL31-REVIEW-R1`, **not** Gate 3 evidence, and **not** publication-ready proof.",
            "",
            f"- verified_candidate_content_sha: `{content_sha}`",
            f"- SOURCE_COMMIT.txt: same verified candidate content SHA (not the metadata-only pin HEAD)",
            f"- Generated on: {date.today().isoformat()}",
            f"- QUALITY_ISSUES open BLOCKER: {summary.get('open_blocker')}",
            f"- QUALITY_ISSUES open MAJOR: {summary.get('open_major')}",
            f"- QUALITY_ISSUES open automatable: {open_auto}",
            waike_readme,
            "",
            "## Contents",
            "",
            "- `CANDIDATE_PROVENANCE.yaml`",
            "- `SOURCE_COMMIT.txt` (= verified_candidate_content_sha)",
            "- `CHAPTER_MANIFEST.yaml`",
            "- `BIBLIOGRAPHY_HASH.txt`",
            "- `FIGURE_MANIFEST.yaml`",
            "- `LAB_REGISTRY_HASH.txt`",
            "- `GLOSSARY_TERMINOLOGY_HASH.txt`",
            "- `WAIKE_SOURCE_SHA.txt`",
            "- `DEVICE_QUARTET_PHYSICAL_PENDING.md`",
            "- `KNOWN_ISSUES_SUMMARY.md`",
            "- `ARTIFACT_MANIFEST.yaml`",
            "- `REVIEW_ROLE_PLAN.md` + `forms/` + `PROTOCOL.md`",
            "",
            "## Rights",
            "",
            "- Manuscript prose / figures: All Rights Reserved",
            "- MIT only where scoped (scripts/CI/lab code samples)",
            "- No blanket CC license",
            "",
        ]
    )
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    print("build_full31_pre_review_candidate:")
    print(f"  wrote: {OUT.relative_to(ROOT)}")
    print(f"  verified_candidate_content_sha: {content_sha}")
    print(f"  waike_sha: {waike_sha}")
    print(f"  pre_review_state_doc: {ready}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
