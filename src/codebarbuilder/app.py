from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .formats import DEFAULT_FORMAT_KEY, FORMATS
from .generator import render_png, render_svg
from .translations import DEFAULT_LANGUAGE, LANGUAGES, translate
from .validation import validate_barcode_value


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.language = DEFAULT_LANGUAGE
        self.current_png: bytes | None = None
        self.current_svg: bytes | None = None

        self.format_combo = QComboBox()
        for barcode_format in FORMATS.values():
            self.format_combo.addItem(barcode_format.label, barcode_format.key)
        self.format_combo.setCurrentIndex(self.format_combo.findData(DEFAULT_FORMAT_KEY))

        self.number_input = QLineEdit()
        self.number_input.returnPressed.connect(self.generate_barcode)
        self.number_input.installEventFilter(self)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setObjectName("statusLabel")

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(420, 210)
        self.preview_label.setObjectName("previewLabel")

        self.generate_button = QPushButton()
        self.generate_button.clicked.connect(self.generate_barcode)
        self.copy_png_button = QPushButton()
        self.copy_png_button.clicked.connect(self.copy_png)
        self.save_png_button = QPushButton()
        self.save_png_button.clicked.connect(self.save_png)
        self.save_svg_button = QPushButton()
        self.save_svg_button.clicked.connect(self.save_svg)
        self.clear_button = QPushButton()
        self.clear_button.clicked.connect(self.clear_form)

        self.format_label = QLabel()
        self.number_label = QLabel()

        self.language_actions: dict[str, QAction] = {}

        self._build_ui()
        self._build_menu()
        self._build_shortcuts()
        self._apply_styles()
        self.apply_language()
        self._set_export_enabled(False)
        self._focus_number_input()

    def _build_ui(self) -> None:
        self.generate_button.setObjectName("primaryButton")
        self.clear_button.setObjectName("quietButton")

        format_layout = QVBoxLayout()
        format_layout.setSpacing(6)
        format_layout.addWidget(self.format_label)
        format_layout.addWidget(self.format_combo)

        number_layout = QVBoxLayout()
        number_layout.setSpacing(6)
        number_layout.addWidget(self.number_label)
        number_layout.addWidget(self.number_input)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        input_layout.addLayout(format_layout, stretch=1)
        input_layout.addLayout(number_layout, stretch=3)
        input_layout.addWidget(self.generate_button, alignment=Qt.AlignmentFlag.AlignBottom)

        export_layout = QHBoxLayout()
        export_layout.setSpacing(10)
        export_layout.addWidget(self.copy_png_button)
        export_layout.addWidget(self.save_png_button)
        export_layout.addWidget(self.save_svg_button)
        export_layout.addStretch(1)
        export_layout.addWidget(self.clear_button)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(16)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.preview_label, stretch=1)
        main_layout.addLayout(export_layout)

        container = QWidget()
        container.setObjectName("appContainer")
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.resize(780, 500)

    def _build_menu(self) -> None:
        self.language_menu = self.menuBar().addMenu("")
        language_group = None
        for language_key, language_label in LANGUAGES.items():
            action = QAction(language_label, self)
            action.setCheckable(True)
            action.triggered.connect(
                lambda checked=False, key=language_key: self.set_language(key)
            )
            if language_group is None:
                from PySide6.QtGui import QActionGroup

                language_group = QActionGroup(self)
                language_group.setExclusive(True)
            language_group.addAction(action)
            self.language_menu.addAction(action)
            self.language_actions[language_key] = action

    def _build_shortcuts(self) -> None:
        self.copy_shortcut = QShortcut(QKeySequence.StandardKey.Copy, self)
        self.copy_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.copy_shortcut.activated.connect(self.copy_png)

        self.clear_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.clear_shortcut.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.clear_shortcut.activated.connect(self.clear_form)

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background: #eef1f5;
            }
            QWidget#appContainer {
                background: #eef1f5;
            }
            QLabel {
                color: #17202a;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                min-height: 38px;
                padding: 5px 10px;
                font-size: 14px;
                background: #ffffff;
                border: 1px solid #cfd7e3;
                border-radius: 7px;
                selection-background-color: #2563eb;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #2563eb;
            }
            QPushButton {
                min-height: 38px;
                padding: 7px 14px;
                font-size: 14px;
                color: #17202a;
                background: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
            }
            QPushButton:hover {
                background: #f8fafc;
                border-color: #94a3b8;
            }
            QPushButton:pressed {
                background: #e9eef5;
            }
            QPushButton:disabled {
                color: #9aa6b2;
                background: #e5e9ef;
                border-color: #d5dbe4;
            }
            QPushButton#primaryButton {
                min-width: 112px;
                color: #ffffff;
                background: #2563eb;
                border: 1px solid #2563eb;
                font-weight: 600;
            }
            QPushButton#primaryButton:hover {
                background: #1d4ed8;
                border-color: #1d4ed8;
            }
            QPushButton#primaryButton:pressed {
                background: #1e40af;
                border-color: #1e40af;
            }
            QPushButton#quietButton {
                color: #475569;
            }
            QLabel#statusLabel {
                min-height: 24px;
                color: #475569;
            }
            QLabel#previewLabel {
                background: #ffffff;
                border: 1px solid #d7dee8;
                border-radius: 8px;
                color: #64748b;
                font-size: 15px;
            }
            """
        )

    def apply_language(self) -> None:
        self.setWindowTitle(self._t("app_title"))
        self.language_menu.setTitle(self._t("menu_language"))
        self.format_label.setText(self._t("format_label"))
        self.number_label.setText(self._t("number_label"))
        self.number_input.setPlaceholderText(self._t("number_placeholder"))
        self.generate_button.setText(self._t("generate_button"))
        self.copy_png_button.setText(self._t("copy_png_button"))
        self.save_png_button.setText(self._t("save_png_button"))
        self.save_svg_button.setText(self._t("save_svg_button"))
        self.clear_button.setText(self._t("clear_button"))
        if self.current_png is None:
            self.preview_label.setText(self._t("preview_placeholder"))
        if not self.status_label.text():
            self.status_label.setText(self._t("ready_message"))
        for language_key, action in self.language_actions.items():
            action.setChecked(language_key == self.language)

    def set_language(self, language: str) -> None:
        if language not in LANGUAGES:
            return
        self.language = language
        self.apply_language()
        self._validate_without_rendering()

    def eventFilter(self, watched, event) -> bool:
        if watched == self.number_input and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self.clear_form()
                return True
            if event.matches(QKeySequence.StandardKey.Copy):
                self.copy_png()
                return True
        return super().eventFilter(watched, event)

    def generate_barcode(self) -> None:
        format_key = self._selected_format_key()
        value = self.number_input.text().strip()
        validation = validate_barcode_value(value, format_key)
        if not validation.is_valid:
            self.current_png = None
            self.current_svg = None
            self._set_export_enabled(False)
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText(self._validation_message(validation.message_key))
            self.status_label.setText(self._validation_message(validation.message_key))
            self._focus_number_input()
            return

        try:
            png = render_png(value, format_key)
            svg = render_svg(value, format_key)
        except Exception as exc:
            QMessageBox.critical(self, self._t("error_title"), self._t("render_error"))
            self.status_label.setText(f"{self._t('render_error')} {exc}")
            return

        self.current_png = png
        self.current_svg = svg
        self._set_preview_png(png)
        self._set_export_enabled(True)
        self.status_label.setText(self._validation_message(validation.message_key))
        self._focus_number_input()

    def copy_png(self) -> None:
        if self.current_png is None:
            self._focus_number_input()
            return
        image = QImage.fromData(self.current_png, "PNG")
        QApplication.clipboard().setImage(image)
        self.status_label.setText(self._t("copied_message"))
        self._focus_number_input()

    def save_png(self) -> None:
        if self.current_png is None:
            return
        path = self._get_save_path(self._t("save_png_title"), self._t("png_filter"), ".png")
        if path is None:
            return
        path.write_bytes(self.current_png)
        self.status_label.setText(self._t("saved_png_message"))

    def save_svg(self) -> None:
        if self.current_svg is None:
            return
        path = self._get_save_path(self._t("save_svg_title"), self._t("svg_filter"), ".svg")
        if path is None:
            return
        path.write_bytes(self.current_svg)
        self.status_label.setText(self._t("saved_svg_message"))

    def clear_form(self) -> None:
        self.number_input.clear()
        self.status_label.setText(self._t("ready_message"))
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setText(self._t("preview_placeholder"))
        self.current_png = None
        self.current_svg = None
        self._set_export_enabled(False)
        self._focus_number_input()

    def _set_preview_png(self, png: bytes) -> None:
        image = QImage.fromData(png, "PNG")
        pixmap = QPixmap.fromImage(image)
        self.preview_label.setText("")
        self.preview_label.setPixmap(
            pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        if self.current_png is not None:
            self._set_preview_png(self.current_png)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._focus_number_input()

    def _set_export_enabled(self, enabled: bool) -> None:
        self.copy_png_button.setEnabled(enabled)
        self.save_png_button.setEnabled(enabled)
        self.save_svg_button.setEnabled(enabled)

    def _validate_without_rendering(self) -> None:
        if not self.number_input.text().strip():
            return
        validation = validate_barcode_value(
            self.number_input.text().strip(),
            self._selected_format_key(),
        )
        self.status_label.setText(self._validation_message(validation.message_key))

    def _validation_message(self, message_key: str) -> str:
        barcode_format = FORMATS[self._selected_format_key()]
        validation = validate_barcode_value(self.number_input.text().strip(), barcode_format.key)
        return self._t(
            message_key,
            format=barcode_format.label,
            length=barcode_format.length,
            expected=validation.expected_check_digit or "",
        )

    def _get_save_path(self, title: str, file_filter: str, suffix: str) -> Path | None:
        filename, _ = QFileDialog.getSaveFileName(self, title, "", file_filter)
        if not filename:
            return None
        path = Path(filename)
        if path.suffix.lower() != suffix:
            path = path.with_suffix(suffix)
        return path

    def _selected_format_key(self) -> str:
        return self.format_combo.currentData()

    def _focus_number_input(self) -> None:
        self.number_input.setFocus(Qt.FocusReason.ShortcutFocusReason)
        self.number_input.selectAll()

    def _t(self, key: str, **params: object) -> str:
        return translate(self.language, key, **params)


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
