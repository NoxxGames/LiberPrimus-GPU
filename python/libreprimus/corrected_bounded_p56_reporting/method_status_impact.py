"""Build Stage 5AE method-status impact records."""

from __future__ import annotations

from pathlib import Path

from .models import METHOD_STATUS_IMPACT_PATH, OUTPUT_DIR, REPORT_FILES
from .records import build_method_status_impact_records, write_record_group


def build_method_status_impact(
    *,
    method_status_impact_out: Path = METHOD_STATUS_IMPACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_method_status_impact_records(),
        method_status_impact_out,
        out_dir,
        REPORT_FILES["method_status"],
    )
