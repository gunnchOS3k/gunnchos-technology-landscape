#!/usr/bin/env python3
"""Fail if retailer passwords, tax IDs, API secrets, or payment details appear in-tree."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIR_NAMES = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "preview",
    "_book",
}

# High-signal secret patterns (not generic "password" documentation).
PATTERNS = [
    (
        "retailer_password_assignment",
        re.compile(
            r"(?i)(kdp|kindle|apple\s*books|google\s*play|kobo).{0,40}(password|passwd)\s*[:=]\s*\S+"
        ),
    ),
    (
        "aws_access_key",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    ),
    (
        "generic_api_secret_assignment",
        re.compile(
            r"(?i)\b(api[_-]?secret|client_secret|private_key|auth_token)\s*[:=]\s*['\"]?[A-Za-z0-9/+=_\-]{16,}"
        ),
    ),
    (
        "us_ssn_like",
        re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    ),
    (
        "payment_pan_like",
        re.compile(r"\b(?:4\d{3}|5[1-5]\d{2}|3[47]\d{2})[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    ),
]

TEXT_SUFFIXES = {
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".py",
    ".sh",
    ".toml",
    ".csv",
    ".html",
    ".qmd",
    ".tex",
    ".svg",
}


def should_scan(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
        "MANIFEST.yaml",
        "CHECKSUMS.sha256",
        "Dockerfile",
        "Makefile",
    }:
        return False
    # Allow documentation that mentions the words without assignments
    return True


def main() -> int:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if not should_scan(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pat in PATTERNS:
            if pat.search(text):
                # Allow explicit "do not store secrets" instructional lines
                rel = path.relative_to(ROOT)
                if name in {"us_ssn_like", "payment_pan_like"} and "example" in text.lower():
                    continue
                errors.append(f"{rel}: matched {name}")

    if errors:
        for e in errors[:50]:
            print(f"FAIL: {e}", file=sys.stderr)
        if len(errors) > 50:
            print(f"FAIL: ... and {len(errors) - 50} more", file=sys.stderr)
        print("secrets-scan: FAIL")
        return 1

    print("secrets-scan: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
