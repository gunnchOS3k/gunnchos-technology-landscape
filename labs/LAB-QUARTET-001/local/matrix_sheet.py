#!/usr/bin/env python3
"""Print a blank LAB-QUARTET-001 CSV skeleton (no measurements invented)."""

from __future__ import annotations

HEADER = [
    "constraint_domain",
    "student_14_5_desk",
    "handheld_hybrid_mobile_docked",
    "ds_xl_coder_learn_to_build",
    "edge_io_wearables_embodied",
    "evidence_status",
]

DOMAINS = [
    "mobility_posture",
    "input_surface",
    "display_attention",
    "power_thermal_class_qualitative",
    "io_peripherals",
    "sensing_privacy",
    "build_inspect_workflow",
    "accessibility_route",
    "likely_failure_domain",
]


def main() -> None:
    print(",".join(HEADER))
    for domain in DOMAINS:
        cells = [domain] + [""] * 4 + ["conceptual_or_analogy"]
        print(",".join(cells))
    print(
        "# Reminder: leave Quartet numeric EVT fields empty; mark PHYSICAL_PENDING.",
        file=__import__("sys").stderr,
    )


if __name__ == "__main__":
    main()
