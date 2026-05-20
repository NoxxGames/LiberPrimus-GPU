"""Build Stage 5B CUDA parity fixture records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_parity.export import write_record_set, write_report
from libreprimus.cuda_parity.loaders import load_records, record_by
from libreprimus.cuda_parity.models import (
    CUDA_PARITY_POLICY,
    FIXTURE_REPORT,
    PARITY_FIXTURES_PATH,
    STAGE5A_PARITY_SCAFFOLD_PATH,
    STAGE5A_TARGET_PLAN_PATH,
    STAGE5B_OUTPUT_DIR,
)


def build_parity_fixtures(
    *,
    target_plan_path: Path = STAGE5A_TARGET_PLAN_PATH,
    parity_scaffold_path: Path = STAGE5A_PARITY_SCAFFOLD_PATH,
    out_dir: Path = STAGE5B_OUTPUT_DIR,
    parity_fixtures_out: Path = PARITY_FIXTURES_PATH,
) -> list[dict[str, object]]:
    targets = load_records(target_plan_path)
    scaffolds = record_by(load_records(parity_scaffold_path), "target_id")
    records = [_fixture_for_target(target, scaffolds.get(str(target.get("target_id")))) for target in targets]
    write_record_set(parity_fixtures_out, records)
    write_report(out_dir, FIXTURE_REPORT, {"records": records})
    return records


def _fixture_for_target(target: dict[str, object], scaffold: dict[str, object] | None) -> dict[str, object]:
    target_id = str(target.get("target_id"))
    status = str(target.get("target_status"))
    stage4o_ref = str(target.get("stage4o_parity_expectation_id") or "")
    stage4p_ref = str(target.get("stage4p_unified_result_reference") or "")
    if status == "ready_for_planning":
        fixture_status = "ready_for_future_kernel" if stage4o_ref else "blocked_missing_parity_expectation"
        expected_source = "stage4o_parity_expectation" if stage4o_ref else "committed_summary_only"
        cpu_present = True
    elif status == "non_cuda_target":
        fixture_status = "skipped_non_target"
        expected_source = "unavailable"
        cpu_present = False
    else:
        fixture_status = "blocked_target_not_ready"
        expected_source = "unavailable"
        cpu_present = False
    return {
        "record_type": "cuda_parity_fixture_record",
        "stage_id": "stage-5b",
        "fixture_id": f"{target_id}-fixture",
        "stage5a_target_id": target_id,
        "stage5a_parity_scaffold_id": str(scaffold.get("scaffold_id")) if scaffold else "",
        "transform_family": str(target.get("transform_family") or ""),
        "input_stream_class": "stage4o_solved_fixture_safe" if status == "ready_for_planning" else "not_applicable",
        "cpu_reference_required": True,
        "cpu_reference_present": cpu_present,
        "parity_expectation_reference": stage4o_ref,
        "score_summary_reference": stage4p_ref,
        "expected_output_hash_source": expected_source,
        "fixture_status": fixture_status,
        "output_text_hash": str(target.get("output_text_hash") or ""),
        "output_token_hash": str(target.get("output_token_hash") or ""),
        "score_summary_shape_hash": str(target.get("score_summary_shape_hash") or ""),
        "blockers": list(target.get("blockers") or []),
        "vram_profile": "compatibility_8gb" if status == "ready_for_planning" else "not_applicable",
        "local_16gb_profile_required": False,
        **CUDA_PARITY_POLICY,
    }
