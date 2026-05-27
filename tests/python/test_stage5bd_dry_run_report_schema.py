from pathlib import Path

import yaml


def test_stage5bd_dry_run_report_schema_forbids_real_outputs() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-dry-run-report-schema.yaml").read_text())

    assert payload["real_token_byte_fields_allowed"] is False
    assert payload["generated_byte_stream_hash_fields_allowed"] is False
    assert payload["decoded_text_fields_allowed"] is False
    assert payload["score_fields_allowed"] is False
