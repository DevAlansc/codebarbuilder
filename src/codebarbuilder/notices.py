from __future__ import annotations

import sys
from pathlib import Path


NOTICE_FILENAME = "THIRD_PARTY_NOTICES.md"
FALLBACK_NOTICES = (
    "Third-party notices could not be loaded. "
    "See THIRD_PARTY_NOTICES.md in the project repository."
)


def load_third_party_notices() -> str:
    for path in _candidate_notice_paths():
        if path.exists():
            return path.read_text(encoding="utf-8")
    return FALLBACK_NOTICES


def _candidate_notice_paths() -> list[Path]:
    paths: list[Path] = []
    frozen_root = getattr(sys, "_MEIPASS", None)
    if frozen_root:
        paths.append(Path(frozen_root) / NOTICE_FILENAME)
    paths.append(Path(__file__).resolve().parents[2] / NOTICE_FILENAME)
    paths.append(Path.cwd() / NOTICE_FILENAME)
    return paths
