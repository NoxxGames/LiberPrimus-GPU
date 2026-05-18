"""Command-line entrypoint for the LiberPrimus GPU workbench."""

from __future__ import annotations

from libreprimus.consistency.runner import run_consistency_suite
from libreprimus.cli_commands.root import app

__all__ = ["app", "run_consistency_suite"]


if __name__ == "__main__":
    app()
