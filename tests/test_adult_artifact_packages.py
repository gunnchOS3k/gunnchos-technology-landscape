"""Negative tests for adult artifact package readiness gates."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ADULT = ROOT / "release-packages" / "adult"


@pytest.fixture
def kindle_pkg(tmp_path: Path) -> Path:
    src = ADULT / "amazon-kindle"
    if not src.is_dir():
        pytest.skip("adult amazon-kindle package missing")
    dest = tmp_path / "amazon-kindle"
    shutil.copytree(src, dest)
    return dest


def _set_readiness(pkg: Path, readiness: str, **extra) -> dict:
    man_path = pkg / "MANIFEST.yaml"
    man = yaml.safe_load(man_path.read_text(encoding="utf-8"))
    man["package_readiness"] = readiness
    man.update(extra)
    man_path.write_text(yaml.safe_dump(man, sort_keys=False), encoding="utf-8")
    return man


def test_stub_hard_fails_when_artifacts_built(kindle_pkg: Path):
    from adult_package_common import NO_STUB_STATES, is_stub_path

    man = _set_readiness(kindle_pkg, "ARTIFACTS_BUILT", blocks=[])
    stubs = [p for p in (kindle_pkg / "artifacts").rglob("*") if p.is_file() and is_stub_path(p)]
    assert stubs, "expected cover stub to remain for this negative case"
    assert man["package_readiness"] in NO_STUB_STATES


def test_ready_for_upload_forbidden_with_owner_cover_block(kindle_pkg: Path):
    from adult_package_common import OWNER_BLOCK_STATES

    man = _set_readiness(
        kindle_pkg,
        "READY_FOR_OWNER_UPLOAD",
        blocks=["BLOCKED_OWNER_COVER"],
    )
    assert set(man["blocks"]) & OWNER_BLOCK_STATES


def test_ready_for_upload_rejects_fake_isbn(kindle_pkg: Path):
    import re
    from adult_package_common import FAKE_ISBN_RE

    man = _set_readiness(kindle_pkg, "READY_FOR_OWNER_UPLOAD", blocks=[], isbn13="9781234567897")
    text = yaml.safe_dump(man)
    assert re.search(FAKE_ISBN_RE, text)


def test_ready_for_upload_rejects_stub_cover_as_final(kindle_pkg: Path):
    man = _set_readiness(kindle_pkg, "READY_FOR_OWNER_UPLOAD", blocks=[])
    for a in man.get("artifacts") or []:
        if "cover" in a.get("path", ""):
            a["final"] = True
            a["artifact_type"] = "STUB"
    (kindle_pkg / "MANIFEST.yaml").write_text(yaml.safe_dump(man, sort_keys=False), encoding="utf-8")
    assert any(
        a.get("final") is True and a.get("artifact_type") == "STUB"
        for a in man.get("artifacts") or []
    )


def test_digital_vs_print_pdf_roles_distinguished():
    df = ADULT / "direct-free" / "MANIFEST.yaml"
    pb = ADULT / "amazon-paperback" / "MANIFEST.yaml"
    if not df.is_file() or not pb.is_file():
        pytest.skip("packages not built yet")
    direct = yaml.safe_load(df.read_text(encoding="utf-8"))
    paper = yaml.safe_load(pb.read_text(encoding="utf-8"))
    roles_d = {a.get("pdf_role") for a in direct.get("artifacts") or [] if a.get("pdf_role")}
    roles_p = {a.get("pdf_role") for a in paper.get("artifacts") or [] if a.get("pdf_role")}
    assert "DIGITAL_ACCESS_PDF" in roles_d
    assert "PRINT_INTERIOR_PDF" in roles_p
    assert "DIGITAL_ACCESS_PDF" not in roles_p
