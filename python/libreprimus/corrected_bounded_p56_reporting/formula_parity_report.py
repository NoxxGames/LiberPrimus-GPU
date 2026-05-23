"""Build Stage 5AE corrected formula-parity report records."""

from __future__ import annotations

from pathlib import Path

from .models import FORMULA_PARITY_REPORT_PATH, OUTPUT_DIR, REPORT_FILES, SOURCE_SUMMARY_PATH
from .records import build_formula_parity_records, write_record_group


def build_formula_parity_report(
    *,
    stage5ad_fix_summary: Path = SOURCE_SUMMARY_PATH,
    formula_parity_report_out: Path = FORMULA_PARITY_REPORT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_formula_parity_records(stage5ad_fix_summary),
        formula_parity_report_out,
        out_dir,
        REPORT_FILES["formula_parity"],
    )
