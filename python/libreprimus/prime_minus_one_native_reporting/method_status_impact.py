"""Build Stage 5Y method-status impact records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_reporting.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_reporting.models import COMMON_RECORD_FLAGS, METHOD_STATUS_IMPACT_PATH, OUTPUT_DIR, REPORT_FILES


IMPACTS = [
    (
        "prime_minus_one_stream",
        "infrastructure_only",
        "Stage 5Y reports bounded no-GPU native parity only; this is not a solve status upgrade.",
    ),
    (
        "p56_bounded_prime_minus_one",
        "infrastructure_only",
        "Bounded p56 native parity carries a known solved-fixture-safe hash check; full p56 remains blocked.",
    ),
    (
        "gematria_shift_score_only",
        "infrastructure_only",
        "Shift-score parity remains control/infrastructure context and not original transform-family verification.",
    ),
    (
        "prime_minus_one_cuda_contract",
        "readiness_metadata_only",
        "CUDA contract preparation may become ready as metadata only; kernel implementation remains blocked.",
    ),
    (
        "unsolved_page_cuda",
        "blocked",
        "Unsolved-page CUDA remains blocked pending canonical corpus, page-boundary, source-lock, null-control, and operator gates.",
    ),
]


def build_method_status_impact(
    *,
    method_status_impact_out: Path = METHOD_STATUS_IMPACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = []
    for method_family_id, impact_status, rationale in IMPACTS:
        records.append(
            {
                **COMMON_RECORD_FLAGS,
                "record_type": "prime_minus_one_native_method_status_impact_record",
                "schema": "schemas/cuda/prime-minus-one-native-method-status-impact-record-v0.schema.json",
                "impact_record_id": f"stage5y-method-impact-{method_family_id}",
                "method_family_id": method_family_id,
                "method_status_impact": impact_status,
                "method_status_upgraded": False,
                "method_status_upgrade_allowed": False,
                "marked_solved": False,
                "solve_claim": False,
                "rationale": rationale,
            }
        )
    write_records(method_status_impact_out, records)
    write_json_report(out_dir, REPORT_FILES["method_status"], {"records": records})
    return records
