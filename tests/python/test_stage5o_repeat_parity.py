from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_solved_fixture_cuda_repeat.repeat_parity import build_repeat_parity_records
from libreprimus.gematria_solved_fixture_cuda_repeat.repeat_run_records import build_repeat_run_records
from libreprimus.gematria_solved_fixture_cuda_repeat.repeat_verification import run_repeat_verification
from libreprimus.gematria_solved_fixture_cuda_repeat.validation import validate_stage5o_results


def _records(path: str | Path) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def _write_records(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(yaml.safe_dump({"records": records}, sort_keys=False), encoding="utf-8")


def test_stage5o_committed_repeat_parity_passes_against_stage5l_and_stage5m_hashes() -> None:
    records = _records("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml")
    assert len(records) == 5
    for record in records:
        assert record["repeat_parity_status"] == "passed"
        assert record["stage5l_native_hash_match"] is True
        assert record["stage5m_cuda_hash_match"] is True
        assert record["stage5o_repeat_cuda_output_token_hash"] == record["expected_native_output_token_hash"]
        assert record["stage5o_repeat_cuda_output_token_hash"] == record["stage5m_cuda_output_token_hash"]


def test_stage5o_skipped_repeat_parity_does_not_pass(tmp_path: Path) -> None:
    repeat_run = tmp_path / "repeat-run.yaml"
    repeat_parity = tmp_path / "repeat-parity.yaml"
    build_repeat_run_records(repeat_run_out=repeat_run, out_dir=tmp_path)
    run_repeat_verification(
        repeat_run_records=repeat_run,
        repeat_run_out=repeat_run,
        out_dir=tmp_path,
        skip_run=True,
    )

    records = build_repeat_parity_records(
        repeat_run_records=repeat_run,
        repeat_parity_out=repeat_parity,
        out_dir=tmp_path,
    )

    assert len(records) == 5
    assert all(record["repeat_parity_status"] == "skipped_not_requested" for record in records)
    assert all(record["stage5p_result_store_preflight_ready"] is False for record in records)


def test_stage5o_hash_mismatch_becomes_failed_parity(tmp_path: Path) -> None:
    records = _records("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml")
    records[0]["repeat_cuda_status"] = "passed"
    records[0]["repeat_cuda_output_token_hash"] = "0" * 64
    records[0]["repeat_cuda_native_hash_match"] = False
    records[0]["repeat_cuda_stage5m_hash_match"] = False
    repeat_run = tmp_path / "repeat-run.yaml"
    repeat_parity = tmp_path / "repeat-parity.yaml"
    _write_records(repeat_run, records)

    parity = build_repeat_parity_records(
        repeat_run_records=repeat_run,
        repeat_parity_out=repeat_parity,
        out_dir=tmp_path,
    )

    assert parity[0]["repeat_parity_status"] == "failed_hash_mismatch"


def test_stage5o_validation_rejects_false_pass_hash_mismatch(tmp_path: Path) -> None:
    repeat_run = Path("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml")
    result_store = Path("data/cuda/stage5o-gematria-cuda-result-store-preflight.yaml")
    score = Path("data/cuda/stage5o-gematria-cuda-score-summary-preflight.yaml")
    decision = Path("data/cuda/stage5o-gematria-cuda-expansion-decision.yaml")
    summary = Path("data/cuda/stage5o-repeat-verification-result-store-summary.yaml")
    parity = _records("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml")
    parity[0]["stage5o_repeat_cuda_output_token_hash"] = "0" * 64
    parity_path = tmp_path / "repeat-parity.yaml"
    _write_records(parity_path, parity)

    _, errors = validate_stage5o_results(
        repeat_run_path=repeat_run,
        repeat_parity_path=parity_path,
        result_store_preflight_path=result_store,
        score_summary_preflight_path=score,
        expansion_decision_path=decision,
        summary_path=summary,
        results_dir=Path("experiments/results/gematria-solved-fixture-cuda-repeat/stage5o"),
    )
    assert any("passed parity requires repeat hash equal Stage 5L native hash" in error for error in errors)
