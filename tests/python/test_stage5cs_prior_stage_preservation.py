from libreprimus.token_block.stage5cs import validate_stage5cs_prior_stage_preservation

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_preserves_prior_approval_layers() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-stage5cm-boundary-preservation.yaml")
    assert payload["stage5cm_boundary_preserved"] is True
    assert payload["stage5cm_parallel_worker_cap_preserved"] == 8
    counts, errors = validate_stage5cs_prior_stage_preservation()
    assert not errors
    assert counts["stage5cs_prior_stage_preservation_valid"] is True
