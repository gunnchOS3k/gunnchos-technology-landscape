# Render projects

Chapter and Concept Edition modules use a **chapter-local** Quarto project file
beside their source, not a temporary rename of the root book config.

## Pattern

```text
book/chapters/ch02/_quarto.yml     # Chapter 2 standalone → preview/
book/chapters/chNN/_quarto.yml     # future chapters
concept-edition/ce-0N/_quarto.yml  # Concept Edition modules (same idea)
_quarto.yml                        # root book project → _book/ (untouched by chapter builds)
```

## Commands

```bash
quarto render book/chapters/ch02 --to html   # also: make preview
quarto render book/chapters/ch02 --to pdf    # also: make pdf
quarto render book/chapters/ch02 --to epub   # also: make epub
quarto render .                              # also: make book
```

Outputs for Chapter 2 are normalized to `preview/ch02.{html,pdf,epub}`.

See `PUBLICATION_TOOLCHAIN.md` for the full decision record.
