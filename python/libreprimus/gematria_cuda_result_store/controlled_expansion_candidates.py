"""Build Stage 5P controlled expansion candidate records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_cuda_result_store.export import write_record_set, write_report
from libreprimus.gematria_cuda_result_store.models import (
    COMMON_POLICY_FLAGS,
    CONTROLLED_EXPANSION_CANDIDATE_REPORT,
    CONTROLLED_EXPANSION_CANDIDATES_PATH,
    NEXT_STAGE_READY,
    OUTPUT_DIR,
)


def build_controlled_expansion_candidates(
    *,
    controlled_expansion_candidates_out: Path = CONTROLLED_EXPANSION_CANDIDATES_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Record Stage 5Q candidate classes without executing CUDA."""

    rows = [
        (
            "stage5p-expansion-exact-repeat-pack",
            "exact_stage5o_repeat_pack",
            "consumed_passed",
            "No additional execution is required for the exact Stage 5O repeat pack.",
            "no_action",
        ),
        (
            "stage5p-expansion-additional-shift-score-fixtures",
            "additional_solved_fixture_shift_score_candidates",
            "ready_for_stage5q_candidate_mapping",
            "A future stage may map additional solved-fixture-safe shift_score candidates before any CUDA run.",
            NEXT_STAGE_READY,
        ),
        (
            "stage5p-expansion-original-transform-cuda",
            "additional_original_transform_family_cuda_candidates",
            "blocked_requires_separate_kernel_contract",
            "Original transform families need separate CPU/CUDA contracts before CUDA execution.",
            "Stage 5Q - original-transform CUDA contract review",
        ),
        (
            "stage5p-expansion-broad-solved-campaign",
            "broad_solved_fixture_cuda_campaign",
            "blocked_broad_scope",
            "A broad solved-fixture CUDA campaign is outside the compact integration scope.",
            "no_action",
        ),
        (
            "stage5p-expansion-unsolved-cuda",
            "unsolved_page_cuda",
            "blocked_unsolved",
            "Unsolved-page CUDA remains blocked until later parity, benchmarks, and approvals exist.",
            "no_action",
        ),
        (
            "stage5p-expansion-result-store-integration",
            "result_store_and_score_summary_integration",
            "complete",
            "Stage 5P completes compact result-store and score-summary integration.",
            NEXT_STAGE_READY,
        ),
    ]
    records: list[dict[str, Any]] = []
    for candidate_id, candidate_class, status, rationale, next_stage in rows:
        records.append(
            {
                "record_type": "gematria_cuda_controlled_expansion_candidate_record",
                "controlled_expansion_candidate_id": candidate_id,
                "candidate_class": candidate_class,
                "candidate_status": status,
                "candidate_rationale": rationale,
                "recommended_next_stage": next_stage,
                "requires_new_cuda_kernel": False,
                "requires_cuda_execution": False,
                "requires_benchmark": False,
                "requires_unsolved_page_input": False,
                "guardrails": [
                    "solved_fixture_safe_only",
                    "no_cuda_execution_in_stage5p",
                    "compact_metadata_only",
                    "generated_bodies_ignored",
                    "no_method_status_upgrade_by_parity_alone",
                ],
                **COMMON_POLICY_FLAGS,
            }
        )
    write_record_set(controlled_expansion_candidates_out, records)
    write_report(out_dir, CONTROLLED_EXPANSION_CANDIDATE_REPORT, {"records": records})
    return records
