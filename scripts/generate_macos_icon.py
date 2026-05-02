from __future__ import annotations

from pathlib import Path

from PIL import Image
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer


ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "assets" / "codebarbuilder.svg"
PNG_PATH = ROOT / "build" / "icons" / "codebarbuilder-1024.png"
ICNS_PATH = ROOT / "build" / "icons" / "codebarbuilder.icns"

ICNS_SIZES = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)]


def main() -> None:
    ICNS_PATH.parent.mkdir(parents=True, exist_ok=True)
    renderer = QSvgRenderer(str(SVG_PATH))
    if not renderer.isValid():
        raise SystemExit(f"Invalid SVG icon: {SVG_PATH}")

    write_png(renderer, 1024, PNG_PATH)
    image = Image.open(PNG_PATH)
    image.save(ICNS_PATH, format="ICNS", sizes=ICNS_SIZES)
    print(f"Generated {ICNS_PATH}")


def write_png(renderer: QSvgRenderer, size: int, path: Path) -> None:
    image = QImage(QSize(size, size), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    image.save(str(path), "PNG")


if __name__ == "__main__":
    app = QGuiApplication([])
    main()
    app.quit()
