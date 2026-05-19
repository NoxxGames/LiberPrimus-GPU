"""Stage 4M image preflight CLI commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.image_preflight.export import build_image_preflight
from libreprimus.image_preflight.models import (
    DEFAULT_ARTIFACT_CANDIDATES_OUT,
    DEFAULT_BIGRAM_IMAGE,
    DEFAULT_BIGRAM_READINESS_OUT,
    DEFAULT_COMPRESSION_OBSERVATIONS,
    DEFAULT_COMPRESSION_OUT,
    DEFAULT_IMAGE_ARTIFACTS,
    DEFAULT_IMAGE_DIR,
    DEFAULT_IMAGE_LOCKS,
    DEFAULT_MANIFEST_READINESS,
    DEFAULT_OUT_DIR,
    DEFAULT_PROMOTION_READINESS,
    DEFAULT_SOURCE_DELTA,
    DEFAULT_SOURCE_VARIANT_OUT,
    DEFAULT_SUMMARY_OUT,
)
from libreprimus.image_preflight.summary import load_summary
from libreprimus.image_preflight.validation import validate_image_preflight_records
from libreprimus.paths import repo_root

image_preflight_app = typer.Typer(no_args_is_help=True)
console = Console()


@image_preflight_app.command("build")
def image_preflight_build(
    image_dir: Path = typer.Option(DEFAULT_IMAGE_DIR, "--image-dir", help="Local ignored LP page-image directory."),
    image_artifacts: Path = typer.Option(
        DEFAULT_IMAGE_ARTIFACTS,
        "--image-artifacts",
        help="Committed LP page image artifact JSONL records.",
    ),
    image_locks: Path = typer.Option(
        DEFAULT_IMAGE_LOCKS,
        "--image-locks",
        help="Committed LP page image lock JSONL records.",
    ),
    source_delta: Path = typer.Option(DEFAULT_SOURCE_DELTA, "--source-delta", help="Committed source-delta YAML."),
    compression_observations: Path = typer.Option(
        DEFAULT_COMPRESSION_OBSERVATIONS,
        "--compression-observations",
        help="Committed image compression observation YAML.",
    ),
    promotion_readiness: Path = typer.Option(
        DEFAULT_PROMOTION_READINESS,
        "--promotion-readiness",
        help="Stage 4L promotion readiness YAML.",
    ),
    manifest_readiness: Path = typer.Option(
        DEFAULT_MANIFEST_READINESS,
        "--manifest-readiness",
        help="Stage 4L manifest readiness YAML.",
    ),
    bigram_image: Path = typer.Option(DEFAULT_BIGRAM_IMAGE, "--bigram-image", help="Local ignored bigram screenshot."),
    out_dir: Path = typer.Option(DEFAULT_OUT_DIR, "--out-dir", help="Generated image preflight output directory."),
    source_variant_out: Path = typer.Option(
        DEFAULT_SOURCE_VARIANT_OUT,
        "--source-variant-out",
        help="Committed source-variant preflight records YAML.",
    ),
    compression_out: Path = typer.Option(
        DEFAULT_COMPRESSION_OUT,
        "--compression-out",
        help="Committed compression metric records YAML.",
    ),
    artifact_candidates_out: Path = typer.Option(
        DEFAULT_ARTIFACT_CANDIDATES_OUT,
        "--artifact-candidates-out",
        help="Committed artifact review candidate records YAML.",
    ),
    summary_out: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary-out", help="Committed image preflight summary YAML."),
    bigram_readiness_out: Path = typer.Option(
        DEFAULT_BIGRAM_READINESS_OUT,
        "--bigram-readiness-out",
        help="Committed bigram readiness YAML.",
    ),
    allow_missing_bigram_image: bool = typer.Option(
        False,
        "--allow-missing-bigram-image",
        help="Permit metadata build when the local screenshot is absent.",
    ),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Record warnings without failing build."),
) -> None:
    """Build Stage 4M image source-variant and compression preflight records."""

    try:
        summary = build_image_preflight(
            image_dir=_resolve(image_dir),
            image_artifacts=_resolve(image_artifacts),
            image_locks=_resolve(image_locks),
            source_delta=_resolve(source_delta),
            compression_observations=_resolve(compression_observations),
            promotion_readiness=_resolve(promotion_readiness),
            manifest_readiness=_resolve(manifest_readiness),
            bigram_image=_resolve(bigram_image),
            out_dir=_resolve(out_dir),
            source_variant_out=_resolve(source_variant_out),
            compression_out=_resolve(compression_out),
            artifact_candidates_out=_resolve(artifact_candidates_out),
            summary_out=_resolve(summary_out),
            bigram_readiness_out=_resolve(bigram_readiness_out),
            allow_missing_bigram_image=allow_missing_bigram_image,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI should surface deterministic failures.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_summary(summary)


@image_preflight_app.command("validate")
def image_preflight_validate(
    source_variant: Path = typer.Option(
        DEFAULT_SOURCE_VARIANT_OUT,
        "--source-variant",
        help="Source-variant preflight YAML.",
    ),
    compression: Path = typer.Option(DEFAULT_COMPRESSION_OUT, "--compression", help="Compression preflight YAML."),
    artifact_candidates: Path = typer.Option(
        DEFAULT_ARTIFACT_CANDIDATES_OUT,
        "--artifact-candidates",
        help="Artifact candidate YAML.",
    ),
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Image preflight summary YAML."),
    bigram_readiness: Path = typer.Option(
        DEFAULT_BIGRAM_READINESS_OUT,
        "--bigram-readiness",
        help="Bigram readiness YAML.",
    ),
) -> None:
    """Validate committed Stage 4M image preflight records."""

    counts, errors = validate_image_preflight_records(
        source_variant=_resolve(source_variant),
        compression=_resolve(compression),
        artifact_candidates=_resolve(artifact_candidates),
        summary=_resolve(summary),
        bigram_readiness=_resolve(bigram_readiness),
    )
    for key, value in counts.items():
        console.print(f"{key}_count={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("image_preflight_valid=true")


@image_preflight_app.command("summary")
def image_preflight_summary(
    summary: Path = typer.Option(DEFAULT_SUMMARY_OUT, "--summary", help="Image preflight summary YAML."),
    bigram_readiness: Path = typer.Option(
        DEFAULT_BIGRAM_READINESS_OUT,
        "--bigram-readiness",
        help="Bigram readiness YAML.",
    ),
) -> None:
    """Print the committed Stage 4M image preflight summary."""

    del bigram_readiness
    _print_summary(load_summary(_resolve(summary)))


def _print_summary(summary: dict) -> None:
    for key, value in summary.items():
        if isinstance(value, dict):
            continue
        if isinstance(value, list):
            console.print(f"{key}={','.join(str(item) for item in value)}")
            continue
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def register(root_app: typer.Typer) -> None:
    """Register image-preflight commands on the public root app."""

    root_app.add_typer(image_preflight_app, name="image-preflight")
