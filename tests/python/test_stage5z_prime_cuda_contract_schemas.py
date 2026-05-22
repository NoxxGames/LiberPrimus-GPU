from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError

from libreprimus.prime_minus_one_cuda_contract.buffer_contract import build_buffer_contract
from libreprimus.prime_minus_one_cuda_contract.contract_records import build_contract_records
from libreprimus.prime_minus_one_cuda_contract.full_p56_blocker import build_full_p56_blocker
from libreprimus.prime_minus_one_cuda_contract.future_parity_plan import build_future_parity_plan
from libreprimus.prime_minus_one_cuda_contract.host_runner_contract import build_host_runner_contract
from libreprimus.prime_minus_one_cuda_contract.implementation_readiness import (
    build_implementation_readiness_gate,
)
from libreprimus.prime_minus_one_cuda_contract.kernel_abi import build_kernel_abi
from libreprimus.prime_minus_one_cuda_contract.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_cuda_contract.result_store_compatibility import (
    build_result_store_compatibility,
)
from libreprimus.prime_minus_one_cuda_contract.scored_experiment_deferral import (
    build_scored_experiment_deferral,
)
from libreprimus.prime_minus_one_cuda_contract.summary import build_summary
from libreprimus.prime_minus_one_cuda_contract.validation_vectors import build_validation_vectors


def _schema(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def _records(path: Path) -> list[dict[str, Any]]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return list(payload["records"])


def _summary(path: Path) -> dict[str, Any]:
    return dict(yaml.safe_load(path.read_text(encoding="utf-8")))


def _build_all(tmp_path: Path) -> dict[str, Path]:
    out_dir = tmp_path / "reports"
    paths = {
        "out_dir": out_dir,
        "contract": tmp_path / "contract.yaml",
        "kernel": tmp_path / "kernel.yaml",
        "host": tmp_path / "host.yaml",
        "buffer": tmp_path / "buffer.yaml",
        "vectors": tmp_path / "vectors.yaml",
        "future": tmp_path / "future.yaml",
        "result": tmp_path / "result.yaml",
        "blocker": tmp_path / "blocker.yaml",
        "scored": tmp_path / "scored.yaml",
        "gate": tmp_path / "gate.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    build_contract_records(cuda_contract_out=paths["contract"], out_dir=out_dir)
    build_kernel_abi(kernel_abi_out=paths["kernel"], out_dir=out_dir)
    build_host_runner_contract(host_runner_contract_out=paths["host"], out_dir=out_dir)
    build_buffer_contract(buffer_contract_out=paths["buffer"], out_dir=out_dir)
    build_validation_vectors(validation_vectors_out=paths["vectors"], out_dir=out_dir)
    build_future_parity_plan(future_parity_plan_out=paths["future"], out_dir=out_dir)
    build_result_store_compatibility(result_store_compatibility_out=paths["result"], out_dir=out_dir)
    build_full_p56_blocker(full_p56_blocker_out=paths["blocker"], out_dir=out_dir)
    build_scored_experiment_deferral(scored_experiment_deferral_out=paths["scored"], out_dir=out_dir)
    build_implementation_readiness_gate(implementation_readiness_out=paths["gate"], out_dir=out_dir)
    build_next_stage_decision(next_stage_decision_out=paths["decision"], out_dir=out_dir)
    build_summary(
        cuda_contract=paths["contract"],
        kernel_abi=paths["kernel"],
        host_runner_contract=paths["host"],
        buffer_contract=paths["buffer"],
        validation_vectors=paths["vectors"],
        future_parity_plan=paths["future"],
        result_store_compatibility=paths["result"],
        full_p56_blocker=paths["blocker"],
        scored_experiment_deferral=paths["scored"],
        implementation_readiness_gate=paths["gate"],
        next_stage_decision=paths["decision"],
        summary_out=paths["summary"],
        out_dir=out_dir,
    )
    return paths


def test_stage5z_schemas_validate_records(tmp_path: Path) -> None:
    paths = _build_all(tmp_path)
    cases = [
        ("schemas/cuda/prime-minus-one-cuda-contract-record-v0.schema.json", paths["contract"]),
        ("schemas/cuda/prime-minus-one-cuda-kernel-abi-record-v0.schema.json", paths["kernel"]),
        (
            "schemas/cuda/prime-minus-one-cuda-host-runner-contract-record-v0.schema.json",
            paths["host"],
        ),
        ("schemas/cuda/prime-minus-one-cuda-buffer-contract-record-v0.schema.json", paths["buffer"]),
        (
            "schemas/cuda/prime-minus-one-cuda-validation-vector-record-v0.schema.json",
            paths["vectors"],
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-future-parity-plan-record-v0.schema.json",
            paths["future"],
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-result-store-compatibility-record-v0.schema.json",
            paths["result"],
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-full-p56-blocker-record-v0.schema.json",
            paths["blocker"],
        ),
        (
            "schemas/cuda/prime-minus-one-scored-experiment-deferral-record-v0.schema.json",
            paths["scored"],
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-implementation-readiness-gate-record-v0.schema.json",
            paths["gate"],
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-next-stage-decision-record-v0.schema.json",
            paths["decision"],
        ),
    ]
    for schema_path, record_path in cases:
        validator = _schema(schema_path)
        for record in _records(record_path):
            validator.validate(record)
    _schema("schemas/cuda/stage5z-prime-minus-one-cuda-contract-summary-v0.schema.json").validate(
        _summary(paths["summary"])
    )


def test_stage5z_schema_rejects_forbidden_guardrail_values(tmp_path: Path) -> None:
    record = build_contract_records(cuda_contract_out=tmp_path / "contract.yaml", out_dir=tmp_path)[0]
    schema = _schema("schemas/cuda/prime-minus-one-cuda-contract-record-v0.schema.json")
    for patch in (
        {"cuda_execution_performed": True},
        {"cuda_source_modified": True},
        {"new_cuda_kernels_added": 1},
        {"solve_claim": True},
        {"generated_outputs_committed": True},
        {"raw_data_processed": True},
    ):
        with pytest.raises(ValidationError):
            schema.validate({**record, **patch})
