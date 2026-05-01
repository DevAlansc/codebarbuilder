from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BarcodeFormat:
    key: str
    label: str
    length: int
    library_name: str


FORMATS: dict[str, BarcodeFormat] = {
    "ean13": BarcodeFormat("ean13", "EAN-13", 13, "ean13"),
    "upca": BarcodeFormat("upca", "UPC-A", 12, "upca"),
    "ean8": BarcodeFormat("ean8", "EAN-8", 8, "ean8"),
}

DEFAULT_FORMAT_KEY = "ean13"
