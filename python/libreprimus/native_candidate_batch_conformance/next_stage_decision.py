"""Next-stage decision records for Stage 5V."""

from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import COMMON_FLAGS, NEXT_STAGE_DECISION_PATH, NEXT_STAGE_REASON, NEXT_STAGE_TITLE, OUTPUT_DIR, REPORT_FILES


def build_next_stage_decision(
    *,
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    options = [
        ("stage5w_prime_minus_one_stream_native_contract", "selected", NEXT_STAGE_TITLE, NEXT_STAGE_REASON),
        (
            "stage5w_explicit_key_vigenere_native_contract",
            "deferred",
            "Stage 5W - explicit-key Vigenere native parity contract preparation",
            "Key-schedule shape is valid, but stream conformance is the higher-ranked Stage 5T family.",
        ),
        (
            "stage5w_affine_reverse_native_contract",
            "deferred",
            "Stage 5W - affine/reverse native parity contract preparation",
            "Affine/reverse formulas need a family-specific contract before execution semantics widen.",
        ),
        (
            "stage5w_topk_reducer_contract",
            "deferred",
            "Stage 5W - top-k reducer native contract preparation",
            "Top-k shape is deterministic but reducers should wait for family score vectors.",
        ),
        (
            "stage5w_native_cpp_adapter_gap_closure",
            "deferred",
            "Stage 5W - native C++ Candidate Batch ABI adapter gap closure",
            "Pure Python conformance is sufficient for Stage 5V; C++ can be added later if scoped.",
        ),
        (
            "stage5w_cuda_kernel_implementation",
            "blocked",
            "Stage 5W - CUDA kernel implementation",
            "CUDA kernels remain blocked until family-specific native contracts are ready.",
        ),
        (
            "stage5w_gpu_benchmark_planning",
            "blocked",
            "Stage 5W - GPU benchmark planning",
            "Benchmark execution remains blocked; Stage 5V contains no performance evidence.",
        ),
        (
            "stage5w_unsolved_page_cuda",
            "blocked",
            "Stage 5W - unsolved-page CUDA execution",
            "Unsolved pages, raw data, and canonical corpus inputs remain prohibited.",
        ),
        (
            "stage5w_deep_research_review",
            "deferred",
            "Deep Research - Candidate Batch ABI conformance review",
            "No further Deep Research is needed before the next bounded native contract stage.",
        ),
    ]
    records = [
        {
            **COMMON_FLAGS,
            "record_type": "cuda_next_stage_decision_record",
            "schema": "schemas/cuda/cuda-next-stage-decision-record-v0.schema.json",
            "decision_id": option_id,
            "status": status,
            "selected": status == "selected",
            "recommended_prompt_type": "Codex" if status != "blocked" else "none",
            "recommended_stage_title": title,
            "rationale": reason,
            "deep_research_recommended_next": False,
            "cuda_execution_allowed": False,
            "cuda_source_changes_allowed": False,
            "benchmark_execution_allowed": False,
            "unsolved_page_cuda_allowed": False,
            "generated_body_publication_allowed": False,
            "method_status_upgrade_allowed": False,
        }
        for option_id, status, title, reason in options
    ]
    write_record_set(next_stage_decision_out, records)
    write_report(out_dir, REPORT_FILES["next_stage"], {"records": records, "count": len(records)})
    return records
