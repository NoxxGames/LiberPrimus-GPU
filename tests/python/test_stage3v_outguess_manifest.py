from __future__ import annotations

from libreprimus.stego.outguess_manifest import load_artifacts, load_manifest, validate_manifest_and_artifacts


def test_stage3v_outguess_manifest_validates() -> None:
    summary, errors = validate_manifest_and_artifacts(
        "experiments/manifests/stego/outguess-regression-v1.yaml",
        "data/observations/stego/outguess-artifacts-v0.yaml",
    )

    assert errors == []
    assert summary["case_count"] == 7
    assert summary["historical_positive_placeholder_count"] == 4
    assert summary["synthetic_control_count"] == 3
    assert summary["no_solve_claim"] is True


def test_stage3v_artifact_and_manifest_flags_are_safe() -> None:
    manifest = load_manifest("experiments/manifests/stego/outguess-regression-v1.yaml")
    artifacts = load_artifacts("data/observations/stego/outguess-artifacts-v0.yaml")

    assert manifest.allow_missing_tool is True
    assert manifest.allow_missing_assets is True
    assert manifest.payload["cuda_enabled"] is False
    assert manifest.payload["no_solve_claim"] is True
    assert all(record.payload["solve_claim"] is False for record in artifacts.values())
