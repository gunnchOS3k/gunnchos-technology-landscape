#!/usr/bin/env python3
"""LAB-PKT-001 CLI — safe fixture quiz and optional DNS check.

No packet capture of other users. No credentials. Fixture-first.
"""
from __future__ import annotations

import argparse
import csv
import json
import socket
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_JSON = LAB_ROOT / "fixtures" / "sample_path_trace.json"
FIXTURE_CSV = LAB_ROOT / "fixtures" / "sample_timing_table.csv"


def load_fixture() -> dict:
    data = json.loads(FIXTURE_JSON.read_text(encoding="utf-8"))
    if data.get("label") != "ILLUSTRATIVE_FIXTURE":
        raise SystemExit("fixture missing ILLUSTRATIVE_FIXTURE label")
    return data


def show_fixture(data: dict) -> None:
    print("LAB-PKT-001 fixture path trace")
    print("honesty:", data.get("honesty"))
    eth = data["frame"]["ethernet"]
    ip = data["frame"]["ipv4"]
    print(f"ethernet.ethertype={eth['ethertype']} ({eth['ethertype_meaning']})")
    print(f"ipv4.ttl={ip['ttl']} src={ip['src']} dst={ip['dst']}")
    print("access_network.mode=", data["access_network"]["mode"])
    print(
        "placement=",
        data["placement_hypothesis"]["edge_or_cloud"],
        f"({data['placement_hypothesis']['confidence']})",
    )
    print("metric_family=", data["metric_family"])
    print("scopes:", ", ".join(data["scopes"].keys()))
    print(
        "distinctions: Wi-Fi ≠ Internet ≠ cellular ≠ cloud; "
        "latency ≠ throughput ≠ reliability"
    )


def run_quiz(data: dict) -> int:
    ok = 0
    for q in data.get("parse_questions") or []:
        print()
        print(f"Q[{q['id']}] ({q['kind']}): {q['ask']}")
        print(f"  expected_answer_for_fixture: {q['answer']!r}")
        ok += 1
    print()
    print(f"quiz_items_ready={ok}")
    return 0


def show_timing() -> None:
    print()
    print("Timing table (ILLUSTRATIVE_FIXTURE):")
    with FIXTURE_CSV.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row.get("label") != "ILLUSTRATIVE_FIXTURE":
                raise SystemExit("timing row missing ILLUSTRATIVE_FIXTURE")
            print(
                f"  run={row['run_id']} access={row['access_mode']} "
                f"phase={row['phase']} ms={row['ms']} family={row['metric_family']}"
            )


def dns_check(host: str) -> int:
    print(
        f"EXTERNAL_DEPENDENCY dns-check for {host!r} "
        "(no secrets; failure is valid evidence)"
    )
    try:
        infos = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    except OSError as exc:
        print(f"dns_or_resolution_failure: {exc}")
        print(
            "Treat as observation of a resolution/reachability problem "
            "— or switch to --fixture."
        )
        return 0
    addrs = sorted({item[4][0] for item in infos})
    print("resolved_addresses:", ", ".join(addrs[:8]))
    print(
        "Note: resolution success ≠ good latency/throughput/reliability "
        "to the service."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LAB-PKT-001 safe path inspector")
    parser.add_argument("--fixture", action="store_true", help="Load and print fixture path story")
    parser.add_argument("--quiz", action="store_true", help="Print fixture parse questions")
    parser.add_argument("--timing", action="store_true", help="Print fixture timing CSV")
    parser.add_argument(
        "--dns-check",
        metavar="HOST",
        help="Optional EXTERNAL_DEPENDENCY name lookup (e.g. example.com)",
    )
    args = parser.parse_args(argv)

    if not any([args.fixture, args.quiz, args.timing, args.dns_check]):
        args.fixture = True
        args.timing = True

    if args.fixture or args.quiz:
        data = load_fixture()
        if args.fixture:
            show_fixture(data)
        if args.quiz:
            run_quiz(data)
    if args.timing:
        show_timing()
    if args.dns_check:
        return dns_check(args.dns_check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
