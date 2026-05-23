"""Build Stage 5AE hash-material policy records."""

from __future__ import annotations

from pathlib import Path

from .models import HASH_MATERIAL_POLICY_PATH, OUTPUT_DIR, REPORT_FILES
from .records import build_hash_material_policy_records, write_record_group


def build_hash_material_policy(
    *,
    hash_material_policy_out: Path = HASH_MATERIAL_POLICY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_hash_material_policy_records(),
        hash_material_policy_out,
        out_dir,
        REPORT_FILES["hash_material"],
    )
