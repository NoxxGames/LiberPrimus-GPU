from __future__ import annotations

import importlib.util

import pytest


@pytest.mark.skipif(importlib.util.find_spec("PySide6") is None, reason="PySide6 is optional")
def test_qt_modules_import_when_pyside6_available() -> None:
    from libreprimus.operator_console.main_window import MainWindow
    from libreprimus.operator_console.source_browser.table_model import SourceBrowserTableModel

    assert MainWindow is not None
    assert SourceBrowserTableModel is not None
