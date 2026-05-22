from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_host_runner_not_implemented_and_no_cpp_python_worker_launch(
    tmp_path: Path,
) -> None:
    record = _records(_build_all(tmp_path)["host"])[0]
    assert record["host_runner_status"] == "contract_only_not_implemented"
    assert record["cxx_launches_python_workers"] is False
    assert record["cuda_host_runner_implemented"] is False
    assert record["host_runner_implemented"] is False
    assert record["cuda_execution_allowed"] is False
    assert record["result_store_summary_policy"] == "compact_summary_only"
