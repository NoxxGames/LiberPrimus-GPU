"""Solved-fixture-safe mapping records for future Gematria CUDA parity."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_shift_contract.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_shift_contract.models import COMMON_POLICY_FLAGS, MAPPING_JSON, MAPPING_PATH, OUTPUT_DIR, PREFLIGHT_BLOCKERS, STAGE4O_SOLVED_FIXTURE_MANIFEST
from libreprimus.paths import repo_root


def build_solved_fixture_mapping_records(
    *,
    manifest: Path = STAGE4O_SOLVED_FIXTURE_MANIFEST,
    mapping_out: Path = MAPPING_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build blocked solved-fixture-safe mapping records from Stage 4O fixture streams."""

    payload = read_yaml(manifest)
    manifest_label = _repo_relative_label(manifest)
    streams = [
        dict(stream)
        for stream in payload.get("input_streams", [])
        if isinstance(stream, dict) and stream.get("source_kind") == "solved_fixture"
    ]
    records: list[dict[str, Any]] = []
    for index, stream in enumerate(streams):
        records.append(
            {
                "record_type": "gematria_solved_fixture_safe_mapping_record",
                "mapping_id": f"stage5h-solved-fixture-safe-mapping-{index:02d}",
                "source_manifest": manifest_label,
                "source_input_stream_id": str(stream.get("input_stream_id")),
                "fixture_id": str(stream.get("fixture_id")),
                "mapping_status": "blocked_pending_future_stage_approval",
                "readiness_state": "blocked",
                "token_domain_mapping_status": "blocked_needs_explicit_0_28_rune_token_mapping_review",
                "separator_policy_status": "declared_but_not_execution_authorization",
                "stage4o_parity_expectation_linkage": "required_before_future_cuda_execution",
                "preflight_blockers": list(PREFLIGHT_BLOCKERS),
                "preflight_blocker_count": len(PREFLIGHT_BLOCKERS),
                "solved_fixture_stream_token_count": int(stream.get("token_count", 0)),
                "solved_fixture_stream_transformable_token_count": int(stream.get("transformable_token_count", 0)),
                **COMMON_POLICY_FLAGS,
            }
        )
    write_record_set(mapping_out, records)
    write_report(out_dir, MAPPING_JSON, {"records": records})
    write_warnings(out_dir, [] if records else [{"warning": "no solved fixture streams discovered"}])
    return records


def _repo_relative_label(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
