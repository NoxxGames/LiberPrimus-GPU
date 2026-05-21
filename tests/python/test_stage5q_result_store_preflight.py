from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_expansion_candidate_mapping.candidate_inventory import build_candidate_inventory
from libreprimus.gematria_expansion_candidate_mapping.native_parity import build_native_parity_records
from libreprimus.gematria_expansion_candidate_mapping.result_store_preflight import build_result_store_preflight_records
from libreprimus.gematria_expansion_candidate_mapping.token_mapping import build_token_mapping_records


def test_stage5q_result_store_preflight_is_stage4p_stage4i_compatible(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.yaml"
    mapping = tmp_path / "mapping.yaml"
    native = tmp_path / "native.yaml"
    preflight = tmp_path / "preflight.yaml"
    build_candidate_inventory(candidate_inventory_out=inventory, out_dir=tmp_path / "inventory-out")
    build_token_mapping_records(candidate_inventory=inventory, token_mapping_out=mapping, out_dir=tmp_path / "mapping-out")
    build_native_parity_records(token_mapping=mapping, native_parity_out=native, out_dir=tmp_path / "native-out")

    records = build_result_store_preflight_records(
        token_mapping=mapping,
        native_parity=native,
        result_store_preflight_out=preflight,
        out_dir=tmp_path / "preflight-out",
    )

    assert len(records) == 3
    assert all(record["preflight_status"] == "ready_for_future_result_store_integration" for record in records)
    assert all(record["stage4p_compatibility"] is True for record in records)
    assert all(record["stage4i_compatibility"] is True for record in records)
    assert all(record["confidence_interpretation"] == "triage_only" for record in records)
    assert all(record["generated_body_publication_allowed"] is False for record in records)
