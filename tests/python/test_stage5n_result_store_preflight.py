from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5n_result_store_preflight_requires_stage4p_compatibility() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5n-gematria-cuda-result-store-preflight.yaml").read_text(encoding="utf-8"))["records"]
    assert len(records) == 2
    assert all(record["stage4p_compatibility_required"] is True for record in records)
    assert all(record["stage4p_summary_present"] is True for record in records)
    assert all(record["result_source_kind"] == "solved_fixture_safe_cuda_parity" for record in records)


def test_stage5n_score_summary_preflight_keeps_confidence_labels_triage_only() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5n-gematria-cuda-result-store-preflight.yaml").read_text(encoding="utf-8"))["records"]
    assert all(record["stage4i_confidence_labels_only"] is True for record in records)
    assert all(record["confidence_label_interpretation"] == "triage_only" for record in records)
    assert all(record["method_status_upgrade_allowed"] is False for record in records)
