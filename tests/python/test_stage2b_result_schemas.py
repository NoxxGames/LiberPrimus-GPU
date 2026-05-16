import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate


SCHEMA_DIR = Path("schemas/results")


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _valid_run_record() -> dict:
    return {
        "record_type": "experiment_run_record",
        "run_id": "run-1",
        "run_kind": "solved_baseline",
        "run_status": "pass",
        "manifest_id": "manifest",
        "manifest_sha256": "a" * 64,
        "registry_id": "registry",
        "registry_sha256": "b" * 64,
        "git_commit": "abc",
        "branch": "main",
        "created_at_utc": "2026-05-16T00:00:00Z",
        "completed_at_utc": "2026-05-16T00:00:01Z",
        "elapsed_ms": 1.0,
        "host": {
            "os": "Windows",
            "platform": "Windows",
            "machine": "AMD64",
            "processor": "CPU",
            "python_version": "3.12.0",
        },
        "tool_versions": {},
        "input_sources": [],
        "profiles": [],
        "corpus_candidate_id": "rtkd-master-v0-candidate",
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "search_performed": False,
        "scoring_used": False,
        "cuda_used": False,
        "gpu_required": False,
        "random_seed": None,
        "fixture_counts": {"total": 10, "pass": 10, "fail": 0, "pending": 0, "skipped": 0},
        "transform_counts": {},
        "output_artifacts": [],
        "warnings": [],
        "trusted_as_canonical": False,
        "notes": [],
    }


def test_valid_experiment_run_record_validates() -> None:
    validate(instance=_valid_run_record(), schema=_schema("experiment-run-record-v0.schema.json"))


def test_run_record_missing_run_id_fails() -> None:
    payload = _valid_run_record()
    payload.pop("run_id")

    with pytest.raises(ValidationError):
        validate(instance=payload, schema=_schema("experiment-run-record-v0.schema.json"))


@pytest.mark.parametrize(
    "field",
    ["canonical_corpus_active", "search_performed", "scoring_used", "cuda_used", "trusted_as_canonical"],
)
def test_stage2b_false_fields_are_enforced(field: str) -> None:
    payload = _valid_run_record()
    payload[field] = True

    with pytest.raises(ValidationError):
        validate(instance=payload, schema=_schema("experiment-run-record-v0.schema.json"))


def test_generated_artifact_cannot_be_committed() -> None:
    artifact = {
        "record_type": "experiment_artifact_record",
        "run_id": "run-1",
        "artifact_id": "artifact",
        "artifact_kind": "jsonl",
        "path": "experiments/results/result-store/stage2b/run_records.jsonl",
        "sha256": "c" * 64,
        "size_bytes": 1,
        "committed": True,
        "ignored_by_git": True,
        "notes": [],
        "trusted_as_canonical": False,
    }

    with pytest.raises(ValidationError):
        validate(instance=artifact, schema=_schema("experiment-artifact-record-v0.schema.json"))
