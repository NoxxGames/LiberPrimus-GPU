from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_parity.native_execution import build_native_run_records, execute_prime_minus_one_tokens


def test_stage5x_native_execution_attempts_only_ready_mappings(tmp_path: Path) -> None:
    records = build_native_run_records(native_run_out=tmp_path / "run.yaml", out_dir=tmp_path)
    attempted = [record for record in records if record["native_execution_performed"] is True]
    skipped = [record for record in records if record["native_execution_status"].startswith("skipped")]
    assert {record["mapping_id"] for record in attempted} == {
        "stage5w-mapping-synthetic-prime-control-v0",
        "stage5w-mapping-p56-stage4o-bounded-v0",
    }
    assert [record["mapping_id"] for record in skipped] == ["stage5w-mapping-p56-full-fixture-blocked-v0"]
    assert all(record["cuda_execution_performed"] is False for record in records)
    assert all(record["gpu_benchmark_performed"] is False for record in records)


def test_stage5x_prime_minus_one_formula_preserves_separator_and_advances_on_runes_only() -> None:
    tokens = [
        {"position": 0, "token_kind": "rune", "transformable": True, "index29": 0},
        {"position": 1, "token_kind": "word_separator", "transformable": False, "index29": -1},
        {"position": 2, "token_kind": "rune", "transformable": True, "index29": 2},
    ]
    output, used = execute_prime_minus_one_tokens(tokens=tokens, stream_values=[1, 2])
    assert used == [1, 2]
    assert output == [
        {"position": 0, "token_kind": "rune", "transformable": True, "index29": 28},
        {"position": 1, "token_kind": "word_separator", "transformable": False, "index29": -1},
        {"position": 2, "token_kind": "rune", "transformable": True, "index29": 0},
    ]
