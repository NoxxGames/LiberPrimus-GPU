from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import yaml

from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest
from libreprimus.experiment_execution.models import CPUExecutionManifest
from libreprimus.experiment_execution.safety_gates import evaluate_execution_safety_gates

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "experiments/results/cpu-execution/stage2f"
DIRECT = REPO / "experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml"
SOLVED = REPO / "experiments/manifests/cpu-execution/stage2f-solved-baseline-replay.yaml"


def test_synthetic_safe_manifest_passes() -> None:
    manifest = load_cpu_execution_manifest(DIRECT)
    gates = evaluate_execution_safety_gates(manifest, out_dir=OUT_DIR)

    assert all(gate.status == "pass" for gate in gates)


def test_solved_fixture_only_manifest_passes() -> None:
    manifest = load_cpu_execution_manifest(SOLVED)
    gates = evaluate_execution_safety_gates(manifest, out_dir=OUT_DIR)

    assert all(gate.status == "pass" for gate in gates)


def test_future_unsolved_page_candidate_fails_gate() -> None:
    payload = yaml.safe_load(DIRECT.read_text(encoding="utf-8"))
    payload["corpus_slice"] = {"slice_kind": "future_unsolved_page_candidate"}
    manifest = CPUExecutionManifest(payload=payload, path="synthetic", sha256="0")

    gates = evaluate_execution_safety_gates(manifest, out_dir=OUT_DIR)

    assert any(gate.gate_id == "corpus_slice_safe" and gate.status == "fail" for gate in gates)


def test_output_path_outside_ignored_dir_fails(tmp_path: Path) -> None:
    manifest = load_cpu_execution_manifest(DIRECT)
    gates = evaluate_execution_safety_gates(manifest, out_dir=tmp_path)

    assert any(gate.gate_id == "output_path_policy" and gate.status == "fail" for gate in gates)


def test_transform_with_search_enabled_fails(monkeypatch) -> None:
    import libreprimus.experiment_execution.safety_gates as safety_gates

    manifest = load_cpu_execution_manifest(DIRECT)
    bad_definition = SimpleNamespace(
        supports_cpu_reference=True,
        search_enabled=True,
        supports_gpu=False,
    )
    monkeypatch.setattr(safety_gates, "load_registry", lambda: object())
    monkeypatch.setattr(safety_gates, "resolve_transform", lambda _registry, _transform_id: bad_definition)

    gates = evaluate_execution_safety_gates(manifest, out_dir=OUT_DIR)

    assert any(gate.gate_id == "transform_search_disabled" and gate.status == "fail" for gate in gates)

