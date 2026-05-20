"""Read-only loaders for Stage 5A CUDA planning."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_jsonl, read_yaml, resolve_repo_path
from libreprimus.cuda_planning.models import (
    FALLBACK_SCORE_SUMMARY_SHAPE_HASH,
    FALLBACK_STAGE4O_PARITY_EXPECTATIONS,
    FALLBACK_STAGE4P_UNIFIED_RESULT_ID,
    STAGE4O_PARITY_EXPECTATIONS_PATH,
    STAGE4O_SUMMARY_PATH,
    STAGE4P_SUMMARY_PATH,
    STAGE4P_UNIFIED_RESULTS_PATH,
    STAGE4Q_READINESS_PATH,
    STAGE4Q_SUMMARY_PATH,
)


def load_stage4q_readiness(path: Path = STAGE4Q_READINESS_PATH) -> list[dict[str, Any]]:
    payload = read_yaml(path)
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError(f"Stage 4Q readiness records must be a list: {path}")
    return [record for record in records if isinstance(record, dict)]


def load_stage4q_summary(path: Path = STAGE4Q_SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)


def load_stage4o_summary(path: Path = STAGE4O_SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)


def load_stage4p_summary(path: Path = STAGE4P_SUMMARY_PATH) -> dict[str, Any]:
    return read_yaml(path)


def load_stage4o_parity_expectations(path: Path = STAGE4O_PARITY_EXPECTATIONS_PATH) -> list[dict[str, Any]]:
    resolved = resolve_repo_path(path)
    if resolved.is_file():
        return read_jsonl(path)
    return [
        {
            "candidate_id": candidate_id,
            "transform_family": transform_family,
            "transform_id": transform_family,
            "output_text_hash": output_text_hash,
            "output_token_hash": output_token_hash,
            "score_summary_shape_hash": FALLBACK_SCORE_SUMMARY_SHAPE_HASH,
            "parity_contract_version": "stage4o-cpu-cuda-parity-v0",
            "record_type": "cpu_batch_parity_expectation",
            "cuda_used": False,
            "generated_outputs_committed": False,
            "no_solve_claim": True,
        }
        for candidate_id, transform_family, output_text_hash, output_token_hash in FALLBACK_STAGE4O_PARITY_EXPECTATIONS
    ]


def load_stage4p_unified_results(path: Path = STAGE4P_UNIFIED_RESULTS_PATH) -> list[dict[str, Any]]:
    resolved = resolve_repo_path(path)
    if resolved.is_file():
        return read_jsonl(path)
    return [
        {
            "record_type": "unified_result_record",
            "unified_result_id": FALLBACK_STAGE4P_UNIFIED_RESULT_ID,
            "parity_expectation_id": candidate_id,
            "result_source_kind": "cpu_batch_parity_expectation",
            "source_presence_status": "committed_summary_present",
            "cuda_used": False,
            "generated_outputs_committed": False,
            "solve_claim": False,
        }
        for candidate_id, *_ in FALLBACK_STAGE4O_PARITY_EXPECTATIONS
    ]


def cuda_scaffold_metadata() -> dict[str, Any]:
    root = resolve_repo_path(Path("."))
    cu_files = sorted(
        str(path.relative_to(root)).replace("\\", "/")
        for path in root.glob("cuda/**/*.cu")
        if "build" not in path.parts
    )
    cuh_files = sorted(
        str(path.relative_to(root)).replace("\\", "/")
        for path in root.glob("cuda/**/*.cuh")
        if "build" not in path.parts
    )
    return {
        "cuda_directory_present": (root / "cuda").is_dir(),
        "cmake_cuda_config_present": (root / "cmake" / "CudaConfig.cmake").is_file(),
        "existing_cuda_source_files": cu_files,
        "existing_cuda_header_files": cuh_files,
        "stage5a_cuda_source_added": False,
        "stage5a_cuda_source_modified": False,
    }
