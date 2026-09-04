#!/usr/bin/env python3
"""Run official W3C EPUBCheck against the Full31 EPUB artifact.

Downloads a pinned EPUBCheck release into tools/cache/ (gitignored) — does not
vendor the JAR in-repo. Distinguishes fatal/error from warning. Does not claim
accessibility certification.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EPUB = ROOT / "preview/full31/technology-landscape-full31-epub.epub"
# Pin exact upstream release (W3C EPUBCheck).
EPUBCHECK_VERSION = os.environ.get("EPUBCHECK_VERSION", "5.2.1")
CACHE = ROOT / "tools" / "cache" / f"epubcheck-{EPUBCHECK_VERSION}"
JAR_NAME = f"epubcheck.jar"
RELEASE_URL = (
    f"https://github.com/w3c/epubcheck/releases/download/"
    f"v{EPUBCHECK_VERSION}/epubcheck-{EPUBCHECK_VERSION}.zip"
)


def find_java() -> str | None:
    return shutil.which("java")


def ensure_epubcheck() -> Path:
    jar = CACHE / JAR_NAME
    if jar.is_file():
        return jar
    CACHE.mkdir(parents=True, exist_ok=True)
    zip_path = CACHE / f"epubcheck-{EPUBCHECK_VERSION}.zip"
    print(f"run_epubcheck: downloading {RELEASE_URL}")
    urllib.request.urlretrieve(RELEASE_URL, zip_path)  # noqa: S310
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(CACHE)
    # Archive root is epubcheck-VERSION/
    extracted = CACHE / f"epubcheck-{EPUBCHECK_VERSION}" / JAR_NAME
    if not extracted.is_file():
        # sometimes nested differently
        candidates = list(CACHE.rglob("epubcheck.jar"))
        if not candidates:
            raise FileNotFoundError("epubcheck.jar not found after extract")
        extracted = candidates[0]
    # Stabilize path
    if extracted.resolve() != jar.resolve():
        shutil.copy2(extracted, jar)
    return jar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--epub",
        type=Path,
        default=DEFAULT_EPUB,
        help="Path to EPUB artifact",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=ROOT / "publication/full31/quality/EPUBCHECK_RESULT.json",
        help="Write machine-readable result",
    )
    parser.add_argument(
        "--allow-unavailable",
        action="store_true",
        help="Exit 0 with explicit limitation if Java/network unavailable",
    )
    args = parser.parse_args()

    result: dict = {
        "tool": "W3C EPUBCheck",
        "version": EPUBCHECK_VERSION,
        "epub": str(args.epub),
        "status": "NOT_RUN",
        "errors": 0,
        "fatal_errors": 0,
        "warnings": 0,
        "usage": 0,
        "limitation": None,
        "command": None,
        "exit_code": None,
    }

    if not args.epub.is_file():
        result["status"] = "MISSING_EPUB"
        result["limitation"] = f"EPUB not found: {args.epub}"
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("run_epubcheck: FAIL — missing EPUB")
        return 1

    java = find_java()
    if not java:
        result["status"] = "TOOLING_UNAVAILABLE"
        result["limitation"] = "Java runtime not found on PATH; EPUBCheck not executed."
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("run_epubcheck: EPUBCheck unavailable (no java)")
        return 0 if args.allow_unavailable else 1

    try:
        jar = ensure_epubcheck()
    except Exception as exc:  # noqa: BLE001
        result["status"] = "DOWNLOAD_FAILED"
        result["limitation"] = f"Could not download/extract EPUBCheck {EPUBCHECK_VERSION}: {exc}"
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("run_epubcheck:", result["limitation"])
        return 0 if args.allow_unavailable else 1

    with tempfile.TemporaryDirectory() as tmp:
        out_json = Path(tmp) / "epubcheck-out.json"
        cmd = [
            java,
            "-jar",
            str(jar),
            str(args.epub),
            "--json",
            str(out_json),
        ]
        result["command"] = " ".join(cmd)
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        result["exit_code"] = proc.returncode
        result["stdout_tail"] = (proc.stdout or "")[-2000:]
        result["stderr_tail"] = (proc.stderr or "")[-2000:]
        if out_json.is_file():
            try:
                payload = json.loads(out_json.read_text(encoding="utf-8"))
                checker = payload.get("checker") or {}
                result["errors"] = int(checker.get("nError") or 0)
                result["fatal_errors"] = int(checker.get("nFatal") or 0)
                result["warnings"] = int(checker.get("nWarning") or 0)
                result["usage"] = int(checker.get("nUsage") or 0)
                result["epubcheck_payload_summary"] = {
                    "path": checker.get("path"),
                    "publicationVersion": (payload.get("publication") or {}).get(
                        "ePubVersion"
                    ),
                }
            except json.JSONDecodeError:
                result["limitation"] = "EPUBCheck JSON output unreadable"

    fatal = result["fatal_errors"] + result["errors"]
    if fatal:
        result["status"] = "FAIL"
    else:
        result["status"] = "PASS"
        if result["warnings"]:
            result["status"] = "PASS_WITH_WARNINGS"

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        f"run_epubcheck: {result['status']} "
        f"(v{EPUBCHECK_VERSION}; errors={result['errors']} "
        f"fatal={result['fatal_errors']} warnings={result['warnings']})"
    )
    print(
        "NOTE: EPUBCheck structural validation is not an accessibility certification."
    )
    return 0 if result["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
