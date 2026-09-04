#!/usr/bin/env python3
"""Cover geometry helpers for adult distribution (no marketing art generation)."""
from __future__ import annotations

import argparse
import json


def ebook_canvas(platform: str = "kdp_ideal") -> dict:
    presets = {
        "kdp_ideal": {"width_px": 1600, "height_px": 2560, "colorspace": "RGB"},
        "kdp_minimum": {"width_px": 625, "height_px": 1000, "colorspace": "RGB"},
        "apple_min_shortest": {"width_px": 1400, "height_px": 2240, "colorspace": "RGB"},
        "google_min": {"width_px": 640, "height_px": 1024, "colorspace": "RGB"},
    }
    if platform not in presets:
        raise SystemExit(f"unknown platform preset: {platform}")
    return {"preset": platform, **presets[platform]}


def print_wrap_inches(
    trim_w: float,
    trim_h: float,
    page_count: int,
    paper: str = "white",
    bleed: float = 0.125,
) -> dict:
    """Placeholder wrap math. Spine inches require live KDP Cover Calculator."""
    # Conservative white-paper approximate only — NOT official.
    # Marked as estimate; owner must replace with calculator output.
    approx_spine = round(page_count * 0.002252, 4)  # common indie rule-of-thumb; NOT official
    wrap_w = bleed + trim_w + approx_spine + trim_w + bleed
    wrap_h = bleed + trim_h + bleed
    return {
        "trim_in": [trim_w, trim_h],
        "bleed_in": bleed,
        "page_count": page_count,
        "paper": paper,
        "spine_in_ESTIMATE_ONLY": approx_spine,
        "spine_status": "LIVE_COVER_CALCULATOR_REQUIRED",
        "wrap_width_in_ESTIMATE_ONLY": round(wrap_w, 4),
        "wrap_height_in": round(wrap_h, 4),
        "warning": "Do not use ESTIMATE spine for final upload; use KDP Cover Calculator (LIVE_COVER_CALCULATOR_REQUIRED).",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("ebook")
    e.add_argument("--preset", default="kdp_ideal")
    p = sub.add_parser("print-wrap")
    p.add_argument("--trim-w", type=float, default=6.0)
    p.add_argument("--trim-h", type=float, default=9.0)
    p.add_argument("--pages", type=int, required=True)
    p.add_argument("--paper", default="white")
    args = ap.parse_args()
    if args.cmd == "ebook":
        print(json.dumps(ebook_canvas(args.preset), indent=2))
    else:
        print(json.dumps(print_wrap_inches(args.trim_w, args.trim_h, args.pages, args.paper), indent=2))


if __name__ == "__main__":
    main()
