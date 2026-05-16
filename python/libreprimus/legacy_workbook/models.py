"""Data models for non-canonical legacy workbook extraction."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SOURCE_ID = "legacy-google-sheet-1JwbWW04y1Fy5Qvwca7B2e3dsFWd5rf3NSorFj53IBNE"
LOCAL_FILENAME = "tranlsations.xlsx"

KNOWN_GIDS: dict[str, str] = {
    "629803470": "README",
    "137197189": "Prime Sums",
    "0": "A Warning",
    "126279850": "Some Wisdom",
    "2124456769": "Welcome",
    "1187777662": "A Koan A Man",
    "592446840": "The Loss Of",
    "1421979231": "A Koan During",
    "1360576785": "An Instruction",
    "480300769": "p57 Parable",
    "2053328121": "p56 An End",
}

KNOWN_SHEETS = tuple(KNOWN_GIDS.values())
SOLVED_DELTA_SHEETS = tuple(name for name in KNOWN_SHEETS if name not in {"README", "Prime Sums"})


def to_jsonable(value: Any) -> Any:
    """Convert dataclasses and paths into JSON-serializable values."""
    if hasattr(value, "__dataclass_fields__"):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    return value


@dataclass(frozen=True)
class WarningRecord:
    record_type: str
    source_id: str
    workbook_sha256: str
    sheet_name: str | None
    message: str
    cell: str | None = None
    line_label: str | None = None
    row: int | None = None


@dataclass(frozen=True)
class SheetRecord:
    record_type: str
    source_id: str
    workbook_sha256: str
    sheet_index: int
    sheet_name: str
    max_row: int
    max_column: int
    non_empty_cell_count: int
    formula_cell_count: int
    classification: str
    trusted_as_canonical: bool
    trusted_as_solved_fixture_hint: bool
    first_non_empty_cell: str | None = None
    first_non_empty_row: int | None = None
    first_non_empty_value: str | None = None


@dataclass(frozen=True)
class SolvedDeltaRecord:
    record_type: str
    source_id: str
    workbook_sha256: str
    sheet_name: str
    sheet_index: int
    line_label: str
    line_number: int | None
    position_in_line: int
    source_row: int
    source_column: int
    cipher_rune: str | None
    cipher_index: int | None
    message_token: str | None
    message_index: int | None
    cipher_minus_message_mod29: int | None
    message_minus_cipher_mod29: int | None
    trusted_as_canonical: bool
    trusted_as_solved_fixture_hint: bool


@dataclass(frozen=True)
class PrimeSumRecord:
    record_type: str
    source_id: str
    workbook_sha256: str
    sheet_name: str
    text_row: int
    value_row: int
    sequence_index: int
    tokens: list[str]
    prime_values: list[int]
    sum: int | None
    is_prime: bool | None
    trusted_as_canonical: bool
    raw_is_prime: str | None = None


@dataclass(frozen=True)
class FormulaRecord:
    record_type: str
    source_id: str
    workbook_sha256: str
    sheet_name: str
    cell: str
    formula: str
    cached_value: Any


@dataclass(frozen=True)
class WorkbookSummary:
    record_type: str
    source_id: str
    workbook_sha256: str
    workbook_path: str
    sheet_count: int
    sheet_names: list[str]
    total_delta_records: int
    total_prime_sum_records: int
    total_formula_records: int
    warnings: list[str] = field(default_factory=list)
    canonical_corpus_allowed: bool = False
    trusted_as_canonical: bool = False


@dataclass(frozen=True)
class WorkbookExtraction:
    sheet_records: list[SheetRecord]
    delta_records: list[SolvedDeltaRecord]
    prime_sum_records: list[PrimeSumRecord]
    formula_records: list[FormulaRecord]
    warning_records: list[WarningRecord]
    summary: WorkbookSummary
