from __future__ import annotations

import subprocess

from test_stage5dy_common import ROOT, ensure_stage5dy_built, load_yaml, run_token_block_cli


def test_nonmutating_validator_policy() -> None:
    ensure_stage5dy_built()
    payload = load_yaml("data/project-state/stage5dy-nonmutating-validator-policy.yaml")

    assert payload["validate_commands_read_only_for_committed_data"] is True
    assert payload["summary_commands_read_only_for_committed_data"] is True
    assert payload["build_commands_write_current_stage_records_only"] is True
    assert payload["parallel_validation_writes_ignored_outputs_only"] is True


def test_representative_validate_and_summary_commands_do_not_mutate_tracked_files() -> None:
    ensure_stage5dy_built()
    before = subprocess.run(
        ["git", "diff", "--name-only", "--", "data", "python", "schemas", "scripts", "tests", "docs"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    run_token_block_cli("validate-stage5dy-validation-profile-registry")
    run_token_block_cli("validate-stage5dy-nonmutating-validator-policy")
    run_token_block_cli("stage5dy-summary")

    after = subprocess.run(
        ["git", "diff", "--name-only", "--", "data", "python", "schemas", "scripts", "tests", "docs"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert after == before
