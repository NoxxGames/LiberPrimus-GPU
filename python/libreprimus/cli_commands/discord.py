"""Discord archive/review/promotion CLI commands."""
# ruff: noqa: F403,F405

from __future__ import annotations

import typer

from libreprimus.cli_commands.common import *

discord_ingest_app = typer.Typer(no_args_is_help=True)
discord_promote_app = typer.Typer(no_args_is_help=True)
discord_review_app = typer.Typer(no_args_is_help=True)
discord_leads_app = typer.Typer(no_args_is_help=True)


@discord_ingest_app.command("scan")
def discord_ingest_scan(
    source_dir: Path = typer.Option(..., "--source-dir", help="Local Discord HTML archive directory."),
    out_dir: Path = typer.Option(..., "--out-dir", help="Generated Discord ingestion output directory."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Write empty outputs if source dir is missing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite non-blocking warnings."),
) -> None:
    """Scan admin-provided local Discord HTML logs without committing raw content."""
    try:
        summary = scan_discord_archive(
            source_dir=_resolve_output_path(source_dir),
            out_dir=_resolve_output_path(out_dir),
            allow_missing=allow_missing,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_discord_ingestion_summary(summary)


@discord_ingest_app.command("validate-results")
def discord_ingest_validate_results(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated Discord ingestion result directory."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Allow missing generated results."),
) -> None:
    """Validate generated Discord ingestion records."""
    try:
        counts, errors = validate_discord_ingestion_results(
            _resolve_output_path(results_dir),
            allow_missing=allow_missing,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Discord ingestion results OK")


@discord_ingest_app.command("summary")
def discord_ingest_print_summary(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated Discord ingestion result directory."),
) -> None:
    """Print a concise generated Discord ingestion summary."""
    try:
        summary = load_discord_ingestion_summary(_resolve_output_path(results_dir))
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_discord_ingestion_summary(summary)


@discord_ingest_app.command("export-aggregate")
def discord_ingest_export_aggregate(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated Discord ingestion result directory."),
    archive_out: Path = typer.Option(..., "--archive-out", help="Committed aggregate archive record path."),
    observation_out: Path = typer.Option(..., "--observation-out", help="Committed aggregate observation summary path."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Allow missing generated results."),
) -> None:
    """Export aggregate-only committed records from generated Discord ingestion results."""
    try:
        archive_record, observation_record = export_discord_aggregate_records(
            results_dir=_resolve_output_path(results_dir),
            archive_out=_resolve_output_path(archive_out),
            observation_out=_resolve_output_path(observation_out),
            allow_missing=allow_missing,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"archive_id={archive_record.get('archive_id')}")
    console.print(f"html_file_count={observation_record.get('html_file_count', 0)}")
    console.print(f"link_count={observation_record.get('link_count', 0)}")
    console.print(f"archive_out={_resolve_output_path(archive_out)}")
    console.print(f"observation_out={_resolve_output_path(observation_out)}")


def _print_discord_ingestion_summary(summary: dict) -> None:
    for key in [
        "archive_id",
        "html_file_count",
        "total_bytes",
        "link_count",
        "unique_domain_count",
        "attachment_candidate_count",
        "method_claim_candidate_count",
        "numeric_observation_candidate_count",
        "known_bogus_or_debunked_claim_candidate_count",
        "source_candidate_count",
        "hash_like_candidate_count",
        "warning_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    console.print(f"raw_logs_committed={str(summary.get('raw_logs_committed')).lower()}")
    console.print(f"message_bodies_committed={str(summary.get('message_bodies_committed')).lower()}")
    console.print(f"usernames_committed={str(summary.get('usernames_committed')).lower()}")
    console.print(f"ai_upload_used={str(summary.get('ai_upload_used')).lower()}")
    console.print(f"live_api_used={str(summary.get('live_api_used')).lower()}")
    console.print(f"scrape_used={str(summary.get('scrape_used')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@discord_promote_app.command("promote")
def discord_promote_run(
    ingestion_dir: Path = typer.Option(..., "--ingestion-dir", help="Generated Stage 3N ingestion directory."),
    out_dir: Path = typer.Option(..., "--out-dir", help="Generated Stage 3O promotion output directory."),
    promoted_links_out: Path = typer.Option(..., "--promoted-links-out", help="Committed promoted source links YAML."),
    promoted_methods_out: Path = typer.Option(..., "--promoted-methods-out", help="Committed promoted method claims YAML."),
    promoted_numerics_out: Path = typer.Option(..., "--promoted-numerics-out", help="Committed promoted numeric observations YAML."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Write empty outputs if generated inputs are missing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite non-blocking warnings."),
) -> None:
    """Promote public redacted Discord-discovered links and observations."""
    try:
        summary = promote_discord_sources(
            ingestion_dir=_resolve_output_path(ingestion_dir),
            out_dir=_resolve_output_path(out_dir),
            promoted_links_out=_resolve_output_path(promoted_links_out),
            promoted_methods_out=_resolve_output_path(promoted_methods_out),
            promoted_numerics_out=_resolve_output_path(promoted_numerics_out),
            allow_missing=allow_missing,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_discord_promotion_summary(summary)


@discord_promote_app.command("validate-promoted")
def discord_promote_validate(
    links: Path = typer.Option(..., "--links", help="Committed promoted public links YAML."),
    methods: Path = typer.Option(..., "--methods", help="Committed promoted method claims YAML."),
    numerics: Path = typer.Option(..., "--numerics", help="Committed promoted numeric observations YAML."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Allow absent or empty promotion files."),
) -> None:
    """Validate committed Stage 3O promoted records."""
    try:
        counts, errors = validate_promoted_records(
            links=_resolve_output_path(links),
            methods=_resolve_output_path(methods),
            numerics=_resolve_output_path(numerics),
            allow_empty=allow_empty,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Discord promotion records OK")


@discord_promote_app.command("summary")
def discord_promote_print_summary(
    out_dir: Path = typer.Option(..., "--out-dir", help="Generated Stage 3O promotion output directory."),
) -> None:
    """Print a concise generated Discord promotion summary."""
    try:
        summary = load_discord_promotion_summary(_resolve_output_path(out_dir))
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_discord_promotion_summary(summary)


def _print_discord_promotion_summary(summary: dict) -> None:
    for key in [
        "run_id",
        "public_links_promoted_count",
        "method_claims_promoted_count",
        "numeric_observations_promoted_count",
        "private_or_unsafe_links_rejected_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    console.print(f"raw_message_bodies_committed={str(summary.get('raw_message_bodies_committed')).lower()}")
    console.print(f"usernames_committed={str(summary.get('usernames_committed')).lower()}")
    console.print(
        f"private_attachment_urls_committed={str(summary.get('private_attachment_urls_committed')).lower()}"
    )
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@discord_review_app.command("build-bundles")
def discord_review_build_bundles(
    ingestion_dir: Path = typer.Option(..., "--ingestion-dir", help="Generated Stage 3N ingestion directory."),
    promotion_dir: Path = typer.Option(..., "--promotion-dir", help="Generated Stage 3O promotion directory."),
    raw_dir: Path = typer.Option(..., "--raw-dir", help="Local ignored Discord HTML archive directory."),
    out_dir: Path = typer.Option(..., "--out-dir", help="Generated Stage 3Q review-bundle output directory."),
    aggregate_out: Path = typer.Option(..., "--aggregate-out", help="Committed aggregate review-bundle YAML."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Write empty outputs if generated inputs are missing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite non-blocking warnings."),
) -> None:
    """Build redacted Discord topic shards and local AI-review indexes."""
    try:
        summary = build_review_bundles(
            ingestion_dir=_resolve_output_path(ingestion_dir),
            promotion_dir=_resolve_output_path(promotion_dir),
            raw_dir=_resolve_output_path(raw_dir),
            out_dir=_resolve_output_path(out_dir),
            aggregate_out=_resolve_output_path(aggregate_out),
            allow_missing=allow_missing,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_discord_review_summary(summary)


@discord_review_app.command("validate-bundles")
def discord_review_validate_bundles(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated Stage 3Q review-bundle directory."),
    aggregate: Path = typer.Option(..., "--aggregate", help="Committed aggregate review-bundle YAML."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Allow missing generated outputs."),
) -> None:
    """Validate generated/aggregate Stage 3Q review-bundle records."""
    try:
        counts, errors = validate_discord_review_bundles(
            results_dir=_resolve_output_path(results_dir),
            aggregate=_resolve_output_path(aggregate),
            allow_missing=allow_missing,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Discord review bundles OK")


@discord_review_app.command("summary")
def discord_review_print_summary(
    results_dir: Path = typer.Option(..., "--results-dir", help="Generated Stage 3Q review-bundle directory."),
    aggregate: Path = typer.Option(..., "--aggregate", help="Committed aggregate review-bundle YAML."),
) -> None:
    """Print a concise generated Discord review-bundle summary."""
    try:
        summary = load_discord_review_summary(
            _resolve_output_path(results_dir),
            _resolve_output_path(aggregate),
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_discord_review_summary(summary)


def _print_discord_review_summary(summary: dict) -> None:
    for key in [
        "bundle_id",
        "html_file_count",
        "redacted_message_count",
        "topic_shard_count",
        "review_lead_count",
        "public_link_count",
        "method_claim_count",
        "numeric_observation_count",
        "visual_observation_count",
        "debunk_count",
    ]:
        console.print(f"{key}={summary.get(key)}")
    console.print(f"raw_logs_committed={str(summary.get('raw_logs_committed')).lower()}")
    console.print(f"raw_message_committed={str(summary.get('raw_message_committed')).lower()}")
    console.print(f"username_committed={str(summary.get('username_committed')).lower()}")
    console.print(f"private_url_committed={str(summary.get('private_url_committed')).lower()}")
    console.print(f"ai_upload_used={str(summary.get('ai_upload_used')).lower()}")
    console.print(f"live_api_used={str(summary.get('live_api_used')).lower()}")
    console.print(f"scrape_used={str(summary.get('scrape_used')).lower()}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")


@discord_leads_app.command("promote")
def discord_leads_promote(
    review_dir: Path = typer.Option(..., "--review-dir", help="Generated Stage 3Q review-bundle directory."),
    stage3o_links: Path = typer.Option(..., "--stage3o-links", help="Committed Stage 3O promoted links YAML."),
    stage3o_methods: Path = typer.Option(..., "--stage3o-methods", help="Committed Stage 3O method claims YAML."),
    stage3o_numerics: Path = typer.Option(..., "--stage3o-numerics", help="Committed Stage 3O numeric observations YAML."),
    source_registry: Path = typer.Option(..., "--source-registry", help="Committed source registry YAML."),
    visual_registry: Path = typer.Option(..., "--visual-registry", help="Committed visual observation registry YAML."),
    cookie_records: Path = typer.Option(..., "--cookie-records", help="Committed cookie/hash records YAML."),
    out_dir: Path = typer.Option(..., "--out-dir", help="Generated Stage 3R audit output directory."),
    promoted_sources_out: Path = typer.Option(..., "--promoted-sources-out", help="Committed promoted sources YAML."),
    promoted_observations_out: Path = typer.Option(..., "--promoted-observations-out", help="Committed promoted observations YAML."),
    negative_controls_out: Path = typer.Option(..., "--negative-controls-out", help="Committed negative controls YAML."),
    audit_summary_out: Path = typer.Option(..., "--audit-summary-out", help="Committed audit summary YAML."),
    allow_missing: bool = typer.Option(False, "--allow-missing", help="Proceed with reduced coverage if generated inputs are missing."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite non-blocking warnings."),
) -> None:
    """Promote corroborated Stage 3Q Discord leads without committing raw Discord content."""
    try:
        summary = promote_discord_leads(
            review_dir=_resolve_output_path(review_dir),
            stage3o_links=_resolve_output_path(stage3o_links),
            stage3o_methods=_resolve_output_path(stage3o_methods),
            stage3o_numerics=_resolve_output_path(stage3o_numerics),
            source_registry=_resolve_output_path(source_registry),
            visual_registry=_resolve_output_path(visual_registry),
            cookie_records=_resolve_output_path(cookie_records),
            out_dir=_resolve_output_path(out_dir),
            promoted_sources_out=_resolve_output_path(promoted_sources_out),
            promoted_observations_out=_resolve_output_path(promoted_observations_out),
            negative_controls_out=_resolve_output_path(negative_controls_out),
            audit_summary_out=_resolve_output_path(audit_summary_out),
            allow_missing=allow_missing,
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_discord_leads_summary(summary)


@discord_leads_app.command("build-manifests")
def discord_leads_build_manifests(
    audit_summary: Path = typer.Option(..., "--audit-summary", help="Committed Stage 3R audit summary YAML."),
    out_dir: Path = typer.Option(..., "--out-dir", help="Committed post-Discord manifest directory."),
    allow_warnings: bool = typer.Option(False, "--allow-warnings", help="Return success despite non-blocking warnings."),
) -> None:
    """Build disabled post-Discord experiment manifests."""
    try:
        summary = build_post_discord_manifests(
            audit_summary=_resolve_output_path(audit_summary),
            out_dir=_resolve_output_path(out_dir),
            allow_warnings=allow_warnings,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    console.print(f"manifest_count={summary.get('manifest_count')}")
    for experiment_id, payload in summary.get("experiments", {}).items():
        console.print(f"{experiment_id}_candidate_count_cap={payload.get('candidate_count_cap')}")
        console.print(f"{experiment_id}_execution_enabled={str(payload.get('execution_enabled')).lower()}")
    console.print(f"output_dir={summary.get('output_dir')}")


@discord_leads_app.command("validate")
def discord_leads_validate(
    promoted_sources: Path = typer.Option(..., "--promoted-sources", help="Committed promoted sources YAML."),
    promoted_observations: Path = typer.Option(..., "--promoted-observations", help="Committed promoted observations YAML."),
    negative_controls: Path = typer.Option(..., "--negative-controls", help="Committed negative controls YAML."),
    manifest_dir: Path = typer.Option(..., "--manifest-dir", help="Committed post-Discord manifest directory."),
    allow_empty: bool = typer.Option(False, "--allow-empty", help="Allow absent or empty promoted records."),
) -> None:
    """Validate Stage 3R promoted records and disabled manifests."""
    try:
        counts, errors = validate_stage3r_outputs(
            promoted_sources=_resolve_output_path(promoted_sources),
            promoted_observations=_resolve_output_path(promoted_observations),
            negative_controls=_resolve_output_path(negative_controls),
            manifest_dir=_resolve_output_path(manifest_dir),
            allow_empty=allow_empty,
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    for key, value in counts.items():
        console.print(f"{key}={value}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(f"[red]{error}[/red]")
    if errors:
        raise typer.Exit(1)
    console.print("Discord lead promotion records OK")


@discord_leads_app.command("summary")
def discord_leads_print_summary(
    audit_summary: Path = typer.Option(..., "--audit-summary", help="Committed Stage 3R audit summary YAML."),
    manifest_dir: Path = typer.Option(..., "--manifest-dir", help="Committed post-Discord manifest directory."),
) -> None:
    """Print Stage 3R promotion and post-Discord manifest summary."""
    try:
        summary = load_discord_lead_summary(
            _resolve_output_path(audit_summary),
            _resolve_output_path(manifest_dir),
        )
    except Exception as error:  # noqa: BLE001 - CLI reports errors consistently.
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(1) from error
    _print_discord_leads_summary(summary)


def _print_discord_leads_summary(summary: dict) -> None:
    for key in [
        "run_id",
        "stage3q_review_lead_count",
        "stage3q_public_link_count",
        "source_records_promoted",
        "observation_records_promoted",
        "negative_controls_created",
        "duplicate_records_skipped",
        "unsafe_private_records_rejected",
        "manifest_files_present",
    ]:
        if key in summary:
            console.print(f"{key}={summary.get(key)}")
    console.print(f"experiment_execution_performed={str(summary.get('experiment_execution_performed')).lower()}")
    console.print(f"raw_message_committed={str(summary.get('raw_message_committed')).lower()}")
    console.print(f"username_committed={str(summary.get('username_committed')).lower()}")
    console.print(f"private_url_committed={str(summary.get('private_url_committed')).lower()}")
    console.print(f"solve_claim={str(summary.get('solve_claim')).lower()}")
    for key, path in summary.get("output_paths", {}).items():
        console.print(f"{key}={path}")



def register(root_app: typer.Typer) -> None:
    """Register this module's Typer apps on the public root app."""
    root_app.add_typer(discord_ingest_app, name="discord-ingest")
    root_app.add_typer(discord_promote_app, name="discord-promote")
    root_app.add_typer(discord_review_app, name="discord-review")
    root_app.add_typer(discord_leads_app, name="discord-leads")
