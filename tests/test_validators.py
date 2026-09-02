from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([PY, str(ROOT / "scripts" / script)], capture_output=True, text=True)


def test_validate_book_pass():
    proc = run("validate_book.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_validate_claims_pass():
    proc = run("validate_claims.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_validate_glossary_pass():
    proc = run("validate_glossary.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_validate_labs_pass():
    proc = run("validate_labs.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_validate_figures_pass():
    proc = run("validate_figures.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_validate_accessibility_pass():
    proc = run("validate_accessibility.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_validate_links_pass():
    proc = run("validate_links.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_validate_waike_pass():
    proc = run("validate_waike.py")
    assert proc.returncode == 0, proc.stdout + proc.stderr
