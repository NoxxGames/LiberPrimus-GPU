from __future__ import annotations

from pathlib import Path

from jsonschema import Draft202012Validator
import yaml

from libreprimus.gematria_cuda_parity_reporting.score_summary_preflight import build_score_summary_preflight


def test_stage5k_score_summary_preflight_uses_stage4i_labels(tmp_path: Path) -> None:
    records = build_score_summary_preflight(score_preflight_out=tmp_path / "score.yaml", out_dir=tmp_path)
    record = records[0]
    assert record["score_summary_contract"] == "stage4i"
    assert record["score_interpretation"] == "triage_only"
    assert "scoring_not_available" in record["allowed_confidence_labels"]
    assert record["confidence_labels_triage_only"] is True
    assert record["solve_claim"] is False


def test_stage5k_score_schema_rejects_unknown_confidence_label() -> None:
    schema = yaml.safe_load(Path("schemas/cuda/gematria-cuda-score-summary-preflight-record-v0.schema.json").read_text())
    record = yaml.safe_load(Path("data/cuda/stage5k-gematria-cuda-score-summary-preflight.yaml").read_text())["records"][0]
    record["allowed_confidence_labels"] = ["new_unapproved_label"]
    errors = list(Draft202012Validator(schema).iter_errors(record))
    assert errors
