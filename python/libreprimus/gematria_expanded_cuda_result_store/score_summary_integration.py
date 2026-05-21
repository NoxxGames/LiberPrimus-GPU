"""Build Stage 4I-compatible score-summary integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    COMMON_FLAGS,
    CONFIDENCE_INTERPRETATION,
    CONFIDENCE_LABEL,
    OUTPUT_DIR,
    SCORE_SUMMARY_CONTRACT,
    SCORE_SUMMARY_INTEGRATION_PATH,
    SCORE_SUMMARY_REPORT_JSON,
    RESULT_STORE_INTEGRATION_PATH,
    STAGE4I_CONFIDENCE_LABELS,
)
from libreprimus.benchmark_planning.export import read_yaml


def build_score_summary_integration(
    *,
    result_store_integration: Path = RESULT_STORE_INTEGRATION_PATH,
    confidence_labels: Path = STAGE4I_CONFIDENCE_LABELS,
    score_summary_integration_out: Path = SCORE_SUMMARY_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    allowed = {str(record["label"]) for record in read_yaml(confidence_labels).get("records", [])}
    if CONFIDENCE_LABEL not in allowed:
        raise ValueError(f"Stage 4I confidence label missing: {CONFIDENCE_LABEL}")
    result_store = sorted(read_record_set(result_store_integration), key=lambda record: str(record["fixture_id"]))
    records = [_record(index=index, source=record) for index, record in enumerate(result_store)]
    write_record_set(score_summary_integration_out, records)
    write_report(out_dir, SCORE_SUMMARY_REPORT_JSON, {"records": records})
    return records


def _record(*, index: int, source: dict[str, Any]) -> dict[str, Any]:
    record = {
        "record_type": "gematria_expanded_cuda_score_summary_integration_record",
        "score_summary_integration_id": f"stage5s-score-summary-integration-{index:02d}",
        "result_store_integration_id": source["result_store_integration_id"],
        "fixture_id": source["fixture_id"],
        "candidate_inventory_id": source["source_candidate_inventory_id"],
        "candidate_id": source["candidate_id"],
        "scorer_contract": SCORE_SUMMARY_CONTRACT,
        "confidence_label": CONFIDENCE_LABEL,
        "confidence_interpretation": CONFIDENCE_INTERPRETATION,
        "score_or_label_status": "scoring_not_available",
        "output_token_hash": source["stage5r_cuda_hash"],
        "output_text_hash": None,
        "output_text_hash_status": "blocked_pending_transliteration_policy",
        "score_summary_integration_status": "stage4i_compatible_triage_only",
        "parity_correctness_metadata_only": True,
        "does_not_imply_decrypted_plaintext": True,
        "does_not_rank_unsolved_candidates": True,
        "does_not_validate_original_transform_family_semantics": True,
        "cannot_be_cited_as_performance_evidence": True,
    }
    record.update(COMMON_FLAGS)
    return record
