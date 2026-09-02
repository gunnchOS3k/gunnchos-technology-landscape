#!/usr/bin/env bash
# Render Chapter 2 formats into ./preview using the chapter-local Quarto
# project at book/chapters/ch02/. Never renames or moves the root book
# project `_quarto.yml`.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FORMAT="${1:?format required: html|pdf|epub|book}"
CHAPTER_PROJECT="$ROOT/book/chapters/ch02"

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

if [[ "$FORMAT" == "pdf" || "$FORMAT" == "book" ]]; then
  if ! command -v xelatex >/dev/null 2>&1; then
    echo "pdf: FAIL — TeX engine (xelatex) not installed. export TEXLIVE_BIN=... or install TinyTeX"
    exit 1
  fi
fi

if [[ "$FORMAT" == "pdf" ]]; then
  if ! command -v rsvg-convert >/dev/null 2>&1 && ! command -v inkscape >/dev/null 2>&1; then
    echo "pdf: FAIL — SVG→PDF converter missing (rsvg-convert or inkscape)."
    echo "      macOS: brew install librsvg    Linux: apt-get install librsvg2-bin"
    exit 1
  fi
fi

# Deterministic chapter outputs under preview/ch02.{ext}
normalize_chapter_output() {
  local ext="$1"
  local dest="$ROOT/preview/ch02.${ext}"
  local candidates=(
    "$ROOT/preview/chapter.${ext}"
    "$ROOT/preview/ch02.${ext}"
  )
  local c
  for c in "${candidates[@]}"; do
    if [[ -f "$c" ]]; then
      if [[ "$c" != "$dest" ]]; then
        mv -f "$c" "$dest"
      fi
      local files_dir="${c%.${ext}}_files"
      if [[ -d "$files_dir" ]]; then
        rm -rf "$ROOT/preview/chapter_files" "$ROOT/preview/ch02_files"
        mv "$files_dir" "$ROOT/preview/ch02_files"
      fi
      echo "Normalized $c -> $dest"
      return 0
    fi
  done
  return 1
}

case "$FORMAT" in
  html|pdf|epub)
    # Chapter-local project — root `_quarto.yml` stays untouched.
    "${QUARTO_BIN_RESOLVED}" render "$CHAPTER_PROJECT" --to "$FORMAT"
    if ! normalize_chapter_output "$FORMAT"; then
      if [[ "$FORMAT" == "html" ]]; then
        echo "WARN: Quarto HTML not found in preview/; using fallback renderer"
        "$ROOT/.venv/bin/python" "$ROOT/scripts/render_preview.py"
      else
        echo "${FORMAT}: FAIL — expected output missing under preview/"
        ls -la "$ROOT/preview" || true
        exit 1
      fi
    fi
    ;;
  book)
    # Full book project from canonical root `_quarto.yml` → `_book/`
    "${QUARTO_BIN_RESOLVED}" render "$ROOT"
    echo "Rendered book project into $ROOT/_book"
    ;;
  *)
    echo "Unknown format: $FORMAT"; exit 1
    ;;
esac

echo "Rendered $FORMAT"
ls -la "$ROOT/preview" 2>/dev/null || true
