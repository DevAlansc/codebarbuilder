from __future__ import annotations

import sys
from pathlib import Path


ASSET_DIR_NAME = "assets"
APP_ICON_FILENAME = "codebarbuilder.svg"


def resource_path(*parts: str) -> Path:
    frozen_root = getattr(sys, "_MEIPASS", None)
    if frozen_root:
        return Path(frozen_root).joinpath(*parts)
    return Path(__file__).resolve().parents[2].joinpath(*parts)


def app_icon_path() -> Path:
    return resource_path(ASSET_DIR_NAME, APP_ICON_FILENAME)
