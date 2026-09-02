#!/usr/bin/env bash
# Assemble Gate 3 reader-preview package into docs/ and hash artifacts.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
DOCS="$ROOT/docs"
SNAP="$ROOT/publication/gates/gate-3/REVIEW_SNAPSHOT.yaml"

mkdir -p "$DOCS/chapter" "$DOCS/figures" "$DOCS/lab/browser" "$DOCS/lab/fixtures" "$DOCS/forms"

# Prefer freshly rendered chapter formats when tooling is available.
if [[ "${SKIP_RENDER:-0}" != "1" ]]; then
  if [[ -x "$ROOT/scripts/render_formats.sh" ]]; then
    chmod +x "$ROOT/scripts/render_formats.sh"
    ./scripts/render_formats.sh html || true
    ./scripts/render_formats.sh epub || true
    ./scripts/render_formats.sh pdf || true
  fi
fi

copy_if() {
  local src="$1" dest="$2"
  if [[ -f "$src" ]]; then
    cp -f "$src" "$dest"
    echo "copied $(basename "$src") -> $dest"
  else
    echo "WARN: missing $src"
  fi
}

copy_if "$ROOT/preview/ch02.html" "$DOCS/chapter/ch02.html"
copy_if "$ROOT/preview/ch02.pdf" "$DOCS/chapter/ch02.pdf"
copy_if "$ROOT/preview/ch02.epub" "$DOCS/chapter/ch02.epub"

# Figures (canonical published paths)
cp -f "$ROOT/figures/ecosystem/fig-ch02-001-human-to-system.svg" "$DOCS/figures/"
cp -f "$ROOT/figures/sequence/fig-ch02-002-cross-layer-sequence.svg" "$DOCS/figures/"
cp -f "$ROOT/figures/exploded-views/fig-ch02-003-device-exploded.svg" "$DOCS/figures/"
cp -f "$ROOT/figures/architecture/fig-ch02-004-software-stack.svg" "$DOCS/figures/"
cp -f "$ROOT/figures/ecosystem/fig-ch02-005-local-vs-network.svg" "$DOCS/figures/"
cp -f "$ROOT/figures/architecture/fig-ch02-006-latency-budget.svg" "$DOCS/figures/"
cp -f "$ROOT/figures/architecture/fig-ch02-007-stability-contract.svg" "$DOCS/figures/"

# Simple figures index
cat > "$DOCS/figures/index.html" <<'EOF'
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>CH02 Figures</title>
<style>body{font-family:system-ui,sans-serif;margin:2rem;max-width:48rem;line-height:1.45}
img{max-width:100%;border:1px solid #ccc;margin:1rem 0}</style></head>
<body>
<h1>Chapter 2 figures (CH02-REVIEW-R1)</h1>
<p><a href="../index.html">Back to landing page</a></p>
<figure><figcaption>FIG-CH02-001</figcaption><img src="fig-ch02-001-human-to-system.svg" alt="Human-to-system overview"/></figure>
<figure><figcaption>FIG-CH02-002</figcaption><img src="fig-ch02-002-cross-layer-sequence.svg" alt="Cross-layer sequence"/></figure>
<figure><figcaption>FIG-CH02-003</figcaption><img src="fig-ch02-003-device-exploded.svg" alt="Device exploded view"/></figure>
<figure><figcaption>FIG-CH02-004</figcaption><img src="fig-ch02-004-software-stack.svg" alt="Software stack"/></figure>
<figure><figcaption>FIG-CH02-005</figcaption><img src="fig-ch02-005-local-vs-network.svg" alt="Local vs network"/></figure>
<figure><figcaption>FIG-CH02-006</figcaption><img src="fig-ch02-006-latency-budget.svg" alt="Latency budget"/></figure>
<figure><figcaption>FIG-CH02-007</figcaption><img src="fig-ch02-007-stability-contract.svg" alt="Stability Contract"/></figure>
</body></html>
EOF

# Lab routes
cp -f "$ROOT/labs/LAB-TAP-001/browser/index.html" "$DOCS/lab/browser/index.html"
cp -f "$ROOT/labs/LAB-TAP-001/fixtures/sample_observation.md" "$DOCS/lab/fixtures/"
cp -f "$ROOT/labs/LAB-TAP-001/fixtures/sample_result_table.csv" "$DOCS/lab/fixtures/"
cp -f "$ROOT/labs/LAB-TAP-001/README.md" "$DOCS/lab/README.md"

# Forms + packet
cp -f "$ROOT/reader-preview/forms/"*.md "$DOCS/forms/"
cp -f "$ROOT/publication/gates/gate-3/CH02_READER_REVIEW_PACKET.md" "$DOCS/forms/packet.md"
cp -f "$ROOT/publication/gates/gate-3/REVIEW_PROTOCOL.md" "$DOCS/REVIEW_PROTOCOL.md"

# Landing + instructions are authored under docs/; ensure present
[[ -f "$DOCS/index.html" ]] || { echo "FAIL: docs/index.html missing"; exit 1; }
[[ -f "$DOCS/instructions.md" ]] || { echo "FAIL: docs/instructions.md missing"; exit 1; }

sha256_file() {
  local f="$1"
  if [[ -f "$f" ]]; then
    if command -v shasum >/dev/null 2>&1; then
      shasum -a 256 "$f" | awk '{print $1}'
    else
      sha256sum "$f" | awk '{print $1}'
    fi
  else
    echo ""
  fi
}

HTML_HASH="$(sha256_file "$DOCS/chapter/ch02.html")"
PDF_HASH="$(sha256_file "$DOCS/chapter/ch02.pdf")"
EPUB_HASH="$(sha256_file "$DOCS/chapter/ch02.epub")"
F1="$(sha256_file "$DOCS/figures/fig-ch02-001-human-to-system.svg")"
F2="$(sha256_file "$DOCS/figures/fig-ch02-002-cross-layer-sequence.svg")"
F3="$(sha256_file "$DOCS/figures/fig-ch02-003-device-exploded.svg")"
F4="$(sha256_file "$DOCS/figures/fig-ch02-004-software-stack.svg")"
F5="$(sha256_file "$DOCS/figures/fig-ch02-005-local-vs-network.svg")"
F6="$(sha256_file "$DOCS/figures/fig-ch02-006-latency-budget.svg")"
F7="$(sha256_file "$DOCS/figures/fig-ch02-007-stability-contract.svg")"

"$ROOT/.venv/bin/python" - <<PY
from pathlib import Path
import yaml
snap_path = Path(r"""$SNAP""")
data = yaml.safe_load(snap_path.read_text(encoding="utf-8"))
hashes = data.setdefault("artifacts", {}).setdefault("hashes", {})
hashes["html"] = """$HTML_HASH"""
hashes["pdf"] = """$PDF_HASH"""
hashes["epub"] = """$EPUB_HASH"""
hashes["fig-ch02-001"] = """$F1"""
hashes["fig-ch02-002"] = """$F2"""
hashes["fig-ch02-003"] = """$F3"""
hashes["fig-ch02-004"] = """$F4"""
hashes["fig-ch02-005"] = """$F5"""
hashes["fig-ch02-006"] = """$F6"""
hashes["fig-ch02-007"] = """$F7"""
snap_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
print("Updated REVIEW_SNAPSHOT.yaml hashes")
PY

# Manifest for artifact consumers
"$ROOT/.venv/bin/python" - <<PY
import json, hashlib
from pathlib import Path
root = Path(r"""$DOCS""")
items = {}
for p in sorted(root.rglob("*")):
    if p.is_file() and p.name != "MANIFEST.json":
        rel = str(p.relative_to(root)).replace("\\\\", "/")
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        items[rel] = {"sha256": h, "bytes": p.stat().st_size}
Path(r"""$DOCS/MANIFEST.json""").write_text(json.dumps({
    "review_id": "CH02-REVIEW-R1",
    "source_commit": "a2a4af2f5e1002852933a1b50c24f65b3a3c4651",
    "files": items,
}, indent=2) + "\n", encoding="utf-8")
print(f"Wrote MANIFEST.json with {len(items)} files")
PY

echo "reader-preview package ready under docs/"
ls -la "$DOCS/chapter" "$DOCS/figures" "$DOCS/lab/browser" "$DOCS/forms" | head -80
