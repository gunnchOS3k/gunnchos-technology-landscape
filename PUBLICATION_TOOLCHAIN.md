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
| Book project | `_quarto.yml` (repo root) | Accumulating book (`index.qmd` + chapters) | `_book/` |

### Why a chapter-local project?

Root `_quarto.yml` is a Quarto **book** project. Rendering a single chapter through the book project redirects outputs into `_book/`. A **default** project beside the chapter source:

- keeps figure paths valid relative to `chapter.md`,
- sets `output-dir` to repo `preview/`,
- never touches the book config.

Earlier Wave-1 scripts temporarily renamed `_quarto.yml` during builds. That workaround is removed.

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
make preview   # quarto render book/chapters/ch02 --to html
make pdf       # quarto render book/chapters/ch02 --to pdf
make epub      # quarto render book/chapters/ch02 --to epub
make book      # quarto render .  (root book → _book/)
```

`scripts/render_formats.sh` normalizes Quarto’s `chapter.*` filenames to `preview/ch02.*`. It does **not** search `$HOME` or other arbitrary paths for outputs.

## Make targets

```bash
make setup
make validate
make test
make preview
make pdf
make epub
make book
make all
make ci
```

| Target | Meaning |
|---|---|
| `make all` | **Authoritative full build:** validate + test + HTML + PDF + EPUB |
| `make ci` | TeX-free subset: validate + test + HTML (useful without a TeX install) |
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
