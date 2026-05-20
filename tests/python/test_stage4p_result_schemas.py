from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/results/unified-result-record-v0.schema.json",
    "schemas/results/unified-score-summary-record-v0.schema.json",
    "schemas/results/result-source-inventory-v0.schema.json",
    "schemas/results/result-method-status-join-v0.schema.json",
    "schemas/results/cross-stage-comparison-report-v0.schema.json",
    "schemas/results/result-store-unification-summary-v0.schema.json",
]


def test_stage4p_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_unified_result_schema_rejects_unsafe_flags() -> None:
    validator = Draft202012Validator(_schema("schemas/results/unified-result-record-v0.schema.json"))
    for key, value in (
        ("solve_claim", True),
        ("cuda_used", True),
        ("generated_outputs_committed", True),
    ):
        record = _unified_result()
        record[key] = value
        assert list(validator.iter_errors(record)), key


def test_unified_score_schema_rejects_unknown_labels() -> None:
    validator = Draft202012Validator(_schema("schemas/results/unified-score-summary-record-v0.schema.json"))
    record = _unified_score()
    record["confidence_label"] = "new_magic_label"
    assert list(validator.iter_errors(record))


def test_unified_score_schema_accepts_stage4i_label() -> None:
    validator = Draft202012Validator(_schema("schemas/results/unified-score-summary-record-v0.schema.json"))
    assert not list(validator.iter_errors(_unified_score()))


def _schema(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _unified_result() -> dict:
    return {
        "record_type": "unified_result_record",
        "unified_result_id": "result",
        "source_stage_id": "stage-4p",
        "source_record_type": "summary",
        "result_source_kind": "synthetic_test_fixture",
        "source_path": "synthetic.json",
        "source_presence_status": "committed_summary_present",
        "score_summary_available": False,
        "confidence_label": "scoring_not_available",
        "method_status": "unknown",
        "no_solve_claim": True,
        "solve_claim": False,
        "cuda_used": False,
        "cuda_required": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "new_experiment_executed": False,
        "new_scorer_added": False,
    }


def _unified_score() -> dict:
    return {
        "record_type": "unified_score_summary_record",
        "unified_score_id": "score",
        "source_stage_id": "stage-4p",
        "source_path": "synthetic.json",
        "result_source_kind": "synthetic_test_fixture",
        "score_status": "scoring_not_available",
        "confidence_label": "scoring_not_available",
        "score_interpretation": "triage_only",
        "no_solve_claim": True,
        "solve_claim": False,
        "cuda_used": False,
        "new_scorer_added": False,
    }
