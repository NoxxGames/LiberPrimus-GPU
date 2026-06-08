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
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QListWidget, QScrollArea {
    background: #111113;
    color: #e8e8e8;
    border: 1px solid #3b3b40;
    selection-background-color: #263247;
}
QTableView {
    background: #111113;
    alternate-background-color: #161618;
    color: #e8e8e8;
    gridline-color: #34343a;
    selection-background-color: #263247;
    border: 1px solid #3b3b40;
}
QHeaderView::section {
    background: #202024;
    color: #f0f0f0;
    border: 0;
    border-right: 1px solid #3b3b40;
    padding: 5px;
    font-weight: 600;
}
QTabWidget::pane {
    border: 1px solid #3b3b40;
    background: #111113;
}
QTabBar::tab {
    background: #202024;
    color: #e8e8e8;
    border: 1px solid #3b3b40;
    border-bottom-color: #3b3b40;
    padding: 6px 10px;
    min-height: 20px;
}
QTabBar::tab:selected {
    background: #263247;
    color: #ffffff;
}
QTabBar::tab:hover {
    background: #2b3549;
}
QGroupBox {
    border: 1px solid #3b3b40;
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 10px;
}
QGroupBox::title {
    color: #d8d8d8;
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}
QSplitter::handle {
    background: #3b3b40;
}
QSplitter::handle:horizontal {
    width: 6px;
}
QSplitter::handle:vertical {
    height: 6px;
}
QScrollBar:vertical {
    background: #141416;
    width: 12px;
    margin: 0;
    border: 0;
}
QScrollBar::handle:vertical {
    background: #4a4a50;
    min-height: 28px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #5a6474;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
    border: 0;
    background: transparent;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}
QScrollBar:horizontal {
    background: #141416;
    height: 12px;
    margin: 0;
    border: 0;
}
QScrollBar::handle:horizontal {
    background: #4a4a50;
    min-width: 28px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #5a6474;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
    border: 0;
    background: transparent;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
}
"""
