#!/usr/bin/env python3
"""Full31 publication / accessibility QA (Agent H).

Writes machine + human reports under publication/full31/quality/.
Does not claim WCAG, EPUB, or human print-quality certification.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import zipfile
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

QUALITY_DIR = ROOT / "publication" / "full31" / "quality"
REPORT_YAML = QUALITY_DIR / "PUBLICATION_QA.yaml"
REPORT_MD = QUALITY_DIR / "ACCESSIBILITY_QA.md"
PRINT_CHECKLIST = QUALITY_DIR / "HUMAN_PRINT_VISUAL_CHECKLIST.md"

FULL31_HTML = ROOT / "preview" / "full31" / "technology-landscape-full31-html"
FULL31_EPUB = ROOT / "preview" / "full31" / "technology-landscape-full31-epub.epub"
FULL31_PDF = ROOT / "preview" / "full31" / "technology-landscape-full31-pdf.pdf"

GENERIC_SECTION_IDS = {
    "sec-moment",
    "sec-notice",
    "sec-ecosystem",
    "sec-signal",
    "sec-components",
    "sec-stability",
    "sec-try",
    "sec-build",
    "sec-secure-include",
    "sec-career",
    "sec-check",
    "sec-glossary",
}

NONDESCRIPTIVE_LINK = re.compile(
    r"\[(?:click here|here|this|this link|read more|link|more)\]\([^)]+\)",
    re.I,
)
LOCAL_READER_HREF = re.compile(
    r"""(?:href|src)\s*=\s*["'](?:https?://(?:localhost|127\.0\.0\.1)(?::\d+)?/|file://|/Users/|/home/)""",
    re.I,
)
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)(\{[^}]*\})?")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+\{#([A-Za-z0-9_.:-]+)\})?\s*$", re.M)
ATTR_ID = re.compile(r"\{#([A-Za-z0-9_.:-]+)")
TABLE_ROW = re.compile(r"^\|.+\|$")
TABLE_SEP = re.compile(r"^\|[\s\-:|]+\|$")
CODE_FENCE = re.compile(r"^```")


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"


def discover_quarto() -> str | None:
    env = os.environ.get("QUARTO_BIN")
    if env and Path(env).is_file() and os.access(env, os.X_OK):
        return env
    local = ROOT / "tools" / "quarto" / "bin" / "quarto"
    if local.is_file() and os.access(local, os.X_OK):
        return str(local)
    which = subprocess.run(["which", "quarto"], capture_output=True, text=True)
    path = (which.stdout or "").strip()
    if path and Path(path).is_file():
        return path
    return None


def issue(
    issues: list[dict[str, Any]],
    *,
    issue_id: str,
    severity: str,
    category: str,
    location: str,
    finding: str,
    evidence: str = "",
    fix_status: str = "OPEN",
) -> None:
    issues.append(
        {
            "issue_id": issue_id,
            "severity": severity,
            "category": category,
            "location": location,
            "finding": finding,
            "evidence": evidence,
            "fix_status": fix_status,
        }
    )


def chapter_paths() -> list[Path]:
    return sorted((ROOT / "book" / "chapters").glob("ch*/chapter.md"))


def heading_hierarchy_ok(text: str) -> tuple[bool, str]:
    levels = [len(m.group(1)) for m in HEADING.finditer(text)]
    if not levels:
        return False, "no headings"
    prev = levels[0]
    for lv in levels[1:]:
        if lv > prev + 1:
            return False, f"skip {prev} -> {lv}"
        prev = lv
    return True, "ok"


def check_source_semantics(issues: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "chapters_scanned": 0,
        "figures_embedded": 0,
        "fig_cap_without_fig_alt": 0,
        "empty_markdown_alts": 0,
        "generic_section_id_collisions": {},
        "heading_hierarchy_failures": [],
        "nondescriptive_links": 0,
        "reader_facing_localhost_or_filesystem": 0,
        "tables_missing_header_sep": 0,
    }
    id_map: dict[str, list[str]] = defaultdict(list)
    n = 0

    for path in chapter_paths():
        summary["chapters_scanned"] += 1
        ch = path.parent.name
        text = path.read_text(encoding="utf-8")
        ok, why = heading_hierarchy_ok(text)
        if not ok:
            summary["heading_hierarchy_failures"].append(f"{ch}: {why}")
            issue(
                issues,
                issue_id=f"A11Y-HEAD-{ch.upper()}",
                severity="MAJOR",
                category="heading_hierarchy",
                location=str(path.relative_to(ROOT)),
                finding=f"Heading hierarchy invalid ({why}).",
            )
        if NONDESCRIPTIVE_LINK.search(text):
            summary["nondescriptive_links"] += 1
            issue(
                issues,
                issue_id=f"A11Y-LINK-{ch.upper()}",
                severity="MAJOR",
                category="link_text",
                location=str(path.relative_to(ROOT)),
                finding="Non-descriptive link text (e.g. 'click here').",
            )
        for label, target in MD_LINK.findall(text):
            if target.startswith(("http://localhost", "https://localhost", "http://127.", "file://")):
                summary["reader_facing_localhost_or_filesystem"] += 1
                issue(
                    issues,
                    issue_id=f"A11Y-LOCAL-{ch.upper()}-{n}",
                    severity="BLOCKER",
                    category="reader_links",
                    location=str(path.relative_to(ROOT)),
                    finding=f"Reader-facing local/filesystem link: {target}",
                    evidence=label,
                )
                n += 1

        for m in MD_IMAGE.finditer(text):
            summary["figures_embedded"] += 1
            alt, src, attrs = m.group(1), m.group(2), m.group(3) or ""
            if not alt.strip():
                summary["empty_markdown_alts"] += 1
                issue(
                    issues,
                    issue_id=f"A11Y-ALT-MD-{ch.upper()}-{n}",
                    severity="MAJOR",
                    category="figure_alt",
                    location=str(path.relative_to(ROOT)),
                    finding=f"Empty markdown alt for {src}",
                )
                n += 1
            if "fig-cap" in attrs and "fig-alt" not in attrs:
                summary["fig_cap_without_fig_alt"] += 1

        for m in ATTR_ID.finditer(text):
            id_map[m.group(1)].append(ch)

        lines = text.splitlines()
        for i, line in enumerate(lines):
            if TABLE_ROW.match(line) and i + 1 < len(lines) and not TABLE_SEP.match(lines[i + 1]):
                # Only flag when next line looks like another table row (missing sep)
                if TABLE_ROW.match(lines[i + 1]) and not TABLE_SEP.match(lines[i + 1]):
                    # Heuristic: header row without separator
                    if i == 0 or not TABLE_ROW.match(lines[i - 1]):
                        summary["tables_missing_header_sep"] += 1
                        issue(
                            issues,
                            issue_id=f"A11Y-TABLE-{ch.upper()}-{i}",
                            severity="MODERATE",
                            category="table_headers",
                            location=f"{path.relative_to(ROOT)}:{i+1}",
                            finding="Markdown table appears to lack header separator row.",
                        )

    collisions = {
        k: sorted(set(v))
        for k, v in id_map.items()
        if k in GENERIC_SECTION_IDS and len(set(v)) > 1
    }
    summary["generic_section_id_collisions"] = collisions
    if collisions:
        issue(
            issues,
            issue_id="A11Y-ID-COLLISION",
            severity="MAJOR",
            category="heading_ids",
            location="book/chapters/*/chapter.md",
            finding=(
                "Generic section IDs collide across chapters (EPUB/HTML duplicate "
                f"identifiers): {', '.join(sorted(collisions))}"
            ),
            evidence=str({k: len(v) for k, v in collisions.items()}),
        )
    if summary["fig_cap_without_fig_alt"]:
        issue(
            issues,
            issue_id="A11Y-FIG-ALT-ATTR",
            severity="BLOCKER",
            category="figure_alt",
            location="book/chapters/*/chapter.md figure embeds",
            finding=(
                "Quarto HTML/EPUB emit empty or missing img alt when fig-cap is set "
                "without fig-alt. "
                f"{summary['fig_cap_without_fig_alt']} embeds lack fig-alt."
            ),
        )
    return summary


def check_figure_accessibility(issues: list[dict[str, Any]]) -> dict[str, Any]:
    reg_path = ROOT / "figures" / "figure_registry.yaml"
    reg = load_yaml(reg_path)
    figs = reg.get("figures") or []
    summary = {
        "registry_count": len(figs),
        "missing_sidecar": 0,
        "missing_asset": 0,
        "missing_fields": 0,
        "color_only_risk_notes": 0,
    }
    required = ("alt_text", "text_equivalent", "caption", "reading_order", "status")
    for fig in figs:
        fid = fig.get("figure_id", "?")
        asset = ROOT / fig.get("path", "")
        acc_path = ROOT / fig.get("accessibility", "")
        if not asset.exists():
            summary["missing_asset"] += 1
            issue(
                issues,
                issue_id=f"A11Y-FIG-ASSET-{fid}",
                severity="BLOCKER",
                category="figures",
                location=str(fig.get("path")),
                finding="Figure asset missing",
            )
        if not acc_path.exists():
            summary["missing_sidecar"] += 1
            issue(
                issues,
                issue_id=f"A11Y-FIG-ACC-{fid}",
                severity="BLOCKER",
                category="figures",
                location=str(fig.get("accessibility")),
                finding="Accessibility sidecar missing",
            )
            continue
        acc = load_yaml(acc_path) or {}
        for field in required:
            if not acc.get(field):
                summary["missing_fields"] += 1
                issue(
                    issues,
                    issue_id=f"A11Y-FIG-FIELD-{fid}-{field}",
                    severity="MAJOR",
                    category="figures",
                    location=str(acc_path.relative_to(ROOT)),
                    finding=f"Missing accessibility field {field}",
                )
        # Color-only heuristic: SVG should have text labels or dash/pattern encoding
        if asset.exists() and asset.suffix.lower() == ".svg":
            svg = asset.read_text(encoding="utf-8", errors="replace")
            has_text = bool(re.search(r"<text[\s>]", svg))
            has_noncolor = ("stroke-dasharray" in svg) or ("pattern" in svg.lower()) or has_text
            if not has_noncolor:
                summary["color_only_risk_notes"] += 1
                issue(
                    issues,
                    issue_id=f"A11Y-COLOR-{fid}",
                    severity="MODERATE",
                    category="color_encoding",
                    location=str(asset.relative_to(ROOT)),
                    finding="SVG lacks visible <text>, dash, or pattern cues (color-only risk).",
                    fix_status="NEEDS_HUMAN",
                )
    return summary


def check_labs(issues: list[dict[str, Any]]) -> dict[str, Any]:
    reg = load_yaml(ROOT / "labs" / "lab_registry.yaml")
    summary = {
        "labs": 0,
        "missing_accessible_routes": 0,
        "browser_missing_lang": 0,
        "browser_missing_live_region": 0,
        "a11y_doc_present": 0,
    }
    for item in reg.get("labs") or []:
        summary["labs"] += 1
        lab_id = item["lab_id"]
        lab_dir = ROOT / item["path"]
        lab = load_yaml(lab_dir / "lab.yaml") if (lab_dir / "lab.yaml").exists() else {}
        routes = (lab or {}).get("accessible_routes") or {}
        if not routes.get("no_specialized_hardware"):
            summary["missing_accessible_routes"] += 1
            issue(
                issues,
                issue_id=f"A11Y-LAB-ROUTE-{lab_id}",
                severity="MAJOR",
                category="lab_a11y",
                location=str((lab_dir / "lab.yaml").relative_to(ROOT)),
                finding="Missing no_specialized_hardware accessible route",
            )
        a11y_docs = list(lab_dir.glob("*ACCESSIBILITY*")) + list(lab_dir.glob("*A11Y*"))
        if a11y_docs:
            summary["a11y_doc_present"] += 1
        browser = lab_dir / "browser" / "index.html"
        if browser.exists():
            html = browser.read_text(encoding="utf-8", errors="replace")
            if not re.search(r"<html[^>]*\blang=", html, re.I):
                summary["browser_missing_lang"] += 1
                issue(
                    issues,
                    issue_id=f"A11Y-LAB-LANG-{lab_id}",
                    severity="MAJOR",
                    category="lab_a11y",
                    location=str(browser.relative_to(ROOT)),
                    finding="Lab browser HTML missing lang attribute",
                )
            if "aria-live" not in html and 'role="status"' not in html:
                summary["browser_missing_live_region"] += 1
                issue(
                    issues,
                    issue_id=f"A11Y-LAB-LIVE-{lab_id}",
                    severity="MODERATE",
                    category="lab_a11y",
                    location=str(browser.relative_to(ROOT)),
                    finding="Interactive lab HTML lacks aria-live/status region",
                    fix_status="NEEDS_HUMAN",
                )
    return summary


def check_acronyms(issues: list[dict[str, Any]]) -> dict[str, Any]:
    path = ROOT / "glossary" / "acronym_registry.yaml"
    summary: dict[str, Any] = {
        "registry_entries": 0,
        "identity_expansions": 0,
        "first_use_heuristic": "source_scan_limited",
    }
    if not path.exists():
        issue(
            issues,
            issue_id="A11Y-ACRO-REG",
            severity="MODERATE",
            category="acronyms",
            location=str(path),
            finding="Acronym registry missing",
        )
        return summary
    data = load_yaml(path) or {}
    rows = data.get("acronyms") or []
    summary["registry_entries"] = len(rows)
    identity = []
    for row in rows:
        acr = str(row.get("acronym") or "")
        exp = str(row.get("expands_to") or "")
        if acr and exp and acr.upper() == exp.upper():
            identity.append(acr)
    summary["identity_expansions"] = len(identity)
    if identity:
        issue(
            issues,
            issue_id="A11Y-ACRO-IDENTITY",
            severity="MODERATE",
            category="acronyms",
            location=str(path.relative_to(ROOT)),
            finding=(
                "Acronym registry entries expand to themselves "
                f"({len(identity)}): first-use expansion not machine-checkable."
            ),
            evidence=", ".join(identity[:20]),
            fix_status="HANDOFF_AGENT_J",
        )
    return summary


class _AnchorCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.imgs_missing_alt = 0
        self.imgs_total = 0
        self.has_lang = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag == "html" and (ad.get("lang") or ad.get("xml:lang")):
            self.has_lang = True
        if "id" in ad and ad["id"]:
            self.ids.add(ad["id"])
        if tag == "a" and ad.get("href"):
            self.hrefs.append(ad["href"])
        if tag == "img":
            self.imgs_total += 1
            alt = ad.get("alt")
            if alt is None or not str(alt).strip():
                self.imgs_missing_alt += 1


def check_html(issues: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "artifact_present": FULL31_HTML.is_dir(),
        "pages": 0,
        "missing_lang": 0,
        "imgs_total": 0,
        "imgs_missing_alt": 0,
        "broken_internal_anchors": 0,
        "reader_facing_localhost_href": 0,
        "nav_sidebar_detected": False,
    }
    if not FULL31_HTML.is_dir():
        issue(
            issues,
            issue_id="HTML-ARTIFACT-MISSING",
            severity="MAJOR",
            category="html",
            location=str(FULL31_HTML.relative_to(ROOT)),
            finding="full31 HTML artifact not present; run make full31-html",
            fix_status="TOOLING",
        )
        return summary

    pages = sorted(FULL31_HTML.rglob("*.html"))
    summary["pages"] = len(pages)
    # index nav heuristic
    index = FULL31_HTML / "index.html"
    if index.exists():
        idx = index.read_text(encoding="utf-8", errors="replace")
        summary["nav_sidebar_detected"] = (
            "quarto-sidebar" in idx or 'id="TOC"' in idx or "sidebar" in idx[:8000]
        )

    page_data: dict[Path, _AnchorCollector] = {}
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        # Ignore Quarto clipboard JS mentioning localhost as a regex, not an href
        if LOCAL_READER_HREF.search(text):
            summary["reader_facing_localhost_href"] += 1
            issue(
                issues,
                issue_id=f"HTML-LOCAL-{page.name}",
                severity="BLOCKER",
                category="html_links",
                location=str(page.relative_to(ROOT)),
                finding="Reader-facing localhost/filesystem href/src detected",
            )
        parser = _AnchorCollector()
        try:
            parser.feed(text)
        except Exception as exc:  # noqa: BLE001
            issue(
                issues,
                issue_id=f"HTML-PARSE-{page.name}",
                severity="MODERATE",
                category="html",
                location=str(page.relative_to(ROOT)),
                finding=f"HTML parse error: {exc}",
            )
            continue
        if not parser.has_lang:
            summary["missing_lang"] += 1
            issue(
                issues,
                issue_id=f"HTML-LANG-{page.name}",
                severity="MAJOR",
                category="html_lang",
                location=str(page.relative_to(ROOT)),
                finding="HTML page missing lang/xml:lang",
            )
        summary["imgs_total"] += parser.imgs_total
        summary["imgs_missing_alt"] += parser.imgs_missing_alt
        page_data[page] = parser

    if summary["imgs_missing_alt"]:
        issue(
            issues,
            issue_id="HTML-IMG-ALT",
            severity="BLOCKER",
            category="html_alt",
            location=str(FULL31_HTML.relative_to(ROOT)),
            finding=(
                f"{summary['imgs_missing_alt']}/{summary['imgs_total']} HTML <img> "
                "tags missing non-empty alt (Quarto fig-cap without fig-alt)."
            ),
        )

    # Internal hash targets within same page + relative files
    for page, parser in page_data.items():
        for href in parser.hrefs:
            if href.startswith("#"):
                target = href[1:]
                if target and target not in parser.ids:
                    # Quarto may generate ids lazily; only count explicit missing
                    summary["broken_internal_anchors"] += 1
            elif href.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            else:
                rel = href.split("#", 1)[0]
                if not rel:
                    continue
                dest = (page.parent / rel).resolve()
                try:
                    dest.relative_to(FULL31_HTML.resolve())
                except ValueError:
                    continue
                if not dest.exists():
                    summary["broken_internal_anchors"] += 1
                    issue(
                        issues,
                        issue_id=f"HTML-BROKEN-{page.name}-{summary['broken_internal_anchors']}",
                        severity="MAJOR",
                        category="html_links",
                        location=str(page.relative_to(ROOT)),
                        finding=f"Broken relative link: {href}",
                    )
    return summary


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def check_epub(issues: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "artifact_present": FULL31_EPUB.is_file(),
        "validator": "deterministic_structural_checks",
        "epubcheck": "PENDING_EXTERNAL_RUNNER",
        "epubcheck_limitation": (
            "Official W3C EPUBCheck is invoked via scripts/run_epubcheck.py "
            "(pinned release downloaded to tools/cache/, not vendored). "
            "Deterministic ZIP/OPF/nav/spine/image checks always run here."
        ),
        "mimetype_ok": False,
        "container_ok": False,
        "opf_ok": False,
        "nav_ok": False,
        "spine_ok": False,
        "dc_language": None,
        "dc_title": None,
        "dc_creator": None,
        "imgs_total": 0,
        "imgs_missing_alt": 0,
        "xhtml_missing_lang": 0,
    }
    if not FULL31_EPUB.is_file():
        issue(
            issues,
            issue_id="EPUB-ARTIFACT-MISSING",
            severity="MAJOR",
            category="epub",
            location=str(FULL31_EPUB.relative_to(ROOT)),
            finding="full31 EPUB artifact not present; run make full31-epub",
            fix_status="TOOLING",
        )
        return summary

    with zipfile.ZipFile(FULL31_EPUB) as zf:
        names = set(zf.namelist())
        if "mimetype" in names:
            raw = zf.read("mimetype")
            summary["mimetype_ok"] = raw == b"application/epub+zip"
        summary["container_ok"] = "META-INF/container.xml" in names
        opf_name = None
        if summary["container_ok"]:
            container = ET.fromstring(zf.read("META-INF/container.xml"))
            for node in container.iter():
                if _local_name(node.tag) == "rootfile":
                    opf_name = node.attrib.get("full-path")
                    break
        if not opf_name:
            # fallback
            for n in names:
                if n.endswith(".opf"):
                    opf_name = n
                    break
        if not opf_name or opf_name not in names:
            issue(
                issues,
                issue_id="EPUB-OPF-MISSING",
                severity="BLOCKER",
                category="epub",
                location=str(FULL31_EPUB.relative_to(ROOT)),
                finding="EPUB package document (OPF) missing",
            )
            return summary
        summary["opf_ok"] = True
        opf = ET.fromstring(zf.read(opf_name))
        for node in opf.iter():
            ln = _local_name(node.tag)
            if ln == "language" and node.text:
                summary["dc_language"] = node.text.strip()
            elif ln == "title" and node.text and not summary["dc_title"]:
                summary["dc_title"] = node.text.strip()
            elif ln == "creator" and node.text and not summary["dc_creator"]:
                summary["dc_creator"] = node.text.strip()
            elif ln == "spine":
                summary["spine_ok"] = True
            elif ln == "item" and node.attrib.get("properties", "").find("nav") >= 0:
                summary["nav_ok"] = True
        if not summary["nav_ok"]:
            summary["nav_ok"] = any(n.endswith("nav.xhtml") for n in names)

        if summary["dc_language"] not in {"en", "en-US", "en-GB"}:
            issue(
                issues,
                issue_id="EPUB-LANG",
                severity="BLOCKER",
                category="epub_language",
                location=str(FULL31_EPUB.relative_to(ROOT)),
                finding=(
                    f"EPUB dc:language is '{summary['dc_language']}' "
                    "(expected en*). Often inherited from process LANG=C.*"
                ),
            )
        if not summary["mimetype_ok"]:
            issue(
                issues,
                issue_id="EPUB-MIMETYPE",
                severity="BLOCKER",
                category="epub",
                location=str(FULL31_EPUB.relative_to(ROOT)),
                finding="EPUB mimetype missing or incorrect",
            )
        if not summary["spine_ok"]:
            issue(
                issues,
                issue_id="EPUB-SPINE",
                severity="BLOCKER",
                category="epub",
                location=str(FULL31_EPUB.relative_to(ROOT)),
                finding="EPUB spine missing",
            )
        if not summary["nav_ok"]:
            issue(
                issues,
                issue_id="EPUB-NAV",
                severity="MAJOR",
                category="epub",
                location=str(FULL31_EPUB.relative_to(ROOT)),
                finding="EPUB navigation document not detected",
            )

        for name in names:
            if not name.endswith((".xhtml", ".html")):
                continue
            data = zf.read(name).decode("utf-8", errors="replace")
            if not re.search(r"\blang=|\bxml:lang=", data[:800], re.I):
                summary["xhtml_missing_lang"] += 1
            for attrs in re.findall(r"<img\b([^>]*)>", data, flags=re.I):
                summary["imgs_total"] += 1
                m = re.search(r'\balt=(["\'])(.*?)\1', attrs, flags=re.I | re.S)
                if not m or not m.group(2).strip():
                    summary["imgs_missing_alt"] += 1

    if summary["imgs_missing_alt"]:
        issue(
            issues,
            issue_id="EPUB-IMG-ALT",
            severity="BLOCKER",
            category="epub_alt",
            location=str(FULL31_EPUB.relative_to(ROOT)),
            finding=(
                f"{summary['imgs_missing_alt']}/{summary['imgs_total']} EPUB images "
                "have empty/missing alt"
            ),
        )
    if summary["xhtml_missing_lang"]:
        issue(
            issues,
            issue_id="EPUB-XHTML-LANG",
            severity="MAJOR",
            category="epub_language",
            location=str(FULL31_EPUB.relative_to(ROOT)),
            finding=f"{summary['xhtml_missing_lang']} XHTML documents missing lang",
        )
    return summary


def pdf_page_count(path: Path) -> int | None:
    """Best-effort page count for compressed Quarto/XeLaTeX PDFs."""
    try:
        from pypdf import PdfReader  # type: ignore

        return len(PdfReader(str(path)).pages)
    except Exception:
        pass
    raw = path.read_bytes()
    hits = len(re.findall(rb"/Type\s*/Page(?!s)\b", raw))
    if hits:
        return hits
    # Fallback: parse XeTeX "Output written on ... (N pages)" from sibling logs
    for log in (
        Path("/tmp/full31-pdf-render.log"),
        ROOT / "_book" / "The-Technology-Landscape.log",
    ):
        if not log.exists():
            continue
        text = log.read_text(encoding="utf-8", errors="replace")
        m = re.findall(r"Output written on .*?\((\d+) pages?\)", text)
        if m:
            return int(m[-1])
    return None


def check_pdf(issues: list[dict[str, Any]], log_path: Path | None) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "artifact_present": FULL31_PDF.is_file(),
        "page_count": None,
        "render_success": False,
        "overfull_hbox": 0,
        "overfull_vbox": 0,
        "underfull_hbox": 0,
        "missing_image_log_hits": 0,
        "duplicate_identifier_warnings": 0,
        "blank_page_heuristic": "not_automated",
        "orphan_heading_heuristic": "not_automated",
        "tiny_text_heuristic": "not_automated",
        "clipping_heuristic": "not_automated",
        "wide_table_heuristic": "log_overfull_proxy",
    }
    if FULL31_PDF.is_file():
        summary["render_success"] = True
        summary["page_count"] = pdf_page_count(FULL31_PDF)
        # Spot-check LaTeX chapter counter inflation (known Quarto/book risk).
        try:
            from pypdf import PdfReader  # type: ignore

            reader = PdfReader(str(FULL31_PDF))
            max_loose = 0
            loose_hits = 0
            latex_headers: set[int] = set()
            body_title_hits = 0
            for page in reader.pages:
                text = page.extract_text() or ""
                for m in re.finditer(r"(?i)\bchapter\s+(\d+)\b", text):
                    loose_hits += 1
                    max_loose = max(max_loose, int(m.group(1)))
                # Prefer LaTeX running-header / chapter-open style: "CHAPTER 12."
                for m in re.finditer(r"(?i)\bCHAPTER\s+(\d+)\.\s+", text):
                    latex_headers.add(int(m.group(1)))
                if re.search(
                    r"(?i)Chapter\s+\d+\s+[—\-].{0,80}(System|Stack|Performance|Quartet)",
                    text,
                ):
                    body_title_hits += 1
            max_latex = max(latex_headers) if latex_headers else 0
            summary["pdf_max_chapter_number_seen"] = max_loose
            summary["pdf_chapter_number_mentions"] = loose_hits
            summary["pdf_latex_chapter_headers"] = sorted(latex_headers)
            summary["pdf_max_latex_chapter_header"] = max_latex
            summary["pdf_body_title_hits"] = body_title_hits
            body_headers = sorted(n for n in latex_headers if 1 <= n <= 31)
            backmatter_numeric = sorted(n for n in latex_headers if n > 31)
            summary["pdf_body_chapter_headers"] = body_headers
            summary["pdf_backmatter_numeric_chapter_headers"] = backmatter_numeric
            summary["pdf_body_chapter_header_count"] = len(body_headers)
            # True inflation: LaTeX chapter headers climb far past ~31 body + appendices.
            # Loose "chapter N" text matches are noisy (page merges / cross refs).
            if max_latex > 45:
                issue(
                    issues,
                    issue_id="PDF-CHAPTER-COUNTER",
                    severity="MAJOR",
                    category="pdf_structure",
                    location=str(FULL31_PDF.relative_to(ROOT)),
                    finding=(
                        f"PDF LaTeX-style CHAPTER N. headers reach {max_latex} "
                        f"({summary['page_count']} pages; loose text max={max_loose}). "
                        "Expected ~31 body chapters; likely counter inflation."
                    ),
                    fix_status="OPEN",
                )
            elif backmatter_numeric:
                issue(
                    issues,
                    issue_id="PDF-BACKMATTER-NUMBERING",
                    severity="MAJOR",
                    category="pdf_structure",
                    location=str(FULL31_PDF.relative_to(ROOT)),
                    finding=(
                        "PDF still emits numeric CHAPTER N. headers for back matter: "
                        f"{backmatter_numeric}. Expected unnumbered backmatter "
                        "(\\backmatter) or appendix lettering—not Chapter 32+."
                    ),
                    fix_status="OPEN",
                )
            elif max_latex and max_latex <= 31 and not backmatter_numeric:
                issue(
                    issues,
                    issue_id="PDF-FRONTMATTER-NUMBERING",
                    severity="MODERATE",
                    category="pdf_structure",
                    location=str(FULL31_PDF.relative_to(ROOT)),
                    finding=(
                        "PDF body LaTeX CHAPTER headers are within 1..31 "
                        f"(max={max_latex}); no Chapter 32+ backmatter inflation after "
                        "\\frontmatter/\\mainmatter/\\backmatter. Residual TOC cosmetics "
                        "are human print review only."
                    ),
                    evidence=(
                        f"body_headers_sample={body_headers[:12]}; "
                        f"count={len(body_headers)}; backmatter_numeric=[]"
                    ),
                    fix_status="FIXED",
                )
            elif max_latex and max_latex <= 45:
                toc_sample = ""
                if reader.pages:
                    toc_sample = (reader.pages[min(2, len(reader.pages) - 1)].extract_text() or "")[
                        :1200
                    ]
                if re.search(r"(?i)Manuscript status|Know first|Device Quartet", toc_sample):
                    issue(
                        issues,
                        issue_id="PDF-FRONTMATTER-NUMBERING",
                        severity="MODERATE",
                        category="pdf_structure",
                        location=str(FULL31_PDF.relative_to(ROOT)),
                        finding=(
                            "Front/back matter may still appear as arabic-numbered "
                            "chapters in the PDF TOC despite number: false; body "
                            f"LaTeX headers max={max_latex}. Human print QA should "
                            "confirm unnumbered frontmatter styling."
                        ),
                        fix_status="NEEDS_HUMAN",
                    )
        except Exception as exc:  # noqa: BLE001
            summary["pdf_text_scan_error"] = str(exc)
    else:
        issue(
            issues,
            issue_id="PDF-ARTIFACT-MISSING",
            severity="MAJOR",
            category="pdf",
            location=str(FULL31_PDF.relative_to(ROOT)),
            finding="full31 PDF artifact not present; run make full31-pdf",
            fix_status="TOOLING",
        )

    logs: list[Path] = []
    if log_path and log_path.exists():
        logs.append(log_path)
    # Quarto may leave tex logs under _book or preview
    for cand in [
        ROOT / "_book" / "The-Technology-Landscape.log",
        Path("/tmp/full31-pdf-render.log"),
    ]:
        if cand.exists() and cand not in logs:
            logs.append(cand)

    for log in logs:
        text = log.read_text(encoding="utf-8", errors="replace")
        summary["overfull_hbox"] += len(re.findall(r"Overfull \\hbox", text))
        summary["overfull_vbox"] += len(re.findall(r"Overfull \\vbox", text))
        summary["underfull_hbox"] += len(re.findall(r"Underfull \\hbox", text))
        summary["missing_image_log_hits"] += len(
            re.findall(r"File `[^']+' not found|Unable to load picture", text)
        )
        summary["duplicate_identifier_warnings"] += len(
            re.findall(r"Duplicate identifier", text)
        )

    if summary["overfull_hbox"] or summary["overfull_vbox"]:
        issue(
            issues,
            issue_id="PDF-OVERFULL",
            severity="MODERATE",
            category="pdf_layout",
            location="TeX/Quarto log",
            finding=(
                f"Overfull boxes detected (hbox={summary['overfull_hbox']}, "
                f"vbox={summary['overfull_vbox']}); possible wide tables/figures."
            ),
            fix_status="NEEDS_HUMAN",
        )
    if summary["missing_image_log_hits"]:
        issue(
            issues,
            issue_id="PDF-MISSING-IMAGE",
            severity="BLOCKER",
            category="pdf_figures",
            location="TeX/Quarto log",
            finding=f"Missing image indicators in log: {summary['missing_image_log_hits']}",
        )
    if summary["duplicate_identifier_warnings"]:
        issue(
            issues,
            issue_id="PDF-DUP-ID",
            severity="MAJOR",
            category="heading_ids",
            location="Pandoc/Quarto warnings",
            finding=(
                f"{summary['duplicate_identifier_warnings']} duplicate identifier "
                "warnings during render"
            ),
        )
    return summary


def write_print_checklist() -> None:
    PRINT_CHECKLIST.write_text(
        """# Human visual / print checklist (stub)

**Status:** NOT RUN — human review required later.  
**Do not treat this file as print-quality approval.**

Use after automated `make full31-publication-qa` is green or findings are triaged.

## Setup

- [ ] Print or soft-proof the current full31 PDF on target trim/paper
- [ ] Compare color and grayscale proofs for non-color encodings
- [ ] Confirm correct PDF build SHA recorded in `PUBLICATION_QA.yaml`

## First-pass visual

- [ ] Title page / status banner readable and truthful
- [ ] TOC page numbers match chapter openings
- [ ] No obviously blank spread where content was expected
- [ ] Running heads / folios present and not colliding with content
- [ ] Chapter-opening orphans/widows acceptable

## Figures

- [ ] Every figure present; no missing-image boxes
- [ ] Captions and figure IDs present and match narrative references
- [ ] Labels legible at print size (no tiny unreadable text)
- [ ] No clipped SVG/path edges at trim
- [ ] Color is not the sole encoding (labels, line style, or pattern)

## Tables / code

- [ ] Wide tables do not spill past margins
- [ ] Code blocks remain readable (wrapping vs overflow intentional)

## Accessibility spot-check (human)

- [ ] Sample screen-reader pass on HTML edition (2–3 chapters)
- [ ] Keyboard-only pass on lab browser routes
- [ ] Acronym first-use expansions sound natural in prose

## Sign-off

- Reviewer:
- Date:
- Build SHA:
- Result: PASS / FAIL / DEFER (never auto-claimed by CI)
""",
        encoding="utf-8",
    )


def write_markdown_report(report: dict[str, Any]) -> None:
    lines = [
        "# Accessibility + publication QA (full31)",
        "",
        f"- **Generated:** {report['generated_at']}",
        f"- **Git SHA:** `{report['git_sha']}`",
        f"- **Agent:** {report['agent']}",
        "",
        "## Certification posture",
        "",
        "This report records **automated checks only**.",
        "It does **not** certify WCAG conformance, EPUB accessibility,",
        "or human print quality.",
        "",
        "## Toolchain",
        "",
        f"- Quarto: `{report['toolchain']['quarto']}`",
        f"- LOCAL_RENDER_TOOLCHAIN_UNAVAILABLE: "
        f"**{report['toolchain']['LOCAL_RENDER_TOOLCHAIN_UNAVAILABLE']}**",
        "",
        "## Severity counts",
        "",
    ]
    counts = report.get("severity_counts") or {}
    for sev in ("BLOCKER", "MAJOR", "MODERATE", "MINOR", "EDITORIAL"):
        lines.append(f"- {sev}: {counts.get(sev, 0)}")
    lines += ["", "## Artifacts", ""]
    arts = report.get("artifacts") or {}
    for k, v in arts.items():
        lines.append(f"- **{k}:** `{v}`")
    lines += ["", "## Findings", ""]
    for item in report.get("issues") or []:
        lines.append(
            f"### {item['issue_id']} ({item['severity']} / {item['category']})"
        )
        lines.append("")
        lines.append(f"- Location: `{item['location']}`")
        lines.append(f"- Status: `{item['fix_status']}`")
        lines.append(f"- Finding: {item['finding']}")
        if item.get("evidence"):
            lines.append(f"- Evidence: {item['evidence']}")
        lines.append("")
    lines += [
        "## Human follow-ups",
        "",
        "- See `HUMAN_PRINT_VISUAL_CHECKLIST.md` (stub; not executed).",
        "- Acronym expansion quality handed to terminology/glossary owners when registry is identity-only.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def build_report(pdf_log: Path | None) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    quarto = discover_quarto()
    toolchain_unavailable = quarto is None
    if toolchain_unavailable:
        issue(
            issues,
            issue_id="TOOLCHAIN-QUARTO",
            severity="MAJOR",
            category="toolchain",
            location="tools/quarto or PATH",
            finding="Quarto not found; LOCAL_RENDER_TOOLCHAIN_UNAVAILABLE is truthful.",
            fix_status="TOOLING",
        )

    source = check_source_semantics(issues)
    figures = check_figure_accessibility(issues)
    labs = check_labs(issues)
    acronyms = check_acronyms(issues)
    html = check_html(issues)
    epub = check_epub(issues)
    # Merge official EPUBCheck result if present (from make full31-epubcheck).
    epubcheck_json = QUALITY_DIR / "EPUBCHECK_RESULT.json"
    if epubcheck_json.is_file():
        try:
            payload = json.loads(epubcheck_json.read_text(encoding="utf-8"))
            epub["epubcheck"] = payload.get("status") or "UNKNOWN"
            epub["epubcheck_version"] = payload.get("version")
            epub["epubcheck_errors"] = payload.get("errors")
            epub["epubcheck_fatal_errors"] = payload.get("fatal_errors")
            epub["epubcheck_warnings"] = payload.get("warnings")
            if payload.get("limitation"):
                epub["epubcheck_limitation"] = payload.get("limitation")
            else:
                epub["epubcheck_limitation"] = (
                    "Official W3C EPUBCheck executed; not an accessibility certification."
                )
            status = str(payload.get("status") or "")
            if status not in {"PASS", "PASS_WITH_WARNINGS"} and status not in {
                "TOOLING_UNAVAILABLE",
                "DOWNLOAD_FAILED",
                "NOT_RUN",
            }:
                issue(
                    issues,
                    issue_id="EPUBCHECK-FAIL",
                    severity="MAJOR",
                    category="epub",
                    location=str(FULL31_EPUB.relative_to(ROOT)),
                    finding=(
                        f"W3C EPUBCheck {payload.get('version')} status={status} "
                        f"(errors={payload.get('errors')} fatal={payload.get('fatal_errors')})"
                    ),
                    fix_status="OPEN",
                )
        except Exception as exc:  # noqa: BLE001
            epub["epubcheck_merge_error"] = str(exc)
    pdf = check_pdf(issues, pdf_log)

    counts: dict[str, int] = defaultdict(int)
    for item in issues:
        counts[item["severity"]] += 1

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "report_id": "FULL31_PUBLICATION_QA",
        "agent": "agent-h-publication-qa",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_sha": git_sha(),
        "preferred_base_branch": "cursor/full31-quality-convergence-001",
        "gate_3_policy": "DO_NOT_TOUCH",
        "certification_claims": {
            "wcag": False,
            "epub_accessibility": False,
            "human_print_quality": False,
        },
        "toolchain": {
            "quarto": quarto or "MISSING",
            "LOCAL_RENDER_TOOLCHAIN_UNAVAILABLE": toolchain_unavailable,
        },
        "artifacts": {
            "html": str(FULL31_HTML.relative_to(ROOT))
            if FULL31_HTML.exists()
            else "ABSENT",
            "epub": str(FULL31_EPUB.relative_to(ROOT))
            if FULL31_EPUB.exists()
            else "ABSENT",
            "pdf": str(FULL31_PDF.relative_to(ROOT)) if FULL31_PDF.exists() else "ABSENT",
            "print_checklist": str(PRINT_CHECKLIST.relative_to(ROOT)),
        },
        "severity_counts": {
            "BLOCKER": counts["BLOCKER"],
            "MAJOR": counts["MAJOR"],
            "MODERATE": counts["MODERATE"],
            "MINOR": counts["MINOR"],
            "EDITORIAL": counts["EDITORIAL"],
        },
        "checks": {
            "source_semantics": source,
            "figures": figures,
            "labs": labs,
            "acronyms": acronyms,
            "html": html,
            "epub": epub,
            "pdf": pdf,
        },
        "issues": issues,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pdf-log",
        type=Path,
        default=Path("/tmp/full31-pdf-render.log"),
        help="Optional Quarto/TeX log path for PDF diagnostics",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        default=True,
        help="Write YAML/MD reports (default true)",
    )
    parser.add_argument(
        "--fail-on-blocker",
        action="store_true",
        default=True,
        help="Exit 1 when BLOCKER findings remain OPEN (default)",
    )
    parser.add_argument(
        "--allow-blockers",
        action="store_true",
        help="Exit 0 even when blockers are present (report-only)",
    )
    args = parser.parse_args()

    QUALITY_DIR.mkdir(parents=True, exist_ok=True)
    write_print_checklist()
    report = build_report(args.pdf_log if args.pdf_log.exists() else None)

    if args.write:
        REPORT_YAML.write_text(dump_yaml(report), encoding="utf-8")
        write_markdown_report(report)

    blockers_open = [
        i
        for i in report["issues"]
        if i["severity"] == "BLOCKER" and i.get("fix_status") == "OPEN"
    ]
    print("publication_qa_full31:")
    print(f"  sha: {report['git_sha']}")
    print(f"  blockers_open: {len(blockers_open)}")
    print(f"  severity: {report['severity_counts']}")
    print(f"  wrote: {REPORT_YAML.relative_to(ROOT)}")
    print(f"  wrote: {REPORT_MD.relative_to(ROOT)}")
    print(f"  wrote: {PRINT_CHECKLIST.relative_to(ROOT)}")
    print("NOTE: automated checks do not certify WCAG/EPUB/print quality.")

    if args.allow_blockers:
        return 0
    if args.fail_on_blocker and blockers_open:
        print("publication_qa_full31: FAIL (open blockers)")
        for b in blockers_open[:20]:
            print(f" - {b['issue_id']}: {b['finding']}")
        return 1
    print("publication_qa_full31: PASS (no open blockers)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
