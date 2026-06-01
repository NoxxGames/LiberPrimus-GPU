from libreprimus.token_block.stage5cs import validate_stage5cs_stage5cq_preservation

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_preserves_stage5cq_scaffold_only_boundary() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-stage5cq-operator-decision-scaffold-preservation.yaml")
    assert payload["stage5cq_operator_decision_scaffold_preserved"] is True
    assert payload["stage5cq_operator_decision_scaffold_status_preserved"] == "scaffold_only"
    counts, errors = validate_stage5cs_stage5cq_preservation()
    assert not errors
    assert counts["stage5cs_stage5cq_preservation_valid"] is True
