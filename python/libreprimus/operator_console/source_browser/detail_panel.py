"""Read-only detail panel for selected Source Browser entries."""

from __future__ import annotations

import yaml
from PySide6.QtWidgets import QPlainTextEdit

from .entries import SourceBrowserEntry


class DetailPanel(QPlainTextEdit):
    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)

    def show_entry(self, entry: SourceBrowserEntry | None) -> None:
        if entry is None:
            self.setPlainText("")
            return
        payload = {
            "title": entry.title,
            "summary": entry.summary,
            "stage": entry.stage_id,
            "record_type": entry.record_type,
            "candidate_family": entry.candidate_family_id,
            "status": entry.source_status,
            "trust": entry.trust_tier,
            "confidence": entry.confidence,
            "local_paths": entry.local_paths,
            "image_paths": entry.image_paths,
            "document_paths": entry.document_paths,
            "urls": entry.urls,
            "number_facts": entry.number_facts,
            "warnings": entry.warnings,
            "links_to": entry.links_to,
            "created_at": entry.created_at,
            "modified_at": entry.modified_at,
            "source_record_path": entry.source_record_path,
            "schema_path": entry.schema_path,
            "raw_record": entry.raw_record,
        }
        self.setPlainText(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False))
