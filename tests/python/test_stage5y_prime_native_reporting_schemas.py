from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from libreprimus.prime_minus_one_native_reporting.cuda_contract_readiness import build_cuda_contract_readiness_gate
from libreprimus.prime_minus_one_native_reporting.full_p56_blocker import build_full_p56_blocker_preservation
from libreprimus.prime_minus_one_native_reporting.generated_body_policy import build_generated_body_policy
from libreprimus.prime_minus_one_native_reporting.guardrails import build_guardrails
from libreprimus.prime_minus_one_native_reporting.method_status_impact import build_method_status_impact
from libreprimus.prime_minus_one_native_reporting.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_native_reporting.parity_report import build_parity_report
from libreprimus.prime_minus_one_native_reporting.result_store_integration import build_result_store_integration
from libreprimus.prime_minus_one_native_reporting.scored_experiment_readiness import build_scored_experiment_readiness
from libreprimus.prime_minus_one_native_reporting.score_summary_integration import build_score_summary_integration
from libreprimus.prime_minus_one_native_reporting.summary import build_summary


def _schema(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def _build_all(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "parity": tmp_path / "parity.yaml",
        "result": tmp_path / "result.yaml",
        "score": tmp_path / "score.yaml",
        "method": tmp_path / "method.yaml",
        "policy": tmp_path / "policy.yaml",
        "blocker": tmp_path / "blocker.yaml",
        "gate": tmp_path / "gate.yaml",
        "scored": tmp_path / "scored.yaml",
        "guardrail": tmp_path / "guardrail.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    build_parity_report(parity_report_out=paths["parity"], out_dir=tmp_path)
    build_result_store_integration(
        parity_report=paths["parity"],
        result_store_integration_out=paths["result"],
        out_dir=tmp_path,
    )
    build_score_summary_integration(
        parity_report=paths["parity"],
        score_summary_integration_out=paths["score"],
        out_dir=tmp_path,
    )
    build_method_status_impact(method_status_impact_out=paths["method"], out_dir=tmp_path)
    build_generated_body_policy(generated_body_policy_out=paths["policy"], out_dir=tmp_path)
    build_full_p56_blocker_preservation(full_p56_blocker_preservation_out=paths["blocker"], out_dir=tmp_path)
    build_cuda_contract_readiness_gate(
        parity_report=paths["parity"],
        result_store_integration=paths["result"],
        score_summary_integration=paths["score"],
        cuda_contract_readiness_gate_out=paths["gate"],
        out_dir=tmp_path,
    )
    build_scored_experiment_readiness(scored_experiment_readiness_out=paths["scored"], out_dir=tmp_path)
    build_guardrails(guardrail_out=paths["guardrail"], out_dir=tmp_path)
    build_next_stage_decision(
        cuda_contract_readiness_gate=paths["gate"],
        next_stage_decision_out=paths["decision"],
        out_dir=tmp_path,
    )
    build_summary(
        parity_report=paths["parity"],
        result_store_integration=paths["result"],
        score_summary_integration=paths["score"],
        method_status_impact=paths["method"],
        generated_body_policy=paths["policy"],
        full_p56_blocker_preservation=paths["blocker"],
        cuda_contract_readiness_gate=paths["gate"],
        scored_experiment_readiness=paths["scored"],
        guardrail=paths["guardrail"],
        next_stage_decision=paths["decision"],
        summary_out=paths["summary"],
        out_dir=tmp_path,
    )
    return paths


def test_stage5y_schemas_validate_records(tmp_path: Path) -> None:
    paths = _build_all(tmp_path)
    cases = [
        ("schemas/cuda/prime-minus-one-native-parity-report-record-v0.schema.json", paths["parity"]),
        ("schemas/cuda/prime-minus-one-native-result-store-integration-record-v0.schema.json", paths["result"]),
        ("schemas/cuda/prime-minus-one-native-score-summary-integration-record-v0.schema.json", paths["score"]),
        ("schemas/cuda/prime-minus-one-native-method-status-impact-record-v0.schema.json", paths["method"]),
        ("schemas/cuda/prime-minus-one-generated-body-policy-record-v0.schema.json", paths["policy"]),
        ("schemas/cuda/prime-minus-one-full-p56-blocker-preservation-record-v0.schema.json", paths["blocker"]),
        ("schemas/cuda/prime-minus-one-cuda-contract-readiness-gate-record-v0.schema.json", paths["gate"]),
        ("schemas/cuda/bounded-scored-experiment-readiness-record-v0.schema.json", paths["scored"]),
        ("schemas/cuda/prime-minus-one-native-reporting-guardrail-record-v0.schema.json", paths["guardrail"]),
        ("schemas/cuda/prime-minus-one-native-reporting-next-stage-decision-record-v0.schema.json", paths["decision"]),
    ]
    import yaml

    for schema_path, record_path in cases:
        records = yaml.safe_load(record_path.read_text(encoding="utf-8"))["records"]
        validator = _schema(schema_path)
        for record in records:
            validator.validate(record)

    summary = yaml.safe_load(paths["summary"].read_text(encoding="utf-8"))
    _schema("schemas/cuda/stage5y-prime-minus-one-native-reporting-summary-v0.schema.json").validate(summary)


def test_stage5y_schema_rejects_cuda_solve_and_generated_publication(tmp_path: Path) -> None:
    record = build_parity_report(parity_report_out=tmp_path / "parity.yaml", out_dir=tmp_path)[0]
    schema = _schema("schemas/cuda/prime-minus-one-native-parity-report-record-v0.schema.json")
    for patch in (
        {"cuda_execution_performed": True},
        {"solve_claim": True},
        {"generated_outputs_committed": True},
    ):
        with pytest.raises(ValidationError):
            schema.validate({**record, **patch})
