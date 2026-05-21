from __future__ import annotations

import yaml

from libreprimus.gematria_solved_fixture_mapping.export import read_record_set
from libreprimus.gematria_solved_fixture_mapping.token_mapping import build_token_mapping_records
from libreprimus.paths import repo_root


def test_token_mapping_records_use_source_backed_0_28_values() -> None:
    records = read_record_set(repo_root() / "data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml")
    assert len(records) == 5
    assert {record["mapping_status"] for record in records} == {"mapped"}
    for record in records:
        assert record["token_domain"] == "integers_0_to_28"
        assert len(record["transformable_mask"]) == record["token_count"]
        for value, transformable in zip(record["token_values"], record["transformable_mask"], strict=True):
            if transformable:
                assert isinstance(value, int)
                assert 0 <= value <= 28


def test_token_mapping_preserves_separator_and_token_kind_metadata() -> None:
    records = read_record_set(repo_root() / "data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml")
    for record in records:
        assert record["separator_metadata_preserved"] is True
        assert record["token_kind_metadata_preserved"] is True
        assert len(record["token_kinds"]) == record["token_count"]


def test_token_mapping_blocks_invented_values_without_source(tmp_path) -> None:
    manifest = {
        "input_streams": [
            {
                "input_stream_id": "stream",
                "fixture_id": "fixture",
                "token_count": 1,
                "transformable_token_count": 1,
                "tokens": [{"token_kind": "rune", "latin_label": "X"}],
            }
        ],
        "transform_candidates": [{"candidate_id": "candidate", "input_stream_id": "stream", "transform_id": "direct"}],
    }
    preflight = {
        "records": [
            {
                "preflight_id": "preflight",
                "mapping_id": "mapping",
                "source_input_stream_id": "stream",
                "fixture_id": "fixture",
                "transform_family": "direct_translation",
                "candidate_id": "candidate",
                "solved_fixture_stream_token_count": 1,
            }
        ]
    }
    manifest_path = tmp_path / "manifest.yaml"
    preflight_path = tmp_path / "preflight.yaml"
    out_path = tmp_path / "mapping.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest), encoding="utf-8")
    preflight_path.write_text(yaml.safe_dump(preflight), encoding="utf-8")
    records = build_token_mapping_records(
        source_manifest=manifest_path,
        preflight=preflight_path,
        token_mapping_out=out_path,
        out_dir=tmp_path,
    )
    assert records[0]["mapping_status"] == "blocked"
    assert "blocked_missing_source_backed_0_28_token_value" in records[0]["blockers"]
