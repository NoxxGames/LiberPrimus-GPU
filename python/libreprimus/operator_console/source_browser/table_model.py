"""Qt table model for Source Browser entries."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from .entries import SourceBrowserEntry


class SourceBrowserTableModel(QAbstractTableModel):
    def __init__(self, entries: list[SourceBrowserEntry], columns: list[dict[str, Any]]) -> None:
        super().__init__()
        self.entries = entries
        self.columns = columns

    def rowCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return 0 if parent and parent.isValid() else len(self.entries)

    def columnCount(self, parent: QModelIndex | None = None) -> int:  # noqa: N802
        return 0 if parent and parent.isValid() else len(self.columns)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> object:
        if not index.isValid():
            return None
        entry = self.entries[index.row()]
        key = str(self.columns[index.column()].get("key"))
        if role == Qt.ItemDataRole.DisplayRole:
            return self._display(entry, key)
        if role == Qt.ItemDataRole.ToolTipRole:
            return entry.summary
        return None

    def headerData(  # noqa: N802
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> object:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section].get("label", self.columns[section].get("key", ""))
        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        key = str(self.columns[column].get("key"))
        reverse = order == Qt.SortOrder.DescendingOrder
        self.layoutAboutToBeChanged.emit()
        self.entries.sort(key=lambda entry: self._display(entry, key).lower(), reverse=reverse)
        self.layoutChanged.emit()

    def entry_at(self, row: int) -> SourceBrowserEntry | None:
        if 0 <= row < len(self.entries):
            return self.entries[row]
        return None

    def replace_entries(self, entries: list[SourceBrowserEntry]) -> None:
        self.beginResetModel()
        self.entries = entries
        self.endResetModel()

    def _display(self, entry: SourceBrowserEntry, key: str) -> str:
        if key == "title":
            return entry.title
        if key == "category":
            return entry.category
        if key == "status":
            return entry.source_status or ""
        if key == "images":
            return str(len(entry.image_paths))
        if key == "urls":
            return str(len(entry.urls))
        if key == "number_facts":
            return str(len(entry.number_facts))
        if key == "warnings":
            return str(len(entry.warnings))
        value = getattr(entry, key, "")
        if isinstance(value, list):
            return str(len(value))
        if isinstance(value, dict):
            return str(len(value))
        return "" if value is None else str(value)
