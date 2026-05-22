from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.transform_parameter_contract import build_transform_parameter_contract


def test_stage5u_transform_parameters_cover_existing_families_without_implementation(tmp_path: Path) -> None:
    records = build_transform_parameter_contract(
        transform_parameter_contract_out=tmp_path / "params.yaml",
        out_dir=tmp_path / "reports",
    )
    families = {record["family_id"]: record for record in records}
    assert {"shift_mod29", "reverse_gematria", "rotated_reverse_gematria", "affine_mod29", "vigenere_explicit_key", "prime_minus_one_stream"} == set(families)
    assert families["vigenere_explicit_key"]["requires_key_schedule"] is True
    assert families["prime_minus_one_stream"]["requires_stream_schedule"] is True
    assert families["shift_mod29"]["contract_status"] == "defined_for_existing_gematria_shift_score_control"
    assert all(record["implementation_allowed_now"] is False for record in records)
