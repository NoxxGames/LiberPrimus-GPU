from pathlib import Path

import yaml


def test_stage5bd_future_result_paths_are_validated_not_written() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-future-result-path-validation.yaml").read_text())

    assert payload["future_result_paths_validated"] is True
    assert payload["future_result_paths_written"] is False
    assert payload["blocked_path_count"] == 3
    assert all(record["relative_path"] for record in payload["path_validation_records"])
