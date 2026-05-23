"""Build Stage 5AE result-store integration records."""

from __future__ import annotations

from pathlib import Path

from .models import OUTPUT_DIR, REPORT_FILES, RESULT_STORE_INTEGRATION_PATH
from .records import build_result_store_integration_records, write_record_group


def build_result_store_integration(
    *,
    result_store_integration_out: Path = RESULT_STORE_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_result_store_integration_records(),
        result_store_integration_out,
        out_dir,
        REPORT_FILES["result_store"],
    )
