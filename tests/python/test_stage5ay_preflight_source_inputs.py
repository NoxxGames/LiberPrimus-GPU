from pathlib import Path

import yaml


def test_stage5ay_source_inputs_use_repaired_stage5aw_manifest() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-preflight-source-inputs.yaml").read_text(encoding="utf-8"))

    assert payload["stage5aw_repaired_branch_manifest_used"] is True
    assert payload["stage5av_branch_manifest_used"] is False
    assert payload["missing_required_source_count"] == 0
    assert payload["source_inputs_validated"] is True
