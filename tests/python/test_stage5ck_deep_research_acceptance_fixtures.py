from libreprimus.token_block.stage5ck import DEEP_RESEARCH_FIXTURE_CASES

from test_stage5ck_common import load_yaml


def test_deep_research_acceptance_fixtures_are_unsatisfied() -> None:
    payload = load_yaml("data/token-block/stage5ck-deep-research-acceptance-fixture-pack.yaml")
    assert payload["deep_research_acceptance_fixture_records_created"] is True
    assert payload["actual_deep_research_acceptance_records_created"] is False
    assert payload["deep_research_acceptance_fixture_records_satisfy_acceptance"] is False
    assert set(DEEP_RESEARCH_FIXTURE_CASES) <= set(payload["fixture_cases"])
    for fixture in payload["fixture_records"]:
        assert fixture["fixture_only"] is True
        assert fixture["actual_deep_research_acceptance_record"] is False
        assert fixture["may_authorize_activation"] is False
