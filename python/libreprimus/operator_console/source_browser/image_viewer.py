"""Simple image viewer dialog with explicit operator controls."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
)

from .file_opening import open_file, open_file_location


class ImageViewerDialog(QDialog):
    def __init__(self, image_paths: list[str], start_index: int = 0) -> None:
        super().__init__()
        self.setWindowTitle("Image viewer")
        self.paths = [Path(path) for path in image_paths]
        self.index = start_index
        self.scale = 1.0
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.label)
        self.scroll.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll)
        controls = QHBoxLayout()
        for text, callback in [
            ("Previous", self.previous_image),
            ("Next", self.next_image),
            ("Zoom in", self.zoom_in),
            ("Zoom out", self.zoom_out),
            ("Fit", self.fit_to_window),
            ("Actual size", self.actual_size),
            ("Open location", self.open_location),
            ("Open externally", self.open_external),
            ("Copy path", self.copy_path),
        ]:
            button = QPushButton(text)
            button.clicked.connect(callback)
            controls.addWidget(button)
        layout.addLayout(controls)
        self.load_image()

    def load_image(self) -> None:
        if not self.paths:
            self.label.setText("No image")
            return
        path = self.paths[self.index]
        if not path.exists():
            self.label.setText(f"Missing image: {path.as_posix()}")
            return
        pixmap = QPixmap(str(path))
        if self.scale != 1.0:
            size = pixmap.size()
            pixmap = pixmap.scaled(
                int(size.width() * self.scale),
                int(size.height() * self.scale),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        self.label.setPixmap(pixmap)

    def zoom_in(self) -> None:
        self.scale *= 1.25
        self.load_image()

    def zoom_out(self) -> None:
        self.scale /= 1.25
        self.load_image()

    def fit_to_window(self) -> None:
        self.scale = 1.0
        self.load_image()

    def actual_size(self) -> None:
        self.scale = 1.0
        self.load_image()

    def previous_image(self) -> None:
        if self.paths:
            self.index = (self.index - 1) % len(self.paths)
            self.scale = 1.0
            self.load_image()

    def next_image(self) -> None:
        if self.paths:
            self.index = (self.index + 1) % len(self.paths)
            self.scale = 1.0
            self.load_image()

    def open_location(self) -> None:
        if self.paths:
            open_file_location(self.paths[self.index])

    def open_external(self) -> None:
        if self.paths:
            open_file(self.paths[self.index])

    def copy_path(self) -> None:
        if self.paths:
            QApplication.clipboard().setText(str(self.paths[self.index]))
