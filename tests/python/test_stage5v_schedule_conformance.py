from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.fixtures import build_conformance_fixtures
from libreprimus.native_candidate_batch_conformance.schedule_conformance import build_schedule_conformance


def test_stage5v_variable_length_fixture_offsets_validate(tmp_path: Path) -> None:
    fixtures = build_conformance_fixtures(conformance_fixtures_out=tmp_path / "fixtures.yaml", out_dir=tmp_path / "out")
    variable = next(record for record in fixtures if record["fixture_id"] == "stage5v-variable-length-fixture-pack")
    token_count = len(variable["token_values"])
    for offset, length in zip(variable["fixture_offsets"], variable["fixture_lengths"], strict=True):
        assert offset + length <= token_count


def test_stage5v_schedule_conformance_is_shape_only_without_family_execution(tmp_path: Path) -> None:
    records = build_schedule_conformance(schedule_conformance_out=tmp_path / "schedule.yaml", out_dir=tmp_path / "out")
    assert len(records) == 2
    assert all(record["conformance_status"] == "shape_only" for record in records)
    assert any(record["schedule_kind"] == "vigenere_key_schedule" for record in records)
    assert any(record["schedule_kind"] == "prime_minus_one_stream_schedule" for record in records)
