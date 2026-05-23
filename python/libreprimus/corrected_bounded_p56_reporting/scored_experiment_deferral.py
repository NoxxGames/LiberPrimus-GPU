"""Build Stage 5AE scored-experiment deferral records."""

from __future__ import annotations

from pathlib import Path

from .models import OUTPUT_DIR, REPORT_FILES, SCORED_EXPERIMENT_DEFERRAL_PATH
from .records import build_scored_experiment_deferral_records, write_record_group


def build_scored_experiment_deferral(
    *,
    scored_experiment_deferral_out: Path = SCORED_EXPERIMENT_DEFERRAL_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_scored_experiment_deferral_records(),
        scored_experiment_deferral_out,
        out_dir,
        REPORT_FILES["scored_experiment"],
    )
