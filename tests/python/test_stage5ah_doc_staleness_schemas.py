from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def _yaml(path: str) -> dict:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_stage5ah_committed_records_validate_against_schemas() -> None:
    _validator("schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json").validate(
        _yaml("data/project-state/stage5ah-doc-staleness-source-of-truth.yaml")
    )
    _validator("schemas/project-state/stage-ledger-coverage-summary-v0.schema.json").validate(
        _yaml("data/project-state/stage5ah-stage-ledger-coverage.yaml")
    )
    _validator("schemas/project-state/operational-file-map-coverage-record-v0.schema.json").validate(
        _yaml("data/project-state/stage5ah-operational-file-map-coverage.yaml")
    )
    _validator("schemas/project-state/stage5ah-doc-staleness-summary-v0.schema.json").validate(
        _yaml("data/project-state/stage5ah-doc-staleness-summary.yaml")
    )


def test_stage5ah_stage_ledger_schema_rejects_solve_claim() -> None:
    record = {
        "record_type": "stage_ledger_staleness_record",
        "stage_id": "stage-5ah",
        "path": "README.md",
        "finding_count": 0,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "cuda_execution_performed": False,
        "solve_claim": True,
    }

    with pytest.raises(ValidationError):
        _validator("schemas/project-state/stage-ledger-staleness-record-v0.schema.json").validate(record)


def test_stage5ah_summary_schema_rejects_cuda_execution() -> None:
    record = _yaml("data/project-state/stage5ah-doc-staleness-summary.yaml")
    record["cuda_execution_performed"] = True

    with pytest.raises(ValidationError):
        _validator("schemas/project-state/stage5ah-doc-staleness-summary-v0.schema.json").validate(record)
