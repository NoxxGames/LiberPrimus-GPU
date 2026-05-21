"""Build Stage 5N result-store and score-summary preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda_reporting.export import common_policy_fields, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_reporting.models import (
    OUTPUT_DIR,
    RESULT_STORE_CONTRACT,
    RESULT_STORE_PREFLIGHT_JSON,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_CONTRACT,
    STAGE4P_SUMMARY,
)


def build_result_store_preflight(
    *,
    stage4p_summary: Path = STAGE4P_SUMMARY,
    result_store_preflight_out: Path = RESULT_STORE_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    stage4p_present = _resolve(stage4p_summary).is_file()
    records = [
        {
            "record_type": "gematria_cuda_result_store_preflight_record",
            "preflight_record_id": "stage5n-result-store-preflight-00",
            "preflight_kind": "result_store",
            "result_source_kind": "solved_fixture_safe_cuda_parity",
            "stage4p_compatibility_required": True,
            "stage4p_summary_path": str(stage4p_summary),
            "stage4p_summary_present": stage4p_present,
            "stage4i_confidence_labels_only": True,
            "confidence_label_interpretation": "triage_only",
            "output_token_hash_required": True,
            "output_text_hash_status": "blocked_until_transliteration_policy_explicit",
            "generated_raw_result_bodies_ignored": True,
            "method_status_upgrade_allowed": False,
            "preflight_status": "ready_for_stage5o_result_store_preflight" if stage4p_present else "blocked_missing_stage4p_summary",
            "result_store_contract": RESULT_STORE_CONTRACT,
            "score_summary_contract": SCORE_SUMMARY_CONTRACT,
            **common_policy_fields(),
        },
        {
            "record_type": "gematria_cuda_result_store_preflight_record",
            "preflight_record_id": "stage5n-score-summary-preflight-00",
            "preflight_kind": "score_summary",
            "result_source_kind": "solved_fixture_safe_cuda_parity",
            "stage4p_compatibility_required": True,
            "stage4p_summary_path": str(stage4p_summary),
            "stage4p_summary_present": stage4p_present,
            "stage4i_confidence_labels_only": True,
            "confidence_label_interpretation": "triage_only",
            "output_token_hash_required": True,
            "output_text_hash_status": "blocked_until_transliteration_policy_explicit",
            "generated_raw_result_bodies_ignored": True,
            "method_status_upgrade_allowed": False,
            "preflight_status": "ready_for_stage5o_score_summary_preflight" if stage4p_present else "blocked_missing_stage4p_summary",
            "result_store_contract": RESULT_STORE_CONTRACT,
            "score_summary_contract": SCORE_SUMMARY_CONTRACT,
            **common_policy_fields(),
        },
    ]
    write_record_set(result_store_preflight_out, records)
    write_report(out_dir, RESULT_STORE_PREFLIGHT_JSON, {"records": records})
    return records


def _resolve(path: Path) -> Path:
    from libreprimus.benchmark_planning.export import resolve_repo_path

    return resolve_repo_path(path)
