#!/usr/bin/env python3
"""LAB-CMS-001 Route B — safe, non-destructive resource snapshot.

Read-only sampling of coarse CPU / memory / disk indicators where the host
exposes them. Never invents hardware sensors, temperatures, or vendor claims.
Falls back to 'unavailable' per field when a metric cannot be read.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


UNAVAILABLE = "unavailable"


@dataclass
class Snapshot:
    timestamp_utc: str
    platform: str
    label: str
    cpu_percent: Any
    memory_total_mb: Any
    memory_available_mb: Any
    memory_used_mb: Any
    disk_total_gb: Any
    disk_used_gb: Any
    disk_free_gb: Any
    notes: list[str]


def _utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _read_loadavg_cpu_hint() -> Any:
    """Best-effort, non-destructive CPU hint (not a hardware counter)."""
    try:
        if hasattr(os, "getloadavg"):
            load1, _, _ = os.getloadavg()
            cpus = os.cpu_count() or 1
            # Normalize 1-minute load by CPU count into a rough percent-like scale.
            return round(min(100.0, (load1 / cpus) * 100.0), 1)
    except (OSError, AttributeError):
        pass
    return UNAVAILABLE


def _read_memory_mb() -> tuple[Any, Any, Any, list[str]]:
    notes: list[str] = []
    # Linux: /proc/meminfo
    meminfo = Path("/proc/meminfo")
    if meminfo.is_file():
        data: dict[str, int] = {}
        for line in meminfo.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = line.split(":")
            if len(parts) != 2:
                continue
            key = parts[0].strip()
            val = parts[1].strip().split()[0]
            try:
                data[key] = int(val)  # kB
            except ValueError:
                continue
        total = data.get("MemTotal")
        avail = data.get("MemAvailable")
        if total is not None and avail is not None:
            used = total - avail
            return (
                round(total / 1024, 1),
                round(avail / 1024, 1),
                round(used / 1024, 1),
                notes,
            )
        notes.append("meminfo present but MemTotal/MemAvailable incomplete")

    # macOS / BSD: try sysctl (read-only)
    if platform.system() == "Darwin" and shutil.which("sysctl"):
        try:
            out = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )
            if out.returncode == 0 and out.stdout.strip().isdigit():
                total_mb = int(out.stdout.strip()) / (1024 * 1024)
                notes.append(
                    "Darwin: total RAM via sysctl; available/used marked unavailable "
                    "without privileged sampling"
                )
                return (round(total_mb, 1), UNAVAILABLE, UNAVAILABLE, notes)
        except (OSError, subprocess.SubprocessError):
            notes.append("sysctl memory probe failed")

    return UNAVAILABLE, UNAVAILABLE, UNAVAILABLE, notes


def _read_disk_gb(path: str = ".") -> tuple[Any, Any, Any]:
    try:
        usage = shutil.disk_usage(path)
        to_gb = lambda b: round(b / (1024**3), 2)
        return to_gb(usage.total), to_gb(usage.used), to_gb(usage.free)
    except OSError:
        return UNAVAILABLE, UNAVAILABLE, UNAVAILABLE


def take_snapshot(label: str) -> Snapshot:
    mem_total, mem_avail, mem_used, mem_notes = _read_memory_mb()
    disk_total, disk_used, disk_free = _read_disk_gb()
    notes = [
        "Non-destructive read-only snapshot for LAB-CMS-001.",
        "cpu_percent is a coarse loadavg-derived hint when available — not a root-cause proof.",
        "No thermal sensors, fan curves, or vendor hardware counters are claimed.",
        *mem_notes,
    ]
    return Snapshot(
        timestamp_utc=_utc_now(),
        platform=f"{platform.system()} {platform.release()}",
        label=label,
        cpu_percent=_read_loadavg_cpu_hint(),
        memory_total_mb=mem_total,
        memory_available_mb=mem_avail,
        memory_used_mb=mem_used,
        disk_total_gb=disk_total,
        disk_used_gb=disk_used,
        disk_free_gb=disk_free,
        notes=notes,
    )


def print_human(snap: Snapshot) -> None:
    print(f"label\t{snap.label}")
    print(f"timestamp_utc\t{snap.timestamp_utc}")
    print(f"platform\t{snap.platform}")
    print(f"cpu_percent_hint\t{snap.cpu_percent}")
    print(f"memory_total_mb\t{snap.memory_total_mb}")
    print(f"memory_available_mb\t{snap.memory_available_mb}")
    print(f"memory_used_mb\t{snap.memory_used_mb}")
    print(f"disk_total_gb\t{snap.disk_total_gb}")
    print(f"disk_used_gb\t{snap.disk_used_gb}")
    print(f"disk_free_gb\t{snap.disk_free_gb}")
    for note in snap.notes:
        print(f"note\t{note}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="LAB-CMS-001 safe resource snapshot (read-only)."
    )
    parser.add_argument(
        "--label",
        default="before",
        help="Snapshot label, e.g. before | during | after",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of TSV-style text",
    )
    parser.add_argument(
        "--fixture-demo",
        action="store_true",
        help="Print the bundled fixture table path and exit (no live sampling claims)",
    )
    args = parser.parse_args(argv)

    if args.fixture_demo:
        root = Path(__file__).resolve().parents[1]
        fixture = root / "fixtures" / "sample_observation_table.csv"
        print(f"fixture_fallback\t{fixture}")
        print("status\tFIXTURE_VALIDATED teaching data; not a live device measurement")
        return 0

    snap = take_snapshot(args.label)
    if args.json:
        print(json.dumps(asdict(snap), indent=2, sort_keys=True))
    else:
        print_human(snap)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
