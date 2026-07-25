#!/usr/bin/env bash
# build.sh — lint + metadata + toc
# Usage: ./scripts/build.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== qzz-skill build ==="

echo ""
echo "[1/3] Linting concepts..."
python "$ROOT/tools/lint.py"

echo ""
echo "[2/3] Validating metadata..."
python "$ROOT/tools/metadata.py"

echo ""
echo "[3/3] Generating TOC..."
python "$ROOT/tools/toc.py" --output "$ROOT/skills/qzz-mysql/knowledge/TOC.md"

echo ""
echo "=== Build complete ==="
