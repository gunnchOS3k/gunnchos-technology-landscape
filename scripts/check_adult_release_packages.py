#!/usr/bin/env python3
"""Validate adult release-package layout, manifests, and checksums (stubs OK)."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADULT = ROOT / "release-packages" / "adult"

REQUIRED_CHANNELS = [
    "amazon-kindle",
    "amazon-paperback",
    "amazon-hardcover",
    "apple-books",
    "google-play-books",
    "kobo",
    "direct-free",
    "libraries",
]

REQUIRED_FILES = [
    "README.md",
    "MANIFEST.yaml",
    "CHECKSUMS.sha256",
    "validation-stub.md",
    "HUMAN_CHECKLIST.md",
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    if not ADULT.is_dir():
        print("adult-release-package-check: FAIL — missing release-packages/adult/")
        return 1

    for channel in REQUIRED_CHANNELS:
        pkg = ADULT / channel
        if not pkg.is_dir():
            errors.append(f"missing package dir: {channel}")
            continue
        for name in REQUIRED_FILES:
            if not (pkg / name).is_file():
                errors.append(f"{channel}: missing {name}")
        art = pkg / "artifacts"
        if not art.is_dir() or not any(art.iterdir()):
            errors.append(f"{channel}: artifacts/ empty")

        readme = (pkg / "README.md").read_text(encoding="utf-8")
        if "PUBLICATION_READY" in readme and "Not:" not in readme and "not" not in readme.lower():
            errors.append(f"{channel}: README may overclaim PUBLICATION_READY")
        if "ADULT_SUBMISSION_PACKAGE_PREPARED" not in readme:
            errors.append(f"{channel}: README missing ceiling state")
        if "credential" in readme.lower() and "no credential" not in readme.lower() and "credentials" not in (pkg / "MANIFEST.yaml").read_text(encoding="utf-8"):
            pass
        man = (pkg / "MANIFEST.yaml").read_text(encoding="utf-8")
        if "credentials_included: false" not in man:
            errors.append(f"{channel}: MANIFEST must set credentials_included: false")
        if "not_status: PUBLICATION_READY" not in man:
            errors.append(f"{channel}: MANIFEST must set not_status: PUBLICATION_READY")

        # Verify checksums (exclude CHECKSUMS.sha256 itself)
        checksum_path = pkg / "CHECKSUMS.sha256"
        if checksum_path.is_file():
            for line in checksum_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    digest, rel = line.split(None, 1)
                except ValueError:
                    errors.append(f"{channel}: bad checksum line: {line!r}")
                    continue
                target = pkg / rel
                if not target.is_file():
                    errors.append(f"{channel}: checksum target missing: {rel}")
                    continue
                actual = sha256_file(target)
                if actual != digest:
                    errors.append(f"{channel}: checksum mismatch: {rel}")

        # No secrets patterns in package text
        for path in pkg.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".epub"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for bad in ("BEGIN RSA PRIVATE KEY", "AWS_SECRET", "password=", "api_key="):
                if bad in text:
                    errors.append(f"{channel}: possible secret material in {path.relative_to(pkg)}")

    if errors:
        print("adult-release-package-check: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("adult-release-package-check: PASS")
    print(f"  channels: {len(REQUIRED_CHANNELS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
