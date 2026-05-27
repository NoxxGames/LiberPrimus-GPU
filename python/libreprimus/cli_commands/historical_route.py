"""CLI registration shim for Stage 5BF historical route commands."""

from __future__ import annotations

import typer

from libreprimus.historical_route.cli import register as _register


def register(root_app: typer.Typer) -> None:
    _register(root_app)
