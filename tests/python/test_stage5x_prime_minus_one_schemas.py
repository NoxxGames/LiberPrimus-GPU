from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from libreprimus.prime_minus_one_native_parity.full_p56_blocker import build_full_p56_blocker
from libreprimus.prime_minus_one_native_parity.guardrails import build_guardrails
from libreprimus.prime_minus_one_native_parity.native_execution import build_native_run_records
from libreprimus.prime_minus_one_native_parity.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_native_parity.parity_records import build_parity_records
from libreprimus.prime_minus_one_native_parity.result_store_preflight import build_result_store_preflight
from libreprimus.prime_minus_one_native_parity.score_summary_preflight import build_score_summary_preflight
from libreprimus.prime_minus_one_native_parity.summary import build_summary


def _schema(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def test_stage5x_record_schemas_validate(tmp_path: Path) -> None:
    run = tmp_path / "run.yaml"
    parity = tmp_path / "parity.yaml"
    result = tmp_path / "result.yaml"
    score = tmp_path / "score.yaml"
    blocker = tmp_path / "blocker.yaml"
    guardrail = tmp_path / "guardrail.yaml"
    decision = tmp_path / "decision.yaml"
    summary = tmp_path / "summary.yaml"

    cases = [
        ("schemas/cuda/prime-minus-one-native-run-record-v0.schema.json", build_native_run_records(native_run_out=run, out_dir=tmp_path)),
        ("schemas/cuda/prime-minus-one-native-parity-record-v0.schema.json", build_parity_records(native_run=run, native_parity_out=parity, out_dir=tmp_path)),
        ("schemas/cuda/prime-minus-one-native-result-store-preflight-record-v0.schema.json", build_result_store_preflight(native_parity=parity, result_store_preflight_out=result, out_dir=tmp_path)),
        ("schemas/cuda/prime-minus-one-native-score-summary-preflight-record-v0.schema.json", build_score_summary_preflight(native_parity=parity, score_summary_preflight_out=score, out_dir=tmp_path)),
        ("schemas/cuda/prime-minus-one-full-p56-blocker-record-v0.schema.json", build_full_p56_blocker(full_p56_blocker_out=blocker, out_dir=tmp_path)),
        ("schemas/cuda/prime-minus-one-native-guardrail-record-v0.schema.json", build_guardrails(guardrail_out=guardrail, out_dir=tmp_path)),
        ("schemas/cuda/prime-minus-one-native-next-stage-decision-record-v0.schema.json", build_next_stage_decision(native_parity=parity, next_stage_decision_out=decision, out_dir=tmp_path)),
    ]
    for schema_path, records in cases:
        validator = _schema(schema_path)
        for record in records:
            validator.validate(record)

    summary_record = build_summary(
        native_run=run,
        native_parity=parity,
        result_store_preflight=result,
        score_summary_preflight=score,
        full_p56_blocker=blocker,
        guardrail=guardrail,
        next_stage_decision=decision,
        summary_out=summary,
        out_dir=tmp_path,
    )
    _schema("schemas/cuda/stage5x-prime-minus-one-native-parity-summary-v0.schema.json").validate(summary_record)


def test_stage5x_schemas_reject_cuda_and_solve_claims(tmp_path: Path) -> None:
    record = build_native_run_records(native_run_out=tmp_path / "run.yaml", out_dir=tmp_path)[0]
    schema = _schema("schemas/cuda/prime-minus-one-native-run-record-v0.schema.json")
    with pytest.raises(ValidationError):
        schema.validate({**record, "cuda_execution_performed": True})
    with pytest.raises(ValidationError):
        schema.validate({**record, "solve_claim": True})
