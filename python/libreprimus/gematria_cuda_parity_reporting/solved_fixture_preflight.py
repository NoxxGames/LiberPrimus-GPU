"""Solved-fixture-safe preflight records for Stage 5K."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_cuda_parity_reporting.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_cuda_parity_reporting.models import (
    COMMON_POLICY_FLAGS,
    NEXT_STAGE_WITH_BLOCKERS,
    OUTPUT_DIR,
    PREFLIGHT_BLOCKERS,
    PREFLIGHT_JSON,
    PREFLIGHT_PATH,
    STAGE4O_SOLVED_FIXTURE_MANIFEST,
    STAGE5H_MAPPING_PATH,
)


def build_solved_fixture_preflight(
    *,
    mapping_path: Path = STAGE5H_MAPPING_PATH,
    stage4o_manifest_path: Path = STAGE4O_SOLVED_FIXTURE_MANIFEST,
    preflight_out: Path = PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    mapping_records = read_record_set(mapping_path)
    stage4o_manifest = read_yaml(stage4o_manifest_path)
    streams = {stream["input_stream_id"]: stream for stream in stage4o_manifest.get("input_streams", [])}
    candidates = _candidate_by_stream(stage4o_manifest.get("transform_candidates", []))
    records: list[dict[str, Any]] = []
    for index, mapping in enumerate(mapping_records):
        stream_id = str(mapping.get("source_input_stream_id", ""))
        stream = streams.get(stream_id, {})
        candidate = candidates.get(stream_id, {})
        blockers = list(PREFLIGHT_BLOCKERS)
        record: dict[str, Any] = {
            "record_type": "gematria_solved_fixture_safe_preflight_record",
            "preflight_id": f"stage5k-solved-fixture-safe-preflight-{index:02d}",
            "mapping_id": str(mapping.get("mapping_id", "")),
            "candidate_source_stage": "stage-4o/stage-5h",
            "source_manifest": str(stage4o_manifest_path).replace("\\", "/"),
            "source_input_stream_id": stream_id,
            "fixture_id": str(mapping.get("fixture_id", stream.get("fixture_id", ""))),
            "transform_family": str(candidate.get("transform_family", "unknown")),
            "candidate_id": str(candidate.get("candidate_id", "")),
            "token_domain_compatibility": "blocked_needs_exact_gematria_0_28_mapping",
            "separator_policy_compatibility": "declared_needs_result_record_shape",
            "expected_cpu_native_parity_source": "stage5h-native-fixture-plus-stage4o-parity-expectation",
            "stage4o_parity_expectation_link": "required_before_future_cuda_execution",
            "score_summary_parity_requirements": [
                "future CUDA output_token_hash must match CPU/native output_token_hash",
                "confidence labels must remain Stage 4I triage-only labels",
            ],
            "readiness_status": "needs_token_mapping",
            "blockers": blockers,
            "blocker_count": len(blockers),
            "solved_fixture_stream_token_count": int(stream.get("token_count", 0)),
            "solved_fixture_stream_transformable_token_count": int(stream.get("transformable_token_count", 0)),
            "recommended_next_stage": NEXT_STAGE_WITH_BLOCKERS,
            "notes": [
                "This record is a future bounded verifier candidate only.",
                "Stage 5K does not run solved fixtures through CUDA.",
            ],
            **COMMON_POLICY_FLAGS,
        }
        records.append(record)
    write_record_set(preflight_out, records)
    write_report(out_dir, PREFLIGHT_JSON, {"records": records})
    return records


def _candidate_by_stream(candidates: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(candidates, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        stream_id = str(candidate.get("input_stream_id", ""))
        if stream_id and stream_id not in result:
            result[stream_id] = candidate
    return result
