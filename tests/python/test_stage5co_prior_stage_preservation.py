from libreprimus.token_block.stage5co import validate_stage5co_prior_stage_preservation

from test_stage5co_common import load_yaml


def test_stage5co_preserves_prior_fixture_template_scaffold_contracts() -> None:
    assert load_yaml("data/token-block/stage5co-stage5ck-fixture-preservation.yaml")[
        "stage5ck_fixture_pack_only_preserved"
    ] is True
    assert load_yaml("data/token-block/stage5co-stage5ci-template-preservation.yaml")[
        "stage5ci_templates_preserved"
    ] is True
    assert load_yaml("data/token-block/stage5co-stage5cg-scaffold-preservation.yaml")[
        "stage5cg_scaffolds_preserved"
    ] is True
    assert load_yaml("data/token-block/stage5co-stage5ce-proposal-package-preservation.yaml")[
        "stage5ce_proposal_package_status_preserved"
    ] == "review_package_only"
    assert load_yaml("data/token-block/stage5co-stage5cc-contract-preservation.yaml")[
        "stage5cc_exact_citation_contract_preserved"
    ] is True

    counts, errors = validate_stage5co_prior_stage_preservation()
    assert errors == []
    assert counts["stage5co_prior_stage_preservation_valid"] is True
