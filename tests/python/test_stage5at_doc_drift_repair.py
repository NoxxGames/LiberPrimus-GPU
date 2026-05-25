from pathlib import Path

import yaml


def test_stage5at_doc_drift_repair_matches_active_classes() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5at-doc-drift-repair-summary.yaml").read_text())
    assert payload["doc_drift_repaired"] is True
    assert payload["doc_drift_active_classes_match_data"] is True
    assert payload["stale_doc_only_examples"] == ["f/F", "A/4", "C/G"]
    assert payload["stale_examples_not_active"] is True
