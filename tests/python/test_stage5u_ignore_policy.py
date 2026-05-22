from __future__ import annotations

import subprocess


def _ignored(path: str) -> bool:
    return subprocess.run(["git", "check-ignore", "-q", path], check=False).returncode == 0


def test_stage5u_generated_raw_codex_and_sqlite_paths_are_ignored() -> None:
    paths = [
        "experiments/results/cuda-candidate-batch-abi/stage5u/candidate_batch_abi_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/token_buffer_contract_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/transform_parameter_contract_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/key_schedule_contract_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/stream_schedule_contract_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/score_vector_contract_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/topk_contract_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/backend_contract_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/result_store_compatibility_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/gap_closure_report.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/next_stage_decision.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/summary.json",
        "experiments/results/cuda-candidate-batch-abi/stage5u/warnings.jsonl",
        "experiments/results/cuda-candidate-batch-abi/stage5u/results.sqlite3",
        "codex-output/stage5u-codex-completion.md",
        "data/raw/stage5u-example.txt",
    ]
    for path in paths:
        assert _ignored(path), path


def test_stage5u_raw_generated_codex_and_sqlite_not_staged() -> None:
    completed = subprocess.run(["git", "diff", "--cached", "--name-only"], check=True, capture_output=True, text=True)
    staged = completed.stdout.splitlines()
    assert not any(path.startswith("data/raw/") for path in staged)
    assert not any(path.startswith("codex-output/") for path in staged)
    assert not any(path.endswith((".sqlite", ".sqlite3", ".db")) for path in staged)
    generated = [
        path
        for path in staged
        if path.startswith("experiments/results/") and not path.endswith((".gitkeep", "README.md"))
    ]
    assert generated == []
