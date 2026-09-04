#!/usr/bin/env python3
"""Validate adult release-package layout, manifests, checksums, and artifact honesty."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    # Layout + artifact readiness rules live in the artifact checker.
    cmd = [sys.executable, str(ROOT / "scripts" / "check_adult_artifact_packages.py"), "--negative-tests"]
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print("adult-release-package-check: FAIL (via adult-artifact-package-check)")
        return result.returncode
    print("adult-release-package-check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
