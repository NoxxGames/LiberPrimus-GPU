"""Formula inventory for legacy workbooks."""

from __future__ import annotations

from typing import Any

from openpyxl.cell.cell import Cell

from libreprimus.legacy_workbook.loader import LoadedLegacyWorkbook
from libreprimus.legacy_workbook.models import SOURCE_ID, FormulaRecord


def _formula_text(cell: Cell) -> str | None:
    if isinstance(cell.value, str) and cell.value.startswith("="):
        return cell.value
    return None


def _cached_value(loaded: LoadedLegacyWorkbook, sheet_name: str, cell_coordinate: str) -> Any:
    if sheet_name not in loaded.values.sheetnames:
        return None
    return loaded.values[sheet_name][cell_coordinate].value


def inventory_formulas(loaded: LoadedLegacyWorkbook) -> list[FormulaRecord]:
    """Return one record per formula cell."""
    records: list[FormulaRecord] = []
    for worksheet in loaded.formulas.worksheets:
        for row in worksheet.iter_rows():
            for cell in row:
                formula = _formula_text(cell)
                if formula is None:
                    continue
                records.append(
                    FormulaRecord(
                        record_type="legacy_workbook_formula",
                        source_id=SOURCE_ID,
                        workbook_sha256=loaded.sha256,
                        sheet_name=worksheet.title,
                        cell=cell.coordinate,
                        formula=formula,
                        cached_value=_cached_value(loaded, worksheet.title, cell.coordinate),
                    )
                )
    return records
