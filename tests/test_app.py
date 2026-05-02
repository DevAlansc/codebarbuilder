import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication, QLabel, QTextEdit

from codebarbuilder.formats import DEFAULT_FORMAT_KEY
from codebarbuilder.metadata import APP_AUTHOR, APP_LICENSE, APP_NAME, APP_VERSION
from codebarbuilder.translations import DEFAULT_LANGUAGE
from codebarbuilder.app import MainWindow


def make_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    window.activateWindow()
    window.number_input.setFocus()
    return window


def test_main_window_defaults(qtbot):
    window = make_window(qtbot)

    assert window.format_combo.currentData() == DEFAULT_FORMAT_KEY
    assert window.language == DEFAULT_LANGUAGE
    assert window.windowTitle() == "Codebar builder"
    assert not window.windowIcon().isNull()


def test_application_uses_light_palette(qtbot):
    make_window(qtbot)
    app = QApplication.instance()
    palette = app.palette()

    assert app.style().objectName().lower() == "fusion"
    assert palette.color(QPalette.ColorRole.Base).lightness() > 240
    assert palette.color(QPalette.ColorRole.Text).lightness() < 80


def test_clear_preserves_format_and_language(qtbot):
    window = make_window(qtbot)
    window.format_combo.setCurrentIndex(window.format_combo.findData("upca"))
    window.set_language("en")
    window.width_slider.setValue(150)
    window.height_slider.setValue(75)
    window.number_input.setText("036000291452")

    window.clear_form()

    assert window.format_combo.currentData() == "upca"
    assert window.language == "en"
    assert window.width_slider.value() == 150
    assert window.height_slider.value() == 75
    assert window.number_input.text() == ""


def test_escape_shortcut_clears_and_refocuses_number_input(qtbot):
    window = make_window(qtbot)
    window.number_input.setText("4006381333931")

    qtbot.keyClick(window.number_input, Qt.Key.Key_Escape)

    assert window.number_input.text() == ""


def test_generate_refocuses_number_input(qtbot):
    window = make_window(qtbot)
    window.number_input.setText("4006381333931")

    window.generate_barcode()

    assert window.current_png is not None


def test_geometry_sliders_update_labels_and_regenerate_current_barcode(qtbot):
    window = make_window(qtbot)
    window.number_input.setText("4006381333931")
    window.generate_barcode()
    original_png = window.current_png

    window.width_slider.setValue(150)
    window.height_slider.setValue(75)

    assert window.width_value_label.text() == "150%"
    assert window.height_value_label.text() == "75%"
    assert window.current_png is not None
    assert window.current_png != original_png


def test_copy_shortcut_from_number_input_copies_generated_png(qtbot):
    window = make_window(qtbot)
    window.number_input.setText("4006381333931")
    window.generate_barcode()

    qtbot.keyClick(window.number_input, Qt.Key.Key_C, Qt.KeyboardModifier.ControlModifier)

    assert window.status_label.text() == window._t("copied_message")


def test_help_menu_actions_exist_and_translate(qtbot):
    window = make_window(qtbot)

    assert window.help_menu.title() == "Ayuda"
    assert window.about_action.text() == "Acerca de Codebar builder"
    assert window.third_party_action.text() == "Avisos de terceros"

    window.set_language("en")

    assert window.help_menu.title() == "Help"
    assert window.about_action.text() == "About Codebar builder"
    assert window.third_party_action.text() == "Third-party notices"


def test_about_action_opens_dialog_with_app_metadata(qtbot):
    window = make_window(qtbot)

    window.about_action.trigger()

    assert window.about_dialog is not None
    assert window.about_dialog.windowTitle() == "Acerca de Codebar builder"
    labels = window.about_dialog.findChildren(QLabel)
    text = "\n".join(label.text() for label in labels)
    assert APP_NAME in text
    assert APP_VERSION in text
    assert APP_AUTHOR in text
    assert APP_LICENSE in text


def test_third_party_action_opens_dialog_with_notices(qtbot):
    window = make_window(qtbot)

    window.third_party_action.trigger()

    assert window.third_party_dialog is not None
    text_edits = window.third_party_dialog.findChildren(QTextEdit)
    assert len(text_edits) == 1
    assert "PySide6" in text_edits[0].toPlainText()
    assert "python-barcode" in text_edits[0].toPlainText()
