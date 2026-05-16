"""Models for Stage 1C provenance-only reference summaries."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    return value


@dataclass(frozen=True)
class ReferenceMethodNote:
    record_type: str
    reference_source_id: str
    source_sha256: str
    source_local_path: str
    line_number_start: int
    line_number_end: int
    method_family_candidate: str | None
    key_candidate: str | None
    rotation_candidate: int | None
    skip_rule_candidate: str | None
    page_label_candidate: str | None
    raw_excerpt: str
    trusted_as_canonical: bool
    notes: list[str]


@dataclass(frozen=True)
class ToolingReferenceNote:
    record_type: str
    reference_source_id: str
    source_sha256: str
    source_local_path: str
    line_number_start: int
    line_number_end: int
    behaviour_candidate: str
    raw_excerpt: str
    licence_status: str
    imported_as_dependency: bool
    code_copied: bool
    trusted_as_canonical: bool
    notes: list[str]
