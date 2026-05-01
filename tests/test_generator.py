import pytest

pytest.importorskip("barcode")
pytest.importorskip("PIL")

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
