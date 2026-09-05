#!/usr/bin/env python3
"""Build kids/review-candidates/KIDS-FAMILY-REVIEW-R1/ human-review freeze.

KIDS FULL FAMILY HUMAN REVIEW CANDIDATE
NOT CHILD-VALIDATED
NOT PUBLICATION-READY

Does not execute Stage 2.
Does not fabricate child or adult responses.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "kids/review-candidates/KIDS-FAMILY-REVIEW-R1"
BOOKS_ROOT = ROOT / "kids/books"
ACCEPTED_MAIN = "d511eec102c311f980eead2629175c09d2bf8a49"
RECORDED_WAIKE = "e97e74fc9bfb44b1cdc26b272dc4848264f15fe0"

BOOK_IDS = [
    "KIDS-BABY",
    "KIDS-TODDLER",
    "KIDS-PRESCHOOL",
    "KIDS-PREK",
    "KIDS-ELEM1",
    "KIDS-ELEM2",
]
SUBCANDIDATES = {
    "KIDS-BABY": "KIDS-BABY-R1",
    "KIDS-TODDLER": "KIDS-TODDLER-R1",
    "KIDS-PRESCHOOL": "KIDS-PRESCHOOL-R1",
    "KIDS-PREK": "KIDS-PREK-R1",
    "KIDS-ELEM1": "KIDS-ELEM1-R1",
    "KIDS-ELEM2": "KIDS-ELEM2-R1",
}

BOOK_FILES = [
    "BOOK_MANUSCRIPT.md",
    "UNIT_REGISTRY.yaml",
    "GLOSSARY.yaml",
    "CAREGIVER_EDUCATOR_NOTES.md",
    "ACCESSIBILITY_NOTES.md",
    "STANDARDS_TRACEABILITY.yaml",
    "MEDIA_EVIDENCE_TRACEABILITY.yaml",
    "FIGURE_PLAN.yaml",
    "ARTIFACT_MANIFEST.yaml",
    "BOOK_METADATA.yaml",
]

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


def figure_manifest_for_book(book_id: str) -> dict[str, Any]:
    book = BOOKS_ROOT / book_id
    plan_path = book / "FIGURE_PLAN.yaml"
    figs_dir = book / "figures"
    entries = []
    plan = load_yaml(plan_path) or {} if plan_path.exists() else {}
    for fig in plan.get("figures") or plan.get("figure_plan") or []:
        if not isinstance(fig, dict):
            continue
        fid = fig.get("figure_id") or fig.get("id")
        rel = fig.get("path") or fig.get("svg") or ""
        path = ROOT / rel if rel and not rel.startswith("/") else (figs_dir / Path(str(rel)).name if rel else None)
        if path is None or not path.is_file():
            # try figures/<id>.svg
            cand = figs_dir / f"{fid}.svg" if fid else None
            path = cand if cand and cand.is_file() else None
        entries.append(
            {
                "figure_id": fid,
                "path": str(path.relative_to(ROOT)) if path and path.is_file() else rel or None,
                "sha256": sha256_file(path) if path and path.is_file() else None,
            }
        )
    # Also hash physical SVGs for completeness
    svg_hashes = []
    if figs_dir.is_dir():
        for svg in sorted(figs_dir.glob("*.svg")):
            svg_hashes.append({"path": str(svg.relative_to(ROOT)), "sha256": sha256_file(svg)})
    return {
        "book_id": book_id,
        "plan_sha256": sha256_file(plan_path) if plan_path.exists() else None,
        "planned_figures": entries,
        "svg_files": svg_hashes,
        "svg_count": len(svg_hashes),
    }


def artifact_manifest_for_book(book_id: str) -> dict[str, Any]:
    builds = BOOKS_ROOT / book_id / "builds"
    arts: dict[str, Any] = {}
    if builds.is_dir():
        for p in sorted(builds.iterdir()):
            if p.is_file():
                arts[p.name] = {
                    "path": str(p.relative_to(ROOT)),
                    "sha256": sha256_file(p),
                    "bytes": p.stat().st_size,
                }
    return {"book_id": book_id, "artifacts": arts}


def freeze_book(book_id: str, out_dir: Path) -> dict[str, Any]:
    book = BOOKS_ROOT / book_id
    sub_id = SUBCANDIDATES[book_id]
    sub = out_dir / sub_id
    sub.mkdir(parents=True, exist_ok=True)

    file_hashes: dict[str, Any] = {}
    for name in BOOK_FILES:
        src = book / name
        if src.is_file():
            dest = sub / name
            dest.write_bytes(src.read_bytes())
            file_hashes[name] = sha256_file(src)
        else:
            file_hashes[name] = None

    fig_man = figure_manifest_for_book(book_id)
    fig_text = dump_yaml(fig_man)
    (sub / "FIGURE_MANIFEST.yaml").write_text(fig_text, encoding="utf-8")

    art_man = artifact_manifest_for_book(book_id)
    art_text = dump_yaml(art_man)
    (sub / "ARTIFACT_MANIFEST_FREEZE.yaml").write_text(art_text, encoding="utf-8")

    units = 0
    ureg = book / "UNIT_REGISTRY.yaml"
    if ureg.exists():
        u = load_yaml(ureg) or {}
        units = len(u.get("units") or u.get("unit_registry") or [])
        if units == 0 and isinstance(u.get("units_by_strand"), dict):
            for v in u["units_by_strand"].values():
                if isinstance(v, list):
                    units += len(v)

    meta = load_yaml(book / "BOOK_METADATA.yaml") or {} if (book / "BOOK_METADATA.yaml").exists() else {}

    provenance = {
        "subcandidate_id": sub_id,
        "book_id": book_id,
        "manuscript_sha256": file_hashes.get("BOOK_MANUSCRIPT.md"),
        "unit_registry_sha256": file_hashes.get("UNIT_REGISTRY.yaml"),
        "glossary_sha256": file_hashes.get("GLOSSARY.yaml"),
        "caregiver_educator_notes_sha256": file_hashes.get("CAREGIVER_EDUCATOR_NOTES.md"),
        "accessibility_notes_sha256": file_hashes.get("ACCESSIBILITY_NOTES.md"),
        "standards_traceability_sha256": file_hashes.get("STANDARDS_TRACEABILITY.yaml"),
        "media_evidence_sha256": file_hashes.get("MEDIA_EVIDENCE_TRACEABILITY.yaml"),
        "figure_manifest_sha256": sha256_text(fig_text),
        "artifact_manifest_sha256": sha256_text(art_text),
        "unit_count": units,
        "provisional_cast_state": meta.get("cast_state")
        or meta.get("character_state")
        or "PROVISIONAL_UNLOCKED",
        "final_art_state": meta.get("final_art_state") or "NOT_FINAL_ART",
        "child_validation_status": "NOT_RUN",
        "publication_status": "NOT_PUBLICATION_READY",
        "labels": [
            "KIDS FULL FAMILY HUMAN REVIEW CANDIDATE",
            "NOT CHILD-VALIDATED",
            "NOT PUBLICATION-READY",
        ],
    }
    (sub / "SUBCANDIDATE_PROVENANCE.yaml").write_text(dump_yaml(provenance), encoding="utf-8")
    (sub / "README.md").write_text(
        "\n".join(
            [
                f"# {sub_id}",
                "",
                "```",
                "KIDS FULL FAMILY HUMAN REVIEW CANDIDATE",
                "NOT CHILD-VALIDATED",
                "NOT PUBLICATION-READY",
                "```",
                "",
                f"- book_id: `{book_id}`",
                f"- units: {units}",
                f"- manuscript_sha256: `{provenance['manuscript_sha256']}`",
                "- Stage 2 child usability: NOT EXECUTED",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return provenance


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-sha", default="")
    parser.add_argument("--accepted-main", default=ACCEPTED_MAIN)
    args = parser.parse_args()

    content_sha = (args.content_sha or "").strip() or git_sha()
    OUT.mkdir(parents=True, exist_ok=True)
    responses = OUT / "responses"
    responses.mkdir(exist_ok=True)
    (responses / ".gitkeep").write_text("", encoding="utf-8")
    if any(p for p in responses.iterdir() if p.name != ".gitkeep"):
        print("ERROR: kids freeze responses/ must remain empty", file=sys.stderr)
        return 1

    (OUT / "SOURCE_COMMIT.txt").write_text(content_sha + "\n", encoding="utf-8")

    books_prov: dict[str, Any] = {}
    total_units = 0
    for book_id in BOOK_IDS:
        if not (BOOKS_ROOT / book_id).is_dir():
            print(f"ERROR: missing book {book_id}", file=sys.stderr)
            return 1
        bp = freeze_book(book_id, OUT)
        books_prov[book_id] = {
            "subcandidate_id": bp["subcandidate_id"],
            "manuscript_sha256": bp["manuscript_sha256"],
            "figure_manifest_sha256": bp["figure_manifest_sha256"],
            "standards_traceability_sha256": bp["standards_traceability_sha256"],
            "media_evidence_sha256": bp["media_evidence_sha256"],
            "artifact_manifest_sha256": bp["artifact_manifest_sha256"],
            "unit_count": bp["unit_count"],
        }
        total_units += int(bp["unit_count"] or 0)

    # Family-level shared artifacts
    family_files = {
        "family_continuity": ROOT / "kids/books/KIDS_SPIRAL_CONTINUITY_REPORT.md",
        "misconception_matrix": ROOT / "kids/books/KIDS_MISCONCEPTION_MATRIX.md",
        "global_standards_atlas": ROOT / "kids/standards/GLOBAL_STANDARDS_COVERAGE_REPORT.md",
        "child_media_evidence_register": ROOT / "kids/research/CHILD_MEDIA_RESEARCH_REPORT.md",
        "manuscript_inventory": ROOT / "kids/books/KIDS_MANUSCRIPT_INVENTORY.yaml",
        "character_bible": ROOT / "kids/characters/CHARACTER_BIBLE.md",
    }
    family_hashes: dict[str, Any] = {}
    shared = OUT / "family-shared"
    shared.mkdir(exist_ok=True)
    for key, path in family_files.items():
        if path.is_file():
            dest = shared / path.name
            dest.write_bytes(path.read_bytes())
            family_hashes[f"{key}_sha256"] = sha256_file(path)
        else:
            family_hashes[f"{key}_sha256"] = None

    cast_note = shared / "PROVISIONAL_CAST_STATE.md"
    cast_note.write_text(
        "\n".join(
            [
                "# Provisional cast / final-art state",
                "",
                "```",
                "PROVISIONAL_CAST_UNLOCKED",
                "FINAL_ART_NOT_LOCKED",
                "NOT CHILD-VALIDATED",
                "```",
                "",
                "Stage 1 reviewers must distinguish CONTENT/STRUCTURE, VISUAL-DIRECTION, and FINAL-ART findings.",
                "Owner Stage 2 decisions: `kids/review-candidates/KIDS_STAGE2_OWNER_DECISIONS.md`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    waike_path = ROOT / "kids/waike/KIDS_WAIKE_CROSSWALK.yaml"
    waike_sha = RECORDED_WAIKE
    if waike_path.exists():
        data = load_yaml(waike_path) or {}
        waike_sha = (
            (data.get("waike") or {}).get("waike_sha_reconfirmed")
            or data.get("waike_sha_reconfirmed")
            or RECORDED_WAIKE
        )
    (OUT / "WAIKE_SOURCE_SHA.txt").write_text(f"{waike_sha}\n", encoding="utf-8")

    provenance = {
        "schema_version": 1,
        "candidate_id": "KIDS-FAMILY-REVIEW-R1",
        "verified_candidate_content_sha": content_sha,
        "accepted_main_base_sha": args.accepted_main,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "books": books_prov,
        "book_count": len(BOOK_IDS),
        "unit_count_total": total_units,
        "family_continuity_sha256": family_hashes.get("family_continuity_sha256"),
        "misconception_matrix_sha256": family_hashes.get("misconception_matrix_sha256"),
        "global_standards_atlas_sha256": family_hashes.get("global_standards_atlas_sha256"),
        "child_media_evidence_register_sha256": family_hashes.get(
            "child_media_evidence_register_sha256"
        ),
        "manuscript_inventory_sha256": family_hashes.get("manuscript_inventory_sha256"),
        "waike_source_sha": waike_sha,
        "child_validation_status": "NOT_RUN",
        "publication_status": "NOT_PUBLICATION_READY",
        "stage_1_status": "READY_FOR_ADULT_REVIEW",
        "stage_2_status": "PROTOCOL_PREPARED_NOT_EXECUTED",
        "response_count": 0,
        "labels": [
            "KIDS FULL FAMILY HUMAN REVIEW CANDIDATE",
            "NOT CHILD-VALIDATED",
            "NOT PUBLICATION-READY",
            "NO_CHILD_VALIDATION_EVIDENCE",
            "NO_REVIEW_RESPONSES_YET",
        ],
        "source_commit_policy": (
            "SOURCE_COMMIT.txt / verified_candidate_content_sha pin manuscript family "
            "content being frozen; may differ from final HEAD after provenance-only commits."
        ),
    }
    (OUT / "CANDIDATE_PROVENANCE.yaml").write_text(dump_yaml(provenance), encoding="utf-8")

    (OUT / "README.md").write_text(
        "\n".join(
            [
                "# KIDS-FAMILY-REVIEW-R1",
                "",
                "```",
                "KIDS FULL FAMILY HUMAN REVIEW CANDIDATE",
                "NOT CHILD-VALIDATED",
                "NOT PUBLICATION-READY",
                "NO_CHILD_VALIDATION_EVIDENCE",
                "NO_REVIEW_RESPONSES_YET",
                "```",
                "",
                f"- verified_candidate_content_sha: `{content_sha}`",
                f"- accepted_main_base_sha: `{args.accepted_main}`",
                f"- books: **{len(BOOK_IDS)}/6**",
                f"- units: **{total_units}/42** (expected 42)",
                f"- WAIKE SHA: `{waike_sha}`",
                "- Stage 1 adult review: packets prepared (responses = 0)",
                "- Stage 2 child usability: protocol prepared, **NOT EXECUTED**",
                "",
                "## Subcandidates",
                "",
                *[f"- `{SUBCANDIDATES[b]}/`" for b in BOOK_IDS],
                "",
                "## Shared",
                "",
                "- `family-shared/`",
                "- `responses/` (empty)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    status = ROOT / "kids/review-candidates/KIDS_FAMILY_REVIEW_R1_STATUS.md"
    status.parent.mkdir(parents=True, exist_ok=True)
    status.write_text(
        "\n".join(
            [
                "# KIDS_FAMILY_REVIEW_R1_STATUS",
                "",
                "```",
                "KIDS_FULL_FAMILY_REVIEW_R1_READY_FOR_STAGE1_ADULT_REVIEW",
                "KIDS_CHILD_VALIDATION_PENDING",
                "NOT CHILD-VALIDATED",
                "NOT PUBLICATION-READY",
                "NO_CHILD_VALIDATION_EVIDENCE",
                "NO_REVIEW_RESPONSES_YET",
                "```",
                "",
                f"- Candidate: `kids/review-candidates/KIDS-FAMILY-REVIEW-R1/`",
                f"- verified_candidate_content_sha: `{content_sha}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("build_kids_family_review_r1_candidate:")
    print(f"  wrote: {OUT.relative_to(ROOT)}")
    print(f"  books: {len(BOOK_IDS)} units_total={total_units}")
    print(f"  verified_candidate_content_sha: {content_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
