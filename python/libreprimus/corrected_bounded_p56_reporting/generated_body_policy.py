"""Build Stage 5AE generated-body policy records."""

from __future__ import annotations

from pathlib import Path

from .models import GENERATED_BODY_POLICY_PATH, OUTPUT_DIR, REPORT_FILES
from .records import build_generated_body_policy_records, write_record_group


def build_generated_body_policy(
    *,
    generated_body_policy_out: Path = GENERATED_BODY_POLICY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_generated_body_policy_records(),
        generated_body_policy_out,
        out_dir,
        REPORT_FILES["generated_body"],
    )
