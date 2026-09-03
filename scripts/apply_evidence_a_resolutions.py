#!/usr/bin/env python3
"""Apply Agent EVIDENCE-A SOURCE_NEEDED → SOURCE_IDENTIFIED resolutions.

Only attaches verified citation keys already present or added in this wave.
Does not invent DOI/ISBN/page/year. Does not touch publication/gates/gate-3/.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

# claim_id -> citation_keys to attach (status flips to SOURCE_IDENTIFIED)
RESOLUTIONS: dict[str, list[str]] = {
    # CH03 performance literacy
    "CLM-CH03-001": ["saltzer-kaashoek", "mdn-performance", "iso-iec-25010-2023"],
    "CLM-CH03-002": ["iso-iec-25010-2023", "itu-t-p10-g100"],
    # CH05 digital foundations
    "CLM-CH05-001": ["patterson-hennessy"],
    "CLM-CH05-002": ["patterson-hennessy"],
    "CLM-CH05-003": ["patterson-hennessy"],
    # CH06/CH07 architecture
    "CLM-CH06-002": ["patterson-hennessy", "patterson-hennessy-riscv"],
    "CLM-CH07-002": ["patterson-hennessy", "tanenbaum-bos"],
    # CH08 media capture (displays hitching left SOURCE_NEEDED)
    "CLM-CH08-002": ["w3c-mediacapture-streams-20251009"],
    # CH09 power/thermal
    "CLM-CH09-001": ["linux-cpu-freq"],
    # CH10 interconnects
    "CLM-CH10-001": ["patterson-hennessy"],
    "CLM-CH10-002": ["patterson-hennessy"],
    "CLM-CH10-003": ["patterson-hennessy"],
    # CH11 boot/trust
    "CLM-CH11-003": ["uefi-secure-boot-2.10"],
    "CLM-CH11-004": ["tcg-pc-client-pfp-1.06"],
    # CH12 scheduling diagnosis
    "CLM-CH12-004": ["tanenbaum-bos", "linux-scheduler"],
    # CH14 API contracts / WCAG dual-key repair on adjacent claim
    "CLM-CH14-002": ["semver-2.0.0", "saltzer-kaashoek"],
    # CH15 cloud/edge/isolation
    "CLM-CH15-001": ["tanenbaum-bos", "oci-runtime-spec"],
    "CLM-CH15-002": ["nist-sp800-145", "nist-sp500-325"],
    "CLM-CH15-003": ["tanenbaum-bos", "oci-runtime-spec"],
    "CLM-CH15-004": ["nist-sp800-145", "ieee80211-2020", "threegpp-ts23501"],
    # CH16 DNS / access vs Internet
    "CLM-CH16-004": ["rfc1034", "rfc1035", "kurose-ross-8"],
    "CLM-CH16-005": ["ieee80211-2020", "threegpp-ts23501", "rfc791"],
    # CH17 radio access generations
    "CLM-CH17-001": ["ieee80211-2020", "threegpp-ts23501", "kurose-ross-8"],
    "CLM-CH17-002": ["threegpp-ts23501"],
    "CLM-CH17-004": ["threegpp-ts23501", "kurose-ross-8"],
    # CH18 radio physics survey
    "CLM-CH18-001": ["ieee80211-2020", "kurose-ross-8"],
    "CLM-CH18-002": ["ieee80211-2020"],
    "CLM-CH18-003": ["ieee80211-2020", "kurose-ross-8"],
    # CH19 NTN / continuity (orbit latency numbers + marketing modes remain needed)
    "CLM-CH19-001": ["threegpp-ts23501"],
    "CLM-CH19-002": ["itu-t-p10-g100", "itu-t-g1011", "threegpp-ts23501"],
    # CH20 Stability / QoE
    "CLM-CH20-001": ["iso-iec-25010-2023", "itu-t-p10-g100"],
    "CLM-CH20-002": ["itu-t-p10-g100", "itu-t-g1011", "mdn-performance"],
    "CLM-CH20-003": ["itu-t-g1011", "iso-iec-25010-2023"],
    "CLM-CH20-004": ["itu-t-p10-g100", "mdn-performance"],
    # CH25 ICT access stats
    "CLM-CH25-003": ["itu-facts-figures-2025"],
    # CH26/27/28 official docs / standards
    "CLM-CH26-001": ["git-scm-docs"],
    "CLM-CH27-003": ["otel-signals"],
    "CLM-CH28-002": ["iso-23247-1-2021"],
}

# Also repair undated WCAG shortcut on an already-identified claim (dual-key discipline).
WCAG_REPAIRS: dict[str, list[str]] = {
    "CLM-CH14-004": ["wcag22-20231005", "wcag22-20241212"],
}


def main() -> int:
    chapters = ROOT / "publication" / "full31" / "chapters"
    flipped: list[str] = []
    repaired: list[str] = []
    for path in sorted(chapters.glob("*/CLAIM_PLAN.yaml")):
        data = load_yaml(path) or {}
        claims = data.get("claims") or []
        changed = False
        for claim in claims:
            cid = claim.get("provisional_id")
            if cid in RESOLUTIONS and claim.get("status") == "SOURCE_NEEDED":
                claim["status"] = "SOURCE_IDENTIFIED"
                claim["citation_keys"] = list(RESOLUTIONS[cid])
                flipped.append(cid)
                changed = True
            if cid in WCAG_REPAIRS and claim.get("status") == "SOURCE_IDENTIFIED":
                if claim.get("citation_keys") != WCAG_REPAIRS[cid]:
                    claim["citation_keys"] = list(WCAG_REPAIRS[cid])
                    repaired.append(cid)
                    changed = True
        if changed:
            data["claims"] = claims
            path.write_text(dump_yaml(data), encoding="utf-8")
    print(f"flipped={len(flipped)}")
    for cid in flipped:
        print(f"  {cid} -> {RESOLUTIONS[cid]}")
    print(f"wcag_repaired={len(repaired)} {repaired}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
