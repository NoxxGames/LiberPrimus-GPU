from __future__ import annotations

from libreprimus.parallel_validation.models import PARALLEL_SAFE_CLASSES
from libreprimus.parallel_validation.plan import default_commands
from libreprimus.parallel_validation.validation import validate_registry


def test_registry_commands_are_classified_and_valid() -> None:
    commands = default_commands()
    registry = {
        "commands": [command.to_record() for command in commands],
        "parallel_safe_command_count": sum(command.parallel_safe for command in commands),
        "serial_command_count": sum(command.parallel_class.startswith("serial_") for command in commands),
        "blocked_command_count": sum(command.parallel_class == "blocked" for command in commands),
    }
    assert validate_registry(registry) == []
    assert registry["parallel_safe_command_count"] >= 10


def test_mutating_and_remote_commands_are_serial_only() -> None:
    for command in default_commands():
        if command.uses_git_mutation or command.uses_github_mutation or command.uses_network:
            assert command.requires_serial
            assert command.parallel_class not in PARALLEL_SAFE_CLASSES
