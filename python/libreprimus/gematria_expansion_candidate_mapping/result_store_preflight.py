"""Build Stage 5Q result-store and score-summary preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_expansion_candidate_mapping.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expansion_candidate_mapping.models import (
    COMMON_POLICY_FLAGS,
    HASH_ALGORITHM,
    NATIVE_PARITY_PATH,
    OUTPUT_DIR,
    RESULT_STORE_CONTRACT,
    RESULT_STORE_PREFLIGHT_PATH,
    RESULT_STORE_PREFLIGHT_REPORT,
    SCORE_SUMMARY_CONTRACT,
    STAGE4I_CONFIDENCE_LABELS,
    STAGE4P_SUMMARY,
    TOKEN_MAPPING_PATH,
)


def build_result_store_preflight_records(
    *,
    token_mapping: Path = TOKEN_MAPPING_PATH,
    native_parity: Path = NATIVE_PARITY_PATH,
    stage4p_summary: Path = STAGE4P_SUMMARY,
    confidence_labels: Path = STAGE4I_CONFIDENCE_LABELS,
    result_store_preflight_out: Path = RESULT_STORE_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build result-store preflight records for mapped expansion candidates."""

    mappings = {
        str(record["token_mapping_record_id"]): record
        for record in read_record_set(token_mapping)
        if record.get("mapping_status") == "mapped"
    }
    native = {
        str(record["token_mapping_record_id"]): record
        for record in read_record_set(native_parity)
        if record.get("native_parity_status") == "prepared"
    }
    stage4p = read_yaml(stage4p_summary)
    labels = read_yaml(confidence_labels).get("records", [])
    records: list[dict[str, Any]] = []
    for index, mapping_id in enumerate(sorted(mappings)):
        mapping = mappings[mapping_id]
        native_record = native.get(mapping_id)
        blockers: list[str] = []
        if native_record is None:
            blockers.append("blocked_missing_native_parity_hash")
        if stage4p.get("status") != "complete":
            blockers.append("blocked_stage4p_contract_not_complete")
        if not isinstance(labels, list) or not labels:
            blockers.append("blocked_stage4i_confidence_labels_missing")
        output_hash = native_record.get("output_token_hash") if native_record else None
        if not output_hash:
            blockers.append("blocked_missing_output_token_hash")
        status = "ready_for_future_result_store_integration" if not blockers else "blocked"
        records.append(
            {
                "record_type": "gematria_expansion_result_store_preflight_record",
                "result_store_preflight_id": f"stage5q-result-store-preflight-{index:02d}",
                "token_mapping_record_id": mapping_id,
                "native_parity_record_id": native_record["native_parity_record_id"] if native_record else None,
                "fixture_id": mapping["fixture_id"],
                "candidate_id": mapping["candidate_id"],
                "result_source_kind": "controlled_solved_fixture_safe_gematria_shift_score_candidate",
                "result_store_contract": RESULT_STORE_CONTRACT,
                "score_summary_contract": SCORE_SUMMARY_CONTRACT,
                "stage4p_compatibility": not blockers or "blocked_stage4p_contract_not_complete" not in blockers,
                "stage4i_compatibility": not blockers or "blocked_stage4i_confidence_labels_missing" not in blockers,
                "compact_summary_only": True,
                "generated_body_publication_allowed": False,
                "generated_outputs_committed": False,
                "output_token_hash_required": True,
                "output_token_hash": output_hash,
                "output_hash_algorithm": HASH_ALGORITHM,
                "output_text_hash_required": False,
                "confidence_interpretation": "triage_only",
                "confidence_label": "scoring_not_available",
                "score_status": "scoring_not_available",
                "method_status_upgrade_allowed": False,
                "preflight_status": status,
                "blockers": blockers,
                "blocker_count": len(blockers),
                **COMMON_POLICY_FLAGS,
            }
        )
    write_record_set(result_store_preflight_out, records)
    write_report(out_dir, RESULT_STORE_PREFLIGHT_REPORT, {"records": records})
    return records
