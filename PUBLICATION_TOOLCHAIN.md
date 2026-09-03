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

## Quarto architecture (no config renaming)

Two Quarto project layers coexist; **neither build path moves or renames** root `_quarto.yml`.

| Project | Config | Purpose | Deterministic output |
|---|---|---|---|
| Chapter prototype | `book/chapters/ch02/_quarto.yml` | Independent Chapter 2 HTML/PDF/EPUB | `preview/ch02.{html,pdf,epub}` |
| Full 31-chapter book | `_quarto.yml` (repo root) | All 31 chapters + front/back matter | `preview/full31/technology-landscape-full31-{html,pdf,epub}` |
| Legacy book render | `_quarto.yml` via `make book` | Quarto default `_book/` | `_book/` |

### Why a chapter-local project?

Root `_quarto.yml` is a Quarto **book** project. Rendering a single chapter through the book project redirects outputs into `_book/`. A **default** project beside the chapter source:

- keeps figure paths valid relative to `chapter.md`,
- sets `output-dir` to repo `preview/`,
- never touches the book config,
- **preserves the historical CH02 reader package** used by Gate 3 / `docs/`.

### Extending to Concept Edition (six modules)

Add a sibling `_quarto.yml` beside each module as it matures:

```text
book/chapters/ch02/_quarto.yml
book/chapters/chNN/_quarto.yml
concept-edition/ce-01/_quarto.yml … ce-06/
```

Each uses `project.type: default`, a deterministic `output-dir` under `preview/` (or a module-specific preview name), and leaves root `_quarto.yml` as the full-book aggregator.

### Commands

```bash
make preview      # CH02 HTML → preview/ch02.html (reader package path)
make pdf          # CH02 PDF
make epub         # CH02 EPUB
make book         # root book → _book/ (legacy)
make full31-html  # full 31 → preview/full31/technology-landscape-full31-html/
make full31-pdf   # full 31 → preview/full31/technology-landscape-full31-pdf.pdf
make full31-epub  # full 31 → preview/full31/technology-landscape-full31-epub.epub
make full31-book  # html + epub + pdf
make full31-draft-check   # infra mode by default; FULL31_DRAFT_CHECK_MODE=strict for Batch 1+
```

`scripts/render_formats.sh` normalizes Quarto’s `chapter.*` filenames to `preview/ch02.*`. It does **not** search `$HOME` or other arbitrary paths for outputs.

`scripts/render_full31.sh` renders the root book project into named full31 artifacts and does **not** overwrite `preview/ch02.*` or `docs/`.

## Make targets

```bash
make setup
make validate
make test
make preview
make pdf
make epub
make book
make full31-html
make full31-pdf
make full31-epub
make full31-book
make full31-draft-check
make all
make ci
```

| Target | Meaning |
|---|---|
| `make all` | **Authoritative full build:** validate + test + HTML + PDF + EPUB (CH02 path) |
| `make ci` | TeX-free subset: validate + test + HTML (useful without a TeX install) |
| `make full31-*` | Full 31-chapter artifacts under `preview/full31/` (separate from CH02 reader package) |
| `make full31-draft-check` | Manuscript QA (`infra` default; `FULL31_DRAFT_CHECK_MODE=strict` for WORKING_DRAFT_COMPLETE) |
| Hosted GitHub Actions | Provisions Quarto + TeX + librsvg, then runs validate, test, HTML, EPUB, **and PDF**; uploads artifacts |

## Portability

- Quarto: `QUARTO_BIN` env override, else `tools/quarto/bin/quarto`, else `PATH`
- TeX/xelatex: `TEXLIVE_BIN` env override, else common TinyTeX / TeX Live locations
- Do not hard-code only `${HOME}/Library/TinyTeX/bin/universal-darwin`

Bootstrap helpers:

- `scripts/bootstrap_quarto.sh`
- TinyTeX via `quarto install tinytex` when PDF is required locally

## PDF SVG dependency

PDF builds require an SVG converter on PATH (`rsvg-convert` from librsvg, or Inkscape).

- macOS: `brew install librsvg`
- Debian/Ubuntu: `apt-get install librsvg2-bin`
- Hosted CI installs `librsvg2-bin` and TeX before `make pdf`

## Growth path

Chapter 2 is the canonical prose prototype. Concept Edition modules and the full 31-chapter book accumulate under `concept-edition/` and `book/chapters/` without rewriting this toolchain decision or reintroducing config-file rename workarounds.
