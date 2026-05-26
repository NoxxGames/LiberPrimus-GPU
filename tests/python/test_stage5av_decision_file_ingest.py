from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def _load(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_stage5av_decision_file_ingest_recorded_local_template_hash() -> None:
    ingest = _load("data/token-block/stage5av-decision-file-ingest.yaml")
    assert ingest["decision_file_found"] is True
    assert ingest["decision_file_path"] == (
        "human-review-packs/stage5au/token-case-review-v2/decision-template.yaml"
    )
    assert ingest["decision_file_sha256"] == (
        "dd9e3ee0fe5dccd70fd19dbca864dbb57706c113f48777abe546b98d9d8f25f7"
    )
    assert ingest["decision_file_not_committed"] is True
    assert ingest["solve_claim"] is False
