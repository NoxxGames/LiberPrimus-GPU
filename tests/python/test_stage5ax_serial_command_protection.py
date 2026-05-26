from __future__ import annotations

from libreprimus.parallel_validation.models import PARALLEL_SAFE_CLASSES
from libreprimus.parallel_validation.plan import default_commands


def test_serial_final_and_blocked_commands_are_not_parallel_safe() -> None:
    protected = [
        command
        for command in default_commands()
        if command.parallel_class.startswith("serial_") or command.parallel_class == "blocked"
    ]
    assert protected
    for command in protected:
        assert command.requires_serial
        assert command.parallel_class not in PARALLEL_SAFE_CLASSES
