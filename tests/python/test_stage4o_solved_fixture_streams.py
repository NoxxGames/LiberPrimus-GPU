from __future__ import annotations

from pathlib import Path

from libreprimus.cpu_batch.solved_fixture_streams import (
    skipped_missing_fixture_stream_record,
    solved_fixture_stream_records_from_manifest,
    tokens_from_normalized_plaintext,
)


MANIFEST = Path("experiments/manifests/cpu-batch/stage4o-cpu-cuda-parity-readiness.yaml")


def test_stage4o_solved_fixture_stream_builder_deterministic() -> None:
    first = solved_fixture_stream_records_from_manifest(MANIFEST)
    second = solved_fixture_stream_records_from_manifest(MANIFEST)
    assert first == second
    assert len(first) == 5
    assert all(record["input_token_stream_hash"] for record in first)
    assert all(record["cuda_used"] is False for record in first)


def test_stage4o_missing_raw_fixture_skipped_explicitly(tmp_path: Path) -> None:
    record = skipped_missing_fixture_stream_record(tmp_path / "missing.fixture.json", stream_id="missing-stream")
    assert record["source_type"] == "skipped_missing_fixture"
    assert "skip_reason" in record


def test_stage4o_fixture_tokenizer_is_deterministic() -> None:
    tokens = tokens_from_normalized_plaintext("AN.")
    assert [token["token_kind"] for token in tokens] == ["rune", "rune", "clause_separator"]
    assert [token.get("latin_label") for token in tokens[:2]] == ["A", "N"]
