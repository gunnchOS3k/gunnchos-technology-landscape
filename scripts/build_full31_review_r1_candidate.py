#!/usr/bin/env python3
"""Build publication/review-candidates/FULL31-REVIEW-R1/ human-review freeze.

FULL31-REVIEW-R1 — HUMAN REVIEW CANDIDATE
NO HUMAN VALIDATION HAS OCCURRED
NOT PUBLICATION-READY

Does not overwrite FULL31-PRE-REVIEW-001.
Does not fabricate responses.
Does not mark Gate 3 PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "publication/review-candidates/FULL31-REVIEW-R1"
QUALITY = ROOT / "publication/full31/quality"
PRE_REVIEW = ROOT / "publication/review-candidates/FULL31-PRE-REVIEW-001"
ACCEPTED_MAIN = "d511eec102c311f980eead2629175c09d2bf8a49"
RECORDED_WAIKE = "e97e74fc9bfb44b1cdc26b272dc4848264f15fe0"

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
    try:
        import urllib.request

        req = urllib.request.Request(
            "https://api.github.com/repos/gunnchOS3k/waike-research-ops/commits/main",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "full31-review-r1"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
            data = json.loads(resp.read().decode("utf-8"))
        sha = data.get("sha") or RECORDED_WAIKE
        return sha, "live GitHub API main tip"
    except Exception as exc:  # noqa: BLE001
        return RECORDED_WAIKE, f"fallback recorded SHA (live fetch failed: {exc})"


def chapter_manifest() -> dict[str, Any]:
    chapters = []
    for i in range(1, 32):
        cid = f"CH{i:02d}"
        path = ROOT / f"book/chapters/{cid.lower()}/chapter.md"
        meta = ROOT / f"book/chapters/{cid.lower()}/metadata.yaml"
        entry: dict[str, Any] = {
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
        "candidate_id": "FULL31-REVIEW-R1",
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
    return {
        "registry_path": str(reg_path.relative_to(ROOT)),
        "registry_sha256": sha256_file(reg_path) if reg_path.exists() else None,
        "figure_count": len(figs),
        "figures": figs,
    }


def artifact_manifest() -> dict[str, Any]:
    root = ROOT / "preview/full31"
    arts: dict[str, Any] = {}
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
            index = path / "index.html"
            arts[key] = {
                "path": str(path.relative_to(ROOT)),
                "index_sha256": sha256_file(index) if index.exists() else None,
                "present": True,
            }
        else:
            arts[key] = {"present": False, "path": str(path.relative_to(ROOT))}
    return {
        "candidate_id": "FULL31-REVIEW-R1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "artifacts": arts,
        "note": "Missing preview artifacts are recorded honestly; rebuild before recruiting if needed.",
    }


def front_back_manifest() -> dict[str, Any]:
    paths = [
        "book/_quarto.yml",
        "book/index.qmd",
        "book/references/references.bib",
        "glossary/glossary.yaml",
        "book/terminology.yaml",
    ]
    entries = []
    for rel in paths:
        p = ROOT / rel
        entries.append(
            {
                "path": rel,
                "exists": p.exists(),
                "sha256": sha256_file(p) if p.is_file() else None,
            }
        )
    return {"schema_version": 1, "entries": entries}


def known_issues_summary(qi: dict[str, Any]) -> str:
    summary = qi.get("summary") or {}
    lines = [
        "# Known issues summary — FULL31-REVIEW-R1",
        "",
        "```",
        "FULL31-REVIEW-R1",
        "HUMAN REVIEW CANDIDATE",
        "NO HUMAN VALIDATION HAS OCCURRED",
        "NOT PUBLICATION-READY",
        "```",
        "",
        f"- Registry SHA context: `{qi.get('git_sha')}`",
        f"- Total issues: **{summary.get('total')}**",
        f"- By severity: `{summary.get('by_severity')}`",
        f"- By status: `{summary.get('by_status')}`",
        f"- Open BLOCKER: **{summary.get('open_blocker')}**",
        f"- Open MAJOR: **{summary.get('open_major')}**",
        "",
        "## Deferred / open (not hidden)",
        "",
    ]
    issues = qi.get("issues") or []
    deferred = [
        i
        for i in issues
        if i.get("fix_status")
        in {"DEFERRED_HUMAN_REVIEW", "DEFERRED_PHYSICAL_EVIDENCE", "OPEN"}
    ]
    for i in deferred[:100]:
        lines.append(
            f"- `{i.get('issue_id')}` [{i.get('severity')}/{i.get('fix_status')}] "
            f"{str(i.get('finding') or '')[:160]}"
        )
    if len(deferred) > 100:
        lines.append(f"- … {len(deferred) - 100} more in QUALITY_ISSUES.yaml")
    lines += [
        "",
        "## Integrity reminders",
        "",
        "- HUMAN_VALIDATED = 0/31",
        "- PUBLICATION_READY = 0/31",
        "- GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING",
        "- NO_REVIEW_RESPONSES_YET",
        "",
    ]
    return "\n".join(lines)


def physical_pending_doc() -> str:
    cit = QUALITY / "CITATION_AUDIT.yaml"
    lab = QUALITY / "LAB_ACTIVITY_AUDIT.yaml"
    pp_claims = None
    surfaces: list[Any] = []
    if cit.exists():
        after = (load_yaml(cit) or {}).get("after_counts") or {}
        pp_claims = after.get("PHYSICAL_PENDING")
    if lab.exists():
        surfaces = (load_yaml(lab) or {}).get("physical_pending") or []
    lines = [
        "# Device Quartet — PHYSICAL_PENDING summary",
        "",
        "```",
        "FULL31-REVIEW-R1",
        "NO HUMAN VALIDATION HAS OCCURRED",
        "```",
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
        "Do not invent measurements.",
        "",
    ]
    return "\n".join(lines)


def tool_versions() -> dict[str, Any]:
    versions: dict[str, Any] = {"python": sys.version.split()[0]}
    for cmd, key in ((["quarto", "--version"], "quarto"), (["xelatex", "--version"], "xelatex")):
        try:
            out = subprocess.check_output(cmd, cwd=ROOT, text=True, stderr=subprocess.STDOUT)
            versions[key] = out.strip().splitlines()[0][:120]
        except Exception:  # noqa: BLE001
            versions[key] = "unavailable"
    return versions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--content-sha",
        default="",
        help="verified_candidate_content_sha (non-self-referential pin).",
    )
    parser.add_argument(
        "--accepted-main",
        default=ACCEPTED_MAIN,
        help="accepted_main_base_sha (PR #9 merge tip).",
    )
    args = parser.parse_args()

    if not PRE_REVIEW.is_dir():
        print("ERROR: historical FULL31-PRE-REVIEW-001 missing; refuse to proceed", file=sys.stderr)
        return 1

    qi_path = QUALITY / "QUALITY_ISSUES.yaml"
    qi = load_yaml(qi_path) or {} if qi_path.exists() else {}

    content_sha = (args.content_sha or "").strip() or git_sha()
    OUT.mkdir(parents=True, exist_ok=True)
    # Never write response trees here
    responses = OUT / "responses"
    if responses.exists() and any(responses.iterdir()):
        print("ERROR: responses/ must remain empty for freeze prep", file=sys.stderr)
        return 1
    responses.mkdir(exist_ok=True)
    (responses / ".gitkeep").write_text("", encoding="utf-8")

    (OUT / "SOURCE_COMMIT.txt").write_text(content_sha + "\n", encoding="utf-8")

    ch_man = chapter_manifest()
    ch_text = dump_yaml(ch_man)
    (OUT / "CHAPTER_MANIFEST.yaml").write_text(ch_text, encoding="utf-8")

    bib = ROOT / "book/references/references.bib"
    bib_hash = sha256_file(bib) if bib.exists() else "MISSING"
    (OUT / "BIBLIOGRAPHY_HASH.txt").write_text(
        f"{bib.relative_to(ROOT)}  sha256:{bib_hash}\n", encoding="utf-8"
    )

    fig_man = figure_manifest()
    fig_text = dump_yaml(fig_man)
    (OUT / "FIGURE_MANIFEST.yaml").write_text(fig_text, encoding="utf-8")

    lab_reg = ROOT / "labs/lab_registry.yaml"
    lab_hash = sha256_file(lab_reg) if lab_reg.exists() else "MISSING"
    (OUT / "LAB_REGISTRY_HASH.txt").write_text(
        f"{lab_reg.relative_to(ROOT)}  sha256:{lab_hash}\n", encoding="utf-8"
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

    fb = front_back_manifest()
    fb_text = dump_yaml(fb)
    (OUT / "FRONT_BACK_MATTER_MANIFEST.yaml").write_text(fb_text, encoding="utf-8")

    waike_sha, waike_note = live_waike_sha()
    (OUT / "WAIKE_SOURCE_SHA.txt").write_text(
        f"repo: gunnchOS3k/waike-research-ops\nref: main\n"
        f"sha: {waike_sha}\nmode: {waike_note}\n",
        encoding="utf-8",
    )

    (OUT / "DEVICE_QUARTET_PHYSICAL_PENDING.md").write_text(
        physical_pending_doc(), encoding="utf-8"
    )
    (OUT / "KNOWN_ISSUES_SUMMARY.md").write_text(known_issues_summary(qi), encoding="utf-8")
    art_text = dump_yaml(artifact_manifest())
    (OUT / "ARTIFACT_MANIFEST.yaml").write_text(art_text, encoding="utf-8")
    (OUT / "BUILD_TOOL_VERSIONS.yaml").write_text(
        dump_yaml(tool_versions()), encoding="utf-8"
    )

    qi_hash = sha256_file(qi_path) if qi_path.exists() else "MISSING"
    provenance = {
        "schema_version": 1,
        "candidate_id": "FULL31-REVIEW-R1",
        "verified_candidate_content_sha": content_sha,
        "accepted_main_base_sha": args.accepted_main,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "chapter_manifest_sha256": sha256_text(ch_text),
        "bibliography_sha256": bib_hash,
        "figure_manifest_sha256": sha256_text(fig_text),
        "lab_registry_sha256": lab_hash,
        "glossary_terminology_sha256": gloss_term_hash,
        "front_back_matter_sha256": sha256_text(fb_text),
        "waike_source_sha": waike_sha,
        "waike_verification_mode": waike_note,
        "quality_issues_sha256": qi_hash,
        "artifact_manifest_sha256": sha256_text(art_text),
        "human_validation_status": "NOT_RUN",
        "gate_3_status": "READER_EVIDENCE_PENDING",
        "publication_status": "NOT_PUBLICATION_READY",
        "response_count": 0,
        "historical_pre_review_candidate": "FULL31-PRE-REVIEW-001",
        "source_commit_policy": (
            "SOURCE_COMMIT.txt and verified_candidate_content_sha mean the commit "
            "containing manuscript/assets/QA being frozen. They intentionally differ "
            "from final HEAD when only provenance/review-infra metadata is pinned afterward."
        ),
        "labels": [
            "FULL31-REVIEW-R1",
            "HUMAN REVIEW CANDIDATE",
            "NO HUMAN VALIDATION HAS OCCURRED",
            "NOT PUBLICATION-READY",
        ],
    }
    (OUT / "CANDIDATE_PROVENANCE.yaml").write_text(dump_yaml(provenance), encoding="utf-8")

    readme = "\n".join(
        [
            "# FULL31-REVIEW-R1",
            "",
            "```",
            "FULL31-REVIEW-R1",
            "HUMAN REVIEW CANDIDATE",
            "NO HUMAN VALIDATION HAS OCCURRED",
            "NOT PUBLICATION-READY",
            "```",
            "",
            "First whole-book **human-review** candidate freeze.",
            "Historical automated candidate `FULL31-PRE-REVIEW-001` is preserved untouched.",
            "",
            f"- verified_candidate_content_sha: `{content_sha}`",
            f"- accepted_main_base_sha: `{args.accepted_main}`",
            f"- WAIKE source SHA: `{waike_sha}` ({waike_note})",
            f"- Chapters: **{ch_man.get('count')}**",
            "- HUMAN_VALIDATED = 0/31",
            "- GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING",
            "- NO_REVIEW_RESPONSES_YET",
            "",
            "## Contents",
            "",
            "- `CANDIDATE_PROVENANCE.yaml`",
            "- `SOURCE_COMMIT.txt`",
            "- `CHAPTER_MANIFEST.yaml`",
            "- `FRONT_BACK_MATTER_MANIFEST.yaml`",
            "- `BIBLIOGRAPHY_HASH.txt`",
            "- `FIGURE_MANIFEST.yaml`",
            "- `LAB_REGISTRY_HASH.txt`",
            "- `GLOSSARY_TERMINOLOGY_HASH.txt`",
            "- `WAIKE_SOURCE_SHA.txt`",
            "- `DEVICE_QUARTET_PHYSICAL_PENDING.md`",
            "- `KNOWN_ISSUES_SUMMARY.md`",
            "- `ARTIFACT_MANIFEST.yaml`",
            "- `BUILD_TOOL_VERSIONS.yaml`",
            "- `responses/` (empty — no fabricated responses)",
            "",
            "Reviewer packets live under `publication/reviews/` (forms, coverage, intake).",
            "",
        ]
    )
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    freeze_state = ROOT / "publication/review-candidates/FULL31_REVIEW_R1_STATUS.md"
    freeze_state.write_text(
        "\n".join(
            [
                "# FULL31_REVIEW_R1_STATUS",
                "",
                "```",
                "ADULT_FULL31_REVIEW_R1_READY_FOR_HUMAN_REVIEW",
                "NO HUMAN VALIDATION HAS OCCURRED",
                "HUMAN_VALIDATED = 0/31",
                "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING",
                "PUBLICATION_READY = 0/31",
                "NO_REVIEW_RESPONSES_YET",
                "```",
                "",
                f"- Candidate: `publication/review-candidates/FULL31-REVIEW-R1/`",
                f"- verified_candidate_content_sha: `{content_sha}`",
                f"- accepted_main_base_sha: `{args.accepted_main}`",
                "",
                "Ceiling only: candidate is frozen and ready for recruitment — not validated.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("build_full31_review_r1_candidate:")
    print(f"  wrote: {OUT.relative_to(ROOT)}")
    print(f"  verified_candidate_content_sha: {content_sha}")
    print(f"  chapters: {ch_man.get('count')}")
    print(f"  waike_sha: {waike_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
