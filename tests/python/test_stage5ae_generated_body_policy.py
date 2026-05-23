from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_generated_body_policy_blocks_publication() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-generated-body-policy.yaml").read_text())["records"][0]
    assert record["generated_body_publication_allowed"] is False
    assert record["generated_outputs_committed"] is False
    assert record["codex_output_committed"] is False
    assert "generated_result_bodies" in record["forbidden_committed_payloads"]
