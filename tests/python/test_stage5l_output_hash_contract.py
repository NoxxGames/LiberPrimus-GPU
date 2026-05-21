from __future__ import annotations

from libreprimus.gematria_solved_fixture_mapping.export import read_record_set
from libreprimus.paths import repo_root


def test_output_hash_contract_requires_candidate_major_ordering() -> None:
    records = read_record_set(repo_root() / "data/cuda/stage5l-gematria-solved-fixture-output-hash-contract.yaml")
    assert records[0]["candidate_ordering_required"] == "candidate-major"
    assert records[0]["output_token_hash_required"] is True
    assert records[0]["separator_metadata_required"] is True
    assert records[0]["token_kind_metadata_required"] is True
