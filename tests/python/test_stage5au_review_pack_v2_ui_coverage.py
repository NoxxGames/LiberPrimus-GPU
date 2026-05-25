from pathlib import Path

import yaml


def test_stage5au_ui_coverage_surfaces_context_and_overlays() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-review-pack-v2-ui-coverage.yaml").read_text())
    assert payload["case_challenges_rendered"] == 203
    assert payload["canonical_challenges_rendered"] == 212
    assert payload["all_203_case_challenges_visible_or_linked"] is True
    assert payload["all_212_canonical_challenges_visible_or_linked"] is True
    assert payload["context_small_visible_or_linked_for_every_challenge"] is True
    assert payload["context_medium_visible_or_linked_for_every_challenge"] is True
    assert payload["context_large_visible_or_linked_for_every_challenge"] is True
    assert payload["row_context_visible_or_linked_for_every_challenge"] is True
    assert payload["overlays_visible_or_linked_for_every_challenge"] is True
    assert payload["per_class_page_count"] == 9
    assert payload["per_page_pages"] == [49, 50, 51]
    assert payload["page_transition_page_exists"] is True
    assert payload["canonical_review_page_exists"] is True
