#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

KNOWN = {
    "SOFTWARE_BUILDER",
    "GAME_DEV_INTERACTIVE",
    "COMPUTER_NETWORKING",
    "EMBEDDED_PROTOTYPING",
    "AI_ML_EDGE",
    "CLOUD_DEVOPS",
    "COMM_PD_ETHICS",
    "CYBERSECURITY",
    "DATA_DASHBOARDS",
    "DATA_VIZ_BI",
    "GENERAL_IT",
    "GUNNCHOS_PRODUCT_LAB",
    "HARDWARE_ENGINEERING",
    "PM_AGILE_LSS",
    "ROBOTICS_CONTROL",
    "WIRELESS_6G",
}


def main() -> int:
    errors: list[str] = []
    data = load_yaml(ROOT / "waike/alignment.yaml")
    for row in data.get("alignment") or []:
        for course in row.get("mapped_courses") or []:
            cid = course.get("course_id")
            if cid not in KNOWN:
                errors.append(f"unknown/invented WAIKE course_id: {cid}")
        if not row.get("explicit_non_mapping"):
            errors.append("alignment rows must include explicit_non_mapping honesty notes when inventing is a risk")
    if errors:
        print("validate_waike: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_waike: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
