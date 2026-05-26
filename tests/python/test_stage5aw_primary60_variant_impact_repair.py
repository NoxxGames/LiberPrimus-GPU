from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_primary60_impact_is_recomputed_after_parser_repair() -> None:
    payload = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5aw-repaired-primary60-variant-impact-summary.yaml"
        ).read_text(encoding="utf-8")
    )
    assert payload["primary60_mappable_option_count"] == 99
    assert payload["primary60_unmappable_option_count"] == 65
    assert payload["visual_placeholder_possible_token_count"] == 2
    assert payload["malformed_fragment_count"] == 3
    assert payload["branch_count_upper_bound_product"] == 2720083094132915643088896
    assert payload["branch_count_upper_bound_log10"] == 24.434582
    assert payload["variant_byte_streams_generated"] is False
