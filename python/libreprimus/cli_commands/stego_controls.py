"""CLI registration shim for Stage 5AP stego-control commands."""

from __future__ import annotations

import typer

from libreprimus.stego_controls.cli import register as _register


def register(root_app: typer.Typer) -> None:
    _register(root_app)
