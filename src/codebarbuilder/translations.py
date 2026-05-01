from __future__ import annotations

DEFAULT_LANGUAGE = "es"

LANGUAGES = {
    "es": "Español",
    "en": "English",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "es": {
        "app_title": "Codebar builder",
        "menu_language": "Idioma",
        "format_label": "Formato",
        "number_label": "Número",
        "number_placeholder": "Introduce el número completo",
        "generate_button": "Generar",
        "copy_png_button": "Copiar PNG",
        "save_png_button": "Guardar PNG",
        "save_svg_button": "Guardar SVG",
        "clear_button": "Limpiar",
        "preview_placeholder": "El código de barras aparecerá aquí",
        "ready_message": "Introduce un número y genera el código.",
        "copied_message": "Imagen PNG copiada al portapapeles.",
        "saved_png_message": "PNG guardado correctamente.",
        "saved_svg_message": "SVG guardado correctamente.",
        "save_png_title": "Guardar PNG",
        "save_svg_title": "Guardar SVG",
        "png_filter": "Imagen PNG (*.png)",
        "svg_filter": "Imagen SVG (*.svg)",
        "validation_empty": "Introduce un número.",
        "validation_digits": "El número solo puede contener dígitos.",
        "validation_length": "{format} debe tener exactamente {length} dígitos.",
        "validation_checksum": "Dígito de control incorrecto. Debería ser {expected}.",
        "validation_ok": "Código válido.",
        "error_title": "Error",
        "render_error": "No se pudo generar el código de barras.",
    },
    "en": {
        "app_title": "Codebar builder",
        "menu_language": "Language",
        "format_label": "Format",
        "number_label": "Number",
        "number_placeholder": "Enter the full number",
        "generate_button": "Generate",
        "copy_png_button": "Copy PNG",
        "save_png_button": "Save PNG",
        "save_svg_button": "Save SVG",
        "clear_button": "Clear",
        "preview_placeholder": "The barcode will appear here",
        "ready_message": "Enter a number and generate the barcode.",
        "copied_message": "PNG image copied to the clipboard.",
        "saved_png_message": "PNG saved successfully.",
        "saved_svg_message": "SVG saved successfully.",
        "save_png_title": "Save PNG",
        "save_svg_title": "Save SVG",
        "png_filter": "PNG image (*.png)",
        "svg_filter": "SVG image (*.svg)",
        "validation_empty": "Enter a number.",
        "validation_digits": "The number can contain digits only.",
        "validation_length": "{format} must contain exactly {length} digits.",
        "validation_checksum": "Invalid check digit. It should be {expected}.",
        "validation_ok": "Valid code.",
        "error_title": "Error",
        "render_error": "Could not generate the barcode.",
    },
}


def translate(language: str, key: str, **params: object) -> str:
    text = TRANSLATIONS.get(language, TRANSLATIONS[DEFAULT_LANGUAGE]).get(key, key)
    return text.format(**params)
