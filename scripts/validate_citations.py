#!/usr/bin/env python3
"""Validate citation keys used in manuscript against references.bib."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CITE_RE = re.compile(r"@([a-zA-Z][\w:-]*)")
BIBKEY_RE = re.compile(r"^@\w+\{\s*([^,\s]+)\s*,", re.M)


def main() -> int:
    errors: list[str] = []
    bib = (ROOT / "book/references/references.bib").read_text(encoding="utf-8")
    keys = set(BIBKEY_RE.findall(bib))
    if not keys:
        errors.append("references.bib has no citation keys")

    ch2 = (ROOT / "book/chapters/ch02/chapter.md").read_text(encoding="utf-8")
    # Ignore email-like and yaml-ish; Quarto cites are @key
    used = set()
    for m in CITE_RE.finditer(ch2):
        key = m.group(1)
        # skip common false positives
        if key in {"fig", "tbl", "eq", "sec", "lst"}:
            continue
        if key.startswith("fig-"):
            continue
        used.add(key)

    required = {
        "w3c-uievents",
        "whatwg-dom",
        "rfc9293",
        "linux-scheduler",
        "patterson-hennessy",
    }
    missing_required = sorted(required - used)
    if missing_required:
        errors.append(f"CH02 missing expected citation keys: {', '.join(missing_required)}")

    for key in sorted(used):
        if key not in keys and not key.startswith("fig-ch02"):
            # allow quarto fig crossrefs already filtered
            errors.append(f"unknown citation key used in CH02: {key}")

    if errors:
        print("validate_citations: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print(f"validate_citations: PASS ({len(used)} keys used; {len(keys)} bib keys)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
