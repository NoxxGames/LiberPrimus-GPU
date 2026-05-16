from __future__ import annotations

from pathlib import Path

import subprocess
import yaml

from libreprimus.experiments.candidate_estimator import estimate_candidate_count
from libreprimus.experiments.manifest_loader import load_exploratory_manifest

REPO = Path(__file__).resolve().parents[2]
MANIFEST_DIR = REPO / "experiments/manifests/exploratory"


def _manifest_paths() -> list[Path]:
    return sorted(MANIFEST_DIR.glob("*-dry-run.yaml"))


def test_all_stage2e_manifests_validate() -> None:
    for path in _manifest_paths():
        load_exploratory_manifest(path)


def test_preview_counts_match_expected_values() -> None:
    counts = {
        load_exploratory_manifest(path).manifest_id: estimate_candidate_count(
            load_exploratory_manifest(path).payload
        ).candidate_count
        for path in _manifest_paths()
    }

    assert counts["stage2e-direct-known-fixture-dry-run"] == 1
    assert counts["stage2e-caesar-preview-dry-run"] == 29
    assert counts["stage2e-affine-preview-dry-run"] == 812
    assert counts["stage2e-vigenere-key-list-preview-dry-run"] == 2
    assert counts["stage2e-prime-stream-parameter-preview-dry-run"] == 1


def test_all_manifests_disable_execution_scoring_and_cuda() -> None:
    for path in _manifest_paths():
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        for field in [
            "execution_enabled",
            "search_execution_enabled",
            "candidate_generation_enabled",
            "scoring_enabled",
            "cuda_enabled",
            "canonical_corpus_active",
            "page_boundaries_final",
            "trusted_as_canonical",
        ]:
            assert payload[field] is False


def test_dry_run_output_paths_are_ignored() -> None:
    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "-q",
            "--",
            "experiments/results/exploratory-dry-runs/stage2e/summary.json",
        ],
        cwd=REPO,
        check=False,
    )

    assert result.returncode == 0
