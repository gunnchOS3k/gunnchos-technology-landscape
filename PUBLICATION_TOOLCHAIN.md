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

### Selection criteria (weighted)

Markdown-first authoring, PDF quality, EPUB support, cross-references, citations, figure handling, accessibility hooks, reproducibility, automation, contributor usability.

Quarto best balanced these for a synchronized publication system.

## Fallback

If Quarto is unavailable in an environment, `make preview` falls back to a static HTML preview generated from Markdown, and PDF/EPUB targets report FAIL honestly rather than fabricating PASS.

## Commands

```bash
make setup
make validate
make test
make preview
make pdf
make epub
make all
```
