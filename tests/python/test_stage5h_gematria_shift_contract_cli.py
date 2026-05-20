from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


CONTRACT_MANIFEST = "experiments/manifests/cuda/stage5h-gematria-shift-score-contract.yaml"
FIXTURE_MANIFEST = "experiments/manifests/cuda/stage5h-gematria-native-parity-fixtures.yaml"
MAPPING_MANIFEST = "experiments/manifests/cuda/stage5h-solved-fixture-safe-mapping.yaml"


def test_stage5h_cli_no_gpu_safe_round_trip(tmp_path: Path) -> None:
    out_dir = tmp_path / "stage5h"
    contract = tmp_path / "contract.yaml"
    fixtures = tmp_path / "fixtures.yaml"
    mapping = tmp_path / "mapping.yaml"
    score_plan = tmp_path / "score-plan.yaml"
    summary = tmp_path / "summary.yaml"
    runner = CliRunner()

    contract_result = runner.invoke(
        app,
        [
            "gematria-shift-contract",
            "build-contract",
            "--manifest",
            CONTRACT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--contract-out",
            str(contract),
            "--allow-warnings",
        ],
    )
    assert contract_result.exit_code == 0, contract_result.output
    assert "token_domain=integers_0_to_28" in contract_result.output

    fixture_result = runner.invoke(
        app,
        [
            "gematria-shift-contract",
            "build-native-fixtures",
            "--manifest",
            FIXTURE_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--fixtures-out",
            str(fixtures),
            "--allow-warnings",
        ],
    )
    assert fixture_result.exit_code == 0, fixture_result.output
    assert "stage5f_hash_is_gematria_fixture_hash=false" in fixture_result.output

    mapping_result = runner.invoke(
        app,
        [
            "gematria-shift-contract",
            "build-solved-fixture-mapping",
            "--manifest",
            MAPPING_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--mapping-out",
            str(mapping),
            "--allow-warnings",
        ],
    )
    assert mapping_result.exit_code == 0, mapping_result.output
    assert "solved_fixture_cuda_execution_allowed=false" in mapping_result.output

    score_result = runner.invoke(
        app,
        [
            "gematria-shift-contract",
            "build-score-summary-plan",
            "--manifest",
            CONTRACT_MANIFEST,
            "--out-dir",
            str(out_dir),
            "--score-summary-plan-out",
            str(score_plan),
            "--allow-warnings",
        ],
    )
    assert score_result.exit_code == 0, score_result.output

    summary_result = runner.invoke(
        app,
        [
            "gematria-shift-contract",
            "build-summary",
            "--contract",
            str(contract),
            "--fixtures",
            str(fixtures),
            "--mapping",
            str(mapping),
            "--score-summary-plan",
            str(score_plan),
            "--summary-out",
            str(summary),
            "--out-dir",
            str(out_dir),
            "--allow-warnings",
        ],
    )
    assert summary_result.exit_code == 0, summary_result.output

    validate = runner.invoke(
        app,
        [
            "gematria-shift-contract",
            "validate-stage5h",
            "--contract",
            str(contract),
            "--fixtures",
            str(fixtures),
            "--mapping",
            str(mapping),
            "--score-summary-plan",
            str(score_plan),
            "--summary",
            str(summary),
            "--results-dir",
            str(out_dir),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "gematria_shift_contract_stage5h_valid=true" in validate.output
