from __future__ import annotations

from pathlib import Path

from test_stage5z_prime_cuda_contract_schemas import _build_all, _records, _summary


def test_stage5z_next_stage_selects_stage5aa_and_not_deep_research(tmp_path: Path) -> None:
    paths = _build_all(tmp_path)
    records = _records(paths["decision"])
    selected = [record for record in records if record["selected"] is True]
    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5aa_prime_minus_one_cuda_synthetic_kernel_implementation"
    assert "Stage 5AA - prime-minus-one CUDA synthetic kernel implementation" in (
        selected[0]["recommended_stage_title"]
    )
    deep = [record for record in records if record["recommended_prompt_type"] == "Deep Research"]
    assert len(deep) == 1
    assert deep[0]["selected"] is False
    summary = _summary(paths["summary"])
    assert summary["deep_research_recommended_next"] is False
    assert "Stage 5AA - prime-minus-one CUDA synthetic kernel implementation" in (
        summary["recommended_next_stage_title"]
    )
