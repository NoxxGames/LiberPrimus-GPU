"""Read-only rich detail panel for selected Source Browser entries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMenu,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from .entries import SourceBrowserEntry
from .file_opening import open_file, open_file_location, open_url
from .path_aliases import load_path_aliases, resolve_with_aliases
from .normalizer import url_label
from .number_fact_cards import number_fact_card_widget
from .number_facts import normalize_entry_number_facts, zero_fact_review_state
from .status_display import (
    STATUS_LEGEND,
    STATUS_UNSPECIFIED_TOOLTIP,
    display_status,
)


class ThumbnailButton(QToolButton):
    """Small image action button that never interprets image content."""

    open_requested = Signal(int)

    def __init__(
        self,
        *,
        source_path: str,
        resolved_path: Path,
        index: int,
        hash_value: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.source_path = source_path
        self.resolved_path = resolved_path
        self.index = index
        self.hash_value = hash_value
        self.setObjectName("sourceBrowserThumbnailButton")
        self.setIconSize(QSize(128, 96))
        self.setFixedSize(154, 132)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setText(_short_path_label(source_path, missing=not resolved_path.exists()))
        self.setToolTip(source_path)
        self.clicked.connect(lambda: self.open_requested.emit(self.index))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        if resolved_path.exists():
            pixmap = QPixmap(str(resolved_path))
            if not pixmap.isNull():
                self.setIcon(
                    QIcon(
                        pixmap.scaled(
                            128,
                            96,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation,
                        )
                    )
                )

    def _show_context_menu(self) -> None:
        menu = QMenu(self)
        open_viewer = menu.addAction("Open Image Viewer")
        open_viewer.triggered.connect(lambda: self.open_requested.emit(self.index))
        open_file_action = menu.addAction("Open File")
        open_file_action.setEnabled(self.resolved_path.exists())
        open_file_action.triggered.connect(lambda: open_file(self.resolved_path))
        open_location = menu.addAction("Open File Location")
        open_location.setEnabled(self.resolved_path.exists())
        open_location.triggered.connect(lambda: open_file_location(self.resolved_path))
        copy_path = menu.addAction("Copy Path")
        copy_path.triggered.connect(lambda: _copy_text(self.source_path))
        copy_hash = menu.addAction("Copy SHA/hash")
        copy_hash.setEnabled(bool(self.hash_value))
        copy_hash.triggered.connect(lambda: _copy_text(self.hash_value or ""))
        menu.exec(self.mapToGlobal(self.rect().bottomLeft()))


class EntryDetailPanel(QWidget):
    """Tabbed Source Browser detail panel for one selected entry."""

    image_requested = Signal(list, int)
    hide_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("sourceBrowserEntryDetailPanel")
        self._aliases = load_path_aliases()
        self._entry: SourceBrowserEntry | None = None
        self._build_ui()
        self.show_entry(None)

    def show_entry(self, entry: SourceBrowserEntry | None) -> None:
        self._entry = entry
        self._aliases = load_path_aliases()
        self._clear_dynamic_sections()
        if entry is None:
            self.header.setText("Details")
            self._add_empty(self.overview_layout, "Select a source-browser entry to inspect details.")
            self.raw_text.setPlainText("")
            return
        self.header.setText(entry.title or entry.entry_id)
        self._render_overview(entry)
        self._render_media_files(entry)
        self._render_number_facts(entry)
        self._render_warnings_links(entry)
        self.raw_text.setPlainText(
            yaml.safe_dump(entry.to_dict(include_raw=True), sort_keys=False, allow_unicode=False)
        )

    def focus_panel(self) -> None:
        self.tabs.setFocus(Qt.FocusReason.OtherFocusReason)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)
        header_row = QHBoxLayout()
        self.header = QLabel("Details")
        self.header.setObjectName("sourceBrowserDetailHeader")
        self.header.setStyleSheet("font-weight: 600; color: #eeeeee;")
        header_row.addWidget(self.header, 1)
        hide_button = QPushButton("Hide")
        hide_button.setObjectName("sourceBrowserDetailHideButton")
        hide_button.clicked.connect(self.hide_requested.emit)
        header_row.addWidget(hide_button, 0)
        layout.addLayout(header_row)
        self.tabs = QTabWidget()
        self.tabs.setObjectName("sourceBrowserDetailTabs")
        self.overview_layout = self._add_scroll_tab("Overview")
        self.media_layout = self._add_scroll_tab("Media && Files")
        self.number_facts_layout = self._add_scroll_tab("Number facts")
        self.warnings_layout = self._add_scroll_tab("Warnings && links")
        self.raw_text = QPlainTextEdit()
        self.raw_text.setObjectName("sourceBrowserRawRecordPreview")
        self.raw_text.setReadOnly(True)
        self.raw_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.raw_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tabs.addTab(self.raw_text, "Raw record")
        layout.addWidget(self.tabs, 1)
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _add_scroll_tab(self, title: str) -> QVBoxLayout:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        tab_layout = QVBoxLayout(container)
        tab_layout.setContentsMargins(8, 8, 8, 8)
        tab_layout.setSpacing(8)
        scroll.setWidget(container)
        self.tabs.addTab(scroll, title)
        return tab_layout

    def _clear_dynamic_sections(self) -> None:
        for layout in (
            self.overview_layout,
            self.media_layout,
            self.number_facts_layout,
            self.warnings_layout,
        ):
            _clear_layout(layout)

    def _render_overview(self, entry: SourceBrowserEntry) -> None:
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        overview = QGroupBox("Entry")
        overview.setLayout(form)
        fields = [
            ("Summary", entry.summary),
            ("Entry ID", entry.entry_id),
            ("Category", entry.category),
            ("Entry type", entry.entry_type),
            ("Stage ID", entry.stage_id),
            ("Record type", entry.record_type),
            ("Candidate family ID", entry.candidate_family_id),
            ("Source type", entry.source_type),
            ("Status", _status_display(entry)),
            ("Trust tier", entry.trust_tier),
            ("Confidence", entry.confidence),
            ("Selected now", _bool_display(entry.selected_now)),
            ("Solve claim", _bool_display(entry.solve_claim)),
            ("Execution allowed", _bool_display(entry.execution_allowed)),
            ("Source-lock only", _bool_display(entry.source_lock_only)),
            ("Created at", entry.created_at),
            ("Modified at", entry.modified_at),
            ("Source record path", entry.source_record_path),
            ("Schema path", entry.schema_path),
        ]
        for label, value in fields:
            text = _missing(value)
            widget = QLabel(text)
            widget.setWordWrap(True)
            if label == "Status" and not entry.source_status:
                widget.setToolTip(STATUS_UNSPECIFIED_TOOLTIP)
            form.addRow(label, widget)
        self.overview_layout.addWidget(overview)
        legend = QLabel(STATUS_LEGEND)
        legend.setObjectName("sourceBrowserStatusLegend")
        legend.setWordWrap(True)
        legend.setStyleSheet("color: #c8c8c8;")
        self.overview_layout.addWidget(legend)
        if entry.notes:
            notes = QLabel(entry.notes)
            notes.setWordWrap(True)
            box = QGroupBox("Notes")
            box_layout = QVBoxLayout(box)
            box_layout.addWidget(notes)
            self.overview_layout.addWidget(box)
        self.overview_layout.addStretch(1)

    def _render_media_files(self, entry: SourceBrowserEntry) -> None:
        self.media_layout.addWidget(self._image_group(entry))
        self.media_layout.addWidget(self._path_group(entry))
        self.media_layout.addWidget(self._url_group(entry))
        self.media_layout.addStretch(1)

    def _image_group(self, entry: SourceBrowserEntry) -> QGroupBox:
        box = QGroupBox(f"Images ({len(entry.image_paths)})")
        layout = QGridLayout(box)
        layout.setSpacing(8)
        if not entry.image_paths:
            layout.addWidget(QLabel("No image paths recorded."), 0, 0)
            return box
        for index, path_text in enumerate(entry.image_paths):
            resolved = _resolve(path_text, self._aliases)
            thumb = ThumbnailButton(
                source_path=path_text,
                resolved_path=resolved,
                index=index,
                hash_value=_hash_for_path(entry, path_text),
            )
            thumb.open_requested.connect(lambda image_index: self.image_requested.emit(entry.image_paths, image_index))
            layout.addWidget(thumb, index // 2, index % 2)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        return box

    def _path_group(self, entry: SourceBrowserEntry) -> QGroupBox:
        paths = _unique(entry.local_paths + entry.document_paths + entry.image_paths)
        box = QGroupBox(f"Documents / files ({len(paths)})")
        layout = QVBoxLayout(box)
        if not paths:
            layout.addWidget(QLabel("No file paths recorded."))
            return box
        for path_text in paths:
            layout.addWidget(self._path_row(path_text))
        return box

    def _path_row(self, path_text: str) -> QWidget:
        resolved = _resolve(path_text, self._aliases)
        row = QWidget()
        row.setObjectName("sourceBrowserPathRow")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        status = "present" if resolved.exists() else "missing"
        label = QLabel(
            f"{Path(path_text).suffix.lower() or 'file'}  {path_text}  [{status}]\n"
            f"resolved: {resolved.as_posix()}"
        )
        label.setWordWrap(True)
        label.setToolTip(str(resolved))
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(label, 1)
        open_button = QPushButton("Open")
        open_button.setEnabled(resolved.exists())
        open_button.clicked.connect(lambda: open_file(resolved))
        layout.addWidget(open_button)
        location_button = QPushButton("Open Location")
        location_button.setEnabled(resolved.exists())
        location_button.clicked.connect(lambda: open_file_location(resolved))
        layout.addWidget(location_button)
        copy_button = QPushButton("Copy Path")
        copy_button.clicked.connect(lambda: _copy_text(path_text))
        layout.addWidget(copy_button)
        row.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        row.customContextMenuRequested.connect(lambda _point, path=path_text, resolved_path=resolved: _path_menu(row, path, resolved_path))
        return row

    def _url_group(self, entry: SourceBrowserEntry) -> QGroupBox:
        box = QGroupBox(f"URLs ({len(entry.urls)})")
        layout = QVBoxLayout(box)
        if not entry.urls:
            layout.addWidget(QLabel("No URLs recorded."))
            return box
        for url in entry.urls:
            row = QWidget()
            row.setObjectName("sourceBrowserUrlRow")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            label = QLabel(url_label(url))
            label.setToolTip(url)
            label.setWordWrap(True)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            row_layout.addWidget(label, 1)
            open_button = QPushButton("Open URL")
            open_button.clicked.connect(lambda _checked=False, target=url: open_url(target))
            row_layout.addWidget(open_button)
            copy_button = QPushButton("Copy URL")
            copy_button.clicked.connect(lambda _checked=False, target=url: _copy_text(target))
            row_layout.addWidget(copy_button)
            row.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            row.customContextMenuRequested.connect(lambda _point, target=url, owner=row: _url_menu(owner, target))
            layout.addWidget(row)
        return box

    def _render_number_facts(self, entry: SourceBrowserEntry) -> None:
        cards = normalize_entry_number_facts(entry)
        if not cards:
            state = zero_fact_review_state(entry)
            message = (
                "Reviewed: no relevant number facts found."
                if state == "zero_extracted_facts_reviewed_none_found"
                else "Not reviewed for number facts. Older zero-fact entries are not necessarily number-free."
            )
            self._add_empty(self.number_facts_layout, message)
            return
        counts: dict[str, int] = {}
        for card in cards:
            counts[card.review_state] = counts.get(card.review_state, 0) + 1
        header = QLabel(
            f"{len(cards)} fact card(s). Review states: "
            + ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        )
        header.setWordWrap(True)
        header.setStyleSheet("color: #d8d8d8;")
        self.number_facts_layout.addWidget(header)
        for card in cards:
            self.number_facts_layout.addWidget(number_fact_card_widget(card))
        self.number_facts_layout.addStretch(1)

    def _render_warnings_links(self, entry: SourceBrowserEntry) -> None:
        warnings = QGroupBox(f"Warnings ({len(entry.warnings)})")
        warnings_layout = QVBoxLayout(warnings)
        if entry.warnings:
            for warning in entry.warnings:
                label = QLabel(f"Warning: {warning}")
                label.setWordWrap(True)
                label.setStyleSheet("color: #d6a842;")
                warnings_layout.addWidget(label)
        else:
            warnings_layout.addWidget(QLabel("No warnings recorded."))
        self.warnings_layout.addWidget(warnings)
        links = QGroupBox(f"Links to ({len(entry.links_to)})")
        links_layout = QVBoxLayout(links)
        if entry.links_to:
            for link in entry.links_to:
                row = QWidget()
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.addWidget(QLabel(link), 1)
                copy_button = QPushButton("Copy")
                copy_button.clicked.connect(lambda _checked=False, target=link: _copy_text(target))
                row_layout.addWidget(copy_button)
                links_layout.addWidget(row)
        else:
            links_layout.addWidget(QLabel("No linked candidate/source IDs recorded."))
        self.warnings_layout.addWidget(links)
        self.warnings_layout.addStretch(1)

    def _add_empty(self, layout: QVBoxLayout, text: str) -> None:
        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addStretch(1)


DetailPanel = EntryDetailPanel


def _clear_layout(layout: QLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        child_layout = item.layout()
        if widget is not None:
            widget.deleteLater()
        if child_layout is not None:
            _clear_layout(child_layout)


def _status_display(entry: SourceBrowserEntry) -> str:
    return display_status(entry.source_status)


def _bool_display(value: bool | None) -> str:
    if value is None:
        return "unspecified"
    return str(value).lower()


def _missing(value: Any) -> str:
    if value is None or value == "":
        return "unspecified"
    return str(value)


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def _resolve(path_text: str, aliases: dict[str, str]) -> Path:
    return resolve_with_aliases(path_text, aliases)


def _hash_for_path(entry: SourceBrowserEntry, path_text: str) -> str | None:
    if path_text in entry.hashes:
        return entry.hashes[path_text]
    path_name = Path(path_text).name.lower()
    for key, value in entry.hashes.items():
        if path_name and path_name in key.lower():
            return value
    if len(entry.hashes) == 1:
        return next(iter(entry.hashes.values()))
    return None


def _short_path_label(path_text: str, *, missing: bool) -> str:
    label = Path(path_text).name or path_text[-36:]
    if len(label) > 32:
        label = f"...{label[-29:]}"
    return f"{label}\nmissing" if missing else label


def _copy_text(text: str) -> None:
    QApplication.clipboard().setText(text)


def _path_menu(owner: QWidget, path_text: str, resolved_path: Path) -> None:
    menu = QMenu(owner)
    open_action = menu.addAction("Open File")
    open_action.setEnabled(resolved_path.exists())
    open_action.triggered.connect(lambda: open_file(resolved_path))
    location_action = menu.addAction("Open File Location")
    location_action.setEnabled(resolved_path.exists())
    location_action.triggered.connect(lambda: open_file_location(resolved_path))
    copy_action = menu.addAction("Copy Path")
    copy_action.triggered.connect(lambda: _copy_text(path_text))
    menu.exec(owner.mapToGlobal(owner.rect().bottomLeft()))


def _url_menu(owner: QWidget, url: str) -> None:
    menu = QMenu(owner)
    open_action = menu.addAction("Open URL")
    open_action.triggered.connect(lambda: open_url(url))
    copy_action = menu.addAction("Copy URL")
    copy_action.triggered.connect(lambda: _copy_text(url))
    menu.exec(owner.mapToGlobal(owner.rect().bottomLeft()))
