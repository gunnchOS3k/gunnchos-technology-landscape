#!/usr/bin/env python3
"""Deterministic Full31 claim-source hygiene check (Agent EVIDENCE-A).

Fails when:
  - SOURCE_IDENTIFIED lacks citation_keys and project_evidence
  - citation_keys reference unknown candidate-bib keys (union of CE local bibs
    + CANDIDATE_BIBLIOGRAPHY.bib when present)
  - SOURCE_NEEDED pretends to be verified (non-empty citation_keys without note)

Does not invent sources. Does not touch publication/gates/gate-3/.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

BIBKEY_RE = re.compile(r"^@\w+\{\s*([^,\s]+)\s*,", re.M)
CHAPTERS = ROOT / "publication" / "full31" / "chapters"
PREPROD = ROOT / "publication" / "preproduction"
CE_DIRS = ("ce-01", "ce-03", "ce-04", "ce-05", "ce-06")

# Keys that are publication-internal / repo evidence aliases (not required in bib).
ALLOWLIST = frozenset(
    {
        "SRC-WAIKE",
        "src-waike",
        "SRC-CE06-02",
        "SRC-DEVICE-OS",
        "SRC-HARDWARE",
        "lab-tap-001",
        "src-hardware-quartet",
        "wcag22",  # undated shortcut discouraged; dual dated keys preferred
    }
)


def load_bib_keys() -> set[str]:
    keys: set[str] = set()
    for ce in CE_DIRS:
        path = PREPROD / ce / "references.local.bib"
        if path.exists():
            keys.update(BIBKEY_RE.findall(path.read_text(encoding="utf-8")))
    cand = PREPROD / "CANDIDATE_BIBLIOGRAPHY.bib"
    if cand.exists():
        keys.update(BIBKEY_RE.findall(cand.read_text(encoding="utf-8")))
    return keys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit 1 on failures")
    args = parser.parse_args()

    bib_keys = load_bib_keys()
    errors: list[str] = []
    counts = {
        "SOURCE_NEEDED": 0,
        "SOURCE_IDENTIFIED": 0,
        "other": 0,
    }

    for path in sorted(CHAPTERS.glob("*/CLAIM_PLAN.yaml")):
        data = load_yaml(path) or {}
        for claim in data.get("claims") or []:
            cid = claim.get("provisional_id")
            status = claim.get("status")
            keys = claim.get("citation_keys") or []
            pe = claim.get("project_evidence")
            if status == "SOURCE_NEEDED":
                counts["SOURCE_NEEDED"] += 1
                if keys:
                    errors.append(f"{path.name}:{cid}: SOURCE_NEEDED must not carry citation_keys={keys}")
            elif status == "SOURCE_IDENTIFIED":
                counts["SOURCE_IDENTIFIED"] += 1
                if not keys and not (isinstance(pe, dict) and pe):
                    errors.append(f"{path.name}:{cid}: SOURCE_IDENTIFIED requires citation_keys or project_evidence")
                for key in keys:
                    if key in ALLOWLIST:
                        continue
                    if key not in bib_keys:
                        errors.append(f"{path.name}:{cid}: unknown citation key `{key}` (not in CE local / candidate bib)")
            else:
                counts["other"] += 1

    print(
        "check_full31_claim_sources:",
        f"SOURCE_NEEDED={counts['SOURCE_NEEDED']}",
        f"SOURCE_IDENTIFIED={counts['SOURCE_IDENTIFIED']}",
        f"other={counts['other']}",
        f"bib_keys={len(bib_keys)}",
    )
    if errors:
        print("FAIL")
        for e in errors:
            print(f" - {e}")
        return 1 if args.check else 0
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
