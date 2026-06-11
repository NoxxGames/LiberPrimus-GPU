"""Qt table model for Source Browser entries."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from .entries import SourceBrowserEntry
from .number_facts import NumberFactOverlayCache, number_fact_table_display
from .status_display import STATUS_UNSPECIFIED_TOOLTIP, display_status


class SourceBrowserTableModel(QAbstractTableModel):
    def __init__(self, entries: list[SourceBrowserEntry], columns: list[dict[str, Any]]) -> None:
        super().__init__()
        self.entries = entries
        self.columns = columns
        self._display_cache: dict[tuple[str, str], str] = {}
        self._number_fact_overlay_cache = NumberFactOverlayCache.load()

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
            if key == "status" and not entry.source_status:
                return STATUS_UNSPECIFIED_TOOLTIP
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
        self._display_cache.clear()
        self._number_fact_overlay_cache = NumberFactOverlayCache.load()
        self.endResetModel()

    def _display(self, entry: SourceBrowserEntry, key: str) -> str:
        cache_key = (str(id(entry)), entry.entry_id, key)
        cached = self._display_cache.get(cache_key)
        if cached is not None:
            return cached
        if key == "title":
            value = entry.title
        elif key == "category":
            value = entry.category
        elif key == "status":
            value = display_status(entry.source_status)
        elif key == "images":
            count = len(entry.image_paths)
            value = f"{count} image{'s' if count != 1 else ''}"
        elif key == "document_paths":
            count = len(entry.document_paths)
            value = f"{count} doc{'s' if count != 1 else ''}"
        elif key == "urls":
            count = len(entry.urls)
            value = f"{count} url{'s' if count != 1 else ''}"
        elif key == "number_facts":
            value = number_fact_table_display(entry, overlay_cache=self._number_fact_overlay_cache)
        elif key == "warnings":
            count = len(entry.warnings)
            value = f"{count} warning{'s' if count != 1 else ''}"
        else:
            raw_value = getattr(entry, key, "")
            if isinstance(raw_value, list):
                value = str(len(raw_value))
            elif isinstance(raw_value, dict):
                value = str(len(raw_value))
            else:
                value = "" if raw_value is None else str(raw_value)
        self._display_cache[cache_key] = value
        return value
