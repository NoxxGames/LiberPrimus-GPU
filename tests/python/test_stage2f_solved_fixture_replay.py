from __future__ import annotations

from pathlib import Path

from libreprimus.experiment_execution.cpu_runner import run_cpu_execution_manifest
from libreprimus.experiment_execution.execution_planner import build_execution_plan
from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/cpu-execution/stage2f-solved-baseline-replay.yaml"
OUT_DIR = REPO / "experiments/results/cpu-execution/stage2f"


def test_solved_baseline_replay_manifest_validates() -> None:
    manifest = load_cpu_execution_manifest(MANIFEST)

    assert manifest.execution_scope == "solved_fixture_only"


def test_replay_plan_is_solved_fixture_only() -> None:
    plan = build_execution_plan(MANIFEST, out_dir=OUT_DIR)

    assert plan.execution_scope == "solved_fixture_only"
    assert plan.unsolved_execution_allowed is False


def test_replay_records_expected_ten_passes_without_unsolved_text() -> None:
    _, results, _ = run_cpu_execution_manifest(MANIFEST, out_dir=OUT_DIR)

    assert results[0].match_status == "pass"
    assert "pass_count=10" in results[0].output_normalized_text
    assert results[0].unsolved_execution_allowed is False

