import subprocess
import sys


def test_stage5au_validate_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", "validate-stage5au"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "token_block_stage5au_valid=true" in result.stdout
    assert "case_review_challenge_count=203" in result.stdout


def test_stage5au_validate_cli_does_not_require_ignored_pack_body() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "libreprimus.cli",
            "token-block",
            "validate-stage5au",
            "--review-pack-root",
            "human-review-packs/stage5au/not-present-in-ci",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "token_block_stage5au_valid=true" in result.stdout
    assert "review_pack_v2_local_present=false" in result.stdout


def test_stage5au_review_pack_v2_validate_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "token-block", "validate-stage5au-review-pack-v2"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "token_block_stage5au_review_pack_v2_valid=true" in result.stdout
    assert "canonical_challenges_rendered=212" in result.stdout
