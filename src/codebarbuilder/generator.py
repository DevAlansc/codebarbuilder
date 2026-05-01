from __future__ import annotations

from io import BytesIO

import barcode
from barcode.writer import ImageWriter, SVGWriter

from .formats import FORMATS
from .validation import validate_barcode_value


WRITER_OPTIONS = {
    "module_width": 0.28,
    "module_height": 18.0,
    "quiet_zone": 6.5,
    "font_size": 10,
    "text_distance": 4.0,
    "write_text": True,
}


def render_png(value: str, format_key: str) -> bytes:
    _validate_or_raise(value, format_key)
    barcode_instance = _create_barcode(value, format_key, ImageWriter())
    output = BytesIO()
    barcode_instance.write(output, options=WRITER_OPTIONS)
    return output.getvalue()


def render_svg(value: str, format_key: str) -> bytes:
    _validate_or_raise(value, format_key)
    barcode_instance = _create_barcode(value, format_key, SVGWriter())
    output = BytesIO()
    barcode_instance.write(output, options=WRITER_OPTIONS)
    return output.getvalue()


def _create_barcode(value: str, format_key: str, writer):
    barcode_format = FORMATS[format_key]
    barcode_class = barcode.get_barcode_class(barcode_format.library_name)
    if format_key == "upca":
        return barcode_class(value, writer=writer, make_ean=False)
    return barcode_class(value, writer=writer)


def _validate_or_raise(value: str, format_key: str) -> None:
    result = validate_barcode_value(value, format_key)
    if not result.is_valid:
        raise ValueError(result.message_key)
