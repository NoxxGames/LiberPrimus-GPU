"""Stage 5A non-target CUDA scope records."""

from __future__ import annotations

from typing import Any

from libreprimus.cuda_planning.models import CUDA_PLANNING_POLICY, NON_TARGET_DEFINITIONS


def build_non_target_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for non_target_id, name, reason in NON_TARGET_DEFINITIONS:
        records.append(
            {
                "record_type": "cuda_non_target",
                "stage_id": "stage-5a",
                "non_target_id": f"stage5a-{non_target_id}",
                "name": name,
                "target_status": "non_cuda_target",
                "reason": reason,
                "future_reconsideration_requires": [
                    "explicit future stage scope",
                    "reviewed source/fixture records",
                    "raw/generated output policy",
                    "no solve claim",
                ],
                **CUDA_PLANNING_POLICY,
            }
        )
    return records
