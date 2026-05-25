from __future__ import annotations

from pathlib import Path

import yaml


def _yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_stage5ar_case_policy_covers_required_classes_without_transcription_change() -> None:
    policy = _yaml("data/token-block/stage5ar-token-case-policy.yaml")
    ambiguities = _yaml("data/token-block/stage5ar-token-case-ambiguity-records.yaml")
    classes = {record["ambiguity_class"] for record in ambiguities["records"]}
    assert {"uppercase_I_lowercase_l", "uppercase_O_zero_0", "digit_1_uppercase_I_lowercase_l"} <= classes
    assert policy["canonical_transcription_changed"] is False
    assert policy["unresolved_ambiguity_class_count"] >= 1
