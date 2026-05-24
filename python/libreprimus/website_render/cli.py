"""Typer CLI for the Stage 5AM static research website renderer."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .models import (
    GUARDRAIL_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_MANIFEST_PATH,
    PRIVACY_AUDIT_PATH,
    RENDER_INPUTS_PATH,
    RENDER_POLICY_PATH,
    RESULTS_DIR,
    SITE_ROOT,
    SITE_VALIDATION_PATH,
    STAGE5AL_SUMMARY_PATH,
    SUMMARY_PATH,
    UPLOAD_INSTRUCTIONS_PATH,
    WEBSITE_INGEST_DIR,
)
from .stage5am import (
    build_stage5am_guardrail,
    build_stage5am_next_stage_decision,
    build_stage5am_site,
    build_stage5am_summary,
)
from .validation import validate_stage5am, validate_static_site

console = Console()
app = typer.Typer(help="Stage 5AM static website-render commands.", no_args_is_help=True)


@app.command("build-stage5am-site")
def build_stage5am_site_command(
    website_ingest_dir: Path = typer.Option(WEBSITE_INGEST_DIR),
    stage5al_summary: Path = typer.Option(STAGE5AL_SUMMARY_PATH),
    out_root: Path = typer.Option(SITE_ROOT),
    results_dir: Path = typer.Option(RESULTS_DIR),
    render_policy_out: Path = typer.Option(RENDER_POLICY_PATH),
    render_inputs_out: Path = typer.Option(RENDER_INPUTS_PATH),
    manifest_out: Path = typer.Option(OUTPUT_MANIFEST_PATH),
    privacy_audit_out: Path = typer.Option(PRIVACY_AUDIT_PATH),
    upload_instructions_out: Path = typer.Option(UPLOAD_INSTRUCTIONS_PATH),
) -> None:
    result = build_stage5am_site(
        website_ingest_dir=website_ingest_dir,
        stage5al_summary=stage5al_summary,
        out_root=out_root,
        results_dir=results_dir,
        render_policy_out=render_policy_out,
        render_inputs_out=render_inputs_out,
        manifest_out=manifest_out,
        privacy_audit_out=privacy_audit_out,
        upload_instructions_out=upload_instructions_out,
    )
    inputs = result["inputs"]
    manifest = result["manifest"]
    console.print(f"website_export_generated={str(manifest['website_export_generated']).lower()}")
    console.print(f"upload_directory={manifest['upload_directory']}")
    console.print(f"static_pages_generated={manifest['static_pages_generated']}")
    console.print(f"data_json_files_generated={manifest['data_json_files_generated']}")
    console.print(f"source_card_count={inputs['source_card_count']}")


@app.command("validate-stage5am-site")
def validate_stage5am_site_command(
    site_root: Path = typer.Option(SITE_ROOT),
    manifest: Path = typer.Option(OUTPUT_MANIFEST_PATH),
    privacy_audit: Path = typer.Option(PRIVACY_AUDIT_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
    out: Path = typer.Option(SITE_VALIDATION_PATH),
) -> None:
    validation, errors = validate_static_site(
        site_root=site_root,
        manifest_path=manifest,
        privacy_audit_path=privacy_audit,
        results_dir=results_dir,
        out=out,
    )
    console.print(f"static_site_validation_passed={str(validation['static_site_validation_passed']).lower()}")
    console.print(f"validation_error_count={len(errors)}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)


@app.command("build-stage5am-guardrail")
def build_stage5am_guardrail_command(
    site_root: Path = typer.Option(SITE_ROOT),
    manifest: Path = typer.Option(OUTPUT_MANIFEST_PATH),
    privacy_audit: Path = typer.Option(PRIVACY_AUDIT_PATH),
    out: Path = typer.Option(GUARDRAIL_PATH),
) -> None:
    record = build_stage5am_guardrail(site_root=site_root, manifest_path=manifest, privacy_audit_path=privacy_audit, out=out)
    console.print(f"website_export_generated={str(record['website_export_generated']).lower()}")
    console.print(f"raw_bodies_included={str(record['raw_bodies_included']).lower()}")
    console.print(f"private_ids_published={str(record['private_ids_published']).lower()}")


@app.command("build-stage5am-next-stage-decision")
def build_stage5am_next_stage_decision_command(
    site_validation: Path = typer.Option(SITE_VALIDATION_PATH),
    privacy_audit: Path = typer.Option(PRIVACY_AUDIT_PATH),
    out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
) -> None:
    record = build_stage5am_next_stage_decision(site_validation_path=site_validation, privacy_audit_path=privacy_audit, out=out)
    console.print(f"selected_option_id={record['selected_option_id']}")
    console.print(f"deep_research_next_ready={str(record['deep_research_next_ready']).lower()}")


@app.command("build-stage5am-summary")
def build_stage5am_summary_command(
    render_policy: Path = typer.Option(RENDER_POLICY_PATH),
    render_inputs: Path = typer.Option(RENDER_INPUTS_PATH),
    manifest: Path = typer.Option(OUTPUT_MANIFEST_PATH),
    validation: Path = typer.Option(SITE_VALIDATION_PATH),
    privacy_audit: Path = typer.Option(PRIVACY_AUDIT_PATH),
    upload_instructions: Path = typer.Option(UPLOAD_INSTRUCTIONS_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out: Path = typer.Option(SUMMARY_PATH),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    summary = build_stage5am_summary(
        render_policy_path=render_policy,
        render_inputs_path=render_inputs,
        manifest_path=manifest,
        validation_path=validation,
        privacy_audit_path=privacy_audit,
        upload_instructions_path=upload_instructions,
        guardrail_path=guardrail,
        next_stage_decision_path=next_stage_decision,
        out=out,
        results_dir=results_dir,
    )
    console.print(f"stage_id={summary['stage_id']}")
    console.print(f"website_export_generated={str(summary['website_export_generated']).lower()}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")


@app.command("validate-stage5am")
def validate_stage5am_command(
    render_policy: Path = typer.Option(RENDER_POLICY_PATH),
    render_inputs: Path = typer.Option(RENDER_INPUTS_PATH),
    manifest: Path = typer.Option(OUTPUT_MANIFEST_PATH),
    validation: Path = typer.Option(SITE_VALIDATION_PATH),
    privacy_audit: Path = typer.Option(PRIVACY_AUDIT_PATH),
    upload_instructions: Path = typer.Option(UPLOAD_INSTRUCTIONS_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
    site_root: Path = typer.Option(SITE_ROOT),
    results_dir: Path = typer.Option(RESULTS_DIR),
) -> None:
    counts, errors = validate_stage5am(
        render_policy=render_policy,
        render_inputs=render_inputs,
        manifest=manifest,
        validation=validation,
        privacy_audit=privacy_audit,
        upload_instructions=upload_instructions,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
        site_root=site_root,
        results_dir=results_dir,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("website_render_stage5am_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from .loader import read_yaml

    payload = read_yaml(summary)
    for key in [
        "stage_id",
        "status",
        "website_export_root",
        "static_pages_generated",
        "data_json_files_generated",
        "source_card_count",
        "content_record_count",
        "claim_record_count",
        "bundle_count",
        "privacy_audit_passed",
        "recommended_next_stage_title",
    ]:
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="website-render")
