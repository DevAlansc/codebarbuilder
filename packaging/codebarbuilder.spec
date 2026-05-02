# Build from the repository root with:
# pyinstaller packaging/codebarbuilder.spec --clean

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

ROOT = Path.cwd()
MAC_ICON = ROOT / "build" / "icons" / "codebarbuilder.icns"
datas = collect_data_files("barcode")
datas.extend(
    [
        (str(ROOT / "THIRD_PARTY_NOTICES.md"), "."),
        (str(ROOT / "assets" / "codebarbuilder.svg"), "assets"),
    ]
)

a = Analysis(
    [str(ROOT / "packaging" / "pyinstaller_entry.py")],
    pathex=[str(ROOT / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CodebarBuilder",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="CodebarBuilder",
)

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="CodebarBuilder.app",
        icon=str(MAC_ICON) if MAC_ICON.exists() else None,
        bundle_identifier="com.devalansc.codebarbuilder",
        info_plist={
            "CFBundleName": "Codebar builder",
            "CFBundleDisplayName": "Codebar builder",
            "CFBundleShortVersionString": "0.1.0",
            "CFBundleVersion": "0.1.0",
            "NSHighResolutionCapable": True,
        },
    )
