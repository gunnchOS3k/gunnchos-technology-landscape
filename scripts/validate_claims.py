#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

ALLOWED = {
    "general-knowledge",
    "textbook",
    "standard",
    "peer-reviewed",
    "repository-implemented",
    "repository-documented",
    "repository-tested",
    "measured",
    "simulated",
    "illustrative",
    "planned",
    "hypothesis",
}

STATUS_LANG = {
    "planned": [r"\bcurrently supports\b", r"\bimplements\b", r"\bachieves\b", r"\bprovides\b"],
    "simulated": [r"\bdeployed\b", r"\bin production\b", r"\bmeasured in the field\b"],
    "repository-tested": [r"\bindependently validated\b", r"\bfield proven\b"],
}


def main() -> int:
    errors: list[str] = []
    data = load_yaml(ROOT / "evidence/claim_registry.yaml")
    claims = data.get("claims") or []
    ids = []
    for c in claims:
        cid = c.get("claim_id")
        ids.append(cid)
        if c.get("classification") not in ALLOWED:
            errors.append(f"{cid}: invalid classification {c.get('classification')}")
        if c.get("scope") == "project-specific":
            src = c.get("source") or {}
            if not src.get("repository") and c.get("classification") not in {"illustrative", "planned", "hypothesis"}:
                # illustrative may be local publication path
                if not src.get("path"):
                    errors.append(f"{cid}: project-specific claim missing source")
            if src.get("branch") and src.get("branch") != "main" and c.get("classification") in {
                "repository-implemented",
                "repository-tested",
            }:
                # allow publication branch only for illustrative local claims
                if src.get("repository", "").endswith("gunnchos-technology-landscape") and c.get("classification") == "illustrative":
                    pass
                else:
                    errors.append(f"{cid}: non-main evidence without explicit non-main label")
        text = (c.get("text") or "") + " " + ((c.get("wording") or {}).get("approved") or "")
        for bad in (c.get("wording") or {}).get("prohibited") or []:
            if bad.lower() in text.lower():
                errors.append(f"{cid}: approved text contains prohibited wording '{bad}'")
        for pat in STATUS_LANG.get(c.get("classification"), []):
            if re.search(pat, text, flags=re.I):
                # only fail if sentence lacks requirement/future cue — keep simple/honest
                if not re.search(r"requirement|planned|future|target|illustrative|simulated", text, flags=re.I):
                    errors.append(f"{cid}: suspicious status language for {c.get('classification')}: {pat}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate claim_id values")
    if errors:
        print("validate_claims: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_claims: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
