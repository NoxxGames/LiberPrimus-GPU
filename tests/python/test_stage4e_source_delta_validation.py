from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.source_delta_audit.disabled_manifests import write_disabled_manifests
from libreprimus.source_delta_audit.validation import validate_source_delta_records


def test_validation_rejects_raw_and_font_committed(tmp_path: Path) -> None:
    source_delta = tmp_path / "delta.yaml"
    health = tmp_path / "health.yaml"
    artifact = tmp_path / "artifact.yaml"
    manifests = tmp_path / "manifests"
    write_disabled_manifests(manifests)
    _write(source_delta, [{"record_type": "source_delta_audit_record", "audit_id": "a", "source_id": "s", "raw_file_committed": True, "binary_committed": False, "font_committed": False, "solve_claim": False}])
    _write(health, [{"record_type": "source_health_record", "source_id": "h", "solve_claim": False, "trusted_as_canonical": False}])
    _write(artifact, [_artifact_record()])
    _, errors = validate_source_delta_records(
        source_delta=source_delta,
        source_health=health,
        image_artifact=artifact,
        manifest_dir=manifests,
    )
    assert any(error.startswith("raw_file_committed_not_false") for error in errors)

    _write(source_delta, [{"record_type": "source_delta_audit_record", "audit_id": "a", "source_id": "s", "raw_file_committed": False, "binary_committed": False, "font_committed": True, "solve_claim": False}])
    _, errors = validate_source_delta_records(
        source_delta=source_delta,
        source_health=health,
        image_artifact=artifact,
        manifest_dir=manifests,
    )
    assert any(error.startswith("font_committed_not_false") for error in errors)


def _write(path: Path, records: list[dict]) -> None:
    path.write_text(yaml.safe_dump({"record_set_id": path.stem, "schema": "", "records": records}), encoding="utf-8")


def _artifact_record() -> dict:
    return {
        "record_type": "image_compression_artifact_observation",
        "observation_id": "artifact",
        "future_tests": ["hash comparison"],
        "negative_controls": ["known jpeg"],
        "usable_as_experiment_seed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }
