#!/usr/bin/env python3
"""Full31 manuscript draft check (infra vs strict WORKING_DRAFT_COMPLETE).

Modes
-----
infra (default / Batch 0):
  Infrastructure ready; chapters may still be scaffolds.
  Scaffold / incomplete prose → WARN (exit 0 if infra OK).

strict / WORKING_DRAFT_COMPLETE (Batch 1+ target):
  All 31 chapters must be non-scaffold working drafts with anatomy,
  resolved refs, and no reader-facing placeholders.

Does not modify publication/gates/gate-3/.
Does not claim Gate 3 PASS or publication-ready.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

ANATOMY = [
    "The moment",
    "What you notice",
    "Exploded ecosystem",
    "Follow the signal",
    "Component cards",
    "Stability contract",
    "Try it",
    "Build it",
    "Secure and include it",
    "Career lens",
    "Check understanding",
    "Glossary links",
]

REQUIRED_FRONT = [
    "book/frontmatter/status.qmd",
    "book/frontmatter/how-to-use.qmd",
    "book/frontmatter/reader-pathways.qmd",
    "book/frontmatter/device-quartet.qmd",
    "book/frontmatter/waike.qmd",
    "book/frontmatter/evidence-legend.qmd",
]

REQUIRED_BACK = [
    "book/appendices/glossary.qmd",
    "book/appendices/references.qmd",
    "book/appendices/lab-index.qmd",
    "book/appendices/figure-index.qmd",
    "book/appendices/career-role-map.qmd",
    "book/appendices/acknowledgments.qmd",
]

BANNER_LINES = [
    "WORKING FULL-MANUSCRIPT DRAFT",
    "Human reader validation pending.",
    "Technical/editorial revision pending.",
    "Not publication-ready.",
]

SCAFFOLD_MARKERS = re.compile(
    r"intentionally scaffolded|Status:\s*`?outline`?|Manuscript status:\s*scaffold|"
    r"Do not treat this scaffold|no canonical chapter prose",
    re.I,
)

PLACEHOLDER_RE = re.compile(
    r"\bTODO\b|\bTBD\b|\[INSERT[^\]]*\]|\[PLACEHOLDER[^\]]*\]|FIXME|XXX\b",
    re.I,
)

AGENT_META_RE = re.compile(
    r"\b(as an AI|as a language model|I am an agent|agent handoff|"
    r"cursor agent|batch \d+ agent|do not treat this scaffold as)\b",
    re.I,
)

VSCODE_FILE_RE = re.compile(r"vscode-file://", re.I)
LOCAL_PATH_RE = re.compile(
    r"(?:/Users/[^\s)`\"']+| /home/[^\s)`\"']+|C:\\\\Users\\\\|[A-Z]:\\\\Users\\\\)",
)

SECRET_RE = re.compile(
    r"(?i)(api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]|secret[_-]?key\s*[:=]|"
    r"BEGIN (RSA |OPENSSH )?PRIVATE KEY|aws_secret_access_key|"
    r"xox[baprs]-[0-9A-Za-z-]{10,})",
)

SYNTHETIC_AS_HUMAN_RE = re.compile(
    r"(?i)(synthetic (reader|human) (evidence|validation|response)|"
    r"fake reader (study|feedback)|invented endorsements?|"
    r"GATE_3_PASS|Gate 3 PASS)",
)

FORBIDDEN_READY_RE = re.compile(
    r"(?i)\b(publication[- ]ready|GATE_3_PASS)\b",
)

CITATION_RE = re.compile(r"@([A-Za-z0-9_:-]+)")
FIG_RE = re.compile(r"FIG-CH\d{2}-\d{3}|@fig-ch\d{2}-\d{3}|fig-ch\d{2}-\d{3}", re.I)
LAB_RE = re.compile(r"LAB-[A-Z0-9-]+")


def _strip_code_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def _reader_prose(text: str) -> str:
    """Drop YAML front matter for placeholder scans."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4 :]
    return _strip_code_fences(text)


def _is_scaffold(text: str, meta_status: str | None) -> bool:
    if meta_status and meta_status.lower() in {"outline", "scaffold"}:
        return True
    if SCAFFOLD_MARKERS.search(text):
        return True
    # Very short non-CH02 bodies without anatomy are scaffolds
    prose = _reader_prose(text)
    if len(prose.strip()) < 400:
        return True
    return False


def _load_bib_keys() -> set[str]:
    bib = ROOT / "book/references/references.bib"
    if not bib.exists():
        return set()
    return set(re.findall(r"@\w+\{([^,]+),", bib.read_text(encoding="utf-8")))


def _load_glossary_terms() -> set[str]:
    path = ROOT / "glossary/glossary.yaml"
    if not path.exists():
        return set()
    doc = load_yaml(path) or {}
    terms: set[str] = set()
    entries = doc.get("terms") or doc.get("entries") or doc
    if isinstance(entries, list):
        for item in entries:
            if isinstance(item, dict):
                for key in ("id", "term", "slug"):
                    if item.get(key):
                        terms.add(str(item[key]).lower())
            elif isinstance(item, str):
                terms.add(item.lower())
    elif isinstance(entries, dict):
        terms.update(str(k).lower() for k in entries.keys())
    return terms


def _load_lab_ids() -> set[str]:
    labs_dir = ROOT / "labs"
    ids: set[str] = set()
    if labs_dir.is_dir():
        for p in labs_dir.iterdir():
            if p.is_dir() and p.name.startswith("LAB-"):
                ids.add(p.name)
    return ids


def _load_figure_ids() -> set[str]:
    ids: set[str] = set()
    fig_reg = ROOT / "figures"
    # Prefer registry if present
    for candidate in [
        ROOT / "figures/figure_registry.yaml",
        ROOT / "evidence/figure_registry.yaml",
    ]:
        if candidate.exists():
            doc = load_yaml(candidate) or {}
            for item in doc.get("figures") or []:
                if isinstance(item, dict) and item.get("id"):
                    ids.add(str(item["id"]).upper())
    if fig_reg.is_dir():
        for p in fig_reg.rglob("fig-*.svg"):
            stem = p.stem.upper().replace("FIG-", "FIG-")
            # fig-ch02-001-human-to-system → FIG-CH02-001
            m = re.match(r"FIG-CH(\d{2})-(\d{3})", stem.replace("FIG-", "FIG-"), re.I)
            if not m:
                m = re.match(r"fig-ch(\d{2})-(\d{3})", p.stem, re.I)
            if m:
                ids.add(f"FIG-CH{m.group(1)}-{m.group(2)}")
    return ids


def check_banner(errors: list[str], warnings: list[str]) -> None:
    sources = [
        ROOT / "book/metadata.yaml",
        ROOT / "book/frontmatter/status.qmd",
        ROOT / "index.qmd",
    ]
    blob = "\n".join(p.read_text(encoding="utf-8") if p.exists() else "" for p in sources)
    for line in BANNER_LINES:
        if line not in blob:
            errors.append(f"publication banner missing line: {line!r}")
    meta = load_yaml(ROOT / "book/metadata.yaml") if (ROOT / "book/metadata.yaml").exists() else {}
    status = str(meta.get("status") or "")
    if "WORKING FULL-MANUSCRIPT DRAFT" not in status and "WORKING FULL-MANUSCRIPT DRAFT" not in blob:
        errors.append("book/metadata.yaml must declare WORKING FULL-MANUSCRIPT DRAFT")
    if str(meta.get("human_validation") or "") != "DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT":
        warnings.append("metadata human_validation should be DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT")


def check_quarto_chapters(errors: list[str]) -> list[str]:
    yml = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
    listed: list[str] = []
    for n in range(1, 32):
        needle = f"book/chapters/ch{n:02d}/chapter.md"
        if needle not in yml:
            errors.append(f"_quarto.yml missing {needle}")
        else:
            listed.append(needle)
    for path in REQUIRED_FRONT + REQUIRED_BACK:
        if path not in yml:
            errors.append(f"_quarto.yml missing {path}")
        if not (ROOT / path).exists():
            errors.append(f"missing front/back matter stub: {path}")
    return listed


def check_chapter(
    cid: str,
    title: str,
    mode: str,
    bib_keys: set[str],
    lab_ids: set[str],
    fig_ids: set[str],
    errors: list[str],
    warnings: list[str],
    status: dict[str, str],
) -> None:
    body_path = ROOT / f"book/chapters/{cid.lower()}/chapter.md"
    meta_path = ROOT / f"book/chapters/{cid.lower()}/metadata.yaml"
    if not body_path.exists():
        errors.append(f"{cid}: missing chapter.md")
        status[cid] = "MISSING"
        return
    if not meta_path.exists():
        errors.append(f"{cid}: missing metadata.yaml")
    text = body_path.read_text(encoding="utf-8")
    meta = load_yaml(meta_path) if meta_path.exists() else {}
    meta_title = str(meta.get("title") or "")
    if meta_title and meta_title != title:
        errors.append(f"{cid}: metadata title {meta_title!r} != registry {title!r}")
    # Title should appear in chapter heading somewhere
    if title not in text and title.replace(":", "") not in text:
        warnings.append(f"{cid}: registry title not found in chapter.md heading text")

    scaffold = _is_scaffold(text, str(meta.get("status") or ""))
    status[cid] = "SCAFFOLD" if scaffold else "WORKING_DRAFT_CANDIDATE"

    prose = _reader_prose(text)

    # Forbidden claims in any mode
    if re.search(r"\bGATE_3_PASS\b", prose):
        errors.append(f"{cid}: forbids GATE_3_PASS in reader prose")
    if re.search(r"(?i)this (chapter|book|manuscript) is publication[- ]ready", prose):
        errors.append(f"{cid}: forbids publication-ready claim in reader prose")
    if SECRET_RE.search(prose):
        errors.append(f"{cid}: possible secret/credential pattern in prose")
    if SYNTHETIC_AS_HUMAN_RE.search(prose) and "never" not in prose.lower():
        # Allow explicit prohibitions in stubs; fail clear false claims
        if re.search(r"(?i)GATE_3_PASS|completed human validation|readers confirmed", prose):
            errors.append(f"{cid}: synthetic/false human-evidence claim")

    if scaffold:
        if mode == "strict":
            errors.append(f"{cid}: still scaffold — strict mode requires WORKING_DRAFT_COMPLETE")
        else:
            warnings.append(f"{cid}: scaffold (allowed in infra mode)")
        return

    # Non-scaffold checks
    missing_anatomy = [s for s in ANATOMY if s.lower() not in prose.lower()]
    if missing_anatomy:
        msg = f"{cid}: missing anatomy anchors: {', '.join(missing_anatomy)}"
        if mode == "strict":
            errors.append(msg)
        else:
            warnings.append(msg)

    if PLACEHOLDER_RE.search(prose):
        msg = f"{cid}: reader-facing placeholder (TODO/TBD/[INSERT]/ in prose"
        (errors if mode == "strict" else warnings).append(msg)

    if AGENT_META_RE.search(prose) and cid != "CH01":
        # scaffold chapters often contain agent-facing instructions; already returned
        msg = f"{cid}: agent meta-text in reader prose"
        (errors if mode == "strict" else warnings).append(msg)

    if VSCODE_FILE_RE.search(prose):
        errors.append(f"{cid}: vscode-file:// URI in reader text")

    if LOCAL_PATH_RE.search(prose):
        msg = f"{cid}: local filesystem path in reader text"
        (errors if mode == "strict" else warnings).append(msg)

    # Citation resolve
    for key in CITATION_RE.findall(prose):
        if key.startswith("fig-"):
            continue
        if bib_keys and key not in bib_keys:
            msg = f"{cid}: citation @{key} not in references.bib"
            (errors if mode == "strict" else warnings).append(msg)

    # Lab refs
    for lab in LAB_RE.findall(prose):
        if lab_ids and lab not in lab_ids:
            msg = f"{cid}: lab {lab} not found under labs/"
            (errors if mode == "strict" else warnings).append(msg)

    # Figure refs (best-effort)
    for m in FIG_RE.findall(prose):
        fid = m.upper()
        if fid.startswith("@FIG-"):
            fid = fid[1:]
        if fid.startswith("FIG-CH") and fig_ids and fid not in fig_ids:
            # Allow planned figures not yet on disk in infra; strict warns/fails lightly
            msg = f"{cid}: figure {fid} not found in figures tree/registry"
            warnings.append(msg)

    if not missing_anatomy and not scaffold:
        status[cid] = "STRUCTURE_COMPLETE"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("infra", "strict", "WORKING_DRAFT_COMPLETE"),
        default=None,
        help="infra (default) or strict / WORKING_DRAFT_COMPLETE",
    )
    args = parser.parse_args()
    mode_raw = args.mode or os.environ.get("FULL31_DRAFT_CHECK_MODE") or "infra"
    mode = "strict" if mode_raw in {"strict", "WORKING_DRAFT_COMPLETE"} else "infra"

    errors: list[str] = []
    warnings: list[str] = []
    status: dict[str, str] = {}

    # Decision + docs exist
    decision = ROOT / "publication/full31/VALIDATION_SEQUENCE_DECISION.md"
    if not decision.exists():
        errors.append("missing publication/full31/VALIDATION_SEQUENCE_DECISION.md")
    else:
        dtext = decision.read_text(encoding="utf-8")
        required_needles = [
            "DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT",
            "GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING",
            "CH02-REVIEW-R1",
            "FULL31-REVIEW-R1",
        ]
        for needle in required_needles:
            if needle not in dtext:
                errors.append(f"VALIDATION_SEQUENCE_DECISION.md missing: {needle}")
        if "Gate 3 PASS" not in dtext and "GATE_3_PASS" not in dtext:
            errors.append("VALIDATION_SEQUENCE_DECISION.md must explicitly deny Gate 3 PASS")
        if "Do not create" not in dtext and "do NOT create" not in dtext and "Do not create that snapshot" not in dtext:
            # require deferral of FULL31-REVIEW-R1 snapshot creation
            if "Do **not** create" not in dtext and "**Do not create**" not in dtext:
                errors.append("VALIDATION_SEQUENCE_DECISION.md must defer FULL31-REVIEW-R1 snapshot creation")

    check_banner(errors, warnings)
    check_quarto_chapters(errors)

    # Render script + make target presence (infra)
    if not (ROOT / "scripts/render_full31.sh").exists():
        errors.append("missing scripts/render_full31.sh")
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    for target in (
        "full31-draft-check",
        "full31-html",
        "full31-pdf",
        "full31-epub",
        "technology-landscape-full31",
    ):
        if target == "technology-landscape-full31":
            # artifact names appear in render script
            render = (ROOT / "scripts/render_full31.sh").read_text(encoding="utf-8") if (ROOT / "scripts/render_full31.sh").exists() else ""
            if "technology-landscape-full31-html" not in render:
                errors.append("render_full31.sh must name technology-landscape-full31-html artifact")
            continue
        if target not in makefile:
            errors.append(f"Makefile missing target/reference: {target}")

    reg = load_yaml(ROOT / "book/chapter_registry.yaml")
    chapters = reg.get("chapters") or []
    if len(chapters) != 31:
        errors.append(f"chapter_registry.yaml expected 31 chapters, found {len(chapters)}")

    bib_keys = _load_bib_keys()
    lab_ids = _load_lab_ids()
    fig_ids = _load_figure_ids()

    for ch in chapters:
        cid = str(ch.get("chapter_id") or "")
        title = str(ch.get("title") or "")
        check_chapter(cid, title, mode, bib_keys, lab_ids, fig_ids, errors, warnings, status)

    # Distinctions summary
    exists_n = sum(1 for c in chapters if (ROOT / f"book/chapters/{str(c['chapter_id']).lower()}/chapter.md").exists())
    scaffold_n = sum(1 for v in status.values() if v == "SCAFFOLD")
    structure_n = sum(1 for v in status.values() if v == "STRUCTURE_COMPLETE")
    candidate_n = sum(1 for v in status.values() if v == "WORKING_DRAFT_CANDIDATE")

    print(f"full31-draft-check: mode={mode}")
    print(f" - file_exists: {exists_n}/31")
    print(f" - scaffold: {scaffold_n}/31")
    print(f" - working_draft_candidate: {candidate_n}/31")
    print(f" - structure_complete: {structure_n}/31")
    print(" - gate_posture: GATE_3_IN_PROGRESS — READER_EVIDENCE_PENDING")
    print(" - human_validation: DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT")
    print(" - CH02-REVIEW-R1 / gate-3: not modified by this check")

    if warnings:
        print(f" - warnings ({len(warnings)}):")
        for w in warnings[:80]:
            print(f"   · {w}")
        if len(warnings) > 80:
            print(f"   · … {len(warnings) - 80} more")

    if errors:
        print("full31-draft-check: FAIL")
        for e in errors:
            print(f" - {e}")
        return 1

    if mode == "strict" and structure_n != 31:
        print("full31-draft-check: FAIL")
        print(f" - strict mode requires 31/31 structure_complete, got {structure_n}")
        return 1

    print("full31-draft-check: PASS")
    if mode == "infra":
        print(" - infra ready; chapters may still be scaffold (Batch 1+ use --mode strict)")
    else:
        print(" - WORKING_DRAFT_COMPLETE criteria satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
