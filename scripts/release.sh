#!/usr/bin/env bash
# release.sh — build + git tag + push
# Usage: ./scripts/release.sh 1.0.0
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="${1:-}"

echo "=== qzz-skill release ==="

echo ""
echo "[1/3] Running build..."
bash "$ROOT/scripts/build.sh"

echo ""
echo "[2/3] Checking git status..."
cd "$ROOT"
if [ -n "$(git status --porcelain)" ]; then
    echo "Working tree is not clean. Commit or stash changes before release."
    git status --short
    exit 1
fi

if [ -z "$VERSION" ]; then
    echo ""
    echo "[3/3] No version specified. Dry-run complete."
    echo "To release: ./scripts/release.sh x.y.z"
    exit 0
fi

echo ""
echo "[3/3] Creating tag v$VERSION..."
git tag "v$VERSION"
git push origin "v$VERSION"

echo ""
echo "=== Released v$VERSION ==="
