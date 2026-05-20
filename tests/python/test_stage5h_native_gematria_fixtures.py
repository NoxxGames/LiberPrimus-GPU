from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_shift_contract.native_fixture_records import fixture_expected_hash


def test_stage5h_native_fixture_hash_is_deterministic() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5h-gematria-native-parity-fixtures.yaml").read_text(encoding="utf-8"))["records"][0]
    expected_hash = fixture_expected_hash(record["input_tokens"], record["expected_outputs"])
    assert record["expected_output_hash"] == expected_hash


def test_stage5h_native_fixture_is_not_stage5f_hash() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5h-gematria-native-parity-fixtures.yaml").read_text(encoding="utf-8"))["records"][0]
    assert record["stage5f_hash_is_gematria_fixture_hash"] is False
    assert record["expected_output_hash"] != record["stage5f_synthetic_hash"]
