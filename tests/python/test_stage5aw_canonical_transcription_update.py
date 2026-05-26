from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_canonical_transcription_remains_unchanged() -> None:
    payload = yaml.safe_load(
        (ROOT / "data/token-block/stage5aw-canonical-transcription-update.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert payload["canonical_transcription_changed"] is False
    assert payload["canonical_transcription_change_count"] == 0
    assert payload["canonical_transcription_update_status"] == "unchanged_parser_repair_only"
    assert payload["parser_repair_only"] is True
