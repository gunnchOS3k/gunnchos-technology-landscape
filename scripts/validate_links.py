#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    skip_parts = {".venv", ".git", "tools", "preview", "_book", "node_modules", ".quarto"}
    # Freeze trees pin content via hashes/manifests; skip deep copies to avoid false link fails
    # when optional binaries (figures/builds) are linked rather than duplicated.
    skip_path_markers = (
        ("publication", "review-candidates"),
        ("kids", "review-candidates"),
    )
    for path in ROOT.rglob("*.md"):
        if skip_parts.intersection(path.parts):
            continue
        parts = path.parts
        if any(
            marker[0] in parts and marker[1] in parts and parts.index(marker[0]) < parts.index(marker[1])
            for marker in skip_path_markers
            if marker[0] in parts and marker[1] in parts
        ):
            continue
        text = path.read_text(encoding="utf-8")
        for label, target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            # strip anchors
            rel = target.split("#", 1)[0]
            if not rel:
                continue
            dest = (path.parent / rel).resolve()
            try:
                dest.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{path}: link escapes repo {target}")
                continue
            if not dest.exists():
                errors.append(f"{path}: broken local link {target}")
    if errors:
        print("validate_links: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_links: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
