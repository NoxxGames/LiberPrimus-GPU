from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_contract.source_inventory import build_source_inventory


def test_stage5w_source_inventory_consumes_stage5v_and_abi_sources(tmp_path: Path) -> None:
    records = build_source_inventory(source_inventory_out=tmp_path / "source.yaml", out_dir=tmp_path)
    paths = " ".join(record["source_path"] for record in records)
    assert "stage5v-native-candidate-batch-conformance-summary.yaml" in paths
    assert "stage5u-stream-schedule-contract.yaml" in paths
    assert all(record["raw_data_required"] is False for record in records)
    assert all(record["committed_safe_source"] is True for record in records)


def test_stage5w_source_inventory_does_not_invent_full_p56_tokens(tmp_path: Path) -> None:
    records = build_source_inventory(source_inventory_out=tmp_path / "source.yaml", out_dir=tmp_path)
    fixture_record = next(record for record in records if record["source_inventory_id"] == "stage5w-source-p56-fixture-json")
    mapping_record = next(record for record in records if record["source_inventory_id"] == "stage5w-source-stage5l-p56-token-mapping")
    assert fixture_record["token_values_available"] is False
    assert any("full_cipher_token_buffer_not_committed" in blocker for blocker in fixture_record["blockers"])
    assert mapping_record["token_values_available"] is True
    assert mapping_record["token_count"] == 2
