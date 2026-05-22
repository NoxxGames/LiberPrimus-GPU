"""Build backend-surface contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import BACKEND_REPORT_JSON, BACKEND_SURFACE_CONTRACT_PATH, COMMON_FLAGS, OUTPUT_DIR


def build_backend_surface_contract(
    *,
    backend_surface_contract_out: Path = BACKEND_SURFACE_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Define owner and validation boundaries for backend surfaces."""

    rows = [
        (
            "python_orchestration_surface",
            "python",
            "active_contract_owner",
            "owns manifests, provenance, validation, result-store writes, and report generation",
            ["candidate_batch_abi_v0", "token_buffer_contract"],
            ["compact_yaml_records", "ignored_json_reports"],
            "validates all contracts before any future backend execution",
            False,
            False,
        ),
        (
            "native_cpp_reference_surface",
            "native_cpp",
            "future_reference_adapter",
            "may own deterministic CPU conformance in Stage 5V",
            ["candidate_batch_abi_v0", "token_buffer_contract", "transform_parameter_contract"],
            ["native_conformance_hashes_future"],
            "must prove no-GPU conformance before family-specific CUDA contracts",
            False,
            False,
        ),
        (
            "cuda_host_runner_surface",
            "cuda_host",
            "future_marshalling_only",
            "may marshal buffers only after explicit future scope",
            ["candidate_batch_abi_v0", "backend_surface_contract"],
            ["compact_run_metadata_future"],
            "must not run CUDA in Stage 5U",
            False,
            True,
        ),
        (
            "cuda_device_kernel_surface",
            "cuda_device",
            "future_c_style_kernel_abi",
            "must operate over explicit buffers and counts using conservative CUDA-C style",
            ["token_buffer_contract", "transform_parameter_contract"],
            ["output_token_buffer_future", "score_vector_future"],
            "must satisfy parity and device-code subset checks in a future stage",
            False,
            True,
        ),
        (
            "result_store_surface",
            "python_result_store",
            "compact_metadata_only",
            "receives compact metadata only unless future policy changes",
            ["candidate_batch_result_store_compatibility"],
            ["compact_summary_metadata"],
            "must reject generated body publication",
            False,
            False,
        ),
        (
            "score_summary_surface",
            "python_scoring",
            "stage4i_compatible",
            "preserves finite triage-only labels",
            ["score_vector_contract"],
            ["stage4i_score_summary_shape"],
            "must not invent scorer semantics",
            False,
            False,
        ),
        (
            "generated_body_policy_surface",
            "policy",
            "blocked",
            "keeps full generated token/text bodies ignored and unpublished",
            ["candidate_batch_abi_v0"],
            ["compact_hashes_only"],
            "must keep generated outputs uncommitted",
            False,
            False,
        ),
    ]
    records = [
        {
            "record_type": "backend_surface_contract_record",
            "backend_surface_id": surface_id,
            "owner_layer": owner,
            "current_status": status,
            "future_status": future_status,
            "input_contracts": input_contracts,
            "output_contracts": output_contracts,
            "validation_responsibility": validation,
            "allowed_to_execute_cuda": False,
            "allowed_to_write_generated_bodies": False,
            "allowed_to_commit_compact_records": True,
            "allowed_to_upgrade_method_status": False,
            "requires_no_gpu_ci_compatibility": True,
            "requires_cuda_c_subset": requires_cuda_c_subset,
            "cxx_launches_python_workers": False,
            "allowed_execution_status": "no_execution_in_stage5u" if not future_cuda else "future_explicit_scope_only",
            "generated_body_policy": "compact_hashes_only",
            "result_store_policy": "compact_summary_metadata_only",
            **COMMON_FLAGS,
        }
        for surface_id, owner, status, future_status, input_contracts, output_contracts, validation, future_cuda, requires_cuda_c_subset in rows
    ]
    write_record_set(backend_surface_contract_out, records)
    write_report(out_dir, BACKEND_REPORT_JSON, {"records": records})
    return records
