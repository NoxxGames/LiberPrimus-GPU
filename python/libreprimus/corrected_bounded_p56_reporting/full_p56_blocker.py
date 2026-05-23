"""Build Stage 5AE full-p56 blocker records."""

from __future__ import annotations

from pathlib import Path

from .models import FULL_P56_BLOCKER_PATH, OUTPUT_DIR, REPORT_FILES
from .records import build_full_p56_blocker_records, write_record_group


def build_full_p56_blocker(
    *,
    full_p56_blocker_out: Path = FULL_P56_BLOCKER_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_full_p56_blocker_records(),
        full_p56_blocker_out,
        out_dir,
        REPORT_FILES["full_p56"],
    )
