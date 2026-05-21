from __future__ import annotations

import yaml


def test_stage5r_result_store_preflight_cites_stage4p_and_stays_compact() -> None:
    records = yaml.safe_load(open("data/cuda/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml", encoding="utf-8"))[
        "records"
    ]
    assert len(records) == 3
    for record in records:
        assert record["stage4p_compatibility"] is True
        assert record["result_store_contract"] == "stage4p"
        assert record["output_token_hash_required"] is True
        assert record["generated_body_publication_allowed"] is False
        assert record["generated_result_bodies_committed"] is False
        assert record["method_status_upgrade_allowed"] is False
        assert record["preflight_status"] == "ready_for_stage5s_result_store_integration"
        assert record["stage5s_ready"] is True
