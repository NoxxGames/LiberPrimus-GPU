from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError

from libreprimus.prime_minus_one_cuda_synthetic.device_subset_audit import build_device_subset_audit
from libreprimus.prime_minus_one_cuda_synthetic.kernel_implementation import build_kernel_implementation_records
from libreprimus.prime_minus_one_cuda_synthetic.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_cuda_synthetic.p56_blocker import build_p56_blocker
from libreprimus.prime_minus_one_cuda_synthetic.parity_records import build_parity_records
from libreprimus.prime_minus_one_cuda_synthetic.result_store_preflight import build_result_store_preflight
from libreprimus.prime_minus_one_cuda_synthetic.run_records import run_synthetic_cuda_parity
from libreprimus.prime_minus_one_cuda_synthetic.scored_experiment_deferral import build_scored_experiment_deferral
from libreprimus.prime_minus_one_cuda_synthetic.summary import build_summary


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def _records(path: Path) -> list[dict[str, Any]]:
    return list(yaml.safe_load(path.read_text(encoding="utf-8"))["records"])


def _build_all(tmp_path: Path) -> dict[str, Path]:
    paths = {
        "out": tmp_path / "out",
        "kernel": tmp_path / "kernel.yaml",
        "run": tmp_path / "run.yaml",
        "parity": tmp_path / "parity.yaml",
        "audit": tmp_path / "audit.yaml",
        "result": tmp_path / "result.yaml",
        "p56": tmp_path / "p56.yaml",
        "scored": tmp_path / "scored.yaml",
        "decision": tmp_path / "decision.yaml",
        "summary": tmp_path / "summary.yaml",
    }
    build_kernel_implementation_records(kernel_implementation_out=paths["kernel"], out_dir=paths["out"])
    run_synthetic_cuda_parity(cuda_run_out=paths["run"], out_dir=paths["out"], skip_cuda=True)
    build_parity_records(cuda_run=paths["run"], parity_out=paths["parity"], out_dir=paths["out"])
    build_device_subset_audit(device_subset_audit_out=paths["audit"], out_dir=paths["out"])
    build_result_store_preflight(result_store_preflight_out=paths["result"], out_dir=paths["out"])
    build_p56_blocker(p56_blocker_out=paths["p56"], out_dir=paths["out"])
    build_scored_experiment_deferral(scored_experiment_deferral_out=paths["scored"], out_dir=paths["out"])
    build_next_stage_decision(parity=paths["parity"], next_stage_decision_out=paths["decision"], out_dir=paths["out"])
    build_summary(
        kernel_implementation=paths["kernel"],
        cuda_run=paths["run"],
        parity=paths["parity"],
        device_subset_audit=paths["audit"],
        result_store_preflight=paths["result"],
        p56_blocker=paths["p56"],
        scored_experiment_deferral=paths["scored"],
        next_stage_decision=paths["decision"],
        summary_out=paths["summary"],
        out_dir=paths["out"],
    )
    return paths


def test_stage5aa_schemas_validate_records(tmp_path: Path) -> None:
    paths = _build_all(tmp_path)
    cases = [
        ("schemas/cuda/prime-minus-one-cuda-synthetic-kernel-implementation-record-v0.schema.json", paths["kernel"]),
        ("schemas/cuda/prime-minus-one-cuda-synthetic-run-record-v0.schema.json", paths["run"]),
        ("schemas/cuda/prime-minus-one-cuda-synthetic-parity-record-v0.schema.json", paths["parity"]),
        ("schemas/cuda/prime-minus-one-cuda-device-subset-audit-record-v0.schema.json", paths["audit"]),
        ("schemas/cuda/prime-minus-one-cuda-synthetic-result-store-preflight-record-v0.schema.json", paths["result"]),
        ("schemas/cuda/prime-minus-one-cuda-synthetic-p56-blocker-record-v0.schema.json", paths["p56"]),
        ("schemas/cuda/prime-minus-one-cuda-synthetic-scored-experiment-deferral-record-v0.schema.json", paths["scored"]),
        ("schemas/cuda/prime-minus-one-cuda-synthetic-next-stage-decision-record-v0.schema.json", paths["decision"]),
    ]
    for schema, record_path in cases:
        validator = _validator(schema)
        for record in _records(record_path):
            validator.validate(record)
    _validator("schemas/cuda/stage5aa-prime-minus-one-cuda-synthetic-summary-v0.schema.json").validate(
        yaml.safe_load(paths["summary"].read_text(encoding="utf-8"))
    )


def test_stage5aa_schema_rejects_forbidden_values(tmp_path: Path) -> None:
    record = build_kernel_implementation_records(kernel_implementation_out=tmp_path / "kernel.yaml", out_dir=tmp_path)[0]
    validator = _validator("schemas/cuda/prime-minus-one-cuda-synthetic-kernel-implementation-record-v0.schema.json")
    for patch in (
        {"p56_cuda_execution_performed": True},
        {"full_p56_cuda_execution_performed": True},
        {"unsolved_page_cuda_used": True},
        {"gpu_benchmark_performed": True},
        {"scored_experiment_executed": True},
        {"solve_claim": True},
        {"generated_outputs_committed": True},
        {"raw_data_processed": True},
        {"new_cuda_kernels_added": 2},
    ):
        with pytest.raises(ValidationError):
            validator.validate({**record, **patch})
