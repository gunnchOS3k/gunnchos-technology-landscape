#!/usr/bin/env python3
"""Validate adult print profile results honesty (not printer-certified)."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = ROOT / "publication/distribution/print/PRINT_PROFILE_RESULTS.yaml"
MD_PATH = ROOT / "publication/distribution/print/PRINT_PROFILE_RESULTS.md"
ADULT = ROOT / "release-packages/adult"

EXPECTED_PAGES = {
    "print-6x9": 628,
    "print-7x10": 524,
    "print-85x11": 436,
}


def main() -> int:
    errors: list[str] = []
    if not YAML_PATH.is_file():
        errors.append(f"missing {YAML_PATH.relative_to(ROOT)}")
    if not MD_PATH.is_file():
        errors.append(f"missing {MD_PATH.relative_to(ROOT)}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    if data.get("status") in {"PUBLICATION_READY", "PRINTER_CERTIFIED"}:
        errors.append("print results must not claim PUBLICATION_READY / PRINTER_CERTIFIED")

    digital = data.get("digital_access_reference") or {}
    if digital.get("pdf_role") != "DIGITAL_ACCESS_PDF":
        errors.append("digital_access_reference.pdf_role must be DIGITAL_ACCESS_PDF")

    profiles = {p.get("profile_id"): p for p in (data.get("profiles") or [])}
    for pid, pages in EXPECTED_PAGES.items():
        p = profiles.get(pid)
        if not p:
            errors.append(f"missing profile {pid}")
            continue
        if p.get("pdf_role") != "PRINT_INTERIOR_PDF":
            errors.append(f"{pid}: pdf_role must be PRINT_INTERIOR_PDF")
        if p.get("page_count") != pages:
            errors.append(f"{pid}: expected page_count={pages}, got {p.get('page_count')}")
        if p.get("spine_status") != "LIVE_COVER_CALCULATOR_REQUIRED":
            errors.append(f"{pid}: spine_status must be LIVE_COVER_CALCULATOR_REQUIRED")

    p69 = profiles.get("print-6x9") or {}
    hc69 = (p69.get("hardcover_eligibility") or {})
    if hc69.get("eligible") is not False:
        errors.append("print-6x9 hardcover must be ineligible (page count over verified band)")
    reason = str(hc69.get("reason") or "")
    if "OUTSIDE" not in reason and "INELIGIBLE" not in reason:
        errors.append("print-6x9 hardcover reason must record OUTSIDE/INELIGIBLE page-count band")

    p710 = profiles.get("print-7x10") or {}
    hc710 = (p710.get("hardcover_eligibility") or {})
    if hc710.get("eligible") is not True:
        errors.append("print-7x10 hardcover must be eligible candidate within verified band")

    note = str(data.get("hardcover_decision_note") or "")
    if "6x9" not in note or "7x10" not in note:
        errors.append("hardcover_decision_note must mention 6x9 over-max and 7x10 candidate")

    md = MD_PATH.read_text(encoding="utf-8")
    for needle in ("628", "524", "436", "LIVE_COVER_CALCULATOR_REQUIRED", "DIGITAL_ACCESS"):
        if needle not in md:
            errors.append(f"PRINT_PROFILE_RESULTS.md missing {needle!r}")

    # Packaged interiors must match claimed print SHAs when present (preview/ is gitignored).
    expected_sha = {
        "amazon-paperback": (profiles.get("print-6x9") or {}).get("sha256"),
        "amazon-hardcover": (profiles.get("print-7x10") or {}).get("sha256"),
    }
    for channel, sha in expected_sha.items():
        interior = ADULT / channel / "artifacts" / "interior.pdf"
        if not interior.is_file():
            errors.append(f"{channel}: missing packaged PRINT_INTERIOR_PDF interior.pdf")
            continue
        import hashlib

        got = hashlib.sha256(interior.read_bytes()).hexdigest()
        if sha and got != sha:
            errors.append(f"{channel}: interior.pdf sha256 mismatch vs PRINT_PROFILE_RESULTS")

    direct_pdf = ADULT / "direct-free" / "artifacts" / "book.pdf"
    if direct_pdf.is_file() and digital.get("sha256"):
        import hashlib

        got = hashlib.sha256(direct_pdf.read_bytes()).hexdigest()
        if got != digital.get("sha256"):
            errors.append("direct-free book.pdf sha256 mismatch vs DIGITAL_ACCESS_PDF reference")
        # DIGITAL_ACCESS must not equal a print interior sha
        for pid, p in profiles.items():
            if p.get("sha256") and got == p.get("sha256"):
                errors.append(
                    f"DIGITAL_ACCESS_PDF must differ from PRINT_INTERIOR_PDF ({pid})"
                )

    if errors:
        print("print-profile-check FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("print-profile-check PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
