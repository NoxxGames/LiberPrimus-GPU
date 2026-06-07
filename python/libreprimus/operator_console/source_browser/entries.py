"""Normalized Source Browser entry model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SourceBrowserEntry:
    entry_id: str
    entry_type: str
    category: str
    title: str
    summary: str
    stage_id: str | None
    record_type: str | None
    candidate_family_id: str | None
    source_type: str | None
    source_status: str | None
    trust_tier: str | None
    confidence: str | None
    selected_now: bool | None
    solve_claim: bool | None
    execution_allowed: bool | None
    source_lock_only: bool | None
    local_paths: list[str] = field(default_factory=list)
    image_paths: list[str] = field(default_factory=list)
    document_paths: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    hashes: dict[str, str] = field(default_factory=dict)
    number_facts: list[dict[str, Any]] = field(default_factory=list)
    links_to: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: str | None = None
    created_at: str | None = None
    modified_at: str | None = None
    source_record_path: str = ""
    schema_path: str | None = None
    raw_record: dict[str, Any] = field(default_factory=dict)

    def to_dict(self, include_raw: bool = True) -> dict[str, Any]:
        payload = asdict(self)
        if not include_raw:
            payload.pop("raw_record", None)
        return payload

    @property
    def file_count(self) -> int:
        return len(set(self.local_paths + self.document_paths + self.image_paths))

    @property
    def warning_count(self) -> int:
        return len(self.warnings)
