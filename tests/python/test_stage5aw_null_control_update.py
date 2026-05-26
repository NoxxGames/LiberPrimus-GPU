from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_null_control_routes_future_preflight_to_repaired_manifest() -> None:
    payload = yaml.safe_load(
        (ROOT / "data/token-block/stage5aw-null-control-decision-update.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert payload["supersedes_stage5av_branch_metadata"] is True
    assert payload["future_preflight_must_use_stage5aw_repaired_manifest"] is True
    assert payload["visual_placeholders_excluded_from_primary60_byte_variants"] is True
    assert payload["malformed_prose_fragments_excluded_from_variant_options"] is True
    assert payload["execution_performed"] is False
