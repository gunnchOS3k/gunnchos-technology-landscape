#!/usr/bin/env bash
# Render Chapter 2 formats into ./preview with portable Quarto/TeX discovery.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FORMAT="${1:?format required: html|pdf|epub}"

discover_quarto() {
  if [[ -n "${QUARTO_BIN:-}" && -x "${QUARTO_BIN}" ]]; then
    echo "${QUARTO_BIN}"; return
  fi
  if [[ -x "$ROOT/tools/quarto/bin/quarto" ]]; then
    echo "$ROOT/tools/quarto/bin/quarto"; return
  fi
  if command -v quarto >/dev/null 2>&1; then
    command -v quarto; return
  fi
  echo ""
}

discover_tex_bin() {
  if [[ -n "${TEXLIVE_BIN:-}" && -d "${TEXLIVE_BIN}" ]]; then
    echo "${TEXLIVE_BIN}"; return
  fi
  local candidates=(
    "${HOME}/Library/TinyTeX/bin/universal-darwin"
    "${HOME}/Library/TinyTeX/bin/aarch64-darwin"
    "${HOME}/Library/TinyTeX/bin/x86_64-darwin"
    "${HOME}/.TinyTeX/bin/x86_64-linux"
    "${HOME}/.TinyTeX/bin/aarch64-linux"
    "/usr/local/texlive/2025/bin/x86_64-linux"
    "/usr/local/texlive/2024/bin/x86_64-linux"
  )
  local c
  for c in "${candidates[@]}"; do
    if [[ -x "${c}/xelatex" ]]; then echo "${c}"; return; fi
  done
  echo ""
}

QUARTO_BIN_RESOLVED="$(discover_quarto)"
TEX_BIN="$(discover_tex_bin)"
if [[ -n "${TEX_BIN}" ]]; then export PATH="${TEX_BIN}:${PATH}"; fi
if [[ -x "$ROOT/tools/quarto/bin/quarto" ]]; then export PATH="$ROOT/tools/quarto/bin:${PATH}"; fi
mkdir -p "$ROOT/preview"

if [[ -z "${QUARTO_BIN_RESOLVED}" ]]; then
  if [[ "$FORMAT" == "html" ]]; then
    "$ROOT/.venv/bin/python" "$ROOT/scripts/render_preview.py"; exit 0
  fi
  echo "${FORMAT}: FAIL — Quarto not installed. Set QUARTO_BIN or run scripts/bootstrap_quarto.sh"
  exit 1
fi

if [[ "$FORMAT" == "pdf" ]]; then
  if ! command -v xelatex >/dev/null 2>&1; then
    echo "pdf: FAIL — TeX engine (xelatex) not installed. export TEXLIVE_BIN=... or install TinyTeX"
    exit 1
  fi
  if ! command -v rsvg-convert >/dev/null 2>&1 && ! command -v inkscape >/dev/null 2>&1; then
    echo "pdf: FAIL — SVG→PDF converter missing (rsvg-convert or inkscape)."
    echo "      macOS: brew install librsvg    Linux: apt-get install librsvg2-bin"
    exit 1
  fi
fi

# Avoid book-project output redirection for single-chapter prototype renders.
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
case "$FORMAT" in
  html)
    "${QUARTO_BIN_RESOLVED}" render "$SRC" --to html
    ;;
  pdf)
    "${QUARTO_BIN_RESOLVED}" render "$SRC" --to pdf
    ;;
  epub)
    "${QUARTO_BIN_RESOLVED}" render "$SRC" --to epub
    ;;
  *)
    echo "Unknown format: $FORMAT"; exit 1
    ;;
esac

# Collect outputs from known locations.
collect() {
  local ext="$1"
  local dest="$ROOT/preview/ch02.${ext}"
  local candidates=(
    "$ROOT/book/chapters/ch02/chapter.${ext}"
    "$ROOT/book/chapters/ch02/ch02.${ext}"
    "$ROOT/_book/book/chapters/ch02/chapter.${ext}"
    "$ROOT/_book/chapter.${ext}"
    "$HOME/ch02.${ext}"
    "$HOME/chapter.${ext}"
  )
  local c
  for c in "${candidates[@]}"; do
    if [[ -f "$c" ]]; then
      mv -f "$c" "$dest"
      # also move companion files dir if present
      if [[ -d "${c%.${ext}}_files" ]]; then
        rm -rf "$ROOT/preview/chapter_files"
        mv "${c%.${ext}}_files" "$ROOT/preview/chapter_files"
      fi
      echo "Collected $c -> $dest"
      return 0
    fi
  done
  return 1
}

if ! collect "$FORMAT"; then
  if [[ "$FORMAT" == "html" ]]; then
    echo "WARN: Quarto HTML not found; using fallback renderer"
    "$ROOT/.venv/bin/python" "$ROOT/scripts/render_preview.py"
  else
    echo "${FORMAT}: FAIL — could not locate rendered output"
    exit 1
  fi
fi

echo "Rendered $FORMAT into $ROOT/preview"
ls -la "$ROOT/preview"
