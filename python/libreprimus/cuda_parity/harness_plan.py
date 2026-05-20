"""Build Stage 5B CUDA parity harness plan records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_parity.export import write_empty_warnings, write_record_set, write_report
from libreprimus.cuda_parity.fixture_builder import build_parity_fixtures
from libreprimus.cuda_parity.loaders import load_records, record_by
from libreprimus.cuda_parity.models import (
    CUDA_PARITY_POLICY,
    HARNESS_PLAN_PATH,
    HARNESS_REPORT,
    PARITY_FIXTURES_PATH,
    STAGE5A_PARITY_SCAFFOLD_PATH,
    STAGE5A_TARGET_PLAN_PATH,
    STAGE5B_OUTPUT_DIR,
)


def build_harness_plan(
    *,
    target_plan_path: Path = STAGE5A_TARGET_PLAN_PATH,
    parity_scaffold_path: Path = STAGE5A_PARITY_SCAFFOLD_PATH,
    out_dir: Path = STAGE5B_OUTPUT_DIR,
    harness_plan_out: Path = HARNESS_PLAN_PATH,
    parity_fixtures_out: Path = PARITY_FIXTURES_PATH,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    targets = load_records(target_plan_path)
    scaffolds = record_by(load_records(parity_scaffold_path), "target_id")
    fixtures = build_parity_fixtures(
        target_plan_path=target_plan_path,
        parity_scaffold_path=parity_scaffold_path,
        out_dir=out_dir,
        parity_fixtures_out=parity_fixtures_out,
    )
    fixture_by_target = record_by(fixtures, "stage5a_target_id")
    records = [_harness_for_target(target, scaffolds.get(str(target.get("target_id"))), fixture_by_target) for target in targets]
    write_record_set(harness_plan_out, records)
    write_report(out_dir, HARNESS_REPORT, {"records": records})
    write_empty_warnings(out_dir)
    return records, fixtures


def _harness_for_target(
    target: dict[str, object],
    scaffold: dict[str, object] | None,
    fixture_by_target: dict[str, dict[str, object]],
) -> dict[str, object]:
    target_id = str(target.get("target_id"))
    status = str(target.get("target_status"))
    if status == "ready_for_planning":
        harness_status = "ready_for_future_kernel"
        cpu_present = True
    elif status == "non_cuda_target":
        harness_status = "skipped_non_target"
        cpu_present = False
    else:
        harness_status = "blocked"
        cpu_present = False
    fixture = fixture_by_target.get(target_id, {})
    return {
        "record_type": "cuda_parity_harness_record",
        "stage_id": "stage-5b",
        "harness_id": f"{target_id}-harness",
        "stage5a_target_id": target_id,
        "stage5a_parity_scaffold_id": str(scaffold.get("scaffold_id")) if scaffold else "",
        "stage4o_parity_expectation_reference": str(target.get("stage4o_parity_expectation_id") or ""),
        "stage4p_unified_result_reference": str(target.get("stage4p_unified_result_reference") or ""),
        "parity_fixture_id": str(fixture.get("fixture_id") or ""),
        "transform_family": str(target.get("transform_family") or ""),
        "harness_status": harness_status,
        "cpu_reference_required": True,
        "cpu_reference_present": cpu_present,
        "expected_future_backend_family": "cuda_batch_transform_score",
        "required_output_comparisons": [
            "output_token_hash_exact",
            "output_text_hash_exact_when_applicable",
            "score_summary_shape_exact",
            "score_summary_label_compatible",
            "top_k_ordering_deterministic_when_present",
        ],
        "blocked_conditions": list(target.get("blockers") or []),
        "vram_profile": "compatibility_8gb" if status == "ready_for_planning" else "not_applicable",
        "local_16gb_profile_required": False,
        **CUDA_PARITY_POLICY,
    }
