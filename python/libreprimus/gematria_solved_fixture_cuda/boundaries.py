"""Build Stage 5M CUDA boundary records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda.models import BOUNDARY_RECORDS_PATH, BOUNDARY_REPORT, COMMON_POLICY_FLAGS, OUTPUT_DIR, RUN_RECORDS_PATH


def build_boundary_records(
    *,
    run_records: Path = RUN_RECORDS_PATH,
    boundaries_out: Path = BOUNDARY_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = read_record_set(run_records)
    attempted_count = sum(1 for record in records if record.get("cuda_run_attempted") is True)
    boundary = {
        "record_type": "gematria_solved_fixture_cuda_boundary_record",
        "boundary_record_id": "stage5m-solved-fixture-cuda-boundary",
        "approved_scope": "exact_five_stage5l_mapped_solved_fixture_safe_token_buffers",
        "mapping_count": len(records),
        "cuda_attempted_count": attempted_count,
        "allowed_mapping_ids": [record["mapping_id"] for record in records],
        "prohibited_inputs": [
            "unsolved_pages",
            "raw_liber_primus_page_text",
            "canonical_corpus_material",
            "raw_discord_logs",
            "raw_page_images",
            "raw_stego_audio",
        ],
        "no_benchmark_boundary": True,
        "no_speedup_claim_boundary": True,
        "no_new_kernel_boundary": True,
        "host_runner_only_source_change": True,
        **COMMON_POLICY_FLAGS,
        "cuda_source_modified": True,
        "cuda_source_modification_scope": "stage5m_host_runner_only_no_device_arithmetic_change",
    }
    write_record_set(boundaries_out, [boundary])
    write_report(out_dir, BOUNDARY_REPORT, {"records": [boundary]})
    return [boundary]
