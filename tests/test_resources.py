from codebarbuilder.resources import app_icon_path


def test_app_icon_asset_exists():
    icon_path = app_icon_path()

    assert icon_path.exists()
    assert icon_path.suffix == ".svg"
    assert "barcode" in icon_path.read_text(encoding="utf-8").lower()
