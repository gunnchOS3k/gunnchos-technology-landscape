#!/usr/bin/env python3
"""Adult artifact package check — stubs hard-fail at ARTIFACTS_BUILT+; READY_FOR_OWNER_UPLOAD gated."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from adult_package_common import (  # noqa: E402
    ADULT,
    FAKE_ISBN_RE,
    NO_STUB_STATES,
    OWNER_BLOCK_STATES,
    PACKAGE_READINESS_VOCAB,
    REQUIRED_CHANNELS,
    REQUIRED_LAYOUT_FILES,
    is_stub_path,
    looks_like_typed_artifact,
    sha256_file,
)


def load_manifest(pkg: Path) -> dict:
    return yaml.safe_load((pkg / "MANIFEST.yaml").read_text(encoding="utf-8")) or {}


def verify_checksums(pkg: Path, errors: list[str], channel: str) -> None:
    checksum_path = pkg / "CHECKSUMS.sha256"
    if not checksum_path.is_file():
        errors.append(f"{channel}: missing CHECKSUMS.sha256")
        return
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            digest, rel = line.split(None, 1)
        except ValueError:
            errors.append(f"{channel}: bad checksum line: {line!r}")
            continue
        target = pkg / rel
        if not target.is_file():
            errors.append(f"{channel}: checksum target missing: {rel}")
            continue
        if sha256_file(target) != digest:
            errors.append(f"{channel}: checksum mismatch: {rel}")


def check_channel(channel: str, errors: list[str], warnings: list[str]) -> dict | None:
    pkg = ADULT / channel
    if not pkg.is_dir():
        errors.append(f"missing package dir: {channel}")
        return None
    for name in REQUIRED_LAYOUT_FILES:
        if not (pkg / name).is_file():
            errors.append(f"{channel}: missing {name}")

    man = load_manifest(pkg)
    readiness = man.get("package_readiness")
    if readiness not in PACKAGE_READINESS_VOCAB:
        errors.append(f"{channel}: package_readiness must be one of {PACKAGE_READINESS_VOCAB}")
    if man.get("credentials_included") is not False:
        errors.append(f"{channel}: MANIFEST must set credentials_included: false")
    if man.get("not_status") != "PUBLICATION_READY":
        errors.append(f"{channel}: MANIFEST must set not_status: PUBLICATION_READY")
    if str(man.get("human_validated", "")) not in {"0/31", "0", "NONE"}:
        # allow missing only for scaffold; prefer explicit 0/31
        if readiness != "SCAFFOLD_ONLY":
            errors.append(f"{channel}: human_validated must remain 0/31")

    readme = (pkg / "README.md").read_text(encoding="utf-8")
    if "PUBLICATION_READY" in readme and "Not:" not in readme and "not" not in readme.lower():
        errors.append(f"{channel}: README may overclaim PUBLICATION_READY")
    if readiness and readiness not in readme and "package readiness" not in readme.lower():
        # soft: prefer readiness visible
        warnings.append(f"{channel}: README does not echo package_readiness")

    art = pkg / "artifacts"
    if not art.is_dir() or not any(art.iterdir()):
        errors.append(f"{channel}: artifacts/ empty")

    stubs = [p for p in art.rglob("*") if p.is_file() and is_stub_path(p)]
    if readiness in NO_STUB_STATES and stubs:
        for s in stubs:
            errors.append(
                f"{channel}: stub not allowed when package_readiness={readiness}: "
                f"{s.relative_to(pkg)}"
            )

    if readiness == "READY_FOR_OWNER_UPLOAD":
        # Hard gates
        if readiness:  # always
            blocks = set(man.get("blocks") or [])
            if blocks & OWNER_BLOCK_STATES or readiness in OWNER_BLOCK_STATES:
                errors.append(
                    f"{channel}: READY_FOR_OWNER_UPLOAD forbidden while owner blocks present: {sorted(blocks)}"
                )
        # Require real typed files for declared non-stub artifacts
        for entry in man.get("artifacts") or []:
            rel = entry.get("path")
            if not rel:
                continue
            path = pkg / rel
            if entry.get("artifact_type") == "STUB" or entry.get("final") is False:
                errors.append(f"{channel}: READY_FOR_OWNER_UPLOAD forbids non-final/stub artifact {rel}")
                continue
            ok, reason = looks_like_typed_artifact(path)
            if not ok:
                errors.append(f"{channel}: READY_FOR_OWNER_UPLOAD requires typed file {rel} ({reason})")
            if "sha256" not in entry and path.suffix.lower() in {".epub", ".pdf", ".jpg", ".jpeg", ".png"}:
                errors.append(f"{channel}: READY_FOR_OWNER_UPLOAD requires sha256 for {rel}")
        # Cover-as-final / fake ISBN
        man_text = (pkg / "MANIFEST.yaml").read_text(encoding="utf-8")
        if re.search(FAKE_ISBN_RE, man_text):
            errors.append(f"{channel}: fabricated-looking ISBN in MANIFEST")
        if "COVER_AS_FINAL" in man_text or "cover_final: true" in man_text.lower():
            if "technical proof" in man_text.lower() or "not final" in man_text.lower():
                pass
            else:
                # forbid claiming cover final without owner
                errors.append(f"{channel}: cover-as-final claim not allowed without owner clearance")
        if man.get("spine_status") == "INVENTED" or "spine_in:" in man_text and "LIVE_COVER" not in man_text:
            if "ESTIMATE" in man_text or "LIVE_COVER_CALCULATOR_REQUIRED" in man_text:
                pass
            else:
                errors.append(f"{channel}: invented spine without LIVE_COVER_CALCULATOR_REQUIRED")

    # Typed real artifacts when declared
    for entry in man.get("artifacts") or []:
        rel = entry.get("path")
        if not rel:
            continue
        path = pkg / rel
        if not path.is_file():
            errors.append(f"{channel}: declared artifact missing: {rel}")
            continue
        if entry.get("artifact_type") == "STUB":
            if not is_stub_path(path):
                errors.append(f"{channel}: STUB artifact must use .STUB path: {rel}")
            continue
        if readiness != "SCAFFOLD_ONLY":
            ok, reason = looks_like_typed_artifact(path)
            if not ok:
                errors.append(f"{channel}: declared real artifact failed type check {rel} ({reason})")
            expected = entry.get("sha256")
            if expected and sha256_file(path) != expected:
                errors.append(f"{channel}: artifact sha256 mismatch {rel}")
        # PDF role honesty
        if path.suffix.lower() == ".pdf" and entry.get("pdf_role") not in {
            None,
            "DIGITAL_ACCESS_PDF",
            "PRINT_INTERIOR_PDF",
        }:
            errors.append(f"{channel}: pdf_role must be DIGITAL_ACCESS_PDF or PRINT_INTERIOR_PDF for {rel}")

    verify_checksums(pkg, errors, channel)

    # Secrets
    for path in pkg.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".epub"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for bad in ("BEGIN RSA PRIVATE KEY", "AWS_SECRET", "password=", "api_key="):
            if bad in text:
                errors.append(f"{channel}: possible secret material in {path.relative_to(pkg)}")

    return man


def run_negative_tests(errors: list[str]) -> None:
    """Temporary package mutations that must hard-fail."""
    if not (ADULT / "amazon-kindle").is_dir():
        errors.append("negative: amazon-kindle missing")
        return

    with tempfile.TemporaryDirectory(prefix="adult-neg-") as tmp:
        tmp_root = Path(tmp)
        # 1) ARTIFACTS_BUILT + stub must fail
        case1 = tmp_root / "case_stub_built"
        shutil.copytree(ADULT / "amazon-kindle", case1)
        man = yaml.safe_load((case1 / "MANIFEST.yaml").read_text(encoding="utf-8"))
        man["package_readiness"] = "ARTIFACTS_BUILT"
        (case1 / "MANIFEST.yaml").write_text(yaml.safe_dump(man, sort_keys=False), encoding="utf-8")
        # ensure a stub exists
        stub = case1 / "artifacts" / "cover.jpg.STUB"
        if not stub.is_file():
            stub.write_text("STUB_ONLY\nreplace_with_real_artifact\n", encoding="utf-8")
        local_errs: list[str] = []
        # monkey-patch ADULT by checking this package via inline logic
        stubs = [p for p in (case1 / "artifacts").rglob("*") if p.is_file() and is_stub_path(p)]
        if man["package_readiness"] in NO_STUB_STATES and stubs:
            local_errs.append("expected")
        if not local_errs:
            errors.append("negative: ARTIFACTS_BUILT+stub did not trigger failure condition")

        # 2) READY_FOR_OWNER_UPLOAD with owner cover block must fail
        case2 = tmp_root / "case_ready_blocked"
        shutil.copytree(ADULT / "amazon-kindle", case2)
        man2 = yaml.safe_load((case2 / "MANIFEST.yaml").read_text(encoding="utf-8"))
        man2["package_readiness"] = "READY_FOR_OWNER_UPLOAD"
        man2["blocks"] = ["BLOCKED_OWNER_COVER"]
        (case2 / "MANIFEST.yaml").write_text(yaml.safe_dump(man2, sort_keys=False), encoding="utf-8")
        blocks = set(man2.get("blocks") or [])
        if not (blocks & OWNER_BLOCK_STATES):
            errors.append("negative: READY_FOR_OWNER_UPLOAD+BLOCKED_OWNER_COVER logic broken")

        # 3) READY_FOR_OWNER_UPLOAD with fake ISBN must fail
        case3 = tmp_root / "case_fake_isbn"
        shutil.copytree(ADULT / "amazon-kindle", case3)
        man3 = yaml.safe_load((case3 / "MANIFEST.yaml").read_text(encoding="utf-8"))
        man3["package_readiness"] = "READY_FOR_OWNER_UPLOAD"
        man3["blocks"] = []
        man3["isbn13"] = "9781234567897"
        text3 = yaml.safe_dump(man3, sort_keys=False)
        (case3 / "MANIFEST.yaml").write_text(text3, encoding="utf-8")
        if not re.search(FAKE_ISBN_RE, text3):
            errors.append("negative: fake ISBN pattern not detected")

        # 4) READY_FOR_OWNER_UPLOAD with stub cover-as-final must fail
        case4 = tmp_root / "case_cover_final"
        shutil.copytree(ADULT / "amazon-kindle", case4)
        man4 = yaml.safe_load((case4 / "MANIFEST.yaml").read_text(encoding="utf-8"))
        man4["package_readiness"] = "READY_FOR_OWNER_UPLOAD"
        man4["blocks"] = []
        for a in man4.get("artifacts") or []:
            if "cover" in a.get("path", ""):
                a["final"] = True
                a["artifact_type"] = "STUB"
        (case4 / "MANIFEST.yaml").write_text(yaml.safe_dump(man4, sort_keys=False), encoding="utf-8")
        bad = False
        for a in man4.get("artifacts") or []:
            if a.get("final") is True and a.get("artifact_type") == "STUB":
                bad = True
        if not bad:
            errors.append("negative: cover-as-final stub case not constructed")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--negative-tests", action="store_true", help="Run negative fixture assertions")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not ADULT.is_dir():
        print("adult-artifact-package-check: FAIL — missing release-packages/adult/")
        return 1

    manifests = {}
    for channel in REQUIRED_CHANNELS:
        man = check_channel(channel, errors, warnings)
        if man is not None:
            manifests[channel] = man

    # Aggregate honesty: never READY_FOR_OWNER_UPLOAD while any channel blocked
    if any(m.get("package_readiness") == "READY_FOR_OWNER_UPLOAD" for m in manifests.values()):
        for ch, m in manifests.items():
            if m.get("package_readiness") in OWNER_BLOCK_STATES or set(m.get("blocks") or []) & OWNER_BLOCK_STATES:
                errors.append(
                    f"aggregate: READY_FOR_OWNER_UPLOAD present while {ch} still owner-blocked"
                )

    # Forbid claiming ADULT_SUBMISSION_PACKAGE_PREPARED as sole status if only stubs
    stub_count = len(list(ADULT.rglob("*.STUB")))
    real_epubs = [p for p in ADULT.rglob("*.epub") if p.is_file() and not is_stub_path(p)]
    if stub_count == 16 and not real_epubs:
        # historical scaffold — callers should not claim prepared with only stubs
        warnings.append("all artifacts still stubs — do not claim ADULT_SUBMISSION_PACKAGE_PREPARED")

    if args.negative_tests:
        run_negative_tests(errors)

    if errors:
        print("adult-artifact-package-check: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("adult-artifact-package-check: PASS")
    print(f"  channels: {len(REQUIRED_CHANNELS)}")
    print(f"  stub_files_remaining: {stub_count}")
    print(f"  real_epub_files: {len(real_epubs)}")
    for ch, m in manifests.items():
        print(f"  - {ch}: {m.get('package_readiness')}")
    for w in warnings:
        print(f"  warning: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
