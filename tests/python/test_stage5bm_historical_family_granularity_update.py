from test_stage5bm_common import load_yaml


def test_stage5bm_family_granularity_is_targeted_addendum() -> None:
    record = load_yaml("data/historical-route/stage5bm-historical-family-granularity-update.yaml")
    family_ids = {row["family_id"] for row in record["new_or_refined_family_rows"]}

    assert record["granularity_update_status"] == "targeted_addendum_only"
    assert "token_block_page49_51_string4_branch_context" in family_ids
    assert "pgp_false_path_warning_and_7a35090f_gate" in family_ids
    assert "stego_outguess_openpuff_mp3_positive_controls" in family_ids
    assert record["family_status_records_mutated"] is False
