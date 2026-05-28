from test_stage5bm_common import load_yaml


def test_stage5bm_review_packaging_warning_is_not_failure() -> None:
    record = load_yaml("data/source-harvester/stage5bm-review-packaging-warning.yaml")

    assert record["zip_review_sufficient"] is True
    assert record["exact_final_commit_pin_missing_from_review_zip"] is True
    assert record["ignored_iddqd_v2_tree_absent_from_review_zip"] is True
    assert record["warning_is_stage_failure"] is False
