#!/usr/bin/env python3
"""Validate book/terminology.yaml against glossary and misconception matrix."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REQUIRED_TERM_FIELDS = (
    "id",
    "term",
    "plain_definition",
    "deeper_definition",
    "first_introduced",
    "common_misconception",
    "not_the_same_as",
)

HIGH_RISK_IDS = {
    "system",
    "component",
    "latency",
    "throughput",
    "jitter",
    "reliability",
    "qoe",
    "cpu",
    "core",
    "process",
    "thread",
    "memory",
    "cache",
    "storage",
    "firmware",
    "operating-system",
    "api",
    "runtime",
    "lan",
    "internet",
    "dns",
    "wifi",
    "cellular",
    "edge",
    "cloud",
    "spectrum",
    "channel",
    "antenna",
    "beamforming",
    "mimo",
    "ntn",
    "service-continuity",
    "model",
    "training",
    "inference",
    "generative-ai",
    "authentication",
    "authorization",
    "privacy",
    "security",
    "accessibility",
    "digital-equity",
    "simulation",
    "digital-twin",
    "reproducibility",
}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    term_path = ROOT / "book" / "terminology.yaml"
    if not term_path.exists():
        print("validate_terminology: FAIL")
        print(" - missing book/terminology.yaml")
        return 1

    data = load_yaml(term_path)
    terms = data.get("terms") or []
    if not terms:
        errors.append("terminology registry has no terms")

    ids = [t.get("id") for t in terms]
    if len(ids) != len(set(ids)):
        errors.append("duplicate terminology ids")

    by_id = {t["id"]: t for t in terms if t.get("id")}

    missing_high = sorted(HIGH_RISK_IDS - set(by_id))
    if missing_high:
        errors.append(f"missing high-risk terms: {', '.join(missing_high)}")

    gloss = load_yaml(ROOT / "glossary" / "glossary.yaml")
    gloss_ids = {e.get("id") for e in (gloss.get("entries") or []) if e.get("id")}

    alias_map: dict[str, str] = {}
    collisions: list[str] = []

    for t in terms:
        tid = t.get("id")
        for field in REQUIRED_TERM_FIELDS:
            if t.get(field) in (None, "", []):
                errors.append(f"{tid}: missing {field}")
        if not t.get("later_reinforcement") and t.get("later_reinforcement") is None:
            # allow empty list, but key should exist
            if "later_reinforcement" not in t:
                errors.append(f"{tid}: missing later_reinforcement")

        gid = t.get("glossary_id")
        if gid and gid not in gloss_ids:
            errors.append(f"{tid}: glossary_id '{gid}' not in glossary")

        keys = [tid, (t.get("term") or "").lower()]
        keys += [a.lower() for a in (t.get("aliases") or [])]
        keys += [a.lower() for a in (t.get("acronyms") or [])]
        for k in keys:
            k = (k or "").strip().lower()
            if not k:
                continue
            if k in alias_map and alias_map[k] != tid:
                collisions.append(f"alias '{k}' -> {alias_map[k]} and {tid}")
            else:
                alias_map[k] = tid

        for rel in t.get("not_the_same_as") or []:
            # Relations may point to glossary-only or supporting ids.
            if rel in by_id and tid in (by_id[rel].get("aliases") or []):
                errors.append(f"{tid}: not_the_same_as '{rel}' but also listed as its alias")

    if collisions:
        errors.append(f"alias collisions ({len(collisions)}): " + "; ".join(collisions[:20]))

    matrix = ROOT / "publication" / "full31" / "quality" / "MISCONCEPTION_MATRIX.md"
    if not matrix.exists():
        errors.append("missing publication/full31/quality/MISCONCEPTION_MATRIX.md")
    else:
        text = matrix.read_text(encoding="utf-8")
        required_rows = [
            "Internet ≠ Wi-Fi",
            "cloud ≠ Internet",
            "authentication ≠ authorization",
            "privacy ≠ security",
            "latency ≠ throughput",
            "simulation ≠ measurement",
            "digital twin ≠ any model",
            "storage ≠ memory",
            "process ≠ thread",
            "accessibility ≠ convenience",
            "portfolio evidence ≠ job guarantee",
        ]
        for row in required_rows:
            if row not in text:
                errors.append(f"misconception matrix missing row: {row}")

    # Acronym registry presence for key acronyms
    acr_path = ROOT / "glossary" / "acronym_registry.yaml"
    if acr_path.exists():
        acr = load_yaml(acr_path)
        present = {a.get("acronym") for a in (acr.get("acronyms") or [])}
        for needed in ("CPU", "GPU", "RAM", "API", "DNS", "MIMO", "NTN", "QoE", "AI", "ML"):
            if needed not in present:
                warnings.append(f"acronym registry missing {needed}")
    else:
        warnings.append("glossary/acronym_registry.yaml missing")

    print(f"terminology terms: {len(terms)}")
    print(f"high-risk covered: {len(HIGH_RISK_IDS & set(by_id))}/{len(HIGH_RISK_IDS)}")
    print(f"alias keys: {len(alias_map)}")
    print(f"alias collisions: {len(collisions)}")
    print(f"glossary-linked terms: {sum(1 for t in terms if t.get('glossary_id'))}")
    print(f"terminology-only terms: {sum(1 for t in terms if not t.get('glossary_id'))}")
    print(f"misconception matrix: {matrix.relative_to(ROOT)}")

    if warnings:
        print("validate_terminology: WARNINGS")
        for w in warnings:
            print(" -", w)

    if errors:
        print("validate_terminology: FAIL")
        for e in errors:
            print(" -", e)
        return 1

    print("validate_terminology: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
