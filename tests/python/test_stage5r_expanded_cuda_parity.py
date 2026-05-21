from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_expanded_solved_fixture_cuda.cuda_parity import run_cuda_parity
from libreprimus.gematria_expanded_solved_fixture_cuda.parity_records import build_parity_records
from libreprimus.gematria_expanded_solved_fixture_cuda.summary import decide_next_stage
from libreprimus.gematria_expanded_solved_fixture_cuda.validation import validate_stage5r_results


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def _write_records(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(yaml.safe_dump({"records": records}, sort_keys=False), encoding="utf-8")


def test_stage5r_skipped_cuda_run_cannot_claim_pass(tmp_path: Path) -> None:
    run_path = tmp_path / "run.yaml"
    parity_path = tmp_path / "parity.yaml"
    _write_records(run_path, _records("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml"))

    skipped = run_cuda_parity(run_records_path=run_path, run_records_out=run_path, out_dir=tmp_path, skip_run=True)
    parity = build_parity_records(run_records=run_path, parity_records_out=parity_path, out_dir=tmp_path)

    assert all(record["cuda_run_status"] == "skipped_not_requested" for record in skipped)
    assert all(record["cuda_run_attempted"] is False for record in skipped)
    assert all(record["parity_status"] == "skipped_not_requested" for record in parity)
    assert all(record["stage5s_ready"] is False for record in parity)


def test_stage5r_passed_parity_requires_cuda_hash_equal_native_hash() -> None:
    parity = _records("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml")
    assert len(parity) == 3
    for record in parity:
        assert record["parity_status"] == "passed"
        assert record["cuda_run_attempted"] is True
        assert record["cuda_native_hash_match"] is True
        assert record["stage5r_cuda_output_token_hash"] == record["stage5q_native_output_token_hash"]
        assert record["stage5s_ready"] is True


def test_stage5r_validation_rejects_false_pass(tmp_path: Path) -> None:
    paths = {
        "run": "data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml",
        "parity": "data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml",
        "boundary": "data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml",
        "result": "data/cuda/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml",
        "score": "data/cuda/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml",
    }
    for name, source in paths.items():
        Path(tmp_path, f"{name}.yaml").write_text(Path(source).read_text(encoding="utf-8"), encoding="utf-8")
    summary = yaml.safe_load(Path("data/cuda/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml").read_text(encoding="utf-8"))
    parity = yaml.safe_load(Path(tmp_path, "parity.yaml").read_text(encoding="utf-8"))["records"]
    parity[0]["stage5r_cuda_output_token_hash"] = "0" * 64
    Path(tmp_path, "parity.yaml").write_text(yaml.safe_dump({"records": parity}, sort_keys=False), encoding="utf-8")
    Path(tmp_path, "summary.yaml").write_text(yaml.safe_dump(summary, sort_keys=False), encoding="utf-8")

    _, errors = validate_stage5r_results(
        run_records_path=tmp_path / "run.yaml",
        parity_records_path=tmp_path / "parity.yaml",
        boundaries_path=tmp_path / "boundary.yaml",
        result_store_preflight_path=tmp_path / "result.yaml",
        score_summary_preflight_path=tmp_path / "score.yaml",
        summary_path=tmp_path / "summary.yaml",
        results_dir=tmp_path,
    )
    assert any("passed parity requires Stage 5R CUDA hash equal Stage 5Q native hash" in error for error in errors)


def test_stage5r_next_stage_decision_is_deterministic() -> None:
    ready, ready_reason = decide_next_stage(pass_count=3, fail_count=0, skip_count=0)
    assert ready.startswith("Stage 5S")
    assert "matched" in ready_reason
    mismatch, _ = decide_next_stage(pass_count=2, fail_count=1, skip_count=0)
    assert mismatch.startswith("Stage 5R-fix")
    missing_cuda, _ = decide_next_stage(pass_count=0, fail_count=0, skip_count=3)
    assert missing_cuda.startswith("Stage 5R-followup")
    partial, _ = decide_next_stage(pass_count=1, fail_count=0, skip_count=2)
    assert "partial" in partial
