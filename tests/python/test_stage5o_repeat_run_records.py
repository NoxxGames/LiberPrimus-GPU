from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_solved_fixture_cuda_repeat.repeat_run_records import build_repeat_run_records
from libreprimus.gematria_solved_fixture_cuda_repeat.repeat_verification import run_repeat_verification


def _records(path: Path) -> list[dict[str, object]]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))["records"]


def test_stage5o_repeat_run_builder_represents_exact_five_stage5m_mappings(tmp_path: Path) -> None:
    repeat_run = tmp_path / "repeat-run.yaml"
    records = build_repeat_run_records(repeat_run_out=repeat_run, out_dir=tmp_path)
    mapping_ids = {record["mapping_id"] for record in records}

    assert len(records) == 5
    assert mapping_ids == {
        "stage5h-solved-fixture-safe-mapping-00",
        "stage5h-solved-fixture-safe-mapping-01",
        "stage5h-solved-fixture-safe-mapping-02",
        "stage5h-solved-fixture-safe-mapping-03",
        "stage5h-solved-fixture-safe-mapping-04",
    }
    for record in records:
        assert record["executed_kernel"] == "gematria_mod29_shift_score_kernel"
        assert record["executed_semantics"] == "gematria_shift_score_only"
        assert record["additional_cuda_execution_scope"] == "exact_stage5m_repeat_only"
        assert record["new_cuda_kernels_added"] == 0
        assert record["cuda_source_modified"] is False
        assert record["unsolved_page_cuda_used"] is False
        assert record["real_liber_primus_cuda_data_used"] is False

    assert _records(repeat_run) == records


def test_stage5o_no_gpu_safe_skip_cannot_claim_repeat_success(tmp_path: Path) -> None:
    repeat_run = tmp_path / "repeat-run.yaml"
    build_repeat_run_records(repeat_run_out=repeat_run, out_dir=tmp_path)

    skipped = run_repeat_verification(
        repeat_run_records=repeat_run,
        repeat_run_out=repeat_run,
        out_dir=tmp_path,
        skip_run=True,
    )

    assert len(skipped) == 5
    for record in skipped:
        assert record["repeat_cuda_status"] == "skipped_not_requested"
        assert record["repeat_cuda_attempted"] is False
        assert record["repeat_cuda_execution_performed"] is False
        assert record["repeat_cuda_output_token_hash"] is None
        assert record["stage5p_ready"] is False
