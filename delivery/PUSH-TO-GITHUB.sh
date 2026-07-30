#!/bin/bash
# Usage:
#   1. Unzip PUSH-1D-MC-CLEANUP.zip
#   2. cd into your local 1-D-Fission-Reactor-MC clone
#   3. bash /path/to/unzipped/PUSH-TO-GITHUB.sh /path/to/unzipped
set -euo pipefail

SRC="${1:-}"
if [ -z "$SRC" ] || [ ! -f "$SRC/README.md" ] || [ ! -d "$SRC/fission1d" ]; then
  echo "Usage: bash PUSH-TO-GITHUB.sh /path/to/unzipped-cleanup-folder"
  echo "Run from inside your 1-D-Fission-Reactor-MC git clone."
  exit 1
fi
if [ ! -d .git ]; then
  echo "Error: run this from your 1-D-Fission-Reactor-MC repo root (must contain .git)."
  exit 1
fi

BRANCH="cursor/cleanup-project-structure-28d1"
git checkout -B "$BRANCH"
rsync -a --delete --exclude .git --exclude PUSH-TO-GITHUB.sh "$SRC"/ ./
git add -A
git status --short | head -40
git commit -m "Restructure repo into a clean package with docs and tooling"
git push -u origin "$BRANCH"
echo
echo "Opened branch $BRANCH. Create the PR here:"
echo "https://github.com/dannySchantz/1-D-Fission-Reactor-MC/compare/main...$BRANCH?expand=1"
