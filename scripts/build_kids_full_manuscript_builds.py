#!/usr/bin/env python3
"""Build HTML + PDF review prototypes for Kids full manuscript family.

Banner on all builds:
  KIDS FULL WORKING MANUSCRIPT
  NOT CHILD-VALIDATED
  NOT PUBLICATION-READY

EPUB: generate reflowable candidates for ELEM1/ELEM2 only; run EPUBCheck when available.
BABY/TODDLER: print-first — no vanity EPUB.
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import textwrap
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "kids" / "books"
BANNER = (
    "KIDS FULL WORKING MANUSCRIPT\n"
    "NOT CHILD-VALIDATED\n"
    "NOT PUBLICATION-READY"
)
BANDS = [
    ("KIDS-BABY", "BABY", "0–18 months"),
    ("KIDS-TODDLER", "TODDLER", "18–36 months"),
    ("KIDS-PRESCHOOL", "PRESCHOOL", "3–4 years"),
    ("KIDS-PREK", "PREK", "4–6 years"),
    ("KIDS-ELEM1", "ELEM1", "Kindergarten–Grade 2"),
    ("KIDS-ELEM2", "ELEM2", "Grades 3–5/6"),
]
EPUB_CANDIDATES = {"KIDS-ELEM1", "KIDS-ELEM2"}

UNIT_RE = re.compile(r"^##\s+(Unit|UNIT)\s+", re.M)
SPREAD_RE = re.compile(r"^###?\s+.*?(LOOK|POINT|NAME|WAIT|RESPOND|REPEAT|STORY|NOTICE|CONNECT|PREDICT|TRY|EXPLAIN|MAKE|SAFE|TEACH|OBSERVE|TEST|MEASURE|BUILD|SECURE|REFLECT)\b", re.M | re.I)
CHILD_RE = re.compile(r"\*\*Child-facing text:\*\*\s*(.+?)(?=\n\n|\n\*\*|$)", re.S)
FIG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+\.svg)\)")
TRY_RE = re.compile(r"\*\*Try it:\*\*\s*(.+?)(?=\n\n|\n\*\*|$)", re.S)
TALK_RE = re.compile(r"\*\*Talk together:\*\*\s*(.+?)(?=\n\n|\n\*\*|$)", re.S)


def parse_sections(md: str) -> list[dict]:
    """Split manuscript into figure-associated sections for builds."""
    sections: list[dict] = []
    # Prefer spread-like headings; fall back to ## Unit blocks
    parts = re.split(r"(?=^##\s+)", md, flags=re.M)
    for part in parts:
        if not part.strip():
            continue
        title_m = re.match(r"^##\s+(.+)$", part, re.M)
        title = title_m.group(1).strip() if title_m else "Section"
        # nested ### spreads
        spreads = re.split(r"(?=^###\s+)", part, flags=re.M)
        if len(spreads) > 1:
            for sp in spreads[1:]:
                sm = re.match(r"^###\s+(.+)$", sp, re.M)
                st = sm.group(1).strip() if sm else title
                child = CHILD_RE.search(sp)
                fig = FIG_RE.search(sp)
                try_it = TRY_RE.search(sp)
                talk = TALK_RE.search(sp)
                sections.append(
                    {
                        "title": st,
                        "child": (child.group(1).strip() if child else ""),
                        "fig": (fig.group(1).strip() if fig else ""),
                        "try": (try_it.group(1).strip() if try_it else ""),
                        "talk": (talk.group(1).strip() if talk else ""),
                    }
                )
        else:
            child = CHILD_RE.search(part)
            fig = FIG_RE.search(part)
            if child or fig:
                sections.append(
                    {
                        "title": title,
                        "child": (child.group(1).strip() if child else ""),
                        "fig": (fig.group(1).strip() if fig else ""),
                        "try": "",
                        "talk": "",
                    }
                )
    return sections


def build_html(band_id: str, short: str, ages: str, md: str, sections: list[dict], out: Path) -> None:
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        f"<title>{html.escape(band_id)} full manuscript review preview</title>",
        "<style>",
        "body{font-family:Georgia,serif;max-width:860px;margin:2rem auto;padding:0 1rem;background:#fffef8;color:#111;line-height:1.45;}",
        ".banner{border:3px solid #111;padding:1rem;margin-bottom:1.5rem;background:#f3f3f3;font-family:Helvetica,Arial,sans-serif;}",
        ".stop{position:sticky;top:0;z-index:2;background:#111;color:#fff;padding:.75rem 1rem;font-family:Helvetica,Arial,sans-serif;}",
        "img{max-width:100%;height:auto;border:1px solid #222;}",
        "figure{margin:2rem 0;} figcaption{font-size:.95rem;color:#333;}",
        "a:focus{outline:3px solid #005fcc;outline-offset:2px;}",
        "pre.banner-pre{margin:0;white-space:pre-wrap;}",
        "</style></head><body>",
        "<div class='stop'><a href='#end' style='color:#fff'>Easy exit / stop</a> · Autoplay: OFF · No data collection</div>",
        f"<div class='banner' role='note'><pre class='banner-pre'>{html.escape(BANNER)}</pre></div>",
        f"<h1>{html.escape(band_id)} — Full working manuscript</h1>",
        f"<p>Age guide: {html.escape(ages)}. Caregiver/educator review preview. "
        "Not for unsupervised infant digital product use. Not child-validated. Not publication-ready.</p>",
    ]
    if not sections:
        # Fallback: show manuscript excerpt without claiming child text extraction succeeded
        excerpt = html.escape(md[:4000])
        parts.append(f"<pre style='white-space:pre-wrap'>{excerpt}</pre>")
    for i, sec in enumerate(sections, 1):
        parts.append(f"<figure id='S{i:02d}'>")
        if sec["fig"]:
            # normalize relative path
            src = sec["fig"]
            if src.startswith("figures/"):
                src = "../" + src
            elif not src.startswith("../"):
                src = "../figures/" + Path(src).name
            alt = html.escape((sec["child"] or sec["title"])[:180])
            parts.append(f"<img src='{html.escape(src)}' alt=\"{alt}\"/>")
        caption = f"<strong>{html.escape(sec['title'])}</strong>"
        if sec["child"]:
            caption += "<br/>" + html.escape(sec["child"])
        if sec["talk"]:
            caption += f"<br/><em>Talk together:</em> {html.escape(sec['talk'])}"
        parts.append(f"<figcaption>{caption}</figcaption></figure>")
    parts.append(
        "<section id='end'><h2>End / stop</h2>"
        "<p>Close this preview anytime. No accounts. No tracking. "
        "Adult standards/provenance live outside child-facing blocks.</p></section>"
        "</body></html>"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts), encoding="utf-8")


def build_pdf(band_id: str, short: str, ages: str, sections: list[dict], out: Path) -> None:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas

    out.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out), pagesize=letter)
    w, h = letter

    def banner(cv):
        cv.setFont("Helvetica-Bold", 11)
        y = h - 0.65 * inch
        for line in BANNER.splitlines():
            cv.drawString(0.7 * inch, y, line)
            y -= 13
        return y - 8

    y = banner(c)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.7 * inch, y, f"{band_id} — Full working manuscript")
    y -= 22
    c.setFont("Helvetica", 11)
    c.drawString(0.7 * inch, y, f"Age guide: {ages}")
    y -= 16
    c.drawString(0.7 * inch, y, "Review prototype · not child-validated · not publication-ready")
    c.showPage()

    if not sections:
        y = banner(c)
        c.setFont("Helvetica", 10)
        c.drawString(0.7 * inch, y, "See BOOK_MANUSCRIPT.md — section parser found no spreads.")
        c.showPage()
    for i, sec in enumerate(sections, 1):
        y = banner(c)
        c.setFont("Helvetica-Bold", 13)
        for line in textwrap.wrap(f"S{i:02d} — {sec['title']}", 70):
            c.drawString(0.7 * inch, y, line)
            y -= 16
        # simple geometric stand-in if SVG not embedded
        c.setStrokeColorRGB(0.1, 0.1, 0.1)
        c.setLineWidth(1.5)
        c.rect(0.7 * inch, y - 1.6 * inch, 4.2 * inch, 1.5 * inch)
        c.setFont("Helvetica", 8)
        c.drawString(0.85 * inch, y - 0.85 * inch, (sec.get("fig") or "diagram")[:70])
        y -= 1.85 * inch
        c.setFont("Times-Roman", 11)
        body = sec["child"] or "(See manuscript.)"
        for line in textwrap.wrap(body, 88):
            c.drawString(0.7 * inch, y, line)
            y -= 13
            if y < 1.3 * inch:
                c.showPage()
                y = banner(c)
                c.setFont("Times-Roman", 11)
        if sec.get("try"):
            y -= 4
            c.setFont("Helvetica", 9)
            for line in textwrap.wrap("Try it: " + sec["try"], 95):
                c.drawString(0.7 * inch, y, line)
                y -= 11
                if y < 1.1 * inch:
                    c.showPage()
                    y = banner(c)
                    c.setFont("Helvetica", 9)
        c.setFont("Helvetica", 8)
        c.drawString(0.7 * inch, 0.5 * inch, f"{band_id} · WORKING DRAFT · NOT CHILD-VALIDATED")
        c.showPage()
    c.save()


def build_epub(band_id: str, short: str, md: str, out: Path) -> None:
    """Minimal reflowable EPUB3 candidate for elementary bands."""
    out.parent.mkdir(parents=True, exist_ok=True)
    # Convert markdown lightly to XHTML paragraphs
    body_bits = []
    for line in md.splitlines():
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = html.escape(line.lstrip("# ").strip())
            body_bits.append(f"<h{min(level,3)}>{text}</h{min(level,3)}>")
        elif line.strip():
            body_bits.append(f"<p>{html.escape(line)}</p>")
    content = (
        "<?xml version='1.0' encoding='utf-8'?>"
        "<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en'>"
        "<head><title>"
        + html.escape(band_id)
        + "</title><meta charset='utf-8'/></head><body>"
        + f"<pre>{html.escape(BANNER)}</pre>"
        + "".join(body_bits)
        + "</body></html>"
    )
    container = """<?xml version='1.0' encoding='UTF-8'?>
<container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:container'>
  <rootfiles>
    <rootfile full-path='OEBPS/content.opf' media-type='application/oebps-package+xml'/>
  </rootfiles>
</container>
"""
    opf = f"""<?xml version='1.0' encoding='utf-8'?>
<package xmlns='http://www.idpf.org/2007/opf' version='3.0' unique-identifier='uid'>
  <metadata xmlns:dc='http://purl.org/dc/elements/1.1/'>
    <dc:identifier id='uid'>{band_id}-working-draft</dc:identifier>
    <dc:title>{html.escape(band_id)} Full Working Manuscript</dc:title>
    <dc:language>en</dc:language>
    <meta property='dcterms:modified'>2026-09-05T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id='nav' href='nav.xhtml' media-type='application/xhtml+xml' properties='nav'/>
    <item id='c1' href='chapter.xhtml' media-type='application/xhtml+xml'/>
  </manifest>
  <spine>
    <itemref idref='c1'/>
  </spine>
</package>
"""
    nav = """<?xml version='1.0' encoding='utf-8'?>
<html xmlns='http://www.w3.org/1999/xhtml' xmlns:epub='http://www.idpf.org/2007/ops'>
<head><title>nav</title></head>
<body>
<nav epub:type='toc'><ol><li><a href='chapter.xhtml'>Manuscript</a></li></ol></nav>
</body></html>
"""
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container)
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/nav.xhtml", nav)
        z.writestr("OEBPS/chapter.xhtml", content)


def run_epubcheck(epub: Path) -> tuple[bool, str]:
    jar = shutil.which("epubcheck")
    # Official EPUBCheck java jar may be installed as `epubcheck` script
    if jar:
        proc = subprocess.run([jar, str(epub)], capture_output=True, text=True)
        ok = proc.returncode == 0
        return ok, (proc.stdout + proc.stderr)[-2000:]
    # Try java -jar common locations
    for candidate in (
        ROOT / "tools" / "epubcheck.jar",
        Path("/usr/local/share/java/epubcheck.jar"),
    ):
        if candidate.is_file():
            proc = subprocess.run(
                ["java", "-jar", str(candidate), str(epub)],
                capture_output=True,
                text=True,
            )
            return proc.returncode == 0, (proc.stdout + proc.stderr)[-2000:]
    return False, "EPUBCheck binary not found — recorded as SKIPPED_OFFICIAL_CHECK"


def build_band(band_id: str, short: str, ages: str) -> dict:
    root = BOOKS / band_id
    ms = root / "BOOK_MANUSCRIPT.md"
    if not ms.is_file():
        return {"band": band_id, "ok": False, "error": "missing BOOK_MANUSCRIPT.md"}
    md = ms.read_text(encoding="utf-8")
    sections = parse_sections(md)
    builds = root / "builds"
    html_path = builds / "review-preview.html"
    pdf_path = builds / f"{short}_FULL_MANUSCRIPT.pdf"
    build_html(band_id, short, ages, md, sections, html_path)
    build_pdf(band_id, short, ages, sections, pdf_path)
    result = {
        "band": band_id,
        "ok": True,
        "sections": len(sections),
        "html": str(html_path.relative_to(ROOT)),
        "pdf": str(pdf_path.relative_to(ROOT)),
        "epub": None,
        "epubcheck": None,
    }
    if band_id in EPUB_CANDIDATES:
        epub_path = builds / f"{short}_FULL_MANUSCRIPT.epub"
        build_epub(band_id, short, md, epub_path)
        ok, msg = run_epubcheck(epub_path)
        result["epub"] = str(epub_path.relative_to(ROOT))
        result["epubcheck"] = "PASS" if ok else f"FAIL_OR_SKIP: {msg[:200]}"
        # Keep artifact even if check skipped; validator/CI will treat presence + check status
        (builds / "epubcheck_report.txt").write_text(msg, encoding="utf-8")
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--band", action="append", help="Optional band id filter")
    args = ap.parse_args()
    wanted = set(args.band) if args.band else None
    results = []
    for band_id, short, ages in BANDS:
        if wanted and band_id not in wanted:
            continue
        results.append(build_band(band_id, short, ages))
    for r in results:
        print(r)
    if any(not r.get("ok") for r in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
