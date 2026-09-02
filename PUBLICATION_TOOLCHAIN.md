# Publication Toolchain

## Decision

**Selected primary toolchain: Quarto** (Markdown-first), with Pandoc as the underlying conversion engine.

### Candidates evaluated

| Tool | Strengths | Risks for this project |
|---|---|---|
| Quarto | Markdown-first, PDF/EPUB/HTML, cross-refs, citations, reproducible projects | Requires install; heavier than plain Pandoc |
| Pandoc alone | Universal conversion | Weaker project structure for multi-format book |
| Typst | Excellent PDF typography | EPUB/accessibility ecosystem less mature |
| LaTeX | Print control | Higher contributor friction |
| Sphinx | Docs/HTML strength | Book+EPUB path less natural |
| mdBook | Simple HTML books | Weak print/EPUB story |

## Commands

```bash
make setup
make validate
make test
make preview
make pdf
make epub
make all
make ci
```

| Target | Meaning |
|---|---|
| `make all` | validate + test + HTML + PDF + EPUB (fails honestly if deps missing) |
| `make ci` | validate + test + HTML (hosted CI default; EPUB attempted separately in workflow) |

## Portability

- Quarto: `QUARTO_BIN` env override, else `tools/quarto/bin/quarto`, else `PATH`
- TeX/xelatex: `TEXLIVE_BIN` env override, else common TinyTeX/TeX Live locations on macOS and Linux
- Do not hard-code only `${HOME}/Library/TinyTeX/bin/universal-darwin`

Bootstrap helpers:

- `scripts/bootstrap_quarto.sh`
- TinyTeX via `quarto install tinytex` when PDF is required

## Growth path

Chapter 2 is the canonical prototype. Concept Edition modules and the full 31-chapter book should accumulate under `book/chapters/` and `concept-edition/` without rewriting the toolchain decision.

## PDF SVG dependency

PDF builds require an SVG converter on PATH (`rsvg-convert` from librsvg, or Inkscape).

- macOS: `brew install librsvg`
- Debian/Ubuntu: `apt-get install librsvg2-bin`
