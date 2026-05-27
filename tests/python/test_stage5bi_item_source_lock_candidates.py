from test_stage5bi_fandom_page_triage import load_yaml


def test_stage5bi_item_candidates_include_2014_and_token_block_surfaces() -> None:
    payload = load_yaml("data/historical-route/stage5bi-fandom-item-source-lock-candidates.yaml")
    candidate_ids = {record["candidate_id"] for record in payload["records"]}

    assert payload["candidate_count"] == len(payload["records"])
    assert "stage5bi-c01-2014-growing-hex-surface" in candidate_ids
    assert "stage5bi-c02-2014-1033-hex-surface" in candidate_ids
    assert "stage5bi-c03-2014-3301-hex-surface" in candidate_ids
    assert "stage5bi-c04-page49-51-256-token-surface" in candidate_ids
    assert all(record["execution_allowed"] is False for record in payload["records"])
    assert all(record["solve_claim"] is False for record in payload["records"])
