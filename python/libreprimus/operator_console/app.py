"""Operator Console application launcher."""

from __future__ import annotations

import sys

from .errors import GuiDependencyError
from .settings import GUI_INSTALL_MESSAGE


def run_operator_console() -> int:
    try:
        from PySide6.QtWidgets import QApplication

        from .main_window import MainWindow
        from .styles import DARK_STYLE
    except ModuleNotFoundError as exc:
        if exc.name and exc.name.startswith("PySide6"):
            raise GuiDependencyError(GUI_INSTALL_MESSAGE) from exc
        raise

    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Liber Primus Operator Console")
    app.setStyleSheet(DARK_STYLE)
    window = MainWindow()
    window.resize(1480, 860)
    window.show()
    return app.exec()
