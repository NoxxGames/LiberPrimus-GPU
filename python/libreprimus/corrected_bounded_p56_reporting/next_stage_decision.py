"""Build Stage 5AE next-stage decision records."""

from __future__ import annotations

from pathlib import Path

from .models import NEXT_STAGE_DECISION_PATH, OUTPUT_DIR, REPORT_FILES
from .records import build_next_stage_decision_records, write_record_group


def build_next_stage_decision(
    *,
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_next_stage_decision_records(),
        next_stage_decision_out,
        out_dir,
        REPORT_FILES["next_stage"],
    )
