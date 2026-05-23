"""Build Stage 5AE score-summary integration records."""

from __future__ import annotations

from pathlib import Path

from .models import OUTPUT_DIR, REPORT_FILES, SCORE_SUMMARY_INTEGRATION_PATH
from .records import build_score_summary_integration_records, write_record_group


def build_score_summary_integration(
    *,
    score_summary_integration_out: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_score_summary_integration_records(),
        score_summary_integration_out,
        out_dir,
        REPORT_FILES["score_summary"],
    )
