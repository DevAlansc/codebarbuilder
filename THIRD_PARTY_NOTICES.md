# Third-party notices

This project uses third-party open source packages for runtime, packaging, and
testing. The information below reflects the package metadata verified during
development.

This document is provided for attribution and dependency visibility. It is not
legal advice.

## Runtime dependencies

| Package | Version verified | License | Project |
| --- | --- | --- | --- |
| PySide6 | 6.11.0 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only | https://pyside.org |
| shiboken6 | 6.11.0 | LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only | https://pyside.org |
| python-barcode | 0.16.1 | MIT | https://github.com/WhyNotHugo/python-barcode |
| Pillow | 12.1.0 | MIT-CMU | https://python-pillow.github.io |

PySide6 also installs Qt for Python support packages such as
`PySide6_Essentials` and `PySide6_Addons`, which follow the same Qt for Python
licensing model as PySide6.

## Build and development tooling

| Package | Version verified | License | Project |
| --- | --- | --- | --- |
| PyInstaller | 6.20.0 | GPLv2-or-later with special exception | https://pyinstaller.org |
| pytest | 9.0.3 | MIT | https://docs.pytest.org |
| pytest-qt | 4.5.0 | MIT | https://github.com/pytest-dev/pytest-qt |

Packaged application builds may include additional transitive dependencies from
these packages. Review the exact build environment before distributing release
artifacts.
