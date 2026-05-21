from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_expansion_candidate_mapping.candidate_inventory import build_candidate_inventory
from libreprimus.gematria_expansion_candidate_mapping.expansion_gate import build_expansion_gate_records
from libreprimus.gematria_expansion_candidate_mapping.native_parity import build_native_parity_records
from libreprimus.gematria_expansion_candidate_mapping.result_store_preflight import build_result_store_preflight_records
from libreprimus.gematria_expansion_candidate_mapping.summary import build_summary
from libreprimus.gematria_expansion_candidate_mapping.token_mapping import build_token_mapping_records


def test_stage5q_gate_selects_stage5r_when_mapping_ready(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.yaml"
    mapping = tmp_path / "mapping.yaml"
    native = tmp_path / "native.yaml"
    preflight = tmp_path / "preflight.yaml"
    gate = tmp_path / "gate.yaml"
    summary = tmp_path / "summary.yaml"
    build_candidate_inventory(candidate_inventory_out=inventory, out_dir=tmp_path / "inventory-out")
    build_token_mapping_records(candidate_inventory=inventory, token_mapping_out=mapping, out_dir=tmp_path / "mapping-out")
    build_native_parity_records(token_mapping=mapping, native_parity_out=native, out_dir=tmp_path / "native-out")
    build_result_store_preflight_records(
        token_mapping=mapping,
        native_parity=native,
        result_store_preflight_out=preflight,
        out_dir=tmp_path / "preflight-out",
    )

    gate_records = build_expansion_gate_records(
        candidate_inventory=inventory,
        token_mapping=mapping,
        native_parity=native,
        result_store_preflight=preflight,
        expansion_gate_out=gate,
        out_dir=tmp_path / "gate-out",
    )
    payload = build_summary(
        candidate_inventory=inventory,
        token_mapping=mapping,
        native_parity=native,
        result_store_preflight=preflight,
        expansion_gate=gate,
        summary_out=summary,
        out_dir=tmp_path / "summary-out",
    )

    assert gate_records[0]["stage5r_ready"] is True
    assert "Stage 5R" in gate_records[0]["selected_next_stage"]
    assert gate_records[0]["deep_research_recommended"] is False
    assert payload["new_candidate_count"] == 3
    assert payload["stage5l_5m_5o_duplicate_exclusion_status"].startswith("exact_five_buffer_pack")
    assert payload["cuda_execution_performed"] is False
