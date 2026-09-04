#!/usr/bin/env python3
"""Assemble adult release packages from canonical FULL31 EPUB/PDF + print interiors.

Copies real typed bytes into release-packages/adult/*/artifacts/ where automation allows.
Does not invent ISBN, final cover art, or spine geometry. Does not upload.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from adult_package_common import (  # noqa: E402
    ADULT,
    REQUIRED_CHANNELS,
    eligibility_for_pages,
    sha256_file,
)

EPUB_SRC = ROOT / "preview" / "full31" / "technology-landscape-full31-epub.epub"
DIGITAL_PDF_SRC = ROOT / "preview" / "full31" / "technology-landscape-full31-pdf.pdf"
PRINT_SRC = {
    "6x9": ROOT / "preview" / "print" / "technology-landscape-print-6x9-interior.pdf",
    "7x10": ROOT / "preview" / "print" / "technology-landscape-print-7x10-interior.pdf",
    "8.5x11": ROOT / "preview" / "print" / "technology-landscape-print-85x11-interior.pdf",
}
ADULT_META = ROOT / "publication" / "metadata" / "adult-book.yaml"

FREEZE_SHA = "dd7f0003beae5c56d5ee8b5050aff151ef67d803"
TODAY = date.today().isoformat()

# Aggregate ceiling when automatable packaging/render complete.
AGGREGATE_STATE = "ADULT_AUTOMATED_DISTRIBUTION_PREP_COMPLETE"


def pdf_pages_dims(path: Path) -> tuple[int, float, float]:
    from pypdf import PdfReader

    r = PdfReader(str(path))
    b = r.pages[0].mediabox
    return len(r.pages), float(b.width) / 72.0, float(b.height) / 72.0


def write_checksums(pkg: Path, rel_paths: list[str]) -> None:
    lines = []
    for rel in sorted(rel_paths):
        target = pkg / rel
        if not target.is_file():
            continue
        lines.append(f"{sha256_file(target)}  {rel}")
    (pkg / "CHECKSUMS.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def dump_manifest(pkg: Path, data: dict) -> None:
    # Prefer stable key order for readability
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    (pkg / "MANIFEST.yaml").write_text(text, encoding="utf-8")


def ensure_stub(path: Path, platform: str, note: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "STUB_ONLY\n"
        f"platform={platform}\n"
        "replace_with_real_artifact\n"
        f"note={note}\n"
        f"retrieved_on={TODAY}\n",
        encoding="utf-8",
    )


def copy_real(src: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    # Remove legacy stub sibling once real bytes land (e.g. book.epub.STUB).
    stub_sibling = Path(str(dest) + ".STUB")
    if stub_sibling.exists():
        stub_sibling.unlink()
    shutil.copy2(src, dest)
    return sha256_file(dest)


def update_readme(pkg: Path, channel: str, readiness: str, notes: list[str]) -> None:
    path = pkg / "README.md"
    notes_block = "\n".join(f"- {n}" for n in notes)
    body = f"""# Adult release package — `{channel}`

**Package readiness:** `{readiness}`  
**Aggregate track state (when packaging complete):** `{AGGREGATE_STATE}`  
**Not:** `PUBLICATION_READY` · `READY_FOR_OWNER_UPLOAD` · not uploaded · no credentials · not Gate 3 PASS  
**HUMAN_VALIDATED:** 0/31

## Provenance (frozen; do not rewrite)

- FULL31 pre-review content SHA: `{FREEZE_SHA}`
- Candidate package: `publication/review-candidates/FULL31-PRE-REVIEW-001/`
- Gate 3: `GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING`

## Contents

| Path | Role |
| --- | --- |
| `MANIFEST.yaml` | Declared package files + readiness |
| `CHECKSUMS.sha256` | Hashes for present files |
| `validation-stub.md` | Automated checks that *could* run later |
| `HUMAN_CHECKLIST.md` | Human-only upload checklist — no secrets |
| `artifacts/` | Typed artifacts and/or owner-blocked stubs |

## Channel notes

{notes_block}

## Non-claims

- Do not actually upload from this package without owner approval.
- Cover technical proofs are **not** final marketing art.
- ISBN placeholders remain `PENDING_OWNER_PURCHASE`.
- Kindle Previewer is not automated here (`KINDLE_PREVIEWER_HUMAN_OR_EXTERNAL_PENDING` when applicable).
"""
    path.write_text(body, encoding="utf-8")


def build_library_metadata(dest: Path) -> None:
    stub_sibling = Path(str(dest) + ".STUB")
    if stub_sibling.exists():
        stub_sibling.unlink()
    meta = yaml.safe_load(ADULT_META.read_text(encoding="utf-8"))
    out = {
        "schema": "adult.library.metadata.stub_replacement/v1",
        "source": "publication/metadata/adult-book.yaml",
        "work_id": meta.get("work_id"),
        "title": meta.get("title"),
        "contributors": meta.get("contributors"),
        "language": meta.get("language"),
        "identifiers": meta.get("identifiers"),
        "subjects": meta.get("subjects"),
        "rights_statement": meta.get("rights_statement"),
        "isbn_state": "PENDING_OWNER_PURCHASE",
        "cover_state": "BLOCKED_OWNER_COVER",
        "not_status": "PUBLICATION_READY",
        "generated_on": TODAY,
    }
    dest.write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")


def build_channel(
    channel: str,
    *,
    readiness: str,
    platform_id: str,
    files_meta: list[dict],
    notes: list[str],
    extra_manifest: dict | None = None,
) -> None:
    pkg = ADULT / channel
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "artifacts").mkdir(exist_ok=True)

    file_paths = [f["path"] for f in files_meta] + [
        "HUMAN_CHECKLIST.md",
        "MANIFEST.yaml",
        "README.md",
        "validation-stub.md",
        "CHECKSUMS.sha256",
    ]
    # Unique preserve order
    seen = set()
    ordered = []
    for p in file_paths:
        if p not in seen:
            seen.add(p)
            ordered.append(p)

    update_readme(pkg, channel, readiness, notes)
    # Keep human checklist if present; ensure exists
    hc = pkg / "HUMAN_CHECKLIST.md"
    if not hc.is_file():
        hc.write_text(
            f"# Human-only checklist — `{channel}`\n\n"
            "Do **not** store passwords, API keys, tax IDs, or bank details in this repo.\n\n"
            "- [ ] Owner approval recorded before clicking Publish\n"
            "- [ ] Do not actually upload until ISBN/cover/human review cleared\n",
            encoding="utf-8",
        )

    vs = pkg / "validation-stub.md"
    vs.write_text(
        f"# Validation notes — `{channel}`\n\n"
        "Automated (repo-side) checks:\n\n"
        "1. `make adult-release-package-check` / `make adult-artifact-package-check`\n"
        "2. `make distribution-requirements-check`\n"
        "3. `make full31-epubcheck` (when EPUB present)\n"
        "4. `make full31-pre-review-check` — freeze candidacy unchanged\n\n"
        "Not included: live retailer ingestion, WCAG certification, Kindle Previewer automation,\n"
        "human accessibility audit, ISBN purchase.\n",
        encoding="utf-8",
    )

    man = {
        "package_id": f"adult-{channel}",
        "platform_id": platform_id,
        "package_readiness": readiness,
        "status": AGGREGATE_STATE,
        "not_status": "PUBLICATION_READY",
        "created_on": TODAY,
        "integration_base": "cursor/publication-family-parallel-production-001",
        "full31_pre_review_content_sha": FREEZE_SHA,
        "credentials_included": False,
        "human_validated": "0/31",
        "publication_ready": "0/31",
        "artifacts": files_meta,
        "files": [{"path": p} for p in ordered if p != "CHECKSUMS.sha256"]
        + [{"path": "CHECKSUMS.sha256"}],
    }
    if extra_manifest:
        man.update(extra_manifest)
    dump_manifest(pkg, man)
    # checksums after manifest written
    write_checksums(pkg, [p for p in ordered if p != "CHECKSUMS.sha256"] + ["MANIFEST.yaml", "README.md", "validation-stub.md", "HUMAN_CHECKLIST.md"])
    # rewrite checksums including all present package files except CHECKSUMS itself
    rels = []
    for path in pkg.rglob("*"):
        if path.is_file() and path.name != "CHECKSUMS.sha256":
            rels.append(str(path.relative_to(pkg)))
    write_checksums(pkg, rels)


def require_sources() -> None:
    missing = []
    for p in [EPUB_SRC, DIGITAL_PDF_SRC, *PRINT_SRC.values()]:
        if not p.is_file():
            missing.append(str(p.relative_to(ROOT)))
    if missing:
        raise SystemExit(
            "Missing canonical sources (run make full31-epub/full31-pdf + scripts/render_print_profiles.sh):\n  - "
            + "\n  - ".join(missing)
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skip-print-check", action="store_true")
    args = ap.parse_args()
    if not args.skip_print_check:
        require_sources()

    epub_sha = sha256_file(EPUB_SRC)
    digital_pages, digital_w, digital_h = pdf_pages_dims(DIGITAL_PDF_SRC)
    digital_sha = sha256_file(DIGITAL_PDF_SRC)

    print_meta = {}
    for trim, path in PRINT_SRC.items():
        pages, w, h = pdf_pages_dims(path)
        print_meta[trim] = {
            "path": path,
            "pages": pages,
            "width_in": round(w, 3),
            "height_in": round(h, 3),
            "sha256": sha256_file(path),
            "paperback": eligibility_for_pages(trim if trim != "8.5x11" else "8.5x11", pages, "paperback"),
            "hardcover": eligibility_for_pages(trim if trim != "8.5x11" else "8.5x11", pages, "hardcover"),
        }

    # --- amazon-kindle ---
    kindle = ADULT / "amazon-kindle" / "artifacts"
    copy_real(EPUB_SRC, kindle / "manuscript.epub")
    ensure_stub(
        kindle / "cover.jpg.STUB",
        "amazon_kdp_kindle",
        "BLOCKED_OWNER_COVER — technical proof is not final marketing art",
    )
    build_channel(
        "amazon-kindle",
        readiness="BLOCKED_OWNER_COVER",
        platform_id="amazon_kdp_kindle",
        files_meta=[
            {
                "path": "artifacts/manuscript.epub",
                "artifact_type": "EPUB",
                "role": "MANUSCRIPT",
                "sha256": epub_sha,
                "source": "preview/full31/technology-landscape-full31-epub.epub",
            },
            {
                "path": "artifacts/cover.jpg.STUB",
                "artifact_type": "STUB",
                "role": "COVER",
                "final": False,
                "block": "BLOCKED_OWNER_COVER",
            },
        ],
        notes=[
            "Manuscript EPUB copied from canonical FULL31 render.",
            "Cover remains owner-blocked; do not treat SVG technical proof as final.",
            "`KINDLE_PREVIEWER_HUMAN_OR_EXTERNAL_PENDING` — not automatable in this environment.",
            "Also blocked: ISBN purchase, human Gate 3 review.",
        ],
        extra_manifest={
            "kindle_previewer": "KINDLE_PREVIEWER_HUMAN_OR_EXTERNAL_PENDING",
            "blocks": ["BLOCKED_OWNER_COVER", "BLOCKED_OWNER_ISBN", "BLOCKED_HUMAN_REVIEW"],
        },
    )

    # --- ebook storefronts ---
    for channel, platform_id, epub_name in [
        ("apple-books", "apple_books", "book.epub"),
        ("google-play-books", "google_play_books", "book.epub"),
        ("kobo", "kobo_writing_life", "book.epub"),
    ]:
        art = ADULT / channel / "artifacts"
        copy_real(EPUB_SRC, art / epub_name)
        ensure_stub(
            art / "cover.jpg.STUB",
            platform_id,
            "BLOCKED_OWNER_COVER — technical proof is not final marketing art",
        )
        build_channel(
            channel,
            readiness="BLOCKED_OWNER_COVER",
            platform_id=platform_id,
            files_meta=[
                {
                    "path": f"artifacts/{epub_name}",
                    "artifact_type": "EPUB",
                    "role": "MANUSCRIPT",
                    "sha256": epub_sha,
                    "source": "preview/full31/technology-landscape-full31-epub.epub",
                },
                {
                    "path": "artifacts/cover.jpg.STUB",
                    "artifact_type": "STUB",
                    "role": "COVER",
                    "final": False,
                    "block": "BLOCKED_OWNER_COVER",
                },
            ],
            notes=[
                "EPUB from canonical FULL31 render.",
                "Cover owner-blocked.",
                "ISBN + human review still pending.",
            ],
            extra_manifest={"blocks": ["BLOCKED_OWNER_COVER", "BLOCKED_OWNER_ISBN", "BLOCKED_HUMAN_REVIEW"]},
        )

    # --- direct-free ---
    df = ADULT / "direct-free" / "artifacts"
    copy_real(EPUB_SRC, df / "book.epub")
    copy_real(DIGITAL_PDF_SRC, df / "book.pdf")
    hosting = df / "README-HOSTING.md"
    hosting.write_text(
        "# Direct hosting notes\n\n"
        "- `book.epub` / `book.pdf` are DIGITAL_ACCESS artifacts from FULL31 renders.\n"
        "- `book.pdf` is **DIGITAL_ACCESS_PDF** (review/letter geometry), not a print interior.\n"
        "- Hosting venue + ARR free-access wording remain owner decisions.\n"
        "- Do not actually upload without owner approval.\n",
        encoding="utf-8",
    )
    build_channel(
        "direct-free",
        readiness="BLOCKED_OWNER_METADATA",
        platform_id="direct_web",
        files_meta=[
            {
                "path": "artifacts/book.epub",
                "artifact_type": "EPUB",
                "role": "MANUSCRIPT",
                "sha256": epub_sha,
            },
            {
                "path": "artifacts/book.pdf",
                "artifact_type": "PDF",
                "pdf_role": "DIGITAL_ACCESS_PDF",
                "role": "DIGITAL_ACCESS",
                "sha256": digital_sha,
                "page_count": digital_pages,
                "dimensions_in": [digital_w, digital_h],
                "source": "preview/full31/technology-landscape-full31-pdf.pdf",
            },
            {"path": "artifacts/README-HOSTING.md", "artifact_type": "TEXT", "role": "HOSTING_NOTES"},
        ],
        notes=[
            "DIGITAL_ACCESS_PDF distinguished from PRINT_INTERIOR_PDF.",
            "Hosting venue / public metadata copy remain owner-blocked.",
            "Human review + ISBN decisions still pending for commercial channels.",
        ],
        extra_manifest={"blocks": ["BLOCKED_OWNER_METADATA", "BLOCKED_HUMAN_REVIEW"]},
    )

    # --- libraries ---
    lib = ADULT / "libraries" / "artifacts"
    copy_real(EPUB_SRC, lib / "book.epub")
    build_library_metadata(lib / "metadata.yaml")
    build_channel(
        "libraries",
        readiness="BLOCKED_OWNER_ISBN",
        platform_id="library_distributor",
        files_meta=[
            {
                "path": "artifacts/book.epub",
                "artifact_type": "EPUB",
                "role": "MANUSCRIPT",
                "sha256": epub_sha,
            },
            {
                "path": "artifacts/metadata.yaml",
                "artifact_type": "YAML",
                "role": "LIBRARY_METADATA_DRAFT",
                "isbn_state": "PENDING_OWNER_PURCHASE",
            },
        ],
        notes=[
            "EPUB + draft metadata assembled.",
            "ISBN agency purchase and distributor commercial terms are owner decisions.",
            "Cover for library portals remains owner-blocked if required by channel.",
        ],
        extra_manifest={
            "blocks": ["BLOCKED_OWNER_ISBN", "BLOCKED_OWNER_COVER", "BLOCKED_HUMAN_REVIEW"],
        },
    )

    # --- paperback: primary 6x9 print interior ---
    pb = ADULT / "amazon-paperback" / "artifacts"
    p6 = print_meta["6x9"]
    copy_real(p6["path"], pb / "interior.pdf")
    ensure_stub(
        pb / "cover-wrap.pdf.STUB",
        "amazon_kdp_paperback",
        "LIVE_COVER_CALCULATOR_REQUIRED — no invented spine; BLOCKED_OWNER_COVER",
    )
    build_channel(
        "amazon-paperback",
        readiness="BLOCKED_OWNER_COVER",
        platform_id="amazon_kdp_paperback",
        files_meta=[
            {
                "path": "artifacts/interior.pdf",
                "artifact_type": "PDF",
                "pdf_role": "PRINT_INTERIOR_PDF",
                "role": "PRINT_INTERIOR",
                "trim": "6x9",
                "page_count": p6["pages"],
                "dimensions_in": [p6["width_in"], p6["height_in"]],
                "sha256": p6["sha256"],
                "paperback_eligibility": p6["paperback"],
                "source": "preview/print/technology-landscape-print-6x9-interior.pdf",
            },
            {
                "path": "artifacts/cover-wrap.pdf.STUB",
                "artifact_type": "STUB",
                "role": "COVER_WRAP",
                "final": False,
                "spine_status": "LIVE_COVER_CALCULATOR_REQUIRED",
                "block": "BLOCKED_OWNER_COVER",
            },
        ],
        notes=[
            f"PRINT_INTERIOR_PDF from print-6x9 profile ({p6['pages']} pages, 6×9 in).",
            f"Paperback eligibility: {p6['paperback']['reason']} (band {p6['paperback']['verified_band']}).",
            "Cover wrap spine requires live KDP Cover Calculator — not invented here.",
        ],
        extra_manifest={
            "blocks": ["BLOCKED_OWNER_COVER", "BLOCKED_OWNER_ISBN", "BLOCKED_HUMAN_REVIEW"],
            "spine_status": "LIVE_COVER_CALCULATOR_REQUIRED",
            "primary_trim": "6x9",
        },
    )

    # --- hardcover: 6x9 exceeds 550 → use eligible 7x10 interior as candidate ---
    hc = ADULT / "amazon-hardcover" / "artifacts"
    p6h = print_meta["6x9"]["hardcover"]
    p7 = print_meta["7x10"]
    copy_real(p7["path"], hc / "interior.pdf")
    ensure_stub(
        hc / "cover-wrap.pdf.STUB",
        "amazon_kdp_hardcover",
        "LIVE_COVER_CALCULATOR_REQUIRED — no invented spine; BLOCKED_OWNER_COVER",
    )
    build_channel(
        "amazon-hardcover",
        readiness="BLOCKED_OWNER_COVER",
        platform_id="amazon_kdp_hardcover",
        files_meta=[
            {
                "path": "artifacts/interior.pdf",
                "artifact_type": "PDF",
                "pdf_role": "PRINT_INTERIOR_PDF",
                "role": "PRINT_INTERIOR",
                "trim": "7x10",
                "page_count": p7["pages"],
                "dimensions_in": [p7["width_in"], p7["height_in"]],
                "sha256": p7["sha256"],
                "hardcover_eligibility": p7["hardcover"],
                "note": (
                    f"Primary 6x9 print interior is {p6h['page_count']} pages — "
                    f"{p6h['reason']} vs hardcover band {p6h['verified_band']}. "
                    "Packaged eligible 7x10 interior instead."
                ),
                "source": "preview/print/technology-landscape-print-7x10-interior.pdf",
            },
            {
                "path": "artifacts/cover-wrap.pdf.STUB",
                "artifact_type": "STUB",
                "role": "COVER_WRAP",
                "final": False,
                "spine_status": "LIVE_COVER_CALCULATOR_REQUIRED",
                "block": "BLOCKED_OWNER_COVER",
            },
        ],
        notes=[
            f"6×9 hardcover ineligible at {p6h['page_count']} pages (verified band {p6h['verified_band']}).",
            f"Packaged 7×10 PRINT_INTERIOR_PDF ({p7['pages']} pages) — {p7['hardcover']['reason']}.",
            "Spine/cover wrap: LIVE_COVER_CALCULATOR_REQUIRED.",
            "Owner must confirm whether hardcover ships in v1.",
        ],
        extra_manifest={
            "blocks": ["BLOCKED_OWNER_COVER", "BLOCKED_OWNER_ISBN", "BLOCKED_HUMAN_REVIEW"],
            "spine_status": "LIVE_COVER_CALCULATOR_REQUIRED",
            "hardcover_primary_6x9_eligibility": p6h,
            "hardcover_packaged_trim": "7x10",
        },
    )

    # Top-level README
    (ADULT / "README.md").write_text(
        f"""# Adult release packages

**Aggregate state:** `{AGGREGATE_STATE}`  
**Package readiness vocabulary:** `SCAFFOLD_ONLY` | `ARTIFACTS_BUILT` | `VALIDATED_LOCALLY` | `BLOCKED_OWNER_COVER` | `BLOCKED_OWNER_METADATA` | `BLOCKED_OWNER_ISBN` | `BLOCKED_HUMAN_REVIEW` | `READY_FOR_OWNER_UPLOAD`  
**Not:** `PUBLICATION_READY` · `READY_FOR_OWNER_UPLOAD` (owner cover/ISBN/human review still blocked)

Channels:

- `amazon-kindle/`
- `amazon-paperback/`
- `amazon-hardcover/`
- `apple-books/`
- `google-play-books/`
- `kobo/`
- `direct-free/`
- `libraries/`

See `publication/distribution/ADULT_DISTRIBUTION_READINESS_REPORT.md` and
`publication/distribution/print/PRINT_PROFILE_RESULTS.md`.

HUMAN_VALIDATED = 0/31 · PUBLICATION_READY = 0/31 · Gate 3 pending.
""",
        encoding="utf-8",
    )

    print("build_adult_artifact_packages: PASS")
    print(f"  channels: {len(REQUIRED_CHANNELS)}")
    print(f"  epub_sha256: {epub_sha}")
    print(f"  digital_access_pdf: pages={digital_pages} sha256={digital_sha}")
    for trim, m in print_meta.items():
        print(
            f"  print_{trim}: pages={m['pages']} dim={m['width_in']}x{m['height_in']} "
            f"pb_ok={m['paperback']['eligible']} hc_ok={m['hardcover']['eligible']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
