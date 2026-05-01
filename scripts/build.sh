#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")/.."

python3 -m PyInstaller packaging/codebarbuilder.spec --clean -y

echo "Build complete: dist/CodebarBuilder"
