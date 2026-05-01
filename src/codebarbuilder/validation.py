from __future__ import annotations

from dataclasses import dataclass

from .formats import FORMATS, BarcodeFormat


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    message_key: str
    expected_check_digit: str | None = None


def calculate_check_digit(payload: str) -> str:
    """Calculate the GS1-style modulo-10 check digit for EAN/UPC payloads."""
    total = 0
    reversed_digits = reversed([int(digit) for digit in payload])
    for index, digit in enumerate(reversed_digits):
        weight = 3 if index % 2 == 0 else 1
        total += digit * weight
    return str((10 - (total % 10)) % 10)


def validate_barcode_value(value: str, format_key: str) -> ValidationResult:
    barcode_format = _get_format(format_key)
    normalized = value.strip()

    if not normalized:
        return ValidationResult(False, "validation_empty")

    if not normalized.isdigit():
        return ValidationResult(False, "validation_digits")

    if len(normalized) != barcode_format.length:
        return ValidationResult(
            False,
            "validation_length",
            expected_check_digit=None,
        )

    payload = normalized[:-1]
    expected_check_digit = calculate_check_digit(payload)
    actual_check_digit = normalized[-1]
    if actual_check_digit != expected_check_digit:
        return ValidationResult(
            False,
            "validation_checksum",
            expected_check_digit=expected_check_digit,
        )

    return ValidationResult(True, "validation_ok", expected_check_digit)


def _get_format(format_key: str) -> BarcodeFormat:
    try:
        return FORMATS[format_key]
    except KeyError as exc:
        raise ValueError(f"Unsupported barcode format: {format_key}") from exc
