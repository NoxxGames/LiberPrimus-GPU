"""Transform registry CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

transform_registry_app = typer.Typer(no_args_is_help=True)


@transform_registry_app.command("summary")
def transform_registry_summary(
    registry: Path = typer.Option(DEFAULT_TRANSFORM_REGISTRY, "--registry", help="CPU transform registry JSON path."),
) -> None:
    """Print a concise transform registry summary."""
    loaded = load_registry(_resolve_existing_path(registry, "Transform registry"))
    alias_count = sum(1 for definition in loaded.transforms if definition.alias_of)
    console.print(f"registry_id={loaded.registry_id}")
    console.print(f"registry_sha256={loaded.sha256}")
    console.print(f"transform_count={len(loaded.transforms)}")
    console.print(f"alias_count={alias_count}")
    console.print(f"search_enabled={str(loaded.search_enabled).lower()}")
    console.print(f"cuda_enabled={str(loaded.cuda_enabled).lower()}")
    console.print(f"scoring_enabled={str(loaded.scoring_enabled).lower()}")


@transform_registry_app.command("validate")
def transform_registry_validate(
    registry: Path = typer.Option(DEFAULT_TRANSFORM_REGISTRY, "--registry", help="CPU transform registry JSON path."),
) -> None:
    """Validate CPU transform registry metadata and implementation links."""
    errors = validate_registry_file(_resolve_existing_path(registry, "Transform registry"))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Transform registry validation OK")


@transform_registry_app.command("list")
def transform_registry_list(
    registry: Path = typer.Option(DEFAULT_TRANSFORM_REGISTRY, "--registry", help="CPU transform registry JSON path."),
) -> None:
    """List registered CPU reference transforms."""
    loaded = load_registry(_resolve_existing_path(registry, "Transform registry"))
    table = Table("Transform", "Method", "Alias Of", "Search", "CUDA", "Scoring")
    for definition in loaded.transforms:
        table.add_row(
            definition.transform_id,
            definition.method_family,
            definition.alias_of or "",
            str(definition.search_enabled).lower(),
            str(definition.supports_gpu).lower(),
            str(definition.scoring_enabled).lower(),
        )
    console.print(table)


@transform_registry_app.command("resolve")
def transform_registry_resolve(
    registry: Path = typer.Option(DEFAULT_TRANSFORM_REGISTRY, "--registry", help="CPU transform registry JSON path."),
    transform_id: str = typer.Option(..., "--transform-id", help="Transform ID or alias ID to resolve."),
) -> None:
    """Resolve a transform alias to its canonical transform."""
    loaded = load_registry(_resolve_existing_path(registry, "Transform registry"))
    try:
        definition = resolve_transform(loaded, transform_id)
    except KeyError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(2) from error
    console.print(f"transform_id={transform_id}")
    console.print(f"canonical_transform_id={definition.transform_id}")
    console.print(f"transform_version={definition.transform_version}")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(transform_registry_app, name="transform-registry")
