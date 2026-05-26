from pathlib import Path

import yaml


def test_stage5bb_guardrail_keeps_all_execution_flags_false() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-guardrail.yaml").read_text())

    assert payload["runner_scaffold_only"] is True
    assert payload["execution_performed"] is False
    assert payload["token_experiments_executed"] is False
    assert payload["variant_byte_streams_generated"] is False
    assert payload["cuda_execution_performed"] is False
    assert payload["new_cuda_kernels_added"] == 0
    assert payload["solve_claim"] is False
