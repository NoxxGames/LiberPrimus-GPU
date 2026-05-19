from __future__ import annotations

from libreprimus.cpu_batch.input_streams import normalize_input_stream, stable_json_sha256


def test_stage4h_synthetic_input_stream_deterministic() -> None:
    stream = {
        "record_type": "cpu_batch_input_stream",
        "input_stream_id": "synthetic",
        "source_kind": "synthetic",
        "tokens": [
            {"token_kind": "rune", "index29": 0, "latin_label": "F"},
            {"token_kind": "word_separator", "raw_text": " "},
            {"token_kind": "rune", "index29": 1, "latin_label": "U"},
        ],
    }
    normalized = normalize_input_stream(stream)
    assert normalized["token_count"] == 3
    assert normalized["transformable_token_count"] == 2
    assert normalized["tokens"][0]["token_index_global"] == 0
    assert stable_json_sha256(normalized) == stable_json_sha256(normalize_input_stream(stream))
