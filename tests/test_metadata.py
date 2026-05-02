from importlib.metadata import metadata, version

from codebarbuilder.metadata import APP_AUTHOR, APP_LICENSE, APP_NAME, APP_VERSION
from codebarbuilder.notices import load_third_party_notices


def test_app_metadata_matches_project_metadata():
    project_metadata = metadata("codebarbuilder")

    assert APP_NAME == "Codebar builder"
    assert APP_VERSION == version("codebarbuilder")
    assert APP_AUTHOR == project_metadata["Author"]
    assert APP_LICENSE == project_metadata["License"]


def test_third_party_notices_load_expected_dependency_names():
    notices = load_third_party_notices()

    assert "PySide6" in notices
    assert "python-barcode" in notices
    assert "Pillow" in notices
    assert "PyInstaller" in notices
