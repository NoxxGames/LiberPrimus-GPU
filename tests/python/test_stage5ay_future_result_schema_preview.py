from pathlib import Path

import yaml


def test_stage5ay_future_result_schema_is_preview_only() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-future-result-schema-preview.yaml").read_text(encoding="utf-8"))

    assert payload["future_result_schema_preview_only"] is True
    assert payload["result_generated_now"] is False
    assert "byte_stream_sha256" in payload["preview_fields"]
    assert payload["solve_claim"] is False
