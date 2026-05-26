from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_unresolved_variants_are_branch_metadata_only() -> None:
    payload = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5av-unresolved-token-variant-records.yaml"
        ).read_text(encoding="utf-8")
    )
    assert payload["unresolved_token_variant_count"] == 77
    assert payload["variant_byte_streams_generated"] is False
    assert payload["execution_performed"] is False
    assert all(record["requires_review_followup"] for record in payload["records"])
