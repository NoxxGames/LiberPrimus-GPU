"""Build Stage 5AE reference-contract repair records."""

from __future__ import annotations

from pathlib import Path

from .models import OUTPUT_DIR, REFERENCE_CONTRACT_REPAIR_PATH, REPORT_FILES
from .records import build_reference_contract_records, write_record_group


def build_reference_contract_repair(
    *,
    reference_contract_repair_out: Path = REFERENCE_CONTRACT_REPAIR_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    return write_record_group(
        build_reference_contract_records(),
        reference_contract_repair_out,
        out_dir,
        REPORT_FILES["reference_contract"],
    )
