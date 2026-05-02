#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")/.."

if [ "$(uname)" != "Darwin" ]; then
  echo "This script can only create a macOS .dmg on macOS." >&2
  exit 1
fi

python3 scripts/generate_macos_icon.py
python3 -m PyInstaller packaging/codebarbuilder.spec --clean -y

rm -rf dist/dmg
mkdir -p dist/dmg
cp -R dist/CodebarBuilder.app dist/dmg/
ln -s /Applications dist/dmg/Applications

hdiutil create \
  -volname "CodebarBuilder" \
  -srcfolder dist/dmg \
  -ov \
  -format UDZO \
  dist/CodebarBuilder.dmg

echo "Build complete: dist/CodebarBuilder.dmg"
