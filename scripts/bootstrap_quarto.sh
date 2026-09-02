#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/tools"
VER=1.7.32
URL="https://github.com/quarto-dev/quarto-cli/releases/download/v${VER}/quarto-${VER}-macos.tar.gz"
curl -L "$URL" -o "$ROOT/tools/quarto.tgz"
rm -rf "$ROOT/tools/quarto"
mkdir -p "$ROOT/tools/quarto"
tar -xzf "$ROOT/tools/quarto.tgz" -C "$ROOT/tools/quarto" --strip-components=1
"$ROOT/tools/quarto/bin/quarto" --version
