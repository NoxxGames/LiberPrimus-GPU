"""Reference source CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

reference_source_app = typer.Typer(no_args_is_help=True)


@reference_source_app.command("extract-stage1c")
def reference_source_extract_stage1c(
    out_dir: Path = typer.Option(DEFAULT_REFERENCE_SUMMARY_DIR, "--out-dir", help="Generated reference summary directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite partial reference notes."),
) -> None:
    """Extract small Stage 1C reference-source summaries from mirrored raw files."""
    output_dir = _resolve_output_path(out_dir)
    payload = build_stage1c_reference_summary()
    paths = write_stage1c_reference_outputs(output_dir, payload)
    for name, path in paths.items():
        console.print(f"{name}={path}")
    summary = payload["summary"]
    console.print(f"scream314_method_note_count={summary['scream314_method_note_count']}")
    console.print(f"lipeeeee_tooling_note_count={summary['lipeeeee_tooling_note_count']}")
    console.print(f"divinity_found={str(summary['divinity_found']).lower()}")
    console.print(f"firfumferenfe_found={str(summary['firfumferenfe_found']).lower()}")
    console.print(f"cleartext_f_skip_note_found={str(summary['cleartext_f_skip_note_found']).lower()}")
    console.print(f"imported_as_dependency={str(summary['imported_as_dependency']).lower()}")
    console.print(f"code_copied={str(summary['code_copied']).lower()}")
    if not allow_warnings and not summary["scream314_method_note_count"]:
        raise typer.Exit(1)


@reference_source_app.command("summary")
def reference_source_summary(
    out_dir: Path = typer.Option(DEFAULT_REFERENCE_SUMMARY_DIR, "--out-dir", help="Generated reference summary directory."),
) -> None:
    """Print generated Stage 1C reference-source summary."""
    summary_path = _resolve_output_path(out_dir) / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    for key in [
        "scream314_method_note_count",
        "lipeeeee_tooling_note_count",
        "divinity_found",
        "firfumferenfe_found",
        "cleartext_f_skip_note_found",
        "reference_only",
        "imported_as_dependency",
        "code_copied",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(reference_source_app, name="reference-source")
