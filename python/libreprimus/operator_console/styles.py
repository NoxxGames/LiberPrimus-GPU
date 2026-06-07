"""Qt style sheet for the dark Operator Console UI."""

from __future__ import annotations

DARK_STYLE = """
QMainWindow, QWidget {
    background: #0b0b0c;
    color: #e8e8e8;
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
    font-size: 10pt;
}
QMenuBar, QMenu, QToolBar, QStatusBar {
    background: #141416;
    color: #e8e8e8;
    border: 0;
}
QToolButton, QPushButton {
    background: #202024;
    color: #e8e8e8;
    border: 1px solid #2a2a2e;
    padding: 5px 10px;
}
QToolButton:hover, QPushButton:hover {
    background: #1d2533;
}
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QListWidget {
    background: #111113;
    color: #e8e8e8;
    border: 1px solid #2a2a2e;
    selection-background-color: #263247;
}
QTableView {
    background: #111113;
    alternate-background-color: #161618;
    color: #e8e8e8;
    gridline-color: #2a2a2e;
    selection-background-color: #263247;
}
QHeaderView::section {
    background: #202024;
    color: #f0f0f0;
    border: 0;
    border-right: 1px solid #2a2a2e;
    padding: 5px;
    font-weight: 600;
}
QSplitter::handle {
    background: #2a2a2e;
}
"""
