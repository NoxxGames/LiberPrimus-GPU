from libreprimus.token_block.stage5cu import (
    validate_stage5cu_stage5cs_preservation,
    validate_stage5cu_stage5co_preservation,
    validate_stage5cu_stage5cq_preservation,
    validate_stage5cu_prior_stage_preservation,
)

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_preserves_stage5cs_and_prior_approval_layers() -> None:
    ensure_stage5cu_built()
    summary = load_yaml("data/project-state/stage5cu-summary.yaml")
    assert summary["stage5cs_operator_decision_readiness_package_status_preserved"] == "readiness_package_only"
    assert summary["stage5cq_operator_decision_scaffold_status_preserved"] == "scaffold_only"
    assert summary["stage5co_readiness_package_preserved"] is True
    assert summary["stage5cm_boundary_preserved"] is True
    for validator in (
        validate_stage5cu_stage5cs_preservation,
        validate_stage5cu_stage5cq_preservation,
        validate_stage5cu_stage5co_preservation,
        validate_stage5cu_prior_stage_preservation,
    ):
        counts, errors = validator()
        assert not errors
        assert list(counts.values())[0] is True
