#!/usr/bin/env python3
"""Deterministic Full31 continuity / duplication audit aid.

Produces:
  publication/full31/quality/CONTINUITY_LEDGER.yaml
  publication/full31/quality/CONTINUITY_REPORT.md
  publication/full31/quality/CHAPTER_IDENTITY_MATRIX.yaml
  publication/full31/quality/CHAPTER_IDENTITY_MATRIX.md

This is an audit aid, not an auto-rewrite engine. Human judgment decides
whether flagged duplication is harmful or deliberate reinforcement.
"""
from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "book/chapters"
BRIEFS = ROOT / "publication/full31/chapters"
OUT = ROOT / "publication/full31/quality"
sys.path.insert(0, str(ROOT / "scripts"))
from yaml_util import dump_yaml, load_yaml  # noqa: E402

# ---------------------------------------------------------------------------
# Whitelist: deliberate repeated constructs (not auto-flagged as harmful)
# ---------------------------------------------------------------------------
WHITELIST_PATTERNS = [
    r"stability contract",
    r"user experience exists only while multiple hidden technical conditions",
    r"a device can remain .{0,40}powered on and connected",
    r"connected indicators can remain green while the human experience",
    r"no passwords, tokens, private messages",
    r"no rooting, jailbreaking",
    r"gate_3_in_progress",
    r"reader_evidence_pending",
    r"human validation pending",
    r"not publication-ready",
    r"status:\s*`?draft`?",
    r"status:\s*`?working_draft`?",
    r"deeper entries.{0,40}analogies labeled",
    r"terms introduced or relied on as formal vocabulary",
    r"candidate terms introduced or reinforced here",
    r"walk the layers in ordinary language",
    r"component cards answer:",
    r"those expectations are not decorations",
    r"figure references \(planned embeds",
    r"figure references \(embedded above",
    r"claim footnotes used in this chapter",
    r"for each object: plain language, analogy, technical function",
    r"all figures below are \*\*conceptual\*\*",
    r"device quartet",
    r"wcag",
    r"representative educational architecture",
    r"commodity observations you collect",
    r"fixtures teach concepts; they are not claims",
]

SEVERITY = ("BLOCKER", "MAJOR", "MODERATE", "MINOR", "EDITORIAL")


@dataclass
class Finding:
    finding_id: str
    kind: str
    severity: str
    chapters: list[str]
    summary: str
    evidence: str
    disposition: str = "OPEN"  # OPEN | INTENTIONAL_RETAIN | FIX_CANDIDATE | FIXED
    notes: str = ""
    similarity: float | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "id": self.finding_id,
            "kind": self.kind,
            "severity": self.severity,
            "chapters": self.chapters,
            "summary": self.summary,
            "evidence": self.evidence,
            "disposition": self.disposition,
        }
        if self.similarity is not None:
            d["similarity"] = round(self.similarity, 3)
        if self.notes:
            d["notes"] = self.notes
        return d


@dataclass
class Paragraph:
    chapter: str
    index: int
    raw: str
    norm: str
    section: str
    shingles: set[str] = field(default_factory=set)


def normalize(text: str) -> str:
    t = re.sub(r"```.*?```", " ", text, flags=re.S)
    t = re.sub(r"`[^`]+`", " TERM ", t)
    t = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"@[\w.:-]+", " ", t)
    t = re.sub(r"\{#[^}]+\}", " ", t)
    t = re.sub(r"[#*_>\[\](){}|]", " ", t)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def is_whitelisted(norm: str) -> bool:
    return any(re.search(p, norm) for p in WHITELIST_PATTERNS)


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2]
    return text


def section_for_offset(text: str, offset: int) -> str:
    headers = list(re.finditer(r"^##\s+(.+)$", text, re.M))
    current = "(preamble)"
    for h in headers:
        if h.start() <= offset:
            current = re.sub(r"\{#.*\}", "", h.group(1)).strip()
        else:
            break
    return current[:80]


def extract_paragraphs(chapter_id: str, text: str) -> list[Paragraph]:
    body = strip_frontmatter(text)
    paras: list[Paragraph] = []
    for m in re.finditer(r"(?:\A|\n\n)(.+?)(?=\n\n|\Z)", body, re.S):
        raw = m.group(1).strip()
        if not raw:
            continue
        if raw.startswith("![") or (raw.startswith("#") and "\n" not in raw):
            continue
        if raw.startswith("|") and raw.count("|") >= 2:
            continue
        norm = normalize(raw)
        if len(norm) < 100:
            continue
        toks = norm.split()
        sh = (
            {" ".join(toks[i : i + 5]) for i in range(max(0, len(toks) - 4))}
            if len(toks) >= 5
            else {norm}
        )
        paras.append(
            Paragraph(
                chapter=chapter_id,
                index=len(paras),
                raw=raw,
                norm=norm,
                section=section_for_offset(body, m.start()),
                shingles=sh,
            )
        )
    return paras


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def chapter_ids() -> list[str]:
    return [f"ch{i:02d}" for i in range(1, 32)]


def load_chapter_text(cid: str) -> str:
    return (CHAPTERS / cid / "chapter.md").read_text(encoding="utf-8")


def grab_brief_field(brief: str, label: str) -> str:
    m = re.search(
        rf"##\s+{re.escape(label)}\s*\n+(.*?)(?=\n##\s+|\Z)",
        brief,
        re.S | re.I,
    )
    if not m:
        return ""
    lines = [ln.strip() for ln in m.group(1).strip().splitlines() if ln.strip()]
    # skip table-only blocks
    lines = [ln for ln in lines if not ln.startswith("|")]
    return " ".join(lines)[:400]


def extract_moment(text: str) -> str:
    body = strip_frontmatter(text)
    m = re.search(
        r"##\s+1\.\s+The moment.*?\n\n(.+?)(?:\n\n)",
        body,
        re.S | re.I,
    )
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()[:320]


def extract_question(text: str, meta: dict[str, Any]) -> str:
    hq = meta.get("human_question") or []
    if isinstance(hq, list) and hq:
        return "; ".join(str(x) for x in hq)
    if isinstance(hq, str) and hq:
        return hq
    body = strip_frontmatter(text)
    m = re.search(r"^>\s*(.+)$", body, re.M)
    return m.group(1).strip() if m else ""


def build_identity_matrix(
    texts: dict[str, str], metas: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cid in chapter_ids():
        meta = metas[cid]
        brief_path = BRIEFS / cid / "CHAPTER_BRIEF.md"
        brief = brief_path.read_text(encoding="utf-8") if brief_path.exists() else ""
        moment = extract_moment(texts[cid]) or grab_brief_field(brief, "Anchor human moment")
        question = extract_question(texts[cid], meta)
        promise = grab_brief_field(brief, "Primary reader promise")
        if not promise:
            promise = grab_brief_field(brief, "Reader promise")
        # contribution = unique technical work / reason to exist
        contribution = grab_brief_field(brief, "Emphasis")
        if not contribution:
            concepts = (meta.get("concepts") or {}).get("introduced") or []
            contribution = ", ".join(concepts[:8]) if concepts else meta.get("title", "")
        forward = ""
        # crude bridge: look for "Chapter N" mentions in closing sections
        body = strip_frontmatter(texts[cid])
        fwd = re.findall(
            r"Chapter\s+(\d+|I{1,3}V?|VI?)[^\n.]{0,80}",
            body[-2500:],
            flags=re.I,
        )
        if fwd:
            forward = f"references later/adjacent: {', '.join(fwd[:5])}"
        identity_ok = bool(moment and question and contribution)
        rows.append(
            {
                "chapter_id": f"CH{int(cid[2:]):02d}",
                "number": int(cid[2:]),
                "title": meta.get("title", ""),
                "part": meta.get("part"),
                "anchor_moment": moment,
                "central_question": question,
                "primary_contribution": contribution[:400] or promise[:400],
                "reader_promise": promise[:400],
                "forward_backward_link": forward or "see part registry / neighboring chapters",
                "identity_clear": identity_ok,
                "identity_risk": (
                    "none"
                    if identity_ok
                    else "unclear moment/question/contribution — review before merge"
                ),
            }
        )
    return rows


def flag_identity_collisions(rows: list[dict[str, Any]]) -> list[Finding]:
    findings: list[Finding] = []
    # near-identical moments
    for i, a in enumerate(rows):
        for b in rows[i + 1 :]:
            na, nb = normalize(a["anchor_moment"]), normalize(b["anchor_moment"])
            if len(na) < 60 or len(nb) < 60:
                continue
            sa, sb = set(na.split()), set(nb.split())
            sim = len(sa & sb) / len(sa | sb) if sa and sb else 0.0
            if sim >= 0.72:
                findings.append(
                    Finding(
                        finding_id="",
                        kind="identity_collision",
                        severity="MAJOR" if sim >= 0.85 else "MODERATE",
                        chapters=[a["chapter_id"], b["chapter_id"]],
                        summary="Anchor moments are unusually similar across chapters.",
                        evidence=f"moment Jaccard(tokens)={sim:.2f}; A[:120]={a['anchor_moment'][:120]}",
                        disposition="FIX_CANDIDATE" if sim >= 0.85 else "OPEN",
                        similarity=sim,
                        notes="Each chapter needs a distinct human moment.",
                    )
                )
            nqa, nqb = normalize(a["central_question"]), normalize(b["central_question"])
            if len(nqa) > 40 and nqa == nqb:
                findings.append(
                    Finding(
                        finding_id="",
                        kind="identity_collision",
                        severity="MAJOR",
                        chapters=[a["chapter_id"], b["chapter_id"]],
                        summary="Central questions are identical.",
                        evidence=a["central_question"][:200],
                        disposition="FIX_CANDIDATE",
                    )
                )
    return findings


def find_exact_and_near_duplicates(paras: list[Paragraph]) -> list[Finding]:
    findings: list[Finding] = []
    by_hash: dict[str, list[Paragraph]] = defaultdict(list)
    for p in paras:
        by_hash[hashlib.sha1(p.norm.encode()).hexdigest()].append(p)

    for items in by_hash.values():
        chs = sorted({p.chapter for p in items})
        if len(chs) < 2:
            continue
        sample = items[0]
        wl = is_whitelisted(sample.norm)
        findings.append(
            Finding(
                finding_id="",
                kind="repeated_block",
                severity="EDITORIAL" if wl else "MODERATE",
                chapters=[c.upper() for c in chs],
                summary=(
                    "Whitelisted deliberate repeated construct."
                    if wl
                    else "Exact normalized paragraph repeated across chapters."
                ),
                evidence=re.sub(r"\s+", " ", sample.raw)[:220],
                disposition="INTENTIONAL_RETAIN" if wl else "OPEN",
                similarity=1.0,
                notes=f"section≈{sample.section}; whitelist={wl}",
            )
        )

    # near-duplicates via shingle inverted index
    inv: dict[str, set[int]] = defaultdict(set)
    for i, p in enumerate(paras):
        for sh in list(p.shingles)[:40]:
            inv[sh].add(i)
    cand: Counter[tuple[int, int]] = Counter()
    for idxs in inv.values():
        idxs_l = list(idxs)
        if len(idxs_l) > 60:
            continue
        for a in range(len(idxs_l)):
            for b in range(a + 1, len(idxs_l)):
                ia, ib = idxs_l[a], idxs_l[b]
                if paras[ia].chapter == paras[ib].chapter:
                    continue
                pair = (ia, ib) if ia < ib else (ib, ia)
                cand[pair] += 1

    seen_norm_pairs: set[tuple[str, str, str, str]] = set()
    for (ia, ib), hits in cand.items():
        if hits < 4:
            continue
        pa, pb = paras[ia], paras[ib]
        if pa.norm == pb.norm:
            continue  # already exact
        sim = jaccard(pa.shingles, pb.shingles)
        if sim < 0.55:
            continue
        key = tuple(sorted([pa.chapter, pb.chapter]) + [pa.norm[:60], pb.norm[:60]])  # type: ignore
        if key in seen_norm_pairs:
            continue
        seen_norm_pairs.add(key)  # type: ignore
        wl = is_whitelisted(pa.norm) or is_whitelisted(pb.norm)
        findings.append(
            Finding(
                finding_id="",
                kind="near_duplicate",
                severity="EDITORIAL" if wl else ("MAJOR" if sim >= 0.85 else "MODERATE"),
                chapters=[pa.chapter.upper(), pb.chapter.upper()],
                summary=(
                    "Whitelisted near-duplicate."
                    if wl
                    else "Unusually similar paragraphs across chapters."
                ),
                evidence=f"A[{pa.section}]: {re.sub(r'\\s+', ' ', pa.raw)[:140]} || B[{pb.section}]: {re.sub(r'\\s+', ' ', pb.raw)[:140]}",
                disposition="INTENTIONAL_RETAIN" if wl else "OPEN",
                similarity=sim,
            )
        )
    return findings


def find_templated_filler(texts: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    patterns = [
        (
            "not_x_not_y",
            r"[Nn]ot (?:a |an |the )?[\w-][^.,\n]{0,48}, not (?:a |an |the )?[\w-][^.,\n]{0,48}",
            "EDITORIAL",
        ),
        (
            "generic_promise",
            r"This chapter(?:'s promise)? is (?:simple|ordinary|honest)",
            "EDITORIAL",
        ),
        (
            "before_jargon",
            r"Before jargon, notice the human contract",
            "EDITORIAL",
        ),
    ]
    for kind, pat, sev in patterns:
        hits: dict[str, list[str]] = defaultdict(list)
        for cid, text in texts.items():
            for m in re.finditer(pat, text):
                hits[normalize(m.group(0))[:100]].append(cid.upper())
        for snippet, chs in hits.items():
            uniq = sorted(set(chs))
            if len(uniq) < 4:
                continue
            wl = is_whitelisted(snippet) or kind in {"before_jargon"}
            findings.append(
                Finding(
                    finding_id="",
                    kind="templated_filler",
                    severity="EDITORIAL",
                    chapters=uniq,
                    summary=f"Recurring template pattern ({kind}) across {len(uniq)} chapters.",
                    evidence=snippet[:180],
                    disposition="INTENTIONAL_RETAIN" if wl or kind == "before_jargon" else "OPEN",
                    notes="Pedagogical scaffold; retain unless prose is empty of chapter-specific content.",
                )
            )
    return findings


def find_term_before_explain(texts: dict[str, str], metas: dict[str, dict]) -> list[Finding]:
    """Flag formal **Term** uses before a same-chapter explanation cue."""
    findings: list[Finding] = []
    for cid, text in texts.items():
        body = strip_frontmatter(text)
        # bold terms that look like definitions later
        bold_terms = []
        for m in re.finditer(r"\*\*([A-Z][A-Za-z0-9][A-Za-z0-9 /-]{1,48})\*\*", body):
            term = m.group(1).strip()
            if term.lower() in {
                "status",
                "author",
                "manuscript",
                "gate note",
                "inheritance",
                "goal",
                "route a",
                "route b",
                "route c",
                "truth",
            }:
                continue
            bold_terms.append((term, m.start()))
        introduced = set((metas[cid].get("concepts") or {}).get("introduced") or [])
        # for each early bold term, see if an explanation ("is ", "means ", "—") appears later
        seen_early: set[str] = set()
        for term, pos in bold_terms:
            key = term.lower()
            if key in seen_early:
                continue
            # only consider first 35% of chapter as "early"
            if pos > len(body) * 0.35:
                continue
            # skip if term is in introduced list and first heading after is a definition-ish section
            expl = re.search(
                rf"\*\*{re.escape(term)}\*\*\s*(?:is|means|—|:)\s",
                body[pos : pos + 800],
                re.I,
            )
            if expl:
                continue
            # if term appears in glossary-ish later section only
            later_def = re.search(
                rf"(?:###?\s+{re.escape(term)}|\*\*{re.escape(term)}\*\*\s*(?:is|means))",
                body[pos + 200 :],
                re.I,
            )
            if later_def and pos < len(body) * 0.2:
                # only flag if not a known early teaching term from concepts.introduced slug overlap
                slug = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
                if slug in introduced or any(slug in str(x) for x in introduced):
                    continue
                seen_early.add(key)
                findings.append(
                    Finding(
                        finding_id="",
                        kind="term_before_explain",
                        severity="MINOR",
                        chapters=[cid.upper()],
                        summary=f"Term “{term}” appears early; fuller explanation arrives later in-chapter.",
                        evidence=f"first_pos={pos}; later_def_offset≈{pos + 200 + later_def.start()}",
                        disposition="OPEN",
                        notes="Often acceptable foreshadowing; escalate only if reader-blocking.",
                    )
                )
    return findings


def find_bad_transitions(texts: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []
    for cid, text in texts.items():
        body = strip_frontmatter(text)
        # abrupt part-boundary feel: chapter claims "this chapter closes X" but never names prior chapter
        if re.search(r"Part [IVX]+ (?:has already|closes|opens)", body) and not re.search(
            r"Chapter\s+\d+", body[:1500]
        ):
            # soft signal only for part openers
            pass
        # conclusion without forward bridge
        check = re.search(
            r"##\s+\d+\.\s+Check understanding.*?(?=##\s+\d+\.\s+Glossary|##\s+References|\Z)",
            body,
            re.S | re.I,
        )
        if check:
            block = check.group(0)
            if not re.search(
                r"Chapter\s+\d+|next chapter|later chapter|Part [IVX]+|inherits|bridges",
                block,
                re.I,
            ):
                # many chapters use career/check without forward pointer — EDITORIAL
                findings.append(
                    Finding(
                        finding_id="",
                        kind="bad_transition",
                        severity="EDITORIAL",
                        chapters=[cid.upper()],
                        summary="Check-understanding / close block lacks an explicit forward chapter bridge.",
                        evidence=re.sub(r"\s+", " ", block[:160]),
                        disposition="OPEN",
                        notes="Not always harmful; prefer explicit next-step when Part boundary is near.",
                    )
                )
        # consecutive sections with near-identical first paragraphs (within chapter)
        sections = re.split(r"\n##\s+", body)
        norms = []
        for sec in sections[1:]:
            paras = [normalize(p) for p in re.split(r"\n\s*\n", sec) if len(normalize(p)) > 80]
            if paras:
                norms.append(paras[0][:200])
        for i in range(len(norms) - 1):
            if norms[i] == norms[i + 1]:
                findings.append(
                    Finding(
                        finding_id="",
                        kind="bad_transition",
                        severity="MODERATE",
                        chapters=[cid.upper()],
                        summary="Adjacent sections open with the same paragraph.",
                        evidence=norms[i][:180],
                        disposition="OPEN",
                    )
                )
    return findings


def find_contradictions(texts: dict[str, str]) -> list[Finding]:
    """Heuristic contradiction scan for known teaching assertions."""
    findings: list[Finding] = []
    # Gather Stability Contract definition variants
    defs: list[tuple[str, str]] = []
    for cid, text in texts.items():
        for m in re.finditer(
            r"((?:The\s+)?\*\*Stability Contract\*\*[^.]*\.)",
            text,
        ):
            defs.append((cid.upper(), normalize(m.group(1))))
        for m in re.finditer(
            r"(>\s*A user experience exists only while[^\n]+)",
            text,
        ):
            defs.append((cid.upper(), normalize(m.group(1))))
    # if definitions diverge beyond whitelist core phrase
    core = "user experience exists only while multiple hidden technical conditions remain within acceptable bounds"
    divergent = [(c, d) for c, d in defs if core not in d and "stability contract" in d]
    # Look for direct conflicts: "is the same as" vs "is not the same as" for key pairs
    pairs = [
        ("ram", "storage"),
        ("latency", "throughput"),
        ("authentication", "authorization"),
        ("process", "thread"),
        ("qos", "qoe"),
        ("firmware", "operating system"),
    ]
    for a, b in pairs:
        same_as: list[str] = []
        not_same: list[str] = []
        for cid, text in texts.items():
            n = normalize(text)
            if re.search(rf"{a}.{{0,40}}(?:is|are) (?:the )?same as.{{0,40}}{b}", n):
                same_as.append(cid.upper())
            if re.search(
                rf"{a}.{{0,60}}(?:not (?:the )?same as|≠|is not).{{0,40}}{b}",
                n,
            ):
                not_same.append(cid.upper())
        if same_as and not_same:
            findings.append(
                Finding(
                    finding_id="",
                    kind="contradiction",
                    severity="MAJOR",
                    chapters=sorted(set(same_as + not_same)),
                    summary=f"Possible contradiction on {a} vs {b} equivalence.",
                    evidence=f"same_as_in={same_as}; not_same_in={not_same}",
                    disposition="OPEN",
                )
            )
    if divergent:
        findings.append(
            Finding(
                finding_id="",
                kind="contradiction",
                severity="MODERATE",
                chapters=sorted({c for c, _ in divergent}),
                summary="Stability Contract wording variants diverge from the canonical teaching sentence.",
                evidence=divergent[0][1][:200],
                disposition="OPEN",
                notes="Canonical CE-6 sentence should remain stable; local elaboration is OK if not conflicting.",
            )
        )
    return findings


def assign_ids(findings: list[Finding]) -> None:
    counts: Counter[str] = Counter()
    for f in findings:
        counts[f.kind] += 1
        f.finding_id = f"CONT-{f.kind.upper()[:12]}-{counts[f.kind]:03d}"


def apply_known_dispositions(findings: list[Finding]) -> None:
    """Encode Phase-1 judgment for clear cases before Phase-2 edits."""
    for f in findings:
        chs = set(f.chapters)
        ev = f.evidence.lower()
        if f.disposition != "OPEN":
            continue
        # CH20/CH31 shared connected-but-unusable moment / notice / try-it
        if chs >= {"CH20", "CH31"} and f.kind in {
            "repeated_block",
            "near_duplicate",
            "identity_collision",
        }:
            if any(
                x in ev
                for x in (
                    "everything looks connected",
                    "status shown",
                    "route a — notebook",
                    "lab-ce06-001",
                    "connected-but-unusable",
                    "researcher prompt",
                )
            ) or f.kind == "identity_collision":
                f.disposition = "FIX_CANDIDATE"
                f.severity = "MAJOR" if f.severity in {"MODERATE", "MINOR", "EDITORIAL"} else f.severity
                f.notes = (
                    (f.notes + " " if f.notes else "")
                    + "CH31 must not re-teach CH20 as a second latency lecture; inherit CE-6/CH20."
                )
        # CH06/CH12 identical observable question (CPU framing on OS chapter)
        if chs >= {"CH06", "CH12"} and "familiar local app feels slow" in ev:
            f.disposition = "FIX_CANDIDATE"
            f.severity = "MODERATE"
            f.notes = (
                (f.notes + " " if f.notes else "")
                + "Shared LAB-CMS-001 is intentional; CH12 observable question should emphasize process/thread/scheduler."
            )
        # CH01/CH14 shared systems-lens orientation cards (distinct chapters; shared CE-1 adjacency)
        if chs >= {"CH01", "CH14"} and f.kind in {"repeated_block", "near_duplicate"}:
            if any(x in ev for x in ("orientation tools", "content you can act on")):
                f.disposition = "INTENTIONAL_RETAIN"
                f.notes = "Shared systems-lens orientation cards; chapters diverge in technical depth."
        # Shared LAB-CMS-001 / LAB-CE06-001 operational boilerplate (prereqs, redaction, fixtures)
        if f.kind in {"repeated_block", "near_duplicate"} and any(
            x in ev
            for x in (
                "prerequisites.",
                "monitor screenshots can leak",
                "activity visualizations and color-coded",
                "educators can facilitate",
                "read-only sampling where the os exposes",
                "builder extension.",
                "researcher extension.",
                "educator facilitation.",
                "prefer fixtures and redaction",
                "do not present illustrative fixture",
                "fixture completion is first-class",
                "route f",
                "not every learner has a new multi-core",
                "shared family or school machines",
                "screenshots and logs are evidence and risk",
                "do not save passwords, tokens, private message",
            )
        ):
            f.disposition = "INTENTIONAL_RETAIN"
            f.severity = "EDITORIAL"
            f.notes = (
                (f.notes + " " if f.notes else "")
                + "Shared lab safety / pathway scaffolding retained deliberately."
            )
        # Stability Contract local elaborations are not contradictions of the canonical sentence
        if f.kind == "contradiction" and "stability contract" in ev:
            f.disposition = "INTENTIONAL_RETAIN"
            f.severity = "EDITORIAL"
            f.notes = (
                "Local elaboration coexists with the canonical CE-6 sentence; not a logical conflict."
            )

def write_report(
    ledger: dict[str, Any],
    identity_rows: list[dict[str, Any]],
    findings: list[Finding],
) -> str:
    counts = Counter(f.kind for f in findings)
    by_disp = Counter(f.disposition for f in findings)
    by_sev = Counter(f.severity for f in findings)
    unclear = [r for r in identity_rows if not r.get("identity_clear")]
    fix = [f for f in findings if f.disposition == "FIX_CANDIDATE"]
    retained = [f for f in findings if f.disposition == "INTENTIONAL_RETAIN"]

    lines = [
        "# Full31 Continuity Report",
        "",
        f"**Generated:** {ledger['generated']}  ",
        f"**Base SHA:** `{ledger['base_sha']}`  ",
        f"**Tool:** `scripts/audit_full31_continuity.py` (audit aid; not auto-rewrite)",
        "",
        "## Scope",
        "",
        "- All 31 manuscript chapters under `book/chapters/ch*/chapter.md`",
        "- Flags: repeated blocks, near-duplicates, templated filler, contradictions,",
        "  term-before-explain, bad transitions, identity collisions",
        "- Whitelist: Stability Contract canonical sentence, status/gate banners, safety",
        "  boundaries, glossary boilerplate, pedagogical scaffolds, Device Quartet caveats",
        "",
        "## Counts",
        "",
        f"| Metric | Count |",
        f"|---|---:|",
        f"| Total findings | {len(findings)} |",
        f"| FIX_CANDIDATE | {by_disp.get('FIX_CANDIDATE', 0)} |",
        f"| INTENTIONAL_RETAIN | {by_disp.get('INTENTIONAL_RETAIN', 0)} |",
        f"| OPEN | {by_disp.get('OPEN', 0)} |",
        f"| FIXED (post Phase 2) | {by_disp.get('FIXED', 0)} |",
        "",
        "### By kind",
        "",
        "| Kind | Count |",
        "|---|---:|",
    ]
    for k, n in sorted(counts.items()):
        lines.append(f"| `{k}` | {n} |")
    lines += [
        "",
        "### By severity",
        "",
        "| Severity | Count |",
        "|---|---:|",
    ]
    for s in SEVERITY:
        if by_sev.get(s):
            lines.append(f"| {s} | {by_sev[s]} |")

    lines += [
        "",
        "## Chapter identity matrix",
        "",
        "Canonical machine-readable matrix:",
        "`publication/full31/quality/CHAPTER_IDENTITY_MATRIX.yaml`",
        "",
        "Human-readable companion:",
        "`publication/full31/quality/CHAPTER_IDENTITY_MATRIX.md`",
        "",
        f"Identity-clear chapters: **{len(identity_rows) - len(unclear)} / {len(identity_rows)}**",
        "",
    ]
    if unclear:
        lines.append("Chapters flagged for unclear identity:")
        for r in unclear:
            lines.append(f"- {r['chapter_id']}: {r.get('identity_risk')}")
        lines.append("")

    lines += ["## Highest-priority fix candidates", ""]
    if not fix:
        lines.append("_No FIX_CANDIDATE items._")
    else:
        for f in sorted(fix, key=lambda x: SEVERITY.index(x.severity)):
            lines.append(
                f"- **{f.finding_id}** ({f.severity}, {f.kind}) "
                f"{', '.join(f.chapters)} — {f.summary}"
            )
            lines.append(f"  - Evidence: {f.evidence[:200]}")
            if f.notes:
                lines.append(f"  - Notes: {f.notes}")
    lines += ["", "## Intentional retained samples", ""]
    for f in retained[:12]:
        lines.append(
            f"- **{f.finding_id}** {', '.join(f.chapters)} — {f.summary}"
        )
    if len(retained) > 12:
        lines.append(f"- … {len(retained) - 12} more retained (see ledger)")

    lines += [
        "",
        "## Phase 2 resolutions (this wave)",
        "",
        "Scoped prose edits only; chapters not merged; Gate 3 untouched.",
        "",
        "### Fixed (harmful duplication / identity collision)",
        "",
        "- **CH31** — Distinct EMIT/portfolio anchor moment; notice + Try It reframed to inherit CH20/CE-6 instead of re-teaching connected≠usable; career/check prompts capstone-specific.",
        "- **CH12** — LAB-CMS-001 observable question + prediction + misconception probe reframed to process/thread/scheduler (no longer a CH06 CPU clone).",
        "- **CH07** — LAB-CMS-001 observable question reframed to memory/storage/hierarchy.",
        "- **CH14** — LAB-SYS-001 observable question reframed to UI/runtime/libraries/APIs.",
        "- **CH06** — OS-vs-app misconception probe points forward to CH12 instead of cloning CH12 wording.",
        "",
        "### Intentional retained",
        "",
        "- Canonical Stability Contract sentence and local elaborations.",
        "- Status / Gate banners; safety / privacy / redaction boundaries.",
        "- Shared lab packet scaffolding (LAB-CMS-001, LAB-CE06-001) where chapters deliberately inherit.",
        "- Pedagogical scaffold headings (moment → notice → …) and glossary boilerplate.",
        "",
        "## Phase 2 policy",
        "",
        "- Fix only clear harmful duplication / contradictions.",
        "- Do not remove helpful reinforcement.",
        "- Do not merge chapters.",
        "- Do not touch Gate 3 / CH02-REVIEW-R1.",
        "",
        "## Method notes",
        "",
        "- Exact match: SHA1 of normalized paragraph (citations/markup stripped).",
        "- Near match: 5-token shingle Jaccard ≥ 0.55 with inverted-index candidates.",
        "- Identity collision: token Jaccard ≥ 0.72 on anchor moments; exact central questions.",
        "- Whitelist patterns live in `scripts/audit_full31_continuity.py`.",
        "",
    ]
    return "\n".join(lines) + "\n"


def identity_md(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Chapter identity matrix",
        "",
        "Each chapter must keep a distinct anchor moment, central question, and contribution.",
        "Do not merge chapters in this wave.",
        "",
        "| CH | Title | Anchor moment | Central question | Contribution | Clear? |",
        "|---:|---|---|---|---|---|",
    ]
    for r in rows:
        def esc(s: str) -> str:
            return (s or "").replace("|", "/").replace("\n", " ")[:120]

        lines.append(
            f"| {r['number']} | {esc(r['title'])} | {esc(r['anchor_moment'])} | "
            f"{esc(r['central_question'])} | {esc(r['primary_contribution'])} | "
            f"{'yes' if r['identity_clear'] else 'NO'} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    import subprocess

    OUT.mkdir(parents=True, exist_ok=True)
    base_sha = (
        subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT)
        .decode()
        .strip()
    )

    texts: dict[str, str] = {}
    metas: dict[str, dict[str, Any]] = {}
    all_paras: list[Paragraph] = []
    for cid in chapter_ids():
        texts[cid] = load_chapter_text(cid)
        metas[cid] = load_yaml(CHAPTERS / cid / "metadata.yaml") or {}
        all_paras.extend(extract_paragraphs(cid, texts[cid]))

    identity_rows = build_identity_matrix(texts, metas)
    findings: list[Finding] = []
    findings.extend(find_exact_and_near_duplicates(all_paras))
    findings.extend(find_templated_filler(texts))
    findings.extend(find_contradictions(texts))
    findings.extend(find_term_before_explain(texts, metas))
    findings.extend(find_bad_transitions(texts))
    findings.extend(flag_identity_collisions(identity_rows))
    assign_ids(findings)
    apply_known_dispositions(findings)

    # Promote major CH20/CH31 / CH06/CH12 aggregates into ledger summary entries
    pair_open = Counter()
    for f in findings:
        if f.disposition in {"OPEN", "FIX_CANDIDATE"} and len(f.chapters) == 2:
            pair_open[tuple(sorted(f.chapters))] += 1

    ledger = {
        "schema": "full31.continuity_ledger.v1",
        "generated": str(date.today()),
        "base_sha": base_sha,
        "tool": "scripts/audit_full31_continuity.py",
        "policy": {
            "audit_aid_only": True,
            "no_auto_rewrite": True,
            "no_chapter_merge": True,
            "no_gate3_edits": True,
            "whitelist": [
                "Stability Contract canonical teaching sentence",
                "status / gate banners",
                "safety / privacy boundaries",
                "glossary candidate boilerplate",
                "pedagogical scaffolds (moment→notice→…)",
                "Device Quartet / representative-architecture caveats",
            ],
        },
        "counts": {
            "findings_total": len(findings),
            "by_kind": dict(sorted(Counter(f.kind for f in findings).items())),
            "by_severity": dict(sorted(Counter(f.severity for f in findings).items())),
            "by_disposition": dict(
                sorted(Counter(f.disposition for f in findings).items())
            ),
            "identity_clear": sum(1 for r in identity_rows if r["identity_clear"]),
            "identity_unclear": sum(1 for r in identity_rows if not r["identity_clear"]),
        },
        "hot_pairs": [
            {"chapters": list(pair), "open_or_fix_findings": n}
            for pair, n in pair_open.most_common(12)
        ],
        "identity_matrix_path": "publication/full31/quality/CHAPTER_IDENTITY_MATRIX.yaml",
        "phase2_resolutions": {
            "fixed": [
                {
                    "chapters": ["CH31"],
                    "change": "Distinct EMIT/portfolio moment; inherit CH20/CE-6 instead of re-teaching connected≠usable; capstone-specific Try It / career / check prompts.",
                },
                {
                    "chapters": ["CH12"],
                    "change": "LAB-CMS-001 observable question, prediction, and misconception probe reframed to process/thread/scheduler.",
                },
                {
                    "chapters": ["CH07"],
                    "change": "LAB-CMS-001 observable question reframed to memory/storage/hierarchy.",
                },
                {
                    "chapters": ["CH14"],
                    "change": "LAB-SYS-001 observable question reframed to UI/runtime/libraries/APIs.",
                },
                {
                    "chapters": ["CH06"],
                    "change": "OS-vs-app misconception probe now points forward to CH12 instead of cloning CH12 wording.",
                },
            ],
            "intentional_retained": [
                "Stability Contract canonical sentence + safe local elaborations",
                "Status/gate banners; safety/privacy/redaction boundaries",
                "Shared LAB-CMS-001 / LAB-CE06-001 operational scaffolding",
                "Pedagogical scaffolds and glossary boilerplate",
            ],
            "not_done": [
                "No chapter merges",
                "No Gate 3 / CH02-REVIEW-R1 edits",
            ],
        },
        "findings": [f.to_dict() for f in findings],
    }

    (OUT / "CONTINUITY_LEDGER.yaml").write_text(dump_yaml(ledger), encoding="utf-8")
    (OUT / "CONTINUITY_REPORT.md").write_text(
        write_report(ledger, identity_rows, findings), encoding="utf-8"
    )
    (OUT / "CHAPTER_IDENTITY_MATRIX.yaml").write_text(
        dump_yaml(
            {
                "schema": "full31.chapter_identity_matrix.v1",
                "generated": str(date.today()),
                "base_sha": base_sha,
                "chapters": identity_rows,
            }
        ),
        encoding="utf-8",
    )
    (OUT / "CHAPTER_IDENTITY_MATRIX.md").write_text(
        identity_md(identity_rows), encoding="utf-8"
    )

    print(f"Wrote {OUT / 'CONTINUITY_LEDGER.yaml'}")
    print(f"Wrote {OUT / 'CONTINUITY_REPORT.md'}")
    print(f"Wrote {OUT / 'CHAPTER_IDENTITY_MATRIX.yaml'}")
    print(f"findings={len(findings)} dispositions={dict(Counter(f.disposition for f in findings))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
