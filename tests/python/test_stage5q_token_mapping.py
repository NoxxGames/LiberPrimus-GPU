from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_expansion_candidate_mapping.candidate_inventory import build_candidate_inventory
from libreprimus.gematria_expansion_candidate_mapping.token_mapping import build_token_mapping_records


def test_stage5q_token_mapping_maps_only_source_backed_direct_fixtures(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.yaml"
    token_mapping = tmp_path / "token-mapping.yaml"
    build_candidate_inventory(candidate_inventory_out=inventory, out_dir=tmp_path / "inventory-out")

    records = build_token_mapping_records(candidate_inventory=inventory, token_mapping_out=token_mapping, out_dir=tmp_path)
    mapped = [record for record in records if record["mapping_status"] == "mapped"]
    blocked = [record for record in records if record["mapping_status"] != "mapped"]

    assert len(mapped) == 3
    assert len(blocked) == 7
    assert all(record["source_backed_token_values"] is True for record in mapped)
    assert all(record["token_domain"] == "integers_0_to_28" for record in mapped)
    assert all(record["original_transform_family_semantics_exercised"] is False for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
    assert all(record["mapping_hash"] for record in mapped)
    for record in mapped:
        assert len(record["token_values"]) == len(record["transformable_mask"])
        assert any(record["transformable_mask"])


def test_stage5q_token_mapping_preserves_consumed_controls_as_blocked(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.yaml"
    build_candidate_inventory(candidate_inventory_out=inventory, out_dir=tmp_path / "inventory-out")
    records = build_token_mapping_records(candidate_inventory=inventory, token_mapping_out=tmp_path / "mapping.yaml", out_dir=tmp_path)

    consumed = [record for record in records if record["mapping_status"] == "blocked_already_consumed_control"]
    assert len(consumed) == 5
    assert all(record["blockers"] == ["blocked_already_consumed_stage5l_5m_5o_exact_pack"] for record in consumed)
