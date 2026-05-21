from __future__ import annotations

from libreprimus.gematria_solved_fixture_mapping.export import read_record_set
from libreprimus.gematria_solved_fixture_mapping.native_parity import build_native_parity_records
from libreprimus.paths import repo_root


def test_native_parity_prepared_records_include_output_hashes() -> None:
    records = read_record_set(repo_root() / "data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml")
    assert len(records) == 5
    assert {record["native_parity_status"] for record in records} == {"prepared"}
    for record in records:
        assert len(record["output_token_hash"]) == 64
        assert record["candidate_ordering"] == "candidate-major"
        assert record["cuda_execution_performed"] is False


def test_blocked_native_parity_record_requires_reason(tmp_path) -> None:
    mapping_path = tmp_path / "mapping.yaml"
    mapping_path.write_text(
        """records:
- mapping_id: blocked
  source_input_stream_id: stream
  fixture_id: fixture
  candidate_id: candidate
  mapping_status: blocked
  blockers:
    - blocked_missing_source_backed_0_28_token_value
""",
        encoding="utf-8",
    )
    records = build_native_parity_records(
        token_mapping=mapping_path,
        native_parity_out=tmp_path / "native.yaml",
        out_dir=tmp_path,
    )
    assert records[0]["native_parity_status"] == "blocked"
    assert records[0]["blockers"]
