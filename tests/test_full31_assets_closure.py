from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def test_assets_check_passes_on_current_manuscript():
    proc = subprocess.run(
        [PY, str(ROOT / "scripts/validate_full31_assets.py"), "--check"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS" in proc.stdout


def test_unresolved_figure_ref_fails_assets_check(tmp_path: Path):
    """Negative: dangling reader-facing FIG ref must fail CI."""
    import shutil

    # Use a temporary copy of one chapter with a fake figure id injected
    chapter = ROOT / "book/chapters/ch24/chapter.md"
    text = chapter.read_text(encoding="utf-8")
    poisoned = text + "\n\n**FIG-CH24-999** is an unresolved fake figure.\n"
    # Run validator logic by temporarily writing — restore afterward
    backup = chapter.read_text(encoding="utf-8")
    try:
        chapter.write_text(poisoned, encoding="utf-8")
        proc = subprocess.run(
            [PY, str(ROOT / "scripts/validate_full31_assets.py"), "--check"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        assert proc.returncode != 0, proc.stdout + proc.stderr
        assert "FIG-CH24-999" in (proc.stdout + proc.stderr)
    finally:
        chapter.write_text(backup, encoding="utf-8")


def test_fig_ce3_009_not_live_reader_ref():
    for chapter in (ROOT / "book/chapters").glob("ch*/chapter.md"):
        text = chapter.read_text(encoding="utf-8")
        assert "FIG-CE3-009" not in text, f"{chapter} still cites blocked FIG-CE3-009"


def test_ch24_figure_assets_exist():
    for n in (1, 2, 3):
        path = ROOT / f"figures/full31/ch24/fig-ch24-00{n}.svg"
        assert path.exists(), path
        xml = path.read_text(encoding="utf-8")
        assert "<title" in xml and "<desc" in xml
        assert f'data-figure-id="FIG-CH24-00{n}"' in xml


def test_inventory_generator_runs():
    proc = subprocess.run(
        [PY, str(ROOT / "scripts/generate_full31_manuscript_inventory.py"), "--write"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (ROOT / "publication/full31/FULL31_MANUSCRIPT_INVENTORY.md").exists()
    check = subprocess.run(
        [PY, str(ROOT / "scripts/generate_full31_manuscript_inventory.py"), "--check"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert check.returncode == 0, check.stdout + check.stderr
