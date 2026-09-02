#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402


def main() -> int:
    errors: list[str] = []
    data = load_yaml(ROOT / "glossary/glossary.yaml")
    entries = data.get("entries") or []
    ids = [e.get("id") for e in entries]
    if len(ids) != len(set(ids)):
        errors.append("duplicate glossary ids")
    by_id = {e["id"]: e for e in entries if e.get("id")}
    for e in entries:
        eid = e.get("id")
        for field in ("plain_definition", "technical_definition", "experience_benefit"):
            if not e.get(field):
                errors.append(f"{eid}: missing {field}")
        analogy = e.get("analogy") or {}
        if not analogy.get("explicitly_labeled"):
            errors.append(f"{eid}: analogy must be explicitly labeled")
        for rel in e.get("related") or []:
            if rel not in by_id and rel not in {"permanent-storage", "polling", "user-interface", "application-plugin", "audio-feedback", "display-panel"}:
                # related may point outside; warn only if self-circular definition
                pass
        plain = (e.get("plain_definition") or "").lower()
        if eid and eid.replace("-", " ") in plain and "managed by the" in plain:
            errors.append(f"{eid}: possible circular definition")
    # CH02 introduced terms must exist
    meta = load_yaml(ROOT / "book/chapters/ch02/metadata.yaml")
    for term in ((meta.get("concepts") or {}).get("introduced") or []):
        if term not in by_id:
            errors.append(f"CH02 introduced term missing from glossary: {term}")
    if errors:
        print("validate_glossary: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("validate_glossary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
