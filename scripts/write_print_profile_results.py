#!/usr/bin/env python3
"""Write PRINT_PROFILE_RESULTS.yaml/.md from rendered print interiors."""
from __future__ import annotations

import hashlib
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from adult_package_common import eligibility_for_pages  # noqa: E402

OUT_DIR = ROOT / "publication" / "distribution" / "print"
PRINT_DIR = ROOT / "preview" / "print"
DIGITAL = ROOT / "preview" / "full31" / "technology-landscape-full31-pdf.pdf"

PROFILES = [
    {
        "profile_id": "print-6x9",
        "config": "_quarto-print-6x9.yml",
        "trim": "6x9",
        "trim_in": [6.0, 9.0],
        "pdf": PRINT_DIR / "technology-landscape-print-6x9-interior.pdf",
        "intent": "PRIMARY_TRADE",
    },
    {
        "profile_id": "print-7x10",
        "config": "_quarto-print-7x10.yml",
        "trim": "7x10",
        "trim_in": [7.0, 10.0],
        "pdf": PRINT_DIR / "technology-landscape-print-7x10-interior.pdf",
        "intent": "ALT_FIGURE_HEAVY",
    },
    {
        "profile_id": "print-85x11",
        "config": "_quarto-print-85x11.yml",
        "trim": "8.5x11",
        "trim_in": [8.5, 11.0],
        "pdf": PRINT_DIR / "technology-landscape-print-85x11-interior.pdf",
        "intent": "HANDOUT_ALT_ONLY",
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pages_dims(path: Path) -> tuple[int, float, float]:
    from pypdf import PdfReader

    r = PdfReader(str(path))
    b = r.pages[0].mediabox
    return len(r.pages), float(b.width) / 72.0, float(b.height) / 72.0


def main() -> int:
    missing = [str(p["pdf"].relative_to(ROOT)) for p in PROFILES if not p["pdf"].is_file()]
    if missing:
        print("write_print_profile_results: FAIL — missing renders:")
        for m in missing:
            print(f"  - {m}")
        return 1

    digital = None
    if DIGITAL.is_file():
        dp, dw, dh = pages_dims(DIGITAL)
        digital = {
            "path": str(DIGITAL.relative_to(ROOT)),
            "pdf_role": "DIGITAL_ACCESS_PDF",
            "page_count": dp,
            "dimensions_in": [round(dw, 3), round(dh, 3)],
            "sha256": sha256(DIGITAL),
            "note": "Review/letter PDF from make full31-pdf — not a print interior.",
        }

    results = []
    for p in PROFILES:
        pages, w, h = pages_dims(p["pdf"])
        pb = eligibility_for_pages(p["trim"], pages, "paperback")
        hc = eligibility_for_pages(p["trim"], pages, "hardcover")
        warnings = []
        if abs(w - p["trim_in"][0]) > 0.05 or abs(h - p["trim_in"][1]) > 0.05:
            warnings.append(
                f"Measured page size {w:.3f}x{h:.3f}in differs from intended trim {p['trim_in']}"
            )
        if not pb["eligible"]:
            warnings.append(f"Paperback eligibility: {pb['reason']}")
        if not hc["eligible"]:
            warnings.append(f"Hardcover eligibility: {hc['reason']}")
        warnings.append("Spine/cover wrap geometry: LIVE_COVER_CALCULATOR_REQUIRED (not invented).")
        warnings.append("Not printer-certified; not PUBLICATION_READY.")
        results.append(
            {
                "profile_id": p["profile_id"],
                "config_file": p["config"],
                "intent": p["intent"],
                "trim": p["trim"],
                "intended_trim_in": p["trim_in"],
                "output_pdf": str(p["pdf"].relative_to(ROOT)),
                "pdf_role": "PRINT_INTERIOR_PDF",
                "page_count": pages,
                "measured_dimensions_in": [round(w, 3), round(h, 3)],
                "sha256": sha256(p["pdf"]),
                "paperback_eligibility": pb,
                "hardcover_eligibility": hc,
                "spine_status": "LIVE_COVER_CALCULATOR_REQUIRED",
                "warnings": warnings,
            }
        )

    doc = {
        "schema": "adult.print.profile_results/v1",
        "generated_on": date.today().isoformat(),
        "status": "RENDERED_INTERNAL",
        "not_status": ["PUBLICATION_READY", "PRINTER_CERTIFIED"],
        "kdp_limits_source": "publication/distribution/platforms/PLATFORM_REQUIREMENTS.yaml",
        "digital_access_reference": digital,
        "profiles": results,
        "hardcover_decision_note": (
            "Primary 6x9 print interior exceeds verified hardcover B&W white max (550). "
            "Hardcover package uses eligible 7x10 interior pending owner decision."
        ),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    yaml_path = OUT_DIR / "PRINT_PROFILE_RESULTS.yaml"
    yaml_path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")

    lines = [
        "# Print Profile Results",
        "",
        f"**Generated:** {doc['generated_on']}  ",
        "**Status:** `RENDERED_INTERNAL` — not printer-certified · not `PUBLICATION_READY`",
        "",
        "## Digital access reference (not print)",
        "",
    ]
    if digital:
        lines += [
            f"- Path: `{digital['path']}`",
            f"- Role: `{digital['pdf_role']}`",
            f"- Pages: **{digital['page_count']}** · {digital['dimensions_in'][0]}×{digital['dimensions_in'][1]} in",
            f"- SHA-256: `{digital['sha256']}`",
            "",
        ]
    lines += [
        "## Print interiors",
        "",
        "| Profile | Trim | Pages | Measured | Paperback | Hardcover | SHA-256 (12) |",
        "| --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for r in results:
        lines.append(
            f"| `{r['profile_id']}` | {r['trim']} | {r['page_count']} | "
            f"{r['measured_dimensions_in'][0]}×{r['measured_dimensions_in'][1]} in | "
            f"{'YES' if r['paperback_eligibility']['eligible'] else 'NO'} "
            f"({r['paperback_eligibility']['verified_band']}) | "
            f"{'YES' if r['hardcover_eligibility']['eligible'] else 'NO'} "
            f"({r['hardcover_eligibility'].get('verified_band') or r['hardcover_eligibility']['reason']}) | "
            f"`{r['sha256'][:12]}…` |"
        )
    lines += [
        "",
        "## Warnings",
        "",
        "- Spine / cover wrap: **`LIVE_COVER_CALCULATOR_REQUIRED`** — no invented spine inches.",
        "- Primary **6×9** page count exceeds hardcover verified band **75–550** → hardcover package uses **7×10** interior.",
        "- `8.5×11` remains handout/large alt only; hardcover not in KDP table for this trim.",
        "- Review PDF path (`make full31-pdf`) remains intact and distinct (`DIGITAL_ACCESS_PDF`).",
        "",
        "## Machine-readable",
        "",
        "See `PRINT_PROFILE_RESULTS.yaml`.",
        "",
    ]
    (OUT_DIR / "PRINT_PROFILE_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    print("write_print_profile_results: PASS")
    for r in results:
        print(f"  {r['profile_id']}: pages={r['page_count']} sha={r['sha256'][:16]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
