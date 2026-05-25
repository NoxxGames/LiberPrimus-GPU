from __future__ import annotations

from collections import Counter

from libreprimus.token_block.models import TOKEN_GRID_LINES, token_rows
from libreprimus.token_block.transcription import build_transcription, validate_transcription_record


def test_stage5ap_transcription_shape_and_counts(tmp_path) -> None:
    record = build_transcription(out=tmp_path / "transcription.yaml")
    tokens = [token for row in token_rows() for token in row]
    assert len(TOKEN_GRID_LINES) == 32
    assert record["row_count"] == 32
    assert record["column_count"] == 8
    assert record["token_count"] == 256
    assert record["unique_token_count"] == 161
    assert record["first_character_counts"] == dict(sorted(Counter(token[0] for token in tokens).items()))
    assert record["first_character_counts"] == {"0": 60, "1": 58, "2": 65, "3": 56, "4": 17}
    assert validate_transcription_record(record) == []
