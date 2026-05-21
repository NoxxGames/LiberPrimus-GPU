"""Build Stage 5P Stage 4I-compatible score-summary integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_cuda_result_store.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_cuda_result_store.loaders import load_stage4i_confidence_labels
from libreprimus.gematria_cuda_result_store.models import (
    COMMON_POLICY_FLAGS,
    OUTPUT_DIR,
    RESULT_STORE_INTEGRATION_PATH,
    SCORE_SUMMARY_CONTRACT,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORE_SUMMARY_INTEGRATION_REPORT,
    STAGE4I_CONFIDENCE_LABELS,
)


def build_score_summary_integration(
    *,
    result_store_integration: Path = RESULT_STORE_INTEGRATION_PATH,
    confidence_labels: Path = STAGE4I_CONFIDENCE_LABELS,
    score_summary_integration_out: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build triage-only score-summary views over compact CUDA parity records."""

    labels = load_stage4i_confidence_labels(confidence_labels)
    confidence_label = "scoring_not_available"
    if confidence_label not in labels:
        raise ValueError("Stage 4I confidence labels must include scoring_not_available")
    records: list[dict[str, Any]] = []
    for index, integration in enumerate(
        sorted(read_record_set(result_store_integration), key=lambda item: str(item["result_store_integration_id"]))
    ):
        records.append(
            {
                "record_type": "gematria_cuda_score_summary_integration_record",
                "score_summary_integration_id": f"stage5p-score-summary-integration-{index:02d}",
                "result_store_integration_id": integration["result_store_integration_id"],
                "fixture_id": integration["fixture_id"],
                "candidate_id": integration["candidate_id"],
                "mapping_id": integration["mapping_id"],
                "source_transform_family": integration["source_transform_family"],
                "score_summary_contract": SCORE_SUMMARY_CONTRACT,
                "score_status": "scoring_not_available",
                "confidence_label": confidence_label,
                "confidence_interpretation": "triage_only",
                "score_components": [],
                "score_summary_available": False,
                "score_summary_shape_status": "stage4i_compatible_no_score",
                "score_summary_integration_status": "integrated_triage_only",
                "scoring_reason": "Stage 5P integrates parity metadata only and does not add a scoring model.",
                "output_token_hash": integration["output_token_hash"],
                "output_text_hash": integration.get("output_text_hash"),
                "output_text_hash_status": integration.get("output_text_hash_status"),
                "score_as_solve_evidence_allowed": False,
                **COMMON_POLICY_FLAGS,
            }
        )
    write_record_set(score_summary_integration_out, records)
    write_report(out_dir, SCORE_SUMMARY_INTEGRATION_REPORT, {"records": records})
    return records
