from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_solved_fixture_cuda_repeat.expansion_decision import build_expansion_decision


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def _write(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(yaml.safe_dump({"records": records}, sort_keys=False), encoding="utf-8")


def test_stage5o_expansion_decision_is_stage5p_ready_for_clean_repeat(tmp_path: Path) -> None:
    records = build_expansion_decision(expansion_decision_out=tmp_path / "decision.yaml", out_dir=tmp_path)

    assert records[0]["decision_status"] == "stage5p_ready"
    assert records[0]["stage5p_ready"] is True
    assert records[0]["selected_next_stage"] == "Stage 5P - controlled solved-fixture CUDA result-store integration"
    assert records[0]["broad_solved_fixture_cuda_allowed"] is False
    assert records[0]["unsolved_page_cuda_allowed"] is False


def test_stage5o_expansion_decision_routes_skips_mismatches_and_preflight_blockers(tmp_path: Path) -> None:
    parity = _records("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml")
    result_store = _records("data/cuda/stage5o-gematria-cuda-result-store-preflight.yaml")
    score = _records("data/cuda/stage5o-gematria-cuda-score-summary-preflight.yaml")

    skip_parity = [{**record, "repeat_parity_status": "skipped_not_requested"} for record in parity]
    skip_path = tmp_path / "skip-parity.yaml"
    result_path = tmp_path / "result-store.yaml"
    score_path = tmp_path / "score.yaml"
    _write(skip_path, skip_parity)
    _write(result_path, result_store)
    _write(score_path, score)
    skipped = build_expansion_decision(
        repeat_parity=skip_path,
        result_store_preflight=result_path,
        score_summary_preflight=score_path,
        expansion_decision_out=tmp_path / "skip-decision.yaml",
        out_dir=tmp_path,
    )
    assert skipped[0]["decision_status"] == "repeat_verification_followup_required"

    mismatch_parity = [{**record} for record in parity]
    mismatch_parity[0]["repeat_parity_status"] = "failed_hash_mismatch"
    mismatch_path = tmp_path / "mismatch-parity.yaml"
    _write(mismatch_path, mismatch_parity)
    mismatch = build_expansion_decision(
        repeat_parity=mismatch_path,
        result_store_preflight=result_path,
        score_summary_preflight=score_path,
        expansion_decision_out=tmp_path / "mismatch-decision.yaml",
        out_dir=tmp_path,
    )
    assert mismatch[0]["decision_status"] == "repeat_hash_mismatch_investigation_required"

    blocked_result = [{**record, "stage5p_ready": False} for record in result_store]
    blocked_score = [{**record, "stage5p_ready": False} for record in score]
    blocked_result_path = tmp_path / "blocked-result.yaml"
    blocked_score_path = tmp_path / "blocked-score.yaml"
    _write(blocked_result_path, blocked_result)
    _write(blocked_score_path, blocked_score)
    blocked = build_expansion_decision(
        result_store_preflight=blocked_result_path,
        score_summary_preflight=blocked_score_path,
        expansion_decision_out=tmp_path / "blocked-decision.yaml",
        out_dir=tmp_path,
    )
    assert blocked[0]["decision_status"] == "preflight_followup_required"
