from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app


EXPECTED_GROUPS = {
    "legacy-workbook",
    "legacy-pastebin",
    "transcript-source",
    "corpus-alignment",
    "profile",
    "corpus-candidate",
    "reference-source",
    "transform-registry",
    "solved-baseline",
    "result-store",
    "consistency",
    "experiment",
    "execution",
    "proposal",
    "approval-execution",
    "approval-readiness",
    "bounded-experiment",
    "bounded-run",
    "candidate-inspect",
    "scoring",
    "archive",
    "observation",
    "hash-preimage",
    "image-analysis",
    "image-transform",
    "discord-ingest",
    "discord-promote",
    "discord-review",
    "discord-leads",
    "discord-full-review",
    "post-discord",
    "research-synthesis",
    "stego",
    "solved-fixture",
}


def test_stage3x_root_app_exists() -> None:
    assert app is not None


def test_stage3x_root_command_groups_preserved() -> None:
    groups = {group.name for group in app.registered_groups}

    assert EXPECTED_GROUPS <= groups


def test_stage3x_root_commands_preserved() -> None:
    commands = {_command_name(command) for command in app.registered_commands}

    assert {"smoke", "paths", "toolchain"} <= commands


def test_stage3x_key_subcommands_preserved() -> None:
    group_commands = {
        group.name: {_command_name(command) for command in group.typer_instance.registered_commands}
        for group in app.registered_groups
    }

    assert {"check-state-drift", "check-all"} <= group_commands["consistency"]
    assert "outguess-run" in group_commands["stego"]
    assert "run-cookie-signed-variants" in group_commands["post-discord"]
    assert "run-gp-rune-verifier" in group_commands["post-discord"]
    assert "run-onion7-seed-pack" in group_commands["post-discord"]
    assert "validate" in group_commands["research-synthesis"]
    assert {"build", "validate", "summary"} <= group_commands["discord-full-review"]


def test_stage3x_help_commands_exit_zero() -> None:
    runner = CliRunner()

    for args in [
        ["--help"],
        ["consistency", "--help"],
        ["stego", "outguess-run", "--help"],
        ["post-discord", "run-cookie-signed-variants", "--help"],
        ["post-discord", "run-gp-rune-verifier", "--help"],
        ["post-discord", "run-onion7-seed-pack", "--help"],
        ["research-synthesis", "validate", "--help"],
        ["discord-full-review", "build", "--help"],
    ]:
        result = runner.invoke(app, args)
        assert result.exit_code == 0, result.output


def _command_name(command) -> str:
    return command.name or command.callback.__name__.replace("_", "-")
