from pathlib import Path

import pytest
import yaml

from libreprimus.token_block.stage5bb import ExecutionBlockedError, PreflightRunnerScaffold


def test_stage5bb_runner_scaffold_manifest_blocks_execution() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-runner-scaffold-manifest.yaml").read_text())
    registry = yaml.safe_load(Path("data/token-block/stage5bb-active-manifest-registry.yaml").read_text())

    assert payload["runner_scaffold_created"] is True
    assert payload["runner_execution_created"] is False
    assert payload["real_token_block_byte_generation_supported"] is False
    with pytest.raises(ExecutionBlockedError):
        PreflightRunnerScaffold(registry).generate_real_token_block_byte_stream()
