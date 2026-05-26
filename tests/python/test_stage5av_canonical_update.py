from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5av_canonical_update_is_non_update() -> None:
    payload = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5av-canonical-transcription-update.yaml"
        ).read_text(encoding="utf-8")
    )
    assert payload["canonical_transcription_changed"] is False
    assert payload["canonical_transcription_change_count"] == 0
    assert payload["explicit_change_token_count"] == 0
    assert payload["high_confidence_change_token_count"] == 0
