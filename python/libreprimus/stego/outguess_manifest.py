"""OutGuess manifest and artifact loading."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.stego.models import OutGuessCase, OutGuessManifest, StegoArtifact
from libreprimus.stego.outguess_export import resolve_path

ALLOWED_ROLES = {
    "known_positive",
    "known_negative",
    "synthetic_positive",
    "synthetic_negative",
    "candidate",
    "reference_only",
}


def load_artifacts(path: Path) -> dict[str, StegoArtifact]:
    """Load committed stego artifact records."""
    payload = _read_yaml_mapping(path)
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("artifact records file must contain records list")
    artifacts: dict[str, StegoArtifact] = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("artifact record must be a mapping")
        artifact = _artifact_from_record(record)
        if artifact.artifact_id in artifacts:
            raise ValueError(f"duplicate artifact_id: {artifact.artifact_id}")
        artifacts[artifact.artifact_id] = artifact
    return artifacts


def load_manifest(path: Path) -> OutGuessManifest:
    """Load and validate an OutGuess regression manifest."""
    payload = _read_yaml_mapping(path)
    if payload.get("record_type") != "outguess_regression_manifest":
        raise ValueError("manifest record_type must be outguess_regression_manifest")
    if payload.get("cpu_only") is not True:
        raise ValueError("manifest cpu_only must be true")
    if payload.get("cuda_enabled") is not False:
        raise ValueError("manifest cuda_enabled must be false")
    if payload.get("no_solve_claim") is not True:
        raise ValueError("manifest no_solve_claim must be true")
    if payload.get("generated_outputs_committed") is not False:
        raise ValueError("manifest generated_outputs_committed must be false")
    cap = int(payload.get("expected_case_count_upper_bound", 0))
    if cap <= 0 or cap > 100000:
        raise ValueError("manifest expected_case_count_upper_bound must be 1..100000")
    raw_cases = payload.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ValueError("manifest cases must be a non-empty list")
    cases = tuple(_case_from_record(case) for case in raw_cases)
    if len(cases) > cap:
        raise ValueError(f"case_count_exceeds_cap:{len(cases)}>{cap}")
    return OutGuessManifest(
        manifest_id=str(payload.get("manifest_id", "")),
        allow_missing_tool=bool(payload.get("allow_missing_tool")),
        allow_missing_assets=bool(payload.get("allow_missing_assets")),
        cases=cases,
        expected_case_count_upper_bound=cap,
        payload=payload,
    )


def validate_manifest_and_artifacts(manifest_path: Path, artifacts_path: Path) -> tuple[dict[str, Any], list[str]]:
    """Validate OutGuess manifest and artifacts without running extraction."""
    errors: list[str] = []
    try:
        manifest = load_manifest(manifest_path)
    except Exception as exc:  # noqa: BLE001
        return {}, [str(exc)]
    try:
        artifacts = load_artifacts(artifacts_path)
    except Exception as exc:  # noqa: BLE001
        return {}, [str(exc)]
    for case in manifest.cases:
        if case.artifact_id not in artifacts:
            errors.append(f"{case.case_id}: missing artifact record {case.artifact_id}")
        elif artifacts[case.artifact_id].expected_role != case.expected_role:
            errors.append(f"{case.case_id}: expected_role does not match artifact record")
    if errors:
        return {}, errors
    enabled = [case for case in manifest.cases if case.enabled]
    historical = [artifact for artifact in artifacts.values() if artifact.expected_role == "known_positive"]
    synthetic = [artifact for artifact in artifacts.values() if artifact.expected_role.startswith("synthetic_")]
    return {
        "outguess_manifest_valid": True,
        "manifest_id": manifest.manifest_id,
        "case_count": len(manifest.cases),
        "enabled_case_count": len(enabled),
        "artifact_count": len(artifacts),
        "historical_positive_placeholder_count": len(historical),
        "synthetic_control_count": len(synthetic),
        "allow_missing_tool": manifest.allow_missing_tool,
        "allow_missing_assets": manifest.allow_missing_assets,
        "cuda_enabled": False,
        "no_solve_claim": True,
    }, []


def _artifact_from_record(record: dict[str, Any]) -> StegoArtifact:
    errors = []
    if record.get("record_type") != "stego_artifact_record":
        errors.append("wrong record_type")
    if record.get("expected_role") not in ALLOWED_ROLES:
        errors.append("invalid expected_role")
    if record.get("trusted_as_canonical") is not False:
        errors.append("trusted_as_canonical must be false")
    if record.get("solve_claim") is not False:
        errors.append("solve_claim must be false")
    if record.get("extraction_tool") != "outguess":
        errors.append("extraction_tool must be outguess")
    if errors:
        raise ValueError(f"{record.get('artifact_id', '<unknown>')}: {'; '.join(errors)}")
    expected = record.get("expected_payload_sha256")
    return StegoArtifact(
        artifact_id=str(record.get("artifact_id", "")),
        expected_role=str(record.get("expected_role", "")),
        local_path=Path(str(record.get("local_path", ""))),
        local_path_status=str(record.get("local_path_status", "")),
        expected_payload_sha256=str(expected) if expected else None,
        media_type=str(record.get("media_type", "")),
        payload=record,
    )


def _case_from_record(record: dict[str, Any]) -> OutGuessCase:
    if not isinstance(record, dict):
        raise ValueError("case must be a mapping")
    case_id = str(record.get("case_id", ""))
    artifact_id = str(record.get("artifact_id", ""))
    if not case_id or not artifact_id:
        raise ValueError("case_id and artifact_id are required")
    expected_role = str(record.get("expected_role", ""))
    if expected_role not in ALLOWED_ROLES:
        raise ValueError(f"{case_id}: invalid expected_role")
    generate_synthetic = record.get("generate_synthetic")
    return OutGuessCase(
        case_id=case_id,
        artifact_id=artifact_id,
        enabled=bool(record.get("enabled")),
        expected_role=expected_role,
        generate_synthetic=str(generate_synthetic) if generate_synthetic else None,
        require_expected_payload_hash=bool(record.get("require_expected_payload_hash")),
        notes=str(record.get("notes", "")),
        payload=record,
    )


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    resolved = resolve_path(path)
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"expected mapping YAML at {path}")
    return payload
