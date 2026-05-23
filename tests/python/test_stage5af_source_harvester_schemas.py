from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError


def _yaml(path: str) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _records(path: str) -> list[dict[str, Any]]:
    return list(_yaml(path)["records"])


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def test_stage5af_schemas_validate_committed_records() -> None:
    source_validator = _validator("schemas/source-harvester/source-record-v0.schema.json")
    for record in _records("data/source-harvester/stage5af-cicada-source-manifest.yaml"):
        source_validator.validate(record)

    _validator("schemas/source-harvester/source-manifest-v0.schema.json").validate(
        _yaml("data/source-harvester/stage5af-cicada-source-manifest.yaml")
    )
    bundle_validator = _validator("schemas/source-harvester/research-bundle-plan-record-v0.schema.json")
    for record in _records("data/source-harvester/stage5af-research-bundle-plan.yaml"):
        bundle_validator.validate(record)
    category_validator = _validator("schemas/source-harvester/clue-target-category-record-v0.schema.json")
    for record in _records("data/source-harvester/stage5af-clue-target-categories.yaml"):
        category_validator.validate(record)
    decision_validator = _validator(
        "schemas/source-harvester/source-harvester-next-stage-decision-record-v0.schema.json"
    )
    for record in _records("data/source-harvester/stage5af-source-harvester-next-stage-decision.yaml"):
        decision_validator.validate(record)
    _validator("schemas/source-harvester/stage5af-source-harvester-summary-v0.schema.json").validate(
        _yaml("data/source-harvester/stage5af-source-harvester-summary.yaml")
    )


def test_stage5af_schemas_reject_forbidden_flags() -> None:
    source_validator = _validator("schemas/source-harvester/source-record-v0.schema.json")
    record = _records("data/source-harvester/stage5af-cicada-source-manifest.yaml")[0]
    with pytest.raises(ValidationError):
        source_validator.validate({**record, "solve_claim": True})
    with pytest.raises(ValidationError):
        source_validator.validate({**record, "raw_commit_allowed": True})
    with pytest.raises(ValidationError):
        source_validator.validate({**record, "google_drive_storage_allowed": True})

    summary_validator = _validator("schemas/source-harvester/stage5af-source-harvester-summary-v0.schema.json")
    summary = _yaml("data/source-harvester/stage5af-source-harvester-summary.yaml")
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "cuda_execution_performed": True})
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "new_cuda_kernels_added": 1})
