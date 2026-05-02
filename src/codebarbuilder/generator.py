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

MIN_GEOMETRY_SCALE = 0.5
MAX_GEOMETRY_SCALE = 2.0


def render_png(
    value: str,
    format_key: str,
    width_scale: float = 1.0,
    height_scale: float = 1.0,
) -> bytes:
    _validate_or_raise(value, format_key)
    barcode_instance = _create_barcode(value, format_key, ImageWriter())
    output = BytesIO()
    barcode_instance.write(output, options=_writer_options(width_scale, height_scale))
    return output.getvalue()


def render_svg(
    value: str,
    format_key: str,
    width_scale: float = 1.0,
    height_scale: float = 1.0,
) -> bytes:
    _validate_or_raise(value, format_key)
    barcode_instance = _create_barcode(value, format_key, SVGWriter())
    output = BytesIO()
    barcode_instance.write(output, options=_writer_options(width_scale, height_scale))
    return output.getvalue()


def _writer_options(width_scale: float, height_scale: float) -> dict[str, float | int | bool]:
    _validate_scale(width_scale)
    _validate_scale(height_scale)
    options = dict(WRITER_OPTIONS)
    options["module_width"] = WRITER_OPTIONS["module_width"] * width_scale
    options["module_height"] = WRITER_OPTIONS["module_height"] * height_scale
    return options


def _validate_scale(scale: float) -> None:
    if scale < MIN_GEOMETRY_SCALE or scale > MAX_GEOMETRY_SCALE:
        raise ValueError(
            f"Scale must be between {MIN_GEOMETRY_SCALE} and {MAX_GEOMETRY_SCALE}"
        )


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
