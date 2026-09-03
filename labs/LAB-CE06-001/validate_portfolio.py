#!/usr/bin/env python3
"""Validate LAB-CE06-001 package structure, fixtures, and optional learner portfolio.

Does not award PASS for human learning. Rejects bare PASS evidence and forbidden status.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

LAB_DIR = Path(__file__).resolve().parent
ROOT = LAB_DIR.parents[1]

CAPSTONE_FILES = [
    "human_experience.md",
    "system_boundary.md",
    "components.md",
    "software_code_role.md",
    "network_role.md",
    "stability_contract.md",
    "observations.md",
    "inferences.md",
    "measurements.md",
    "evidence_limitations.md",
    "security_privacy_accessibility.md",
    "equity_societal_impact.md",
    "improve_plan.md",
    "teach_back.md",
    "portfolio_summary.md",
]

REQUIRED_PACKAGE = [
    "README.md",
    "lab.yaml",
    "rubric.yaml",
    "validate_portfolio.py",
    "export_portfolio.py",
    "browser/index.html",
    "fixtures/sample_observation.md",
    "fixtures/sample_result_table.csv",
    "fixtures/illustrative_example/README.md",
    "portfolio/README.md",
    "portfolio/result_table.csv",
    "builder/inspectability_checklist.md",
]

ALLOWED_STATUS = {
    "IMPLEMENTED_DIGITAL",
    "FIXTURE_VALIDATED",
    "PHYSICAL_PENDING",
    "EXTERNAL_DEPENDENCY",
}
FORBIDDEN_STATUS = {"PASS", "PASSED", "COMPLETE", "VERIFIED"}

SECRET_PATTERNS = [
    re.compile(r"(?i)password\s*[:=]\s*\S+"),
    re.compile(r"(?i)api[_-]?key\s*[:=]\s*\S+"),
    re.compile(r"(?i)bearer\s+[a-z0-9\-._~+/]+=*"),
    re.compile(r"(?i)-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
]


def load_yaml(path: Path):
    if yaml is None:
        raise SystemExit("PyYAML is required for validate_portfolio.py")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def check_secrets(text: str, label: str, errors: list[str]) -> None:
    for pat in SECRET_PATTERNS:
        if pat.search(text):
            errors.append(f"{label}: possible secret material matched {pat.pattern}")


def validate_package() -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_PACKAGE:
        if not (LAB_DIR / rel).exists():
            errors.append(f"missing package file: {rel}")

    lab_path = LAB_DIR / "lab.yaml"
    if lab_path.exists():
        lab = load_yaml(lab_path)
        if lab.get("lab_id") != "LAB-CE06-001":
            errors.append("lab.yaml lab_id must be LAB-CE06-001")
        status = lab.get("status")
        if status in FORBIDDEN_STATUS:
            errors.append(f"forbidden status: {status}")
        if status not in ALLOWED_STATUS:
            errors.append(f"status must be one of {sorted(ALLOWED_STATUS)}")
        routes = lab.get("accessible_routes") or {}
        if not routes.get("no_specialized_hardware"):
            errors.append("accessible_routes.no_specialized_hardware must be true")
        if not lab.get("fixture_available"):
            errors.append("fixture_available must be true")
        for field in CAPSTONE_FILES:
            # portfolio_output should mention capstone files
            pass
        interp = lab.get("interpretation") or {}
        for k in ("observation_required", "inference_required", "causation_warning"):
            if not interp.get(k):
                errors.append(f"interpretation.{k} must be true")
        # reject bare PASS culture in lab text
        raw = lab_path.read_text(encoding="utf-8")
        if re.search(r"(?m)^\\s*status:\\s*PASS\\s*$", raw):
            errors.append("lab.yaml must not use status PASS")

    # Fixture CSV must label fixture rows
    fixture_csv = LAB_DIR / "fixtures/sample_result_table.csv"
    if fixture_csv.exists():
        with fixture_csv.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
        if not rows:
            errors.append("fixtures/sample_result_table.csv has no data rows")
        labels = { (r.get("observed_or_inferred_or_fixture") or "").strip() for r in rows }
        if "fixture" not in labels:
            errors.append("fixture CSV must include at least one row labeled fixture")
        for r in rows:
            check_secrets(",".join(r.values()), "fixture CSV", errors)

    illust = LAB_DIR / "fixtures/illustrative_example/README.md"
    if illust.exists():
        text = illust.read_text(encoding="utf-8")
        if "NOT human evidence" not in text and "not human evidence" not in text.lower():
            errors.append("illustrative_example must declare it is NOT human evidence")

    # Blank portfolio templates present
    for name in CAPSTONE_FILES:
        p = LAB_DIR / "portfolio" / name
        if not p.exists():
            errors.append(f"missing blank template: portfolio/{name}")

    browser = LAB_DIR / "browser/index.html"
    if browser.exists():
        html = browser.read_text(encoding="utf-8")
        if "aria-live" not in html:
            errors.append("browser demo should expose aria-live status")
        if "fetch(" in html or "XMLHttpRequest" in html:
            errors.append("browser demo must stay offline-capable (no network fetch)")

    return errors


def validate_learner_portfolio(portfolio_dir: Path) -> list[str]:
    """Optional check of a filled portfolio directory."""
    errors: list[str] = []
    if not portfolio_dir.is_dir():
        return [f"portfolio dir missing: {portfolio_dir}"]
    for name in CAPSTONE_FILES:
        path = portfolio_dir / name
        if not path.exists():
            errors.append(f"missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        check_secrets(text, str(path), errors)
        if re.search(r"(?i)\\bGate\\s*3\\s*PASS\\b", text):
            errors.append(f"{name}: must not claim Gate 3 PASS")
        if re.search(r"(?m)^\\s*PASS\\s*$", text) or text.strip() == "PASS":
            errors.append(f"{name}: bare PASS is not valid evidence")
    table = portfolio_dir / "result_table.csv"
    if table.exists():
        raw = table.read_text(encoding="utf-8")
        check_secrets(raw, "result_table.csv", errors)
        if re.search(r"(?i)^\\s*PASS\\s*$", raw, re.M):
            errors.append("result_table.csv: bare PASS is not valid evidence")
    return errors


def main(argv: list[str]) -> int:
    errors = validate_package()
    if len(argv) > 1:
        errors.extend(validate_learner_portfolio(Path(argv[1])))
    if errors:
        print("LAB-CE06-001 validate_portfolio: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("LAB-CE06-001 validate_portfolio: OK (package structure; not a human learning PASS)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
