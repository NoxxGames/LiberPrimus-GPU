from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_solved_fixture_cuda.parity_records import build_parity_records
from libreprimus.gematria_solved_fixture_cuda.summary import decide_next_stage
from libreprimus.gematria_solved_fixture_cuda.validation import validate_stage5m_results


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5m_passed_parity_requires_cuda_hash_equal_native_hash() -> None:
    records = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml")
    assert len(records) == 5
    for record in records:
        assert record["parity_status"] == "passed"
        assert record["cuda_native_hash_match"] is True
        assert record["cuda_output_token_hash"] == record["expected_native_output_token_hash"]
        assert record["stage5n_ready"] is True


def test_stage5m_skipped_cuda_run_cannot_claim_pass(tmp_path: Path) -> None:
    run_records = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml")
    for record in run_records:
        record["cuda_run_status"] = "skipped_not_requested"
        record["cuda_run_attempted"] = False
        record["cuda_execution_performed"] = False
        record["solved_fixture_cuda_used"] = False
        record["cuda_native_hash_match"] = None
        record["cuda_output_token_hash"] = None
        record["stage5n_ready"] = False
    run_path = tmp_path / "run.yaml"
    parity_path = tmp_path / "parity.yaml"
    run_path.write_text(yaml.safe_dump({"records": run_records}, sort_keys=False), encoding="utf-8")

    parity = build_parity_records(run_records=run_path, parity_records_out=parity_path, out_dir=tmp_path)
    assert len(parity) == 5
    assert all(record["parity_status"] == "skipped_not_requested" for record in parity)
    assert all(record["stage5n_ready"] is False for record in parity)


def test_stage5m_next_stage_decision_is_deterministic() -> None:
    ready, ready_reason = decide_next_stage(pass_count=5, fail_count=0, skip_count=0)
    assert ready.startswith("Stage 5N")
    assert "matched" in ready_reason

    mismatch, _ = decide_next_stage(pass_count=4, fail_count=1, skip_count=0)
    assert mismatch.startswith("Stage 5M-fix")

    missing_cuda, _ = decide_next_stage(pass_count=0, fail_count=0, skip_count=5)
    assert missing_cuda.startswith("Stage 5M-followup")


def test_stage5m_validation_rejects_false_pass(tmp_path: Path) -> None:
    run_records = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml")
    parity_records = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml")
    boundaries = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml")
    summary = yaml.safe_load(Path("data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml").read_text(encoding="utf-8"))
    parity_records[0]["cuda_output_token_hash"] = "0" * 64

    run_path = tmp_path / "run.yaml"
    parity_path = tmp_path / "parity.yaml"
    boundary_path = tmp_path / "boundaries.yaml"
    summary_path = tmp_path / "summary.yaml"
    run_path.write_text(yaml.safe_dump({"records": run_records}, sort_keys=False), encoding="utf-8")
    parity_path.write_text(yaml.safe_dump({"records": parity_records}, sort_keys=False), encoding="utf-8")
    boundary_path.write_text(yaml.safe_dump({"records": boundaries}, sort_keys=False), encoding="utf-8")
    summary_path.write_text(yaml.safe_dump(summary, sort_keys=False), encoding="utf-8")

    _, errors = validate_stage5m_results(
        run_records_path=run_path,
        parity_records_path=parity_path,
        boundaries_path=boundary_path,
        summary_path=summary_path,
        results_dir=tmp_path,
    )
    assert any("passed parity requires CUDA hash equal native hash" in error for error in errors)
