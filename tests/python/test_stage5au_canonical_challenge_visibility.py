from pathlib import Path

import yaml


def test_stage5au_canonical_challenges_are_visible_without_transcription_change() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-canonical-transcription-challenge-set-v2.yaml").read_text())
    assert payload["challenge_count"] == 212
    assert len(payload["records"]) == 212
    assert payload["all_canonical_challenges_rendered"] is True
    assert payload["canonical_transcription_changed"] is False
    assert payload["automatic_case_resolution_performed"] is False
