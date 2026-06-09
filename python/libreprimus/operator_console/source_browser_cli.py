"""Compatibility aliases for the Source Browser CLI."""

from __future__ import annotations

import typer
from rich.console import Console

from .app import run_operator_console
from .errors import GuiDependencyError
from .settings import GUI_INSTALL_MESSAGE
from .source_browser.validators import validate_number_fact_cards, validate_source_index

console = Console()
app = typer.Typer(no_args_is_help=True)


@app.command("run")
def run_command() -> None:
    try:
        raise typer.Exit(run_operator_console())
    except GuiDependencyError:
        console.print(GUI_INSTALL_MESSAGE, markup=False)
        raise typer.Exit(1) from None


@app.command("validate-index")
def validate_index_command() -> None:
    result = validate_source_index()
    console.print(result.to_cli_text())
    console.print(f"source_browser_index_valid={str(result.ok).lower()}")
    if not result.ok:
        raise typer.Exit(1)


@app.command("validate-number-facts")
def validate_number_facts_command() -> None:
    result = validate_number_fact_cards()
    console.print(result.to_cli_text())
    console.print(f"source_browser_number_facts_valid={str(result.ok).lower()}")
    if not result.ok:
        raise typer.Exit(1)


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="source-browser")
