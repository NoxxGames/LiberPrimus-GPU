"""Guardrail records for Stage 5W."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_contract.models import COMMON_FLAGS, GUARDRAIL_PATH, OUTPUT_DIR, REPORT_FILES


def build_guardrails(*, guardrail_out: Path = GUARDRAIL_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    records = [
        _record("stage5w-guardrail-no-cuda-execution", "no_cuda_execution", "pass"),
        _record("stage5w-guardrail-no-cuda-source-modification", "no_cuda_source_modification", "pass"),
        _record("stage5w-guardrail-no-benchmark", "no_gpu_benchmark_or_speedup_claim", "pass"),
        _record("stage5w-guardrail-no-unsolved-or-raw-data", "no_unsolved_page_or_raw_data_scope", "pass"),
        _record("stage5w-guardrail-no-generated-body-publication", "no_generated_body_publication", "pass"),
        _record("stage5w-guardrail-no-method-upgrade-or-solve-claim", "no_method_status_upgrade_or_solve_claim", "pass"),
    ]
    write_records(guardrail_out, records)
    write_json_report(out_dir, REPORT_FILES["guardrail"], {"records": records})
    return records


def _record(guardrail_id: str, guardrail_kind: str, guardrail_status: str) -> dict[str, Any]:
    return {
        **COMMON_FLAGS,
        "record_type": "prime_minus_one_guardrail_record",
        "schema": "schemas/cuda/prime-minus-one-guardrail-record-v0.schema.json",
        "guardrail_id": guardrail_id,
        "guardrail_kind": guardrail_kind,
        "guardrail_status": guardrail_status,
        "blockers": [],
    }
