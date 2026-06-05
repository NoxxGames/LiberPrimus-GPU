from __future__ import annotations

from libreprimus.token_block import stage5dk
from test_stage5dk_common import ensure_stage5dk_built, load_yaml, write_temp_yaml


def test_stage5dk_summary_keeps_all_activation_and_execution_gates_closed() -> None:
    ensure_stage5dk_built()
    summary = load_yaml("data/project-state/stage5dk-summary.yaml")

    for field in [
        "combined_gate_satisfied",
        "activation_authorized",
        "activation_decision_created_now",
        "active_planning_input_authorized",
        "active_planning_input_selected",
        "byte_stream_generation_authorized",
        "byte_stream_generated",
        "execution_authorized",
        "execution_performed",
        "target_class_validation_implemented",
        "tor_network_access_performed",
        "dwh_hash_search_performed",
        "scoring_performed",
        "cuda_performed",
        "website_expansion_performed",
    ]:
        assert summary[field] is False


def test_stage5dk_sidecar_gate_records_validate() -> None:
    ensure_stage5dk_built()

    assert stage5dk.validate_stage5dk_sidecar_gates().validation_error_count == 0
    assert load_yaml("data/token-block/stage5dk-no-active-ingestion-proof.yaml")[
        "active_ingestion_authorized"
    ] is False
    assert load_yaml("data/token-block/stage5dk-no-byte-stream-transition-gate.yaml")[
        "byte_stream_generation_authorized"
    ] is False
    assert load_yaml("data/token-block/stage5dk-no-execution-transition-gate.yaml")[
        "execution_authorized"
    ] is False


def test_stage5dk_governance_validator_rejects_activation(monkeypatch: object, tmp_path) -> None:
    ensure_stage5dk_built()
    summary = load_yaml("data/project-state/stage5dk-summary.yaml")
    summary["activation_authorized"] = True
    summary["combined_gate_satisfied"] = True
    summary["execution_authorized"] = True
    path = write_temp_yaml(tmp_path / "summary.yaml", summary)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "summary", path)

    result = stage5dk.validate_stage5dk_governance_scope()
    assert result.validation_error_count > 0
    assert any("activation_authorized_must_be_false" in error for error in result.errors)
    assert any("combined_gate_satisfied_must_be_false" in error for error in result.errors)
    assert any("execution_authorized_must_be_false" in error for error in result.errors)
