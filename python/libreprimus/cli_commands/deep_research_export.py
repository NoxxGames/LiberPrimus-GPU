"""CLI registration shim for Stage 5AN Deep Research export commands."""

from __future__ import annotations

import typer

from libreprimus.deep_research_export.cli import register as _register


def register(root_app: typer.Typer) -> None:
    _register(root_app)
