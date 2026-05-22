"""Build Stage 4I-compatible score-vector contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import COMMON_FLAGS, OUTPUT_DIR, SCORE_VECTOR_CONTRACT_PATH, SCORE_VECTOR_REPORT_JSON


def build_score_vector_contract(
    *,
    score_vector_contract_out: Path = SCORE_VECTOR_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Define triage-only score-vector components for future backends."""

    rows = [
        ("output_token_hash", "sha256_hex", "64 lowercase hex chars", "required_compact_hash"),
        ("score_status", "enum", "scored|scoring_not_available|calibration_not_available|scorer_error", "required_status"),
        ("confidence_label", "stage4i_enum", "Stage 4I finite labels plus scoring_not_available", "finite_triage_only"),
        ("triage_label", "string_enum", "triage_only_no_solve_label", "finite_triage_only"),
        ("optional_ngram_score_placeholder", "nullable_float", "placeholder_not_execution_ready", "placeholder"),
        ("optional_crib_score_placeholder", "nullable_float", "placeholder_not_execution_ready", "placeholder"),
        ("optional_dictionary_score_placeholder", "nullable_float", "placeholder_not_execution_ready", "placeholder"),
    ]
    records = [
        {
            "record_type": "score_vector_contract_record",
            "score_vector_contract_id": f"stage5u-score-vector-{index:02d}",
            "score_summary_contract": "stage4i",
            "supported_score_components": [component],
            "score_component_id": component,
            "score_value_type": value_type,
            "score_value_domain": domain,
            "missing_score_policy": missing_policy,
            "confidence_label_policy": "stage4i_finite_triage_labels_only",
            "triage_only": True,
            "candidate_ordering": "candidate_major",
            "topk_compatible": True,
            "method_status_upgrade_allowed": False,
            "performance_claim_allowed": False,
            "solve_claim": False,
            "execution_ready": missing_policy != "placeholder",
            **COMMON_FLAGS,
        }
        for index, (component, value_type, domain, missing_policy) in enumerate(rows)
    ]
    write_record_set(score_vector_contract_out, records)
    write_report(out_dir, SCORE_VECTOR_REPORT_JSON, {"records": records})
    return records
