from __future__ import annotations

from libreprimus.gematria_cuda_prep.models import NATIVE_FIXTURE_HASH, STAGE5F_HASH
from libreprimus.gematria_cuda_prep.validation_vectors import build_validation_vector_records


def test_stage5i_validation_vectors_match_stage5h_fixture_hash(tmp_path) -> None:
    record = build_validation_vector_records(validation_vectors_out=tmp_path / "vectors.yaml", out_dir=tmp_path)[0]
    assert record["expected_fixture_hash"] == NATIVE_FIXTURE_HASH
    assert record["expected_fixture_hash"] != STAGE5F_HASH
    assert record["stage5f_hash_is_gematria_fixture_hash"] is False


def test_stage5i_validation_vectors_preserve_separator_positions_by_mask(tmp_path) -> None:
    record = build_validation_vector_records(validation_vectors_out=tmp_path / "vectors.yaml", out_dir=tmp_path)[0]
    assert record["input_token_values"] == [0, 1, 0, 28, 13, 0, 5]
    assert record["transformable_mask"] == [1, 1, 0, 1, 1, 0, 1]
    assert record["separator_positions"] == [2, 5]
    for expected in record["expected_outputs"]:
        assert expected["output_token_values"][2] == 0
        assert expected["output_token_values"][5] == 0
