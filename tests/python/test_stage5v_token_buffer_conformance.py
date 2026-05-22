from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.fixtures import build_conformance_fixtures, candidate_major_shift_outputs
from libreprimus.native_candidate_batch_conformance.token_buffer_conformance import build_token_buffer_conformance


def test_stage5v_token_buffers_preserve_domain_masks_and_separators(tmp_path: Path) -> None:
    fixtures = build_conformance_fixtures(conformance_fixtures_out=tmp_path / "fixtures.yaml", out_dir=tmp_path / "out")
    for fixture in fixtures:
        tokens = fixture["token_values"]
        mask = fixture["transformable_mask"]
        assert len(mask) == len(tokens)
        for index, token in enumerate(tokens):
            if token != -1:
                assert 0 <= token <= 28
            if index in fixture["separator_positions"]:
                assert mask[index] is False


def test_stage5v_shift_outputs_are_candidate_major_and_hash_stable(tmp_path: Path) -> None:
    fixtures = build_conformance_fixtures(conformance_fixtures_out=tmp_path / "fixtures.yaml", out_dir=tmp_path / "out")
    fixture = next(record for record in fixtures if record["fixture_id"] == "stage5v-shift-multi-candidate-fixture")
    outputs = candidate_major_shift_outputs(fixture)
    assert [item["candidate_id"] for item in outputs] == [
        "stage5v-shift-00",
        "stage5v-shift-01",
        "stage5v-shift-03",
        "stage5v-shift-13",
        "stage5v-shift-28",
    ]
    assert outputs == fixture["expected_outputs"]


def test_stage5v_token_buffer_conformance_records_all_surfaces(tmp_path: Path) -> None:
    fixtures = build_conformance_fixtures(conformance_fixtures_out=tmp_path / "fixtures.yaml", out_dir=tmp_path / "out")
    records = build_token_buffer_conformance(
        fixtures=fixtures,
        token_buffer_conformance_out=tmp_path / "token.yaml",
        out_dir=tmp_path / "out",
    )
    assert len(records) == 7
    assert {record["conformance_surface"] for record in records} >= {"token_values", "separator_positions"}
