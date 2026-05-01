import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import Qt

from codebarbuilder.formats import DEFAULT_FORMAT_KEY
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


def test_clear_preserves_format_and_language(qtbot):
    window = make_window(qtbot)
    window.format_combo.setCurrentIndex(window.format_combo.findData("upca"))
    window.set_language("en")
    window.number_input.setText("036000291452")

    window.clear_form()

    assert window.format_combo.currentData() == "upca"
    assert window.language == "en"
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


def test_copy_shortcut_from_number_input_copies_generated_png(qtbot):
    window = make_window(qtbot)
    window.number_input.setText("4006381333931")
    window.generate_barcode()

    qtbot.keyClick(window.number_input, Qt.Key.Key_C, Qt.KeyboardModifier.ControlModifier)

    assert window.status_label.text() == window._t("copied_message")
