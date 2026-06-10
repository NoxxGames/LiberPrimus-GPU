from __future__ import annotations

from pathlib import Path

from test_stage5dy_common import ensure_stage5dy_built, load_yaml, run_token_block_cli


def test_stage_isolation_policy_uses_frozen_fields() -> None:
    ensure_stage5dy_built()
    payload = load_yaml("data/project-state/stage5dy-stage-isolation-policy.yaml")

    assert payload["historical_validators_use_frozen_stage_fields"] is True
    assert payload["mutable_global_source_browser_counts_allowed_in_historical_validators"] is False
    assert payload["stage5dw_global_count_fragility_guarded"] is True


def test_stage5dw_preservation_still_succeeds_after_later_records() -> None:
    ensure_stage5dy_built()

    output = run_token_block_cli("validate-stage5dx-stage5dw-preservation")

    assert "token_block_stage5dx_stage5dw_preservation_valid=true" in output


def test_stage5dw_shared_schema_has_no_later_stage_constants() -> None:
    shared_schema = Path("schemas/operator-console/stage5dw-source-browser-number-fact-review-batch-result-v0.schema.json")
    if shared_schema.exists():
        text = shared_schema.read_text(encoding="utf-8")
        assert "stage-5dx" not in text
        assert "stage-5dy" not in text
