"""CLI registration shim for Stage 5AP token-block commands."""

from __future__ import annotations

import typer

from libreprimus.token_block.cli import register as _register


def register(root_app: typer.Typer) -> None:
    _register(root_app)
