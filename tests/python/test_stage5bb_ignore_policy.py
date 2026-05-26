import subprocess


def test_stage5bb_generated_outputs_and_codex_output_are_ignored() -> None:
    paths = [
        "experiments/results/token-block/stage5bb/dry_run_plan_preview.json",
        "experiments/results/token-block/stage5bb/manifest_reference_validation.json",
        "experiments/results/token-block/stage5bb/fixtures/fixture_result_schema_records.json",
        "codex-output/stage5bb-codex-completion.md",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path


def test_stage5bb_raw_third_party_remains_ignored() -> None:
    result = subprocess.run(["git", "check-ignore", "-q", "third_party/LiberPrimusPages/example.png"], check=False)

    assert result.returncode == 0
