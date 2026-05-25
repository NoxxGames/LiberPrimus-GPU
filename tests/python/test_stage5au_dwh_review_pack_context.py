from pathlib import Path

import yaml


def test_stage5au_dwh_context_stays_review_only() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-dwh-review-pack-context.yaml").read_text())
    assert payload["dwh_expansion"] == "Deep Web Hash"
    assert "Stage 5AU performs no hash or decode work" in payload["review_pack_relevance"]
    assert payload["hash_search_performed"] is False
    assert payload["decode_attempt_performed"] is False
    assert payload["solve_claim"] is False
