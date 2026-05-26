from pathlib import Path

import yaml


def test_stage5bb_validation_evidence_index_lists_required_commands() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-validation-evidence-index.yaml").read_text())

    assert payload["validation_evidence_index_created"] is True
    assert "validate-stage5bb" in payload["local_commands_recorded"]
    assert "run-parallel-validation" in payload["local_commands_recorded"]
    assert payload["generated_validation_outputs_committed"] is False
