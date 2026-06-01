from libreprimus.token_block.stage5cq import validate_stage5cq_prior_stage_preservation

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_preserves_prior_fixture_template_scaffold_contracts() -> None:
    ensure_stage5cq_built()
    assert load_yaml("data/token-block/stage5cq-stage5cm-boundary-preservation.yaml")[
        "stage5cm_fixture_vs_real_boundary_preserved"
    ] is True
    assert load_yaml("data/token-block/stage5cq-stage5ck-fixture-preservation.yaml")[
        "stage5ck_fixture_pack_only_preserved"
    ] is True
    assert load_yaml("data/token-block/stage5cq-stage5ci-template-preservation.yaml")[
        "stage5ci_templates_preserved"
    ] is True
    assert load_yaml("data/token-block/stage5cq-stage5cg-scaffold-preservation.yaml")[
        "stage5cg_scaffolds_preserved"
    ] is True
    assert load_yaml("data/token-block/stage5cq-stage5ce-proposal-package-preservation.yaml")[
        "stage5ce_proposal_package_status_preserved"
    ] == "review_package_only"
    counts, errors = validate_stage5cq_prior_stage_preservation()
    assert not errors
    assert counts["stage5cq_prior_stage_preservation_valid"] is True
