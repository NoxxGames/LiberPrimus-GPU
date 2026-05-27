from pathlib import Path

import yaml


def test_stage5bd_consolidates_stage5bb_placeholders_without_mutating_history() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5bd-stage5bb-validation-evidence-consolidation.yaml").read_text()
    )

    assert payload["stage5bb_validation_evidence_placeholders_found"] is True
    assert payload["stage5bb_historical_file_mutated"] is False
    assert payload["consolidated_validation_status"] == "passed"
