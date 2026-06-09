"""Qt main window for the Liber Primus Operator Console."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QModelIndex, QPoint, QTimer, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMenu,
    QMessageBox,
    QSizePolicy,
    QSplitter,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from .navigation import source_browser_categories
from .settings import APP_NAME, SOURCE_BROWSER_NAME
from .source_browser.column_profiles import visible_columns
from .source_browser.context_file import create_context_file_if_missing
from .source_browser.detail_panel import DetailPanel, STATUS_LEGEND
from .source_browser.dialogs import AddModifyDialog, confirm_remove
from .source_browser.entries import SourceBrowserEntry
from .source_browser.file_opening import open_file, open_file_location, open_url
from .source_browser.filters import filter_entries
from .source_browser.image_viewer import ImageViewerDialog
from .source_browser.loaders import build_source_index
from .source_browser.manual_entries import save_manual_entry
from .source_browser.overrides import save_override
from .source_browser.table_model import SourceBrowserTableModel
from .source_browser.tombstones import save_tombstone


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.all_entries: list[SourceBrowserEntry] = []
        self.filtered_entries: list[SourceBrowserEntry] = []
        self._last_detail_entry_id: str | None = None
        self._filter_timer = QTimer(self)
        self._filter_timer.setSingleShot(True)
        self._filter_timer.setInterval(120)
        self._filter_timer.timeout.connect(self.apply_filters)
        self._build_menu()
        self._build_toolbar()
        self._build_content()
        self.refresh_entries()

    def _build_menu(self) -> None:
        menu = self.menuBar()
        menu.addMenu("File")
        view_menu = menu.addMenu("View")
        self.show_details_action = QAction("Show Details Panel", self)
        self.show_details_action.setCheckable(True)
        self.show_details_action.setChecked(True)
        self.show_details_action.triggered.connect(self.toggle_details_panel)
        view_menu.addAction(self.show_details_action)
        menu.addMenu("Tools")
        menu.addMenu("Help")

    def _build_toolbar(self) -> None:
        toolbar = QToolBar("Source Browser")
        self.addToolBar(toolbar)
        for label, callback in [
            ("Refresh", self.refresh_entries),
            ("Add", self.add_entry),
            ("Modify", self.modify_entry),
            ("Remove", self.remove_entry),
            ("Validate", self.validate_entries),
            ("Open Context", self.open_context),
            ("Open File Location", self.open_selected_location),
            ("Open URL", self.open_selected_url),
        ]:
            action = toolbar.addAction(label)
            action.triggered.connect(callback)
        toolbar.addSeparator()
        self.toggle_details_toolbar_action = toolbar.addAction("Toggle Details")
        self.toggle_details_toolbar_action.setCheckable(True)
        self.toggle_details_toolbar_action.setChecked(True)
        self.toggle_details_toolbar_action.triggered.connect(self.toggle_details_panel)

    def _build_content(self) -> None:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(8, 6, 8, 0)
        layout.setSpacing(4)
        title = QLabel(f"{APP_NAME} / {SOURCE_BROWSER_NAME}")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        title.setMinimumHeight(24)
        title.setMaximumHeight(30)
        title.setStyleSheet(
            "font-size: 12pt; font-weight: 600; color: #f0f0f0; padding: 2px 0;"
        )
        layout.addWidget(title, 0)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search source records, paths, URLs, warnings, number facts...")
        self.search.textChanged.connect(self.schedule_filters)
        self.search.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.search, 0)
        self.status_legend = QLabel(STATUS_LEGEND)
        self.status_legend.setToolTip(STATUS_LEGEND)
        self.status_legend.setStyleSheet("color: #8a8a8a;")
        self.status_legend.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.status_legend, 0)
        self.content_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.categories = QListWidget()
        self.categories.setMinimumWidth(140)
        self.categories.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.categories.addItems(source_browser_categories())
        self.categories.setCurrentRow(0)
        self.categories.currentTextChanged.connect(self.apply_filters)
        self.content_splitter.addWidget(self.categories)
        self.table = QTableView()
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.clicked.connect(self.select_table_row)
        self.table.doubleClicked.connect(self.open_detail_action)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_table_context_menu)
        self.table.setToolTip(STATUS_LEGEND)
        self.model = SourceBrowserTableModel([], visible_columns())
        self.table.setModel(self.model)
        for index, column in enumerate(visible_columns()):
            self.table.setColumnWidth(index, int(column.get("width", 120)))
        self.detail = DetailPanel()
        self.detail.image_requested.connect(self.open_image_viewer_at)
        self.detail.hide_requested.connect(lambda: self.toggle_details_panel(False))
        self.detail.setMinimumWidth(360)
        self.content_splitter.addWidget(self.table)
        self.content_splitter.addWidget(self.detail)
        self.content_splitter.setStretchFactor(0, 0)
        self.content_splitter.setStretchFactor(1, 1)
        self.content_splitter.setStretchFactor(2, 0)
        self.content_splitter.setCollapsible(0, False)
        self.content_splitter.setCollapsible(1, False)
        self.content_splitter.setCollapsible(2, True)
        self.content_splitter.setSizes([220, 1120, 520])
        layout.addWidget(self.content_splitter, 1)
        self.setCentralWidget(root)
        self.statusBar().showMessage("Source Browser ready")
        self.table.selectionModel().selectionChanged.connect(self.selection_changed)

    def refresh_entries(self) -> None:
        index = build_source_index()
        self.all_entries = index.entries
        self.apply_filters()

    def schedule_filters(self) -> None:
        self._filter_timer.start()

    def apply_filters(self) -> None:
        category_item = self.categories.currentItem()
        category = category_item.text() if category_item else "All"
        self.filtered_entries = filter_entries(
            self.all_entries,
            category=category,
            search=self.search.text(),
        )
        self.model.replace_entries(self.filtered_entries)
        self.detail.show_entry(self.current_entry())
        self.statusBar().showMessage(
            f"{len(self.filtered_entries)} of {len(self.all_entries)} entries / category: {category} / "
            "status unspecified means no status field"
        )

    def current_entry(self) -> SourceBrowserEntry | None:
        indexes = self.table.selectionModel().selectedRows()
        if indexes:
            return self.model.entry_at(indexes[0].row())
        index = self.table.currentIndex()
        if index.isValid():
            return self.model.entry_at(index.row())
        return None

    def selection_changed(self) -> None:
        entry = self.current_entry()
        if entry and entry.entry_id == self._last_detail_entry_id:
            return
        self._last_detail_entry_id = entry.entry_id if entry else None
        self.detail.show_entry(entry)
        self.detail.setVisible(self.show_details_action.isChecked())

    def select_table_row(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.table.selectRow(index.row())
        entry = self._entry_for_index(index)
        if entry and entry.entry_id != self._last_detail_entry_id:
            self._last_detail_entry_id = entry.entry_id
            self.detail.show_entry(entry)

    def add_entry(self) -> None:
        dialog = AddModifyDialog()
        if dialog.exec():
            save_manual_entry(dialog.fields())
            self.refresh_entries()

    def modify_entry(self) -> None:
        entry = self.current_entry()
        if entry is None:
            return
        committed = entry.record_type != "source_browser_manual_entry"
        dialog = AddModifyDialog(entry, committed=committed)
        if dialog.exec():
            if committed:
                save_override(
                    target_entry_id=entry.entry_id,
                    target_source_record_path=entry.source_record_path,
                    fields=dialog.fields(),
                )
            else:
                fields = dialog.fields()
                fields["entry_id"] = entry.entry_id
                save_manual_entry(fields)
            self.refresh_entries()

    def remove_entry(self) -> None:
        entry = self.current_entry()
        if entry is None or not confirm_remove(entry):
            return
        if entry.record_type == "source_browser_manual_entry":
            path = Path(entry.source_record_path)
            if path.exists():
                path.unlink()
        else:
            save_tombstone(
                target_entry_id=entry.entry_id,
                target_source_record_path=entry.source_record_path,
            )
        self.refresh_entries()

    def validate_entries(self) -> None:
        from .source_browser.validators import validate_manual_records, validate_source_index

        source_result = validate_source_index()
        manual_result = validate_manual_records()
        QMessageBox.information(
            self,
            "Validation",
            f"Source index errors: {len(source_result.errors)}\n"
            f"Manual record errors: {len(manual_result.errors)}",
        )

    def open_context(self) -> None:
        created = create_context_file_if_missing()
        if created:
            self.refresh_entries()
        open_file(Path("ChatGPT-ContextFile.md"))

    def open_selected_location(self) -> None:
        entry = self.current_entry()
        if entry is None:
            return
        paths = entry.image_paths or entry.document_paths or entry.local_paths
        if paths:
            open_file_location(Path(paths[0]))

    def open_selected_url(self) -> None:
        entry = self.current_entry()
        if entry and entry.urls:
            open_url(entry.urls[0])

    def toggle_details_panel(self, checked: bool) -> None:
        self._set_details_visible(checked)

    def _set_details_visible(self, visible: bool) -> None:
        for action in (self.show_details_action, self.toggle_details_toolbar_action):
            action.blockSignals(True)
            action.setChecked(visible)
            action.blockSignals(False)
        self.detail.setVisible(visible)
        self.content_splitter.setSizes([220, 1120, 520] if visible else [220, 1440, 0])
        if visible:
            self.detail.show_entry(self.current_entry())

    def open_detail_action(self, index: QModelIndex | None = None) -> None:
        entry = self._entry_for_index(index) if index and index.isValid() else self.current_entry()
        if entry is None:
            return
        key = self._column_key(index.column()) if index and index.isValid() else ""
        if key == "images" and entry.image_paths:
            self.open_image_viewer_at(entry.image_paths, 0)
            return
        if key == "urls" and entry.urls:
            open_url(entry.urls[0])
            return
        if key in {"document_paths", "local_paths"}:
            first_path = self._first_file_path(entry)
            if first_path:
                open_file_location(Path(first_path))
                return
        self.detail.show_entry(entry)
        self._set_details_visible(True)
        self.detail.focus_panel()

    def show_table_context_menu(self, position: QPoint) -> None:
        index = self.table.indexAt(position)
        if index.isValid():
            self.table.setCurrentIndex(index)
        entry = self._entry_for_index(index) if index.isValid() else self.current_entry()
        if entry is None:
            return
        menu = self._build_table_context_menu(entry)
        menu.exec(self.table.viewport().mapToGlobal(position))

    def _build_table_context_menu(self, entry: SourceBrowserEntry) -> QMenu:
        menu = QMenu(self)
        show_details = menu.addAction("Show Details")
        show_details.triggered.connect(lambda: self._show_details_for_entry(entry))
        image_action = menu.addAction("Open Image Viewer")
        image_action.setEnabled(bool(entry.image_paths))
        image_action.triggered.connect(lambda: self.open_image_viewer_at(entry.image_paths, 0))
        first_path = self._first_file_path(entry)
        first_url = entry.urls[0] if entry.urls else None
        open_first_file = menu.addAction("Open First File")
        open_first_file.setEnabled(bool(first_path))
        open_first_file.triggered.connect(lambda: open_file(Path(first_path or "")))
        open_location = menu.addAction("Open File Location")
        open_location.setEnabled(bool(first_path))
        open_location.triggered.connect(lambda: open_file_location(Path(first_path or "")))
        open_first_url = menu.addAction("Open First URL")
        open_first_url.setEnabled(bool(first_url))
        open_first_url.triggered.connect(lambda: open_url(first_url or ""))
        menu.addSeparator()
        copy_entry = menu.addAction("Copy Entry ID")
        copy_entry.triggered.connect(lambda: QApplication.clipboard().setText(entry.entry_id))
        copy_source = menu.addAction("Copy Source Record Path")
        copy_source.triggered.connect(lambda: QApplication.clipboard().setText(entry.source_record_path))
        copy_file = menu.addAction("Copy First File Path")
        copy_file.setEnabled(bool(first_path))
        copy_file.triggered.connect(lambda: QApplication.clipboard().setText(first_path or ""))
        copy_url = menu.addAction("Copy First URL")
        copy_url.setEnabled(bool(first_url))
        copy_url.triggered.connect(lambda: QApplication.clipboard().setText(first_url or ""))
        return menu

    def _show_details_for_entry(self, entry: SourceBrowserEntry) -> None:
        self.detail.show_entry(entry)
        self._set_details_visible(True)
        self.detail.focus_panel()

    def open_image_viewer_at(self, paths: list[str], index: int = 0) -> None:
        if paths:
            ImageViewerDialog(paths, start_index=index).exec()

    def _entry_for_index(self, index: QModelIndex) -> SourceBrowserEntry | None:
        return self.model.entry_at(index.row())

    def _column_key(self, column: int) -> str:
        columns = visible_columns()
        if 0 <= column < len(columns):
            return str(columns[column].get("key", ""))
        return ""

    def _first_file_path(self, entry: SourceBrowserEntry) -> str | None:
        paths = entry.image_paths or entry.document_paths or entry.local_paths
        return paths[0] if paths else None
