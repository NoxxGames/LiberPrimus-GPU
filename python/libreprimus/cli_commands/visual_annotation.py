"""Stage 4C visual annotation CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.paths import repo_root
from libreprimus.visual_annotation.export import run_visual_annotation_build
from libreprimus.visual_annotation.models import (
    DEFAULT_CUNEIFORM,
    DEFAULT_DELIMITER,
    DEFAULT_DOT,
    DEFAULT_IMAGE_ARTIFACTS,
    DEFAULT_IMAGE_DIR,
    DEFAULT_IMAGE_LOCKS,
    DEFAULT_NEGATIVE,
    DEFAULT_NEGATIVE_CONTROLS,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SUMMARY,
    DEFAULT_TASKS,
    DEFAULT_VISUAL_OBSERVATIONS,
)
from libreprimus.visual_annotation.summary import summarize_visual_annotation
from libreprimus.visual_annotation.validation import validate_visual_annotation_records

visual_annotation_app = typer.Typer(no_args_is_help=True)
console = Console()


@visual_annotation_app.command("build")
def visual_annotation_build(
    visual_observations: Path = typer.Option(
        DEFAULT_VISUAL_OBSERVATIONS, "--visual-observations", help="Stage 4B visual observations."
    ),
    negative_controls: Path = typer.Option(
        DEFAULT_NEGATIVE_CONTROLS, "--negative-controls", help="Stage 4B negative controls."
    ),
    image_artifacts: Path = typer.Option(
        DEFAULT_IMAGE_ARTIFACTS, "--image-artifacts", help="LP page image artifact JSONL."
    ),
    image_locks: Path = typer.Option(
        DEFAULT_IMAGE_LOCKS, "--image-locks", help="LP page image lock JSONL."
    ),
    image_dir: Path = typer.Option(DEFAULT_IMAGE_DIR, "--image-dir", help="Local ignored LP page image directory."),
    out_dir: Path = typer.Option(
        DEFAULT_OUTPUT_DIR, "--out-dir", help="Generated Stage 4C annotation output directory."
    ),
    task_out: Path = typer.Option(DEFAULT_TASKS, "--task-out", help="Committed annotation tasks YAML."),
    cuneiform_out: Path = typer.Option(
        DEFAULT_CUNEIFORM, "--cuneiform-out", help="Committed cuneiform candidates YAML."
    ),
    dot_out: Path = typer.Option(DEFAULT_DOT, "--dot-out", help="Committed dot annotation tasks YAML."),
    delimiter_out: Path = typer.Option(
        DEFAULT_DELIMITER, "--delimiter-out", help="Committed delimiter annotation tasks YAML."
    ),
    negative_out: Path = typer.Option(
        DEFAULT_NEGATIVE, "--negative-out", help="Committed visual negative-control tasks YAML."
    ),
    summary_out: Path = typer.Option(DEFAULT_SUMMARY, "--summary-out", help="Committed pack summary YAML."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Allow reduced coverage warnings."),
) -> None:
    """Build Stage 4C visual annotation tasks and generated local review site."""

    try:
        result = run_visual_annotation_build(
            visual_observations=_resolve(visual_observations),
            negative_controls=_resolve(negative_controls),
            image_artifacts=_resolve(image_artifacts),
            image_locks=_resolve(image_locks),
            image_dir=_resolve(image_dir),
            out_dir=_resolve(out_dir),
            task_out=_resolve(task_out),
            cuneiform_out=_resolve(cuneiform_out),
            dot_out=_resolve(dot_out),
            delimiter_out=_resolve(delimiter_out),
            negative_out=_resolve(negative_out),
            summary_out=_resolve(summary_out),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI surfaces deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_mapping(result)


@visual_annotation_app.command("validate")
def visual_annotation_validate(
    task: Path = typer.Option(DEFAULT_TASKS, "--task", help="Committed annotation tasks YAML."),
    cuneiform: Path = typer.Option(DEFAULT_CUNEIFORM, "--cuneiform", help="Cuneiform candidates YAML."),
    dot: Path = typer.Option(DEFAULT_DOT, "--dot", help="Dot-pattern tasks YAML."),
    delimiter: Path = typer.Option(DEFAULT_DELIMITER, "--delimiter", help="Delimiter tasks YAML."),
    negative: Path = typer.Option(DEFAULT_NEGATIVE, "--negative", help="Visual negative controls YAML."),
    summary: Path = typer.Option(DEFAULT_SUMMARY, "--summary", help="Annotation pack summary YAML."),
) -> None:
    """Validate committed Stage 4C visual annotation records."""

    counts, errors = validate_visual_annotation_records(
        task=_resolve(task),
        cuneiform=_resolve(cuneiform),
        dot=_resolve(dot),
        delimiter=_resolve(delimiter),
        negative=_resolve(negative),
        summary=_resolve(summary),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("visual_annotation_valid=true")


@visual_annotation_app.command("summary")
def visual_annotation_summary(
    summary: Path = typer.Option(DEFAULT_SUMMARY, "--summary", help="Annotation pack summary YAML."),
) -> None:
    """Print a concise Stage 4C visual annotation summary."""

    _print_mapping(summarize_visual_annotation(_resolve(summary)))


def _print_mapping(payload: dict) -> None:
    for key, value in payload.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                console.print(f"{inner_key}={inner_value}")
        elif isinstance(value, list):
            console.print(f"{key}={','.join(str(item) for item in value)}")
        else:
            console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register this module's Typer app on the public root app."""

    root_app.add_typer(visual_annotation_app, name="visual-annotation")
