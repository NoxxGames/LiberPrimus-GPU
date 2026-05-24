"""Typer CLI for Stage 5AN Deep Research private content exports."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from .combined_webroot import build_combined_webroot
from .content_pack import build_content_pack
from .hosted_export import build_hosted_export
from .models import (
    COMBINED_SUMMARY_PATH,
    COMBINED_WEBROOT,
    CONSUMPTION_GUIDE_PATH,
    CONTENT_PACK_ROOT,
    DEFAULT_RESEARCH_INPUT_ROOTS,
    DEFAULT_SAFE_LOCAL_SOURCE_ROOTS,
    FILE_SELECTION_SUMMARY_PATH,
    GUARDRAIL_PATH,
    HOSTED_CONTENT_ROOT,
    HOSTED_SUMMARY_PATH,
    INPUTS_PATH,
    MANIFEST_SUMMARY_PATH,
    METADATA_SITE_ROOT,
    NEXT_STAGE_DECISION_PATH,
    POLICY_PATH,
    PUBLICATION_GATE_AUDIT_PATH,
    SUMMARY_PATH,
    UPLOAD_INSTRUCTIONS_PATH,
    WEBSITE_INGEST_DIR,
)
from .stage5an import build_guardrail, build_next_stage_decision, build_summary
from .validation import validate_stage5an

console = Console()
app = typer.Typer(help="Stage 5AN private Deep Research export commands.", no_args_is_help=True)


@app.command("build-stage5an-content-pack")
def build_stage5an_content_pack_command(
    metadata_site_root: Path = typer.Option(METADATA_SITE_ROOT),
    website_ingest_dir: Path = typer.Option(WEBSITE_INGEST_DIR),
    research_input_roots: list[Path] | None = typer.Option(None),
    safe_local_source_roots: list[Path] | None = typer.Option(None),
    out_root: Path = typer.Option(CONTENT_PACK_ROOT),
    policy_out: Path = typer.Option(POLICY_PATH),
    inputs_out: Path = typer.Option(INPUTS_PATH),
    manifest_summary_out: Path = typer.Option(MANIFEST_SUMMARY_PATH),
    file_selection_summary_out: Path = typer.Option(FILE_SELECTION_SUMMARY_PATH),
    publication_gate_audit_out: Path = typer.Option(PUBLICATION_GATE_AUDIT_PATH),
) -> None:
    result = build_content_pack(
        metadata_site_root=metadata_site_root,
        website_ingest_dir=website_ingest_dir,
        research_input_roots=research_input_roots or DEFAULT_RESEARCH_INPUT_ROOTS,
        safe_local_source_roots=safe_local_source_roots or DEFAULT_SAFE_LOCAL_SOURCE_ROOTS,
        out_root=out_root,
        policy_out=policy_out,
        inputs_out=inputs_out,
        manifest_summary_out=manifest_summary_out,
        file_selection_summary_out=file_selection_summary_out,
        publication_gate_audit_out=publication_gate_audit_out,
    )
    summary = result["summary"]
    console.print(f"content_pack_generated={str(summary['content_pack_generated']).lower()}")
    console.print(f"content_pack_file_count={summary['content_pack_file_count']}")
    console.print(f"safe_extracts_generated_count={summary['safe_extracts_generated_count']}")


@app.command("build-stage5an-hosted-export")
def build_stage5an_hosted_export_command(
    content_pack_root: Path = typer.Option(CONTENT_PACK_ROOT),
    metadata_site_root: Path = typer.Option(METADATA_SITE_ROOT),
    out_root: Path = typer.Option(HOSTED_CONTENT_ROOT),
    summary_out: Path = typer.Option(HOSTED_SUMMARY_PATH),
    upload_instructions_out: Path = typer.Option(UPLOAD_INSTRUCTIONS_PATH),
    consumption_guide_out: Path = typer.Option(CONSUMPTION_GUIDE_PATH),
) -> None:
    result = build_hosted_export(
        content_pack_root=content_pack_root,
        metadata_site_root=metadata_site_root,
        out_root=out_root,
        summary_out=summary_out,
        upload_instructions_out=upload_instructions_out,
        consumption_guide_out=consumption_guide_out,
    )
    summary = result["summary"]
    console.print(f"hosted_content_export_generated={str(summary['hosted_content_export_generated']).lower()}")
    console.print(f"hosted_content_file_count={summary['hosted_content_file_count']}")


@app.command("build-stage5an-combined-webroot")
def build_stage5an_combined_webroot_command(
    metadata_site_root: Path = typer.Option(METADATA_SITE_ROOT),
    private_content_root: Path = typer.Option(HOSTED_CONTENT_ROOT),
    out_root: Path = typer.Option(COMBINED_WEBROOT),
    summary_out: Path = typer.Option(COMBINED_SUMMARY_PATH),
) -> None:
    summary = build_combined_webroot(
        metadata_site_root=metadata_site_root,
        private_content_root=private_content_root,
        out_root=out_root,
        summary_out=summary_out,
    )
    console.print(f"combined_webroot_generated={str(summary['combined_webroot_generated']).lower()}")
    console.print(f"combined_webroot_file_count={summary['combined_webroot_file_count']}")


@app.command("build-stage5an-guardrail")
def build_stage5an_guardrail_command(
    content_pack_root: Path = typer.Option(CONTENT_PACK_ROOT),
    hosted_export_root: Path = typer.Option(HOSTED_CONTENT_ROOT),
    combined_webroot: Path = typer.Option(COMBINED_WEBROOT),
    out: Path = typer.Option(GUARDRAIL_PATH),
) -> None:
    record = build_guardrail(
        content_pack_root=content_pack_root,
        hosted_export_root=hosted_export_root,
        combined_webroot=combined_webroot,
        out=out,
    )
    console.print(f"private_content_export_generated={str(record['private_content_export_generated']).lower()}")
    console.print(f"combined_webroot_generated={str(record['combined_webroot_generated']).lower()}")


@app.command("build-stage5an-next-stage-decision")
def build_stage5an_next_stage_decision_command(
    manifest_summary: Path = typer.Option(MANIFEST_SUMMARY_PATH),
    hosted_summary: Path = typer.Option(HOSTED_SUMMARY_PATH),
    combined_summary: Path = typer.Option(COMBINED_SUMMARY_PATH),
    publication_gate_audit: Path = typer.Option(PUBLICATION_GATE_AUDIT_PATH),
    out: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
) -> None:
    record = build_next_stage_decision(
        manifest_summary=manifest_summary,
        hosted_summary=hosted_summary,
        combined_summary=combined_summary,
        publication_gate_audit=publication_gate_audit,
        out=out,
    )
    console.print(f"selected_option_id={record['selected_option_id']}")
    console.print(f"deep_research_next_ready={str(record['deep_research_next_ready']).lower()}")


@app.command("build-stage5an-summary")
def build_stage5an_summary_command(
    policy: Path = typer.Option(POLICY_PATH),
    inputs: Path = typer.Option(INPUTS_PATH),
    manifest_summary: Path = typer.Option(MANIFEST_SUMMARY_PATH),
    hosted_summary: Path = typer.Option(HOSTED_SUMMARY_PATH),
    combined_summary: Path = typer.Option(COMBINED_SUMMARY_PATH),
    file_selection_summary: Path = typer.Option(FILE_SELECTION_SUMMARY_PATH),
    publication_gate_audit: Path = typer.Option(PUBLICATION_GATE_AUDIT_PATH),
    upload_instructions: Path = typer.Option(UPLOAD_INSTRUCTIONS_PATH),
    consumption_guide: Path = typer.Option(CONSUMPTION_GUIDE_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    out: Path = typer.Option(SUMMARY_PATH),
) -> None:
    summary = build_summary(
        policy=policy,
        inputs=inputs,
        manifest_summary=manifest_summary,
        hosted_summary=hosted_summary,
        combined_summary=combined_summary,
        file_selection_summary=file_selection_summary,
        publication_gate_audit=publication_gate_audit,
        upload_instructions=upload_instructions,
        consumption_guide=consumption_guide,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        out=out,
    )
    console.print(f"stage_id={summary['stage_id']}")
    console.print(f"recommended_next_stage_title={summary['recommended_next_stage_title']}")


@app.command("validate-stage5an")
def validate_stage5an_command(
    content_pack_root: Path = typer.Option(CONTENT_PACK_ROOT),
    hosted_export_root: Path = typer.Option(HOSTED_CONTENT_ROOT),
    combined_webroot: Path = typer.Option(COMBINED_WEBROOT),
    policy: Path = typer.Option(POLICY_PATH),
    inputs: Path = typer.Option(INPUTS_PATH),
    manifest_summary: Path = typer.Option(MANIFEST_SUMMARY_PATH),
    hosted_summary: Path = typer.Option(HOSTED_SUMMARY_PATH),
    combined_summary: Path = typer.Option(COMBINED_SUMMARY_PATH),
    file_selection_summary: Path = typer.Option(FILE_SELECTION_SUMMARY_PATH),
    publication_gate_audit: Path = typer.Option(PUBLICATION_GATE_AUDIT_PATH),
    upload_instructions: Path = typer.Option(UPLOAD_INSTRUCTIONS_PATH),
    consumption_guide: Path = typer.Option(CONSUMPTION_GUIDE_PATH),
    guardrail: Path = typer.Option(GUARDRAIL_PATH),
    next_stage_decision: Path = typer.Option(NEXT_STAGE_DECISION_PATH),
    summary: Path = typer.Option(SUMMARY_PATH),
) -> None:
    counts, errors = validate_stage5an(
        content_pack_root=content_pack_root,
        hosted_export_root=hosted_export_root,
        combined_webroot=combined_webroot,
        policy=policy,
        inputs=inputs,
        manifest_summary=manifest_summary,
        hosted_summary=hosted_summary,
        combined_summary=combined_summary,
        file_selection_summary=file_selection_summary,
        publication_gate_audit=publication_gate_audit,
        upload_instructions=upload_instructions,
        consumption_guide=consumption_guide,
        guardrail=guardrail,
        next_stage_decision=next_stage_decision,
        summary=summary,
    )
    for key, value in counts.items():
        console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")
    for error in errors:
        console.print(error)
    if errors:
        raise typer.Exit(1)
    console.print("deep_research_export_stage5an_valid=true")


@app.command("summary")
def summary_command(summary: Path = typer.Option(SUMMARY_PATH)) -> None:
    from .inputs import read_yaml

    payload = read_yaml(summary)
    for key in [
        "stage_id",
        "status",
        "content_pack_file_count",
        "hosted_content_file_count",
        "included_bundle_count",
        "included_source_count",
        "included_claim_count",
        "safe_extracts_generated_count",
        "recommended_next_stage_title",
    ]:
        console.print(f"{key}={payload.get(key)}")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="deep-research-export")
