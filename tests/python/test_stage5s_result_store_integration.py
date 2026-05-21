from __future__ import annotations

from pathlib import Path

import yaml


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5s_result_store_records_are_compact_stage4p_metadata() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-result-store-integration.yaml")
    assert len(records) == 3
    for record in records:
        assert record["result_source_kind"] == "expanded_solved_fixture_safe_cuda_parity"
        assert record["stage4p_compatibility"] is True
        assert record["compact_summary_only"] is True
        assert record["generated_body_committed"] is False
        assert record["generated_body_publication_allowed"] is False
        assert record["output_token_hash_required"] is True
        assert record["output_text_hash_required"] is False
        assert record["method_status_upgrade_allowed"] is False
        assert record["no_solve_claim"] is True
        assert "output_tokens" not in record


def test_stage5s_result_store_links_score_summary_records() -> None:
    result_store = _records("data/cuda/stage5s-gematria-expanded-cuda-result-store-integration.yaml")
    score = _records("data/cuda/stage5s-gematria-expanded-cuda-score-summary-integration.yaml")
    score_ids = {record["score_summary_integration_id"] for record in score}
    assert all(record["score_summary_link"] in score_ids for record in result_store)
