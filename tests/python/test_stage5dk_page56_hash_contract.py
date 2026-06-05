from __future__ import annotations

from libreprimus.token_block import stage5dk
from test_stage5dk_common import ensure_stage5dk_built, load_yaml, write_temp_yaml


def test_stage5dk_page56_hash_contract_preserves_unknown_algorithm_and_preimage() -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/project-state/stage5dk-page56-hash-contract-refinement.yaml")

    assert record["page56_hash_hex"] == stage5dk.PAGE56_HASH_HEX
    assert record["page56_hash_hex_length"] == 128
    assert record["page56_hash_byte_length"] == 64
    assert record["page56_hash_bit_length"] == 512
    assert record["page56_hash_algorithm_known"] is False
    assert record["page56_hash_preimage_known"] is False
    assert record["hash_preimage_search_performed"] is False
    assert record["dwh_hash_search_performed"] is False
    assert record["target_class_validation_implemented"] is False
    assert record["tor_network_access_performed"] is False
    assert "unknown_or_custom_512_bit_hash" in record["possible_algorithms"]
    assert "dht_or_freenet_gnunet_p2p_identifier" in record["possible_preimage_classes"]


def test_stage5dk_page56_validator_rejects_hash_change(monkeypatch: object, tmp_path) -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/project-state/stage5dk-page56-hash-contract-refinement.yaml")
    record["page56_hash_hex"] = "0" * 128
    path = write_temp_yaml(tmp_path / "hash-contract.yaml", record)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "page56_hash_contract_refinement", path)

    result = stage5dk.validate_stage5dk_page56_hash_contract()
    assert result.validation_error_count > 0
    assert any("page56_hash_changed" in error for error in result.errors)


def test_stage5dk_page56_validator_rejects_algorithm_preimage_and_search_claims(
    monkeypatch: object,
    tmp_path,
) -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/project-state/stage5dk-page56-hash-contract-refinement.yaml")
    record["page56_hash_algorithm_known"] = True
    record["page56_hash_preimage_known"] = True
    record["hash_preimage_search_performed"] = True
    record["target_class_validation_implemented"] = True
    path = write_temp_yaml(tmp_path / "hash-contract.yaml", record)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "page56_hash_contract_refinement", path)

    result = stage5dk.validate_stage5dk_page56_hash_contract()
    assert result.validation_error_count > 0
    assert any("page56_hash_algorithm_known_must_be_false" in error for error in result.errors)
    assert any("page56_hash_preimage_known_must_be_false" in error for error in result.errors)
    assert any("hash_preimage_search_performed_must_be_false" in error for error in result.errors)
    assert any(
        "target_class_validation_implemented_must_be_false" in error for error in result.errors
    )
