from libreprimus.token_block.stage5ci import validate_stage5ci_deep_research_acceptance_template
from test_stage5ci_common import load_yaml, write_yaml


def test_stage5ci_deep_research_template_is_not_acceptance_record(tmp_path) -> None:
    counts, errors = validate_stage5ci_deep_research_acceptance_template()
    assert not errors
    assert counts["deep_research_activation_accept_record_present_now"] is False
    assert counts["deep_research_activation_accept_satisfied_now"] is False

    payload = load_yaml("data/token-block/stage5ci-deep-research-acceptance-record-template.yaml")
    payload["deep_research_activation_accept_record_present_now"] = True
    bad = tmp_path / "deep-research.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_deep_research_acceptance_template(
        deep_research_template=bad
    )
    assert bad_errors
