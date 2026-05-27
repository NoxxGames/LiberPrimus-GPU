from test_stage5bi_fandom_page_triage import load_yaml


def test_stage5bi_2014_surfaces_are_context_only() -> None:
    payload = load_yaml("data/historical-route/stage5bi-2014-256-byte-surface-context.yaml")
    markers = {str(record["historical_marker"]) for record in payload["surfaces"]}

    assert payload["surface_count"] == 3
    assert markers == {"Patience is a virtue", "1033", "3301"}
    assert payload["page49_51_context"]["token_count"] == 256
    assert payload["page49_51_context"]["execution_allowed"] is False
    assert payload["surface_combination_performed"] is False
    assert payload["xor_attempt_performed"] is False
    assert payload["transposition_attempt_performed"] is False
    assert all(record["claimed_byte_count"] == 256 for record in payload["surfaces"])
    assert all(record["execution_allowed"] is False for record in payload["surfaces"])
    assert all(record["combination_with_page49_51_allowed"] is False for record in payload["surfaces"])
