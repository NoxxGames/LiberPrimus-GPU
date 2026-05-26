from pathlib import Path

import yaml


def test_stage5bb_dry_run_preview_has_counts_without_real_outputs() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-dry-run-plan-preview.yaml").read_text())

    assert payload["dry_run_preview_created"] is True
    assert payload["unique_variant_family_count"] == 10
    assert payload["taxonomy_membership_count"] == 11
    assert payload["real_byte_streams_included"] is False
    assert payload["real_variant_outputs_included"] is False
    assert payload["hash_comparisons_included"] is False
    assert payload["scores_included"] is False
