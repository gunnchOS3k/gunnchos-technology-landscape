#!/usr/bin/env python3
"""Shared vocabulary and helpers for adult release packages."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADULT = ROOT / "release-packages" / "adult"

PACKAGE_READINESS_VOCAB = [
    "SCAFFOLD_ONLY",
    "ARTIFACTS_BUILT",
    "VALIDATED_LOCALLY",
    "BLOCKED_OWNER_COVER",
    "BLOCKED_OWNER_METADATA",
    "BLOCKED_OWNER_ISBN",
    "BLOCKED_HUMAN_REVIEW",
    "READY_FOR_OWNER_UPLOAD",
]

# States that must not retain *.STUB artifact bytes.
NO_STUB_STATES = frozenset(
    {
        "ARTIFACTS_BUILT",
        "VALIDATED_LOCALLY",
        "READY_FOR_OWNER_UPLOAD",
    }
)

# States that forbid READY_FOR_OWNER_UPLOAD aggregation.
OWNER_BLOCK_STATES = frozenset(
    {
        "BLOCKED_OWNER_COVER",
        "BLOCKED_OWNER_METADATA",
        "BLOCKED_OWNER_ISBN",
        "BLOCKED_HUMAN_REVIEW",
        "SCAFFOLD_ONLY",
    }
)

REQUIRED_CHANNELS = [
    "amazon-kindle",
    "amazon-paperback",
    "amazon-hardcover",
    "apple-books",
    "google-play-books",
    "kobo",
    "direct-free",
    "libraries",
]

REQUIRED_LAYOUT_FILES = [
    "README.md",
    "MANIFEST.yaml",
    "CHECKSUMS.sha256",
    "validation-stub.md",
    "HUMAN_CHECKLIST.md",
]

# Magic / type checks for real artifacts (not stubs).
TYPED_ARTIFACT_RULES = {
    ".epub": {"magic_prefixes": (b"PK\x03\x04",), "role_hint": "EPUB"},
    ".pdf": {"magic_prefixes": (b"%PDF",), "role_hint": "PDF"},
    ".jpg": {"magic_prefixes": (b"\xff\xd8\xff",), "role_hint": "JPEG"},
    ".jpeg": {"magic_prefixes": (b"\xff\xd8\xff",), "role_hint": "JPEG"},
    ".png": {"magic_prefixes": (b"\x89PNG\r\n\x1a\n",), "role_hint": "PNG"},
    ".yaml": {"magic_prefixes": (), "role_hint": "YAML"},
    ".yml": {"magic_prefixes": (), "role_hint": "YAML"},
}

# Verified KDP B&W white page ranges from PLATFORM_REQUIREMENTS / PRINT research.
KDP_PAGE_LIMITS = {
    "6x9": {"paperback_bw_white": (24, 828), "hardcover_bw_white": (75, 550)},
    "7x10": {"paperback_bw_white": (24, 828), "hardcover_bw_white": (75, 550)},
    "8.5x11": {"paperback_bw_white": (24, 590), "hardcover_bw_white": None},
}

FAKE_ISBN_RE = r"\b97[89]\d{10}\b"


def sha256_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_stub_path(path: Path) -> bool:
    return path.name.endswith(".STUB") or path.suffix.upper() == ".STUB"


def looks_like_typed_artifact(path: Path) -> tuple[bool, str]:
    """Return (ok, reason). Stubs always fail."""
    if is_stub_path(path):
        return False, "stub_extension"
    if not path.is_file() or path.stat().st_size < 16:
        return False, "missing_or_tiny"
    data = path.read_bytes()[:16]
    # Text marker used by old stubs
    if data.startswith(b"STUB_ONLY") or b"replace_with_real_artifact" in data[:200]:
        return False, "stub_payload"
    suffix = path.suffix.lower()
    rules = TYPED_ARTIFACT_RULES.get(suffix)
    if not rules:
        return True, "untyped_ok"
    prefixes = rules["magic_prefixes"]
    if not prefixes:
        # YAML / text: ensure not stub marker
        text = path.read_text(encoding="utf-8", errors="ignore")[:200]
        if "STUB_ONLY" in text or "replace_with_real_artifact" in text:
            return False, "stub_payload"
        return True, "text_ok"
    if any(data.startswith(p) for p in prefixes):
        return True, "magic_ok"
    return False, f"bad_magic_for_{suffix}"


def eligibility_for_pages(trim: str, page_count: int, binding: str) -> dict:
    limits = KDP_PAGE_LIMITS.get(trim)
    if not limits:
        return {
            "trim": trim,
            "binding": binding,
            "page_count": page_count,
            "eligible": False,
            "reason": "UNKNOWN_TRIM",
        }
    key = "paperback_bw_white" if binding == "paperback" else "hardcover_bw_white"
    band = limits.get(key)
    if band is None:
        return {
            "trim": trim,
            "binding": binding,
            "page_count": page_count,
            "eligible": False,
            "reason": "HARDCOVER_NOT_IN_KDP_TABLE_FOR_TRIM",
            "verified_band": None,
        }
    lo, hi = band
    ok = lo <= page_count <= hi
    return {
        "trim": trim,
        "binding": binding,
        "page_count": page_count,
        "eligible": ok,
        "verified_band": f"{lo}-{hi}",
        "reason": "WITHIN_VERIFIED_KDP_BAND" if ok else "OUTSIDE_VERIFIED_KDP_BAND",
    }
