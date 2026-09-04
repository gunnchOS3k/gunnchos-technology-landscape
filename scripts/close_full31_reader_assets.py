#!/usr/bin/env python3
"""Generate missing conceptual Full31 SVGs, a11y sidecars, registry rows,
and clean reader-facing production meta-text.

Does not invent measurements. FIG-CE3-009 stays blocked (no SVG).
Does not modify publication/gates/gate-3/.
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# fid -> (title, truth_class, template_kind, node_labels)
# template_kind: sequence | map | compare | ladder | boundary
FIGURE_SPECS: dict[str, tuple[str, str, str, list[str]]] = {
    "FIG-CH11-001": ("Boot path sequence", "conceptual", "sequence",
                     ["Power/reset", "Firmware", "Bootloader", "Kernel", "Userspace"]),
    "FIG-CH11-002": ("Root-of-trust stages", "conceptual", "ladder",
                     ["Hardware root", "Verified firmware", "Bootloader policy", "OS trust", "App trust"]),
    "FIG-CH11-003": ("AuthN vs AuthZ at boot", "conceptual", "compare",
                     ["Authentication", "Authorization", "Identity proved", "Permission granted"]),
    "FIG-CH11-004": ("Update and recovery boundary", "conceptual", "boundary",
                     ["Trusted update", "Interrupted update", "Recovery path", "Unsafe rollback"]),
    "FIG-CH13-001": ("Data lifecycle arc", "conceptual", "sequence",
                     ["Create", "Store", "Use", "Share", "Delete/GC"]),
    "FIG-CH13-002": ("Durability stack", "conceptual", "ladder",
                     ["App buffer", "Filesystem", "Device cache", "Persistent media"]),
    "FIG-CH13-003": ("Save click vs durability", "illustrative", "compare",
                     ["UI Save click", "Flush/fsync later", "Visible confirm", "Durable point"]),
    "FIG-CH13-004": ("Files vs databases", "conceptual", "compare",
                     ["Named bytes (files)", "Structured store (DB)", "Paths/names", "Queries/indexes"]),
    "FIG-CH14-001": ("App stack map", "conceptual", "ladder",
                     ["UI", "App logic", "Runtime", "Libraries", "OS services"]),
    "FIG-CH14-002": ("Feature after chrome path", "conceptual", "sequence",
                     ["Chrome ready", "Feature request", "Runtime call", "Result", "UI update"]),
    "FIG-CH14-003": ("Local vs remote API domains", "illustrative", "compare",
                     ["Local API", "Remote API", "Device failure", "Network/service failure"]),
    "FIG-CH17-001": ("Wi-Fi vs cellular on-ramps", "conceptual", "compare",
                     ["Device", "Wi-Fi AP path", "Cellular path", "Internet beyond"]),
    "FIG-CH17-002": ("Cellular generations timeline", "illustrative", "sequence",
                     ["2G/3G era", "4G", "5G deployed", "6G roadmap only"]),
    "FIG-CH17-003": ("Indoor Wi-Fi to outdoor handoff", "conceptual", "sequence",
                     ["Indoor Wi-Fi", "Approach exit", "Wi-Fi weak", "Cellular attach", "Continue task"]),
    "FIG-CH18-001": ("Radio path conditions", "conceptual", "map",
                     ["Device", "Body/obstacles", "Antennas", "Shared spectrum", "Decode"]),
    "FIG-CH18-002": ("Beam and path geometry", "conceptual", "map",
                     ["Transmitter", "Beam/path", "Reflect/block", "Receiver"]),
    "FIG-CH18-003": ("MIMO teaching metaphor", "conceptual", "compare",
                     ["Single stream", "Multiple streams", "Spatial paths", "Combine at receiver"]),
    "FIG-CH18-004": ("Quartet RF PHYSICAL_PENDING overlay", "project_specific", "boundary",
                     ["Teaching RF map", "Measured RF", "PHYSICAL_PENDING", "No invented gain"]),
    "FIG-CH19-001": ("NTN continuity map", "conceptual", "map",
                     ["Human task", "Device", "Terrestrial", "NTN path", "Usable result"]),
    "FIG-CH19-002": ("Continuity vs icon status", "conceptual", "compare",
                     ["Icon lit", "Task usable", "Status green", "Continuity held"]),
    "FIG-CH19-003": ("Illustrative delay families", "illustrative", "compare",
                     ["Terrestrial class", "NTN class", "Illustrative only", "Not measured"]),
    "FIG-CH20-001": ("Stability Contract concurrent conditions", "conceptual", "map",
                     ["Human experience", "Compute", "Storage", "Network", "Power/thermal"]),
    "FIG-CH20-002": ("Latency vs reliability vs throughput", "conceptual", "compare",
                     ["Latency symptom", "Reliability symptom", "Throughput symptom", "One probe ≠ all"]),
    "FIG-CH20-003": ("Evidence ladder for QoE", "conceptual", "ladder",
                     ["Illustrative", "Observation", "Instrumentation", "Correlated signals", "Controlled compare"]),
    "FIG-CH20-004": ("Status vs usable experience", "conceptual", "compare",
                     ["Connected icon", "Usable send", "Green probe", "Human-finished task"]),
    "FIG-CH21-001": ("Data to model to inference", "conceptual", "sequence",
                     ["Data", "Model", "Inference", "Output", "Human review"]),
    "FIG-CH21-002": ("Local vs remote AI placement", "conceptual", "compare",
                     ["On-device", "Edge box", "Remote service", "Privacy/delay trade"]),
    "FIG-CH21-003": ("Fluency vs correctness vs evaluation evidence", "conceptual", "compare",
                     ["Fluency", "Correctness", "Evaluation evidence"]),
    "FIG-CH22-001": ("Sense to edge feedback", "conceptual", "sequence",
                     ["Sense", "Feature", "Edge inference", "Haptic/UI", "Human notice"]),
    "FIG-CH22-002": ("Illustrative latency budget bands", "illustrative", "ladder",
                     ["Sense", "Compute", "Actuate", "Illustrative bands only"]),
    "FIG-CH22-003": ("Wearables PHYSICAL_PENDING badge", "project_specific", "boundary",
                     ["Edge IO Wearables", "Embodied sensing", "PHYSICAL_PENDING", "No shipping specs"]),
    "FIG-CH24-001": ("Privacy lifecycle wheel", "conceptual", "sequence",
                     ["Collect", "Use", "Retain", "Share", "Delete/redact"]),
    "FIG-CH24-002": ("Accessible vs blocked recovery", "conceptual", "compare",
                     ["Accessible recovery", "Blocked recovery", "Auth succeeded", "Task finished"]),
    "FIG-CH24-003": ("Ethics and inclusion ladder", "conceptual", "ladder",
                     ["Notice", "Choice", "Access path", "Accountability", "Redress"]),
    "FIG-CH25-001": ("Same task divergent completion", "conceptual", "compare",
                     ["Task A privileged", "Task A constrained", "Completed", "Blocked/excluded"]),
    "FIG-CH25-002": ("Equity evidence hierarchy", "conceptual", "ladder",
                     ["Anecdote", "Structured observation", "Measured access", "Population claim"]),
    "FIG-CH25-003": ("Exclusion mechanism cards", "conceptual", "map",
                     ["Device cost", "Bandwidth", "Accessibility", "Identity/docs", "Support"]),
    "FIG-CH26-001": ("Edit to review sequence", "conceptual", "sequence",
                     ["Edit", "Status", "Diff", "Commit", "Review"]),
    "FIG-CH26-002": ("Working tree vs history", "conceptual", "compare",
                     ["Working tree", "Committed history", "Unsaved risk", "Reviewable past"]),
    "FIG-CH26-003": ("Secrets must not enter the repository", "conceptual", "boundary",
                     ["Working tree", "REFUSE", "Committed history"]),
    "FIG-CH27-001": ("Evidence hierarchy ladder", "conceptual", "ladder",
                     ["Illustrative", "Commodity observe", "Instrumentation", "Multi-signal", "Controlled compare"]),
    "FIG-CH27-002": ("Test pass vs usable experience", "conceptual", "compare",
                     ["Suite green", "Usable experience", "Unit pass", "Human-finished task"]),
    "FIG-CH27-003": ("Observation to inference gate", "conceptual", "sequence",
                     ["Signals in", "Observation log", "Inference label", "Claim boundary"]),
    "FIG-CH28-001": ("Twin story vs measured world", "conceptual", "compare",
                     ["Simulation/twin", "Measured world", "Declared fidelity", "Outside bounds"]),
    "FIG-CH28-002": ("Reproducibility checklist path", "conceptual", "sequence",
                     ["Inputs pinned", "Code/version", "Environment", "Outputs", "Audit trail"]),
    "FIG-CH28-003": ("Validity bounds annulus", "conceptual", "boundary",
                     ["Trusted inside ring", "Declared limits", "Unlabeled outside", "Do not overclaim"]),
    "FIG-CH29-001": ("Complete product ecosystem map", "conceptual", "map",
                     ["Human experience", "App/code", "Local resources", "Network", "Society"]),
    "FIG-CH29-002": ("Secure/include inside design gates", "conceptual", "sequence",
                     ["Need", "Design gate", "Secure/include", "Ship candidate", "Evidence"]),
    "FIG-CH29-003": ("One-pager evidence fields", "conceptual", "ladder",
                     ["Experience", "System boundary", "Risks", "Evidence", "Limitations"]),
    "FIG-CH30-001": ("Role to artifact to review", "conceptual", "sequence",
                     ["Role family", "Artifact", "Review criteria", "Non-guarantee boundary"]),
    "FIG-CH30-002": ("Portfolio checklist fields", "conceptual", "ladder",
                     ["Index entry", "Claim type", "Evidence link", "Limitations", "Teach-back"]),
    "FIG-CH30-003": ("Learning proof vs employment", "conceptual", "boundary",
                     ["Learning proof", "Portfolio", "Employer decision", "No promise"]),
    "FIG-CH31-001": ("Capstone concurrent-condition hub", "conceptual", "map",
                     ["Human experience", "System", "Network", "Security/privacy", "Society"]),
    "FIG-CH31-002": ("EMIT cycle with evidence gates", "conceptual", "sequence",
                     ["Explain", "Measure", "Improve", "Teach", "Evidence gate"]),
    "FIG-CH31-003": ("Fixture vs human-evidence firewall", "conceptual", "boundary",
                     ["Fixture/illustrative", "Teaching aid", "Human evidence", "Gate 3 pending"]),
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def wrap_lines(text: str, width: int = 28) -> list[str]:
    return textwrap.wrap(text, width=width) or [text]


def svg_for(fid: str, title: str, truth: str, kind: str, nodes: list[str]) -> str:
    tid = fid.lower()
    evidence = (
        "Conceptual/illustrative teaching figure; not measured data. "
        "No invented physical measurements."
    )
    if truth == "project_specific":
        evidence = (
            "Project-specific teaching overlay. Physical Device Quartet attributes "
            "remain PHYSICAL_PENDING unless real evidence exists."
        )
    desc = (
        f"{title}. Truth class: {truth}. Nodes: {', '.join(nodes)}. "
        f"{evidence}"
    )
    # layout boxes
    boxes = []
    if kind == "sequence":
        n = len(nodes)
        w, h, gap = 150, 64, 18
        total = n * w + (n - 1) * gap
        x0 = max(24, (1000 - total) // 2)
        y = 150
        for i, label in enumerate(nodes):
            x = x0 + i * (w + gap)
            lines = wrap_lines(label, 16)
            ty = y + 28 - 6 * (len(lines) - 1)
            text_el = "".join(
                f'<text x="{x+w/2}" y="{ty + j*14}" text-anchor="middle" '
                f'font-family="Helvetica,Arial,sans-serif" font-size="12" '
                f'font-weight="bold" fill="#111111">{esc(line)}</text>'
                for j, line in enumerate(lines)
            )
            boxes.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" '
                f'stroke="#111111" stroke-width="2"/>{text_el}'
            )
            if i < n - 1:
                boxes.append(
                    f'<line x1="{x+w}" y1="{y+h/2}" x2="{x+w+gap}" y2="{y+h/2}" '
                    f'stroke="#111111" stroke-width="2" marker-end="url(#arr-{tid})"/>'
                )
    elif kind == "ladder":
        n = len(nodes)
        w, h, gap = 520, 44, 12
        x = 240
        y0 = 90
        for i, label in enumerate(nodes):
            y = y0 + i * (h + gap)
            rank = n - i
            boxes.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ffffff" '
                f'stroke="#111111" stroke-width="2"/>'
                f'<text x="{x+16}" y="{y+28}" font-family="Helvetica,Arial,sans-serif" '
                f'font-size="13" font-weight="bold" fill="#111111">{rank}. {esc(label)}</text>'
            )
            if i < n - 1:
                boxes.append(
                    f'<line x1="{x+w/2}" y1="{y+h}" x2="{x+w/2}" y2="{y+h+gap}" '
                    f'stroke="#111111" stroke-width="2"/>'
                )
    elif kind == "compare":
        left = nodes[: len(nodes) // 2] or nodes[:1]
        right = nodes[len(nodes) // 2 :] or nodes[1:]
        boxes.append(
            '<rect x="40" y="100" width="430" height="220" fill="#f7f7f7" '
            'stroke="#111111" stroke-width="2"/>'
            '<text x="255" y="130" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
            'font-size="14" font-weight="bold" fill="#111111">Side A</text>'
        )
        boxes.append(
            '<rect x="530" y="100" width="430" height="220" fill="#ffffff" '
            'stroke="#111111" stroke-width="2"/>'
            '<text x="745" y="130" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
            'font-size="14" font-weight="bold" fill="#111111">Side B</text>'
        )
        for i, label in enumerate(left[:4]):
            boxes.append(
                f'<text x="255" y="{170 + i*28}" text-anchor="middle" '
                f'font-family="Helvetica,Arial,sans-serif" font-size="13" fill="#111111">'
                f'{esc(label)}</text>'
            )
        for i, label in enumerate(right[:4]):
            boxes.append(
                f'<text x="745" y="{170 + i*28}" text-anchor="middle" '
                f'font-family="Helvetica,Arial,sans-serif" font-size="13" fill="#111111">'
                f'{esc(label)}</text>'
            )
        boxes.append(
            '<text x="500" y="360" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
            'font-size="11" fill="#444444">Labels encode meaning; color is not required</text>'
        )
    elif kind == "boundary":
        boxes.append(
            '<circle cx="500" cy="210" r="120" fill="#ffffff" stroke="#111111" stroke-width="3"/>'
            '<circle cx="500" cy="210" r="70" fill="#f5f5f5" stroke="#1F4B7A" stroke-width="2" '
            'stroke-dasharray="6 4"/>'
        )
        inner = nodes[0] if nodes else "Inside"
        outer = nodes[1] if len(nodes) > 1 else "Outside"
        note = nodes[2] if len(nodes) > 2 else ""
        note2 = nodes[3] if len(nodes) > 3 else ""
        boxes.append(
            f'<text x="500" y="205" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="13" font-weight="bold" fill="#111111">{esc(inner)}</text>'
            f'<text x="500" y="225" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="11" fill="#1F4B7A">{esc(outer)}</text>'
        )
        if note:
            boxes.append(
                f'<text x="500" y="360" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" '
                f'font-size="12" fill="#333333">{esc(note)}{" — " + esc(note2) if note2 else ""}</text>'
            )
    else:  # map
        positions = [
            (80, 160), (250, 90), (250, 230), (450, 160), (650, 160), (820, 160)
        ]
        for i, label in enumerate(nodes[:6]):
            x, y = positions[i]
            lines = wrap_lines(label, 14)
            ty = y + 30 - 6 * (len(lines) - 1)
            text_el = "".join(
                f'<text x="{x+65}" y="{ty + j*13}" text-anchor="middle" '
                f'font-family="Helvetica,Arial,sans-serif" font-size="11" '
                f'font-weight="bold" fill="#111111">{esc(line)}</text>'
                for j, line in enumerate(lines)
            )
            boxes.append(
                f'<rect x="{x}" y="{y}" width="130" height="60" fill="#ffffff" '
                f'stroke="#111111" stroke-width="2"/>{text_el}'
            )
        # simple connectors
        boxes.append(
            '<path d="M210,190 L250,150 M210,190 L250,250 M380,190 L450,190 '
            'M580,190 L650,190 M780,190 L820,190" fill="none" stroke="#111111" stroke-width="2"/>'
        )

    body = "\n  ".join(boxes)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="420" viewBox="0 0 1000 420" role="img"
     aria-labelledby="{tid}-title {tid}-desc"
     data-figure-id="{fid}">
  <title id="{tid}-title">{esc(title)}</title>
  <desc id="{tid}-desc">{esc(desc)}</desc>
  <defs>
    <marker id="arr-{tid}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#111111"/>
    </marker>
  </defs>
  <rect width="1000" height="420" fill="#ffffff"/>
  <rect x="1" y="1" width="998" height="418" fill="none" stroke="#222222" stroke-width="2"/>
  <text x="24" y="32" font-family="Helvetica,Arial,sans-serif" font-size="16" font-weight="bold" fill="#111111">{esc(title)}</text>
  <text x="24" y="52" font-family="Helvetica,Arial,sans-serif" font-size="11" fill="#444444">{fid} · truth: {truth} · educational architecture (not a product measurement)</text>
  {body}
  <text x="24" y="400" font-family="Helvetica,Arial,sans-serif" font-size="10" fill="#555555">{esc(evidence)}</text>
</svg>
'''


def a11y_yaml(fid: str, title: str, truth: str, nodes: list[str]) -> str:
    m = re.match(r"FIG-CH(\d{2})-(\d{3})", fid)
    ch = m.group(1) if m else "00"
    src = f"figures/full31/ch{ch}/{fid.lower()}.svg"
    status = "conceptual" if truth == "project_specific" else truth
    ro = "\n".join(f"- {n}" for n in nodes)
    te = (
        f"{title}. Nodes in reading order: {'; '.join(nodes)}. "
        f"Truth: {truth}. Educational architecture; no invented measurements."
    )
    return (
        f"figure_id: {fid}\n"
        f"title: \"{title}\"\n"
        f"caption: \"{title}. Truth classification: {truth}. Color is not the sole encoding.\"\n"
        f"alt_text: \"{title}. Reading order: {'; '.join(nodes)}.\"\n"
        f"text_equivalent: |\n"
        f"  {te}\n"
        f"reading_order:\n"
        f"{ro}\n"
        f"source: {src}\n"
        f"evidence_note: \"Conceptual/illustrative teaching asset; no invented measurements.\"\n"
        f"truth_classification: {truth}\n"
        f"qualification: null\n"
        f"status: {status}\n"
        f"production_status: implemented\n"
        f"color_independent_encoding: \"Shape + label + solid vs dashed stroke; do not rely on color alone.\"\n"
        f"reviewer: pending-human-visual-review\n"
        f"version: 0.1.0\n"
    )


def clean_chapter_text(text: str) -> str:
    # Remove production parentheticals after FIG refs
    text = re.sub(
        r"(\*\*FIG-[A-Z0-9-]+\*\*)\s*\((?:planned|conceptual|illustrative|project-specific)[^)]*\)",
        r"\1",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(\*\*FIG-[A-Z0-9-]+\*\*)\s*\([^)]*(?:planned|to be added|future figure|embed)[^)]*\)",
        r"\1",
        text,
        flags=re.I,
    )
    # Integrator / agent merge notes in glossary sections
    text = re.sub(
        r"(?m)^.*\bintegrator merge\b.*\n?",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(?m)^.*\bCandidate terms for integrator\b.*\n?",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(?m)^.*\bChapter-local candidates \(integrator merge required[^\n]*\n?",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"for integrator merge; do not treat the table below as an automatic glossary write\.?",
        "listed for linking in the living glossary.",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"Candidate definitions also appear in the chapter packet’s `GLOSSARY_CANDIDATES\.yaml` "
        r"for integrator merge; do not treat the table below as an automatic glossary write\.?",
        "Candidate definitions also appear in the chapter packet glossary candidates file.",
        text,
        flags=re.I,
    )
    # FIG-CE3-009: remove as live figure ref; keep blocked honesty without dangling asset
    text = re.sub(
        r"\*\*FIG-CE3-009\*\*",
        "a measured CMS monitor plate (still blocked pending qualifying evidence)",
        text,
    )
    text = re.sub(r"\bFIG-CE3-009\b", "the blocked CMS measured plate", text)
    # Soften leftover planned language adjacent to figures
    text = re.sub(r"\bplanned conceptual plates?\b", "conceptual plates", text, flags=re.I)
    text = re.sub(
        r"(?m)^## Figure references \(planned conceptual plates; accessibility metadata\)\s*$",
        "## Figure references",
        text,
    )
    return text


def upsert_registry(entries: list[dict]) -> None:
    reg_path = ROOT / "figures/figure_registry.yaml"
    existing = reg_path.read_text(encoding="utf-8") if reg_path.exists() else "figures:\n"
    for e in entries:
        fid = e["figure_id"]
        if f"figure_id: {fid}" in existing or f"id: {fid}" in existing:
            continue
        block = (
            f"\n  - figure_id: {fid}\n"
            f"    id: {fid}\n"
            f"    title: \"{e['title']}\"\n"
            f"    path: {e['path']}\n"
            f"    accessibility: {e['accessibility']}\n"
            f"    status: {e['truth']}\n"
            f"    truth_classification: {e['truth']}\n"
            f"    chapter: {e['chapter']}\n"
            f"    evidence_note: \"Conceptual/illustrative teaching asset; no invented measurements.\"\n"
        )
        existing += block
    reg_path.write_text(existing, encoding="utf-8")


def main() -> None:
    created = []
    for fid, (title, truth, kind, nodes) in FIGURE_SPECS.items():
        m = re.match(r"FIG-CH(\d{2})-(\d{3})", fid)
        if not m:
            raise ValueError(fid)
        ch = f"ch{m.group(1)}"
        out_dir = ROOT / "figures" / "full31" / ch
        out_dir.mkdir(parents=True, exist_ok=True)
        svg_name = f"{fid.lower()}.svg"
        svg_path = out_dir / svg_name
        a11y_path = ROOT / "figures" / "accessibility" / f"{fid.lower()}.yaml"
        a11y_path.parent.mkdir(parents=True, exist_ok=True)
        svg_path.write_text(svg_for(fid, title, truth, kind, nodes), encoding="utf-8")
        a11y_path.write_text(a11y_yaml(fid, title, truth, nodes), encoding="utf-8")
        created.append(
            {
                "figure_id": fid,
                "title": title,
                "path": str(svg_path.relative_to(ROOT)),
                "accessibility": str(a11y_path.relative_to(ROOT)),
                "truth": truth,
                "chapter": ch.upper(),
            }
        )
    upsert_registry(created)

    # Clean chapters
    for chapter in sorted((ROOT / "book/chapters").glob("ch*/chapter.md")):
        # Do not broadly rewrite CH02; only mechanical CE3 / meta if any
        original = chapter.read_text(encoding="utf-8")
        cleaned = clean_chapter_text(original)
        if chapter.parent.name == "ch02":
            # Only allow FIG-CE3-009 / meta mechanical cleanup on CH02 if present
            if cleaned != original:
                # Revert any non-CE3 changes for CH02 by checking diff size heuristically
                # Prefer: apply only CE3 substitution on CH02
                cleaned = re.sub(
                    r"\*\*FIG-CE3-009\*\*",
                    "a measured CMS monitor plate (still blocked pending qualifying evidence)",
                    original,
                )
                cleaned = re.sub(r"\bFIG-CE3-009\b", "the blocked CMS measured plate", cleaned)
        if cleaned != original:
            chapter.write_text(cleaned, encoding="utf-8")

    print(f"created {len(created)} figures")
    for e in created:
        print(e["figure_id"], "->", e["path"])


if __name__ == "__main__":
    main()
