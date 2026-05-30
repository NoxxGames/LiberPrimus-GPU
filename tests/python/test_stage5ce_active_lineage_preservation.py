from pathlib import Path

import yaml

from libreprimus.token_block.stage5ca import INCORRECT_STAGE5AW_PATH
from libreprimus.token_block.stage5ce import validate_stage5ce_sidecar_gates
from test_stage5ce_common import load_yaml


def test_stage5ce_active_lineage_preserved() -> None:
    payload = load_yaml("data/token-block/stage5ce-active-lineage-preservation.yaml")
    assert payload["active_lineage_preservation_status"] == "preserved_unchanged"
    assert payload["active_lineage_record_count"] == 8
    assert payload["deprecated_stage5aw_path_included"] is False
    assert payload["correct_stage5aw_path_included"] is True
    assert payload["all_preserved_active_paths_resolve"] is True


def test_stage5ce_deprecated_stage5aw_active_lineage_path_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/token-block/stage5ce-active-lineage-preservation.yaml")
    payload["preserved_active_record_paths"][1] = INCORRECT_STAGE5AW_PATH
    candidate = tmp_path / "active_lineage.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_sidecar_gates(active_lineage=candidate)
    assert counts["stage5ce_sidecar_gates_valid"] is False
    assert "deprecated_stage5aw_path_present" in errors
