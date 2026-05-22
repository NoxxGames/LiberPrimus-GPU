"""Build Stage 5Z host-runner contract records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import HOST_RUNNER_CONTRACT_PATH, HOST_RUNNER_ID, OUTPUT_DIR, base_record


def build_host_runner_contract(
    host_runner_contract_out: Path = HOST_RUNNER_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    record = base_record(
        "prime_minus_one_cuda_host_runner_contract_record",
        "schemas/cuda/prime-minus-one-cuda-host-runner-contract-record-v0.schema.json",
        host_runner_contract_record_id="stage5z-prime-minus-one-host-runner-contract-v0",
        host_runner_contract_id=HOST_RUNNER_ID,
        host_runner_status="contract_only_not_implemented",
        host_orchestration="python",
        cxx_launches_python_workers=False,
        cxx_backend_implemented=False,
        cuda_host_runner_implemented=False,
        input_validation_required=True,
        output_hash_policy="host_side_sha256_canonical_json_v1",
        result_store_summary_policy="compact_summary_only",
        generated_body_publication_allowed=False,
        cuda_execution_allowed=False,
        benchmark_allowed=False,
        implementation_allowed=False,
    )
    records = [record]
    write_records(host_runner_contract_out, records)
    write_json_report(out_dir, "host_runner_contract_report.json", {"records": records})
    return records
