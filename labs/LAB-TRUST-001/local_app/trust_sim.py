#!/usr/bin/env python3
"""LAB-TRUST-001 Route L — local trust / inference simulator.

Safe educational toy only:
- No network calls
- No real model weights
- No secrets collection
- Deterministic offline answer for one fixed practical question

Statuses: IMPLEMENTED_DIGITAL | FIXTURE_VALIDATED fallback available.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

SAFE_QUESTION = (
    "How can I tell whether a public library website is slow because of my phone "
    "or because of the site, without logging into any personal accounts?"
)

LOCAL_ANSWER = """Try these checks on a public page you already open without signing in:
1) Reload once and note whether the address bar spinner stops before readable text appears.
2) Compare the same public URL on a second network you control (feel only — not a benchmark).
3) If both networks are slow, prefer investigating the site/upstream before blaming only the phone.

Hedge: this is a checklist, not a root-cause diagnosis.
"""


@dataclass
class InferenceTrace:
    route: str
    label: str
    data_stage: str
    model_stage: str
    inference_stage: str
    network_required: str
    data_leaving_device_claimed: str
    authn_required: str
    authz_note: str
    lifecycle: list[str]
    security_principle: str
    uncertainty_hedge: str
    answer: str


def run_local_inference(question: str) -> InferenceTrace:
    """Map data → model → inference with explicit trust metadata."""
    if question.strip() != SAFE_QUESTION:
        # Keep learners on the safe prompt; do not process arbitrary private text.
        raise SystemExit(
            "Use the lab's safe practical question exactly (see README). "
            "Refusing free-form input protects privacy in this teaching simulator."
        )
    return InferenceTrace(
        route="L",
        label="SIMULATED_LOCAL_INFERENCE",
        data_stage="prompt held in local process buffer",
        model_stage="toy-local-rules-v0 (deterministic table; not a person)",
        inference_stage="template answer generated offline",
        network_required="N",
        data_leaving_device_claimed="N (prompt body); OS telemetry unknown",
        authn_required="N",
        authz_note="Public-page observation only; no privileged actions",
        lifecycle=["collect(local buffer)", "use(inference)", "retain(session)", "share(none claimed)", "delete(on exit)"],
        security_principle="least privilege + psychological acceptability (no extra permissions requested)",
        uncertainty_hedge="checklist ≠ diagnosis",
        answer=LOCAL_ANSWER.strip(),
    )


def print_human(trace: InferenceTrace) -> None:
    print("LAB-TRUST-001 local simulator")
    print("Label:", trace.label)
    print("Network required:", trace.network_required)
    print("Data leaving device (claimed):", trace.data_leaving_device_claimed)
    print("Authn required:", trace.authn_required)
    print("Authz note:", trace.authz_note)
    print("Lifecycle:", " → ".join(trace.lifecycle))
    print("Security principle:", trace.security_principle)
    print("Uncertainty:", trace.uncertainty_hedge)
    print("--- data → model → inference ---")
    print("Data:", trace.data_stage)
    print("Model:", trace.model_stage)
    print("Inference:", trace.inference_stage)
    print("--- answer ---")
    print(trace.answer)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LAB-TRUST-001 local trust simulator")
    parser.add_argument(
        "--question",
        default=SAFE_QUESTION,
        help="Must match the lab safe practical question",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON trace")
    parser.add_argument(
        "--show-fixture-path",
        action="store_true",
        help="Print path to Route L fixture fallback",
    )
    args = parser.parse_args(argv)

    if args.show_fixture_path:
        fixture = Path(__file__).resolve().parents[1] / "fixtures" / "route_l_transcript.md"
        print(fixture)
        return 0

    trace = run_local_inference(args.question)
    if args.json:
        print(json.dumps(asdict(trace), indent=2))
    else:
        print_human(trace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
