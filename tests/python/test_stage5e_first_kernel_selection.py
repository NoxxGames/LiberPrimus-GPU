from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_kernel_contract.selection import select_first_kernel_contract


def test_stage5e_selects_shift_score_contract(tmp_path: Path) -> None:
    contract, adapter = select_first_kernel_contract(
        out_dir=tmp_path / "out",
        contract_out=tmp_path / "contract.yaml",
        adapter_selection_out=tmp_path / "adapter.yaml",
    )

    selected = contract[0]
    assert selected["selected_kernel_id"] == "shift_score_kernel"
    assert selected["selected_target_id"] == "stage5a-caesar_mod29-cuda-target"
    assert selected["selected_transform_family"] == "caesar_mod29"
    assert selected["cuda_kernel_added"] is False
    assert selected["cuda_transform_executed"] is False
    assert len(selected["alternate_candidates"]) == 3
    assert len(selected["blocked_or_rejected_candidates"]) == 10

    assert adapter[0]["selected_adapter_family"] == "native_cpu_synthetic_shift_adapter"
    assert adapter[0]["stage5d_reference_required"] is True
    assert adapter[0]["cuda_source_modified"] is False
