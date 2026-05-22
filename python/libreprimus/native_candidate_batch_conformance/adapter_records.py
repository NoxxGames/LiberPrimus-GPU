"""Adapter records for Stage 5V Candidate Batch ABI conformance."""

from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import ADAPTER_RECORDS_PATH, COMMON_FLAGS, OUTPUT_DIR, REPORT_FILES


def build_adapter_records(
    *,
    adapter_records_out: Path = ADAPTER_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = [
        {
            **COMMON_FLAGS,
            "record_type": "native_candidate_batch_adapter_record",
            "schema": "schemas/cuda/native-candidate-batch-adapter-record-v0.schema.json",
            "adapter_id": "stage5v-python-reference-adapter",
            "adapter_kind": "python_reference_adapter",
            "adapter_status": "implemented",
            "implemented_language": "python",
            "supports_shift_mod29": True,
            "supports_token_buffer_shape": True,
            "supports_key_schedule_shape": True,
            "supports_stream_schedule_shape": True,
            "supports_score_vector_shape": True,
            "supports_topk_shape": True,
            "deterministic_ordering": True,
            "generated_body_committed": False,
            "notes": "Pure Python no-GPU reference adapter selected for Stage 5V CI-safe conformance.",
        },
        {
            **COMMON_FLAGS,
            "record_type": "native_candidate_batch_adapter_record",
            "schema": "schemas/cuda/native-candidate-batch-adapter-record-v0.schema.json",
            "adapter_id": "stage5v-cpp-reference-adapter",
            "adapter_kind": "cpp_reference_adapter",
            "adapter_status": "deferred",
            "implemented_language": "cpp",
            "supports_shift_mod29": False,
            "supports_token_buffer_shape": False,
            "supports_key_schedule_shape": False,
            "supports_stream_schedule_shape": False,
            "supports_score_vector_shape": False,
            "supports_topk_shape": False,
            "deterministic_ordering": False,
            "generated_body_committed": False,
            "blockers": ["deferred_to_avoid_invasive_cpp_changes_in_stage5v"],
            "notes": "C++ Candidate Batch ABI adapter remains pending; no C++ or CUDA source was changed.",
        },
    ]
    write_record_set(adapter_records_out, records)
    write_report(out_dir, REPORT_FILES["native_adapter"], {"records": records, "count": len(records)})
    return records
