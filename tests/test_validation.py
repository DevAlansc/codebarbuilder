import pytest

from codebarbuilder.validation import calculate_check_digit, validate_barcode_value


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ("400638133393", "1"),
        ("03600029145", "2"),
        ("9638507", "4"),
    ],
)
def test_calculate_check_digit(payload, expected):
    assert calculate_check_digit(payload) == expected


@pytest.mark.parametrize(
    ("value", "format_key"),
    [
        ("4006381333931", "ean13"),
        ("036000291452", "upca"),
        ("96385074", "ean8"),
    ],
)
def test_valid_codes(value, format_key):
    result = validate_barcode_value(value, format_key)

    assert result.is_valid is True
    assert result.message_key == "validation_ok"


@pytest.mark.parametrize(
    ("value", "format_key"),
    [
        ("4006381333932", "ean13"),
        ("036000291453", "upca"),
        ("96385075", "ean8"),
    ],
)
def test_invalid_check_digits(value, format_key):
    result = validate_barcode_value(value, format_key)

    assert result.is_valid is False
    assert result.message_key == "validation_checksum"


@pytest.mark.parametrize(
    ("value", "format_key", "message_key"),
    [
        ("", "ean13", "validation_empty"),
        ("40063813339A1", "ean13", "validation_digits"),
        ("400638133393", "ean13", "validation_length"),
        ("03600029145", "upca", "validation_length"),
        ("9638507", "ean8", "validation_length"),
    ],
)
def test_invalid_input_shape(value, format_key, message_key):
    result = validate_barcode_value(value, format_key)

    assert result.is_valid is False
    assert result.message_key == message_key


def test_unsupported_format_raises():
    with pytest.raises(ValueError):
        validate_barcode_value("4006381333931", "qr")
