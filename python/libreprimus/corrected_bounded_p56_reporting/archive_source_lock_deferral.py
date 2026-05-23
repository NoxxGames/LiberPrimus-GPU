"""Build Stage 5AE archive/source-lock deferral records."""

from __future__ import annotations

from pathlib import Path

from .models import ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH, OUTPUT_DIR, REPORT_FILES
from .records import build_archive_source_lock_deferral_records, write_record_group


def build_archive_source_lock_deferral(
    *,
    archive_source_lock_deferral_out: Path = ARCHIVE_SOURCE_LOCK_DEFERRAL_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_archive_source_lock_deferral_records(),
        archive_source_lock_deferral_out,
        out_dir,
        REPORT_FILES["archive_source_lock"],
    )
