#!/usr/bin/env bash
# Render Chapter 2 formats into ./preview without book-project path confusion.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FORMAT="${1:?format required: html|pdf|epub}"
export PATH="$ROOT/tools/quarto/bin:${HOME}/Library/TinyTeX/bin/universal-darwin:${PATH}"
QUARTO_BIN="${QUARTO:-$ROOT/tools/quarto/bin/quarto}"
mkdir -p "$ROOT/preview"

if [[ ! -x "$QUARTO_BIN" ]]; then
  if [[ "$FORMAT" == "html" ]]; then
    "$ROOT/.venv/bin/python" "$ROOT/scripts/render_preview.py"
    exit 0
  fi
  echo "${FORMAT}: FAIL — Quarto not installed"
  exit 1
fi

if [[ "$FORMAT" == "pdf" ]] && ! command -v xelatex >/dev/null 2>&1; then
  echo "pdf: FAIL — TeX engine (xelatex/TinyTeX) not installed"
  exit 1
fi

MOVED=0
if [[ -f "$ROOT/_quarto.yml" ]]; then
  mv "$ROOT/_quarto.yml" "$ROOT/_quarto.yml.book"
  MOVED=1
fi
cleanup() {
  if [[ "$MOVED" -eq 1 && -f "$ROOT/_quarto.yml.book" ]]; then
    mv "$ROOT/_quarto.yml.book" "$ROOT/_quarto.yml"
  fi
}
trap cleanup EXIT

SRC="$ROOT/book/chapters/ch02/chapter.md"
# Render beside the source, then move into preview/ (Quarto path math is unreliable with deep trees).
case "$FORMAT" in
  html)
    "$QUARTO_BIN" render "$SRC" --to html
    if [[ -f "$ROOT/book/chapters/ch02/chapter.html" ]]; then
      mv -f "$ROOT/book/chapters/ch02/chapter.html" "$ROOT/preview/ch02.html"
    elif [[ -f "$HOME/ch02.html" ]]; then
      mv -f "$HOME/ch02.html" "$ROOT/preview/ch02.html"
    else
      # fallback
      "$ROOT/.venv/bin/python" "$ROOT/scripts/render_preview.py"
    fi
    ;;
  pdf)
    "$QUARTO_BIN" render "$SRC" --to pdf
    if [[ -f "$ROOT/book/chapters/ch02/chapter.pdf" ]]; then
      mv -f "$ROOT/book/chapters/ch02/chapter.pdf" "$ROOT/preview/ch02.pdf"
    elif [[ -f "$HOME/ch02.pdf" ]]; then
      mv -f "$HOME/ch02.pdf" "$ROOT/preview/ch02.pdf"
    else
      echo "pdf: FAIL — could not locate rendered PDF"; exit 1
    fi
    ;;
  epub)
    "$QUARTO_BIN" render "$SRC" --to epub
    if [[ -f "$ROOT/book/chapters/ch02/chapter.epub" ]]; then
      mv -f "$ROOT/book/chapters/ch02/chapter.epub" "$ROOT/preview/ch02.epub"
    elif [[ -f "$HOME/ch02.epub" ]]; then
      mv -f "$HOME/ch02.epub" "$ROOT/preview/ch02.epub"
    else
      echo "epub: FAIL — could not locate rendered EPUB"; exit 1
    fi
    ;;
  *)
    echo "Unknown format: $FORMAT"
    exit 1
    ;;
esac

echo "Rendered $FORMAT into $ROOT/preview"
ls -la "$ROOT/preview"
