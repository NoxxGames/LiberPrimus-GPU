from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest

REPO = Path(__file__).resolve().parents[2]
MANIFEST_DIR = REPO / "experiments/manifests/cpu-execution"
SAFE_MANIFESTS = [
    "stage2f-synthetic-direct-execution.yaml",
    "stage2f-synthetic-reverse-gematria-execution.yaml",
    "stage2f-synthetic-rotated-reverse-execution.yaml",
    "stage2f-synthetic-vigenere-execution.yaml",
    "stage2f-synthetic-prime-stream-execution.yaml",
    "stage2f-solved-baseline-replay.yaml",
]
BLOCKED = MANIFEST_DIR / "stage2f-blocked-unsolved-example.yaml"


@pytest.mark.parametrize("name", SAFE_MANIFESTS)
def test_safe_stage2f_manifest_validates(name: str) -> None:
    manifest = load_cpu_execution_manifest(MANIFEST_DIR / name)

    assert manifest.payload["search_execution_enabled"] is False
    assert manifest.payload["candidate_generation_enabled"] is False
    assert manifest.payload["scoring_enabled"] is False
    assert manifest.payload["cuda_enabled"] is False
    assert manifest.payload["canonical_corpus_active"] is False


def test_blocked_unsolved_manifest_fails_as_expected() -> None:
    payload = yaml.safe_load(BLOCKED.read_text(encoding="utf-8"))

    assert payload["expected_validation_status"] == "fail"
    with pytest.raises(ValueError):
        load_cpu_execution_manifest(BLOCKED)


def test_generated_cpu_execution_outputs_are_ignored() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", "experiments/results/cpu-execution/stage2f/summary.json"],
        cwd=REPO,
        check=False,
    )

    assert result.returncode == 0

