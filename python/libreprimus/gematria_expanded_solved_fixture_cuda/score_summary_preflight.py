"""Build Stage 5R score-summary preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_expanded_solved_fixture_cuda.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expanded_solved_fixture_cuda.models import COMMON_POLICY_FLAGS, OUTPUT_DIR, PARITY_RECORDS_PATH, SCORE_SUMMARY_CONTRACT, SCORE_SUMMARY_PREFLIGHT_PATH, SCORE_SUMMARY_PREFLIGHT_REPORT, STAGE4I_CONFIDENCE_LABELS


def build_score_summary_preflight(
    *,
    parity_records: Path = PARITY_RECORDS_PATH,
    confidence_labels: Path = STAGE4I_CONFIDENCE_LABELS,
    score_summary_preflight_out: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    labels = {str(record["label"]) for record in read_yaml(confidence_labels).get("records", [])}
    confidence_label = "scoring_not_available"
    if confidence_label not in labels:
        raise ValueError("Stage 4I confidence labels must include scoring_not_available")
    records = [
        _record(index=index, parity=record, confidence_label=confidence_label)
        for index, record in enumerate(sorted(read_record_set(parity_records), key=lambda item: str(item["parity_record_id"])))
    ]
    write_record_set(score_summary_preflight_out, records)
    write_report(out_dir, SCORE_SUMMARY_PREFLIGHT_REPORT, {"records": records})
    return records


def _record(*, index: int, parity: dict[str, Any], confidence_label: str) -> dict[str, Any]:
    ready = parity["parity_status"] == "passed"
    record = {
        "record_type": "gematria_expanded_solved_fixture_score_summary_preflight_record",
        "score_summary_preflight_id": f"stage5r-score-summary-preflight-{index:02d}",
        "parity_record_id": parity["parity_record_id"],
        "fixture_id": parity["fixture_id"],
        "candidate_id": parity["candidate_id"],
        "source_input_stream_id": parity["source_input_stream_id"],
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "score_interpretation": "triage_only",
        "stage4i_confidence_labels_only": True,
        "new_scorer_added": False,
        "score_summary_shape_status": "ready_for_stage5s_compact_summary_integration" if ready else "blocked_parity_not_clean",
        "confidence_label": confidence_label,
        "score_status": "scoring_not_available",
        "score_components": [],
        "score_summary_available": False,
        "score_as_solve_evidence_allowed": False,
        "output_token_hash": parity.get("stage5r_cuda_output_token_hash"),
        "method_status_upgrade_allowed": False,
        "stage5s_ready": ready,
        "cuda_execution_performed": parity["cuda_execution_performed"],
        "solved_fixture_cuda_used": parity["solved_fixture_cuda_used"],
    }
    record.update(COMMON_POLICY_FLAGS)
    record["cuda_execution_performed"] = parity["cuda_execution_performed"]
    record["solved_fixture_cuda_used"] = parity["solved_fixture_cuda_used"]
    return record
