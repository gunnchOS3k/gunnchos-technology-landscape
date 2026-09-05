#!/usr/bin/env python3
"""Validate Kids full manuscript family (Prompt 26 working drafts).

Claim ceiling allowed: KIDS_FULL_MANUSCRIPT_FAMILY_WORKING_DRAFT_COMPLETE
Still required: NOT CHILD-VALIDATED · NOT PUBLICATION-READY · KIDS_CHILD_VALIDATION_PENDING
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "kids" / "books"
SCOPE = ROOT / "kids" / "curriculum" / "KIDS_SCOPE_AND_SEQUENCE.yaml"
ATLAS = ROOT / "kids" / "standards" / "GLOBAL_STANDARDS_ATLAS.yaml"
SPIRAL = ROOT / "kids" / "concepts" / "ADULT31_TO_KIDS_SPIRAL.yaml"
MEDIA = ROOT / "kids" / "research" / "CHILD_MEDIA_EVIDENCE_REGISTER.yaml"
WAIKE = ROOT / "kids" / "waike" / "KIDS_WAIKE_CROSSWALK.yaml"

BANDS = [
    "KIDS-BABY",
    "KIDS-TODDLER",
    "KIDS-PRESCHOOL",
    "KIDS-PREK",
    "KIDS-ELEM1",
    "KIDS-ELEM2",
]
STRANDS = [
    "STRAND-ME-TECH",
    "STRAND-INSIDE",
    "STRAND-INSTRUCTIONS",
    "STRAND-MESSAGES",
    "STRAND-DATA",
    "STRAND-SAFE",
    "STRAND-BUILD",
]
REQUIRED_FILES = [
    "BOOK_MANUSCRIPT.md",
    "BOOK_METADATA.yaml",
    "UNIT_REGISTRY.yaml",
    "GLOSSARY.yaml",
    "STANDARDS_TRACEABILITY.yaml",
    "MEDIA_EVIDENCE_TRACEABILITY.yaml",
    "ACCESSIBILITY_NOTES.md",
    "CAREGIVER_EDUCATOR_NOTES.md",
    "FIGURE_PLAN.yaml",
    "ARTIFACT_MANIFEST.yaml",
    "README.md",
]
SHARED_REQUIRED = [
    "KIDS_MANUSCRIPT_INVENTORY.yaml",
    "KIDS_MANUSCRIPT_INVENTORY.md",
    "KIDS_BOOK_FORMAT_MATRIX.yaml",
    "KIDS_SPIRAL_CONTINUITY_REPORT.md",
    "KIDS_MISCONCEPTION_MATRIX.md",
    "KIDS_FULL_MANUSCRIPT_QUALITY_ISSUES.yaml",
]

CHILD_FACING_BLOCK_RE = re.compile(
    r"\*\*Child-facing text:\*\*\s*(.+?)(?=\n\n|\n\*\*|$)",
    re.S,
)
# Match real placeholders only — allow explicit "no IMAGE HERE" / "without IMAGE HERE" notes.
PLACEHOLDER_RE = re.compile(
    r"(?<!\bno\s)(?<!\bwithout\s)(?<!\breject\s)IMAGE HERE|TODO_IMAGE|lorem ipsum|\[placeholder\]",
    re.I,
)
CHILD_FACING_PROJECT_META_RE = re.compile(
    r"(?:"
    r"not\s+child[- ]validated"
    r"|publication[- ]ready"
    r"|developmental\s+prototype"
    r"|kids\s+developmental\s+prototype"
    r"|kids\s+full\s+working\s+manuscript"
    r"|working\s+draft\s+complete"
    r"|review\s+candidate"
    r"|owner[- ]locked"
    r"|source\s+SHA"
    r"|commit\s+SHA"
    r"|adult\s+chapter\s+prose"
    r"|do\s+not\s+copy\s+adult"
    r"|\bCursor\b"
    r"|\bintegrator\b"
    r"|\bagent\b"
    r"|frequency-to-intelligence"
    r"|magic\s+megahertz"
    r"|brain[- ]activating"
    r"|STANDARDS_CERTIFICATION"
    r"|NO_CHILD_VALIDATION_EVIDENCE"
    r"|KIDS_CHILD_VALIDATION_PENDING"
    r"|MAP-[A-Z0-9-]+"
    r"|STD-WIRE-[A-Z0-9-]+"
    r"|CME-\d+"
    r")",
    re.I,
)
FORBIDDEN_CLAIM_RE = re.compile(
    r"(?:"
    r"CHILD[- ]VALIDATED(?!\s+PENDING)"
    r"|PUBLICATION[- ]READY(?!\s*=\s*false)"
    r"|officially\s+aligned"
    r"|standards[- ]certified"
    r"|STANDARDS_CERTIFICATION_EVIDENCE(?!\s*=\s*false)"
    r")",
    re.I,
)
# Allow explicit non-claims / forbidden lists.
ALLOW_NEAR_FORBIDDEN = re.compile(
    r"(?i)(not[:\s*]|never\b|no_|forbidden|non-claim|reject|do not|≠|"
    r"must remain|AUTHORITY_CLAIMS|Forbidden claim|NOT CHILD|NOT PUBLICATION|"
    r"NO_STANDARDS_CERTIFICATION|NO_CHILD_VALIDATION)"
)
UNSUPPORTED_NEURO_RE = re.compile(
    r"(?i)brain[- ]activating|magic\s+frequenc|attention\s*=\s*learning|"
    r"high[- ]pitch.{0,40}intelligence|autoplay.{0,40}infinite"
)

MIN_CHILD_WORDS = {
    "KIDS-BABY": 40,
    "KIDS-TODDLER": 80,
    "KIDS-PRESCHOOL": 350,
    "KIDS-PREK": 450,
    "KIDS-ELEM1": 1800,
    "KIDS-ELEM2": 2800,
}
MIN_SPREADS_PER_UNIT = {
    "KIDS-BABY": 4,
    "KIDS-TODDLER": 4,
    "KIDS-PRESCHOOL": 5,
    "KIDS-PREK": 5,
    "KIDS-ELEM1": 6,
    "KIDS-ELEM2": 6,
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def extract_child_facing(text: str) -> list[str]:
    return [m.group(1).strip() for m in CHILD_FACING_BLOCK_RE.finditer(text)]


def child_word_count(text: str) -> int:
    return sum(len(b.split()) for b in extract_child_facing(text))


def concept_ids() -> set[str]:
    data = load_yaml(SPIRAL)
    ids = set()
    for c in data.get("concepts") or []:
        if isinstance(c, dict) and c.get("concept_id"):
            ids.add(c["concept_id"])
    return ids


def atlas_mapping_ids() -> set[str]:
    text = ATLAS.read_text(encoding="utf-8")
    return set(re.findall(r"mapping_id:\s*(MAP-[A-Z0-9-]+)", text))


def media_evidence_ids() -> set[str]:
    text = MEDIA.read_text(encoding="utf-8")
    return set(re.findall(r"\bCME-\d+\b", text))


def scope_units_by_band() -> dict[str, list[dict]]:
    data = load_yaml(SCOPE)
    out: dict[str, list[dict]] = {b: [] for b in BANDS}
    for u in data.get("units") or []:
        band = u.get("age_band")
        if band in out:
            out[band].append(u)
    return out


def as_unit_list(reg) -> list[dict]:
    if isinstance(reg, dict):
        if isinstance(reg.get("units"), list):
            return [u for u in reg["units"] if isinstance(u, dict)]
        # mapping of unit_id -> fields
        units = []
        for k, v in reg.items():
            if k in ("meta", "document_id", "version", "book_id", "age_band"):
                continue
            if isinstance(v, dict) and (v.get("unit_id") or k.startswith("UNIT-")):
                item = dict(v)
                item.setdefault("unit_id", v.get("unit_id") or k)
                units.append(item)
        return units
    if isinstance(reg, list):
        return [u for u in reg if isinstance(u, dict)]
    return []


def check_forbidden_claims(path: Path, text: str, errors: list[str]) -> None:
    for m in FORBIDDEN_CLAIM_RE.finditer(text):
        window = text[max(0, m.start() - 100) : m.end() + 80]
        if ALLOW_NEAR_FORBIDDEN.search(window):
            continue
        # Allow "NOT CHILD-VALIDATED" / "NOT PUBLICATION-READY" style banners
        if re.search(r"(?i)not\s+" + re.escape(m.group(0).split()[0]), window):
            continue
        errors.append(f"{path}: unsupported claim near {m.group(0)!r}")


def validate_band(band: str, scope_units: list[dict], concepts: set[str], atlas: set[str], media: set[str]) -> list[str]:
    errors: list[str] = []
    root = BOOKS / band
    if not root.is_dir():
        return [f"missing book directory {root}"]

    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"{band}: missing {name}")

    ms = root / "BOOK_MANUSCRIPT.md"
    if not ms.is_file():
        return errors
    text = ms.read_text(encoding="utf-8")
    if PLACEHOLDER_RE.search(text):
        errors.append(f"{band}: placeholder / IMAGE HERE in manuscript")
    if UNSUPPORTED_NEURO_RE.search(text):
        errors.append(f"{band}: unsupported neuroscience / compulsion language")
    for hit in CHILD_FACING_PROJECT_META_RE.finditer("\n".join(extract_child_facing(text))):
        errors.append(f"{band}: child-facing project meta {hit.group(0)!r}")

    words = child_word_count(text)
    if words < MIN_CHILD_WORDS[band]:
        errors.append(f"{band}: child-facing words {words} < min {MIN_CHILD_WORDS[band]} (anti-shell)")

    # Banner honesty in manuscript (adult-facing region OK)
    for needle in ("NOT CHILD-VALIDATED", "NOT PUBLICATION-READY"):
        if needle not in text:
            errors.append(f"{band}: manuscript missing honesty banner {needle}")

    reg_path = root / "UNIT_REGISTRY.yaml"
    if not reg_path.is_file():
        return errors
    reg = load_yaml(reg_path)
    units = as_unit_list(reg)
    if len(units) != 7:
        errors.append(f"{band}: expected 7 units in UNIT_REGISTRY, found {len(units)}")

    scope_ids = {u["unit_id"] for u in scope_units}
    reg_ids = {u.get("unit_id") for u in units}
    missing = scope_ids - reg_ids
    extra = reg_ids - scope_ids
    if missing:
        errors.append(f"{band}: registry missing scope units {sorted(missing)}")
    if extra:
        errors.append(f"{band}: registry has unknown units {sorted(x for x in extra if x)}")

    strand_seen = set()
    for u in units:
        uid = u.get("unit_id")
        strand = u.get("strand") or u.get("kids_strand")
        status = u.get("status")
        strand_seen.add(strand)
        if status != "WORKING_DRAFT_COMPLETE":
            errors.append(f"{band}/{uid}: status must be WORKING_DRAFT_COMPLETE, got {status!r}")
        if status and "PUBLICATION" in str(status).upper() and "READY" in str(status).upper():
            errors.append(f"{band}/{uid}: publication-ready status forbidden")
        spreads = int(u.get("spread_or_section_count") or 0)
        if spreads < MIN_SPREADS_PER_UNIT[band]:
            errors.append(f"{band}/{uid}: spreads {spreads} < min {MIN_SPREADS_PER_UNIT[band]}")
        for cid in u.get("concept_ids") or u.get("technology_concepts") or []:
            if cid not in concepts:
                errors.append(f"{band}/{uid}: unknown concept_id {cid}")
        for mid in u.get("standards_mapping_ids") or []:
            # Unit-level MAP-UNIT-* are curriculum maps; atlas maps may also appear
            if mid.startswith("MAP-UNIT-"):
                continue
            if mid.startswith("MAP-") and mid not in atlas:
                errors.append(f"{band}/{uid}: unknown atlas mapping {mid}")
        for eid in u.get("media_evidence_ids") or []:
            if eid not in media:
                errors.append(f"{band}/{uid}: unknown media evidence {eid}")
        # Anti-shell: require figures + activities listed
        if not (u.get("figures") or u.get("figure_ids")):
            errors.append(f"{band}/{uid}: missing figures list")
        if not (u.get("activities") or u.get("activity_ids")):
            errors.append(f"{band}/{uid}: missing activities list")

    for s in STRANDS:
        if s not in strand_seen:
            errors.append(f"{band}: missing strand {s}")

    # Builds
    builds = root / "builds"
    html = builds / "review-preview.html"
    pdfs = list(builds.glob("*.pdf")) if builds.is_dir() else []
    if not html.is_file():
        errors.append(f"{band}: missing builds/review-preview.html")
    else:
        h = html.read_text(encoding="utf-8", errors="ignore")
        for needle in (
            "KIDS FULL WORKING MANUSCRIPT",
            "NOT CHILD-VALIDATED",
            "NOT PUBLICATION-READY",
        ):
            if needle not in h:
                errors.append(f"{band}: HTML missing banner line {needle}")
    if not pdfs:
        errors.append(f"{band}: missing PDF review prototype under builds/")

    # Quality issues open blockers/majors checked at family level
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml", ".html", ".svg"}:
            t = p.read_text(encoding="utf-8", errors="ignore")
            check_forbidden_claims(p, t, errors)
            if PLACEHOLDER_RE.search(t) and p.name != "BOOK_MANUSCRIPT.md":
                # already flagged manuscript; still flag others
                if "IMAGE HERE" in t.upper():
                    errors.append(f"{p.relative_to(ROOT)}: IMAGE HERE placeholder")

    return errors


def validate_family(mode: str) -> int:
    errors: list[str] = []
    if not BOOKS.is_dir():
        print("FAIL: kids/books missing")
        return 1

    concepts = concept_ids()
    atlas = atlas_mapping_ids()
    media = media_evidence_ids()
    scope = scope_units_by_band()

    if mode in ("all", "check", "inventory", "continuity", "accessibility", "safety", "meta"):
        for name in SHARED_REQUIRED:
            if not (BOOKS / name).is_file():
                errors.append(f"missing shared {name}")

    if mode in ("all", "check", "inventory"):
        total_units = 0
        for band in BANDS:
            errs = validate_band(band, scope[band], concepts, atlas, media)
            errors.extend(errs)
            reg = BOOKS / band / "UNIT_REGISTRY.yaml"
            if reg.is_file():
                total_units += len(as_unit_list(load_yaml(reg)))
        if mode in ("all", "check") and total_units not in (0, 42):
            # if directories exist but incomplete
            if all((BOOKS / b).is_dir() for b in BANDS) and total_units != 42:
                errors.append(f"family unit count {total_units} != 42")

    if mode in ("all", "check", "continuity"):
        cont = BOOKS / "KIDS_SPIRAL_CONTINUITY_REPORT.md"
        misc = BOOKS / "KIDS_MISCONCEPTION_MATRIX.md"
        if cont.is_file():
            t = cont.read_text(encoding="utf-8")
            for needle in (
                "deepen",
                "vocabulary",
                "contradiction",
                "Baby",
                "safety",
            ):
                if needle.lower() not in t.lower():
                    errors.append(f"continuity report missing theme '{needle}'")
        if misc.is_file():
            t = misc.read_text(encoding="utf-8")
            for needle in (
                "every tap uses the internet",
                "CPU",
                "Wi-Fi",
                "AI",
                "cloud",
                "deletion",
            ):
                if needle.lower() not in t.lower():
                    errors.append(f"misconception matrix missing '{needle}'")

    if mode in ("all", "check", "accessibility"):
        for band in BANDS:
            p = BOOKS / band / "ACCESSIBILITY_NOTES.md"
            if not p.is_file():
                continue
            t = p.read_text(encoding="utf-8").lower()
            for needle in (
                "low vision",
                "color",
                "hearing",
                "dyslexia",
                "motor",
                "neurodiversity",
                "aac",
                "sensory",
                "multilingual",
            ):
                if needle not in t:
                    errors.append(f"{band}: accessibility notes missing '{needle}'")

    if mode in ("all", "check", "safety"):
        for band in BANDS:
            paths = [
                BOOKS / band / "BOOK_MANUSCRIPT.md",
                BOOKS / band / "CAREGIVER_EDUCATOR_NOTES.md",
            ]
            blob = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in paths if p.is_file())
            # Soft check: require explicit adult mediation / no accounts language somewhere
            if blob and "no accounts" not in blob.lower() and "no child account" not in blob.lower():
                errors.append(f"{band}: safety language should mention no child accounts")

    if mode in ("all", "check", "meta"):
        # Child-facing blocks across all manuscripts
        for band in BANDS:
            ms = BOOKS / band / "BOOK_MANUSCRIPT.md"
            if not ms.is_file():
                continue
            text = ms.read_text(encoding="utf-8")
            for i, block in enumerate(extract_child_facing(text), 1):
                for m in CHILD_FACING_PROJECT_META_RE.finditer(block):
                    errors.append(f"{band} child block #{i}: meta {m.group(0)!r}")

    if mode in ("all", "check"):
        qi = BOOKS / "KIDS_FULL_MANUSCRIPT_QUALITY_ISSUES.yaml"
        if qi.is_file():
            data = load_yaml(qi)
            issues = data.get("issues") if isinstance(data, dict) else data
            open_blocker = open_major = 0
            if isinstance(issues, list):
                for issue in issues:
                    if not isinstance(issue, dict):
                        continue
                    if str(issue.get("status", "OPEN")).upper() != "OPEN":
                        continue
                    sev = str(issue.get("severity", "")).upper()
                    if sev == "BLOCKER":
                        open_blocker += 1
                    elif sev == "MAJOR":
                        open_major += 1
            if open_blocker:
                errors.append(f"OPEN BLOCKER count {open_blocker} != 0")
            if open_major:
                errors.append(f"OPEN MAJOR count {open_major} != 0")

        # WAIKE crosswalk must still exist and cite SHA
        if WAIKE.is_file():
            w = WAIKE.read_text(encoding="utf-8")
            if "e97e74fc9bfb44b1cdc26b272dc4848264f15fe0" not in w:
                errors.append("WAIKE crosswalk missing reconfirmed SHA e97e74fc…")
        else:
            errors.append("missing kids/waike/KIDS_WAIKE_CROSSWALK.yaml")

    if errors:
        print(f"FAIL ({mode}): {len(errors)} issue(s)")
        for e in errors[:80]:
            print(f"  - {e}")
        if len(errors) > 80:
            print(f"  … {len(errors) - 80} more")
        return 1

    print(f"PASS: kids full manuscript family ({mode})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--mode",
        default="all",
        choices=["all", "check", "inventory", "continuity", "accessibility", "safety", "meta"],
    )
    args = ap.parse_args()
    return validate_family(args.mode)


if __name__ == "__main__":
    sys.exit(main())
