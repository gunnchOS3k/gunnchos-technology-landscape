#!/usr/bin/env python3
"""Publication-family integrity check (S1–S11 coordination)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "publication/family/README.md",
    "publication/family/PUBLICATION_FAMILY_REGISTRY.yaml",
    "publication/family/CONCEPT_REGISTRY.yaml",
    "publication/family/EXTERNAL_GATES.yaml",
    "publication/family/OWNER_DECISIONS_NEEDED.md",
    "publication/family/PARALLEL_PRODUCTION_STATUS.md",
    "publication/family/RIGHTS_POLICY_CONFIRMATION.md",
    "publication/distribution/ADULT_DISTRIBUTION_READINESS_REPORT.md",
    "kids/KIDS_PRODUCTION_STATUS.md",
    "kids/standards/GLOBAL_STANDARDS_COVERAGE_REPORT.md",
    "kids/standards/WIRE_HOOK_REGISTRY.yaml",
    "kids/research/CHILD_MEDIA_RESEARCH_REPORT.md",
    "kids/pilots/ONE_TAP/PILOT_REPORT.md",
]

FORBIDDEN_OVERCLAIM = re.compile(
    r"\b(officially aligned|globally aligned|child[- ]validated|we are publication[- ]ready)\b",
    re.IGNORECASE,
)

# Status phrases that must remain present as non-claims / preserved truth
MUST_MENTION = [
    (ROOT / "publication/family/PARALLEL_PRODUCTION_STATUS.md", "GATE_3_IN_PROGRESS"),
    (ROOT / "publication/family/PARALLEL_PRODUCTION_STATUS.md", "PUBLICATION_READY = 0/31"),
    (ROOT / "publication/family/RIGHTS_POLICY_CONFIRMATION.md", "All Rights Reserved"),
    (ROOT / "publication/family/RIGHTS_POLICY_CONFIRMATION.md", "MIT"),
]


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing: {rel}")
    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    family = load_yaml(ROOT / "publication/family/PUBLICATION_FAMILY_REGISTRY.yaml")
    rights = family.get("rights_policy") or {}
    if rights.get("blanket_creative_commons") is not False:
        errors.append("rights_policy.blanket_creative_commons must be false")
    if rights.get("free_price_equals_open_license") is not False:
        errors.append("rights_policy.free_price_equals_open_license must be false")
    if "ARR" not in str(rights.get("confirmation", "")) and "All Rights Reserved" not in str(
        rights.get("manuscript_and_original_artwork", "")
    ):
        errors.append("rights_policy must confirm ARR manuscript")

    editions = family.get("editions") or []
    ed_ids = {e.get("edition_id") for e in editions}
    for required_id in [
        "ADULT-FULL31",
        "KIDS-BABY",
        "KIDS-TODDLER",
        "KIDS-PRESCHOOL",
        "KIDS-PREK",
        "KIDS-ELEM1",
        "KIDS-ELEM2",
    ]:
        if required_id not in ed_ids:
            errors.append(f"family registry missing edition {required_id}")

    for e in editions:
        pub = (e.get("publication_state") or "").upper()
        if pub in {"PUBLICATION_READY", "PUBLISHED"}:
            errors.append(f"{e.get('edition_id')}: publication_state overclaim {pub}")
        if e.get("edition_id") == "ADULT-FULL31":
            if e.get("human_validation") not in {"0/31", "NONE", 0}:
                if str(e.get("human_validation")) != "0/31":
                    errors.append("adult human_validation must remain 0/31")
            if "NOT" not in str(e.get("publication_state", "")).upper():
                errors.append("adult must remain NOT_PUBLICATION_READY")

    concepts = load_yaml(ROOT / "publication/family/CONCEPT_REGISTRY.yaml").get("concepts") or []
    if len(concepts) != 31:
        errors.append(f"CONCEPT_REGISTRY expected 31 concepts, found {len(concepts)}")

    gates = load_yaml(ROOT / "publication/family/EXTERNAL_GATES.yaml").get("gates") or []
    if len(gates) < 10:
        errors.append("EXTERNAL_GATES.yaml unexpectedly sparse")
    for g in gates:
        if g.get("status") not in {None, "INCOMPLETE", "PENDING", "OPEN"}:
            errors.append(f"gate {g.get('gate_id')} must remain incomplete, got {g.get('status')}")

    wire = load_yaml(ROOT / "kids/standards/WIRE_HOOK_REGISTRY.yaml")
    if (wire.get("summary") or {}).get("official_alignment_claims", 1) != 0:
        errors.append("wire registry must record zero official alignment claims")

    for path, needle in MUST_MENTION:
        text = path.read_text(encoding="utf-8")
        if needle not in text:
            errors.append(f"{path.relative_to(ROOT)} missing required phrase {needle!r}")

    # Scan family + kids status docs for overclaims (allow negation contexts)
    scan_paths = [
        ROOT / "publication/family",
        ROOT / "kids/KIDS_PRODUCTION_STATUS.md",
        ROOT / "kids/pilots/ONE_TAP/PILOT_REPORT.md",
    ]
    for base in scan_paths:
        paths = [base] if base.is_file() else list(base.rglob("*.md")) + list(base.rglob("*.yaml"))
        for path in paths:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for m in FORBIDDEN_OVERCLAIM.finditer(text):
                # allow explicit rejection lines
                line = text[max(0, m.start() - 80) : m.end() + 80]
                if re.search(r"(?i)(not|never|no|reject|forbidden|non-claim)", line):
                    continue
                errors.append(
                    f"overclaim in {path.relative_to(ROOT)}: {m.group(0)!r}"
                )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        print(f"publication-family-check: FAIL ({len(errors)} issues)")
        return 1

    print("publication-family-check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
