from pathlib import Path

import yaml


def test_stage5bb_branch_eligibility_reference_validation_counts_options() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5bb-branch-eligibility-reference-validation.yaml").read_text()
    )

    assert payload["branch_eligibility_policy_required"] is True
    assert payload["branch_eligibility_policy_present"] is True
    assert payload["branch_eligibility_policy_validated"] is True
    assert payload["option_record_count"] == 167
    assert payload["primary60_mappable_option_count"] == 99
    assert payload["execution_ineligible_option_count"] == 68
