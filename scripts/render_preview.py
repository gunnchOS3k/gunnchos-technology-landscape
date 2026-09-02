#!/usr/bin/env python3
"""Fallback HTML preview when Quarto is unavailable."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "book/chapters/ch02/chapter.md"
out_dir = ROOT / "preview"
out_dir.mkdir(parents=True, exist_ok=True)
text = src.read_text(encoding="utf-8")
# strip YAML front matter
text = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)

def convert(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            if not in_code:
                out.append("<pre><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        if line.startswith("# "):
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{html.escape(line[2:])}</blockquote>")
        elif line.strip() == "":
            out.append("")
        else:
            out.append(f"<p>{html.escape(line)}</p>")
    return "\n".join(out)

html_doc = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\"/>
<title>Chapter 2 Preview — The Technology Landscape</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 48rem; margin: 2rem auto; line-height: 1.5; padding: 0 1rem; }}
code, pre {{ font-family: ui-monospace, monospace; }}
</style>
</head>
<body>
<p><strong>Fallback preview</strong> (Quarto not detected). Semantic Markdown features are limited in this mode.</p>
{convert(text)}
</body>
</html>
"""
(out_dir / "ch02.html").write_text(html_doc, encoding="utf-8")
print(f"Wrote {out_dir / 'ch02.html'}")
