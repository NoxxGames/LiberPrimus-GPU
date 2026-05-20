from __future__ import annotations

import subprocess


def test_stage4p_generated_and_raw_paths_ignored() -> None:
    paths = [
        "experiments/results/result-store-unification/stage4p/source_inventory.json",
        "experiments/results/result-store-unification/stage4p/unified_result_records.jsonl",
        "experiments/results/result-store-unification/stage4p/unified_score_summary_records.jsonl",
        "experiments/results/result-store-unification/stage4p/cross_stage_report.json",
        "experiments/results/result-store-unification/stage4p/summary.json",
        "experiments/results/result-store-unification/stage4p/results.sqlite3",
        "data/raw/example.bin",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
