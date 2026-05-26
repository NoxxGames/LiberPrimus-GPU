import subprocess


def test_stage5az_generated_outputs_and_codex_output_are_ignored() -> None:
    paths = [
        "experiments/results/token-block/stage5az/preflight_manifest_integrity_audit.json",
        "experiments/results/token-block/stage5az/repaired_variant_family_manifest.json",
        "codex-output/stage5az-codex-completion.md",
    ]

    for path in paths:
        result = subprocess.run(
            ["git", "check-ignore", "-q", path],
            check=False,
            text=True,
        )
        assert result.returncode == 0, path


def test_stage5az_raw_third_party_remains_ignored() -> None:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "third_party/LiberPrimusPages/example.png"],
        check=False,
        text=True,
    )

    assert result.returncode == 0
