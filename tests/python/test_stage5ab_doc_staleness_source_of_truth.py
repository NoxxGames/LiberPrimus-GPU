from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from libreprimus.doc_staleness.source_of_truth import load_operational_paths, load_source_of_truth


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def test_stage5ab_source_of_truth_schema_and_loader() -> None:
    path = Path("data/project-state/stage5ah-doc-staleness-source-of-truth.yaml")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))

    _validator("schemas/project-state/doc-staleness-source-of-truth-record-v0.schema.json").validate(payload)
    source = load_source_of_truth(path)
    assert source.latest_completed_stage_prefix == "Stage 5DO"
    assert source.expected_next_stage_prefix == "Stage 5DP"
    assert source.next_stage_after_this_stage == (
        "Stage 5DP - Lightweight source-lock browser GUI design/build, without puzzle execution"
    )


def test_stage5ab_operational_file_map_schema_and_loader() -> None:
    path = Path("data/project-state/operational-file-map.yaml")
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))

    _validator("schemas/project-state/operational-file-map-record-v0.schema.json").validate(payload)
    paths = load_operational_paths(path)
    assert "README.md" in paths
    assert "docs/onboarding/operational-file-map.md" in paths
    assert len(paths) >= 40


def test_stage5ab_summary_and_findings_schemas() -> None:
    _validator("schemas/project-state/stage5ab-doc-staleness-summary-v0.schema.json").validate(
        yaml.safe_load(
            Path("data/project-state/stage5ab-doc-staleness-summary.yaml").read_text(encoding="utf-8")
        )
    )
    _validator("schemas/project-state/doc-staleness-finding-record-v0.schema.json").validate(
        yaml.safe_load(
            Path("data/project-state/stage5ab-doc-staleness-findings.yaml").read_text(encoding="utf-8")
        )
    )
