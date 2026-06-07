"""Add/modify/remove dialogs for Source Browser entries."""

from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QVBoxLayout,
)

from .entries import SourceBrowserEntry


class AddModifyDialog(QDialog):
    def __init__(self, entry: SourceBrowserEntry | None = None, committed: bool = False) -> None:
        super().__init__()
        self.setWindowTitle("Modify entry" if entry else "Add entry")
        self.entry = entry
        self.committed = committed
        layout = QVBoxLayout(self)
        if committed:
            layout.addWidget(QLabel("Committed records are read-only. Saving creates a manual override."))
        form = QFormLayout()
        self.title = QLineEdit(entry.title if entry else "")
        self.category = QComboBox()
        self.category.addItems(
            [
                "Manual entries",
                "Source-locks",
                "Candidate families",
                "Number facts",
                "Images",
                "Documents",
                "References",
                "Warnings",
                "Mayfly",
                "Dots",
                "Cover geometry",
            ]
        )
        if entry:
            index = self.category.findText(entry.category)
            if index >= 0:
                self.category.setCurrentIndex(index)
        self.entry_type = QLineEdit(entry.entry_type if entry else "manual_note")
        self.status = QLineEdit(entry.source_status or "" if entry else "review_note")
        self.trust = QLineEdit(entry.trust_tier or "" if entry else "operator_local")
        self.confidence = QLineEdit(entry.confidence or "" if entry else "not_applicable")
        self.summary = QPlainTextEdit(entry.summary if entry else "")
        self.candidate = QLineEdit(entry.candidate_family_id or "" if entry else "")
        self.stage_id = QLineEdit(entry.stage_id or "" if entry else "")
        self.local_paths = QPlainTextEdit("\n".join(entry.local_paths) if entry else "")
        self.image_paths = QPlainTextEdit("\n".join(entry.image_paths) if entry else "")
        self.document_paths = QPlainTextEdit("\n".join(entry.document_paths) if entry else "")
        self.urls = QPlainTextEdit("\n".join(entry.urls) if entry else "")
        self.number_facts = QPlainTextEdit("\n".join(str(item) for item in entry.number_facts) if entry else "")
        self.links_to = QPlainTextEdit("\n".join(entry.links_to) if entry else "")
        self.warnings = QPlainTextEdit("\n".join(entry.warnings) if entry else "")
        self.notes = QPlainTextEdit(entry.notes or "" if entry else "")
        for label, widget in [
            ("Title", self.title),
            ("Category", self.category),
            ("Entry type", self.entry_type),
            ("Status", self.status),
            ("Trust tier", self.trust),
            ("Confidence", self.confidence),
            ("Summary", self.summary),
            ("Candidate family", self.candidate),
            ("Stage ID", self.stage_id),
            ("Local paths", self.local_paths),
            ("Image paths", self.image_paths),
            ("Document paths", self.document_paths),
            ("URLs", self.urls),
            ("Number facts", self.number_facts),
            ("Links to entries", self.links_to),
            ("Warnings", self.warnings),
            ("Notes", self.notes),
        ]:
            form.addRow(label, widget)
        layout.addLayout(form)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def fields(self) -> dict[str, Any]:
        return {
            "title": self.title.text(),
            "category": self.category.currentText(),
            "entry_type": self.entry_type.text(),
            "status": self.status.text(),
            "trust_tier": self.trust.text(),
            "confidence": self.confidence.text(),
            "summary": self.summary.toPlainText(),
            "candidate_family_links": self._lines(self.candidate.text()),
            "stage_id": self.stage_id.text(),
            "local_paths": self._lines(self.local_paths.toPlainText()),
            "image_paths": self._lines(self.image_paths.toPlainText()),
            "document_paths": self._lines(self.document_paths.toPlainText()),
            "urls": self._lines(self.urls.toPlainText()),
            "number_facts": self._lines(self.number_facts.toPlainText()),
            "links_to": self._lines(self.links_to.toPlainText()),
            "warnings": self._lines(self.warnings.toPlainText()),
            "notes": self.notes.toPlainText(),
        }

    def _lines(self, value: str) -> list[str]:
        return [line.strip() for line in value.splitlines() if line.strip()]


def confirm_remove(entry: SourceBrowserEntry) -> bool:
    message = QMessageBox()
    message.setWindowTitle("Delete / hide entry")
    message.setText("Are you sure you want to remove this entry from the browser?")
    if entry.record_type != "source_browser_manual_entry":
        message.setInformativeText(
            "This will hide the record in the browser by creating a tombstone. "
            "It will not delete the committed source-lock record."
        )
    message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    return message.exec() == QMessageBox.StandardButton.Yes
