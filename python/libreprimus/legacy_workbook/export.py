"""High-level legacy workbook extraction and export."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from libreprimus.legacy_workbook.delta_extract import extract_solved_deltas
from libreprimus.legacy_workbook.formulas import inventory_formulas
from libreprimus.legacy_workbook.inventory import inventory_sheets
from libreprimus.legacy_workbook.loader import load_legacy_workbook
from libreprimus.legacy_workbook.models import (
    SOURCE_ID,
    WarningRecord,
    WorkbookExtraction,
    WorkbookSummary,
    to_jsonable,
)
from libreprimus.legacy_workbook.prime_sums import extract_prime_sums


def _warning_messages(warnings: Iterable[WarningRecord]) -> list[str]:
    return [warning.message for warning in warnings]


def extract_workbook(path: Path) -> WorkbookExtraction:
    """Run all non-canonical legacy workbook extractors."""
    loaded = load_legacy_workbook(path)

    sheet_records, inventory_warnings = inventory_sheets(loaded)
    delta_records, delta_warnings = extract_solved_deltas(loaded)
    prime_sum_records, prime_warnings = extract_prime_sums(loaded)
    formula_records = inventory_formulas(loaded)
    warning_records = inventory_warnings + delta_warnings + prime_warnings

    summary = WorkbookSummary(
        record_type="legacy_workbook_summary",
        source_id=SOURCE_ID,
        workbook_sha256=loaded.sha256,
        workbook_path=str(loaded.path),
        sheet_count=len(sheet_records),
        sheet_names=[record.sheet_name for record in sheet_records],
        total_delta_records=len(delta_records),
        total_prime_sum_records=len(prime_sum_records),
        total_formula_records=len(formula_records),
        warnings=_warning_messages(warning_records),
        canonical_corpus_allowed=False,
        trusted_as_canonical=False,
    )

    return WorkbookExtraction(
        sheet_records=sheet_records,
        delta_records=delta_records,
        prime_sum_records=prime_sum_records,
        formula_records=formula_records,
        warning_records=warning_records,
        summary=summary,
    )


def write_json(path: Path, payload: Any) -> None:
    """Write deterministic JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(to_jsonable(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, records: Iterable[Any]) -> None:
    """Write deterministic JSON Lines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(to_jsonable(record), sort_keys=True, ensure_ascii=False))
            handle.write("\n")


def write_extraction(out_dir: Path, extraction: WorkbookExtraction) -> dict[str, Path]:
    """Write all generated extraction files to an ignored output directory."""
    paths = {
        "sheet_inventory": out_dir / "sheet_inventory.json",
        "solved_delta_rows": out_dir / "solved_delta_rows.jsonl",
        "prime_sum_rows": out_dir / "prime_sum_rows.jsonl",
        "formula_cells": out_dir / "formula_cells.jsonl",
        "summary": out_dir / "summary.json",
        "warnings": out_dir / "warnings.jsonl",
    }
    write_json(paths["sheet_inventory"], extraction.sheet_records)
    write_jsonl(paths["solved_delta_rows"], extraction.delta_records)
    write_jsonl(paths["prime_sum_rows"], extraction.prime_sum_records)
    write_jsonl(paths["formula_cells"], extraction.formula_records)
    write_json(paths["summary"], extraction.summary)
    write_jsonl(paths["warnings"], extraction.warning_records)
    return paths
