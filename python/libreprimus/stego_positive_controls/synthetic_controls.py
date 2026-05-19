"""Synthetic Stage 4N control metadata used for CI-safe readiness tests."""

from __future__ import annotations

from typing import Any


def synthetic_outguess_controls() -> list[dict[str, Any]]:
    """Return deterministic synthetic control records that do not use historical artefacts."""

    return [
        {
            "fixture_id": "stage4n-synthetic-positive-control",
            "source_id": "stage4n-synthetic",
            "source_url": None,
            "source_path": "synthetic/stage4n-positive.bin",
            "artifact_type": "synthetic_control",
            "expected_role": "synthetic_positive",
            "local_availability": "generated_test_only",
            "toolchain": ["synthetic_control"],
            "notes": "CI-safe synthetic positive; no historical artefact involved.",
        },
        {
            "fixture_id": "stage4n-synthetic-negative-control",
            "source_id": "stage4n-synthetic",
            "source_url": None,
            "source_path": "synthetic/stage4n-negative.bin",
            "artifact_type": "synthetic_control",
            "expected_role": "synthetic_negative",
            "local_availability": "generated_test_only",
            "toolchain": ["synthetic_control"],
            "notes": "CI-safe synthetic negative; no historical artefact involved.",
        },
    ]
