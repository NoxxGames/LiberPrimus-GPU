from pathlib import Path

import yaml


def test_stage5ay_branch_eligibility_classifies_options() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-branch-eligibility-policy.yaml").read_text(encoding="utf-8"))
    classes = payload["eligibility_classes"]

    assert classes["primary60_mappable_option"] == 99
    assert classes["execution_ineligible_option"] > 0
    assert classes["visual_placeholder_from_reviewer_notes"] == 2
    assert classes["malformed_fragment_audit_only"] == 3
