from __future__ import annotations

from pathlib import Path

from libreprimus.experiments.dry_run_planner import build_dry_run_plan
from libreprimus.solved_fixtures.models import to_jsonable

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/exploratory/stage2e-caesar-preview-dry-run.yaml"


def test_dry_run_produces_plan_record(tmp_path: Path) -> None:
    plan = build_dry_run_plan(MANIFEST, out_dir=tmp_path)

    assert plan.record_type == "exploratory_dry_run_plan"
    assert plan.manifest_id == "stage2e-caesar-preview-dry-run"
    assert plan.candidate_count_estimate == 29


def test_plan_preserves_disabled_execution_flags(tmp_path: Path) -> None:
    plan = build_dry_run_plan(MANIFEST, out_dir=tmp_path)

    assert plan.execution_enabled is False
    assert plan.search_execution_enabled is False
    assert plan.scoring_enabled is False
    assert plan.cuda_enabled is False
    assert plan.canonical_corpus_active is False


def test_plan_has_no_candidate_plaintext_field(tmp_path: Path) -> None:
    payload = to_jsonable(build_dry_run_plan(MANIFEST, out_dir=tmp_path))
    serialized_keys = " ".join(payload.keys())

    assert "candidate_plaintext" not in payload
    assert "plaintext" not in serialized_keys


def test_generated_plan_is_deterministic(tmp_path: Path) -> None:
    first = to_jsonable(build_dry_run_plan(MANIFEST, out_dir=tmp_path))
    second = to_jsonable(build_dry_run_plan(MANIFEST, out_dir=tmp_path))

    assert first == second


def test_safety_gate_results_are_recorded(tmp_path: Path) -> None:
    plan = build_dry_run_plan(MANIFEST, out_dir=tmp_path)

    assert plan.safety_gate_results
    assert all(gate["status"] == "pass" for gate in plan.safety_gate_results)
