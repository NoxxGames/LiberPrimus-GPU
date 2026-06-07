"""Qt main window for the Liber Primus Operator Console."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
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
from .source_browser.detail_panel import DetailPanel
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
        self._build_menu()
        self._build_toolbar()
        self._build_content()
        self.refresh_entries()

    def _build_menu(self) -> None:
        menu = self.menuBar()
        menu.addMenu("File")
        menu.addMenu("View")
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
        self.search.textChanged.connect(self.apply_filters)
        self.search.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.search, 0)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.categories = QListWidget()
        self.categories.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.categories.addItems(source_browser_categories())
        self.categories.setCurrentRow(0)
        self.categories.currentTextChanged.connect(self.apply_filters)
        splitter.addWidget(self.categories)
        table_and_detail = QSplitter(Qt.Orientation.Vertical)
        self.table = QTableView()
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self.open_detail_action)
        self.model = SourceBrowserTableModel([], visible_columns())
        self.table.setModel(self.model)
        for index, column in enumerate(visible_columns()):
            self.table.setColumnWidth(index, int(column.get("width", 120)))
        self.detail = DetailPanel()
        table_and_detail.addWidget(self.table)
        table_and_detail.addWidget(self.detail)
        table_and_detail.setStretchFactor(0, 1)
        table_and_detail.setStretchFactor(1, 0)
        table_and_detail.setCollapsible(1, True)
        table_and_detail.setSizes([1, 0])
        self.detail.hide()
        splitter.addWidget(table_and_detail)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([220, 1200])
        layout.addWidget(splitter, 1)
        self.setCentralWidget(root)
        self.statusBar().showMessage("Source Browser ready")
        self.table.selectionModel().selectionChanged.connect(self.selection_changed)

    def refresh_entries(self) -> None:
        index = build_source_index()
        self.all_entries = index.entries
        self.apply_filters()

    def apply_filters(self) -> None:
        category_item = self.categories.currentItem()
        category = category_item.text() if category_item else "All"
        self.filtered_entries = filter_entries(
            self.all_entries,
            category=category,
            search=self.search.text(),
        )
        self.model.replace_entries(self.filtered_entries)
        self.statusBar().showMessage(
            f"{len(self.filtered_entries)} of {len(self.all_entries)} entries / category: {category}"
        )

    def current_entry(self) -> SourceBrowserEntry | None:
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return None
        return self.model.entry_at(indexes[0].row())

    def selection_changed(self) -> None:
        entry = self.current_entry()
        self.detail.show_entry(entry)
        self.detail.setVisible(entry is not None)

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

    def open_detail_action(self) -> None:
        entry = self.current_entry()
        if entry and entry.image_paths:
            ImageViewerDialog(entry.image_paths).exec()
        else:
            self.detail.show_entry(entry)
            self.detail.setVisible(entry is not None)
