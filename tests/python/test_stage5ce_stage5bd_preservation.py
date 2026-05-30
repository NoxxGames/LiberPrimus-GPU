from pathlib import Path

import yaml

from libreprimus.token_block.stage5ce import validate_stage5ce_sidecar_gates
from test_stage5ce_common import load_yaml


def test_stage5ce_stage5bd_plan_preserved() -> None:
    payload = load_yaml("data/token-block/stage5ce-stage5bd-plan-preservation.yaml")
    assert payload["stage5bd_plan_preservation_status"] == "preserved_unchanged"
    assert payload["stage5bd_run_plan_id_count"] == 10
    assert payload["stage5bd_run_plan_ids_changed"] is False
    assert payload["stage5bd_dry_run_plan_manifest_changed"] is False


def test_stage5ce_stage5bd_run_plan_count_change_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-stage5bd-plan-preservation.yaml")
    payload["stage5bd_run_plan_id_count"] = 11
    candidate = tmp_path / "stage5bd.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_sidecar_gates(stage5bd_preservation=candidate)
    assert counts["stage5ce_sidecar_gates_valid"] is False
    assert "Stage 5BD run-plan count must remain 10" in errors
