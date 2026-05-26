from pathlib import Path

import yaml


def test_stage5az_reference_audit_preserves_stage5aw_active_stage5av_inactive() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5az-manifest-reference-audit.yaml").read_text(encoding="utf-8")
    )

    assert payload["missing_reference_count"] == 0
    assert payload["stage5aw_repaired_branch_manifest_used"] is True
    assert payload["stage5av_branch_manifest_used"] is False
    assert payload["stage5av_branch_manifest_inactive"] is True
