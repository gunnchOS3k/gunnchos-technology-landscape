#!/usr/bin/env bash
# Render the full 31-chapter book project (root `_quarto.yml`) into named full31 artifacts.
# Does NOT touch CH02 reader-package outputs under preview/ch02.* or docs/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FORMAT="${1:?format required: html|pdf|epub|all}"

ARTIFACT_ROOT="$ROOT/preview/full31"
HTML_NAME="technology-landscape-full31-html"
PDF_NAME="technology-landscape-full31-pdf.pdf"
EPUB_NAME="technology-landscape-full31-epub.epub"
# Also accept directory-style names without extension for packaging docs.
PDF_DIR_NAME="technology-landscape-full31-pdf"
EPUB_DIR_NAME="technology-landscape-full31-epub"

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

if [[ -z "${QUARTO_BIN_RESOLVED}" ]]; then
  echo "full31 ${FORMAT}: FAIL — Quarto not installed. Set QUARTO_BIN or run scripts/bootstrap_quarto.sh"
  exit 1
fi

mkdir -p "$ARTIFACT_ROOT"

render_html() {
  local tmp="$ROOT/_book"
  rm -rf "$tmp"
  "${QUARTO_BIN_RESOLVED}" render "$ROOT" --to html
  rm -rf "$ARTIFACT_ROOT/$HTML_NAME"
  mkdir -p "$ARTIFACT_ROOT"
  mv "$tmp" "$ARTIFACT_ROOT/$HTML_NAME"
  echo "Wrote $ARTIFACT_ROOT/$HTML_NAME/"
}

render_pdf() {
  if ! command -v xelatex >/dev/null 2>&1; then
    echo "full31 pdf: FAIL — TeX engine (xelatex) not installed. export TEXLIVE_BIN=... or install TinyTeX"
    exit 1
  fi
  if ! command -v rsvg-convert >/dev/null 2>&1 && ! command -v inkscape >/dev/null 2>&1; then
    echo "full31 pdf: FAIL — SVG→PDF converter missing (rsvg-convert or inkscape)."
    exit 1
  fi
  local tmp="$ROOT/_book"
  rm -rf "$tmp"
  "${QUARTO_BIN_RESOLVED}" render "$ROOT" --to pdf
  mkdir -p "$ARTIFACT_ROOT/$PDF_DIR_NAME"
  # Quarto book PDF typically lands as _book/*.pdf
  local pdf
  pdf="$(find "$tmp" -maxdepth 2 -type f -name '*.pdf' | head -n 1 || true)"
  if [[ -z "$pdf" ]]; then
    echo "full31 pdf: FAIL — no PDF under $tmp"
    ls -la "$tmp" || true
    exit 1
  fi
  cp -f "$pdf" "$ARTIFACT_ROOT/$PDF_NAME"
  cp -f "$pdf" "$ARTIFACT_ROOT/$PDF_DIR_NAME/technology-landscape-full31.pdf"
  echo "Wrote $ARTIFACT_ROOT/$PDF_NAME"
}

render_epub() {
  local tmp="$ROOT/_book"
  rm -rf "$tmp"
  "${QUARTO_BIN_RESOLVED}" render "$ROOT" --to epub
  mkdir -p "$ARTIFACT_ROOT/$EPUB_DIR_NAME"
  local epub
  epub="$(find "$tmp" -maxdepth 2 -type f -name '*.epub' | head -n 1 || true)"
  if [[ -z "$epub" ]]; then
    echo "full31 epub: FAIL — no EPUB under $tmp"
    ls -la "$tmp" || true
    exit 1
  fi
  cp -f "$epub" "$ARTIFACT_ROOT/$EPUB_NAME"
  cp -f "$epub" "$ARTIFACT_ROOT/$EPUB_DIR_NAME/technology-landscape-full31.epub"
  echo "Wrote $ARTIFACT_ROOT/$EPUB_NAME"
}

case "$FORMAT" in
  html) render_html ;;
  pdf) render_pdf ;;
  epub) render_epub ;;
  all)
    render_html
    render_epub
    render_pdf
    ;;
  *)
    echo "Unknown format: $FORMAT (use html|pdf|epub|all)"; exit 1
    ;;
esac

# Safety: never overwrite CH02 reader package outputs
if [[ -f "$ROOT/preview/ch02.html" || -f "$ROOT/preview/ch02.pdf" || -f "$ROOT/preview/ch02.epub" ]]; then
  echo "Note: CH02 reader-package artifacts under preview/ch02.* left untouched."
fi
echo "full31 ${FORMAT}: OK"
ls -la "$ARTIFACT_ROOT" | head -40
