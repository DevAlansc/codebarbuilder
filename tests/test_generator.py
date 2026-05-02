import pytest

pytest.importorskip("barcode")
pytest.importorskip("PIL")

from io import BytesIO

from PIL import Image

from codebarbuilder.generator import render_png, render_svg


@pytest.mark.parametrize(
    ("value", "format_key"),
    [
        ("4006381333931", "ean13"),
        ("036000291452", "upca"),
        ("96385074", "ean8"),
    ],
)
def test_render_png_returns_image_bytes(value, format_key):
    png = render_png(value, format_key)

    assert png.startswith(b"\x89PNG")
    assert len(png) > 100


@pytest.mark.parametrize(
    ("value", "format_key"),
    [
        ("4006381333931", "ean13"),
        ("036000291452", "upca"),
        ("96385074", "ean8"),
    ],
)
def test_render_svg_returns_svg_bytes(value, format_key):
    svg = render_svg(value, format_key)

    assert b"<svg" in svg
    assert b"</svg>" in svg


def test_render_rejects_invalid_code():
    with pytest.raises(ValueError):
        render_png("4006381333932", "ean13")


def test_width_scale_changes_width_more_than_height():
    narrow = Image.open(BytesIO(render_png("4006381333931", "ean13", width_scale=0.5)))
    wide = Image.open(BytesIO(render_png("4006381333931", "ean13", width_scale=2.0)))

    assert narrow.width < wide.width
    assert abs(narrow.height - wide.height) <= 2


def test_height_scale_changes_height_more_than_width():
    flat = Image.open(BytesIO(render_png("4006381333931", "ean13", height_scale=0.5)))
    tall = Image.open(BytesIO(render_png("4006381333931", "ean13", height_scale=2.0)))

    assert flat.height < tall.height
    assert abs(flat.width - tall.width) <= 2


def test_render_rejects_out_of_range_geometry_scale():
    with pytest.raises(ValueError):
        render_png("4006381333931", "ean13", width_scale=0.25)
