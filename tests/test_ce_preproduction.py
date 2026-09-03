from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def test_validate_ce_preproduction_pass():
    proc = subprocess.run(
        [PY, str(ROOT / "scripts" / "validate_ce_preproduction.py")],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
