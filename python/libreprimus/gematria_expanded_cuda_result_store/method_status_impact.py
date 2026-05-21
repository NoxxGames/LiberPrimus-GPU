"""Build Stage 5S method-status impact records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import write_record_set, write_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    COMMON_FLAGS,
    METHOD_STATUS_IMPACT_PATH,
    METHOD_STATUS_REPORT_JSON,
    OUTPUT_DIR,
)

_IMPACTS = (
    ("gematria_mod29_shift_score_kernel", "caesar_mod29", "expanded_parity_verified_infrastructure_only"),
    ("direct_translation", "direct_translation", "not_upgraded_mapped_fixture_source_only"),
    ("reverse_gematria", "reverse_gematria", "unaffected"),
    ("rotated_reverse_gematria", "rotated_reverse_gematria", "unaffected"),
    ("vigenere_explicit_key", "vigenere", "unaffected"),
    ("prime_minus_one_stream", "prime_minus_one_stream", "unaffected"),
    ("stage5q_blocked_original_family_fixtures", "original_transform_family_contracts", "remain_blocked_pending_separate_contracts"),
)


def build_method_status_impact(
    *,
    method_status_impact_out: Path = METHOD_STATUS_IMPACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [_record(index=index, subject=subject, family=family, status=status) for index, (subject, family, status) in enumerate(_IMPACTS)]
    write_record_set(method_status_impact_out, records)
    write_report(out_dir, METHOD_STATUS_REPORT_JSON, {"records": records})
    return records


def _record(*, index: int, subject: str, family: str, status: str) -> dict[str, Any]:
    record = {
        "record_type": "gematria_expanded_cuda_method_status_impact_record",
        "method_status_impact_id": f"stage5s-method-status-impact-{index:02d}",
        "method_subject": subject,
        "method_family": family,
        "impact_status": status,
        "method_status_before": "infrastructure_or_existing_status_preserved",
        "method_status_after": "infrastructure_or_existing_status_preserved",
        "method_status_upgrade_allowed": False,
        "method_status_upgraded": False,
        "upgraded_to_solved": False,
        "reason": "Stage 5S integrates parity metadata only; parity success is not solve evidence or original-family validation.",
        "unsolved_page_family_activated": False,
        "broad_solved_fixture_expansion_approved": False,
    }
    record.update(COMMON_FLAGS)
    return record
