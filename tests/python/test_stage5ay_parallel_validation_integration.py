from pathlib import Path

import yaml


def test_stage5ay_references_stage5ax_parallel_validation() -> None:
    source_inputs = yaml.safe_load(Path("data/token-block/stage5ay-preflight-source-inputs.yaml").read_text(encoding="utf-8"))
    summary = yaml.safe_load(Path("data/project-state/stage5ay-summary.yaml").read_text(encoding="utf-8"))

    assert any(record["role"] == "stage5ax_parallel_validation_run_summary" for record in source_inputs["records"])
    assert summary["parallel_validation_harness_used"] is True
