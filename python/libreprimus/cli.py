"""Command-line interface for Stage 0A smoke validation."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from libreprimus.paths import package_root, repo_root
from libreprimus.toolchain import ToolStatus, collect_toolchain

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def smoke() -> None:
    """Print the Stage 0A Python smoke message."""
    console.print("LiberPrimus Python Stage 0A smoke OK")


@app.command()
def paths() -> None:
    """Print important project paths."""
    table = Table("Name", "Path")
    table.add_row("repo_root", str(repo_root()))
    table.add_row("package_root", str(package_root()))
    console.print(table)


@app.command()
def toolchain() -> None:
    """Print a concise toolchain report."""
    table = Table("Tool", "Present", "Path", "Version")
    report = collect_toolchain()
    for name, status in report.items():
        if isinstance(status, ToolStatus):
            table.add_row(name, str(status.present).lower(), status.path or "", status.version or "")
        else:
            table.add_row(name, "true" if status else "false", status or "", "")
    console.print(table)


if __name__ == "__main__":
    app()
