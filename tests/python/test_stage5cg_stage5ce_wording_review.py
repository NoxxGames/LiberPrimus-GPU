from libreprimus.token_block.stage5cg import validate_stage5cg_stage5ce_wording_review
from test_stage5cg_common import load_yaml, write_yaml


def test_stage5cg_stage5ce_wording_review_is_not_gate_opener(tmp_path) -> None:
    counts, errors = validate_stage5cg_stage5ce_wording_review()
    assert not errors
    assert counts["wording_warning_disposition"] == "not_reproduced_current_repo"
    assert counts["reported_typo_field_present_current_repo"] is False

    payload = load_yaml("data/token-block/stage5cg-stage5ce-combined-gate-wording-review.yaml")
    payload["stage5ce_wording_blemish_gate_opener"] = True
    bad = tmp_path / "wording.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5cg_stage5ce_wording_review(wording_review=bad)
    assert bad_errors
