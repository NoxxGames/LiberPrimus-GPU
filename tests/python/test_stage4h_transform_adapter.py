from __future__ import annotations

from libreprimus.cpu_batch.transform_adapter import adapter_status, apply_transform
from libreprimus.transforms.registry import load_registry


def test_stage4h_transform_adapter_applies_known_transform() -> None:
    result = apply_transform(
        registry=load_registry(),
        stream=_stream(),
        candidate={
            "candidate_id": "direct",
            "input_stream_id": "stream",
            "transform_id": "direct_translation",
            "transform_parameters": {},
        },
    )
    assert result.status == "executed"
    assert result.canonical_transform_id == "direct_translation"
    assert result.output_text == "FU"


def test_stage4h_unsupported_adapter_returns_adapter_missing() -> None:
    result = apply_transform(
        registry=load_registry(),
        stream=_stream(),
        candidate={
            "candidate_id": "missing",
            "input_stream_id": "stream",
            "transform_id": "future_transform",
            "transform_parameters": {},
        },
    )
    assert result.status == "adapter_missing"
    assert adapter_status("future_transform") == "adapter_missing"


def _stream() -> dict:
    return {
        "input_stream_id": "stream",
        "token_count": 2,
        "transformable_token_count": 2,
        "tokens": [
            {"token_kind": "rune", "index29": 0, "latin_label": "F", "token_index_global": 0},
            {"token_kind": "rune", "index29": 1, "latin_label": "U", "token_index_global": 1},
        ],
    }
