#!/usr/bin/env python3
"""LAB-TAP-001 Route B — local timestamped tap demo.

No specialized hardware required. Uses Tkinter when available.
"""
from __future__ import annotations

import time
import urllib.request
from dataclasses import dataclass, field

try:
    import tkinter as tk
except Exception as exc:  # pragma: no cover
    raise SystemExit(
        "Tkinter is required for the GUI route. "
        "On headless systems, use the browser route or fixtures/sample_result_table.csv."
    ) from exc


@dataclass
class Trail:
    rows: list[tuple[str, float]] = field(default_factory=list)

    def mark(self, label: str) -> float:
        t = time.perf_counter()
        self.rows.append((label, t))
        print(f"{label}\t{t:.6f}")
        return t


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LAB-TAP-001 Local Tap Timer")
        self.geometry("520x320")
        self.trail = Trail()
        self.status = tk.StringVar(value="Ready. Do not enter secrets.")
        tk.Label(self, textvariable=self.status, wraplength=480, justify="left").pack(pady=8)
        tk.Button(self, text="Local only", command=self.local_only).pack(pady=4)
        tk.Button(self, text="Fetch remote sample", command=self.remote).pack(pady=4)
        tk.Button(self, text="Print table", command=self.print_table).pack(pady=4)

    def local_only(self) -> None:
        self.trail.mark("input: click (local)")
        self.trail.mark("handler: start (local)")
        self.status.set("Local state updated.")
        self.update_idletasks()
        self.trail.mark("output: status updated (local)")
        self.trail.mark("handler: end (local)")

    def remote(self) -> None:
        self.trail.mark("input: click (remote)")
        self.trail.mark("handler: start (remote)")
        self.status.set("Requesting sample...")
        self.update_idletasks()
        self.trail.mark("network: request start")
        try:
            with urllib.request.urlopen("https://httpbin.org/delay/1", timeout=10) as resp:
                resp.read(64)
            self.trail.mark("network: response received")
            self.status.set("Remote sample received.")
        except Exception as exc:  # noqa: BLE001
            self.trail.mark("network: failure")
            self.status.set(f"Remote request failed: {type(exc).__name__}")
        self.update_idletasks()
        self.trail.mark("output: status updated (remote)")
        self.trail.mark("handler: end (remote)")

    def print_table(self) -> None:
        if not self.trail.rows:
            print("No marks yet.")
            return
        t0 = self.trail.rows[0][1]
        print("marker\tseconds_since_first_mark")
        for label, t in self.trail.rows:
            print(f"{label}\t{t - t0:.6f}")


if __name__ == "__main__":
    App().mainloop()
