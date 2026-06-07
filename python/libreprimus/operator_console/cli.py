"""Typer CLI for the Liber Primus Operator Console."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

from .app import run_operator_console
from .errors import GuiDependencyError
from .resources import ensure_default_configs
from .settings import CONTEXT_FILE, GUI_INSTALL_MESSAGE, INDEX_CACHE_PATH
from .source_browser.context_file import create_context_file_if_missing, context_file_status
from .source_browser.loaders import build_source_index, write_index_cache
from .source_browser.validators import (
    source_browser_summary,
    validate_manual_records,
    validate_source_index,
)

console = Console()
app = typer.Typer(no_args_is_help=True)


@app.command("run")
def run_command() -> None:
    """Run the local Operator Console GUI."""
    try:
        raise typer.Exit(run_operator_console())
    except GuiDependencyError:
        console.print(GUI_INSTALL_MESSAGE, markup=False)
        raise typer.Exit(1) from None


@app.command("build-source-index")
def build_source_index_command(
    out: Path = typer.Option(INDEX_CACHE_PATH),
) -> None:
    """Build the ignored Source Browser index cache."""
    ensure_default_configs()
    index = build_source_index()
    write_index_cache(out, index)
    console.print(f"records_scanned={len(index.scanned_paths)}")
    console.print(f"entries_loaded={len(index.entries)}")
    console.print(f"parse_error_count={len(index.parse_errors)}")
    console.print(f"index_cache={out.as_posix()}")


@app.command("validate-source-index")
def validate_source_index_command() -> None:
    """Validate Source Browser index loading and config."""
    result = validate_source_index()
    console.print(result.to_cli_text())
    console.print(f"operator_console_source_index_valid={str(result.ok).lower()}")
    if not result.ok:
        raise typer.Exit(1)


@app.command("validate-manual-entries")
def validate_manual_entries_command() -> None:
    """Validate manual entries, overrides, and tombstones."""
    result = validate_manual_records()
    console.print(result.to_cli_text())
    console.print(f"operator_console_manual_entries_valid={str(result.ok).lower()}")
    if not result.ok:
        raise typer.Exit(1)


@app.command("open-context")
def open_context_command(
    create_if_missing: bool = typer.Option(False, "--create-if-missing"),
) -> None:
    """Report the ChatGPT context-file status, optionally creating a template."""
    created = False
    if create_if_missing:
        created = create_context_file_if_missing(CONTEXT_FILE)
    status = context_file_status(CONTEXT_FILE)
    console.print(f"context_file_path={status['path']}")
    console.print(f"context_file_exists={str(status['exists']).lower()}")
    console.print(f"context_file_created={str(created).lower()}")
    console.print(f"huge_raw_blob_suspected={str(status['huge_raw_blob_suspected']).lower()}")


@app.command("summary")
def summary_command() -> None:
    """Print a compact Source Browser summary."""
    summary = source_browser_summary()
    for key, value in summary.items():
        if isinstance(value, list):
            console.print(f"{key}={','.join(value)}")
        elif isinstance(value, dict):
            console.print(f"{key}={json.dumps(value, sort_keys=True)}")
        else:
            console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="operator-console")
