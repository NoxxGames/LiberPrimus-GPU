"""Result store CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *
from libreprimus.cli_commands.solved_baselines import stage2a_smoke

result_store_app = typer.Typer(no_args_is_help=True)


@result_store_app.command("validate-manifest")
def result_store_validate_manifest(
    manifest: Path = typer.Option(DEFAULT_RESULT_STORE_MANIFEST, "--manifest", help="Result-store manifest path."),
) -> None:
    """Validate a result-store manifest."""
    errors = validate_result_store_manifest_file(_resolve_existing_path(manifest, "Result-store manifest"))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Result-store manifest validation OK")


@result_store_app.command("import-solved-baseline")
def result_store_import_solved_baseline(
    manifest: Path = typer.Option(DEFAULT_RESULT_STORE_MANIFEST, "--manifest", help="Result-store manifest path."),
    solved_baseline_results: Path = typer.Option(
        DEFAULT_STAGE2A_RESULTS_DIR,
        "--solved-baseline-results",
        help="Generated Stage 2A solved-baseline results directory.",
    ),
    out_dir: Path = typer.Option(DEFAULT_STAGE2B_RESULT_STORE_DIR, "--out-dir", help="Generated result-store directory."),
    replace: bool = typer.Option(False, "--replace", help="Replace duplicate run_id rows in SQLite."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite imported warnings."),
) -> None:
    """Import solved-baseline manifest-run outputs into JSONL and SQLite result stores."""
    try:
        result = import_solved_baseline(
            _resolve_existing_path(manifest, "Result-store manifest"),
            solved_baseline_results=_resolve_output_path(solved_baseline_results),
            out_dir=_resolve_output_path(out_dir),
            replace=replace,
        )
    except (FileNotFoundError, ValueError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    paths = result["paths"]
    summary = result["summary"]
    run_record = result["run_records"][0]
    for name, path in paths.items():
        console.print(f"{name}={path}")
    console.print(f"run_id={run_record.run_id}")
    console.print(f"manifest_id={run_record.manifest_id}")
    console.print(f"manifest_sha256={run_record.manifest_sha256}")
    console.print(f"registry_sha256={run_record.registry_sha256}")
    console.print(f"run_count={summary.run_count}")
    console.print(f"fixture_total={run_record.fixture_counts['total']}")
    console.print(f"fixture_pass={run_record.fixture_counts['pass']}")
    console.print(f"fixture_fail={run_record.fixture_counts['fail']}")
    console.print(f"fixture_pending={run_record.fixture_counts['pending']}")
    console.print(f"fixture_skipped={run_record.fixture_counts['skipped']}")
    console.print(f"artifact_count={summary.generated_artifact_count}")
    console.print(f"search_performed_any={str(summary.search_performed_any).lower()}")
    console.print(f"cuda_used_any={str(summary.cuda_used_any).lower()}")
    console.print(f"scoring_used_any={str(summary.scoring_used_any).lower()}")
    if summary.warnings and not allow_warnings:
        raise typer.Exit(1)


@result_store_app.command("validate")
def result_store_validate(
    results_dir: Path = typer.Option(DEFAULT_STAGE2B_RESULT_STORE_DIR, "--results-dir", help="Generated result-store directory."),
    sqlite: Path = typer.Option(DEFAULT_STAGE2B_SQLITE, "--sqlite", help="Generated SQLite result-store path."),
) -> None:
    """Validate JSONL and SQLite result-store outputs."""
    errors = validate_result_store(_resolve_output_path(results_dir), _resolve_output_path(sqlite))
    if errors:
        for error in errors:
            console.print(f"[red]{error}[/red]")
        raise typer.Exit(1)
    console.print("Result-store validation OK")


@result_store_app.command("summary")
def result_store_summary(
    results_dir: Path = typer.Option(DEFAULT_STAGE2B_RESULT_STORE_DIR, "--results-dir", help="Generated result-store directory."),
) -> None:
    """Print generated result-store summary counts."""
    resolved = _resolve_output_path(results_dir)
    summary = load_result_store_summary(resolved)
    for key in [
        "summary_id",
        "run_count",
        "pass_count",
        "fail_count",
        "partial_count",
        "pending_count",
        "skipped_count",
        "error_count",
        "canonical_corpus_active_any",
        "search_performed_any",
        "scoring_used_any",
        "cuda_used_any",
        "generated_artifact_count",
        "jsonl_path",
        "sqlite_database_path",
    ]:
        value = summary.get(key)
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    sqlite_path = resolved / "results.sqlite3"
    if sqlite_path.is_file():
        counts = table_counts(sqlite_path)
        console.print(f"sqlite_run_count={counts.get('runs')}")
        console.print(f"sqlite_event_count={counts.get('events')}")
        console.print(f"sqlite_artifact_count={counts.get('artifacts')}")
    run_records_path = resolved / "run_records.jsonl"
    if run_records_path.is_file():
        first_record = json.loads(run_records_path.read_text(encoding="utf-8").splitlines()[0])
        fixture_counts = first_record.get("fixture_counts", {})
        console.print(f"fixture_total={fixture_counts.get('total')}")
        console.print(f"fixture_pass={fixture_counts.get('pass')}")
        console.print(f"fixture_fail={fixture_counts.get('fail')}")
        console.print(f"fixture_pending={fixture_counts.get('pending')}")
        console.print(f"fixture_skipped={fixture_counts.get('skipped')}")


@result_store_app.command("stage2b-smoke")
def stage2b_smoke(
    solved_baseline_manifest: Path = typer.Option(
        DEFAULT_SOLVED_BASELINE_MANIFEST,
        "--solved-baseline-manifest",
        help="Stage 2A solved-baseline manifest.",
    ),
    result_store_manifest: Path = typer.Option(
        DEFAULT_RESULT_STORE_MANIFEST,
        "--result-store-manifest",
        help="Stage 2B result-store import manifest.",
    ),
    solved_baseline_out_dir: Path = typer.Option(
        DEFAULT_STAGE2A_RESULTS_DIR,
        "--solved-baseline-out-dir",
        help="Generated Stage 2A solved-baseline output directory.",
    ),
    result_store_out_dir: Path = typer.Option(
        DEFAULT_STAGE2B_RESULT_STORE_DIR,
        "--result-store-out-dir",
        help="Generated Stage 2B result-store output directory.",
    ),
    replace: bool = typer.Option(False, "--replace", help="Replace duplicate run_id rows in SQLite."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite warnings."),
) -> None:
    """Run Stage 2B solved-baseline result-store import smoke."""
    solved_baseline_dir = _resolve_output_path(solved_baseline_out_dir)
    if not (solved_baseline_dir / "summary.json").is_file() or not (
        solved_baseline_dir / "manifest_run_records.jsonl"
    ).is_file():
        stage2a_smoke(
            manifest=solved_baseline_manifest,
            candidate_dir=None,
            out_dir=solved_baseline_out_dir,
            allow_warnings=allow_warnings,
        )
    result_store_validate_manifest(manifest=result_store_manifest)
    result_store_import_solved_baseline(
        manifest=result_store_manifest,
        solved_baseline_results=solved_baseline_out_dir,
        out_dir=result_store_out_dir,
        replace=replace,
        allow_warnings=allow_warnings,
    )
    result_store_validate(
        results_dir=result_store_out_dir,
        sqlite=_resolve_output_path(result_store_out_dir) / "results.sqlite3",
    )
    result_store_summary(results_dir=result_store_out_dir)
    console.print("Stage 2B smoke OK")




def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(result_store_app, name="result-store")
