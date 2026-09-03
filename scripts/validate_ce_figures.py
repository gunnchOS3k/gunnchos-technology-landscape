#!/usr/bin/env python3
"""Validate Concept Edition preproduction figures (Agent F visual system).

Checks:
  - duplicate figure IDs
  - missing IDs
  - malformed SVG
  - missing a11y metadata
  - missing plan mapping
  - measured without evidence (must be blocked)
  - physical without PHYSICAL_PENDING qualification
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

REG_PATH = ROOT / "figures/preproduction/ce_figure_registry.yaml"
PLAN_PATHS = [
    ROOT / "publication/preproduction/ce-01/FIGURE_PLAN.yaml",
    ROOT / "publication/preproduction/ce-03/FIGURE_PLAN.yaml",
    ROOT / "publication/preproduction/ce-04/FIGURE_PLAN.yaml",
    ROOT / "publication/preproduction/ce-05/FIGURE_PLAN.yaml",
    ROOT / "publication/preproduction/ce-06/FIGURE_PLAN.yaml",
]
TEMPLATE_DIR = ROOT / "figures/templates"
REQUIRED_TEMPLATES = [
    "tmpl-ecosystem-system-map.svg",
    "tmpl-sequence-path.svg",
    "tmpl-layered-comparison.svg",
    "tmpl-hierarchy-resource-ladder.svg",
    "tmpl-status-vs-usable-experience.svg",
    "tmpl-failure-domain-trust-boundary.svg",
    "tmpl-stability-contract-condition-map.svg",
]
A11Y_REQUIRED = (
    "figure_id",
    "title",
    "caption",
    "alt_text",
    "text_equivalent",
    "reading_order",
    "truth_classification",
)
PHYSICAL_HINT = re.compile(r"PHYSICAL_PENDING|Device Quartet|device-quartet|quartet form", re.I)


def load_plan_index() -> dict[str, dict]:
    index: dict[str, dict] = {}
    for path in PLAN_PATHS:
        if not path.exists():
            continue
        data = load_yaml(path) or {}
        chapter = data.get("chapter_id")
        for fig in data.get("figures") or []:
            fid = fig.get("provisional_id")
            if not fid:
                continue
            index[fid] = {**fig, "chapter_id": chapter, "plan_path": str(path.relative_to(ROOT))}
    return index


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for name in REQUIRED_TEMPLATES:
        tpath = TEMPLATE_DIR / name
        if not tpath.exists():
            errors.append(f"missing template: figures/templates/{name}")
        else:
            try:
                ET.parse(tpath)
            except ET.ParseError as exc:
                errors.append(f"malformed template SVG {name}: {exc}")

    if not REG_PATH.exists():
        errors.append(f"missing registry {REG_PATH.relative_to(ROOT)}")
        print("validate_ce_figures: FAIL")
        for e in errors:
            print(f" - {e}")
        return 1

    reg = load_yaml(REG_PATH) or {}
    figures = reg.get("figures") or []
    plan_index = load_plan_index()

    ids = [f.get("figure_id") for f in figures]
    if any(not i for i in ids):
        errors.append("missing IDs: one or more registry entries lack figure_id")
    if len(ids) != len(set(ids)):
        seen: set[str] = set()
        dups: set[str] = set()
        for i in ids:
            if i in seen:
                dups.add(str(i))
            seen.add(i)
        errors.append(f"duplicate IDs: {sorted(dups)}")

    planned_ids = set(plan_index)
    registry_ids = {i for i in ids if i}
    missing_from_reg = sorted(planned_ids - registry_ids)
    extra_in_reg = sorted(registry_ids - planned_ids)
    if missing_from_reg:
        errors.append(f"missing plan mapping in registry (planned but absent): {missing_from_reg}")
    if extra_in_reg:
        errors.append(f"registry IDs not in FIGURE_PLAN.yaml: {extra_in_reg}")

    for fig in figures:
        fid = fig.get("figure_id") or "<no-id>"
        plan = plan_index.get(fid)
        if not plan:
            errors.append(f"{fid}: missing plan mapping")
            continue

        truth = fig.get("truth_classification") or plan.get("truth_classification")
        status = fig.get("production_status")
        qual = fig.get("qualification") or plan.get("qualification")

        acc_rel = fig.get("accessibility")
        if not acc_rel:
            errors.append(f"{fid}: missing a11y metadata path")
        else:
            acc_path = ROOT / acc_rel
            if not acc_path.exists():
                errors.append(f"{fid}: missing a11y sidecar {acc_rel}")
            else:
                acc = load_yaml(acc_path) or {}
                for field in A11Y_REQUIRED:
                    if not acc.get(field):
                        errors.append(f"{fid}: a11y missing {field}")
                if acc.get("figure_id") and acc.get("figure_id") != fid:
                    errors.append(f"{fid}: a11y figure_id mismatch ({acc.get('figure_id')})")

        if truth == "measured":
            evidence_ok = False
            src = str(plan.get("data_or_evidence_source") or "").lower()
            if status == "implemented" and "fixture" in src and "to be captured" not in src:
                evidence_ok = True
            if status == "blocked" and fig.get("block_reason") == "BLOCKED_EVIDENCE_REQUIRED":
                evidence_ok = True
            if not evidence_ok:
                errors.append(
                    f"{fid}: measured without evidence — require BLOCKED_EVIDENCE_REQUIRED "
                    f"(status={status}, block_reason={fig.get('block_reason')})"
                )
            if status == "blocked" and fig.get("path"):
                errors.append(f"{fid}: blocked measured figure must not ship SVG path")

        blob = " ".join(
            str(x)
            for x in (
                plan.get("pedagogical_purpose"),
                plan.get("reader_should_notice"),
                plan.get("data_or_evidence_source"),
                plan.get("expected_geometry"),
                plan.get("accessibility_description_requirement"),
            )
            if x
        )
        needs_physical = bool(PHYSICAL_HINT.search(blob)) or fid in {"FIG-CE1-006", "FIG-CE3-008"}
        if needs_physical and status == "implemented" and qual != "PHYSICAL_PENDING":
            errors.append(
                f"{fid}: physical/Device Quartet content without PHYSICAL_PENDING qualification "
                f"(qualification={qual!r})"
            )

        if status == "implemented":
            rel = fig.get("path")
            if not rel:
                errors.append(f"{fid}: implemented but missing SVG path")
                continue
            svg_path = ROOT / rel
            if not svg_path.exists():
                errors.append(f"{fid}: missing SVG asset {rel}")
                continue
            try:
                tree = ET.parse(svg_path)
                root = tree.getroot()
            except ET.ParseError as exc:
                errors.append(f"{fid}: malformed SVG: {exc}")
                continue
            text_blob = ET.tostring(root, encoding="unicode")
            if fid not in text_blob:
                errors.append(f"{fid}: SVG missing stable figure ID text")
            data_truth = root.attrib.get("data-truth-classification")
            if not data_truth:
                for k, v in root.attrib.items():
                    if k.endswith("data-truth-classification"):
                        data_truth = v
            if "truth_classification" not in text_blob and not data_truth:
                errors.append(f"{fid}: SVG missing truth_classification marker")
            title_el = root.find("{http://www.w3.org/2000/svg}title")
            desc_el = root.find("{http://www.w3.org/2000/svg}desc")
            if title_el is None:
                title_el = root.find("title")
            if desc_el is None:
                desc_el = root.find("desc")
            if title_el is None or not (title_el.text or "").strip():
                errors.append(f"{fid}: SVG missing <title>")
            if desc_el is None or not (desc_el.text or "").strip():
                errors.append(f"{fid}: SVG missing <desc>")

        elif status == "blocked":
            man = fig.get("blocked_manifest")
            if not man or not (ROOT / man).exists():
                errors.append(f"{fid}: blocked figure missing blocked_manifest")

    if len(planned_ids) != 41:
        warnings.append(f"expected 41 planned figures, found {len(planned_ids)}")

    if errors:
        print("validate_ce_figures: FAIL")
        for e in errors:
            print(f" - {e}")
        for w in warnings:
            print(f" ! {w}")
        return 1

    counts = reg.get("counts") or {}
    print("validate_ce_figures: PASS")
    print(
        f" planned={counts.get('planned', len(figures))}"
        f" implemented={counts.get('implemented')}"
        f" blocked={counts.get('blocked')}"
        f" physical_pending={counts.get('physical_pending')}"
    )
    by = counts.get("by_truth_classification") or {}
    for truth, c in sorted(by.items()):
        print(
            f"  {truth}: planned={c.get('planned')} "
            f"implemented={c.get('implemented')} blocked={c.get('blocked')}"
        )
    for w in warnings:
        print(f" ! {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
