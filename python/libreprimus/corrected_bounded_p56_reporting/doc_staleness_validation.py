"""Build Stage 5AE doc-staleness validation records."""

from __future__ import annotations

from pathlib import Path

from .models import DOC_STALENESS_VALIDATION_PATH, OUTPUT_DIR, REPORT_FILES
from .records import build_doc_staleness_validation_records, write_record_group


def build_doc_staleness_validation(
    *,
    doc_staleness_validation_out: Path = DOC_STALENESS_VALIDATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_doc_staleness_validation_records(),
        doc_staleness_validation_out,
        out_dir,
        REPORT_FILES["doc_staleness"],
    )
