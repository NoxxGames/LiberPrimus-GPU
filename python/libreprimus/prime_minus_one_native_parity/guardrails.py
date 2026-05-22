"""Guardrail records for Stage 5X."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_parity.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_parity.models import COMMON_RECORD_FLAGS, GUARDRAIL_PATH, OUTPUT_DIR, REPORT_FILES


def build_guardrails(*, guardrail_out: Path = GUARDRAIL_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    records = [
        _record("stage5x-ready-mapping-native-only", "native_execution_performed_for_ready_no_gpu_mappings_only", True),
        _record("stage5x-full-p56-blocked", "blocked_full_p56_mapping_not_executed", True),
        _record("stage5x-no-cuda", "cuda_execution_source_changes_and_new_kernels_disabled", True),
        _record("stage5x-no-benchmark", "gpu_benchmark_speedup_and_performance_claims_disabled", True),
        _record("stage5x-no-raw-unsolved", "raw_data_canonical_corpus_page_boundaries_and_unsolved_scope_disabled", True),
        _record("stage5x-no-publication-solve", "generated_body_publication_method_upgrade_and_solve_claims_disabled", True),
        _record("stage5x-no-cxx-python-workers", "cxx_launches_python_workers_false", True),
    ]
    write_records(guardrail_out, records)
    write_json_report(out_dir, REPORT_FILES["guardrail"], {"records": records})
    return records


def _record(guardrail_id: str, guardrail_status: str, enforced: bool) -> dict[str, Any]:
    return {
        **COMMON_RECORD_FLAGS,
        "record_type": "prime_minus_one_native_guardrail_record",
        "schema": "schemas/cuda/prime-minus-one-native-guardrail-record-v0.schema.json",
        "guardrail_id": guardrail_id,
        "guardrail_status": guardrail_status,
        "enforced": enforced,
        "native_execution_performed": True,
        "python_reference_execution_performed": True,
        "native_cpu_execution_performed": False,
    }
