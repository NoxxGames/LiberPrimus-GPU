from pathlib import Path

import yaml


def test_stage5au_records_stage5at_pack_as_not_usable() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-review-pack-usability-audit.yaml").read_text())
    assert payload["stage5at_review_pack_generated"] is True
    assert payload["stage5at_review_pack_count_validated"] is True
    assert payload["stage5at_html_case_card_count"] == 80
    assert payload["stage5at_html_includes_all_203_challenges"] is False
    assert payload["stage5at_manual_review_usable"] is False
    assert payload["manual_review_should_proceed_from_stage5at_pack"] is False
    assert payload["repair_required"] is True
