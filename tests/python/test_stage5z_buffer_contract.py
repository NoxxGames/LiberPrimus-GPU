from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records


def test_stage5z_buffer_contract_covers_required_buffers(tmp_path: Path) -> None:
    records = _records(_build_all(tmp_path)["buffer"])
    names = {record["buffer_name"] for record in records}
    assert {
        "token_values",
        "transformable_mask",
        "fixture_offsets_lengths",
        "stream_schedule_values",
        "candidate_fixture_stream_refs",
        "output_tokens",
        "status_codes",
        "output_hash_policy",
    } <= names
    assert all(record["cuda_c_style_subset"] is True for record in records)
    assert all(record["implementation_allowed"] is False for record in records)
    assert all(record["cuda_execution_allowed"] is False for record in records)
