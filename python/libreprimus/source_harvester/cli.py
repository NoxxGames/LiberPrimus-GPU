"""Typer CLI for Stage 5AF Cicada source harvester."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .bundles import build_bundle_scaffolds
from .export import write_json, write_jsonl
from .extractors import extract_html_file
from .fetcher import fetch_source
from .hashing import inventory_archive, write_hash_path
from .manifest import validate_manifest
from .models import (
    CLUE_TARGET_CATEGORIES_PATH,
    COLLECTION_PRIORITIES_PATH,
    DRY_RUN_SUMMARY_PATH,
    FAILURES_REPORT,
    HARVEST_PLAN_REPORT,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    RESEARCH_BUNDLE_PLAN_PATH,
    SOURCE_MANIFEST_PATH,
    SUMMARY_PATH,
    TOOL_POLICY_PATH,
)
from .planning import build_plan
from .summary import summarize_stage5af
from .validation import validate_stage5af

console = Console()
app = typer.Typer(help="Stage 5AF Cicada source-harvester commands.", no_args_is_help=True)


@app.command("validate-manifest")
def validate_manifest_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    summary, errors = validate_manifest(manifest, out_dir=out_dir)
    console.print(f"source_manifest_records={summary['source_manifest_records']}")
    console.print(f"required_source_ids_present={str(summary['required_source_ids_present']).lower()}")
    console.print(f"validation_error_count={len(errors)}")
    if errors:
        raise typer.Exit(1)


@app.command("plan")
def plan_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    out: Path = typer.Option(OUTPUT_DIR / HARVEST_PLAN_REPORT),
    dry_run_summary_out: Path = typer.Option(DRY_RUN_SUMMARY_PATH),
    out_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    records, summary = build_plan(
        manifest_path=manifest,
        out_path=out,
        dry_run_summary_out=dry_run_summary_out,
        out_dir=out_dir,
    )
    console.print(f"dry_run_plan_records={len(records)}")
    console.print(f"network_fetch_performed={str(summary['network_fetch_performed']).lower()}")


@app.command("fetch")
def fetch_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    source_id: str = typer.Option(...),
    out_root: Path | None = typer.Option(None),
    allow_network: bool = typer.Option(False),
    allow_downloads: bool = typer.Option(False),
    rate_limit_seconds: float = typer.Option(3.0),
) -> None:
    if out_root is None:
        raise typer.BadParameter("fetch requires --out-root")
    try:
        metadata = fetch_source(
            manifest_path=manifest,
            source_id=source_id,
            out_root=out_root,
            allow_network=allow_network,
            allow_downloads=allow_downloads,
            rate_limit_seconds=rate_limit_seconds,
        )
    except Exception as exc:
        write_jsonl(OUTPUT_DIR / FAILURES_REPORT, [{"source_id": source_id, "error": str(exc)}])
        raise typer.BadParameter(str(exc)) from exc
    console.print(f"fetched_source_id={metadata['source_id']}")
    console.print(f"sha256={metadata['sha256']}")


@app.command("extract")
def extract_command(
    input_path: Path = typer.Option(..., "--input"),
    out: Path = typer.Option(...),
    source_id: str | None = typer.Option(None),
) -> None:
    record = extract_html_file(input_path, source_id=source_id, out=out)
    console.print(f"link_count={len(record['links'])}")
    console.print(f"image_link_count={len(record['image_links'])}")


@app.command("inventory")
def inventory_command(
    path: Path = typer.Option(...),
    out: Path = typer.Option(...),
    source_id: str | None = typer.Option(None),
) -> None:
    records = write_hash_path(path, out=out, source_id=source_id)
    console.print(f"inventory_records={len(records)}")


@app.command("hash-path")
def hash_path_command(
    path: Path = typer.Option(...),
    out: Path = typer.Option(...),
    source_id: str | None = typer.Option(None),
) -> None:
    records = write_hash_path(path, out=out, source_id=source_id)
    console.print(f"hash_records={len(records)}")


@app.command("inventory-archive")
def inventory_archive_command(
    source_id: str = typer.Option(...),
    path: Path = typer.Option(...),
    out_root: Path | None = typer.Option(None),
    out: Path | None = typer.Option(None),
) -> None:
    if out is None:
        if out_root is None:
            raise typer.BadParameter("inventory-archive requires --out or --out-root")
        out = out_root / f"{source_id}-archive-inventory.jsonl"
    records = inventory_archive(path=path, source_id=source_id, out=out)
    console.print(f"archive_inventory_records={len(records)}")


@app.command("build-bundles")
def build_bundles_command(
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    out_root: Path = typer.Option(OUTPUT_DIR / "research_bundles_preview"),
) -> None:
    records = build_bundle_scaffolds(bundle_plan_path=bundle_plan, out_root=out_root)
    console.print(f"bundle_scaffolds={len(records)}")
    console.print("do_not_assume_generated=true")
    console.print("known_questions_generated=true")


@app.command("summarize")
def summarize_command(
    manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    collection_priorities: Path = typer.Option(COLLECTION_PRIORITIES_PATH),
    clue_target_categories: Path = typer.Option(CLUE_TARGET_CATEGORIES_PATH),
    bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    tool_policy: Path = typer.Option(TOOL_POLICY_PATH),
    dry_run_summary: Path = typer.Option(DRY_RUN_SUMMARY_PATH),
    next_stage_decision_out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary_out: Path = typer.Option(SUMMARY_PATH),
    out: Path = typer.Option(OUTPUT_DIR / "summary.json"),
) -> None:
    summary = summarize_stage5af(
        source_manifest_path=manifest,
        collection_priorities_path=collection_priorities,
        clue_target_categories_path=clue_target_categories,
        research_bundle_plan_path=bundle_plan,
        tool_policy_path=tool_policy,
        dry_run_summary_path=dry_run_summary,
        next_stage_decision_out=next_stage_decision_out,
        summary_out=summary_out,
        out_dir=out.parent,
    )
    write_json(out, summary)
    write_jsonl(out.parent / FAILURES_REPORT, [])
    console.print(f"source_manifest_records={summary['source_manifest_records']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")


@app.command("validate-stage5af")
def validate_stage5af_command(
    source_manifest: Path = typer.Option(SOURCE_MANIFEST_PATH),
    collection_priorities: Path = typer.Option(COLLECTION_PRIORITIES_PATH),
    clue_target_categories: Path = typer.Option(CLUE_TARGET_CATEGORIES_PATH),
    research_bundle_plan: Path = typer.Option(RESEARCH_BUNDLE_PLAN_PATH),
    tool_policy: Path = typer.Option(TOOL_POLICY_PATH),
    dry_run_summary: Path = typer.Option(DRY_RUN_SUMMARY_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(OUTPUT_DIR),
) -> None:
    counts, errors = validate_stage5af(
        source_manifest_path=source_manifest,
        collection_priorities_path=collection_priorities,
        clue_target_categories_path=clue_target_categories,
        research_bundle_plan_path=research_bundle_plan,
        tool_policy_path=tool_policy,
        dry_run_summary_path=dry_run_summary,
        next_stage_decision_path=next_stage_decision,
        summary_path=summary,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("source_harvester_stage5af_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from .export import read_yaml

    payload = read_yaml(summary)
    for key in (
        "source_manifest_records",
        "clue_target_category_records",
        "research_bundle_plan_records",
        "network_fetch_performed",
        "raw_downloads_committed",
        "recommended_next_stage_title",
    ):
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="source-harvester")
