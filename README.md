# Codebar builder

Codebar builder is a cross-platform Python desktop application for generating
technical product barcodes. It validates and renders existing product numbers in
EAN-13, UPC-A, and EAN-8 formats.

The application does not issue official GS1 numbers. It only validates and
renders barcode numbers that you already own or manage.

## Features

- Generate EAN-13, UPC-A, and EAN-8 barcodes.
- Validate numeric input, exact length, and check digit.
- Preview the barcode before exporting it.
- Copy the generated barcode as a PNG image to the system clipboard.
- Save the generated barcode as PNG or SVG.
- Clear the current barcode while keeping the selected format.
- Switch the interface between Spanish and English from the language menu.
- View app metadata and third-party dependency notices from the Help menu.
- Use a custom barcode-style application icon.
- Package the app as a desktop binary with PyInstaller.

## Requirements

- Python 3.10 or newer.
- A desktop environment supported by Qt/PySide6.

## Development Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project with development dependencies:

```bash
pip install -e ".[dev]"
```

## Run the App

```bash
codebarbuilder
```

Alternatively:

```bash
python -m codebarbuilder
```

## Run Tests

```bash
pytest
```

In headless environments, run Qt tests with:

```bash
QT_QPA_PLATFORM=offscreen pytest
```

## Build a Desktop Binary

Install development dependencies first, then run:

On macOS or Linux:

```bash
sh scripts/build.sh
```

To create a macOS `.app` and `.dmg` on macOS:

```bash
sh scripts/build_macos_dmg.sh
```

On Windows:

```powershell
scripts\build.bat
```

This creates a portable PyInstaller app under `dist\CodebarBuilder`; it is not
an installer.

To create a Windows installer `.exe`, install Inno Setup 6 on Windows and run:

```powershell
scripts\build_windows_installer.bat
```

The installer output is:

```text
dist\installer\CodebarBuilder-Setup-0.1.0.exe
```

These scripts wrap the PyInstaller command:

```bash
pyinstaller packaging/codebarbuilder.spec --clean
```

The generated portable application will be placed under `dist/CodebarBuilder`.
The macOS DMG script also creates `dist/CodebarBuilder.app` and
`dist/CodebarBuilder.dmg`.

Expected outputs depend on the operating system:

- Windows: portable app folder from PyInstaller, or installer `.exe` with Inno Setup.
- macOS: app bundle or executable depending on the PyInstaller configuration.
- Linux: executable.

PyInstaller should normally be run on each target operating system. For example,
build the Windows binary on Windows, the macOS binary on macOS, and the Linux
binary on Linux.

## Supported Formats

| Format | Length | Notes |
| --- | ---: | --- |
| EAN-13 | 13 digits | Default format when the app starts. |
| UPC-A | 12 digits | Common in the United States and Canada. |
| EAN-8 | 8 digits | Compact product barcode format. |

In v1, the app expects the full number including the check digit. It validates
the check digit but does not auto-calculate or append it.
