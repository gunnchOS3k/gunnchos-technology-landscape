#!/usr/bin/env python3
"""Full31 quality audit — rebuild/check central QUALITY_ISSUES registry.

Also runs continuity audit aid in check-friendly mode when --full is set.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--full",
        action="store_true",
        help="Also run continuity audit (write) before registry rebuild",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate existing QUALITY_ISSUES.yaml without rebuilding",
    )
    args = parser.parse_args()
    py = sys.executable

    if args.full:
        rc = run([py, "scripts/audit_full31_continuity.py"])
        if rc != 0:
            return rc

    if args.check_only:
        return run([py, "scripts/build_quality_issues_registry.py", "--check"])

    rc = run([py, "scripts/build_quality_issues_registry.py", "--write"])
    if rc != 0:
        return rc
    return run([py, "scripts/build_quality_issues_registry.py", "--check"])


if __name__ == "__main__":
    raise SystemExit(main())
