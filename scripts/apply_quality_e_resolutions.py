#!/usr/bin/env python3
"""Apply Agent QUALITY-E SOURCE_NEEDED resolutions / reframes.

Only attaches verified citation keys added or already present in this wave.
Does not invent DOI/ISBN/page/year. Does not touch publication/gates/gate-3/.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

# claim_id -> citation_keys (status flips to SOURCE_IDENTIFIED)
RESOLUTIONS: dict[str, list[str]] = {
    "CLM-CH08-001": ["mdn-requestanimationframe", "whatwg-html"],
    "CLM-CH09-002": ["iec-62133-2", "ul-2054"],
    "CLM-CH11-006": ["android-ab-ota"],
    "CLM-CH13-003": ["postgresql-mvcc"],
    "CLM-CH13-005": ["nist-sp800-88r1"],
    "CLM-CH17-003": ["itu-r-m2160-2023"],
    "CLM-CH19-003": ["threegpp-tr38821", "kurose-ross-8"],
    "CLM-CH22-004": ["w3c-mediacapture-streams-20251009", "w3c-permissions-20251006"],
}

# Pedagogy-only / no external BoK selected this wave.
REFRAMES_ILLUSTRATIVE: dict[str, dict[str, str]] = {
    "CLM-CH09-003": {
        "text": (
            "Mechanical design choices affect thermals, durability, accessibility of "
            "controls, and repairability (qualitative teaching model; no pinned "
            "industrial-design textbook in this wave)."
        ),
        "wording_boundary": (
            "approved: qualitative teaching model without pinned design BoK | "
            "prohibited: invented ISBN/EVT; shipping Quartet SKUs; Gate 3 PASS"
        ),
    },
    "CLM-CH29-003": {
        "text": (
            "Product-management body-of-knowledge citations are not selected for this "
            "edition; chapter remains pedagogy/synthesis-only without PMI/ISBN claims."
        ),
        "wording_boundary": (
            "approved: pedagogy/synthesis without external PM BoK | "
            "prohibited: fake PMI/ISBN cites"
        ),
    },
}

# Claim text adjustments when resolving meta / over-broad SOURCE_NEEDED wording.
TEXT_UPDATES: dict[str, str] = {
    "CLM-CH22-004": (
        "Camera/microphone sensing is mediated by platform permission and media-capture "
        "models (W3C). Do not invent IMU-fusion ISO/IEEE designations in this wave."
    ),
    "CLM-CH17-003": (
        "6G / IMT-2030 remains a roadmap framework topic (ITU-R M.2160); do not claim "
        "deployed consumer 6G networks as present fact."
    ),
}


def main() -> int:
    chapters = ROOT / "publication" / "full31" / "chapters"
    flipped: list[str] = []
    reframed: list[str] = []
    for path in sorted(chapters.glob("*/CLAIM_PLAN.yaml")):
        data = load_yaml(path) or {}
        claims = data.get("claims") or []
        changed = False
        for claim in claims:
            cid = claim.get("provisional_id")
            if cid in RESOLUTIONS and claim.get("status") == "SOURCE_NEEDED":
                claim["status"] = "SOURCE_IDENTIFIED"
                claim["citation_keys"] = list(RESOLUTIONS[cid])
                if cid in TEXT_UPDATES:
                    claim["text"] = TEXT_UPDATES[cid]
                flipped.append(cid)
                changed = True
            if cid in REFRAMES_ILLUSTRATIVE and claim.get("status") == "SOURCE_NEEDED":
                meta = REFRAMES_ILLUSTRATIVE[cid]
                claim["status"] = "ILLUSTRATIVE_ONLY"
                claim["claim_class"] = "illustrative"
                claim["citation_keys"] = []
                claim["text"] = meta["text"]
                claim["wording_boundary"] = meta["wording_boundary"]
                reframed.append(cid)
                changed = True
        if changed:
            data["claims"] = claims
            path.write_text(dump_yaml(data), encoding="utf-8")
    print(f"flipped={len(flipped)}")
    for cid in flipped:
        print(f"  {cid} -> {RESOLUTIONS[cid]}")
    print(f"reframed_illustrative={len(reframed)} {reframed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
