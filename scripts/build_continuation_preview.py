#!/usr/bin/env python3
"""Build maintainer-facing continuation development preview (not Gate 3 reader package)."""
from __future__ import annotations

import html
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import load_yaml  # noqa: E402

OUT_DIR = ROOT / "preview" / "continuation"
BANNER = (
    "PREPRODUCTION / DEVELOPMENT — not canonical final prose and not Gate 3 reader evidence."
)


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def write(path: Path, body: str, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)}</title>
<style>
:root {{
  --ink:#1a2332; --muted:#5b6675; --line:#d7dde5; --bg:#f3f6fa; --card:#fff;
  --accent:#0b5fff; --warn:#8a5a00; --ok:#0b6b3a;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0; font-family:"IBM Plex Sans", "Segoe UI", sans-serif; color:var(--ink);
  background:
    radial-gradient(1200px 500px at 10% -10%, #d9e7ff 0%, transparent 55%),
    linear-gradient(180deg, #eef3f8, var(--bg));
}}
header {{
  padding:1.25rem 1.5rem; border-bottom:1px solid var(--line); background:rgba(255,255,255,.86);
  backdrop-filter: blur(8px); position:sticky; top:0;
}}
.banner {{
  display:inline-block; margin:0 0 .6rem; padding:.35rem .65rem; border:1px solid #e0c48a;
  background:#fff6e3; color:var(--warn); font-size:.85rem; font-weight:600;
}}
h1 {{ margin:.2rem 0; font-size:1.45rem; }}
nav a {{ margin-right:1rem; color:var(--accent); text-decoration:none; font-weight:600; }}
main {{ max-width:1100px; margin:0 auto; padding:1.25rem 1.5rem 3rem; }}
table {{ width:100%; border-collapse:collapse; background:var(--card); }}
th, td {{ border:1px solid var(--line); padding:.45rem .55rem; text-align:left; vertical-align:top; font-size:.92rem; }}
th {{ background:#f7f9fc; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:.8rem; }}
.card {{ background:var(--card); border:1px solid var(--line); padding:.9rem 1rem; }}
.muted {{ color:var(--muted); }}
code {{ font-family:"IBM Plex Mono", ui-monospace, monospace; font-size:.86em; }}
ul {{ padding-left:1.1rem; }}
</style>
</head>
<body>
<header>
  <div class="banner">{esc(BANNER)}</div>
  <h1>{esc(title)}</h1>
  <nav>
    <a href="index.html">Overview</a>
    <a href="labs.html">Labs</a>
    <a href="figures.html">Figures</a>
    <a href="sources.html">Sources</a>
    <a href="full31.html">Full31 registry</a>
  </nav>
</header>
<main>
{body}
</main>
</body>
</html>
"""
    path.write_text(doc, encoding="utf-8")


def build() -> int:
    labs = load_yaml(ROOT / "labs/lab_registry.yaml").get("labs") or []
    figs_doc = load_yaml(ROOT / "figures/preproduction/ce_figure_registry.yaml")
    figs = figs_doc.get("figures") or []
    sources = load_yaml(ROOT / "publication/preproduction/CANDIDATE_SOURCE_INDEX.yaml")
    full31 = load_yaml(ROOT / "publication/full31/CHAPTER_PRODUCTION_REGISTRY.yaml")

    counts = full31.get("counts") or {}
    overview = f"""
<p class="muted">Maintainer development dashboard for the full31 continuation wave. This preview is intentionally separate from the CH02 Gate 3 reader package.</p>
<p><strong>WORKING FULL-MANUSCRIPT DRAFT</strong> — Human reader validation pending. Technical/editorial revision pending. Not publication-ready.</p>
<div class="grid">
  <div class="card"><strong>Labs</strong><div>{len(labs)} registered</div></div>
  <div class="card"><strong>CE figures</strong><div>{len(figs)} planned / tracked</div></div>
  <div class="card"><strong>Unique sources</strong><div>{sources.get('unique_source_records', 'n/a')}</div></div>
  <div class="card"><strong>Full31 chapters</strong><div>{len(full31.get('chapters') or [])}</div></div>
</div>
<p style="margin-top:1.2rem"><strong>Gate posture:</strong> <code>{esc(full31.get('gate_posture'))}</code></p>
<p><strong>Human validation:</strong> <code>DEFERRED_UNTIL_FULL_MANUSCRIPT_DRAFT</code></p>
<p><strong>Accepted main:</strong> <code>{esc(full31.get('accepted_main_sha'))}</code></p>
<h2>Normalized progress dimensions</h2>
<pre>architecture:              {esc(counts.get('architecture_registered', 0))}/31
packet:                    {esc(counts.get('minimum_packet_coverage', 0))}/31
substantive_preproduction: {esc(counts.get('substantive_preproduction_complete', 0))}/31 complete ({esc(counts.get('substantive_preproduction_started', 0))}/31 started)
working_draft:             {esc(counts.get('working_draft', counts.get('canonical_full_drafts', 0)))}/31
technical_review:          {esc(counts.get('technical_review', 0))}/31
human_validation:          {esc(counts.get('human_validated', 0))}/31
publication_readiness:     {esc(counts.get('publication_ready', 0))}/31</pre>
<p class="muted">See <code>publication/full31/PROGRESS_DIMENSIONS.md</code> and <code>make full31-draft-check</code>.</p>
"""
    write(OUT_DIR / "index.html", overview, "Continuation development preview")

    lab_rows = "\n".join(
        f"<tr><td><code>{esc(l.get('lab_id'))}</code></td><td>{esc(l.get('title'))}</td>"
        f"<td>{esc(l.get('chapter'))}</td><td>{esc(l.get('status'))}</td>"
        f"<td><code>{esc(l.get('path'))}</code></td></tr>"
        for l in labs
    )
    write(
        OUT_DIR / "labs.html",
        f"<p class='muted'>Runnable CE lab packages + Wave 1 LAB-TAP-001.</p>"
        f"<table><thead><tr><th>ID</th><th>Title</th><th>Chapter</th><th>Status</th><th>Path</th></tr></thead>"
        f"<tbody>{lab_rows}</tbody></table>",
        "Labs development preview",
    )

    fig_rows = "\n".join(
        f"<tr><td><code>{esc(f.get('figure_id'))}</code></td><td>{esc(f.get('title'))}</td>"
        f"<td>{esc(f.get('truth_classification'))}</td><td>{esc(f.get('production_status'))}</td>"
        f"<td>{esc(f.get('block_reason') or '')}</td></tr>"
        for f in figs
    )
    write(
        OUT_DIR / "figures.html",
        f"<p class='muted'>Draft CE figures. Measured claims stay blocked without evidence.</p>"
        f"<table><thead><tr><th>ID</th><th>Title</th><th>Truth</th><th>Status</th><th>Block</th></tr></thead>"
        f"<tbody>{fig_rows}</tbody></table>",
        "Figures development preview",
    )

    ver = sources.get("verification_counts") or {}
    ver_rows = "\n".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in ver.items())
    wcag = sources.get("wcag_resolution") or {}
    write(
        OUT_DIR / "sources.html",
        f"<p class='muted'>Candidate source verification dashboard (Concept Edition).</p>"
        f"<p>Unique source records: <strong>{esc(sources.get('unique_source_records'))}</strong></p>"
        f"<h2>Verification counts</h2><table><thead><tr><th>Status</th><th>Count</th></tr></thead>"
        f"<tbody>{ver_rows}</tbody></table>"
        f"<h2>WCAG resolution</h2><pre>{esc(wcag)}</pre>",
        "Sources development preview",
    )

    ch_rows = "\n".join(
        f"<tr><td>{esc(c.get('chapter_number'))}</td><td><code>{esc(c.get('chapter_id'))}</code></td>"
        f"<td>{esc(c.get('title'))}</td><td>{esc(c.get('part'))}</td>"
        f"<td>{esc(c.get('current_state'))}</td><td>{esc(c.get('canonical_prose_state'))}</td>"
        f"<td>{esc(c.get('next_automatable_action'))}</td></tr>"
        for c in full31.get("chapters") or []
    )
    write(
        OUT_DIR / "full31.html",
        f"<p class='muted'>Unified 31-chapter production registry.</p>"
        f"<table><thead><tr><th>#</th><th>ID</th><th>Title</th><th>Part</th>"
        f"<th>current_state</th><th>canonical_prose</th><th>next_automatable_action</th></tr></thead>"
        f"<tbody>{ch_rows}</tbody></table>",
        "Full31 registry development preview",
    )

    print(f"continuation preview written under {OUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
