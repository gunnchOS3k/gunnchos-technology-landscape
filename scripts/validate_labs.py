#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REQUIRED = [
    "lab_id",
    "title",
    "chapter",
    "question",
    "prerequisites",
    "accessible_routes",
    "prediction",
    "procedure",
    "evidence",
    "interpretation",
    "limits",
    "portfolio",
    "teach_back",
]


def main() -> int:
    errors: list[str] = []
    reg = load_yaml(ROOT / "labs/lab_registry.yaml")
    for item in reg.get("labs") or []:
        lab_id = item["lab_id"]
        path = ROOT / item["path"] / "lab.yaml"
        if not path.exists():
            errors.append(f"{lab_id}: missing lab.yaml")
            continue
        lab = load_yaml(path)
        for key in REQUIRED:
            if key not in lab:
                errors.append(f"{lab_id}: missing section/field {key}")
        routes = lab.get("accessible_routes") or {}
        if not routes.get("no_specialized_hardware"):
            errors.append(f"{lab_id}: missing no_specialized_hardware route")
        interp = lab.get("interpretation") or {}
        for k in ("observation_required", "inference_required", "causation_warning"):
            if not interp.get(k):
                errors.append(f"{lab_id}: interpretation.{k} must be true")
        if not (lab.get("evidence") or {}).get("required_artifacts"):
            errors.append(f"{lab_id}: missing evidence.required_artifacts")
        readme = path.parent / "README.md"
        if not readme.exists():
            errors.append(f"{lab_id}: missing README.md")
        if lab_id == "LAB-TAP-001":
            for rel in [
                "browser/index.html",
                "local_app/tap_timer.py",
                "portfolio/README.md",
                "fixtures/sample_result_table.csv",
            ]:
                if not (path.parent / rel).exists():
                    errors.append(f"{lab_id}: missing {rel}")
        if lab_id == "LAB-PKT-001":
            for rel in [
                "browser/index.html",
                "cli/path_inspect.py",
                "portfolio/README.md",
                "fixtures/sample_path_trace.json",
                "fixtures/sample_timing_table.csv",
                "fixtures/sample_observation.md",
                "ACCESSIBILITY.md",
                "PRIVACY_AND_SAFETY.md",
                "STATUS.yaml",
            ]:
                if not (path.parent / rel).exists():
                    errors.append(f"{lab_id}: missing {rel}")
        if lab_id == "LAB-SYS-001":
            for rel in [
                "browser/index.html",
                "fixtures/readiness_demo.html",
                "portfolio/README.md",
            ]:
                if not (path.parent / rel).exists():
                    errors.append(f"{lab_id}: missing {rel}")
        if lab_id == "LAB-CMS-001":
            for rel in [
                "local_app/safe_snapshot.py",
                "fixtures/FIG-CE3-009-monitor-transcript.md",
                "fixtures/sample_observation_table.csv",
                "portfolio/README.md",
                "routes/commodity_computer.md",
            ]:
                if not (path.parent / rel).exists():
                    errors.append(f"{lab_id}: missing {rel}")
        if lab_id == "LAB-TRUST-001":
            for rel in [
                "browser/index.html",
                "local_app/trust_sim.py",
                "fixtures/route_c_transcript.md",
                "fixtures/route_l_transcript.md",
                "portfolio/README.md",
                "A11Y_PRIVACY_SAFETY.md",
            ]:
                if not (path.parent / rel).exists():
                    errors.append(f"{lab_id}: missing {rel}")
        if lab_id == "LAB-CE06-001":
            for rel in [
                "browser/index.html",
                "fixtures/sample_result_table.csv",
                "fixtures/illustrative_example/README.md",
                "portfolio/README.md",
                "export_portfolio.py",
            ]:
                if not (path.parent / rel).exists():
                    errors.append(f"{lab_id}: missing {rel}")
    if errors:
        print("validate_labs: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_labs: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
