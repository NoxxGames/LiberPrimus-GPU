"""Stage 5I Gematria CUDA preparation summary generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_yaml
from libreprimus.gematria_cuda_prep.export import read_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_prep.models import (
    ABI_PLAN_PATH,
    CHECKLIST_PATH,
    COMMON_POLICY_FLAGS,
    NATIVE_FIXTURE_HASH,
    NEXT_STAGE,
    OUTPUT_DIR,
    PREPARATION_ID,
    PREPARATION_PATH,
    SUMMARY_JSON,
    SUMMARY_PATH,
    VALIDATION_VECTORS_PATH,
)


def build_summary(
    *,
    preparation_path: Path = PREPARATION_PATH,
    abi_plan_path: Path = ABI_PLAN_PATH,
    validation_vectors_path: Path = VALIDATION_VECTORS_PATH,
    implementation_checklist_path: Path = CHECKLIST_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    """Build the committed Stage 5I aggregate summary."""

    preparations = read_record_set(preparation_path)
    abi_plans = read_record_set(abi_plan_path)
    vectors = read_record_set(validation_vectors_path)
    checklists = read_record_set(implementation_checklist_path)
    stage5j_ready = bool(preparations and abi_plans and vectors and checklists) and all(
        bool(record.get("stage5j_ready_for_synthetic_implementation", True))
        for record in [*preparations, *checklists]
    )
    summary = {
        "record_type": "stage5i_gematria_cuda_preparation_summary",
        "stage_id": "stage-5i",
        "status": "complete",
        "preparation_id": PREPARATION_ID,
        "kernel_preparation_records": len(preparations),
        "abi_plan_records": len(abi_plans),
        "validation_vector_records": len(vectors),
        "implementation_checklist_records": len(checklists),
        "native_fixture_hash": NATIVE_FIXTURE_HASH,
        "gematria_cuda_preparation_complete": True,
        "stage5j_ready_for_synthetic_implementation": stage5j_ready,
        "next_stage": NEXT_STAGE,
        **COMMON_POLICY_FLAGS,
    }
    write_yaml(summary_out, summary)
    write_report(out_dir, SUMMARY_JSON, summary)
    write_warnings(out_dir, [])
    return summary


def load_summary(summary_path: Path = SUMMARY_PATH) -> dict[str, Any]:
    """Load a Stage 5I summary."""

    return read_yaml(summary_path)
