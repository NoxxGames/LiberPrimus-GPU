from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_expansion_candidate_mapping.candidate_inventory import build_candidate_inventory
from libreprimus.gematria_expansion_candidate_mapping.native_parity import build_native_parity_records
from libreprimus.gematria_expansion_candidate_mapping.token_mapping import build_token_mapping_records


def test_stage5q_native_parity_prepares_hashes_without_cuda(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.yaml"
    mapping = tmp_path / "mapping.yaml"
    native = tmp_path / "native.yaml"
    build_candidate_inventory(candidate_inventory_out=inventory, out_dir=tmp_path / "inventory-out")
    build_token_mapping_records(candidate_inventory=inventory, token_mapping_out=mapping, out_dir=tmp_path / "mapping-out")

    records = build_native_parity_records(token_mapping=mapping, native_parity_out=native, out_dir=tmp_path / "native-out")
    prepared = [record for record in records if record["native_parity_status"] == "prepared"]
    blocked = [record for record in records if record["native_parity_status"] == "blocked"]

    assert len(prepared) == 3
    assert len(blocked) == 7
    assert all(record["output_token_hash"] for record in prepared)
    assert all(record["candidate_shifts"] == [0, 1, 3, 13, 28] for record in records)
    assert all(record["future_cuda_execution_allowed"] is False for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
    assert all(record["new_cuda_kernels_added"] == 0 for record in records)
