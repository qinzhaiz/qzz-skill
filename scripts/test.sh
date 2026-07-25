#!/usr/bin/env bash
# test.sh — lint + metadata
# Usage: ./scripts/test.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== qzz-skill test ==="

echo ""
echo "[1/2] Linting concepts..."
python "$ROOT/tools/lint.py"

echo ""
echo "[2/2] Validating metadata..."
python "$ROOT/tools/metadata.py"

echo ""
echo "=== All tests passed ==="
