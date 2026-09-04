#!/usr/bin/env bash
# Render adult print geometry profiles to preview/print/ (does NOT replace review full31 PDF).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

discover_quarto() {
  if [[ -n "${QUARTO_BIN:-}" && -x "${QUARTO_BIN}" ]]; then echo "${QUARTO_BIN}"; return; fi
  if [[ -x "$ROOT/tools/quarto/bin/quarto" ]]; then echo "$ROOT/tools/quarto/bin/quarto"; return; fi
  if command -v quarto >/dev/null 2>&1; then command -v quarto; return; fi
  echo ""
}
discover_tex_bin() {
  if [[ -n "${TEXLIVE_BIN:-}" && -d "${TEXLIVE_BIN}" ]]; then echo "${TEXLIVE_BIN}"; return; fi
  local candidates=(
    "${HOME}/Library/TinyTeX/bin/universal-darwin"
    "${HOME}/Library/TinyTeX/bin/aarch64-darwin"
    "${HOME}/Library/TinyTeX/bin/x86_64-darwin"
  )
  local c
  for c in "${candidates[@]}"; do
    if [[ -x "${c}/xelatex" ]]; then echo "${c}"; return; fi
  done
  echo ""
}

QUARTO_BIN_RESOLVED="$(discover_quarto)"
TEX_BIN="$(discover_tex_bin)"
[[ -n "${TEX_BIN}" ]] && export PATH="${TEX_BIN}:${PATH}"
[[ -x "$ROOT/tools/quarto/bin/quarto" ]] && export PATH="$ROOT/tools/quarto/bin:${PATH}"
if [[ -z "${QUARTO_BIN_RESOLVED}" ]]; then
  echo "render_print_profiles: FAIL — Quarto not installed"; exit 1
fi
if ! command -v xelatex >/dev/null 2>&1; then
  echo "render_print_profiles: FAIL — xelatex missing"; exit 1
fi

OUT="$ROOT/preview/print"
mkdir -p "$OUT"
PROFILES=(print-6x9 print-7x10 print-85x11)

for profile in "${PROFILES[@]}"; do
  echo "=== Rendering profile ${profile} ==="
  rm -rf "$ROOT/_book"
  log="$OUT/${profile}.log"
  "${QUARTO_BIN_RESOLVED}" render "$ROOT" --to pdf --profile "${profile}" >"$log" 2>&1
  pdf="$ROOT/_book/The-Technology-Landscape.pdf"
  if [[ ! -f "${pdf}" ]]; then
    pdf="$(find "$ROOT/_book" -maxdepth 2 -name '*.pdf' -type f | head -1 || true)"
  fi
  if [[ -z "${pdf}" || ! -f "${pdf}" ]]; then
    echo "render_print_profiles: FAIL — no PDF for ${profile} (see ${log})"; exit 1
  fi
  dest="$OUT/technology-landscape-${profile}-interior.pdf"
  cp -f "$pdf" "$dest"
  echo "Wrote $dest"
done
echo "render_print_profiles: PASS"
